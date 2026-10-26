"""Saved-head timeline export planning and streaming ``.astrid`` writer."""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote, unquote
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk.client import SCHEMA_DIGEST
from astrid.sdk.pagination import paged_rows
from astrid.version import ASTRID_VERSION

__all__ = ["export_plan", "export_timeline", "inventory_elements"]

_HEX = re.compile(r"^[0-9a-f]{64}$")
_OBJECT_URL = re.compile(r"^https?://(?:127\.0\.0\.1|localhost|\[::1\])(?::\d+)?/(?:api/runtime/)?v1/objects/([^/?#]+)(?:[?#].*)?$")
_DEFAULT_MEDIA = {"media", "video", "audio", "image", "shot", "text", "solid", "group"}
_KIND_MAP = {"effects": "effect", "effect": "effect", "animations": "animation", "animation": "animation", "transitions": "transition", "transition": "transition"}


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if hasattr(value, "__dataclass_fields__"):
        from dataclasses import asdict
        return _plain(asdict(value))
    return value


def _data(result: Any, what: str) -> Mapping[str, Any]:
    if hasattr(result, "ok") and not result.ok:
        raise ValueError(f"cannot export timeline: {getattr(result, 'error', None)}")
    value = _plain(getattr(result, "data", result))
    if isinstance(value, Mapping) and isinstance(value.get("data"), Mapping):
        value = value["data"]
    if not isinstance(value, Mapping):
        raise ValueError(f"Runtime returned no {what}")
    return value


def _strip_machine_paths(value: Any, *, key: str = "") -> Any:
    """Remove workstation-specific source/slot paths and normalize object URLs."""
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for raw_key, child in value.items():
            child_key = str(raw_key)
            if child_key.lower() == "source" and isinstance(child, str) and (
                Path(child).is_absolute() or child.startswith("file://") or re.match(r"^[A-Za-z]:[\\/]", child)
            ):
                continue
            if child_key == "media" and isinstance(child, str) and (
                Path(child).is_absolute() or child.startswith("file://") or re.match(r"^[A-Za-z]:[\\/]", child)
            ):
                continue
            out[child_key] = _strip_machine_paths(child, key=child_key)
        return out
    if isinstance(value, list):
        return [_strip_machine_paths(item, key=key) for item in value]
    if isinstance(value, str):
        match = _OBJECT_URL.match(value)
        if match:
            object_id = unquote(match.group(1))
            return object_id if object_id.startswith("sha256:") else "sha256:" + object_id
    return value


def _descriptor_for(ref: Mapping[str, Any], *, catalog: Mapping[tuple[str, str, str], Mapping[str, Any]]) -> dict[str, Any] | None:
    kind_raw = str(ref.get("kind") or "effect").lower()
    kind = _KIND_MAP.get(kind_raw)
    element_id = ref.get("id")
    pack_id = ref.get("packId") or ref.get("pack_id")
    revision = ref.get("revision")
    if not isinstance(element_id, str) or not element_id:
        return None
    if pack_id:
        return {"packId": str(pack_id), "kind": kind or kind_raw, "id": element_id,
                "revision": revision, "pinned": bool(revision)}
    if kind is None:
        kind = "effect"
    found = catalog.get((kind, element_id, "")) or catalog.get((kind, element_id, "*"))
    if found:
        return {"packId": str(found.get("packId") or ""), "kind": kind, "id": element_id,
                "revision": str(revision or found.get("revision") or ""), "pinned": bool(revision)}
    return {"packId": "", "kind": kind, "id": element_id,
            "revision": str(revision or ""), "pinned": bool(revision)}


def _catalog_descriptors(elements: Any = None) -> dict[tuple[str, str, str], Mapping[str, Any]]:
    if elements is None:
        from astrid.core.element.catalog import list_element_descriptors
        rows = list(list_element_descriptors())
    elif isinstance(elements, Mapping):
        rows = list(elements.values())
    else:
        rows = list(elements or [])
    result: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        kind = _KIND_MAP.get(str(row.get("kind") or "").lower(), str(row.get("kind") or ""))
        element_id = row.get("id")
        pack_id = row.get("packId") or row.get("pack_id") or ""
        if isinstance(element_id, str):
            result[(kind, element_id, "")] = row
            result[(kind, element_id, str(pack_id))] = row
            result[(kind, element_id, "*")] = row
    return result


