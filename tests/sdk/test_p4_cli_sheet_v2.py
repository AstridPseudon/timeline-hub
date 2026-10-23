"""P4's real CLI/sheet front door against the joined G3/R2 source.

The generated-client method is the only fake boundary here.  Its acceptance
path still runs the repository command engine and canonical document compiler;
the parser, NativeSheet adapter, emitter seam, and durable outbox are not
stubbed.  This test remains red until the CLI/sheet caller is mounted on G3.
"""
from __future__ import annotations

import hashlib
import json

import pytest

from astrid.packs.timeline import cli
from astrid.sdk import storage_root
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.outbox import request_bytes
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from tests.sdk.test_timeline_commit_provider_document import document_fixture
from tests.sdk.test_timeline_sheet_native import edit_cell
from tests.sdk.test_timeline_sync import connected  # noqa: F401


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The installed apply handler still routes native sheet rows through "
        "cli_native.commit_edit/NativeSheet.apply, not G3 emit_document_commands."
    ),
)
@pytest.mark.usefixtures("connected")
def test_cli_sheet_v2_front_door_preserves_provenance_and_unrelated_fields(
    tmp_path, capsys, monkeypatch, request
):
    """An edited sheet must become one guarded v2 doc.patch commit."""
    fixture = request.getfixturevalue("connected")
    client, generated, path = fixture
    monkeypatch.setattr(storage_root, "resolve_runtime_data_root", lambda: path.parent)
    scope = {"realm_id": "realm", "actor_id": "actor", "project_id": "p", "timeline_id": "t"}
    outbox_path = path.parent / "timeline-outbox" / (
        hashlib.sha256(request_bytes(scope)).hexdigest() + ".json"
    )
    generated.path = outbox_path
    document = document_fixture(shared=False)
    document.update(project_id="p", timeline_id="t")
    document["parent_revision"]["revision_id"] = "r0"
    # Keep the witness's intended CLI value (5 seconds) exact rather than
    # making the native fallback's 30000/1001 frame quantization part of P4.
    document["parent_revision"]["payload"]["config"]["output"]["fps"] = 30
    document["parent_revision"]["content_digest"] = _digest(
        document["parent_revision"]["payload"]
    )
    original = bundle_from_document(document)
    generated.bundles = {"r0": original}
    generated.head = {"revision_id": "r0", "publication_id": "pub0"}

    # The real adapter creates the pinned editable sheet and stores its source
    # bundle in the same durable outbox used by the CLI commit.
    session = TimelineSession.open("p", "t", client=client)
    sheet = NativeSheet.export(session)
    edited = edit_cell(sheet.text, "parent/clip:clip-a", "5")
    sheet_path = tmp_path / "edited.sheet"
    sheet_path.write_text(edited, encoding="utf-8")

    # This is the installed product parser/handler.  No --native flag is
    # supplied; the handler itself chooses the current sheet route.
    parsed = cli.build_parser(client).parse_args([
        "apply", "t", str(sheet_path), "--project", "p", "--json",
        "--idempotency-key", "p4-cli-sheet-v2",
    ])
    assert parsed.native is False
    assert parsed.handler(parsed) == 0
    reply = json.loads(capsys.readouterr().out)
    assert reply["ok"] is True
    assert reply["data"]["status"] == "accepted"

    assert len(generated.calls) == 1
    body = json.loads(generated.calls[0][0])
    assert generated.calls[0][1] == "p4-cli-sheet-v2"

    # The real acceptance path applied exactly the requested edit.  Every
    # unrelated closure field remains byte-for-byte equal to the original.
    accepted = generated.bundles["r1"]
    assert accepted["parent"]["clips"][0]["at"] == 5
    assert accepted["parent"]["clips"][1] == original["parent"]["clips"][1]
    assert accepted["parent"]["config"]["tracks"] == original["parent"]["config"]["tracks"]
    assert accepted["parent"]["config"]["output"] == original["parent"]["config"]["output"]
    assert accepted["parent"].get("registry") == original["parent"].get("registry")
    assert accepted["parent"]["unknown"] == original["parent"]["unknown"]
    assert accepted["shots"] == original["shots"]
    assert accepted["placements"] == original["placements"]

    expected_change = {
        "op": "set",
        "ref": "parent",
        "path": ["clips", "id:clip-a", "at"],
        "before": {"state": "present", "value": 1},
        "value": 5,
    }
    expected_step = {
        "id": "sheet-1",
        "label": "Apply sheet",
        "intent": "",
        "tags": ["sheet"],
        "command_ordinals": [0],
        "patch": [expected_change],
    }

    # Aggregate the contract failures so the red test records the complete
    # seam, rather than hiding the missing step patch behind the first mismatch.
    mismatches = []
    if body.get("api_version") != 1:
        mismatches.append(("api_version", body.get("api_version")))
    if {key: body.get(key) for key in ("project_id", "timeline_id", "base_revision_id",
                                       "base_publication_id")} != {
        "project_id": "p", "timeline_id": "t", "base_revision_id": "r0",
        "base_publication_id": "pub0",
    }:
        mismatches.append(("identity/base", body))
    if body.get("commands") != [{
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": None,
        "args": {"changes": [expected_change]},
    }]:
        mismatches.append(("commands", body.get("commands")))
    if body.get("label") != "Apply sheet":
        mismatches.append(("label", body.get("label")))
    if body.get("steps") != [expected_step]:
        mismatches.append(("steps", body.get("steps")))
    if body.get("merge") != "atomic":
        mismatches.append(("merge", body.get("merge")))
    if body.get("source") != {"via": "sheet"}:
        mismatches.append(("caller", body.get("source")))
    if body.get("dry_run") is not False:
        mismatches.append(("dry_run", body.get("dry_run")))
    if body.get("reads") is not None:
        mismatches.append(("optional request reads", body.get("reads")))

    # The generated transport fixture returns the current accepted envelope;
    # canonical closure/digest/head/receipt/authoritative commands are real
    # fixture fields.  v2 step dependencies/merge_mode and conflict/invalid/
    # preview/history variants are not supplied by this generated boundary yet.
    for field in ("canonical_document", "document_digest", "accepted_revision_id", "commands"):
        if field not in reply["data"]:
            mismatches.append((f"reply.{field}", None))
    if "receipt" not in reply or not reply["receipt"]:
        mismatches.append(("reply.receipt", reply.get("receipt")))

    # Required mutation idempotency is carried by the generated call's header,
    # not overlaid into the wire body or reconstructed in this test.
    assert not mismatches, f"v2 CLI/sheet front-door mismatches: {mismatches}"
