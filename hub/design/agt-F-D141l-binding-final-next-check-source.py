#!/usr/bin/env python3
"""Executable source/control checks; never submits or admits a service job."""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import stat
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ROOT = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-final-next/evidence")
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
ORIGINAL = {
    "receipt": str(ORCH / "workers/agt-F-D141i-cut-controller-0249/evidence/admission.json"),
    "receipt_sha256": "5fbdab93245696b725f7b67eca44f02d939536c8f6e5d6c6678ea628de4b5a35",
    "brief": str(ORCH / "workers/agt-F-D141i-cut-controller-0249/brief.md"),
    "brief_sha256": "379e1eb69b3f5e589346ac2cced4e19035ce449ce9d1075c5128be74c77137b5",
    "schema": "timeline.agent.d141i.cut-controller.admission.v1",
    "controller": "agt-F-D141i-cut-controller-0249",
    "service_id": "agent-agent-core-full-1026025151-24049",
    "floor": 4700000000,
}
EXPECTED_FILES = {
    "command-cut.sh", "command-pristine.sh", "check-source.py", "tiny-controls.sh",
    "positive-stub.sh", "positive.manifest", "poison.manifest", "rows.txt",
    "binding-source.py", "controller-continuation.sh",
    "admission-derivation.json", "owner-brief.txt",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def run(argv, **kwargs):
    return subprocess.run(argv, capture_output=True, check=True, **kwargs).stdout


def manifest():
    return load(ROOT / "source-manifest.json")


def artifacts():
    bindings = manifest()["file_sha256"]
    require(set(bindings) == EXPECTED_FILES, "incomplete source hash set")
    for name, expected in bindings.items():
        require(digest(ROOT / name) == expected, "source hash changed: " + name)
    for name, expected in manifest()["retained_original_sha256"].items():
        require(digest(name) == expected, "retained original changed: " + name)
    derivative = manifest()["derivative"]
    require(derivative["source_commit"] == "6a2d1c22ec800229812f4d756d7198aece8111ed"
            and derivative["source_tree"] == "57f68e1fad9c84ce0c0a2fa10f9a2f8defb1a847", "incorrect derivative base tree")
    for name, expected in derivative["original_sha256"].items():
        require(digest(Path(derivative["original_root"]) / name) == expected, "original0735 changed: " + name)
    for path, expected in manifest()["native_source_sha256"].items():
        require(digest(path) == expected, "native operational source changed: " + path)
    for name, expected in derivative["predecessor_sha256"].items():
        require(digest(Path(derivative["predecessor_root"]) / name) == expected, "Sol-next changed: " + name)
    brief = manifest()["owner_brief"]
    require(brief["path"] == str(ROOT / "owner-brief.txt") and digest(brief["path"]) == brief["sha256"], "assigned brief hash/path")
    require(Path(brief["path"]).read_bytes() == (ROOT.parent / "brief.md").read_bytes(), "brief snapshot is not the actual assigned brief")
    require(Path(brief["path"]).stat().st_mode & 0o222 == 0, "brief snapshot writable")
    require((ROOT / "positive.manifest").resolve() != (ROOT / "source-manifest.json").resolve(),
            "command manifest and source manifest alias")
    require(digest(ROOT / "positive.manifest") != digest(ROOT / "source-manifest.json"),
            "manifest/source-manifest bytes unexpectedly equal")


def sources(mode):
    artifacts()
    data = manifest()
    group = "integrated" if mode == "cut" else "pristine"
    result = {}
    # The pristine comparator still retains the current normal receiving tuple.
    groups = ["integrated"] if mode == "cut" else ["integrated", "pristine"]
    for which in groups:
        for label, expected in data[which].items():
            path = Path(expected["path"])
            require(path.resolve(strict=True) == path, "checkout path alias: " + str(path))
            def git(*args):
                return run(["git", "--no-optional-locks", "-C", str(path), *args], text=True).strip()
            actual = {"path": str(path), "sha": git("rev-parse", "HEAD"),
                      "tree": git("rev-parse", "HEAD^{tree}"),
                      "parents": git("rev-list", "--parents", "-n", "1", "HEAD")}
            require(actual == expected, "current checkout tuple differs: " + str(path))
            require(git("status", "--porcelain", "--untracked-files=all") == "", "dirty checkout: " + str(path))
            result[which + "." + label] = actual
    for relative, expected_hash in data["protected_tests"]["sha256"].items():
        require(digest(Path(data["integrated"]["agent"]["path"]) / relative) == expected_hash, "protected test changed: " + relative)
    agent = Path(data[group]["agent"]["path"])
    for relative in data["roots"][mode]:
        require((agent / relative).exists(), "missing source selector: " + str(agent / relative))
    for relative in data["absent_pristine_roots"]:
        require(not (Path(data["pristine"]["agent"]["path"]) / relative).exists(),
                "pristine N/A root now exists: " + relative)
    for name, binding in data["receipts"].items():
        require(digest(binding["path"]) == binding["sha256"], "owner receipt changed: " + name)
    ar = load(data["receipts"]["agent-U4a-D141-postREG-home-0622.json"]["path"])
    app = load(data["receipts"]["app-D141s-postREG-source-home-0545.json"]["path"])
    app_final = load(data["receipts"]["app-D141w-final-catchup-source-home-0734.json"]["path"])
    normal = data["integrated"]
    require(ar["schema"] == "agent.manager.normal-home-receipt.v1" and ar["clean"] is True,
            "Agent normal-home receipt shape")
    require((ar["head"], ar["tree"]) == (normal["agent"]["sha"], normal["agent"]["tree"]), "Agent receipt tuple")
    require(ar["runtime_head"] == normal["runtime"]["sha"], "Agent receipt Runtime binding")
    require(ar["parents"] == normal["agent"]["parents"].split()[1:], "Agent receipt parents")
    require(digest(Path(normal["agent"]["path"]) / "runtime.lock.json") == ar["runtime_lock_sha256"], "Agent lock receipt hash")
    require(digest(ar["queue_receipt"]) == ar["queue_sha256"], "Agent home merge receipt hash")
    # The retained 0545 receipt is historical and remains bound to App 4de.
    # The new 82e App input is authenticated by the checkout tuple above; a
    # future normal-home receipt may be attached by ordinary sync, but is not
    # fabricated or silently retargeted here.
    require(app["app"]["head"] == "4de54db14bdc9ddc2ce2e5887258b03acbffd30d",
            "historical App receipt was rewritten")
    require((app_final["head"], app_final["tree"]) == (normal["app"]["sha"], normal["app"]["tree"])
            and app_final["clean"] is True and app_final["candidate_tree_equals_home"] is True,
            "final App 82e home receipt tuple")
    result["receipts"] = data["receipts"]
    result["app_receipt_agent_observation"] = app["agent"]
    result["app_receipt_status"] = "historical_4de_retained; new_82e_input_tuple_checked"
    result["app_final_receipt"] = data["receipts"]["app-D141w-final-catchup-source-home-0734.json"]
    return json.dumps(result, sort_keys=True)


def validate_original(receipt, brief, binding=ORIGINAL):
    """The proved 0309 fixed-path, fixed-hash original receipt/brief checks."""
    receipt, brief = Path(receipt), Path(brief)
    record = load(receipt)
    witness = record["manager_dispatch_witness"]
    require(record["schema"] == binding["schema"], "unknown original receipt schema")
    require(record["controller"] == binding["controller"], "wrong original controller")
    require(record["service_id"] == binding["service_id"], "wrong original service")
    require(type(witness["free_bytes"]) is int and witness["free_bytes"] >= binding["floor"]
            and witness["required_bytes"] == binding["floor"] and witness["comparison"] == "PASS",
            "original dispatch was not admitted")
    require(str(receipt) == binding["receipt"] and digest(receipt) == binding["receipt_sha256"],
            "original admission receipt binding mismatch")
    require(str(brief) == binding["brief"] and digest(brief) == binding["brief_sha256"],
            "original manager brief binding mismatch")
    statement = (f"MANAGER actual dispatch witness: {witness['utc']} "
                 f"shutil.disk_usage.free={witness['free_bytes']} bytes >={binding['floor']};")
    require(statement in brief.read_text(), "original manager dispatch witness missing")
    return record


def admitted_dispatch(*args):
    if len(args) != 6:
        raise ValueError("admission requires receipt brief mode command manifest source-manifest")
    run([sys.executable, "-P", str(ROOT / "binding-source.py"), "admission", *args])


def item(path, hashed=True):
    path = Path(path)
    require(path.resolve(strict=True) == path, "custody path alias: " + str(path))
    s = path.lstat()
    require(stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode), "custody path type: " + str(path))
    result = {"inode": s.st_ino, "device": s.st_dev, "uid": s.st_uid, "gid": s.st_gid,
              "mode": stat.S_IMODE(s.st_mode), "path": str(path)}
    if hashed and path.is_file():
        result["sha256"] = digest(path)
    return result


