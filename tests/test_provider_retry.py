"""Fake provider rejections exercise the durable canonical task loop."""
from datetime import datetime, timedelta, timezone
from itertools import count

import pytest

from runtime_protocol.errors import ConflictError, LeaseError, ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore

CAP = "fixture.provider"
DIGEST = "sha256:" + "a" * 64


@pytest.fixture
def world(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    clock = [datetime.now(timezone.utc)]
    service.store._provider_retry_now = lambda: clock[0]
    service.register_capability({"capability_id": CAP, "definition_digest": DIGEST})
    service.store.upsert_executor("fake", [CAP], max_concurrency=4, runtime_epoch=service.health()["runtime_epoch"])
    keys = count()

    def task(provider="fake-paid-provider"):
        return service.create_task({"capability_id": CAP, "capability_digest": DIGEST,
            "spec": {"inputs": {"provider": provider}}, "input_object_ids": [],
            "idempotency_key": f"task-{next(keys)}"})["task"]["id"]

    def claim():
        return service.claim_next({"executor_id": "fake", "capability_ids": [CAP],
            "runtime_epoch": service.health()["runtime_epoch"]}, idempotency_key=f"claim-{next(keys)}")

    def fail(attempt, *, retryable=True, delay=7, key=None):
        return service.fail_attempt(attempt["attempt_id"], {
            "lease_id": attempt["lease_id"], "fence": attempt["fence"],
            "runtime_epoch": attempt["runtime_epoch"],
            "error": {"code": "provider_failure", "message": "429" if retryable else "400 final",
                "provider_id": "fake-paid-provider", "retryable": retryable, "retry_after_seconds": delay},
        }, idempotency_key=key or f"fail-{next(keys)}")

    def settle(attempt):
        return service.settle_attempt(attempt["attempt_id"], {
            "lease_id": attempt["lease_id"], "fence": attempt["fence"],
            "runtime_epoch": attempt["runtime_epoch"], "outputs": [], "result": {"http_status": 200},
        }, idempotency_key=f"settle-{next(keys)}")

    try:
        yield service, clock, task, claim, fail, settle
    finally:
        service.close()


def test_429_then_200_one_task_one_success_and_idempotent_rejection(world):
    service, clock, task, claim, fail, settle = world
    task_id = task()
    original = service.task(task_id)
    first = claim()
    assert first["task_id"] == task_id
    queued = fail(first, key="429")
    assert queued["data"]["state"] == "queued"
    assert fail(first, key="429") == queued
    assert claim() is None
    clock[0] += timedelta(seconds=7)
    second = claim()
    assert second["task_id"] == task_id
    assert second["attempt_id"] != first["attempt_id"]
    assert second["fence"] > first["fence"]
    assert settle(second)["data"]["state"] == "succeeded"
    final = service.task(task_id)
    assert final["task"]["run_id"] == original["task"]["run_id"]
    assert final["task"]["capability_digest"] == DIGEST
    assert final["task"]["result"]["http_status"] == 200
    assert service.store.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 1
    events = service.store.list_events(first["run_id"])
    assert sum(e["kind"] == "task.completed" for e in events) == 1
    assert claim() is None


def test_two_tasks_share_provider_retry_after_spacing_without_blocking_other_provider(world):
    service, clock, task, claim, fail, settle = world
    first_id = task()
    first = claim()
    calls = [(first_id, clock[0])]
    fail(first)
    second_id = task()
    unrelated = task("other-provider")
    other = claim()
    assert other["task_id"] == unrelated
    settle(other)
    assert claim() is None
    clock[0] += timedelta(seconds=6.999)
    assert claim() is None
    clock[0] += timedelta(milliseconds=1)
    retry = claim()
    calls.append((retry["task_id"], clock[0]))
    settle(retry)
    assert claim() is None  # second request cannot burst at the same deadline
    clock[0] += timedelta(seconds=7)
    second = claim()
    calls.append((second["task_id"], clock[0]))
    settle(second)
    assert [item[0] for item in calls] == [first_id, first_id, second_id]
    assert [(b[1] - a[1]).total_seconds() for a, b in zip(calls, calls[1:])] == [7, 7]


def test_final_failure_is_visible_and_never_automatically_retried(world):
    service, clock, task, claim, fail, _ = world
    task_id = task()
    fail(claim(), retryable=False)
    clock[0] += timedelta(days=1)
    assert claim() is None
    result = service.task(task_id)["task"]
    assert result["status"] == "failed"
    assert result["result"]["error"]["message"] == "400 final"
    assert result["attempt"] == 1


def test_cancel_during_retry_wait_and_stale_attempt_cannot_resubmit(world):
    service, clock, task, claim, fail, settle = world
    task_id = task()
    old = claim()
    fail(old)
    service.cancel_task_canonical(task_id, idempotency_key="cancel-wait")
    clock[0] += timedelta(seconds=30)
    assert claim() is None
    with pytest.raises(LeaseError):
        fail(old)
    with pytest.raises(LeaseError):
        settle(old)
    assert service.task(task_id)["task"]["status"] == "cancelled"


def test_loss_of_current_attempt_cannot_schedule_provider_retry(world):
    service, _, task, claim, fail, _ = world
    task_id = task()
    old = claim()
    service.store.conn.execute("UPDATE tasks SET lease_expires_at=? WHERE id=?",
        ((datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(), task_id))
    service.store._reap_expired_leases()
    with pytest.raises(LeaseError):
        fail(old)
    assert service.store.conn.execute("SELECT COUNT(*) FROM events WHERE kind='task.provider_retry_scheduled'").fetchone()[0] == 0


def test_runtime_backoff_is_bounded_and_keeps_last_failure(world):
    service, clock, task, claim, fail, _ = world
    task_id = task()
    for delay in (1, 2, 4):
        fail(claim(), delay=0)
        assert claim() is None
        clock[0] += timedelta(seconds=delay)
    fail(claim(), delay=0)
    assert claim() is None
    terminal = service.task(task_id)["task"]
    assert terminal["status"] == "failed"
    assert terminal["attempt"] == 4
    assert terminal["result"]["error"]["message"] == "429"


def test_retry_deadline_survives_store_reopen(world):
    service, clock, task, claim, fail, _ = world
    task_id = task()
    fail(claim())
    root = service.store.root
    service.close()
    reopened = RuntimeService(root)
    try:
        reopened.store._provider_retry_now = lambda: clock[0]
        row = reopened.store.conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        assert reopened.store._provider_retry_waiting_reason(row) == "provider_retry_after"
        clock[0] += timedelta(seconds=7)
        assert reopened.store._provider_retry_waiting_reason(row) is None
    finally:
        reopened.close()


def test_unknown_provider_state_is_never_replaced_by_retry_wait(world):
    service, clock, task, claim, fail, _ = world
    task_id = task()
    fail(claim())
    service.store.conn.execute("UPDATE tasks SET waiting_reason='provider_state_unknown' WHERE id=?", (task_id,))
    for advance in (0, 30):
        clock[0] += timedelta(seconds=advance)
        blocked = claim()
        assert blocked["waiting_reason"] == "provider_state_unknown"
        assert "attempt_id" not in blocked
        assert service.task(task_id)["task"]["waiting_reason"] == "provider_state_unknown"


@pytest.mark.parametrize("bad_delay", [-1, float("inf"), True])
def test_invalid_retry_after_cannot_schedule_work(world, bad_delay):
    service, _, task, claim, fail, _ = world
    task_id = task()
    attempt = claim()
    with pytest.raises(ValidationError, match="invalid provider failure"):
        fail(attempt, delay=bad_delay)
    assert service.task(task_id)["task"]["status"] == "running"
    assert service.store.conn.execute("SELECT COUNT(*) FROM events WHERE kind='task.provider_retry_scheduled'").fetchone()[0] == 0


def test_concurrent_rejections_cannot_shorten_provider_cooldown(world):
    service, clock, task, claim, fail, _ = world
    task()
    first = claim()
    task()
    already_running = claim()
    fail(first, delay=9)
    clock[0] += timedelta(seconds=1)
    fail(already_running, delay=2)
    third_id = task()
    clock[0] += timedelta(seconds=2)
    assert claim() is None
    clock[0] += timedelta(seconds=6)
    resumed = claim()
    assert resumed is not None
    assert resumed["task_id"] != third_id
    assert claim() is None
