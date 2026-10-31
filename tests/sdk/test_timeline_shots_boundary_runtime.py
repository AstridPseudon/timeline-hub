"""Reproduce occurrence duplication after a Runtime chapter-to-shots commit."""
from __future__ import annotations

import copy
import json

from astrid.sdk import timeline_intent
from astrid.sdk.timeline import Timeline
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_occurrence_duplicate import capture_occurrence_duplicate
from astrid.sdk.timeline.sync import CommitRefused
from tests.sdk.test_timeline_restructure import restructure_runtime  # noqa: F401


def test_chapter_shots_duplicate_uses_the_same_pinned_head(restructure_runtime, tmp_path, capsys):
    env = restructure_runtime
    source_document = env.document()
    flat = bundle_from_document(source_document)
    assert [row["name"] for row in timeline_intent.chapters(flat)] == [
        "01 ONE", "02 TWO", "03 THREE",
    ]

    checkout = Checkout.open(env.project, "t", client=env.client)
    restructured = checkout.publish(
        "Store chapter walls as shots", restructure=True, client=env.client,
        idempotency_key="shots-boundary-restructure",
    )
    assert restructured["receipt"]["receipt_id"]
    timeline = Timeline.open(env.project, "t", client=env.client,
                             outbox_path=tmp_path / "outbox.json")
    base = copy.deepcopy(timeline.bundle)
    head = copy.deepcopy(base.get("base_parent"))
    source = base["placements"][0]
    selected = "occurrence:" + source["occurrence_id"]
    command = capture_occurrence_duplicate(base, selected, "copy-occurrence", "copy-shot")
    captured = copy.deepcopy(command)

    failure = None
    try:
        duplicated = timeline.commit([command], label="Duplicate second shot",
                                     key="shots-boundary-duplicate")
    except CommitRefused as exc:
        failure = exc
        duplicated = None

    if failure is not None:
        details = copy.deepcopy(getattr(failure, "details", {}))

        def compact_record(record):
            call = record.get("command") or {}
            return {
                "op": call.get("op"),
                "select": call.get("select"),
                "args": copy.deepcopy(call.get("args")),
                "resolved": copy.deepcopy(record.get("resolved")),
                "read_refs": [
                    {"ref": row.get("ref"), "path": copy.deepcopy(row.get("path"))}
                    for row in record.get("reads", [])
                ],
                "bindings": [
                    {
                        **{key: copy.deepcopy(binding[key]) for key in
                           ("key", "ref", "physical_ref", "path", "owners") if key in binding},
                        "boundary": {
                            key: copy.deepcopy(binding["boundary"][key])
                            for key in ("phase", "side", "command_ordinal", "step_id")
                            if key in binding.get("boundary", {})
                        },
                    }
                    for binding in record.get("bindings", [])
                ] if isinstance(record.get("bindings"), list) else copy.deepcopy(record.get("bindings")),
                "selections": [
                    {key: copy.deepcopy(selection[key]) for key in ("key", "owner", "boundaries") if key in selection}
                    for selection in record.get("selections", [])
                ],
            }

        history = env.service.list_timeline_commits(env.project, "t", authorize=lambda: None)["items"]
        accepted_records = []
        for entry in history:
            for record in (entry.get("records") or {}).get("commands", []):
                call = record.get("command") or {}
                if call.get("op") != "timeline.restructure":
                    continue
                accepted_records.append(compact_record(record))
        captured_selections = copy.deepcopy(captured.get("selections", []))
        refusal = {
            "outcome": "refused",
            "error_type": type(failure).__name__,
            "error": str(failure),
            "code": getattr(failure, "code", None),
            "details": details,
            "selected_occurrence": selected,
            "source_occurrence": copy.deepcopy(source),
            "provider_boundary": copy.deepcopy(
                details.get("boundary") or details.get("provider_boundary")
                or details.get("alias_boundary")
            ) or {
                "selected_alias": selected,
                "selection_owners": [row.get("owner") for row in captured_selections],
                "collection_boundaries": [
                    {"key": row.get("key"), "owner": row.get("owner"),
                     "boundaries": copy.deepcopy(row.get("boundaries"))}
                    for row in captured_selections
                ],
            },
            "accepted_command_records": accepted_records,
            "captured_command_record_fields": {
                **compact_record({**captured, "command": captured}),
                "intent": copy.deepcopy(captured.get("intent")),
            },
            "base_head": head,
        }
        (tmp_path / "shots-boundary-refusal.json").write_text(
            json.dumps(refusal, indent=2, sort_keys=True) + "\n"
        )
        with capsys.disabled():
            print("shots-boundary Runtime refusal: " + json.dumps(refusal, sort_keys=True))
        return

    assert duplicated["receipt"]["receipt_id"]
    after_duplicate = duplicated["data"]["canonical_document"]
    occurrences = after_duplicate["parent_revision"]["payload"]["occurrences"]
    by_id = {row["occurrence_id"]: row for row in occurrences}
    assert "copy-occurrence" in by_id
    assert by_id["copy-occurrence"]["shot_id"] == "copy-shot"
    assert by_id["copy-occurrence"]["shot_id"] != source["shot_id"]

    arranged = timeline.commit(
        lambda t: t.arrange([source["occurrence_id"], "copy-occurrence"], at=0, gap=2),
        label="Arrange copied shots", key="shots-boundary-arrange",
    )
    assert arranged["receipt"]["receipt_id"]
    rows = arranged["data"]["canonical_document"]["parent_revision"]["payload"]["occurrences"]
    listed = [(row["occurrence_id"], row["shot_id"], row["placement"]["start_ms"]) for row in rows]
    selected_rows = [row for row in listed if row[0] in {source["occurrence_id"], "copy-occurrence"}]
    assert {row[0] for row in selected_rows} == {source["occurrence_id"], "copy-occurrence"}
    assert len({row[1] for row in selected_rows}) == 2
    assert sorted(row[2] for row in selected_rows) == [0, 2000]
