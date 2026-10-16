"""Explicit registry producer through generated public COMMIT and exact readback.

The Runtime port/storage and scene evaluator are synthetic boundary doubles.
This is not an App hook or installed Runtime acceptance proof.
"""
import copy
import json

import pytest
from test_timeline_graph_commands import closure, opened, port_for  # noqa: F401
from test_timeline_commit import StaleHead
from test_timeline_saved_publish import setup, synthetic_scene_answers  # noqa: F401

from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.identity import retain_cut_reservations
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.saved_intent import read_saved_calls
from astrid.sdk.workspace_client import WorkspaceClientError

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")
ASSET = 'literal.key["quoted"]'
ENTRY = dict(media_id="sha256:" + "a" * 64, type="image/png",
             opaque={"null": None, "literal": {"op": "clear"}}, file="image.png")


def call(entry=None, asset=ASSET):
    return dict(op="timeline.register-asset", select=None,
                args=dict(asset_id=asset, entry=copy.deepcopy(ENTRY if entry is None else entry)))


def test_saved_producer_public_commit_exact_readback_retry_and_one_inverse(setup, monkeypatch):
    draft, runtime = setup
    # This older fixture's generic head uses a literal publication marker.
    # Model its actual accepted publication identity for the history guard.
    original_port = runtime.port
    def port(body):
        value = original_port(body)
        value.head = lambda: dict(revision_id=runtime.current,
            publication_id="pub-0" if runtime.current == "rev-0" else "pub-" + runtime.current,
            updated_at="fixture")
        return value
    monkeypatch.setattr(runtime, "port", port)
    before = draft.document()
    # The real public SDK adapter records explicit intent, never a snapshot diff.
    draft.register_asset(ASSET, ENTRY)
    draft.save(quiet=True)
    recorded = read_saved_calls(Checkout.load(draft.path))
    assert len(recorded) == 1 and recorded[0]["op"] == "timeline.register-asset"
    assert recorded[0]["args"] == call()["args"]
    assert recorded[0]["bindings"] == {} and recorded[0]["created"] == []
    runtime.lose = True
    with pytest.raises(WorkspaceClientError, match="timed out"):
        draft.publish("register", client=runtime.client())
    assert len(runtime.publications) == 1
    accepted = Checkout.load(draft.path).publish("retry", client=runtime.client())
    assert runtime.calls[0][0] == runtime.calls[1][0]
    body = json.loads(runtime.calls[0][0])
    assert body["change"]["commands"] == list(recorded)
    assert accepted["status"] == "accepted"
    assert len(runtime.publications) == 1
    changed = copy.deepcopy(body)
    changed["change"]["commands"][0]["args"]["entry"]["opaque"]["null"] = False
    refused = runtime.client().commit_timeline(changed)
    assert refused["error"]["code"] == "request_id_conflict"
    assert len(runtime.publications) == 1
    closure = runtime.closure(accepted["accepted_revision_id"])
    assert closure["parent_revision"]["payload"]["registry"]["assets"][ASSET] == ENTRY
    assert closure["parent_revision"]["content_digest"] == _digest(closure["parent_revision"]["payload"])
    after = accepted["canonical_document"]
    assert after["parent"]["config"] == before["parent"]["config"]
    inverse = inverse_command(accepted["change"]["commands"], before, after, accepted["accepted_publication_id"])
    undo = copy.deepcopy(body)
    undo.update(request_id="registry-undo", base_revision_id=accepted["accepted_revision_id"],
                base_publication_id=accepted["accepted_publication_id"])
    undo["change"] = dict(commands=[inverse])
    result = runtime.client().commit_timeline(undo)
    assert result["status"] == "accepted", result
    expected = retain_cut_reservations(copy.deepcopy(before))
    assert result["canonical_document"]["parent"] == expected["parent"]
    assert len(result["change"]["commands"]) == 1 and len(runtime.publications) == 2


@pytest.mark.parametrize("registry", [None, {}, {"assets": {}}, {"assets": {ASSET: {**ENTRY, "opaque": None}}, "opaque": None}])
def test_sparse_and_opaque_presence_replay_inverse_and_local_one_undo(closure, registry, tmp_path):
    base = opened(closure)
    if registry is None:
        base["parent"].pop("registry", None)
    else:
        base["parent"]["registry"] = copy.deepcopy(registry)
    tl = Checkout(copy.deepcopy(base))
    tl.save(tmp_path / "registry.json", quiet=True)
    before = tl.document()
    plan = commands.run(tl, call())
    after = tl.document()
    assert after["parent"]["config"] == before["parent"]["config"]
    replay = rebase(plan.calls, before)
    assert not replay.conflicts and replay.document == after
    inverse = inverse_command(plan.calls, before, after, "pub-register")
    restored, _, _ = RuntimeCommitService._apply(after, [inverse])
    assert restored["parent"] == before["parent"]
    tl.undo()
    assert tl.document()["parent"] == before["parent"]
    with pytest.raises(commands.TimelineEditError, match="nothing to undo"):
        tl.undo()


def test_disjoint_rebase_and_whole_entry_conflict(closure):
    base = opened(closure)
    base["parent"]["registry"] = dict(assets={ASSET: copy.deepcopy(ENTRY)}, opaque=None)
    replacement = {**ENTRY, "opaque": {"new": None}}
    tl = Checkout(copy.deepcopy(base))
    plan = commands.run(tl, call(replacement))
    assert len(plan.direct_writes) == 1
    assert plan.direct_writes[0]["before"]["value"] == ENTRY
    assert plan.direct_writes[0]["after"]["value"] == replacement
    head = copy.deepcopy(base)
    head["parent"]["registry"]["assets"]["other"] = copy.deepcopy(ENTRY)
    result = rebase(plan.calls, head)
    assert not result.conflicts and result.document["parent"]["registry"]["assets"]["other"] == ENTRY
    head["parent"]["registry"]["assets"][ASSET]["opaque"].pop("null")
    result = rebase(plan.calls, head)
    assert result.document is None and result.conflicts[0]["kind"] == "same-property"


