"""CLI -> generated COMMIT -> real semantic provider, with synthetic acceptance.

No installed Runtime, credentials, realm, public film or publication is touched.
"""
from __future__ import annotations

import copy
import json
from types import SimpleNamespace

import pytest
from test_timeline_commit import bundle, restore_fixture, synthetic_scene_answers  # noqa: F401
from test_workspace_commit_adapter import _client

from astrid.packs.timeline import cli_history
from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline import journal, restore_commit, saved_publish
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.revisions import Revision, resolve_revision_record

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


@pytest.fixture
def journey(bundle, monkeypatch, tmp_path):  # noqa: F811 - imported pytest fixture
    original_body, port, closures = restore_fixture(bundle)
    target = closures["opaque-selected"]["parent_revision"]
    rows = [dict(revision_id="rev-0", publication_id="pub-rev-0", is_current_head=True,
                 previous_revision_id="opaque-selected", previous_publication_id="pub-selected"),
            dict(revision_id="opaque-selected", publication_id="pub-selected", is_current_head=False,
                 previous_revision_id=None, previous_publication_id=None,
                 content_digest=target["content_digest"])]
    port.revisions = lambda opts: copy.deepcopy(rows)
    calls, publications = [], []
    service = RuntimeCommitService()
    accept = port.accept
    def accept_image(prepared):
        accepted = accept(prepared)
        publications.append(dict(revision_id=accepted["stored_result"]["accepted_revision_id"],
            publication_id=accepted["stored_result"]["accepted_publication_id"],
            previous_revision_id=prepared["expected_head_revision_id"],
            previous_publication_id=prepared["restore"]["expected_publication_id"],
            restored_from_revision_id=prepared["restore"]["revision_id"],
            message=prepared["label"], provenance=accepted["stored_result"]["provenance"]))
        port.current = accepted["stored_result"]["accepted_revision_id"]
        return accepted
    port.accept = accept_image
    def transport(method, path, headers, payload):
        body = json.loads(payload)
        calls.append((method, path, copy.deepcopy(headers), body, payload))
        port.body = copy.deepcopy(body)
        result = service.commit(body, port)
        return 200, {}, json.dumps(result).encode()
    workspace = _client(transport)
    workspace.get_project_parent_composition_revision = lambda p, t, rid: copy.deepcopy(closures[rid]["parent_revision"])
    def child(kind, rid):
        return copy.deepcopy(next(row for closure in closures.values() for row in closure[kind]
                                  if row["revision_id"] == rid))
    def shot(p, s, rid):
        row = child("shot_revisions", rid)
        internal = child("internal_timeline_revisions", row["internal_timeline_revision_id"])
        row["internal_timeline_id"] = internal["timeline_id"]
        return row
    workspace.get_project_shot_revision = shot
    workspace.get_project_timeline_revision = lambda p, t, rid: child("internal_timeline_revisions", rid)
    class Timelines:
        def resolve_scope(self, p, t):
            assert (p, t) == ("project-name", "timeline-name")
            return DomainResult.success(dict(project_id="p", timeline_id="t"))
        def head_canonical(self, p, t):
            assert (p, t) == ("p", "t")
            return DomainResult.success(port.head())
        def list_parent_composition_revisions(self, p, t, **opts):
            assert (p, t) == ("p", "t")
            return DomainResult.success((copy.deepcopy(rows), None))
        def restore_parent_composition_revision(self, *a, **kw):
            pytest.fail("CLI bypassed semantic COMMIT")
    client = SimpleNamespace(timelines=Timelines(), _remote=SimpleNamespace(_transport=workspace))
    monkeypatch.setattr(journal, "_drafts_root", lambda: tmp_path)
    monkeypatch.setattr(restore_commit, "_authenticate", lambda w: (
        dict(realm_id="synthetic-realm", principal="fixture-publisher"), "synthetic-session"))
    parsed = SimpleNamespace(client=client, project="project-name", ref="timeline-name",
        from_ref="timeline-name@prev", idempotency_key="restore-fixture-key", message="Restore selected cut", json=True)
    return SimpleNamespace(parsed=parsed, port=port, closures=closures, rows=rows, calls=calls,
                           publications=publications, original_body=original_body)