def inventory_elements(timeline_bundle: Mapping[str, Any], *, elements: Any = None) -> list[dict[str, Any]]:
    """Inventory every effect-like clip/reference/pin in parent and child timelines."""
    catalog = _catalog_descriptors(elements)
    found: dict[tuple[str, str, str], dict[str, Any]] = {}

    def add(ref: Mapping[str, Any]) -> None:
        descriptor = _descriptor_for(ref, catalog=catalog)
        if descriptor is None:
            return
        key = (descriptor["packId"], descriptor["kind"], descriptor["id"])
        old = found.get(key)
        if old is None:
            found[key] = descriptor
        elif descriptor.get("pinned") and not old.get("pinned"):
            found[key] = descriptor

    def visit_clip(clip: Mapping[str, Any]) -> None:
        raw_ref = clip.get("elementRef") or clip.get("element_ref")
        if isinstance(raw_ref, Mapping):
            add(raw_ref)
        clip_type = clip.get("clipType")
        if isinstance(clip_type, str) and clip_type not in _DEFAULT_MEDIA and not (
            isinstance(raw_ref, Mapping) and raw_ref.get("id") == clip_type
        ):
            # clipType is itself the element identity for legacy/unpinned clips.
            add({"kind": "effect", "id": clip_type})
        for field in ("entrance", "exit", "continuous"):
            animation = clip.get(field)
            if isinstance(animation, Mapping):
                identity = animation.get("id") or animation.get("type")
                if isinstance(identity, str):
                    add({**animation, "kind": "animation", "id": identity})
                for item in animation.values():
                    if isinstance(item, Mapping) and isinstance(item.get("id"), str):
                        add({**item, "kind": "animation"})
            elif isinstance(animation, str) and animation:
                add({"kind": "animation", "id": animation})
        animations = clip.get("animations")
        if isinstance(animations, list):
            for item in animations:
                if isinstance(item, Mapping):
                    identity = item.get("id") or item.get("type")
                    if isinstance(identity, str):
                        add({**item, "kind": "animation", "id": identity})
                elif isinstance(item, str):
                    add({"kind": "animation", "id": item})
        transition = clip.get("transition")
        if isinstance(transition, Mapping):
            identity = transition.get("id") or transition.get("type")
            if isinstance(identity, str):
                add({**transition, "kind": "transition", "id": identity})
        elif isinstance(transition, str) and transition:
            add({"kind": "transition", "id": transition})

    def walk(value: Any) -> None:
        if isinstance(value, Mapping):
            if "clipType" in value or "elementRef" in value or "element_ref" in value:
                visit_clip(value)
            for field in ("entrance", "exit", "continuous", "animations", "transition"):
                if field in value and not any(key in value for key in ("clipType", "elementRef", "element_ref")):
                    visit_clip({field: value[field]})
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(timeline_bundle)
    return sorted(found.values(), key=lambda row: (row["packId"], row["kind"], row["id"]))


def _transcript_refs(bundle: Mapping[str, Any]) -> set[str]:
    config = (bundle.get("parent") or {}).get("config") or {}
    bundle_config = config.get("bundle") if isinstance(config, Mapping) else None
    refs = bundle_config.get("transcriptReferences") if isinstance(bundle_config, Mapping) else None
    associations = refs.get("associations") if isinstance(refs, Mapping) else None
    return {str(row["documentId"]) for row in (associations or [])
            if isinstance(row, Mapping) and isinstance(row.get("documentId"), str)}


