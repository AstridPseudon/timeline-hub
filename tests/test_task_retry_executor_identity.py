"""Same-task retry cannot queue work for an obsolete executor digest."""
from __future__ import annotations

import time

import pytest

from runtime_protocol.errors import ConflictError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore

CAPABILITY = "fixture.retry-identity"
OLD = "sha256:" + "a" * 64
NEW = "sha256:" + "b" * 64


@pytest.fixture
def failed_task(tmp_path):
    RealmStore.initialize(tmp_path / "realm").close()
    service = RuntimeService(tmp_path / "realm")
    service.register_capability({"capability_id": CAPABILITY, "definition_digest": OLD})
    epoch = service.health()["runtime_epoch"]
    service.store.upsert_executor("fake-provider", [CAPABILITY], runtime_epoch=epoch)
    task = service.create_task({"capability_id": CAPABILITY, "capability_digest": OLD,
        "input_object_ids": [], "spec": {}, "idempotency_key": "initial"})["task"]
    service.store._claim_task(task["id"], "fake-provider", "lease", runtime_epoch=epoch)
    service.store.fail_task(task["id"], "lease", {"message": "disposable failure"})
    try:
        yield service, task["id"]
    finally:
        service.close()


@pytest.mark.parametrize("route", ["task", "run"])
def test_retry_digest_mismatch_fails_immediately_without_mutating_failure(failed_task, route):
    service, task_id = failed_task
    original = service.task(task_id)
    service.register_capability({"capability_id": CAPABILITY, "definition_digest": NEW})
    service.store.upsert_executor("fake-provider", [CAPABILITY], runtime_epoch=service.health()["runtime_epoch"])
    events = service.events(original["run"]["id"])
    started = time.monotonic()
    with pytest.raises(ConflictError, match="capability digest mismatch") as caught:
        if route == "task":
            service.retry_task(task_id, idempotency_key="retry-obsolete")
        else:
            service.retry_run(original["run"]["id"], idempotency_key="retry-obsolete")
    elapsed = time.monotonic() - started
    print(f"{route} retry digest mismatch returned in {elapsed:.6f}s")
    assert elapsed < 30
    assert caught.value.details["admitted_digest"] == OLD
    assert caught.value.details["registered_digest"] == NEW
    assert caught.value.details["task_id"] == task_id
    assert "new task" in caught.value.details["next_action"]
    assert service.task(task_id) == original
    assert service.events(original["run"]["id"]) == events


@pytest.mark.parametrize("route", ["task", "run"])
def test_unchanged_digest_retry_runs_with_fake_executor(failed_task, route):
    service, task_id = failed_task
    if route == "task":
        service.retry_task(task_id, idempotency_key="retry-unchanged")
    else:
        service.retry_run(service.task(task_id)["run"]["id"], idempotency_key="retry-unchanged")
    claimed = service.store._claim_task(task_id, "fake-provider", "fresh-lease",
        runtime_epoch=service.health()["runtime_epoch"])
    assert claimed["task"]["status"] == "running"
    assert claimed["task"]["capability_digest"] == OLD
    assert claimed["task"]["attempt"] == 2