@pytest.mark.parametrize("source", ["timeline-name@prev", "opaque-selected", "opaque"])
def test_cli_named_restore_commit_exact_pins_ancestry_receipt_and_replay(journey, capsys, monkeypatch, source):
    j = journey
    j.parsed.from_ref = source
    original = copy.deepcopy(j.closures)
    assert cli_history.run_restore(j.parsed) == 0
    first = json.loads(capsys.readouterr().out)
    assert first["ok"] and first["idempotency_key"] == "restore-fixture-key"
    method, path, headers, body, payload = j.calls[0]
    assert (method, path) == ("POST", "/astrid/v1/projects/p/timelines/t/commit")
    assert headers["Idempotency-Key"] == body["request_id"] == "restore-fixture-key"
    assert headers["X-Astrid-Session"] == body["session_id"] == "synthetic-session"
    assert body["base_revision_id"] == "rev-0" and body["base_publication_id"] == "pub-rev-0"
    assert body["label"] == "Restore selected cut" and body["source"] == {"via": "cli"}
    assert body["scope"] == dict(target="parent", complete=["clips", "tracks"], projection_version=1)
    assert body["change"]["commands"] == [dict(op="timeline.restore", select=None, resolved=[], version=None,
        args=dict(revision_id="opaque-selected", publication_id="pub-selected",
                  content_digest=original["opaque-selected"]["parent_revision"]["content_digest"]))]
    assert j.port.accepts[0]["restore"] == dict(body["change"]["commands"][0]["args"],
                                                expected_publication_id="pub-rev-0")
    assert j.publications == [dict(revision_id="accepted-fixture", publication_id="publication-fixture",
        previous_revision_id="rev-0", previous_publication_id="pub-rev-0",
        restored_from_revision_id="opaque-selected", message=body["label"],
        provenance=dict(publisher="fixture-publisher", source=dict(via="cli")))]
    assert first["data"] == j.port.saved["result"]
    assert first["data"]["runtime_receipt"]["publisher"] == "fixture-publisher"
    assert {rid: j.closures[rid] for rid in original} == original
    # Recovery must not re-resolve @prev, refresh the head or change session identity.
    monkeypatch.setattr(j.parsed.client.timelines, "head_canonical", lambda *a: pytest.fail("replay read head"))
    monkeypatch.setattr(j.parsed.client.timelines, "list_parent_composition_revisions", lambda *a, **k: pytest.fail("replay reselected history"))
    monkeypatch.setattr(restore_commit, "_authenticate", lambda w: (
        dict(realm_id="synthetic-realm", principal="fixture-publisher"), "new-session"))
    assert cli_history.run_restore(j.parsed) == 0
    assert json.loads(capsys.readouterr().out) == first
    assert j.calls[1][4] == payload and len(j.port.accepts) == len(j.publications) == 1
    log = journal.journal_path("p", "t")
    assert not journal.verify(log)
    records = [json.loads(line) for line in log.read_text().splitlines()]
    assert records[0]["evidence"][0]["body"] == body
    assert records[-1]["evidence"][0]["result"] == first["data"]
    # Normal saved-draft readers still accept all journal rows.
    checkout = SimpleNamespace(bundle=dict(project_id="p", timeline_id="t"), path="/tmp/main.json")
    assert saved_publish.read_rows(checkout, log.read_text()) == []


def test_cli_restore_lost_response_reuses_journaled_envelope(journey, capsys):
    j = journey
    accept = j.port.accept
    def lost(prepared):
        accept(prepared)
        raise TimeoutError("synthetic accepted response lost")
    j.port.accept = lost
    assert cli_history.run_restore(j.parsed) != 0
    failure = json.loads(capsys.readouterr().out)
    assert not failure["ok"] and failure["idempotency_key"] == j.parsed.idempotency_key
    j.port.accept = accept
    assert cli_history.run_restore(j.parsed) == 0
    assert json.loads(capsys.readouterr().out)["data"] == j.port.saved["result"]
    assert j.calls[0][4] == j.calls[1][4] and len(j.port.accepts) == 1


@pytest.mark.parametrize("damage", ["stale-head", "stale-publication", "wrong-project", "wrong-timeline",
                                    "unknown-publication", "digest-mismatch"])
