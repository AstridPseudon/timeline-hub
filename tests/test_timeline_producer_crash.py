"""SIGKILL storage proof, using prepared providers rather than Agent semantics."""
from __future__ import annotations

import copy
import json
import os
import selectors
import signal
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_timeline_commit_port import PreparedProvider, commit, request
from test_timeline_producer_checkpoint import _admit, _checkpoint
from test_timeline_producer_checkpoint import producer as producer  # noqa: PLC0414
from test_timeline_producer_guards import _context, _execute, _settle

from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_producer import ProducerReads
from runtime_protocol.timeline_commit_store import TimelineCommitStore
from tests.lanes import requires_posix_process_groups

pytestmark = [requires_posix_process_groups, pytest.mark.timeout(90)]

TABLES = (
    "timelines", "parent_composition_heads", "parent_composition_revisions",
    "internal_timeline_revisions", "shot_revisions", "shot_revision_heads",
    "timeline_commit_history", "timeline_render_publications", "timeline_events",
    "command_idempotency", "project_sequences", "timeline_document_input_contents",
    "timeline_document_input_bindings", "timeline_document_input_links",
    "tasks", "runs", "attempts", "task_specs", "events", "objects", "project_objects",
    "managed_output_associations", "managed_output_lifecycle",
)


def _snapshot(conn):
    return {table: [tuple(row) for row in conn.execute(f'SELECT * FROM "{table}" ORDER BY rowid')]
            for table in TABLES}


def _files(root):
    # Only managed bytes and staging; never collect credentials or realm config.
    return {str(path.relative_to(root)): path.read_bytes()
            for directory in (root / "cas", root / "staging")
            for path in directory.rglob("*") if path.is_file()}


def _message(child):
    deadline = time.monotonic() + 25
    data = b""
    with selectors.DefaultSelector() as selector:
        selector.register(child.stdout, selectors.EVENT_READ)
        while b"\n" not in data:
            ready = selector.select(max(0, deadline - time.monotonic()))
            assert ready, "child did not reach its crash boundary within 25s"
            chunk = os.read(child.stdout.fileno(), 65536)
            assert chunk, f"child exited before its crash boundary: {data.decode(errors='replace')}"
            data += chunk
    return json.loads(data)


def _crash(producer, seam, observe):
    context = _context(producer)
    payload = {key: getattr(producer, key) for key in ("project", "task", "pin", "proposal")}
    payload.update(root=str(producer.root), context=context)
    producer.service.close()
    source = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": os.pathsep.join((str(source), str(source / "tests"),
                                                      os.environ.get("PYTHONPATH", ""))),
           "PYTHONDONTWRITEBYTECODE": "1"}
    child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), seam],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=source)
    try:
        child.stdin.write(json.dumps(payload).encode() + b"\n")
        child.stdin.flush()
        reached = _message(child)
        assert reached["seam"] == seam
        assert reached["context"] == context
        assert reached["epoch"] > producer.pin["runtime_epoch"]
        assert child.poll() is None
        # A separate reader must see the actual durable side of the boundary
        # while the child is blocked, before we deliver SIGKILL.
        conn = sqlite3.connect(f"file:{producer.root / 'realm.sqlite3'}?mode=ro", uri=True, timeout=2)
        try:
            observe(reached, conn)
        finally:
            conn.close()
        child.kill()
        assert child.wait(timeout=5) == -signal.SIGKILL
    finally:
        if child.poll() is None:
            child.kill()
            child.wait(timeout=5)
        child.stdin.close()
        child.stdout.close()
    producer.service = RuntimeService(producer.root)
    assert producer.service.store.admission_report["ok"]
    assert producer.service.health()["runtime_epoch"] > reached["epoch"]
    assert _context(producer) == context
    task = producer.service.task(producer.task)["task"]
    assert task["status"] == "completed"
    assert task["attempt_id"] == producer.pin["attempt_id"]
    assert task["executor_id"] == producer.pin["executor_id"]
    assert task["runtime_epoch"] == producer.pin["runtime_epoch"]
    assert task["lease_fence"] == producer.pin["fence"]
    attempt = producer.service.store.conn.execute("SELECT * FROM attempts WHERE id=?",
                                                 (producer.pin["attempt_id"],)).fetchone()
    assert attempt["settled"] == 1 and attempt["runtime_epoch"] == producer.pin["runtime_epoch"]
    return reached


