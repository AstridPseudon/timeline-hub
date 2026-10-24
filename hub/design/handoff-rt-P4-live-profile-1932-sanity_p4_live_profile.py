"""Finite instrumentation checks. No daemon, sockets, bodies or timing evidence."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

path = Path(__file__).with_name("p4_live_profile.py")
spec = importlib.util.spec_from_file_location("p4_live_profile", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory(prefix="p4-profile-sanity-", dir=os.environ["TMPDIR"]) as temp:
    capture = module.Capture(Path(temp) / "capture")
    daemon = SimpleNamespace(instance_id="SANITY-ONLY", service=object())
    server = SimpleNamespace(daemon_runtime=daemon, runtime=daemon.service)
    daemon.httpd = server
    handler = SimpleNamespace(server=server, headers={"Idempotency-Key": "p4-ten-note-redo-note-1"},
                              command="POST", path="/SANITY-ONLY")
    seen = []

    def dispatched(instance, sentinel):
        assert instance is handler
        seen.append(instance)
        if sentinel is ValueError:
            raise ValueError("SANITY-ONLY")
        return sentinel

    wrapped = capture.handler(dispatched)
    result = object()
    assert wrapped(handler, result) is result
    try:
        wrapped(handler, ValueError)
    except ValueError as error:
        assert str(error) == "SANITY-ONLY"
    else:
        raise AssertionError("exception changed")
    assert len(seen) == 2
    # An unattached handler must delegate untouched, without another profile.
    daemon.httpd = object()
    assert wrapped(handler, result) is result
    assert capture.sequence == 2
    capture.finish(0, [])
    summary = json.loads((capture.directory / "summary.json").read_text())
    assert summary["handler_count"] == 2
    assert summary["boundaries"][1]["error_type"] == "ValueError"
    assert summary["boundaries"][0]["idempotency_key"] == "p4-ten-note-redo-note-1"
    assert summary["boundaries"][0]["pid"] == os.getpid()
    assert summary["per_note_undo_redo"]["note-1"]["redo"]["error_type"] == "ValueError"
    assert summary["calls"] == dict.fromkeys(module.counters(module.pstats.Stats(str(capture.directory / "handlers.prof"))), 0)
    assert summary["top10_cumulative"]
    assert len((capture.directory / "events.jsonl").read_text().splitlines()) == 4
    try:
        module.Capture(capture.directory)
    except FileExistsError:
        pass
    else:
        raise AssertionError("existing output could be overwritten")

# Static source linkage: fixture invokes RuntimeHandler; daemon supplies itself.
agent = Path("/home/user/work/agent")
fixture = (agent / "tests/editing_conformance/test_native_batch_ingress.py").read_text()
assert "RuntimeHandler(sock, ('127.0.0.1', 1), server)" in fixture
assert "server = daemon.httpd" in fixture
runtime = Path("/home/user/work/wt/rt-P4-live-profile-sol-1932")
daemon_source = (runtime / "runtime_protocol/daemon.py").read_text()
assert "self.httpd.daemon_runtime = self" in daemon_source
assert "self.httpd.runtime = self.service" in daemon_source
assert module.TARGET.endswith("::test_http_ten_note_commit_per_step_inverse_and_redo")
# Exercise the installation hook against the actual class without calling it.
sys.path.insert(0, str(runtime))
from runtime_protocol.server import RuntimeHandler
with tempfile.TemporaryDirectory(prefix="p4-profile-hook-sanity-", dir=os.environ["TMPDIR"]) as temp:
    capture = module.Capture(Path(temp) / "capture")
    module._capture = capture
    original = RuntimeHandler._dispatch
    hook = module.pytest_runtest_call(SimpleNamespace(nodeid=module.TARGET))
    next(hook)
    assert RuntimeHandler._dispatch is not original
    assert RuntimeHandler._dispatch.__wrapped__ is original
    try:
        next(hook)
    except StopIteration:
        pass
    assert RuntimeHandler._dispatch is original
    module._capture = None
print("PASS: finite helper delegation, exception, scope, raw profile, counts, output and source-link checks")
print("SANITY ONLY: no authentic P4 body and no performance measurements")