def test_cli_restore_provider_refusals_preserve_public_state(journey, capsys, damage):
    j = journey
    if damage.startswith("stale"):
        head = j.port.head
        j.port.head = lambda: {**head(), ("revision_id" if damage == "stale-head" else "publication_id"): "later"}
        # Caller captures original; provider sees the changed Runtime head.
        j.parsed.client.timelines.head_canonical = lambda *a: DomainResult.success(
            dict(revision_id="rev-0", publication_id="pub-rev-0", updated_at="fixture"))
    elif damage.startswith("wrong"):
        field = "project_id" if damage == "wrong-project" else "timeline_id"
        j.closures["opaque-selected"]["parent_revision"][field] = "other"
    elif damage == "unknown-publication":
        j.port.revisions = lambda opts: []
    else:
        j.rows[1]["content_digest"] = "sha256:" + "0" * 64
    before = copy.deepcopy(j.closures)
    assert cli_history.run_restore(j.parsed) != 0
    result = json.loads(capsys.readouterr().out)
    assert not result["ok"]
    receipt = result["error"]["details"]["receipt"]
    assert receipt["status"] == ("conflict" if damage.startswith("stale") else "refused")
    assert receipt["accepted_revision_id"] is receipt["runtime_receipt"] is None
    assert not j.port.accepts and not j.publications and j.closures == before


@pytest.mark.parametrize("source", ["unknown-revision", "other-timeline@prev"])
def test_cli_restore_unknown_or_cross_timeline_selection_never_dispatches(journey, source):
    journey.parsed.from_ref = source
    with pytest.raises(TimelineEditError):
        cli_history.run_restore(journey.parsed)
    assert not journey.calls and not journey.port.accepts


def test_restore_positional_selection_keeps_exact_republication_event():
    digest = "sha256:" + "1" * 64
    older = Revision("same", "cli", None, None, None, publication_id="older", content_digest=digest)
    head = Revision("same", "cli", None, "same", None, publication_id="head",
                    previous_publication_id="older", is_current_head=True, content_digest=digest)
    store = SimpleNamespace(list=lambda *a, **kw: [head, older])
    assert resolve_revision_record("p", "t", "prev", store=store) == older
    assert resolve_revision_record("p", "t", "same", store=store) == head


def test_restore_key_cannot_change_intent_or_origin(journey, capsys, monkeypatch):
    cli_history.run_restore(journey.parsed)
    capsys.readouterr()
    journey.parsed.from_ref = "opaque-selected"
    with pytest.raises(TimelineEditError, match="different scope, origin or intent"):
        cli_history.run_restore(journey.parsed)
    journey.parsed.from_ref = "timeline-name@prev"
    monkeypatch.setattr(restore_commit, "_authenticate", lambda w: (
        dict(realm_id="other-realm", principal="fixture-publisher"), "synthetic-session"))
    with pytest.raises(TimelineEditError, match="different scope, origin or intent"):
        cli_history.run_restore(journey.parsed)
    assert len(journey.calls) == len(journey.port.accepts) == 1


def test_restore_unverified_response_retains_key_and_pending_request(journey, capsys, monkeypatch):
    journey.parsed.idempotency_key = None
    verify = restore_commit._verify_result
    monkeypatch.setattr(restore_commit, "_verify_result", lambda *a: (_ for _ in ()).throw(
        TimelineEditError("unverified COMMIT receipt")))
    assert cli_history.run_restore(journey.parsed) != 0
    failure = json.loads(capsys.readouterr().out)
    key = failure["idempotency_key"]
    assert key and not failure["ok"] and len(journey.port.accepts) == 1
    log = journal.journal_path("p", "t")
    assert len(log.read_text().splitlines()) == 1  # only the original pending envelope
    journey.parsed.idempotency_key = key
    monkeypatch.setattr(restore_commit, "_verify_result", verify)
    assert cli_history.run_restore(journey.parsed) == 0
    assert json.loads(capsys.readouterr().out)["data"] == journey.port.saved["result"]
    assert len(journey.port.accepts) == 1