def _pending(producer, accepted):
    checkpoint = _checkpoint(producer)
    assert checkpoint["state"] == "prepared" and checkpoint["render_task_id"] is None
    assert checkpoint["prepared"]["pin"] == producer.pin
    context = _context(producer)
    assert checkpoint["prepared"]["identity"] == {
        **{key: context[key] for key in ("realm_id", "publisher", "idempotency_key", "request_hash")},
        "project_id": producer.project, "timeline_id": "main"}
    pending = checkpoint["prepared"]["pending_render"]
    selector = pending["body"]["spec"]["params"]["canonical_revision"]
    assert checkpoint["result"]["accepted"] == {"receipt": accepted["receipt"], **selector}
    assert selector["revision_id"] == accepted["data"]["accepted_revision_id"]
    assert selector["publication_id"] == accepted["receipt"]["receipt_id"]
    return copy.deepcopy(pending)


def _forbidden(*args, **kwargs):
    pytest.fail("exact durable replay must not invoke the provider, request port or live producer authority")


def test_sigkill_after_checkpoint_insert_leaves_no_partial_acceptance(producer):
    _settle(producer)
    before, files = _snapshot(producer.service.store.conn), _files(producer.root)

    def observe(reached, conn):
        assert reached["in_transaction"] is True
        assert reached["checkpoint"]["result"] is None
        for table in ("parent_composition_revisions", "timeline_commit_history", "command_idempotency",
                      "timeline_render_publications"):
            assert reached["counts"][table] == len(before[table]) + 1
        assert _snapshot(conn) == before

    _crash(producer, "checkpoint-insert", observe)
    assert _snapshot(producer.service.store.conn) == before
    assert _files(producer.root) == files
    assert _checkpoint(producer) is None
    accepted = _execute(producer)
    _pending(producer, accepted)
    after = _snapshot(producer.service.store.conn)
    for table in ("parent_composition_revisions", "timeline_commit_history", "command_idempotency"):
        assert len(after[table]) == len(before[table]) + 1
    assert after["tasks"] == before["tasks"] and after["runs"] == before["runs"]
    assert _execute(producer) == accepted
    assert _snapshot(producer.service.store.conn) == after


def test_sigkill_after_acceptance_replays_exact_receipt_and_pending_render(producer, monkeypatch):
    _settle(producer)
    before = _snapshot(producer.service.store.conn)

    def observe(reached, conn):
        assert reached["in_transaction"] is False
        assert reached["checkpoint"]["result"]["accepted"]["receipt"] == reached["accepted"]["receipt"]
        durable = _snapshot(conn)
        for table in ("parent_composition_revisions", "timeline_commit_history", "command_idempotency",
                      "timeline_render_publications"):
            assert len(durable[table]) == len(before[table]) + 1
        assert durable["tasks"] == before["tasks"] and durable["runs"] == before["runs"]
        result, = conn.execute("SELECT result_json FROM timeline_render_publications").fetchone()
        assert json.loads(result) == reached["checkpoint"]["result"]

    reached = _crash(producer, "acceptance-durable", observe)
    assert _checkpoint(producer) == reached["checkpoint"]
    _pending(producer, reached["accepted"])
    stable, files = _snapshot(producer.service.store.conn), _files(producer.root)
    monkeypatch.setattr(ProducerReads, "capture", _forbidden)
    assert _execute(producer, provider=PreparedProvider(_forbidden), port_factory=_forbidden) == reached["accepted"]
    assert _snapshot(producer.service.store.conn) == stable
    assert _files(producer.root) == files