OUTPUTS = ["raw-stdout.log", "raw-stderr.log", "runner.log", "agent-core-full.xml", "disk-trace.txt"]


def custody_before(root, inputs):
    root = Path(root)
    require(item(root)["mode"] == 0o700 and item(root)["uid"] == os.getuid(), "run directory custody")
    fixed = [root / n for n in ["KEEP", "source-before.txt", "interpreter.txt", "callerargv.txt", "service.txt"]]
    require((root / "KEEP").read_bytes() == b"KEEP" and item(root / "KEEP")["mode"] == 0o444, "KEEP state")
    result = {"fixed": [item(p) for p in fixed + list(map(Path, inputs))],
              "mutable": [item(root / n, False) for n in OUTPUTS], "directory": item(root)}
    (root / "custody-before.json").write_text(json.dumps(result, sort_keys=True) + "\n")


def custody_after(root, started):
    root = Path(root)
    before = load(root / "custody-before.json")
    require(item(root) == before["directory"], "run directory metadata changed")
    for old in before["fixed"]:
        require(item(old["path"]) == old, "fixed custody changed: " + old["path"])
    for old in before["mutable"]:
        require(item(old["path"], False) == old, "output identity/mode changed: " + old["path"])
    require((root / "source-before.txt").read_bytes() == (root / "source-after.txt").read_bytes(), "source changed across body")
    if int(started):
        stdout = (root / "raw-stdout.log").read_bytes()
        stderr = (root / "raw-stderr.log").read_bytes()
        require(bool(stdout or stderr), "both raw streams empty")
        expected_log = b"--- raw stdout ---\n" + stdout + b"--- raw stderr ---\n" + stderr
        require((root / "runner.log").read_bytes() == expected_log, "raw/runner log dataflow differs")
        xml = ET.parse(root / "agent-core-full.xml").getroot()
        suites = [xml] if xml.tag == "testsuite" else list(xml.iter("testsuite"))
        require(sum(int(s.get("tests", "0")) for s in suites) > 0, "JUnit has no tests")
        require(xml.tag in {"testsuite", "testsuites"}, "JUnit root")
        require(len(list(xml.iter("testcase"))) > 0, "JUnit has no cases")
        runner = (root / "runner-exit.txt").read_text().strip()
        if runner == "runner_exit=0":
            require(not list(xml.iter("failure")) and not list(xml.iter("error"))
                    and all(int(s.get("failures", "0")) == 0 and int(s.get("errors", "0")) == 0 for s in suites),
                    "zero body exit conflicts with JUnit failures")
        require(shlex.split((root / "callerargv.txt").read_text()), "empty caller argv")
        require((root / "interpreter.txt").stat().st_size and (root / "service.txt").stat().st_size, "missing interpreter/service witness")
    trace = (root / "disk-trace.txt").read_text().splitlines()
    require(trace and any("phase=after_body\t" in x for x in trace), "missing terminal disk sample")
    times = []
    for line in trace:
        fields = dict(x.split("=", 1) for x in line.split("\t"))
        int(fields["available_bytes"])
        times.append(datetime.datetime.fromisoformat(fields["utc"].replace("Z", "+00:00")))
    require(all(0 <= (b-a).total_seconds() <= 6 for a, b in zip(times, times[1:])), "disk trace gap exceeds five-second sampler allowance")
    # Freeze completed outputs, then retain and verify EVERY content hash.
    for p in root.rglob("*"):
        require(not p.is_symlink(), "symlink in retained output")
        if p.is_file():
            p.chmod(0o444 if p.name == "KEEP" else 0o400)
    after = [item(p) for p in sorted(root.rglob("*")) if p.name != "custody-after.json"]
    out = root / "custody-after.json"
    out.write_text(json.dumps(after, sort_keys=True) + "\n")
    out.chmod(0o400)
    verify_seal(root)