@pytest.fixture
def refusal_capture(journey, monkeypatch, capsys):
    """Synthetic journals only: replace the sealed capture's byte digests, never read D data."""
    import hashlib

    from astrid.sdk.workspace_client import WorkspaceClientError

    for index in range(14):
        journal.append(journal.journal_path("p", "t"), project="p", timeline="t",
                       kind="edit", label=f"Synthetic prior edit {index}")
    workspace = restore_commit._workspace(journey.parsed.client)
    monkeypatch.setattr(workspace, "commit_timeline", lambda body: (_ for _ in ()).throw(
        WorkspaceClientError(401, "unauthorized", "authoring invocation revoked or unavailable")))
    assert cli_history.run_restore(journey.parsed) != 0
    capsys.readouterr()
    path = journal.journal_path("p", "t")
    prefix = path.read_bytes()
    intent = json.loads(prefix.splitlines()[-1])["evidence"][0]
    response = (json.dumps(dict(ok=False, data=None, receipt=None,
        idempotency_key=intent["body"]["request_id"], error=dict(code="unauthorized",
        message="authoring invocation revoked or unavailable", details={}))) + "\n").encode()
    qualified = {**restore_commit._REFUSAL_CAPTURE,
        "request_id": intent["body"]["request_id"], "request_hash": intent["request_hash"],
        "project_id": "p", "timeline_id": "t",
        "journal_sha256": hashlib.sha256(prefix).hexdigest(),
        "response_sha256": hashlib.sha256(response).hexdigest()}
    monkeypatch.setattr(restore_commit, "_REFUSAL_CAPTURE", qualified)
    evidence = dict(kind="restore-refusal-evidence-v1", **qualified, origin=intent["origin"],
                    protocol_proof=copy.deepcopy(restore_commit._REFUSAL_PROTOCOL_PROOF))
    return SimpleNamespace(path=path, prefix=prefix, intent=intent, response=response,
                           evidence=evidence, journey=journey)


def _resolve_capture(capture):
    return restore_commit.resolve_restore_refusal("p", "t", evidence=capture.evidence,
                                                 response=capture.response)


def test_local_refusal_resolution_preserves_prefix_and_is_idempotent(refusal_capture, monkeypatch):
    c = refusal_capture
    fsyncs = []
    sync = journal._fsync_directory
    monkeypatch.setattr(journal, "_fsync_directory", lambda path: (fsyncs.append(path), sync(path))[-1])
    result = _resolve_capture(c)
    after = c.path.read_bytes()
    assert len(c.prefix.splitlines()) == 15
    assert after.startswith(c.prefix) and len(after.splitlines()) == len(c.prefix.splitlines()) + 1
    row = json.loads(after.splitlines()[-1])
    assert (row["kind"], row["outcome"]) == ("restore-refusal-resolution", "locally-resolved-refusal")
    assert row["evidence"] == [result]
    assert result["kind"] == "restore-commit-local-refusal-resolution-v1"
    assert result["request_id"] == c.intent["body"]["request_id"]
    assert result["request_hash"] == c.intent["request_hash"]
    assert result["evidence_hash"] == restore_commit._digest(c.evidence)
    assert "result" not in result and "body" not in result and "origin" not in result
    assert not journal.verify(c.path) and fsyncs == [c.path.parent]
    assert _resolve_capture(c) == result
    assert c.path.read_bytes() == after
    assert fsyncs == [c.path.parent, c.path.parent]  # idempotent return confirms durability
    assert not c.journey.calls and not c.journey.port.accepts and not c.journey.publications
    with pytest.raises(TimelineEditError, match="locally resolved"):
        cli_history.run_restore(c.journey.parsed)
    assert not c.journey.calls and c.path.read_bytes() == after


@pytest.mark.parametrize("field", ["request_id", "request_hash", "project_id", "timeline_id",
    "origin", "response_sha256", "journal_sha256", "qualification", "protocol_proof",
    "send_count", "missing", "extra"])
def test_refusal_resolution_rejects_mismatched_or_incomplete_evidence(refusal_capture, field):
    c = refusal_capture
    if field == "missing":
        del c.evidence["origin"]
    elif field == "extra":
        c.evidence["secret"] = "must not be retained"
    else:
        c.evidence[field] = {"wrong": True} if field in {"origin", "protocol_proof"} else "wrong"
    with pytest.raises(TimelineEditError):
        _resolve_capture(c)
    assert c.path.read_bytes() == c.prefix


@pytest.mark.parametrize("field", ["runtime_commit", "authoring_scene_sha256", "timeline_commit_sha256",
    "ruling_sha256", "checks", "exceptions_rollback", "post_acceptance_readback"])
def test_refusal_resolution_requires_complete_qualified_ordering(refusal_capture, field):
    c = refusal_capture
    c.evidence["protocol_proof"][field] = False
    with pytest.raises(TimelineEditError):
        _resolve_capture(c)
    assert c.path.read_bytes() == c.prefix


@pytest.mark.parametrize("damage", ["duplicate", "result", "chain", "body", "origin", "row-scope",
    "not-pending", "second-send", "missing-newline", "unknown-response", "post-acceptance",
    "timeout", "response-lost", "duplicate-json", "oversized"])
