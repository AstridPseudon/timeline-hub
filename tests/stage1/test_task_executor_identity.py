"""Executor byte identity reaches real Runtime admission without a provider."""
from __future__ import annotations

import json
import os
import py_compile
import shutil
import time
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost
from astrid.sdk import invocation
from astrid.sdk.remote import RemoteTasks
from tests.test_generic_host import _write_manifest


def _fixture(tmp_path):
    root = tmp_path / "checkout" / "echo"
    _write_manifest(root)
    (root / "executor.py").write_text("VALUE = 'broken'\n")
    return root


def _record(root):
    return GenericPackHost(pack_roots=[root]).discover()[0]


@pytest.mark.parametrize("change", ["checkout", "mtime", "pyc"])
def test_identical_source_keeps_capability_identity(tmp_path, change):
    root = _fixture(tmp_path)
    if change == "pyc":
        py_compile.compile(str(root / "executor.py"), cfile=str(root / "executor.pyc"),
            dfile="old-checkout/executor.py", doraise=True)
        old_bytecode = (root / "executor.pyc").read_bytes()
    before = _record(root).capability_digest
    if change == "checkout":
        other = tmp_path / "other-checkout" / "renamed-source-folder"
        shutil.copytree(root, other)
        root = other
    elif change == "mtime":
        for path in root.iterdir():
            os.utime(path, (1700000000, 1700000000))
    else:
        # Exercise both normal cache placement and legacy adjacent bytecode.
        py_compile.compile(str(root / "executor.py"), cfile=str(root / "executor.pyc"),
            dfile="new-checkout/executor.py", doraise=True)
        assert (root / "executor.pyc").read_bytes() != old_bytecode
        cache = root / "__pycache__"
        cache.mkdir()
        py_compile.compile(str(root / "executor.py"), cfile=str(cache / "executor.test.pyc"), doraise=True)
    assert _record(root).capability_digest == before


@pytest.mark.parametrize("kind", ["external_pack", "python_action"])
def test_imported_pack_source_is_portable_and_bound(tmp_path, kind):
    if kind == "python_action":
        from tests.core.execution.test_generic_host_actions_v3 import pack
        root = pack(tmp_path)[0]
    else:
        root = tmp_path / "fixture_provider"
        _write_manifest(root / "executors" / "echo", capability_id="fixture_provider.echo")
        (root / "pack.yaml").write_text(json.dumps({"schema_version": 1,
            "id": "fixture_provider", "name": "Fixture", "version": "1.0",
            "capabilities": ["echo"], "content": {"executors": "executors"}}))
    helper = root / "helper.py"
    helper.write_text("VALUE = 'before'\n")
    before = _record(root).capability_digest
    moved = tmp_path / "another-checkout" / root.name
    shutil.copytree(root, moved)
    assert _record(moved).capability_digest == before
    (moved / "helper.py").write_text("VALUE = 'after'\n")
    assert _record(moved).capability_digest != before


def test_executor_source_fix_admits_new_task_and_failed_replay_stays_explicit(tmp_path, capsys):
    # Required dependency: execute with the exact assigned Runtime on PYTHONPATH.
    from runtime_protocol.errors import ConflictError
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    from astrid.core.cli.domain_tasks import _cmd_retry
    from astrid.sdk.workspace_client import WorkspaceClientError

    root = _fixture(tmp_path)
    RealmStore.initialize(tmp_path / "realm").close()
    service = RuntimeService(tmp_path / "realm")

    class Transport:
        def list_capabilities(self, **_kwargs):
            return [service.list_capabilities()["items"], None]

        def admit_task(self, **payload):
            # Match generated-client wire omission of optional null fields.
            created = service.create_task({key: value for key, value in payload.items() if value is not None})
            return service._task_resource(service.task(created["task"]["id"]))

        def retry_task(self, task_id, *, idempotency_key):
            try:
                return service.retry_task(task_id, idempotency_key=idempotency_key)["data"]
            except ConflictError as exc:
                raise WorkspaceClientError(exc.status, exc.code, exc.message, exc.details) from exc

    client = SimpleNamespace(tasks=RemoteTasks(Transport()))
    capability = SimpleNamespace(id="test.echo", capability_type="executor", inputs=())

    def register():
        digest = _record(root).capability_digest
        service.register_capability({"capability_id": capability.id, "definition_digest": digest})
        service.store.upsert_executor("fake-provider", [capability.id], runtime_epoch=service.health()["runtime_epoch"])
        return digest

    def invoke(**kwargs):
        return invocation._kernel_invoke(capability, kind="executor", project=None,
            inputs={"prompt": "same"}, outputs={}, _client=client, **kwargs)

    try:
        old_digest = register()
        first = invoke()
        assert first[5] is True
        task_id = first[1]
        service.store._claim_task(task_id, "fake-provider", "lease", runtime_epoch=service.health()["runtime_epoch"])
        service.store.fail_task(task_id, "lease", {"message": "fixture failure"})
        # No sleeps: explicitly age the disposable receipt for replay labeling.
        service.store.conn.execute("UPDATE tasks SET created_at='2020-01-01T00:00:00Z' WHERE id=?", (task_id,))
        service.store.conn.commit()
        replay = invoke()
        assert replay[1] == task_id
        assert replay[5] is False
        assert replay[4]["error"]["code"] == "replayed_failed_task"
        assert "rerun=True" in replay[4]["error"]["message"]
        deliberate = invoke(rerun=True)
        assert deliberate[5] is True and deliberate[1] != task_id
        (root / "executor.py").write_text("VALUE = 'fixed'\n")
        new_digest = register()
        changed = invoke()
        assert changed[5] is True
        assert changed[1] not in {task_id, deliberate[1]}
        assert new_digest != old_digest
        assert service.task(task_id)["task"]["status"] == "failed"
        assert service.task(changed[1])["task"]["capability_digest"] == new_digest
        assert invoke()[1] == changed[1]
        started = time.monotonic()
        exit_code = _cmd_retry(SimpleNamespace(client=client, task_id=task_id,
            idempotency_key="retry-obsolete-cli", json=True))
        elapsed = time.monotonic() - started
        output = capsys.readouterr().out
        assert exit_code != 0
        assert "capability digest mismatch" in output
        assert old_digest in output and new_digest in output
        assert elapsed < 30
        assert service.task(task_id)["task"]["status"] == "failed"
        print(f"tasks retry CLI exit={exit_code} digest mismatch in {elapsed:.6f}s")
    finally:
        service.close()
