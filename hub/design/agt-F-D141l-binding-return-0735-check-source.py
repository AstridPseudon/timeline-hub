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

ROOT = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-return-0735/evidence")
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
    "admission-derivation.json",
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
    for expected in load(Path(root) / "custody-after.json"):
        require(item(expected["path"]) == expected, "sealed custody mismatch: " + expected["path"])


def shell_argv(mode):
    command = ROOT / f"command-{mode}.sh"
    script = 'source "$1"; configure; build_argv; printf "%s\\0" "${BODY_ARGV[@]}"'
    return run(["/bin/bash", "--noprofile", "--norc", "-c", script, "_", str(command)]).decode().split("\0")[:-1]


def verify_argv():
    data = manifest()
    common = None
    for mode in ["cut", "pristine"]:
        argv = shell_argv(mode)
        group = "integrated" if mode == "cut" else "pristine"
        agent, runtime = [data[group][r]["path"] for r in ["agent", "runtime"]]
        xml = str(ROOT / f"privatecontrol-logs/run-{mode}/agent-core-full.xml")
        pytest = ["-m", "pytest", "-q", "-n3", "-o", "addopts=", "-p", "no:cacheprovider", "--timeout=45", f"--junitxml={xml}"] + data["roots"][mode]
        prefix = ["env", "-i", "HOME=/root", "LANG=C.UTF-8", "LC_ALL=C.UTF-8", "PYTHONDONTWRITEBYTECODE=1", "PYTHONNOUSERSITE=1",
                  f"PYTHONPATH={agent}:{runtime}", "PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin",
                  "VIRTUAL_ENV=/home/user/work/venv-agent", f"ASTRID_RUNTIME_CHECKOUT={runtime}", f"ASTRID_RUNTIME_SOURCE_ROOT={runtime}",
                  "ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110",
                  "ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node",
                  "ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules"]
        if mode == "cut":
            expected = prefix + [f"P4_D73_MANIFEST={ROOT}/positive.manifest", f"P4_D73_EVIDENCE={ROOT}/privatecontrol-logs/run-cut/launcher-evidence", "P4_D73_REQUEST_ID=agent-core-full",
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

def controller_controls(scratch):
    """Run the exact future controller against tiny command doubles."""
    fixture = scratch / "controller-route"
    (fixture / "bin").mkdir(parents=True)
    (fixture / "tests").mkdir()
    suite = fixture / "tests" / "suites.conf"
    suite.write_text("agent agent-core-full /bin/bash /bin/old /tmp/old-receipt /tmp/old-brief\n")
    counter = fixture / "counter"
    counter.write_text("0")
    request_test = fixture / "bin" / "request-test"
    request_test.write_text("""#!/bin/sh
set -eu
n=$(cat "$FIXTURE_COUNTER")
n=$((n + 1))
printf '%s' "$n" > "$FIXTURE_COUNTER"
id="agent-agent-core-full-20990101000000-$n"
d="$FIXTURE_ORCH/tests/$id"
mkdir -m 700 "$d"
printf '%s\n' "target=integration:agent" "repo=agent" "suite=agent-core-full" "files=''" "nocache=1" "requested=2099-01-01T00:00:00Z" > "$d/request"
printf 'queued\n' > "$d/status"
printf '%s/\n' "$d"
""")
    test_run = fixture / "bin" / "test-run"
    test_run.write_text("""#!/bin/sh
set -eu
d="$FIXTURE_ORCH/tests/$1"
printf 'pass\n' > "$d/status"
printf '0\n' > "$d/exit"
printf 'fixture pass\n' > "$d/summary"
printf 'fixture log\n' > "$d/log.txt"
exit 0
""")
    wait_test = fixture / "bin" / "wait-test"
    wait_test.write_text("""#!/bin/sh
set -eu
d="$FIXTURE_ORCH/tests/$1"
cat "$d/summary"
exit "$(cat "$d/exit")"
""")
    fake_df = fixture / "bin" / "df"
    fake_df.write_text("#!/bin/sh\nprintf 'Avail\\n4800000000\\n'\n")
    for path in [request_test, test_run, wait_test, fake_df]:
        path.chmod(0o700)
    output = fixture / "output"
    env = dict(os.environ)
    env.update({
        "D141L_ORCH": str(fixture),
        "D141L_BIN": str(fixture / "bin"),
        "D141L_SUITES_CONF": str(suite),
        "FIXTURE_ORCH": str(fixture),
        "FIXTURE_COUNTER": str(counter),
        "PATH": f"{fixture / 'bin'}:" + env["PATH"],
    })
    result = subprocess.run(["/bin/bash", str(ROOT / "controller-continuation.sh"), "dispatch", str(output)],
                            capture_output=True, text=True, env=env, timeout=20)
    require(result.returncode == 0, "isolated real controller route failed: " + result.stderr)
    readiness = load(output / "readiness.json")
    require(readiness["status"] == "QUALIFIED" and len(readiness["service_ids"]) == 2,
            "isolated controller did not produce two terminal bindings")
    require(readiness["service_ids"][0] != readiness["service_ids"][1],
            "isolated controller reused a placeholder service ID")
    require(suite.read_text() == "agent agent-core-full /bin/bash /bin/old /tmp/old-receipt /tmp/old-brief\n",
            "isolated controller did not restore the original row")
    require(counter.read_text() == "2", "isolated controller did not use both request-test calls")
    return output


def admission_controls(scratch):
    """Exercise the same consumer on the isolated controller's real artifacts."""
    output = controller_controls(scratch)
    command = [sys.executable, "-P", str(ROOT / "binding-source.py")]
    positive_binding = output / "cut" / "binding.json"
    positive = subprocess.run(command + ["consume", str(positive_binding), "cut",
                                         str(ROOT / "command-cut.sh"), str(ROOT / "positive.manifest"),
                                         str(ROOT / "source-manifest.json")], capture_output=True, text=True)
    require(positive.returncode == 0, "isolated controller binding was refused")
    base = json.loads(positive_binding.read_text())
    cases = []
    for name, change in [
        ("missing-binding", lambda data: None),
        ("receipt-path", lambda data: data["receipt"].update(path=str(scratch / "missing-receipt"))),
        ("receipt-hash", lambda data: data["receipt"].update(sha256="0" * 64)),
        ("brief-hash", lambda data: data["brief"].update(sha256="0" * 64)),
        ("terminal-path", lambda data: data["terminal"].update(path=str(scratch / "missing-terminal"))),
        ("service-id", lambda data: data.update(service_id="agent-agent-core-full-20990101000000-99",
                                                request_id="agent-agent-core-full-20990101000000-99")),
        ("mode", lambda data: data.update(mode="pristine")),
        ("wrong-request-id", lambda data: data.update(request_id="not-a-placeholder")),
        ("receipt-retarget", lambda data: data["receipt"].update(path=str(output / "cut" / "terminal.json"))),
    ]:
        candidate = scratch / (name + ".json")
        if name != "missing-binding":
            changed = json.loads(json.dumps(base))
            change(changed)
            candidate.write_text(json.dumps(changed) + "\n")
            path = candidate
        else:
            path = scratch / "does-not-exist.json"
        result = subprocess.run(command + ["consume", str(path), "cut",
                                            str(ROOT / "command-cut.sh"), str(ROOT / "positive.manifest"),
                                            str(ROOT / "source-manifest.json")],
                                capture_output=True, text=True)
        require(result.returncode != 0, "negative binding case passed: " + name)
        cases.append({"case": name, "refused": result.stderr.strip()})
    return [{"case": "positive", "status": "accepted_only_as_isolated_controller"}] + cases


def lifecycle_controls(scratch):
    results = []
    for mode in ["cut", "pristine"]:
        for case, expected in [("success", 0), ("body17", 17), ("missing-junit", 98), ("bad-junit", 98), ("failed-junit-zero-exit", 98), ("empty-raw", 98),
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
                            + ('exit 17\n' if case == "body17" else 'exit 0\n'))
            driver = work / "driver.sh"
            driver.write_text('source "$1"\nconfigure\nRUN_ROOT="$2"\nPAIR_LOCK="$3"\nsetup_paths\n'
                              'capture_sources() { printf "isolated fixture source\\n"; }\n'
                              'interpreter() { printf "isolated fixture interpreter\\n"; }\n'
                              'admitted_dispatch() { printf "ISOLATED FIXTURE, NO ADMISSION\\n"; }\n'
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
                                                  'BASHPID_PARENT=$BASHPID\n( command sleep .15; kill -TERM "$BASHPID_PARENT" ) &')
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
    registered = (ORCH / "tests/suites.conf").read_text().splitlines()
    require(any(row.split()[:2] == ["agent", "agent-core-full"] for row in registered),
            "existing agent-core-full registration disappeared")
    require(any("agt-F-D141i-terminal-floor-return-sol-0309" in row
                for row in registered if row.split()[:2] == ["agent", "agent-core-full"]),
            "historical live row changed before the future controller dispatch")
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
    (ROOT / "privatecontrol-logs").mkdir(mode=0o700, exist_ok=True)
    tiny_output = run(["bash", str(ROOT / "tiny-controls.sh")], text=True)
    # All fixtures are private, small, and explicitly incapable of admission.
    scratch = Path(tempfile.mkdtemp(prefix="d141l-controls-", dir=os.environ["TMPDIR"]))
    admissions = admission_controls(scratch)
    lifecycle = lifecycle_controls(scratch)
    result = {"control_status": "PASS", "pair_status": "SOURCE_READY_NO_LIVE_REGISTRATION",
              "real_pair_started": False, "tiny": tiny_output.splitlines(),
              "admission_controls": admissions, "lifecycle_controls": lifecycle,
              "controller_route": "isolated request-test -> test-run -> wait-test only; no live request",
              "source_manifest_sha256": digest(ROOT / "source-manifest.json"),
              "fixture_root": str(scratch), "command": shlex.join([sys.executable, "-P", str(ROOT / "check-source.py"), "check"])}
    logs = ROOT / "privatecontrol-logs"
    logs.mkdir(mode=0o700, exist_ok=True)
    out = logs / ("check-" + str(time.time_ns()) + ".json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"control_status": result["control_status"], "pair_status": result["pair_status"],
                      "admission_cases": len(admissions), "lifecycle_cases": len(lifecycle),
                      "controller_route": "isolated request-test -> test-run -> wait-test",
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

