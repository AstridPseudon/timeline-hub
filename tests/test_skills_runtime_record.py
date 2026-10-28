from __future__ import annotations

import hashlib
import json
import time
from contextlib import AbstractContextManager
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.sdk import AstridClient
from astrid.skills import cli as skills_cli
from astrid.skills.runtime_record import app_state_key, publish


class FakeTransport:
    def __init__(self, *, get=None, put=None):
        self.get_value = get or {"version": 0, "content": None}
        self.put_error = put
        self.gets = []
        self.puts = []

    def get_user_app_state(self, key):
        self.gets.append(key)
        if isinstance(self.get_value, Exception):
            raise self.get_value
        if callable(self.get_value):
            return self.get_value(key)
        return self.get_value

    def update_user_app_state(self, key, content, *, expected_version, idempotency_key):
        self.puts.append((key, content, expected_version, idempotency_key))
        if self.put_error:
            raise self.put_error
        return {"version": expected_version + 1}


class FakeClient(AbstractContextManager):
    def __init__(self, transport):
        self._remote = SimpleNamespace(_transport=transport)

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


class ApiFailure(RuntimeError):
    def __init__(self, code, status=0):
        self.code = code
        self.status = status


def _local_state(path: Path, *, size=1):
    value = {
        "skills": {
            "claude": {"synced_at": "2026-10-28T00:00:00+00:00", "skills": {
                "rendering": {"role": "main", "selected": True, "digest": "a" * size},
            }},
            "codex": {"synced_at": None, "skills": {}},
            "hermes": {"synced_at": None, "skills": {}},
        },
        "version": 1,
        "installs": {},
    }
    path.write_text(json.dumps(value), encoding="utf-8")
    return value


def _factory(transport):
    return lambda: FakeClient(transport)


def test_publish_gets_then_puts_once_with_versioned_idempotency(tmp_path):
    state_file = tmp_path / "skills.json"
    local = _local_state(state_file)
    transport = FakeTransport(get={"version": 7, "content": {"old": True}})

    result = publish(package_root=tmp_path, state_file=state_file, client_factory=_factory(transport))

    assert result == {"status": "published"}
    assert transport.gets == [app_state_key(tmp_path)]
    assert len(transport.puts) == 1
    key, content, expected_version, idempotency_key = transport.puts[0]
    assert key == app_state_key(tmp_path)
    assert content["format"] == "astrid.skills.v1"
    assert content["harnesses"] == local["skills"]
    assert content["install"] == {
        "id": app_state_key(tmp_path).rsplit(".", 1)[1],
        "package_root": str(tmp_path.resolve()),
        "state_path": str(state_file),
    }
    assert expected_version == 7
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert idempotency_key == hashlib.sha256(encoded + b"7").hexdigest()


@pytest.mark.parametrize(
    "error,reason",
    [
        (RuntimeError("offline"), "unavailable"),
        (ApiFailure("protocol_error"), "protocol_error"),
    ],
)
def test_get_failures_are_pending_and_leave_local_state_unchanged(tmp_path, error, reason):
    state_file = tmp_path / "skills.json"
    _local_state(state_file)
    before = state_file.read_bytes()
    transport = FakeTransport(get=error)

    assert publish(package_root=tmp_path, state_file=state_file, client_factory=_factory(transport)) == {
        "status": "pending", "reason": reason,
    }
    assert transport.puts == []
    assert state_file.read_bytes() == before


def test_timeout_is_bounded_and_does_not_change_local_state(tmp_path):
    state_file = tmp_path / "skills.json"
    _local_state(state_file)
    before = state_file.read_bytes()
    transport = FakeTransport(get=lambda _key: time.sleep(30))
    started = time.monotonic()

    result = publish(
        package_root=tmp_path,
        state_file=state_file,
        client_factory=_factory(transport),
        timeout=0.05,
    )

    assert time.monotonic() - started < 1
    assert result == {"status": "pending", "reason": "timeout"}
    assert transport.puts == []
    assert state_file.read_bytes() == before


def test_timeout_uses_eight_second_bound(tmp_path):
    state_file = tmp_path / "skills.json"
    _local_state(state_file)
    transport = FakeTransport(get=lambda _key: time.sleep(30))
    started = time.monotonic()

    assert publish(package_root=tmp_path, state_file=state_file, client_factory=_factory(transport)) == {
        "status": "pending", "reason": "timeout",
    }
    assert time.monotonic() - started < 9


