"""Exact project-pack source selections carried by immutable render inputs."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping

from astrid.core.element import project_packs
from astrid.core.element.registry import ElementRegistry, load_default_registry, load_pack_elements

CARRIER = "astrid_project_element_snapshots"
PACK_ROOTS_ENV = "ASTRID_RENDER_PACK_ROOTS"
REGISTRY_ROOT_ENV = "ASTRID_RENDER_REGISTRY_ROOT"


def selections(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    app = config.get("app")
    return app.get(CARRIER, []) if isinstance(app, Mapping) else []


def selection_key(reference: Mapping[str, str]) -> tuple[str, str, str, str]:
    return reference["packId"], reference["kind"], reference["id"], reference["revision"]


def render_key(selection: Mapping[str, Any]) -> str:
    ref = selection["reference"]
    scope = project_packs._json_digest([
        selection["realm"], selection["project"], ref["packId"], ref["kind"], ref["id"],
    ]).removeprefix("sha256:")
    return f"pinned_{scope}_{ref['revision'].removeprefix('sha256:')}"


def _project_references(config: Mapping[str, Any]) -> dict[tuple[str, str, str, str], dict[str, str]]:
    from astrid.core.foundation.paths import REPO_ROOT
    from astrid.core.pack.discovery import discover_pack_metadata

    refs = {}
    for clip in config.get("clips", []):
        ref = clip.get("elementRef") if isinstance(clip, Mapping) else None
        if (isinstance(ref, Mapping)
                and all(isinstance(ref.get(key), str) and ref[key]
                        for key in ("packId", "kind", "id", "revision"))
                and not ref["revision"].startswith("draft-")):
            refs[selection_key(ref)] = dict(ref)
    if not refs:
        return refs
    installed_owners = {row.id for row in discover_pack_metadata(project_root=REPO_ROOT)
                        if row.source_kind in {"source", "local"}}
    return {key: ref for key, ref in refs.items() if ref["packId"] not in installed_owners}


def require_project_snapshots(config: Mapping[str, Any]) -> None:
    selected = {selection_key(row["reference"]) for row in selections(config)}
    for key in _project_references(config):
        if key not in selected:
            raise ValueError(f"Project element snapshot missing for {key[0]}/{key[1]}/{key[2]}@{key[3]}")


def resolve_project_elements(config: Mapping[str, Any], *, project: str, client: Any) -> dict[str, Any]:
    """Fetch each exact admission once; never use authoring files or the catalog.

    The mutable document locates a retained admission, selected by the complete
    element ref. The scoped verified-document/object ports authenticate its
    portable source, which then travels with this render's frozen inputs.
    """
    result = copy.deepcopy(dict(config))
    app = result.get("app")
    if isinstance(app, dict):
        app.pop(CARRIER, None)  # Authored data cannot nominate executable inputs.
    refs = _project_references(result)
    if not refs:
        return result

    realm = client.documents._identity()["realm_id"]
    reader = getattr(client.documents, "_client", client)
    documents = {}
    objects = {}
    selected = []
    for ref in refs.values():
        label = f"{ref['packId']}/{ref['kind']}/{ref['id']}@{ref['revision']}"
        owner = ref["packId"]
        if owner not in documents:
            _, row = project_packs._read_document(client, realm, project)
            if row is None or row["content"]["pack_id"] != owner:
                _, row = project_packs._read_document(client, realm, project, owner)
            if row is None or row["content"]["pack_id"] != owner:
                raise ValueError(f"Project element snapshot missing for {label}")
            pin = {"document_id": row["document_id"], "version": row["version"],
                   "content_digest": project_packs._json_digest(row["content"])}
            try:
                documents[owner] = reader.get_project_verified_document(project, pin)
            except Exception as exc:
                raise ValueError(f"Project element snapshot missing for {label}: {exc}") from exc
        verified = documents[owner]
        admissions = verified["document"]["content"]["admissions"]
        matches = [row for row in admissions if all(row.get(key) == ref[key]
                   for key in ("id", "kind", "revision"))]
        if len(matches) != 1 or not matches[0].get("snapshot_object"):
            raise ValueError(f"Project element snapshot missing for {label}; re-admit pack")
        object_id = matches[0]["snapshot_object"]["object_id"]
        if (owner, object_id) not in objects:
            try:
                objects[owner, object_id] = reader.get_project_verified_document_object(
                    project, verified["pin"], object_id)
            except Exception as exc:
                raise ValueError(f"Project element snapshot missing for {label}: {exc}") from exc
        snapshot = objects[owner, object_id]
        try:
            descriptor = project_packs.admitted_element_snapshot_descriptor(
                realm, project, ref, verified, snapshot)
        except ValueError as exc:
            raise ValueError(f"Project element snapshot digest mismatch or invalid source for {label}: {exc}") from exc
        selected.append({"realm": realm, "project": project, "reference": ref,
                         "verified": verified, "snapshot": snapshot, "descriptor": descriptor})
    result.setdefault("app", {})[CARRIER] = selected
    return result


def stage_project_elements(
    config: Mapping[str, Any], root: Path, *, registry: ElementRegistry | None = None,
) -> tuple[ElementRegistry, list[dict[str, str]]]:
    """Recheck frozen bytes and stage separate, unmodified pack source trees."""
    require_project_snapshots(config)
    registry = registry if registry is not None else load_default_registry()
    roots = []
    for selected in selections(config):
        ref = selected["reference"]
        descriptor = project_packs.admitted_element_snapshot_descriptor(
            selected["realm"], selected["project"], ref,
            selected["verified"], selected["snapshot"])
        snapshot = selected["snapshot"]
        files, _ = project_packs._snapshot_object_resources(
            {key: snapshot[key] for key in ("object_id", "digest", "size", "media_type")},
            project_packs._decode_base64(snapshot["bytes_base64"]))
        key = render_key(selected)
        pack_root = root / key / ref["packId"]
        pack_root.mkdir(parents=True, exist_ok=True, mode=0o700)
        for name, data in files.items():
            path = pack_root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        # Discover each closure independently: two revisions deliberately have
        # the same authored pack ID, which ordinary discovery deduplicates.
        elements = load_pack_elements(project_root=root, extra_pack_roots=(str(pack_root),))
        exact = [item for item in elements if item.id == ref["id"]
                 and item.kind == ref["kind"] + "s" and item.root.is_relative_to(pack_root)]
        if len(exact) != 1:
            raise ValueError(f"Staged project element snapshot is unavailable: {ref}")
        element = exact[0]
        metadata = {**element.metadata, "render_revision": descriptor["revision"],
                    "render_key": key, "render_import_scope": f"pack-{key}-elements"}
        registry.register(replace(element, metadata=metadata))
        roots.append({"root": str(pack_root), "scope": f"pack-{key}-elements"})
    return registry, roots