def _text_binding_media(bundle: Mapping[str, Any]) -> set[str]:
    """Return immutable UTF-8 text objects pinned by saved shot bindings."""
    result: set[str] = set()
    shots = bundle.get("shots")
    if not isinstance(shots, Mapping):
        return result
    for shot in shots.values():
        payload = shot.get("payload") if isinstance(shot, Mapping) else None
        bindings = payload.get("text_bindings") if isinstance(payload, Mapping) else None
        for binding in bindings if isinstance(bindings, list) else []:
            if not isinstance(binding, Mapping):
                continue
            media_id = binding.get("media_id") or binding.get("mediaId")
            if isinstance(media_id, str) and media_id:
                result.add(media_id if media_id.startswith("sha256:") else "sha256:" + media_id)
    return result


def _resolve_project(client: Any, project: str) -> str:
    result = client.projects.show(project)
    data = _plain(getattr(result, "data", result))
    if hasattr(result, "ok") and not result.ok:
        raise ValueError(f"cannot resolve project {project!r}: {result.error}")
    if not isinstance(data, Mapping):
        raise ValueError(f"project {project!r} is unavailable")
    project_id = data.get("project_id") or data.get("id")
    if not isinstance(project_id, str) or not project_id:
        raise ValueError(f"project {project!r} has no Runtime identity")
    return project_id


def _transport(client: Any) -> Any:
    remote = getattr(client, "_remote", None)
    transport = getattr(remote, "_transport", None)
    if transport is None:
        transport = getattr(getattr(client, "timelines", None), "_client", None)
    if transport is None:
        raise ValueError("timeline export requires an Astrid Runtime client")
    return transport


def _saved_head_bundle(client: Any, project: str, timeline: str) -> tuple[Mapping[str, Any], str, str]:
    """Read the saved head closure through the GET-only revision API."""
    project_id = _resolve_project(client, project)
    transport = _transport(client)
    timeline_rows = paged_rows(transport.list_timelines, project_id, limit=50)
    if timeline_rows is None:
        raise ValueError("Runtime could not list project timelines")
    row = next((item for item in timeline_rows if isinstance(item, Mapping) and
                timeline in {str(item.get("timeline_id") or ""), str(item.get("id") or ""),
                             str(item.get("name") or ""), str(item.get("slug") or "")}), None)
    timeline_id = str(row.get("timeline_id") or row.get("id")) if row else timeline
    head_result = transport.get_project_timeline(project_id, timeline_id)
    head_row = _data(head_result, "timeline head")
    head = head_row.get("head_revision_id") or head_row.get("parent_revision_id")
    if not isinstance(head, str) or not head:
        raise ValueError(f"timeline {timeline!r} has no saved parent-composition head")
    parent = _data(transport.get_project_parent_composition_revision(project_id, timeline_id, head), "saved parent revision")
    if str(parent.get("revision_id") or parent.get("parent_revision_id") or "") != head:
        raise ValueError("Runtime returned a parent revision that does not match the saved head")
    payload = parent.get("payload")
    occurrences = payload.get("occurrences") if isinstance(payload, Mapping) else None
    if not isinstance(occurrences, list):
        raise ValueError("saved parent revision has no occurrence list")
    shots: dict[str, Mapping[str, Any]] = {}
    internals: dict[str, Mapping[str, Any]] = {}
    for occurrence in occurrences:
        if not isinstance(occurrence, Mapping):
            raise ValueError("saved parent occurrence is not an object")
        shot_id = occurrence.get("shot_id")
        shot_revision = occurrence.get("shot_revision_id") or occurrence.get("revision_id")
        if not isinstance(shot_id, str) or not isinstance(shot_revision, str):
            raise ValueError("saved parent occurrence has no pinned shot revision")
        if shot_revision not in shots:
            shot = _data(transport.get_project_shot_revision(project_id, shot_id, shot_revision), "saved shot revision")
            if str(shot.get("project_id") or project_id) != project_id or str(shot.get("revision_id") or "") != shot_revision:
                raise ValueError("Runtime returned a shot revision that does not match the saved pin")
            shots[shot_revision] = shot
        shot = shots[shot_revision]
        shot_payload = shot.get("payload")
        internal_revision = shot.get("internal_timeline_revision_id")
        if not isinstance(internal_revision, str) and isinstance(shot_payload, Mapping):
            internal_revision = shot_payload.get("internal_timeline_revision_id")
        if not isinstance(internal_revision, str) or not internal_revision:
            raise ValueError("saved shot revision has no pinned internal timeline revision")
        if internal_revision not in internals:
            internal = _data(transport.get_project_timeline_revision(project_id, timeline_id, internal_revision), "saved internal timeline revision")
            if str(internal.get("project_id") or project_id) != project_id or str(internal.get("revision_id") or "") != internal_revision:
                raise ValueError("Runtime returned an internal timeline revision that does not match the saved pin")
            internals[internal_revision] = internal
    return open_authoring_bundle(parent, shot_revisions=list(shots.values()), internal_timeline_revisions=list(internals.values())), project_id, timeline_id


