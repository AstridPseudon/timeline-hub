"""Capture the real provider candidate rejected after chapter restructure + duplicate."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_occurrence_duplicate import capture_occurrence_duplicate
from astrid.sdk.timeline.sync import CommitRefused
from tests.sdk.test_timeline_restructure import restructure_runtime  # noqa: F401


def _cut_records(bundle):
    records = []
    placements = {row["occurrence_id"]: row for row in bundle.get("placements", [])}
    for shot_id, shot in bundle.get("shots", {}).items():
        for clip in shot.get("internal_timeline", {}).get("clips", []):
            app = clip.get("app", {})
            astrid = app.get("astrid", {}) if isinstance(app, dict) else {}
            cut = astrid.get("cut") if isinstance(astrid, dict) else None
            if cut is None:
                continue
            source = bundle.get("source_mapping", {}).get("shots", {}).get(shot_id, {})
            for occurrence_id, placement in placements.items():
                if placement.get("shot_id") == shot_id:
                    records.append({
                        "cut_id": cut,
                        "occurrence_id": occurrence_id,
                        "shot_id": shot_id,
                        "clip_id": clip.get("id"),
                        "internal_timeline_id": source.get("internal_timeline_id"),
                        "internal_timeline_revision_id": source.get("internal_timeline_revision_id"),
                        "internal_timeline_content_digest": source.get("internal_timeline_content_digest"),
                    })
    return records


def test_restructured_chapter_duplicate_captures_rejected_cut_candidate(
    restructure_runtime, tmp_path, monkeypatch, capsys,
):
    from astrid.sdk.timeline import _commit_timing_validation
    from astrid.sdk.timeline import validation

    env = restructure_runtime
    source = Checkout.open(env.project, "t", client=env.client)
    source.publish("Restructure labeled chapters", client=env.client,
                   idempotency_key="capture-cut-restructure", restructure=True)

    candidate_capture = {}
    validation_view_capture = {}
    original_validate = validation.validate_final_candidate
    original_compile = _commit_timing_validation.compile_timing

    def capture_candidate(candidate, **kwargs):
        candidate_capture["bundle"] = copy.deepcopy(candidate)
        return original_validate(candidate, **kwargs)

    def capture_validation_view(inputs):
        view = inputs.bundle
        validation_view_capture["bundle"] = copy.deepcopy(view)
        return original_compile(inputs)

    monkeypatch.setattr(validation, "validate_final_candidate", capture_candidate)
    monkeypatch.setattr(_commit_timing_validation, "compile_timing", capture_validation_view)

    bundle = bundle_from_document(env.document())
    placement = bundle["placements"][0]
    command = capture_occurrence_duplicate(
        bundle,
        f"occurrence:{placement['occurrence_id']}",
        "copy-occurrence",
        "copy-shot",
    )
    session = timeline.open(env.project, "t", client=env.client,
                            outbox_path=tmp_path / "cut-capture-outbox.json")

    with pytest.raises(CommitRefused) as refused:
        session.commit([command], label="Duplicate chapter occurrence",
                       idempotency_key="capture-cut-duplicate")

    assert type(refused.value) is CommitRefused
    assert refused.value.failure["message"] == "candidate.timing: ambiguous cut identity across occurrences"
    assert "bundle" in candidate_capture
    assert "bundle" in validation_view_capture

    request, key = env.calls[-1]
    selected = request["commands"][-1]
    source_read = next(row for row in selected["reads"] if row["ref"].endswith("/source"))
    report = {
        "selected_command": {
            "op": selected["op"],
            "select": selected["select"],
            "args": copy.deepcopy(selected["args"]),
            "source_read_cut_records": [
                {"clip_id": clip.get("id"),
                 "cut_id": clip.get("app", {}).get("astrid", {}).get("cut")}
                for clip in source_read["state"]["value"]["clips"]
                if clip.get("app", {}).get("astrid", {}).get("cut") is not None
            ],
        },
        "idempotency_key": key,
        "provider_failure": copy.deepcopy(refused.value.failure),
        "candidate_cut_records": _cut_records(candidate_capture["bundle"]),
        "validation_view_cut_records": _cut_records(validation_view_capture["bundle"]),
    }
    with capsys.disabled():
        print("Rejected cut identity capture: " + json.dumps(report, sort_keys=True))
    assert report["selected_command"]["op"] == "occurrence.duplicate"
    assert {record["occurrence_id"] for record in report["candidate_cut_records"]} >= {
        placement["occurrence_id"], "copy-occurrence",
    }