def test_refusal_resolution_leaves_ambiguous_or_tampered_journal_unchanged(refusal_capture, monkeypatch, damage):
    import hashlib
    c = refusal_capture
    if damage in {"duplicate", "result", "second-send"}:
        item = copy.deepcopy(c.intent) if damage == "duplicate" else dict(
            kind="restore-commit-result-v1" if damage == "result" else "restore-commit-dispatch-v1",
            request_id=c.intent["body"]["request_id"], request_hash=c.intent["request_hash"])
        journal.append(c.path, project="p", timeline="t", kind="restore", outcome="pending", evidence=(item,))
    elif damage in {"body", "origin", "row-scope", "not-pending"}:
        row = json.loads(c.prefix.splitlines()[-1])
        if damage == "body":
            row["evidence"][0]["body"]["session_id"] = "tampered"
        elif damage == "origin":
            row["evidence"][0]["origin"] = {"principal": "other"}
        else:
            row["project" if damage == "row-scope" else "outcome"] = "other"
        row["hash"] = journal._hash(row["prev"], {k: v for k, v in row.items() if k != "hash"})
        c.path.write_bytes(b"".join(c.prefix.splitlines(keepends=True)[:-1]) + (json.dumps(row) + "\n").encode())
    elif damage == "chain":
        c.path.write_bytes(c.prefix.replace(b'"seq":1', b'"seq":7'))
    elif damage == "missing-newline":
        c.path.write_bytes(c.prefix.rstrip(b"\n"))
    elif damage == "duplicate-json":
        c.response = b'{"ok":false,"ok":true}'
    elif damage == "oversized":
        c.response = b" " * 16385
    else:
        c.response = json.dumps(dict(ok=False, error=dict(code=damage))).encode()
    # Even a changed snapshot digest cannot qualify an unknown response or invalid envelope.
    # Retain fixed production qualification semantics while exercising structural checks.
    if damage in {"duplicate", "result", "body", "origin", "row-scope", "not-pending", "second-send",
                  "chain", "missing-newline"}:
        digest = hashlib.sha256(c.path.read_bytes()).hexdigest()
        monkeypatch.setitem(restore_commit._REFUSAL_CAPTURE, "journal_sha256", digest)
        c.evidence["journal_sha256"] = digest
    before = c.path.read_bytes()
    with pytest.raises(TimelineEditError):
        _resolve_capture(c)
    assert c.path.read_bytes() == before
    assert not c.journey.calls


@pytest.mark.parametrize("failure", ["response-lost", "post-acceptance-readback"])
def test_accepted_ambiguity_cannot_use_refusal_capture(journey, monkeypatch, capsys, failure):
    from astrid.sdk.workspace_client import WorkspaceClientError
    workspace = restore_commit._workspace(journey.parsed.client)
    commit = workspace.commit_timeline
    def ambiguous(body):
        commit(body)
        raise WorkspaceClientError(500, "unverified_commit", failure)
    monkeypatch.setattr(workspace, "commit_timeline", ambiguous)
    assert cli_history.run_restore(journey.parsed) != 0
    failure_result = json.loads(capsys.readouterr().out)
    assert "repeat restore" not in failure_result["error"]["details"].get("retry", "")
    path = journal.journal_path("p", "t")
    before = path.read_bytes()
    with pytest.raises(TimelineEditError):
        restore_commit.resolve_restore_refusal("p", "t", evidence={}, response=json.dumps(failure_result).encode())
    assert path.read_bytes() == before and len(journey.port.accepts) == 1


@pytest.mark.parametrize("check", ["before_publication", "inside_acceptance_transaction"])
def test_qualified_refusal_ordering_is_source_protocol_proof_only(refusal_capture, check):
    """Assert the admitted source proof, not a pretend execution of Runtime rollback."""
    c = refusal_capture
    proof = c.evidence["protocol_proof"]
    assert check in proof["checks"]
    assert proof["exceptions_rollback"] is True
    assert proof["post_acceptance_readback"] == "distinct_ambiguous_path"
    assert proof["runtime_commit"] == "9eaa2aafd40cedac80adcf9c738ea8f09a854eed"
    assert proof["ruling_sha256"] == "d922e1b7da3c9b3e8fde3475954ae3890846a257fcf12c00b678218eb10141ac"
    assert _resolve_capture(c)["qualification"] == c.evidence["qualification"]
    assert not c.journey.calls and not c.journey.port.accepts