def export_plan(client: Any, project: str, timeline: str) -> dict[str, Any]:
    """Build metadata and exact media closure for the saved current head."""
    bundle, export_project_id, timeline_id = _saved_head_bundle(client, project, timeline)
    bundle = _plain(bundle)
    compilation = compile_authoring_candidate(bundle)
    elements = inventory_elements(bundle)
    custom = [item for item in elements if item["packId"].startswith("project_")]
    if custom:
        raise ValueError("This timeline uses custom effect " + ", ".join(item["id"] for item in custom) + " from a project pack; custom effects can't travel yet.")
    media_rows = list(compilation.publication["dependency_manifest"]["media"])
    # Runtime publication dependencies cover playable media, while immutable
    # shot text bindings are separate project-owned objects required at commit.
    known_media = {str(row.get("media_id") or row.get("content_digest") or "")
                   for row in media_rows if isinstance(row, Mapping)}
    known_media |= {item if item.startswith("sha256:") else "sha256:" + item for item in list(known_media)}
    for media_id in sorted(_text_binding_media(bundle) - known_media):
        media_rows.append({"media_id": media_id})
    media: list[dict[str, Any]] = []
    object_rows = paged_rows(_transport(client).list_project_objects, export_project_id, limit=100)
    if object_rows is None:
        raise ValueError("Runtime could not list project media metadata")
    object_index = {
        str(row.get("digest") or row.get("object_id") or "").removeprefix("sha256:"): row
        for row in object_rows if isinstance(row, Mapping)
    }
    for row in media_rows:
        digest = str(row.get("media_id") or row.get("content_digest") or "").removeprefix("sha256:")
        if not _HEX.fullmatch(digest):
            raise ValueError(f"compiler returned invalid media identity {digest!r}")
        metadata = object_index.get(digest, {})
        size = metadata.get("size")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ValueError(f"Runtime did not return valid object metadata for media sha256:{digest}")
        media_type = metadata.get("media_type") or metadata.get("mime_type") or "application/octet-stream"
        original_name = str(metadata.get("original_name") or metadata.get("filename") or metadata.get("name") or digest)
        original_name = original_name.replace("\\", "/").rsplit("/", 1)[-1] or digest
        media.append({"sha256": digest, "size": size, "media_type": str(media_type), "original_name": str(original_name)})

    project_id = export_project_id
    rows = paged_rows(_transport(client).list_timelines, project_id, limit=50)
    if rows is None:
        raise ValueError("Runtime could not list project timelines")
    row = next((item for item in rows if isinstance(item, Mapping) and str(item.get("timeline_id") or item.get("id")) == timeline_id), {})
    name = str(row.get("name") or row.get("slug") or timeline_id)
    transcript_docs: dict[str, dict[str, Any]] = {}
    refs = _transcript_refs(bundle)
    docs_result = client.documents.list(project=project_id, kind="media.transcript", limit=100)
    if hasattr(docs_result, "ok") and not docs_result.ok:
        raise ValueError(f"cannot list transcripts: {docs_result.error}")
    doc_rows = _plain(getattr(docs_result, "data", docs_result))
    closure = {"sha256:" + item["sha256"] for item in media}
    for doc in doc_rows if isinstance(doc_rows, list) else []:
        if not isinstance(doc, Mapping) or doc.get("kind") != "media.transcript":
            continue
        content = doc.get("content")
        if not isinstance(content, Mapping) or content.get("media_id") not in closure:
            continue
        document_id = str(doc.get("document_id") or doc.get("id") or "")
        digest = str(content.get("media_id")).removeprefix("sha256:")
        source = str(content.get("source_id") or "source")
        safe_source = quote(source, safe="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-") or "source"
        entry = f"transcripts/{digest}.{safe_source}.json"
        transcript_docs[entry] = {"document_id": document_id, "kind": "media.transcript", "content": _plain(content)}
    missing_refs = refs - {row["document_id"] for row in transcript_docs.values()}
    if missing_refs:
        raise ValueError("timeline references transcript document(s) that could not be exported: " + ", ".join(sorted(missing_refs)))

    clean_bundle = _strip_machine_paths(bundle)
    manifest = {
        "format": "astrid.timeline/1",
        "name": name,
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "astrid": {"version": ASTRID_VERSION, "runtime_schema_digest": SCHEMA_DIGEST},
        "theme": str(((bundle.get("parent") or {}).get("config") or {}).get("theme") or ""),
        "media": media,
        "elements": elements,
        "transcripts": sorted(transcript_docs),
    }
    return {"manifest": manifest, "timeline": clean_bundle, "transcripts": transcript_docs, "media": media}


