"""Request-scoped port read snapshots stay isolated without duplicate detaches."""
from __future__ import annotations

import copy

import pytest
from test_timeline_commit_port import (
    PreparedProvider,
    commit,
    prepared,
    request,
    use_provider,
)

import runtime_protocol.timeline_commit_port as port_module
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore


@pytest.fixture
def service(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    runtime = RuntimeService(root)
    provider = PreparedProvider()
    runtime.register_timeline_commit_provider(provider)
    runtime.__dict__["test_provider"] = provider
    project = runtime.create_project({"slug": "read-isolation", "name": "Read isolation"})["id"]
    runtime.create_timeline(project, "main", idempotency_key="create-main")
    runtime.__dict__["test_project"] = project
    try:
        yield runtime
    finally:
        runtime.close()


def test_revision_read_isolation_and_single_port_detach(service, monkeypatch):
    body = request(service)
    base_revision_id = body["base_revision_id"]
    real_deepcopy = copy.deepcopy
    observed = {}

    def action(context, port):
        head = port.head()
        baseline = real_deepcopy(port.revision_closure(head["revision_id"]))
        calls = 0

        def counted(value, memo=None, _deepcopy=real_deepcopy):
            nonlocal calls
            calls += 1
            return _deepcopy(value, memo) if memo is not None else _deepcopy(value)

        monkeypatch.setattr(port_module.copy, "deepcopy", counted)
        try:
            first = port.revision_closure(head["revision_id"])
            first["parent_revision"]["payload"]["read_isolation_probe"] = "mutated"
            second = port.revision_closure(head["revision_id"])
        finally:
            monkeypatch.setattr(port_module.copy, "deepcopy", real_deepcopy)

        observed["copy_calls"] = calls
        observed["second"] = second
        observed["baseline"] = baseline
        return port.accept(prepared(context, port))

    use_provider(service, PreparedProvider(action))
    result = commit(service, body, key="read-isolation")

    assert result["data"]["status"] == "accepted"
    # Each public read gets exactly one isolated boundary copy; the first read
    # must not also copy the private request snapshot into the closure cache.
    assert observed["copy_calls"] == 2
    assert observed["second"] == observed["baseline"]
    stored = service._timeline_commits()[0].revision_closure(
        service.test_project, "main", base_revision_id
    )
    assert "read_isolation_probe" not in stored["parent_revision"]["payload"]
