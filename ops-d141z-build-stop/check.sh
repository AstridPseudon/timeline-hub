#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP_ROOT=$(mktemp -d /tmp/d141z-check.XXXXXX)
export D141Z_ROOT="$ROOT"
export D141Z_TMP="$TMP_ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

python3 - <<'PY'
import importlib.util
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

root = Path(os.environ["D141Z_ROOT"])
tmp = Path(os.environ["D141Z_TMP"])
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("candidate", root / "run-final-delivery.py")
candidate = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate)
life = importlib.import_module("delivery_lifecycle")

stub_sampler = tmp / "sampler.py"
stub_sampler.write_text(
    "import signal, sys, time\n"
    "trace, job, body, probe, ticks = sys.argv[1:]\n"
    "mode = __import__('os').environ.get('D141Z_SAMPLER_MODE', 'normal')\n"
    "stopping = False\n"
    "def stop(_sig, _frame):\n"
    "    global stopping\n"
    "    stopping = True\n"
    "signal.signal(signal.SIGTERM, stop)\n"
    "header = 'timestamp_utc\\tmonotonic_ns\\tavailable_bytes\\tjob_id\\tbody_pid\\tkind\\n'\n"
    "def row(value, kind):\n"
    "    with open(trace, 'a', encoding='utf-8') as out:\n"
    "        out.write(f'2026-01-01T00:00:{time.monotonic_ns() % 60:02d}Z\\t{time.monotonic_ns()}\\t{value}\\t{job}\\t{body}\\t{kind}\\n')\n"
    "Path = __import__('pathlib').Path\n"
    "Path(trace).write_text(header, encoding='utf-8')\n"
    "print('ready\\t1\\t1\\t0\\t600\\t1\\t' + '0' * 64, flush=True)\n"
    "row(5000000000, 'first')\n"
    "if mode == 'invalid':\n"
    "    raise SystemExit(9)\n"
    "if mode == 'frozen':\n"
    "    time.sleep(2)\n"
    "elif mode == 'lowduring':\n"
    "    time.sleep(0.08); row(3999999999, 'periodic'); time.sleep(2)\n"
    "else:\n"
    "    time.sleep(2)\n"
    "if stopping:\n"
    "    row(3999999999 if mode == 'lowafter' else 5000000000, 'final')\n"
    "else:\n"
    "    row(5000000000, 'final')\n"
)
stub_validator = tmp / "validator.py"
stub_validator.write_text(
    "import sys\n"
    "rows = open(sys.argv[1], encoding='utf-8').read().splitlines()\n"
    "if len(rows) < 3 or not rows[1].endswith('\\tfirst') or not rows[-1].endswith('\\tfinal'):\n"
    "    raise SystemExit(1)\n"
    "print('trace PASS')\n"
)
child = tmp / "child.py"
child.write_text(
    "import signal, sys, time\n"
    "pidfile, mode = sys.argv[1:]\n"
    "open(pidfile, 'w').write(str(__import__('os').getpid()))\n"
    "signal.signal(signal.SIGTERM, signal.SIG_IGN if mode == 'ignore' else signal.SIG_DFL)\n"
    "time.sleep(30)\n"
)
builder = tmp / "builder.py"
builder.write_text(
    "import subprocess, sys, time\n"
    "child, pidfile, mode = sys.argv[1:]\n"
    "p = subprocess.Popen([sys.executable, child, pidfile, mode], start_new_session=True)\n"
    "if mode == 'normal': time.sleep(0.15); p.terminate()\n"
    "elif mode == 'cadence': time.sleep(5.3); p.terminate()\n"
    "p.wait()\n"
)
wrapper = tmp / "wrapper.py"
wrapper.write_text(
    "import subprocess, sys\n"
    "raise SystemExit(subprocess.call([sys.executable, sys.argv[1], *sys.argv[2:]], start_new_session=True))\n"
)
driver = tmp / "driver.py"
driver.write_text(
    "import importlib, pathlib, sys, time, os, signal, threading\n"
    "life = importlib.import_module('delivery_lifecycle')\n"
    "life.TRACE_SCRIPT = pathlib.Path(sys.argv[1])\n"
    "life.TRACE_VALIDATOR = pathlib.Path(sys.argv[2])\n"
    "life.available_bytes = lambda _probe: 5000000000\n"
    "mode, tmp, builder, wrapper, pidfile, timeout, cancel = sys.argv[3:]\n"
    "__import__('os').environ['D141Z_SAMPLER_MODE'] = mode\n"
    "cancel_path = pathlib.Path(cancel) if cancel != '-' else None\n"
    "time.sleep(1.0)\n"
    "if os.environ.get('D141Z_SELF_SIGNAL'):\n"
    "    threading.Timer(2.0, lambda: os.kill(os.getpid(), int(os.environ['D141Z_SELF_SIGNAL']))).start()\n"
    "if os.environ.get('D141Z_SELF_CANCEL') and cancel_path is not None:\n"
    "    threading.Timer(2.0, lambda: cancel_path.write_text('cancel\\n')).start()\n"
    "code, _output, record = life.run_delivery([sys.executable, wrapper, builder, str(pathlib.Path(tmp) / 'child.py'), pidfile, mode], pathlib.Path(tmp), cancel_path=cancel_path, timeout_seconds=float(timeout))\n"
    "print(code)\n"
    "print(record)\n"
    "raise SystemExit(code)\n"
)