@pytest.mark.parametrize("during_accept", [False, True])
@pytest.mark.parametrize("overlap", [False, True])
def test_captured_base_moved_head_and_cas_retry(closure, during_accept, overlap):
    closure["parent_revision"]["payload"]["registry"] = dict(assets={})
    closure["parent_revision"]["content_digest"] = _digest(closure["parent_revision"]["payload"])
    head = copy.deepcopy(closure)
    head["parent_revision"]["revision_id"] = "head-1"
    head["parent_revision"]["payload"]["registry"]["assets"][ASSET if overlap else "other"] = {**ENTRY, "opaque": None}
    head["parent_revision"]["content_digest"] = _digest(head["parent_revision"]["payload"])
    body, port = port_for(closure, call())
    reads = []
    def read(rid):
        reads.append(rid)
        return copy.deepcopy(closure if rid == "rev-0" else head)
    port.revision_closure = read
    if during_accept:
        def race(port, prepared):
            port.on_accept = None
            port.current = "head-1"
            raise StaleHead()
        port.on_accept = race
    else:
        port.current = "head-1"
    result = RuntimeCommitService().commit(body, port)
    assert result["base_revision_id"] == "rev-0" and result["rebased_onto"] == "head-1"
    assert reads == ["rev-0", "head-1"]
    if overlap:
        assert result["status"] == "conflict" and port.saved is None
        assert len(port.accepts) == int(during_accept)
    else:
        assert result["status"] == "accepted", result
        assert len(port.accepts) == 1 + int(during_accept)
        assert port.accepts[-1]["expected_head_revision_id"] == "head-1"
        assets = result["canonical_document"]["parent"]["registry"]["assets"]
        assert assets[ASSET] == ENTRY and assets["other"]["opaque"] is None
        if during_accept:
            assert port.accepts[0]["evidence"]["commands"] == port.accepts[1]["evidence"]["commands"]


@pytest.mark.parametrize("version", [0, 1, 2])
def test_supported_integer_versions_are_preserved(closure, version):
    parent = closure["parent_revision"]
    parent["payload"]["config"] = dict(app=dict(astrid=dict(v=version, opaque=None)))
    parent["content_digest"] = _digest(parent["payload"])
    body, port = port_for(closure, call())
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "accepted", result
    assert result["canonical_document"]["parent"]["config"] == parent["payload"]["config"]


@pytest.mark.parametrize("entry", [{}, {"file": "legacy.png"}, {"media_id": None},
    {"media_id": True}, {"media_id": "wrong"}, {**ENTRY, "object_id": "sha256:" + "b" * 64},
    {**ENTRY, "content_sha256": "b" * 64}, {**ENTRY, "local_path": "/tmp/private"}])
def test_absent_invalid_or_disagreeing_source_refuses_atomically(closure, entry):
    body, port = port_for(closure, call(asset="first"), call(entry))
    original = copy.deepcopy(closure)
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "refused", result
    assert not port.accepts and port.saved is None and closure == original


@pytest.mark.parametrize("version", [True, None, "1", 3])
def test_exact_version_refusal(closure, version):
    parent = closure["parent_revision"]
    parent["payload"]["config"] = dict(app=dict(astrid=dict(v=version)))
    parent["content_digest"] = _digest(parent["payload"])
    body, port = port_for(closure, call())
    result = RuntimeCommitService().commit(body, port)
    assert result["error"]["code"] == "unsupported_feature" and not port.accepts


def test_unknown_operation_and_snapshot_stay_refused(closure):
    for value in (dict(op="registry.patch", select=None, args=call()["args"]),
                  {**call(), "select": "occurrence:a"}):
        body, port = port_for(closure, value)
        result = RuntimeCommitService().commit(body, port)
        assert result["status"] == "refused" and not port.accepts
    body, port = port_for(closure)
    body["change"] = dict(document=opened(closure), adapter="app-save")
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "refused" and not port.accepts


@pytest.mark.parametrize("bad", ["project", "timeline", "digest"])
def test_wrong_or_invalid_immutable_base_refuses(closure, bad):
    if bad == "digest":
        closure["parent_revision"]["content_digest"] = "sha256:" + "0" * 64
    else:
        closure["parent_revision"][bad + "_id"] = "wrong"
    body, port = port_for(closure, call())
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "refused" and not port.accepts


def test_exact_entry_no_change_and_dry_run_do_not_create_extra_undo(closure, tmp_path):
    tl = Checkout(opened(closure))
    tl.save(tmp_path / "registry.json", quiet=True)
    before = tl.document()
    preview = commands.run(tl, call(), dry_run=True)
    assert preview.changed and tl.document() == before
    commands.run(tl, call())
    after = tl.document()
    assert not commands.run(tl, call()).changed
    tl.undo()
    assert tl.document()["parent"] == before["parent"]
    tl.redo()
    assert tl.document()["parent"] == after["parent"]
    parent = closure["parent_revision"]
    parent["payload"]["registry"] = dict(assets={ASSET: copy.deepcopy(ENTRY)})
    parent["content_digest"] = _digest(parent["payload"])
    body, port = port_for(closure, call())
    result = RuntimeCommitService().commit(body, port)
    assert result["status"] == "no_change" and port.accepts[0]["publication"] is None
