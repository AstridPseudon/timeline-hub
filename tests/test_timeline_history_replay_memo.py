"""D42 memoizes only successful replay of complete, freshly captured inputs."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys

import pytest
import test_timeline_commit_port as port_tests
from test_timeline_commit_authentication import body, candidate, provider
from test_timeline_commit_port import commit

from runtime_protocol import timeline_commit_auth as auth
from runtime_protocol import timeline_commit_store as store_module
from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ProtocolError
from runtime_protocol.timeline_commit_store import TimelineCommitStore

service = port_tests.service


def setup_read(service, monkeypatch, *, sequential=False):
    provider(service)
    if sequential:
        def execute(context, port):
            prepared = candidate(context, port)
            source = port.revision_closure(prepared["expected_head"]["revision_id"])
            execution = {"evaluated_head": prepared["expected_head"], "records": prepared["records"],
                         "commands": [{"boundary": {k: v for k, v in prepared["records"]["commands"][0]["bindings"][0]["boundary"].items()
                                                    if k != "change_ordinal"},
                                       "input": source, "output": prepared["canonical_document"]}]}
            port.capture_sequential_execution({
                "schema_version": 1, "context": context, "original": execution, "landing": execution,
                "replay_bindings": [], "prepared_digest": validation.digest(prepared),
            })
            return port.accept(prepared)
        service.test_provider.action = execute
    accepted = commit(service, body(service))
    publication = accepted["receipt"]["receipt_id"]
    commits, _ = service._timeline_commits()
    calls = []
    validate = auth.validate

    def counted(*args, **kwargs):
        calls.append(None)
        return validate(*args, **kwargs)

    monkeypatch.setattr(auth, "validate", counted)

    def read():
        return commits.history_entry(service.test_project, "main", publication)

    return commits, publication, calls, read


def test_warm_history_skips_actual_replay_and_schema_work(service, monkeypatch):
    _, _, calls, read = setup_read(service, monkeypatch, sequential=True)
    schema_calls = []
    validate = auth.validate_commit_value

    def counted(*args, **kwargs):
        schema_calls.append(None)
        return validate(*args, **kwargs)

    monkeypatch.setattr(validation, "validate_commit_value", counted)
    first = read()
    assert calls
    cold_replays = len(calls)
    assert schema_calls
    cold_schemas = len(schema_calls)
    assert read() == first
    assert len(calls) == cold_replays
    assert len(schema_calls) == cold_schemas


def test_exact_json_byte_change_replays_even_with_identical_parsed_record(service, monkeypatch):
    _, publication, calls, read = setup_read(service, monkeypatch)
    first = read()
    conn = service.store.conn
    raw = conn.execute("SELECT records_json FROM timeline_commit_history WHERE publication_id=?",
                       (publication,)).fetchone()[0]
    conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?", (raw + " ", publication))
    assert read() == first
    assert len(calls) == 2
    read()
    assert len(calls) == 2


@pytest.mark.parametrize("version", ["replay", "schema", "validator"])
def test_schema_or_validator_change_misses(service, monkeypatch, version):
    _, _, calls, read = setup_read(service, monkeypatch)
    read()
    if version == "replay":
        monkeypatch.setattr(store_module, "_REPLAY_VALIDATOR_VERSION", 2)
    elif version == "schema":
        bundle, registry = validation._schema_resources()
        bundle = copy.deepcopy(bundle)
        bundle["$comment"] = "New installed schema version"
        monkeypatch.setattr(validation, "_schema_resources", lambda: (bundle, registry))
    else:
        validator = validation._validator
        monkeypatch.setattr(validation, "_validator", lambda definition: validator(definition))
    read()
    assert len(calls) == 2
    read()
    assert len(calls) == 2


def test_failed_replay_is_never_memoized(service, monkeypatch):
    commits, _, calls, read = setup_read(service, monkeypatch)
    validate = auth.validate
    failures = []

    def refused(*args, **kwargs):
        failures.append(None)
        raise ValueError("replay refused")

    before = len(commits._replay_memo)
    monkeypatch.setattr(auth, "validate", refused)
    for _ in range(2):
        with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
            read()
    assert len(failures) == 2
    assert len(commits._replay_memo) == before
    monkeypatch.setattr(auth, "validate", validate)
    read()
    read()
    assert len(calls) == 1


def test_memo_has_bounded_lru_eviction(service, monkeypatch):
    commits, publication, calls, read = setup_read(service, monkeypatch)
    monkeypatch.setattr(store_module, "_REPLAY_MEMO_LIMIT", 2)
    conn = service.store.conn
    raw = conn.execute("SELECT records_json FROM timeline_commit_history WHERE publication_id=?",
                       (publication,)).fetchone()[0]
    for suffix in ("", " ", "  ", " "):
        conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?",
                     (raw + suffix, publication))
        read()
        assert len(commits._replay_memo) <= 2
    assert len(calls) == 3
    conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?", (raw, publication))
    read()
    assert len(calls) == 4


def test_store_instance_and_process_are_cold(service, monkeypatch):
    commits, publication, calls, read = setup_read(service, monkeypatch)
    read()
    other = TimelineCommitStore(service.store, validate_prepared=commits.validate_prepared)
    assert not other._replay_memo
    other.history_entry(service.test_project, "main", publication)
    assert len(calls) == 2
    read()
    assert len(calls) == 2
    code = '''
import sys
from runtime_protocol.service import RuntimeService
from runtime_protocol import timeline_commit_auth as auth
runtime = RuntimeService(sys.argv[1])
commits, _ = runtime._timeline_commits()
assert not commits._replay_memo
calls = []
validate = auth.validate
def counted(*args, **kwargs):
    calls.append(None)
    return validate(*args, **kwargs)
auth.validate = counted
commits.history_entry(sys.argv[2], "main", sys.argv[3])
assert len(calls) == 1
runtime.close()
'''
    service.close()
    result = subprocess.run([sys.executable, "-c", code, str(service.store.root), service.test_project, publication],
                            env=os.environ.copy(), capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stderr


def test_caller_return_mutation_cannot_poison_replay_or_history(service, monkeypatch):
    _, _, calls, read = setup_read(service, monkeypatch)
    first = read()
    expected = copy.deepcopy(first)
    first["records"]["steps"][0]["patch"].clear()
    first["receipt"]["result"]["canonical_document"]["parent_revision"]["payload"].clear()
    first["publisher"] = "forged"
    assert read() == expected
    assert len(calls) == 1


@pytest.mark.parametrize("field", ["publisher", "realm"])
def test_actor_or_realm_change_cannot_reuse_warm_entry(service, monkeypatch, field):
    _, publication, calls, read = setup_read(service, monkeypatch)
    read()
    if field == "publisher":
        conn = service.store.conn
        raw = conn.execute("SELECT result_json FROM command_idempotency WHERE txn_id=?", (publication,)).fetchone()[0]
        result = json.loads(raw)
        result["publisher"] = "forged"
        conn.execute("UPDATE command_idempotency SET result_json=? WHERE txn_id=?", (json.dumps(result), publication))
        with pytest.raises(ProtocolError):
            read()
        assert len(calls) == 1
    else:
        conn = service.store.conn
        old = conn.execute("SELECT realm_id FROM projects WHERE id=?", (service.test_project,)).fetchone()[0]
        conn.execute("INSERT INTO realm SELECT id || '-migrated', display_name, created_at, updated_at "
                     "FROM realm WHERE id=?", (old,))
        conn.execute("UPDATE projects SET realm_id=? WHERE id=?", (old + "-migrated", service.test_project))
        read()
        assert len(calls) == 2
