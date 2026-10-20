"""Synthetic retained source input; pure preparation, never capture certification."""
from __future__ import annotations

import base64
import hashlib
import struct
import zlib

from runtime_protocol.timeline_commit_validation import digest, validate_commit_value

RUNTIME = "2c4ac180c2220bdad966bc01e95ad230e99ce26a"
AGENT = "d8749a9ce12a699672faf3ad96b4e4cbea9245c2"
APP = "cee35da4b1ed653db50dd9d5c26693fab00f04ad"


def image_bytes():
    # Same synthetic 16x16 RGB(240,240,240) PNG as the measured MAIN cap case.
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress((b"\x00" + bytes([240, 240, 240]) * 16) * 16))
            + chunk(b"IEND", b""))


def build_fixture(project_id="project-demo", timeline_id="timeline-1"):
    image = image_bytes()
    bare = hashlib.sha256(image).hexdigest()
    media_id = "sha256:" + bare
    track = {"id": "picture", "kind": "visual", "label": "Picture", "fit": "cover"}
    internal = {"timeline_id": timeline_id, "revision_id": "image-internal", "payload": {
        "tracks": [track], "clips": [{"id": "image", "clipType": "image", "asset": "image",
            "track": "picture", "at": 0, "hold": 5, "effects": [{"fade_out": 1}]}],
        "registry": {"assets": {"image": {"media_id": media_id, "content_sha256": bare,
            "type": "image", "resolution": "16x16"}}}}}
    shot = {"shot_id": "image-shot", "revision_id": "image-shot-revision",
        "internal_timeline_revision_id": internal["revision_id"], "payload": {
            "name": "Image cap analog", "text_bindings": [],
            "internal_timeline_revision_id": internal["revision_id"]}}
    parent = {"revision_id": "image-cap-parent", "payload": {
        "config": {"tracks": [track], "clips": [], "output": {"fps": 30,
            "resolution": "1920x1080", "file": "output.mp4"},
            "theme_overrides": {"visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}}},
        "registry": {"assets": {}}, "clips": [], "occurrences": [{
            "occurrence_id": "image-occurrence", "shot_id": shot["shot_id"],
            "shot_revision_id": shot["revision_id"], "placement": {"start_ms": 0, "track": "picture"},
            "track": "picture", "duration_ms": 4000, "source_offset": 0, "speed": 1,
            "gain": 1, "muted": False, "transform": {}, "provenance": {}}]}}
    for image_record in (parent, shot, internal):
        image_record["content_digest"] = digest(image_record["payload"])
    document = {"schema_version": 1, "project_id": project_id, "timeline_id": timeline_id,
        "parent_revision": parent, "shot_revisions": [shot], "internal_timeline_revisions": [internal],
        "dependency_manifest": {
            "shots": [{k: shot[k] for k in ("shot_id", "revision_id", "internal_timeline_revision_id", "content_digest")}],
            "internal_timelines": [{k: internal[k] for k in ("timeline_id", "revision_id", "content_digest")}],
            "media": [{"media_id": media_id, "content_digest": media_id}], "documents": []}}
    validate_commit_value(document, "CanonicalDocument")
    return {"setup": "synthetic initial retained source; NOT an edit-writer or capture qualification",
        "canonical_document": document, "document_digest": digest(document),
        "media": [{"object_id": media_id, "digest": media_id, "size": len(image),
            "media_type": "image/png", "original_name": "image-cap.png",
            "bytes_base64": base64.b64encode(image).decode()}]}


def restore_request(document, head):
    """Existing S2 request; the live server must generate the acceptance and ref."""
    parent = document["parent_revision"]
    request = {"api_version": 1, "project_id": document["project_id"], "timeline_id": document["timeline_id"],
        "base_revision_id": head["revision_id"], "base_publication_id": head["publication_id"],
        "commands": [{"schema_version": 1, "op": "timeline.restore", "version": "1", "select": None,
            "args": {"revision_id": parent["revision_id"], "content_digest": parent["content_digest"]}}]}
    validate_commit_value(request, "CommitRequest")
    return request
