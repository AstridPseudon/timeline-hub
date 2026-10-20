"""D09 witness for frame-cache source identity and cached scene rows.

This is deliberately a pure cache/projection test.  It does not invoke a
renderer, Root, source preparation, or scene-query process.
"""
from __future__ import annotations

import copy

from astrid.packs.rendering.actions.timeline_visualize.composed_frame import (
    FrameCaptureCache,
    frame_cache_key,
)


def _snapshot() -> dict:
    return {
        "config": {
            "tracks": [{"id": "picture", "kind": "visual"}],
            "clips": [{"id": "compiled:clip", "track": "picture", "at": 0, "hold": 1}],
        },
        "registry": {
            "assets": {
                "component:image": {
                    "object_id": "object:image",
                    "digest": "sha256:" + "a" * 64,
                },
            },
        },
        "fps_rational": [30000, 1001],
        "duration_frames": 120,
        "resolved_theme": {
            "id": "theme:current",
            "visual": {"canvas": {"width": 1920, "height": 1080, "fps": [30000, 1001]}},
        },
        "metadata": {
            "capture_authority": {
                "timeline_id": "timeline:one",
                "parent_revision_id": "revision:canonical-a",
            },
            "capture_identity": "sha256:" + "b" * 64,
            "working_copy": {
                "candidate_digest": "sha256:" + "c" * 64,
                "publication_digest": "sha256:" + "d" * 64,
            },
            "scene_clips": {
                "compiled:clip": {
                    "address": "c08.title",
                    "source_clip_id": "source:title",
                    "occurrence_id": "occurrence:a",
                },
            },
        },
    }


def _key(snapshot, monkeypatch):
    # Isolate the snapshot contract from this checkout's changing source tree.
    monkeypatch.setattr(
        "astrid.packs.rendering.actions.timeline_visualize.composed_frame.renderer_environment_identity",
        lambda: "stable-renderer-environment",
    )
    return frame_cache_key(snapshot, 24, [320, 180])


def test_d09_cache_key_binds_retained_source_and_root_inputs(monkeypatch):
    cases = {
        "canonical revision": ("metadata", "capture_authority", "parent_revision_id", "revision:canonical-b"),
        "candidate": ("metadata", "working_copy", "candidate_digest", "sha256:" + "e" * 64),
        "compiled id map": ("metadata", "scene_clips", "compiled:clip", {
            "address": "c08.body",
            "source_clip_id": "source:title",
            "occurrence_id": "occurrence:a",
        }),
        "root profile": ("resolved_theme", "visual", "canvas", {
            "width": 1280, "height": 720, "fps": [30000, 1001],
        }),
        "component asset digest": ("registry", "assets", "component:image", {
            "object_id": "object:image",
            "digest": "sha256:" + "f" * 64,
        }),
        "source hash": ("metadata", "capture_identity", None, "sha256:" + "1" * 64),
    }

    for name, (first, second, leaf, value) in cases.items():
        changed = copy.deepcopy(_snapshot())
        if leaf is None:
            changed[first][second] = value
        else:
            changed[first][second][leaf] = value
        assert _key(changed, monkeypatch) != _key(_snapshot(), monkeypatch), name


def test_d09_same_source_key_ignores_only_ephemeral_attempt_location(monkeypatch):
    first = _snapshot()
    second = copy.deepcopy(first)
    first["metadata"]["asset_integrity"] = {
        "component:image": "/tmp/astrid-attempt-one/managed-objects/object:image",
    }
    second["metadata"]["asset_integrity"] = {
        "component:image": "/tmp/astrid-attempt-two/managed-objects/object:image",
    }
    assert _key(first, monkeypatch) == _key(second, monkeypatch)


def test_d09_png_cache_has_no_source_binding_or_public_rows(tmp_path, monkeypatch):
    snapshot = _snapshot()
    key = _key(snapshot, monkeypatch)
    cache = FrameCaptureCache(tmp_path / "cache")
    cache.write(key, b"PNG bytes")

    assert cache.read(key) == b"PNG bytes"
    assert sorted(path.name for path in cache.root.iterdir()) == [f"{key}.png"]
    # A cache hit can identify bytes by key only; no retained scene rows or
    # source identity are available from the cache entry itself.
    assert not any(path.suffix != ".png" for path in cache.root.iterdir())