def test_conflict_is_not_retried_and_oversize_skips_put(tmp_path):
    state_file = tmp_path / "skills.json"
    _local_state(state_file)
    conflict = ApiFailure("version_conflict", 409)
    transport = FakeTransport(put=conflict)
    assert publish(package_root=tmp_path, state_file=state_file, client_factory=_factory(transport)) == {
        "status": "pending", "reason": "version_conflict",
    }
    assert len(transport.gets) == 1 and len(transport.puts) == 1

    _local_state(state_file, size=20_000)
    too_large = FakeTransport()
    assert publish(package_root=tmp_path, state_file=state_file, client_factory=_factory(too_large)) == {
        "status": "too_large",
    }
    assert too_large.gets == [] and too_large.puts == []


def test_package_roots_get_distinct_keys(tmp_path):
    first, second = tmp_path / "one", tmp_path / "two"
    first.mkdir()
    second.mkdir()
    assert app_state_key(first) != app_state_key(second)


def test_default_connection_uses_only_no_start_launcher_method(tmp_path, monkeypatch):
    state_file = tmp_path / "skills.json"
    _local_state(state_file)
    transport = FakeTransport()
    calls = []

    def existing(cls):
        calls.append("existing")
        return FakeClient(transport)

    def start(cls, *_args, **_kwargs):
        calls.append("start")
        raise AssertionError("skills publication must not start Runtime")

    monkeypatch.setattr(AstridClient, "open_existing_from_launcher", classmethod(existing))
    monkeypatch.setattr(AstridClient, "open_from_launcher", classmethod(start))
    assert publish(package_root=tmp_path, state_file=state_file) == {"status": "published"}
    assert calls == ["existing"]


@pytest.mark.parametrize("reason", ["unavailable", "protocol_error", "timeout"])
def test_cli_pending_publish_does_not_change_exit_or_local_state(tmp_path, monkeypatch, capsys, reason):
    state_file = tmp_path / "skills.json"
    _local_state(state_file)
    before = state_file.read_bytes()
    monkeypatch.setattr(skills_cli, "install_fn", lambda **_kwargs: {"actions": []})
    monkeypatch.setattr(skills_cli, "publish", lambda **_kwargs: {"status": "pending", "reason": reason})

    assert skills_cli.main(["install", "rendering", "--json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["runtime_record"] == {"status": "pending", "reason": reason}
    assert state_file.read_bytes() == before


@pytest.mark.integration
def test_paired_runtime_publishes_and_reads_back_inventory(tmp_path, monkeypatch, real_runtime):
    daemon = real_runtime()
    state_file = tmp_path / "skills.json"
    inventory = {
        "claude": {"synced_at": "2026-10-28T12:00:00+00:00", "skills": {
            "rendering-worlds": {"role": "extra", "selected": True, "digest": "a" * 64},
        }},
        "codex": {"synced_at": "2026-10-28T12:01:00+00:00", "skills": {
            "rendering": {"role": "main", "selected": False, "digest": "b" * 64},
        }},
        "hermes": {"synced_at": None, "skills": {}},
    }
    state_file.write_text(json.dumps({"skills": inventory}), encoding="utf-8")
    monkeypatch.setenv("ASTRID_TIMELINE_EVAL_ENDPOINT", daemon.endpoint)
    monkeypatch.setenv("ASTRID_TIMELINE_EVAL_CREDENTIAL", str(daemon.credential_path))
    monkeypatch.setenv("ASTRID_TIMELINE_EVAL_REALM_ID", daemon.service.realm["id"])
    monkeypatch.setenv("ASTRID_TIMELINE_EVAL_ACTOR_ID", "owner")
    try:
        assert publish(package_root=tmp_path, state_file=state_file) == {"status": "published"}
        key = app_state_key(tmp_path)
        with AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=daemon.service.realm["id"],
            actor_id="owner",
        ) as client:
            record = client._remote._transport.get_user_app_state(key)
        assert record["content"]["harnesses"] == inventory
        assert record["content"]["format"] == "astrid.skills.v1"
        assert record["content"]["install"]["id"] == key.rsplit(".", 1)[1]
    finally:
        daemon.stop()