def assert_gone(pidfile: Path) -> None:
    if not pidfile.exists():
        return
    pid = int(pidfile.read_text())
    for _ in range(50):
        if not Path(f"/proc/{pid}").exists():
            return
        time.sleep(0.02)
    raise AssertionError(f"descendant {pid} survived stop")

def case(name: str, dispatch: int, mode: str, expected: int, *, timeout=1.0, sampler=None, sampler_mode=None, stale=15.0, caller=False) -> dict:
    case_dir = tmp / name
    case_dir.mkdir()
    pidfile = case_dir / "child.pid"
    life.TRACE_SCRIPT = Path(sampler or stub_sampler)
    life.TRACE_VALIDATOR = stub_validator
    life.SAMPLER_STALE_SECONDS = stale
    os.environ["D141Z_SAMPLER_MODE"] = sampler_mode or mode
    life.available_bytes = lambda _probe, value=dispatch: value
    command = [sys.executable, str(wrapper), str(builder), str(child), str(pidfile), mode]
    if caller:
        code, _out = candidate.run_wrapper(command, case_dir)
    else:
        code, _out, _record = life.run_delivery(command, case_dir, timeout_seconds=timeout)
    record = __import__("json").loads((case_dir / "timeline-delivery-KEEP" / "lifecycle.json").read_text())
    assert code == expected, (name, code, record)
    assert (case_dir / "timeline-delivery-KEEP" / "KEEP").is_file(), name
    assert (case_dir / "timeline-delivery-KEEP" / "lifecycle.json").is_file(), name
    if expected in {75, 124, 125, 130, 143}:
        assert record["status"] in {"stopped", "unknown", "refused"}, (name, record)
        assert_gone(pidfile)
    return record

assert candidate.run_wrapper.__code__.co_names.count("run_delivery") == 1
assert candidate.REVIEWED_BUILDER_SHA256 == "ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca"
bad = tmp / "bad"
bad.write_text("x")
link = tmp / "bad-link"
link.symlink_to(bad)
try:
    candidate.regular_file(link, "guard")
except ValueError:
    pass
else:
    raise AssertionError("symlink path guard was weakened")
try:
    candidate.checked_file(bad, "0" * 64, "guard")
except ValueError:
    pass
else:
    raise AssertionError("hash guard was weakened")

for sig, expected, name in ((signal.SIGTERM, 143, "sigterm"), (signal.SIGINT, 130, "sigint")):
    signal_dir = tmp / name
    signal_dir.mkdir()
    life.TRACE_SCRIPT = stub_sampler
    life.TRACE_VALIDATOR = stub_validator
    life.SAMPLER_STALE_SECONDS = 15.0
    os.environ["D141Z_SAMPLER_MODE"] = "ignore"
    life.available_bytes = lambda _probe: 5000000000
    threading.Timer(2.0, lambda sig=sig: os.kill(os.getpid(), sig)).start()
    code, _out, record = life.run_delivery([sys.executable, str(wrapper), str(builder), str(child), str(signal_dir / "child.pid"), "ignore"], signal_dir, timeout_seconds=10)
    assert code == expected, (name, code, record)
    assert_gone(signal_dir / "child.pid")

cancel = tmp / "cancel"
cancel_case = tmp / "cancel-case"
cancel_case.mkdir()
life.TRACE_SCRIPT = stub_sampler
life.TRACE_VALIDATOR = stub_validator
life.SAMPLER_STALE_SECONDS = 15.0
os.environ["D141Z_SAMPLER_MODE"] = "ignore"
life.available_bytes = lambda _probe: 5000000000
threading.Timer(2.0, lambda: cancel.write_text("cancel\n")).start()
code, _out, record = life.run_delivery([sys.executable, str(wrapper), str(builder), str(child), str(cancel_case / "child.pid"), "ignore"], cancel_case, cancel_path=cancel, timeout_seconds=10)
assert code == 130, ("cancel", code, record)
assert_gone(cancel_case / "child.pid")

case("normal", 5000000000, "normal", 0, caller=True)
case("low-before", 4859999999, "normal", 75)
case("low-during", 5000000000, "lowduring", 75)
case("low-after", 5000000000, "normal", 75, sampler_mode="lowafter")
case("sampler-invalid", 5000000000, "invalid", 125)
case("sampler-frozen", 5000000000, "ignore", 125, sampler_mode="frozen", stale=0.1)
missing = tmp / "missing-sampler.py"
case("sampler-missing", 5000000000, "normal", 125, sampler=missing)
case("timeout", 5000000000, "ignore", 124, timeout=0.15)

fakebin = tmp / "bin"
fakebin.mkdir()
(fakebin / "df").write_text("#!/bin/sh\nprintf 'Avail\\n5000000000\\n'\n")
(fakebin / "df").chmod(0o755)
old_path = os.environ["PATH"]
os.environ["PATH"] = str(fakebin) + os.pathsep + old_path
donor = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-disk-trace.py")
record = case("actual-5s-trace", 5000000000, "cadence", 0, timeout=8, sampler=donor)
trace = Path(record["trace"])
rows = trace.read_text().splitlines()
assert any(row.split("\t")[-1] == "periodic" for row in rows[1:]), rows
assert rows[1].split("\t")[-1] == "first" and rows[-1].split("\t")[-1] == "final"
assert record["trace_status"] == "PASS" and record["reaped_pids"]
os.environ["PATH"] = old_path

print("D141z acceptance PASS: normal, descendant TERM/KILL/reap, low-disk before/during/after, invalid/frozen/missing sampler, timeout, SIGTERM/SIGINT/cancel, trace/KEEP, and source guards")
PY