def test_sigkill_after_historical_admission_replays_original_task_and_link_after_c(producer, monkeypatch):
    _settle(producer)
    accepted = _execute(producer)
    pending = _pending(producer, accepted)
    before = _snapshot(producer.service.store.conn)

    def observe(reached, conn):
        assert reached["in_transaction"] is False
        linked = reached["checkpoint"]
        assert linked["state"] == "published"
        assert linked["render_task_id"] == reached["admitted"]["task"]["id"]
        durable = _snapshot(conn)
        for table in ("tasks", "runs", "command_idempotency"):
            assert len(durable[table]) == len(before[table]) + 1
        row, = conn.execute("SELECT render_task_id, result_json FROM timeline_render_publications").fetchall()
        assert row[0] == linked["render_task_id"]
        assert json.loads(row[1]) == linked["result"]

    reached = _crash(producer, "render-admission-durable", observe)
    linked = reached["checkpoint"]
    assert _checkpoint(producer) == linked
    assert linked["prepared"]["pending_render"] == pending
    service = producer.service
    service.register_timeline_commit_provider(PreparedProvider())
    service.test_project = producer.project
    later = commit(service, request(service), key="unrelated-c")
    assert later["data"]["accepted_revision_id"] != accepted["data"]["accepted_revision_id"]
    stable, files = _snapshot(service.store.conn), _files(producer.root)
    monkeypatch.setattr(ProducerReads, "capture", _forbidden)
    replay = _admit(producer, pending)
    assert replay == reached["admitted"]
    assert _checkpoint(producer) == linked
    authority = replay["task"]["spec"]["spec"]["inputs"]["timeline_authority"]
    assert authority["parent_revision_id"] == accepted["data"]["accepted_revision_id"]
    assert authority["publication_id"] == accepted["receipt"]["receipt_id"]
    assert authority["parent_content_digest"] == pending["body"]["spec"]["params"]["canonical_revision"]["content_digest"]
    receipt, = service.store.conn.execute(
        "SELECT txn_id, request_hash FROM command_idempotency WHERE command_kind='task.create' AND idempotency_key=?",
        (pending["idempotency_key"],)).fetchall()
    assert linked["result"]["render"] == {"task_id": replay["task"]["id"], "run_id": replay["run"]["id"],
        "receipt_id": receipt[0], "request_hash": receipt[1], "idempotency_key": pending["idempotency_key"]}
    assert _snapshot(service.store.conn) == stable
    assert _files(producer.root) == files


def _child(seam):
    payload = json.loads(sys.stdin.buffer.readline())
    context = payload.pop("context")
    producer = SimpleNamespace(**payload)
    producer.service = RuntimeService(producer.root)
    assert _context(producer) == context

    def pause(**facts):
        print(json.dumps({"seam": seam, "context": context,
            "epoch": producer.service.health()["runtime_epoch"],
            "in_transaction": producer.service.store.conn.in_transaction,
            "checkpoint": _checkpoint(producer), **facts}), flush=True)
        # Parent keeps stdin open until killing us. EOF also releases a failed
        # parent's child; no exception unwinding is used as crash evidence.
        sys.stdin.buffer.read(1)
        raise AssertionError("parent released crash boundary without SIGKILL")

    if seam == "checkpoint-insert":
        original = producer.service.store.prepare_timeline_render_publication

        def prepare(*args, **kwargs):
            original(*args, **kwargs)
            pause(counts={table: len(rows) for table, rows in _snapshot(producer.service.store.conn).items()})

        producer.service.store.prepare_timeline_render_publication = prepare
        _execute(producer)
    elif seam == "acceptance-durable":
        original = TimelineCommitStore.accept

        def accept(*args, **kwargs):
            accepted = original(*args, **kwargs)
            pause(accepted=accepted)

        TimelineCommitStore.accept = accept
        _execute(producer)
    elif seam == "render-admission-durable":
        original = producer.service.create_task

        def admit(*args, **kwargs):
            admitted = original(*args, **kwargs)
            pause(admitted=admitted)

        producer.service.create_task = admit
        _admit(producer)
    raise AssertionError(f"crash boundary not reached: {seam}")


if __name__ == "__main__":
    _child(sys.argv[1])