def _write_object_stream(client: Any, object_id: str, output: Any, expected_size: int, expected_digest: str) -> None:
    generated = _transport(client)._generated
    digest = hashlib.sha256()
    total = 0

    def reader(response: Any) -> bytes:
        nonlocal total
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
            digest.update(chunk)
            total += len(chunk)
        return b""

    try:
        generated._request("GET", "/v1/objects/" + quote(object_id, safe=""), expected=(200,), response_reader=reader)
    except Exception as exc:
        raise ValueError(f"missing or unreadable media object {object_id}: {exc}") from exc
    if total != expected_size:
        raise ValueError(f"media object {object_id} size mismatch: expected {expected_size}, received {total}")
    actual = digest.hexdigest()
    if actual != expected_digest:
        raise ValueError(f"media object {object_id} digest mismatch: expected {expected_digest}, received {actual}")


def export_timeline(client: Any, project: str, timeline: str, out_path: str | os.PathLike[str]) -> dict[str, Any]:
    """Write stored ZIP64 entries using bounded response chunks and atomic replace."""
    plan = export_plan(client, project, timeline)
    destination = Path(out_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    os.close(fd)
    total_bytes = 0
    try:
        with ZipFile(temp_name, "w", compression=ZIP_STORED, allowZip64=True) as archive:
            for name, value in (("manifest.json", plan["manifest"]), ("timeline.json", plan["timeline"])):
                body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
                archive.writestr(name, body, compress_type=ZIP_STORED)
            for name, value in sorted(plan["transcripts"].items()):
                body = json.dumps(value["content"], ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
                archive.writestr(name, body, compress_type=ZIP_STORED)
            for item in plan["media"]:
                digest = item["sha256"]
                object_id = "sha256:" + digest
                info = ZipInfo(f"media/{digest}")
                info.compress_type = ZIP_STORED
                entry = archive.open(info, "w", force_zip64=True)
                try:
                    _write_object_stream(client, object_id, entry, item["size"], digest)
                except Exception as exc:
                    raise ValueError(f"cannot export media {item.get('original_name') or object_id}: {exc}") from exc
                finally:
                    entry.close()
                total_bytes += item["size"]
        os.replace(temp_name, destination)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return {"path": str(destination), "name": plan["manifest"]["name"], "media_count": len(plan["media"]),
            "media_bytes": total_bytes, "archive_bytes": destination.stat().st_size}