@pytest.mark.parametrize("gateway", ["family", "product"])
@pytest.mark.parametrize("syntax", ["separate", "equals", "abbreviated"])
def test_cli_refusal_resolution_is_offline_at_gateway(refusal_capture, tmp_path, monkeypatch, capsys, gateway, syntax):
    from astrid.core.gateway.dispatch import _dispatch_product, _dispatch_timelines
    from astrid.sdk.client import AstridClient
    c = refusal_capture
    dispatch = _dispatch_timelines if gateway == "family" else lambda args: _dispatch_product(["timelines", *args])
    evidence = tmp_path / "refusal.json"
    response = tmp_path / "response.json"
    evidence.write_text(json.dumps(c.evidence))
    response.write_bytes(c.response)
    monkeypatch.setattr(AstridClient, "open_from_launcher", lambda **kw: pytest.fail("Runtime acquisition"))
    # The gateway must parse this route without even consulting current project.
    args = ["restore", "t", "--project", "p", "--resolve-refusal", str(evidence),
            "--refusal-response", str(response), "--json"]
    if syntax == "equals":
        args[4:6] = ["--resolve-refusal=" + str(evidence)]
    elif syntax == "abbreviated":
        args[4] = "--resolve-ref"
    assert dispatch(args) == 0
    assert json.loads(capsys.readouterr().out)["data"]["kind"] == "restore-commit-local-refusal-resolution-v1"
    after = c.path.read_bytes()
    assert dispatch(args) == 0
    capsys.readouterr()
    assert c.path.read_bytes() == after and not c.journey.calls
    with pytest.raises(SystemExit) as exc:
        dispatch(["restore", "t", "--resolve-refusal=" + str(evidence),
                  "--refusal-response", str(response)])
    assert exc.value.code == 2 and c.path.read_bytes() == after


def test_resolution_directory_fsync_failure_can_only_repeat_resolution(refusal_capture, monkeypatch):
    c = refusal_capture
    sync = journal._fsync_directory
    monkeypatch.setattr(journal, "_fsync_directory", lambda p: (_ for _ in ()).throw(OSError("synthetic fsync")))
    with pytest.raises(TimelineEditError, match="durability is unconfirmed"):
        _resolve_capture(c)
    after = c.path.read_bytes()
    assert after.startswith(c.prefix) and len(after.splitlines()) == len(c.prefix.splitlines()) + 1
    with pytest.raises(TimelineEditError, match="durability is unconfirmed"):
        _resolve_capture(c)
    assert c.path.read_bytes() == after
    monkeypatch.setattr(journal, "_fsync_directory", sync)
    _resolve_capture(c)
    assert c.path.read_bytes() == after
    with pytest.raises(TimelineEditError, match="locally resolved"):
        cli_history.run_restore(c.journey.parsed)
    assert not c.journey.calls


@pytest.mark.parametrize("damage", ["duplicate-resolution", "resolution-metadata", "result-after-resolution"])
def test_resolved_capture_rejects_conflicting_or_duplicate_records(refusal_capture, damage):
    c = refusal_capture
    resolution = _resolve_capture(c)
    row = journal.read(c.path)[-1].to_json()
    if damage == "resolution-metadata":
        row["evidence"][0]["evidence_hash"] = "sha256:" + "0" * 64
        row["hash"] = journal._hash(row["prev"], {k: v for k, v in row.items() if k != "hash"})
        c.path.write_bytes(c.prefix + (json.dumps(row) + "\n").encode())
    else:
        item = resolution if damage == "duplicate-resolution" else dict(
            kind="restore-commit-result-v1", request_id=resolution["request_id"], request_hash=resolution["request_hash"])
        journal.append(c.path, project="p", timeline="t", kind="restore-refusal-resolution",
                       outcome="locally-resolved-refusal", evidence=(item,))
    before = c.path.read_bytes()
    with pytest.raises(TimelineEditError):
        _resolve_capture(c)
    assert c.path.read_bytes() == before and not c.journey.calls


def test_captured_key_cannot_be_retried_even_before_local_resolution(refusal_capture):
    c = refusal_capture
    with pytest.raises(TimelineEditError, match="do not retry"):
        cli_history.run_restore(c.journey.parsed)
    assert c.path.read_bytes() == c.prefix and not c.journey.calls


@pytest.mark.parametrize("modes", [[], ["--from", "prev", "--resolve-refusal", "refusal.json"]])
def test_restore_cli_requires_one_unambiguous_mode(modes):
    from astrid.packs.timeline.cli import build_parser
    with pytest.raises(SystemExit) as exc:
        build_parser(None).parse_args(["restore", "t", "--project", "p", *modes])
    assert exc.value.code == 2
