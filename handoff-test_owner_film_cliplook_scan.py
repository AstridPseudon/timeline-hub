"""Portable synthetic smokes for the owner-film delivery scanner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SCANNER_PATH = Path(__file__).resolve().with_name("owner_film_cliplook_scan.py")
if not SCANNER_PATH.is_file():
    SCANNER_PATH = Path(__file__).resolve().parents[1] / "owner_film_cliplook_scan.py"
SPEC = importlib.util.spec_from_file_location("owner_film_cliplook_scan", SCANNER_PATH)
assert SPEC is not None and SPEC.loader is not None
SCANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCANNER)


def _clip(
    clip_id: str,
    at: float,
    track: str,
    *,
    asset: str,
    element: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": clip_id,
        "at": at,
        "hold": 2,
        "track": track,
        "asset": asset,
        "clipType": "media",
        "opaqueSecret": "must-not-appear-in-output",
        "credential": "SYNTHETIC_CREDENTIAL_MARKER",
    }
    if element is not None:
        result["elementRef"] = {"id": element, "kind": "effect"}
    result.update(extra)
    return result


def synthetic_document(*, dependency_manifest: bool = True) -> dict[str, Any]:
    clips = [
        _clip(
            "element-a",
            1,
            "picture",
            asset="video-a",
            element="am-footage",
            opacity=0.8,
            cropLeft=0.1,
            speed=1.5,
            entrance={"type": "fade", "duration": 0.5},
        ),
        _clip(
            "element-b",
            2,
            "picture",
            asset="video-b",
            element="am-footage",
            transition={"id": "cross-fade", "durationFrames": 6},
            exit={"type": "fade", "duration": 0.5},
        ),
        _clip(
            "element-unknown",
            3.5,
            "picture",
            asset="video-b",
            element="not-registered",
            opacity=0.5,
        ),
        _clip(
            "audio-curved",
            5,
            "audio",
            asset="audio-a",
            clipType="audio",
            params={"fadeIn": 0.5, "fadeInCurve": "equal-power"},
        ),
        _clip(
            "audio-default-curve",
            8,
            "audio",
            asset="audio-b",
            clipType="audio",
            params={"fadeOut": 0.25},
        ),
        _clip(
            "audio-unknown",
            11,
            "audio-unresolved",
            asset="missing-audio",
            clipType="audio",
            params={"fadeOut": 0.25, "fadeOutCurve": "not-a-registered-curve"},
        ),
        _clip(
            "media-look",
            14,
            "picture",
            asset="video-a",
            entrance={"type": "fade", "duration": 0.5},
        ),
    ]
    payload: dict[str, Any] = {
        "config": {
            "output": {"fps": {"numerator": 30000, "denominator": 1001}},
            "tracks": [
                {"id": "picture", "role": "picture"},
                {"id": "audio", "role": "music"},
                {"id": "audio-unresolved"},
            ],
        },
        "clips": clips,
        "registry": {
            "assets": {
                "video-a": {"type": "video"},
                "video-b": {"type": "video"},
                "audio-a": {"type": "audio"},
                "audio-b": {"type": "audio"},
            }
        },
        "occurrences": [
            {
                "occurrence_id": "occurrence-1",
                "shot_id": "shot-1",
                "shot_revision_id": "shot-revision-1",
                "at_ms": 12000,
                "duration_ms": 2000,
            }
        ],
    }
    document: dict[str, Any] = {
        "schema_version": 1,
        "project_id": "synthetic-project",
        "timeline_id": "synthetic-timeline",
        "parent_revision": {
            "project_id": "synthetic-project",
            "timeline_id": "synthetic-timeline",
            "revision_id": "synthetic-revision",
            "payload": payload,
        },
        "shot_revisions": [
            {
                "shot_id": "shot-1",
                "revision_id": "shot-revision-1",
                "internal_timeline_revision_id": "internal-revision-1",
            }
        ],
        "internal_timeline_revisions": [
            {
                "revision_id": "internal-revision-1",
                "payload": {
                    "tracks": [{"id": "shot-audio", "role": "music"}],
                    "clips": [
                        {
                            "id": "child-audio",
                            "at": 0,
                            "hold": 1,
                            "track": "shot-audio",
                            "asset": "child-audio-asset",
                            "clipType": "audio",
                            "params": {"fadeIn": 0.25},
                        }
                    ],
                    "registry": {"assets": {"child-audio-asset": {"type": "audio"}}},
                },
            }
        ],
    }
    if dependency_manifest:
        document["dependency_manifest"] = {"synthetic": True}
    return document


def _findings(result: dict[str, Any], category: str) -> list[dict[str, Any]]:
    return [row for row in result["findings"] if row["semantic_category"] == category]


def test_three_categories_rational_fps_pins_and_known_unknown(agent_root: Path) -> None:
    result = SCANNER.scan(synthetic_document(), agent_root=agent_root)

    assert result["status"] == "complete", result
    assert result["fps_rational"] == [30000, 1001]
    assert result["clean_claim"] is False
    assert {row["semantic_category"] for row in result["findings"]} == {
        "curve_honoured",
        "element_clip_look_overlap",
        "continuous_audio_fade",
    }
    curved = next(row for row in _findings(result, "curve_honoured") if row["clip_id"] == "audio-curved")
    assert curved["knowledge"] == "known"
    assert "params.fadeInCurve" in curved["properties"]
    assert curved["interval_frames"] == [150, 210]
    child = next(
        row for row in _findings(result, "continuous_audio_fade") if row["clip_id"] == "occurrence-1:child-audio"
    )
    assert child["occurrence_id"] == "occurrence-1"
    assert child["shot_id"] == "shot-1"
    assert child["shot_revision_id"] == "shot-revision-1"
    assert child["internal_timeline_revision_id"] == "internal-revision-1"
    unknown = next(row for row in _findings(result, "curve_honoured") if row["clip_id"] == "audio-unknown")
    assert unknown["knowledge"] == "unknown"
    assert not any(row["clip_id"] == "audio-default-curve" for row in _findings(result, "curve_honoured"))
    transition = next(row for row in result["transition_boundaries"] if row["clip_id"] == "element-b")
    assert transition["transition_id"] == transition["transition_type"] == "cross-fade"
    assert transition["semantics"] == "incoming"
    assert transition["interval_frames"] == [60, 120]
    assert "transition_conversion" in result["not_covered"]


def test_defaults_overlap_scope_and_opaque_data_are_bounded(agent_root: Path) -> None:
    result = SCANNER.scan(synthetic_document(), agent_root=agent_root)
    assert not any(row["clip_id"] == "audio-default-curve" for row in _findings(result, "curve_honoured"))
    overlaps = [row for row in _findings(result, "element_clip_look_overlap") if len(row["clip_ids"]) == 2]
    assert {tuple(row["clip_ids"]) for row in overlaps} == {
        ("element-a", "element-b"),
        ("element-b", "element-unknown"),
    }
    assert next(row for row in overlaps if row["clip_ids"] == ["element-b", "element-unknown"])["knowledge"] == "unknown"
    element_a = next(row for row in _findings(result, "element_clip_look_overlap") if row["clip_ids"] == ["element-a"])
    assert {"crop_left", "speed"} <= set(element_a["properties"])
    media = next(row for row in result["media_look_inventory"] if row["clip_id"] == "media-look")
    assert media["properties"] == ["entrance"]
    assert media["knowledge"] == "known"
    assert "projected.config.tracks[1].role" in next(
        row for row in _findings(result, "continuous_audio_fade") if row["clip_id"] == "audio-curved"
    )["source_paths"]
    encoded = json.dumps(result)
    assert "must-not-appear-in-output" not in encoded
    assert "SYNTHETIC_CREDENTIAL_MARKER" not in encoded
    assert "opaqueSecret" not in encoded
    assert '"raw"' not in encoded


def test_incomplete_closure_is_not_clean(agent_root: Path) -> None:
    result = SCANNER.scan(synthetic_document(dependency_manifest=False), agent_root=agent_root)
    assert result["status"] == "incomplete"
    assert "dependency_manifest is absent" in result["closure_errors"]
    assert result["clean_claim"] is False


def test_projector_and_scanner_preserve_explicit_optional_asset_clear(agent_root: Path) -> None:
    document = synthetic_document()
    parent = document["parent_revision"]
    parent["payload"]["clips"][0]["asset"] = None
    authored_before_scan = json.dumps(document, sort_keys=True)
    api = SCANNER._agent_api(agent_root)

    projected = api["project_runtime_parent_composition"](
        parent,
        shot_revisions=document["shot_revisions"],
        internal_timeline_revisions=document["internal_timeline_revisions"],
    )

    assert projected.config["clips"][0]["asset"] is None
    result = SCANNER.scan(document, agent_root=agent_root)
    assert result["status"] == "complete", result
    assert all("asset reference must be a string" not in error for error in result["closure_errors"])
    assert json.dumps(document, sort_keys=True) == authored_before_scan


def test_element_overlap_includes_cross_track_half_open_intervals(agent_root: Path) -> None:
    document = synthetic_document()
    payload = document["parent_revision"]["payload"]
    payload["config"]["tracks"].append({"id": "other-picture", "role": "picture"})
    payload["clips"][2]["track"] = "other-picture"
    result = SCANNER.scan(document, agent_root=agent_root)
    overlaps = [row for row in _findings(result, "element_clip_look_overlap") if len(row["clip_ids"]) == 2]
    assert {tuple(row["clip_ids"]) for row in overlaps} == {
        ("element-a", "element-b"),
        ("element-b", "element-unknown"),
    }


def test_cross_track_boundary_is_half_open_no_overlap(agent_root: Path) -> None:
    document = synthetic_document()
    payload = document["parent_revision"]["payload"]
    payload["config"]["tracks"].append({"id": "other-picture", "role": "picture"})
    payload["clips"][2]["track"] = "other-picture"
    payload["clips"][2]["at"] = 4
    result = SCANNER.scan(document, agent_root=agent_root)
    overlaps = [row for row in _findings(result, "element_clip_look_overlap") if len(row["clip_ids"]) == 2]
    assert {tuple(row["clip_ids"]) for row in overlaps} == {("element-a", "element-b")}


def test_pair_without_a_declared_look_is_omitted(agent_root: Path) -> None:
    document = synthetic_document()
    clips = document["parent_revision"]["payload"]["clips"]
    clips.extend(
        [
            _clip("plain-a", 17, "picture", asset="video-a", element="am-footage"),
            _clip("plain-b", 18, "picture", asset="video-b", element="am-footage"),
        ]
    )
    result = SCANNER.scan(document, agent_root=agent_root)
    assert not any(
        set(row["clip_ids"]) == {"plain-a", "plain-b"}
        for row in _findings(result, "element_clip_look_overlap")
    )


def test_missing_and_unprojectable_closure_fail_closed(agent_root: Path) -> None:
    result = SCANNER.scan({"project_id": "synthetic-project"}, agent_root=agent_root)
    assert result["status"] == "incomplete"
    assert result["findings"] == []
    assert result["clean_claim"] is False


def test_malformed_scope_reference_is_not_copied_to_closure_error() -> None:
    marker = "SYNTHETIC_PRIVATE_CAPTION_MARKER"
    result = SCANNER.scan({"project_id": {"caption": marker}}, agent_root="/unused")

    encoded = json.dumps(result)
    assert result["status"] == "incomplete"
    assert "project_id" not in result
    assert marker not in encoded
    assert "project_id reference must be a string" in result["closure_errors"]
    assert "missing top-level keys: timeline_id, parent_revision, shot_revisions, internal_timeline_revisions" in result[
        "closure_errors"
    ]


@pytest.mark.parametrize(
    "mutate",
    [
        lambda document: document.__setitem__("project_id", {"nested": "SYNTHETIC_PRIVATE_NESTED_MARKER"}),
        lambda document: document.__setitem__("project_id", None),
        lambda document: document.__setitem__("timeline_id", ["SYNTHETIC_PRIVATE_NESTED_MARKER"]),
        lambda document: document["parent_revision"].__setitem__("revision_id", True),
        lambda document: document["parent_revision"]["payload"]["occurrences"][0].__setitem__(
            "occurrence_id", {"nested": "SYNTHETIC_PRIVATE_NESTED_MARKER"}
        ),
        lambda document: document["parent_revision"]["payload"]["clips"][0].__setitem__(
            "id", {"nested": "SYNTHETIC_PRIVATE_NESTED_MARKER"}
        ),
    ],
)
def test_malformed_nested_references_are_redacted_from_projectable_results(
    mutate: Any, agent_root: Path
) -> None:
    document = synthetic_document()
    mutate(document)

    result = SCANNER.scan(document, agent_root=agent_root)

    encoded = json.dumps(result)
    assert result["status"] == "incomplete"
    assert "SYNTHETIC_PRIVATE_NESTED_MARKER" not in encoded
    for field in ("project_id", "timeline_id", "revision_id"):
        if field in result:
            assert isinstance(result[field], str)


def test_malformed_finding_source_path_is_omitted_and_unknown() -> None:
    errors: list[str] = []
    result = SCANNER._finding(
        category="curve_honoured",
        known=True,
        properties=[],
        source_paths=[],
        refs={"source_path": {"nested": "SYNTHETIC_PRIVATE_NESTED_MARKER"}},
        errors=errors,
    )

    assert "source_path" not in result
    assert result["knowledge"] == "unknown"
    assert "SYNTHETIC_PRIVATE_NESTED_MARKER" not in json.dumps(result)
    assert errors == ["source_path reference must be a string"]


@pytest.mark.parametrize(
    ("curve", "knowledge"),
    [(None, None), ("linear", None), ("equal-power", "known"), ("not-a-registered-curve", "unknown")],
)
def test_curve_requires_explicit_non_linear_value(
    agent_root: Path, curve: str | None, knowledge: str | None
) -> None:
    document = synthetic_document()
    clip = document["parent_revision"]["payload"]["clips"][3]
    clip["id"] = "name-that-looks-like-a-curve"
    clip["params"] = {"fadeIn": 0.5}
    if curve is not None:
        clip["params"]["fadeInCurve"] = curve
    result = SCANNER.scan(document, agent_root=agent_root)
    rows = [row for row in _findings(result, "curve_honoured") if row["clip_id"] == clip["id"]]
    assert len(rows) == (0 if knowledge is None else 1)
    if knowledge is not None:
        assert rows[0]["knowledge"] == knowledge
    assert len([row for row in _findings(result, "continuous_audio_fade") if row["clip_id"] == clip["id"]]) == 1


def test_duplicate_internal_positions_keep_occurrence_identity() -> None:
    document = synthetic_document()
    duplicate = json.loads(json.dumps(document["internal_timeline_revisions"][0]))
    duplicate["payload"]["clips"][0]["id"] = "duplicate-child"
    document["internal_timeline_revisions"].insert(0, duplicate)
    paths = SCANNER._raw_clip_sources(document)
    assert paths["occurrence-1:child-audio"]["source_path"] == (
        "internal_timeline_revisions[1].payload.clips[0]"
    )
    assert paths["occurrence-1:child-audio"]["occurrence_id"] == "occurrence-1"


def test_cli_runs_from_relocated_directory_without_orch_environment(agent_root: Path, tmp_path: Path) -> None:
    input_path = tmp_path / "canonical_document.json"
    output_path = tmp_path / "result.json"
    input_path.write_text(json.dumps(synthetic_document()), encoding="utf-8")
    env = {"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1"}
    completed = subprocess.run(
        [
            sys.executable,
            str(SCANNER_PATH),
            "--input",
            str(input_path),
            "--agent-root",
            str(agent_root),
            "--json-out",
            str(output_path),
        ],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(output_path.read_text(encoding="utf-8"))["fps_rational"] == [30000, 1001]
    assert "owner_film_cliplook_scan.py" not in completed.stderr


def test_cli_rejects_same_path_symlink_and_hardlink_before_writing(agent_root: Path, tmp_path: Path) -> None:
    input_path = tmp_path / "canonical_document.json"
    input_path.write_text(json.dumps(synthetic_document()), encoding="utf-8")
    original_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    original_mtime_ns = input_path.stat().st_mtime_ns

    def rejected(output_path: Path) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCANNER_PATH),
                "--input",
                str(input_path),
                "--agent-root",
                str(agent_root),
                "--json-out",
                str(output_path),
            ],
            cwd=tmp_path,
            env={"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1"},
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode != 0

    rejected(input_path)
    hardlink = tmp_path / "hardlink.json"
    os.link(input_path, hardlink)
    rejected(hardlink)
    symlink = tmp_path / "symlink.json"
    symlink.symlink_to(input_path)
    rejected(symlink)
    assert hashlib.sha256(input_path.read_bytes()).hexdigest() == original_hash
    assert input_path.stat().st_mtime_ns == original_mtime_ns


