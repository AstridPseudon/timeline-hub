"""Canonical birth text changes with neither observer timezone nor locale."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from astrid.core.execution import custody_broker as custody
from astrid.core.execution import process_group as groups
from astrid.core.execution import remotion_host_session as host
from astrid.core.execution import remotion_pipe as pipe


@pytest.mark.skipif(sys.platform != "darwin", reason="native Darwin birth census")
def test_same_live_native_child_birth_across_timezone_and_locale(tmp_path):
    source = str(Path(__file__).resolve().parents[3])
    code = """import json,locale,os,sys,time
sys.path.insert(0,sys.argv[1])
from astrid.core.execution.process_group import process_birth_identity
from astrid.core.execution.custody_broker import default_process_identity
for line in sys.stdin:
 zone,language=json.loads(line)
 os.environ['TZ']=zone;time.tzset();locale.setlocale(locale.LC_ALL,language)
 print(json.dumps({'pid':os.getpid(),'birth':process_birth_identity(),
                   'identity':default_process_identity(os.getpid()),
                   'zone':time.strftime('%z'),'locale':locale.setlocale(locale.LC_ALL)}),flush=True)
"""
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "TZ": "UTC", "LC_ALL": "C"}
    process = subprocess.Popen([sys.executable, "-I", "-B", "-c", code, source],
                               env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True)
    try:
        original = groups.process_birth_identity(process.pid)
        assert original
        contexts = [("UTC", "C"), ("Europe/Berlin", "de_DE.UTF-8"),
                    ("Pacific/Honolulu", "fr_FR.UTF-8")]
        offsets, languages = set(), set()
        for context in contexts:
            process.stdin.write(json.dumps(context) + "\n")
            process.stdin.flush()
            import select
            assert select.select([process.stdout], [], [], 5)[0]
            observed = json.loads(process.stdout.readline())
            assert process.poll() is None
            assert observed["pid"] == process.pid
            assert observed["birth"] == original == groups.process_birth_identity(process.pid)
            assert observed["identity"] == custody.default_process_identity(process.pid)
            assert observed["identity"]["birth_id"] == original
            offsets.add(observed["zone"]); languages.add(observed["locale"])
        assert len(offsets) == len(languages) == 3
        process.stdin.close()
        assert process.wait(timeout=5) == 0
    finally:
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        for stream in (process.stdin, process.stdout):
            stream.close()


@pytest.mark.parametrize("mutation", ["pid", "birth", "missing", "unprovable"])
def test_bootstrap_retains_exact_original_incarnation_fence(monkeypatch, mutation):
    birth = custody._ps_lstart_birth(1791421200)
    binding = {"purpose": "rendering.timeline_visualize", "pid": os.getpid(),
               "birth": birth, "executable": str(Path(sys.executable).resolve())}
    if mutation == "pid":
        binding["pid"] += 1
    elif mutation == "birth":
        binding["birth"] = custody._ps_lstart_birth(1791421201)
    elif mutation == "missing":
        binding.pop("birth")
    monkeypatch.setattr(host, "_client", None)
    monkeypatch.setattr(pipe, "process_birth_identity", lambda: "" if mutation == "unprovable" else birth)
    raw = pipe._encode({"protocol": pipe.VERSION, "binding": binding,
                        "digest": hashlib.sha256(pipe._encode(binding)).hexdigest()})
    monkeypatch.setattr(pipe, "_line", lambda *args, **kwargs: raw)
    monkeypatch.setattr(pipe, "ExecutorPipeChannel", lambda *args: pytest.fail("unproved incarnation installed"))
    with pytest.raises(ValueError, match="original executor incarnation"):
        pipe.install_executor_client()
    assert host.host_remotion_client() is None


def test_darwin_identity_observation_failure_remains_refusal(monkeypatch):
    monkeypatch.setattr(custody.sys, "platform", "darwin")
    def unavailable(*args):
        raise custody.CustodyError("native census unavailable")
    monkeypatch.setattr(custody, "_darwin_process_records", unavailable)
    monkeypatch.setattr(groups, "_darwin_process_records", unavailable)
    with pytest.raises(custody.CustodyError, match="unavailable"):
        custody.default_process_identity(os.getpid())
    with pytest.raises(custody.CustodyError, match="unavailable"):
        groups.process_birth_identity()


def test_invalid_birth_instant_remains_refusal():
    with pytest.raises(custody.CustodyError, match="birth is invalid"):
        custody._ps_lstart_birth(10 ** 100)
