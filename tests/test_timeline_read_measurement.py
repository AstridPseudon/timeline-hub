"""Check native diagnostic timers without opening a server or a socket."""
from __future__ import annotations

import copy
import json
import runpy
from pathlib import Path

import pytest

from runtime_protocol import server
from runtime_protocol import timeline_commit_inputs as inputs
from runtime_protocol import timeline_commit_port as port
from runtime_protocol import timeline_commit_store as store
from runtime_protocol import timeline_commit_validation as validation


@pytest.mark.parametrize("mode", ["plain", "detail", "accounting"])
def test_diagnostic_separates_plain_timing_from_accounting(tmp_path, monkeypatch, mode):
    class FakePort:
        def __init__(self):
            self._RequestCommitPort__request = {"label": "test read"}

        def _read(self, call):
            return call()

        def close(self):
            pass

    # Register every instrumentation target for restoration after run_path.
    targets = [(copy, "deepcopy"), (validation, "finite_json"), (validation, "detached"),
               (inputs, "finite_json"), (inputs, "capture_document_input"),
               (port, "detached"), (store, "detached"), (server.RuntimeHandler, "_send")]
    targets.extend((store.TimelineCommitStore, name) for name in
                   ("head", "history_entry", "history", "revision_closure", "_history_entry_view", "_history_view"))
    originals = {(module, name): getattr(module, name) for module, name in targets}
    for (module, name), original in originals.items():
        monkeypatch.setattr(module, name, original)
    monkeypatch.setattr(port, "RequestCommitPort", FakePort)
    monkeypatch.setenv("D111B_ENABLED", "1")
    monkeypatch.setenv("D111B_MODE", mode)
    monkeypatch.setenv("D111B_LOG_DIR", str(tmp_path))
    monkeypatch.setenv("D111B_RUN_ID", "unit-test")
    diagnostic = Path(__file__).resolve().parents[1] / "diagnostics/sitecustomize_d111b.py"
    namespace = runpy.run_path(str(diagnostic))
    if mode == "plain":
        for (module, name), original in originals.items():
            if name != "_send":
                assert getattr(module, name) is original
    instance = FakePort()
    value = {"items": [{"nested": [1, 2, 3]}]}
    actual = instance._read(lambda: instance._read(lambda: validation.detached(value)))
    assert actual == value and actual is not value
    actual["items"].clear()
    assert value["items"]
    reads = namespace["states"][id(instance)]["reads"]
    assert len(reads) == 1
    record = reads[0]
    assert record["port_read_ns"] > 0
    if mode == "plain":
        assert set(record) == {"operation", "operations", "port_read_ns"}
    else:
        assert record["deepcopy_calls"] == record["finite_json_calls"] == record["detached_calls"] == 1
        if mode == "accounting":
            size = len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode())
            assert record["deepcopy_bytes"] == record["finite_json_bytes"] == record["detached_bytes"] == size
        else:
            assert not any(key.endswith("_bytes") for key in record)
