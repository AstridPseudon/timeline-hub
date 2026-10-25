"""Private native read timers; byte accounting runs in a separate lifecycle."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import threading
import time
from pathlib import Path

if os.environ.get("D111B_ENABLED") == "1":
    from runtime_protocol import timeline_commit_inputs as inputs
    from runtime_protocol import timeline_commit_port as port
    from runtime_protocol import timeline_commit_store as store
    from runtime_protocol import timeline_commit_validation as validation

    mode = os.environ["D111B_MODE"]
    assert mode in {"plain", "detail", "accounting"}
    output = Path(os.environ["D111B_LOG_DIR"])
    local = threading.local()
    records = []
    states = {}

    def module_identity(module):
        path = module.__file__
        assert path is not None
        return {"path": path, "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}

    def instrument(module, name, category):
        original = getattr(module, name)

        def measured(*args, **kwargs):
            record = getattr(local, "record", None)
            depth = getattr(local, category, 0)
            setattr(local, category, depth + 1)
            started = time.perf_counter_ns()
            try:
                result = original(*args, **kwargs)
            finally:
                elapsed = time.perf_counter_ns() - started
                setattr(local, category, depth)
            if record is not None and depth == 0:
                record[category + "_ns"] = record.get(category + "_ns", 0) + elapsed
                record[category + "_calls"] = record.get(category + "_calls", 0) + 1
                if category == "store":
                    operation = {"name": name, "ns": elapsed}
                    if name in {"history_entry", "_history_entry_view"}:
                        operation["publication_id"] = result["publication_id"]
                    record["operations"].append(operation)
                if mode == "accounting" and category != "store":
                    value = args[0]
                    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
                    record[category + "_bytes"] = record.get(category + "_bytes", 0) + len(encoded)
            return result

        setattr(module, name, measured)

    # Plain mode changes only _read and close: no hashing, serialisation,
    # recursive wrappers or operation accounting runs inside its timer.
    if mode != "plain":
        instrument(copy, "deepcopy", "deepcopy")
        instrument(validation, "finite_json", "finite_json")
        inputs.finite_json = validation.finite_json
        instrument(validation, "detached", "detached")
        port.detached = store.detached = validation.detached
        for name in ("head", "history_entry", "history", "revision_closure", "_history_entry_view", "_history_view"):
            instrument(store.TimelineCommitStore, name, "store")
        instrument(inputs, "capture_document_input", "source_store")

    original_read = port.RequestCommitPort._read
    original_close = port.RequestCommitPort.close

    def measured_read(self, call):
        previous = getattr(local, "record", None)
        # Nested _read calls belong to the one ordinary top-level interval.
        if previous is not None:
            return original_read(self, call)
        state = states.setdefault(id(self), {"label": self._RequestCommitPort__request.get("label"), "reads": []})
        record = {"operation": call.__qualname__, "operations": []}
        if mode != "plain":
            record["source_document_calls"] = int(call.__qualname__.startswith("RequestCommitPort._document."))
        local.record = record
        started = time.perf_counter_ns()
        try:
            return original_read(self, call)
        finally:
            record["port_read_ns"] = time.perf_counter_ns() - started
            local.record = previous
            state["reads"].append(record)

    def measured_close(self):
        try:
            return original_close(self)
        finally:
            state = states.pop(id(self), None)
            if state is not None:
                records.append(state)
                modules = {module.__name__: module_identity(module)
                           for module in (port, store, sys.modules["astrid.sdk.timeline.commit"])}
                (output / "port-metrics.json").write_text(json.dumps({"mode": mode, "sys_setprofile": False, "modules": modules, "records": records}) + "\n")

    port.RequestCommitPort._read = measured_read
    port.RequestCommitPort.close = measured_close

    from runtime_protocol import server

    original_send = server.RuntimeHandler._send

    def measured_send(self, status, *args, **kwargs):
        tag = self.headers.get("X-D111B-Refusal-Tag")
        if tag:
            print(f"D111b refusal tag={tag} status={status}", file=sys.stderr, flush=True)
        return original_send(self, status, *args, **kwargs)

    server.RuntimeHandler._send = measured_send
    print(f"D111b startup run={os.environ['D111B_RUN_ID']} mode={mode}", file=sys.stderr, flush=True)