def verify_seal(root):
    root = Path(root)
    sealed = load(root / "custody-after.json")
    expected_paths = {entry["path"] for entry in sealed}
    actual_paths = {str(p) for p in root.rglob("*") if p.name not in {"custody-after.json", "status.txt"}}
    require(actual_paths == expected_paths - {str(root / "status.txt")}, "sealed file inventory changed")
    for expected in sealed:
        require(item(expected["path"]) == expected, "sealed custody mismatch: " + expected["path"])


def shell_argv(mode):
    command = ROOT / f"command-{mode}.sh"
    script = 'source "$1"; configure; REQUEST_ID=isolated-argv-control; build_argv; printf "%s\\0" "${BODY_ARGV[@]}"'
    return run(["/bin/bash", "--noprofile", "--norc", "-c", script, "_", str(command)]).decode().split("\0")[:-1]


def verify_argv():
    data = manifest()
    common = None
    for mode in ["cut", "pristine"]:
        argv = shell_argv(mode)
        group = "integrated" if mode == "cut" else "pristine"
        agent, runtime = [data[group][r]["path"] for r in ["agent", "runtime"]]
        xml = str(ROOT / f"private-control-logs/run-{mode}/agent-core-full.xml")
        pytest = ["-m", "pytest", "-q", "-n3", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45", f"--junitxml={xml}"] + data["roots"][mode]
        prefix = ["env", "-i", "HOME=/root", "LANG=C.UTF-8", "LC_ALL=C.UTF-8", "PYTHONDONTWRITEBYTECODE=1", "PYTHONNOUSERSITE=1",
                  f"PYTHONPATH={agent}:{runtime}", "PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin",
                  "VIRTUAL_ENV=/home/user/work/venv-agent", f"ASTRID_RUNTIME_CHECKOUT={runtime}", f"ASTRID_RUNTIME_SOURCE_ROOT={runtime}",
                  "ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110",
                  "ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node",
                  "ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules"]
        if mode == "cut":
            expected = prefix + [f"P4_D73_MANIFEST={ROOT}/positive.manifest", f"P4_D73_EVIDENCE={ROOT}/private-control-logs/run-cut/launcher-evidence", "P4_D73_REQUEST_ID=isolated-argv-control",
                                 "/bin/bash", "--noprofile", "--norc", "-c", 'exec "$@"', "_", agent + "/tools/p4-d73-pinned-launch.sh", str(ROOT / "positive.manifest"), "run", "--"] + pytest
        else:
            expected = prefix + ["/bin/bash", "--noprofile", "--norc", "-c", 'unset PYTHONNOUSERSITE; exec "$@"', "_", "/home/user/work/venv-agent/bin/python", "-P"] + pytest
        require(argv == expected, "shell-generated argv differs: " + mode)
        # Execute just the shell's exec forwarding against /bin/printf, never pytest.
        wrapper = argv.index("-c")
        forwarded = run(argv[wrapper-3:wrapper+3] + ["/usr/bin/printf", "%s\\0"] + pytest)
        require(forwarded.decode().split("\0")[:-1] == pytest, "shell forwarding changed pytest argv")
        normalized = [x if "=" not in x else x.split("=", 1)[0] + "=" + {agent: "AGENT", runtime: "RUNTIME", agent + ":" + runtime: "AGENT:RUNTIME"}.get(x.split("=", 1)[1], x.split("=", 1)[1]) for x in prefix]
        if common is not None:
            require(common == normalized, "cut/pristine environment differs")
        common = normalized

def admission_controls(scratch):
    """Exercise real controller functions and bounded native source excerpts.

    Only ORCH paths and polling delay are relocated. The queue actor below is
    a dependency double; it is never represented as a real dispatcher receipt.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("owned_binding", ROOT / "binding-source.py")
    binding = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(binding)
    fixture = scratch / "native-route"
    for name in ("bin", "tests", "queue/pending"):
        (fixture / name).mkdir(parents=True, exist_ok=True)
    suite = fixture / "tests/suites.conf"
    original = "# outside bytes retained  \nagent agent-core-full /bin/bash /bin/old\nruntime untouched /bin/true\n"
    suite.write_text(original)
    suite.chmod(0o600)
    excerpts = {}
    for name in ("request-test", "wait-test", "request-stop-test"):
        source = (ORCH / "bin" / name).read_text()
        relocated = source.replace("O=" + str(ORCH), "O=" + str(fixture))
        require(relocated != source, "native ORCH relocation failed")
        path = fixture / "bin" / name
        path.write_text(relocated)
        path.chmod(0o700)
        excerpts[name] = {"original_sha256": digest(ORCH / "bin" / name),
                          "relocated_sha256": digest(path), "changes": "O path only"}
    # A local sleep dependency shortens polling without changing wait-test.
    sleep = fixture / "bin/sleep"
    sleep.write_text("#!/bin/sh\nexec /bin/sleep .01\n")
    sleep.chmod(0o700)
    native = (ORCH / "bin/test-run").read_text()
    terminal = native[native.index('ST=fail;'):native.index('# zero executed tests')]
    require('cmd: $CMD' in terminal, "native terminal excerpt changed")
    snap_line = next(line for line in native.splitlines() if "printf 'tree=%s" in line)
    snap = "printf 'tree=%s\\nkey=%s\\nworktree=%s\\n' $TREE $KEY $W > $D/snap\n"
    require(snap.strip() in snap_line, "native snapshot excerpt changed")
    (fixture / "terminal-excerpt.sh").write_text(snap + terminal)
    excerpts["terminal_snapshot"] = {"source_sha256": digest(ORCH / "bin/test-run"),
                                      "excerpt_sha256": digest(fixture / "terminal-excerpt.sh")}
    # Existing lifecycle outputs are our own tiny fixtures, never shared benches.
    roots = {"cut": scratch / "cut-measurement-fail/run", "pristine": scratch / "pristine-success/run"}
    daemon = fixture / "queue-actor.py"
    daemon.write_text('''import os, pathlib, subprocess, sys, time
root, packet, cut, pristine, tree, worktree = sys.argv[1:]
root, packet = pathlib.Path(root), pathlib.Path(packet)
bad_row = os.environ.get('FIXTURE_BAD_ROW') == '1'
seen = {p.name for p in (root / 'queue/pending').glob('test-*')} if bad_row else set()
(root / ('actor-ready-bad' if bad_row else 'actor-ready')).write_text('ready')
for count in range(1 if bad_row else 2):
    deadline = time.monotonic() + 30
    while True:
        pending = [p for p in (root / 'queue/pending').glob('test-*') if p.name not in seen]
        if pending: break
        if time.monotonic() > deadline: raise SystemExit('fixture queue timed out')
        time.sleep(.01)
    marker = pending[0]
    seen.add(marker.name)
    kind, service = marker.read_text().split()
    assert kind == 'TEST' and service == marker.name.removeprefix('test-')
    result = root / 'tests' / service
    row = [r for r in (root / 'tests/suites.conf').read_text().splitlines() if r.split()[:2] == ['agent', 'agent-core-full']]
    assert len(row) == 1
    command = ' '.join(row[0].split()[2:])
    mode = 'cut' if count == 0 else 'pristine'
    assert command == '/bin/bash ' + str(packet / ('command-' + mode + '.sh'))
    if bad_row:
        command = '/bin/bash /bin/stale'
        registry = root / 'tests/suites.conf'
        registry.write_text(registry.read_text().replace(row[0], 'agent agent-core-full ' + command))
    run = pathlib.Path(cut if mode == 'cut' else pristine)
    rc = int(dict(line.split('=', 1) for line in (run / 'status.txt').read_text().splitlines())['runner_exit'])
    (result / 'log.txt').write_bytes((run / 'runner.log').read_bytes())
    env = dict(os.environ, D=str(result), TREE=tree, KEY='a'*32, W=worktree,
               RC=str(rc), T0=str(int(time.time())), CMD=command, ID=service,
               suite='agent-core-full', target='integration:agent', repo='agent', tree=tree)
    subprocess.run(['/bin/bash', str(root / 'terminal-excerpt.sh')], env=env, check=True)

    if mode == 'cut' and not bad_row:
        import importlib.util, json
        spec = importlib.util.spec_from_file_location('checker', packet / 'check-source.py')
        checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
        checker.verify_seal(run)
        launch = run / 'launcher-evidence'; launch.mkdir(mode=0o700)
        assertion = root / 'assertion.py'; assertion.write_text('assert 1 == 2, "isolated failed measurement"\\n')
        launch_env = dict(os.environ, P4_D73_EVIDENCE=str(launch), P4_D73_REQUEST_ID=service,
                          PYTHONDONTWRITEBYTECODE='1', HOME='/root', LANG='C.UTF-8', LC_ALL='C.UTF-8')
        launch_proc = subprocess.run(['/home/user/work/agent/tools/p4-d73-pinned-launch.sh',
            str(packet / 'positive.manifest'), 'dry', '--', '/home/user/work/venv-agent/bin/python', str(assertion)],
            env=launch_env, capture_output=True)
        (root / 'launcher.stdout').write_bytes(launch_proc.stdout)
        (root / 'launcher.stderr').write_bytes(launch_proc.stderr)
        assert launch_proc.returncode == 1
        seal = run / 'custody-after.json'; records = json.loads(seal.read_text())
        for path in sorted(launch.rglob('*')):
            if path.is_file(): path.chmod(0o400)
        for path in [launch, *sorted(launch.rglob('*'))]: records.append(checker.item(path))
        seal.chmod(0o600); seal.write_text(json.dumps(records) + '\\n'); seal.chmod(0o400)
        checker.verify_seal(run)
    (result / 'exit').write_text(str(rc) + '\\n')
    (result / 'status').write_text(('pass' if rc == 0 else 'fail') + '\\n')
''')
    output = fixture / "output"
    driver = fixture / "driver.sh"
    driver.write_text('''source "$1"
ORCH=$2; BIN=$2/bin; SUITES=$2/tests/suites.conf
CUT_RUN_ROOT=$4; PRISTINE_RUN_ROOT=$5
available() { printf 4714564096; }
if dispatch "$3"; then rc=0; else rc=$?; fi
printf "%s\\n" "$rc" > "$3/controller.exit"
exit "$rc"
''')
    env = dict(os.environ, PATH=str(fixture / "bin") + ":" + os.environ["PATH"])
    actor = subprocess.Popen([sys.executable, "-P", str(daemon), str(fixture), str(ROOT),
                              str(roots["cut"]), str(roots["pristine"]),
                              manifest()["integrated"]["agent"]["tree"], manifest()["integrated"]["agent"]["path"]],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    try:
        proc = subprocess.run(["/bin/bash", str(driver), str(ROOT / "controller-continuation.sh"),
                               str(fixture), str(output), str(roots["cut"]), str(roots["pristine"])], capture_output=True, text=True, env=env, timeout=45)
        (fixture / "controller.stdout").write_text(proc.stdout)
        (fixture / "controller.stderr").write_text(proc.stderr)
        if proc.returncode != 1:
            actor.terminate()
        stdout, stderr = actor.communicate(timeout=5)
    finally:
        if actor.poll() is None:
            actor.terminate()
            actor.wait(timeout=5)
    (fixture / "controller.stdout").write_text(proc.stdout)
    (fixture / "controller.stderr").write_text(proc.stderr)
    require(proc.returncode == 1, "failed cut did not retain its exit: " + proc.stderr)
    require(actor.returncode == 0, "queue dependency failed: " + stderr.decode())
    outcomes = (output / "pair-outcomes.txt").read_text()
    require("cut_test_exit=1\npristine_test_exit=0\n" in outcomes, "failed cut did not run pristine")
    require(suite.read_text() == original, "serial controller failed to restore row")
    ids = [(output / mode / "returned-result-dir.txt").read_text().strip() for mode in ("cut", "pristine")]
    require(len(set(ids)) == 2, "native queue reused a service ID")
    require(not (fixture / "bin/test-run").exists(), "fixture unexpectedly supplies a second launch owner")
    # All ten original association dimensions remain checked, now against native
    # fields and terminal artifacts. Positive is readback only, never admission.
    args = [ids[1], "pristine", str(ROOT / "command-pristine.sh"),
            str(ROOT / "positive.manifest"), str(ROOT / "source-manifest.json"), str(roots["pristine"]), str(output / "pristine")]
    observed = binding.inspect_result(*args)
    require(observed["test_status"] == "pass" and observed["admitted"] is False, "observation granted admission")
    cases = [{"case": "positive", "scope": "isolated native artifact readback; admitted=false"}]
    result = Path(ids[1])
    for name, path, changed in [
        ("missing-binding", result / "summary", b""),
        ("request-target", result / "request", (result / "request").read_bytes().replace(b'integration:agent', b'integration:runtime')),
        ("request-suite", result / "request", (result / "request").read_bytes().replace(b'agent-core-full', b'full')),
        ("request-duplicate", result / "request", (result / "request").read_bytes() + b'repo=agent\n'),
        ("snapshot-tree", result / "snap", (result / "snap").read_bytes().replace(manifest()["integrated"]["agent"]["tree"].encode(), b'0'*40)),
        ("snapshot-source", result / "snap", (result / "snap").read_bytes().replace(b'/home/user/work/agent', b'/wrong/source')),
        ("resolved-row", result / "summary", (result / "summary").read_bytes().replace(b'command-pristine.sh', b'command-cut.sh')),
        ("terminal-exit", result / "exit", b'1\n'),
        ("custody", roots["pristine"] / "raw-stdout.log", b'changed'),
    ]:
        before, mode = path.read_bytes(), path.stat().st_mode & 0o777
        path.chmod(0o600)
        path.write_bytes(changed)
        path.chmod(mode)
        try:
            binding.inspect_result(*args)
        except (ValueError, KeyError, OSError, IndexError):
            cases.append({"case": name, "refused": True})
        else:
            raise ValueError("negative native association passed: " + name)
        finally:
            path.chmod(0o600)
            path.write_bytes(before)
            path.chmod(mode)
    # Additional binding dimensions do not replace the ten retained controls.
    extra_cases = []
    for name, path, changed in [
        ("dispatch-brief", output / "dispatch-witness.txt", (output / "dispatch-witness.txt").read_bytes().replace(manifest()["owner_brief"]["sha256"].encode(), b'0'*64)),
        ("row-hash", output / "pristine/row-before-request.json", (output / "pristine/row-before-request.json").read_bytes().replace(b'agent-core-full', b'wrong-row')),
        ("pre-body-context", roots["pristine"] / "service.txt", b'{}'),
    ]:
        before, bits = path.read_bytes(), path.stat().st_mode & 0o777
        path.chmod(0o600); path.write_bytes(changed); path.chmod(bits)
        try:
            binding.inspect_result(*args)
        except (ValueError, KeyError, OSError):
            extra_cases.append({"case": name, "refused": True})
        else:
            raise ValueError("additional binding mutation accepted: " + name)
        finally:
            path.chmod(0o600); path.write_bytes(before); path.chmod(bits)
    # Run the same full future dispatch path again. The private actor changes
    # the row only after request-test queued it: retrospective mismatch MUST
    # withdraw that returned ID and must not start pristine or overwrite the edit.
    bad_output = fixture / "stale-output"
    bad_env = dict(env, FIXTURE_BAD_ROW="1")
    bad_actor = subprocess.Popen([sys.executable, "-P", str(daemon), str(fixture), str(ROOT),
                                  str(roots["cut"]), str(roots["pristine"]),
                                  manifest()["integrated"]["agent"]["tree"], manifest()["integrated"]["agent"]["path"]],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=bad_env)
    try:
        deadline = time.monotonic() + 5
        while not (fixture / "actor-ready-bad").exists():
            require(time.monotonic() < deadline, "private stale actor did not become ready")
            time.sleep(.01)
        bad = subprocess.run(["/bin/bash", str(driver), str(ROOT / "controller-continuation.sh"),
                              str(fixture), str(bad_output), str(roots["cut"]), str(roots["pristine"])],
                             capture_output=True, text=True, env=bad_env, timeout=45)
        bad_stdout, bad_stderr = bad_actor.communicate(timeout=5)
    finally:
        if bad_actor.poll() is None:
            bad_actor.terminate(); bad_actor.wait(timeout=5)
    (fixture / "stale.stdout").write_text(bad.stdout)
    (fixture / "stale.stderr").write_text(bad.stderr + bad_stderr.decode())
    require(bad.returncode == 78 and bad_actor.returncode == 0, "stale result did not refuse: " + bad.stderr + bad_stderr.decode())
    bad_id = Path((bad_output / "cut/returned-result-dir.txt").read_text().strip()).name
    require((fixture / "queue/pending" / ("stoptest-" + bad_id)).read_text() ==
            "STOPTEST " + bad_id + " --withdraw native artifact binding mismatch\n", "stale result not withdrawn")
    require(not (bad_output / "pristine").exists() and not (bad_output / "pair-outcomes.txt").exists(), "invalid custody advanced/credited")
    require(suite.read_text() == original.replace("/bin/old", "/bin/stale"), "intervening row/outside bytes overwritten")
    # Exercise the immediate readback independently: a changed row must never
    # submit a request. Its private queue inventory must remain byte-identical.
    before_queue = {path.name: path.read_bytes() for path in (fixture / "queue/pending").iterdir()}
    pre = fixture / "pre-request-refusal"; pre.mkdir()
    pre_driver = fixture / "pre-request-refusal.sh"
    pre_driver.write_text('''source "$1"
BIN=$2/bin; SUITES=$2/tests/suites.conf
INSTALLED_ROW='agent agent-core-full /bin/bash /bin/ours'
if queue_and_wait "$3"; then exit 91; else rc=$?; fi
[ "$rc" -eq 78 ]
''')
    run(["/bin/bash", str(pre_driver), str(ROOT / "controller-continuation.sh"), str(fixture), str(pre)])
    require(before_queue == {path.name: path.read_bytes() for path in (fixture / "queue/pending").iterdir()}, "pre-request readback refusal queued a request")
    # Existing installer exercised in place on a private registry; an intervening
    # edit is retained byte for byte. No unowned production registry is changed.
    conservation = fixture / "conservation.sh"
    conservation.write_text('''source "$1"
SUITES=$2; ORIGINAL_ROW=$(read_row)
INSTALLED_ROW="agent agent-core-full /bin/bash /bin/ours"
replace_row "$ORIGINAL_ROW" "$INSTALLED_ROW" "$3/install" || exit 90
printf 'agent agent-core-full /bin/bash /bin/intervening\\n' > "$SUITES"
if restore_row "$3/restore"; then exit 91; else rc=$?; fi
[ "$rc" -eq 78 ] && [ "$(read_row)" = 'agent agent-core-full /bin/bash /bin/intervening' ]
''')
    saved = fixture / "row-conservation"
    saved.mkdir()
    run(["/bin/bash", str(conservation), str(ROOT / "controller-continuation.sh"), str(suite), str(saved)])
    # No arbitrary caller JSON supplies native admission. Future entry itself
    # was exercised above with only private registry/queue/admission dependencies.
    for action in ("admission", "consume"):
        refused = subprocess.run([sys.executable, "-P", str(ROOT / "binding-source.py"), action,
                                  str(output / "cut/observation.json")], capture_output=True, text=True)
        require(refused.returncode == 78 and "not native service admission" in refused.stderr, "caller JSON granted admission")
    # Post-body mismatch withdraws the returned native fixture ID and stops
    # before pristine. Use the exact future invalidation function + relocated
    # native withdrawal request writer, never the live service.
    invalid = fixture / "invalid-control"
    invalid.mkdir()
    withdrawal = fixture / "withdrawal.sh"
    withdrawal.write_text('''source "$1"
BIN=$2/bin; SUITES=$2/tests/suites.conf
SERVICE_DIR=$3
INSTALLED_ROW=; ORIGINAL_ROW=$(read_row)
if invalidate_result "$4" 'isolated invalid custody'; then exit 91; else rc=$?; fi
[ "$rc" -eq 78 ]
''')
    run(["/bin/bash", str(withdrawal), str(ROOT / "controller-continuation.sh"), str(fixture), ids[1], str(invalid)])
    marker = fixture / "queue/pending" / ("stoptest-" + Path(ids[1]).name)
    require(marker.read_text() == "STOPTEST " + Path(ids[1]).name + " --withdraw isolated invalid custody\n", "invalid result was not withdrawn")
    require("qualification=INVALID" in (invalid / "invalid.txt").read_text(), "invalid result credited")
    native_cases = native_admission_controls(fixture)
    return cases, {"source_excerpts": excerpts, "queue_actor": "explicit dependency double, not native custody",
                   "pair_exit": proc.returncode, "outcomes": outcomes.splitlines(),
                   "row_edit": "conserved", "production_dispatch": "real dispatch function, isolated dependencies; not live admission",
                   "admission": native_cases, "result_dirs": ids, "extra_bindings": extra_cases,
                   "stale_row": {"exit": bad.returncode, "withdrawn_fixture_id": bad_id, "pristine_started": False},
                   "pre_request_readback": "changed row refused before queue"}


def native_admission_controls(fixture):
    """Run the unchanged native classification and admission expressions."""
    native = (ORCH / "bin/test-run").read_text()
    classification = next(x for x in native.splitlines() if x.startswith("HV=light;"))
    a = native.index('  [ $HV = heavy ] && [ $(alive heavy)')
    b = native.index('  [ $HV = heavy ] && touch $D/heavy', a)
    admission = native[a:b]
    results = []
    for name, suite, free, heavy, expected in [
        ("cut-heavy-equal", "agent-core-full", 4700000000, 0, 0),
        ("pristine-heavy-equal", "agent-core-full", 4700000000, 0, 0),
        ("core-below", "agent-core-full", 4699999999, 0, 3),
        ("one-heavy", "agent-core-full", 4800000000, 1, 3),
        ("global-stop", "agent-core-full", 4500000000, 0, 3),
        ("light-below", "targeted", 4999999999, 0, 3),
        ("light-equal", "targeted", 5000000000, 0, 0),
        ("default-heavy-equal", "full", 5200000000, 0, 3),
        ("default-heavy-above", "full", 5200000001, 0, 0),
        ("disk-unreadable", "agent-core-full", "error", 0, 3),
    ]:
        output = fixture / ("admission-" + name)
        output.mkdir()
        script = output / "driver.sh"
        script.write_text('set -u\nsuite=$1; D=$2; MEASURED_FLOOR=\n'
                          'refuse() { printf "%s\\n" "$*"; exit 3; }\n'
                          'alive() { if [ "$1" = heavy ]; then printf "%s" "$FIXTURE_HEAVY"; else printf 0; fi; }\n'
                          'df() { [ "$FIXTURE_FREE" != error ] || return 1; printf "Avail\\n%s\\n" "$FIXTURE_FREE"; }\n'
                          + classification + '\n' + admission + '\nexit 0\n')
        env = dict(os.environ, FIXTURE_FREE=str(free), FIXTURE_HEAVY=str(heavy))
        proc = subprocess.run(["/bin/bash", str(script), suite, str(output)], capture_output=True, text=True, env=env)
        require(proc.returncode == expected, "native admission " + name + ": " + proc.stdout + proc.stderr)
        results.append({"case": name, "exit": proc.returncode, "expected": expected,
                        "scope": "isolated native source excerpt; no live admission"})
    return results


def lifecycle_controls(scratch):
    results = []
    for mode in ["cut", "pristine"]:
        for case, expected in [("success", 0), ("body17", 17), ("measurement-fail", 1), ("missing-junit", 98), ("bad-junit", 98), ("failed-junit-zero-exit", 98), ("empty-raw", 98),
                               ("keep-tamper", 98), ("source-tamper", 98), ("floor-below", 124),
                               ("floor-equal", 0), ("floor-above", 0), ("disk-unreadable", 97),
                               ("disk-unwritable", 98), ("monitor-stop", 124), ("monitor-read", 97), ("monitor-write", 98), ("cadence", 0), ("term", 143)]:
            work = scratch / (mode + "-" + case)
            work.mkdir(mode=0o700)
            root = work / "run"
            fake = work / "body.sh"
            fake.write_text('#!/bin/bash\nprintf "fixture stdout\\n"\nprintf "fixture stderr\\n" >&2\n'
                            + ('' if case == "missing-junit" else 'printf \'<testsuites><testsuite tests="1"><testcase name="tiny"/></testsuite></testsuites>\' > "$1"\n')
                            + ('printf broken > "$1"\n' if case == "bad-junit" else '')
                            + ("printf '%s' '<testsuite tests=\"1\" failures=\"1\"><testcase name=\"tiny\"><failure/></testcase></testsuite>' > \"$1\"\n" if case == "failed-junit-zero-exit" else '')
                            + (': > "$(dirname "$1")/raw-stdout.log"\n: > "$(dirname "$1")/raw-stderr.log"\n' if case == "empty-raw" else '')
                            + ('printf changed > "$(dirname "$1")/source-before.txt"\n' if case == "source-tamper" else '')
                            + ('chmod 600 "$(dirname "$1")/KEEP"\n' if case == "keep-tamper" else '')
                            + ('sleep 5.2\n' if case == 'cadence' else '')
                            + ('sleep 30\n' if case in ["monitor-stop", "monitor-read", "monitor-write", "term"] else '')
                            + ('''printf '%s' '<testsuite tests="1" failures="1"><testcase name="assertion"><failure/></testcase></testsuite>' > "$1"
/home/user/work/venv-agent/bin/python -c 'assert 1 == 2, "isolated measurement failure"'
exit $?
''' if case == 'measurement-fail' else 'exit 17\n' if case == 'body17' else 'exit 0\n'))
            driver = work / "driver.sh"
            driver.write_text('source "$1"\nconfigure\nRUN_ROOT="$2"\nPAIR_LOCK="$3"\nsetup_paths\n'
                              'capture_sources() { printf "isolated fixture source\\n"; }\n'
                              'interpreter() { printf "isolated fixture interpreter\\n"; }\n'
                              'admitted_dispatch() { "$PYTHON" -P "$BINDING_SOURCE" dispatch-readiness "$SOURCE_MANIFEST" "$COMMAND_PATH" "$MANIFEST"; }\n'
                              'native_service_identity() { printf "isolated-lifecycle-control\\n"; }\n'
                              'FIXTURE_BODY=$4\nbuild_argv() { BODY_ARGV=(/bin/bash "$FIXTURE_BODY" "$JUNIT_XML"); }\n'
                              'AGENT_CHECKOUT="$5"\n'
                              + ('sleep() { command sleep 0.03; }\n' if case != 'cadence' else '')
                              + ('available_bytes() { printf 3999999999; }\n' if case == "floor-below" else
                                 'available_bytes() { return 97; }\n' if case == "disk-unreadable" else
                                 'available_bytes() { printf 4000000001; }\n' if case == "floor-above" else
                                 'available_bytes() { printf 4000000000; }\n')
                              + ('record_disk() { return 98; }\n' if case == "disk-unwritable" else '')
                              + ('available_bytes() { if [[ ${FUNCNAME[*]} == *monitor_disk* ]]; then for ((i=0;i<100;i++)); do [ -s "$JUNIT_XML" ] && break; command sleep .01; done; printf 3999999999; else printf 4000000000; fi; }\n' if case == "monitor-stop" else '')
                              + ('available_bytes() { if [[ ${FUNCNAME[*]} == *monitor_disk* ]]; then for ((i=0;i<100;i++)); do [ -s "$JUNIT_XML" ] && break; command sleep .01; done; return 97; else printf 4000000000; fi; }\n' if case == "monitor-read" else '')
                              + ('available_bytes() { if [[ ${FUNCNAME[*]} == *monitor_disk* ]]; then for ((i=0;i<100;i++)); do [ -s "$JUNIT_XML" ] && break; command sleep .01; done; fi; printf 4000000000; }\nrecord_disk_original=$(declare -f record_disk)\neval "${record_disk_original/record_disk/record_disk_original}"\nrecord_disk() { if [ "$1" = monitor ]; then DISK_TRACE_FILE=/dev/full record_disk_original "$@"; else record_disk_original "$@"; fi; }\n' if case == "monitor-write" else '')
                              + ('( command sleep .15; kill -TERM "$BASHPID_PARENT" ) &\n' if case == "term" else '')
                              + 'run\n')
            # A shell driver overrides only fixture dependencies. All run/finish,
            # custody, argv execution, waits and signal handlers are actual source.
            argv = ["/bin/bash", str(driver), str(ROOT / f"command-{mode}.sh"), str(root), str(work / "lock"), str(fake), str(work)]
            env = dict(os.environ)
            if case == "term":
                text = driver.read_text().replace('( command sleep .15; kill -TERM "$BASHPID_PARENT" ) &',
                                                  'BASHPID_PARENT=$BASHPID\n( for ((i=0;i<500;i++)); do [ ! -s "$JUNIT_XML" ] || break; command sleep .01; done; kill -TERM "$BASHPID_PARENT" ) &')
                driver.write_text(text)
            proc = subprocess.run(argv, capture_output=True, env=env, timeout=15)
            (work / "stdout").write_bytes(proc.stdout)
            (work / "stderr").write_bytes(proc.stderr)
            status = dict(line.split("=", 1) for line in (root / "status.txt").read_text().splitlines())
            require(proc.returncode == expected, f"lifecycle {mode}/{case}: {proc.returncode} != {expected}: {proc.stderr.decode()}")
            require(int(status["exit"]) == proc.returncode, "terminal status/process exit mismatch")
            require((status["state"] == "PASS") == (expected == 0), "terminal state mismatch")
            if expected == 98:
                require(status["evidence_exit"] == "98", "evidence failure missing from status: " + mode + "/" + case)
            if case == "body17":
                require(status["runner_exit"] == "17" and status["monitor_exit"] == "0", "body exit lost")
            if case == "success":
                verify_seal(root)
                for name in ["raw-stdout.log", "raw-stderr.log", "agent-core-full.xml", "disk-trace.txt", "KEEP", "source-before.txt", "source-after.txt", "interpreter.txt", "callerargv.txt", "service.txt"]:
                    target = root / name
                    previous, mode_bits = target.read_bytes(), target.stat().st_mode & 0o777
                    target.chmod(0o600)
                    target.write_bytes(previous + b"post-seal mutation")
                    target.chmod(mode_bits)
                    try:
                        verify_seal(root)
                    except ValueError:
                        pass
                    else:
                        raise ValueError("sealed hash mutation undetected: " + name)
                    target.chmod(0o600)
                    target.write_bytes(previous)
                    target.chmod(mode_bits)
                verify_seal(root)
            results.append({"mode": mode, "case": case, "exit": proc.returncode, "status": status,
                            "driver": str(driver), "driver_sha256": digest(driver)})
    return results


def check():
    artifacts()
    arithmetic = load(ROOT / "admission-derivation.json")
    inputs = arithmetic["inputs"]
    growth = max(inputs["actual_26496_dispatch_bytes"] - inputs["actual_26496_min_trace_bytes"],
                 inputs["actual_26496_source_admission_bytes"] - inputs["actual_26496_min_trace_bytes"])
    floor = max(inputs["dispatch_floor_base_bytes"], inputs["continuous_stop_bytes"] + growth + inputs["safety_margin_bytes"])
    require(growth == arithmetic["derivation"]["x_bytes"] == 514564096
            and floor == arithmetic["derivation"]["floor_bytes"] == 4714564096,
            "D89d floor arithmetic differs")
    for mode in ["cut", "pristine"]:
        run(["bash", "-n", str(ROOT / f"command-{mode}.sh")])
        sources(mode)
    run(["bash", "-n", str(ROOT / "positive-stub.sh")])
    run(["bash", "-n", str(ROOT / "tiny-controls.sh")])
    run(["bash", "-n", str(ROOT / "controller-continuation.sh")])
    run([sys.executable, "-P", "-c", "import ast, pathlib, sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())", str(ROOT / "binding-source.py")])
    verify_argv()
    require(digest(ROOT / "positive-stub.sh") == "38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0", "original stub hash differs")
    positive = (ROOT / "positive.manifest").read_text().splitlines()
    poison = (ROOT / "poison.manifest").read_text().splitlines()
    require(len(positive) == len(poison) and [a.split("=", 1)[0] for a, b in zip(positive, poison) if a != b] == ["agent_sha"], "poison delta differs")
    (ROOT / "private-control-logs").mkdir(mode=0o700, exist_ok=True)
    tiny_output = run(["bash", str(ROOT / "tiny-controls.sh")], text=True)
    # All fixtures are private, small, and explicitly incapable of admission.
    scratch = Path(tempfile.mkdtemp(prefix="d141l-controls-", dir=ROOT / "private-control-logs"))
    lifecycle = lifecycle_controls(scratch)
    admissions, native = admission_controls(scratch)
    result = {"control_status": "PASS", "pair_status": "READY_SOURCE_D141aa_NOT_RUN_LIVE",
              "real_pair_started": False, "tiny": tiny_output.splitlines(),
              "admission_controls": admissions, "lifecycle_controls": lifecycle,
              "controller_route": "isolated request-test -> queue actor -> wait-test; no live request",
              "native_controls": native,
              "source_manifest_sha256": digest(ROOT / "source-manifest.json"),
              "fixture_root": str(scratch), "command": shlex.join([sys.executable, "-P", str(ROOT / "check-source.py"), "check"])}
    logs = ROOT / "private-control-logs"
    logs.mkdir(mode=0o700, exist_ok=True)
    out = logs / ("check-" + str(time.time_ns()) + ".json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"control_status": result["control_status"], "pair_status": result["pair_status"],
                      "admission_cases": len(admissions), "lifecycle_cases": len(lifecycle),
                      "controller_route": "isolated request-test -> queue actor -> wait-test",
                      "log": str(out)}))


def main():
    action, *args = sys.argv[1:]
    if action == "check":
        check()
    elif action == "sources":
        print(sources(*args))
    elif action == "admission":
        admitted_dispatch(*args)
    elif action == "custody-before":
        custody_before(args[0], args[1:])
    elif action == "custody-after":
        custody_after(*args)
    else:
        raise ValueError("unknown checker action")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, TypeError, ET.ParseError, subprocess.SubprocessError) as exc:
        print("REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(78)

