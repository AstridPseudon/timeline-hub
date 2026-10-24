# Farm Codex handoff: OPS-farm-agent-full-v3

Source review only.  This packet authorizes no live operation.  Do not invoke
the installer, `test-run`, or a checkpoint without the exact normal
D21b child receipt. The child request precedes its resulting receipt: checkout
receipts → managed Remotion preflight → child request → normal receipt validation
→ guarded installation → parent/isolated-child preflight → checkpoint.

The supported child request is in `README.md`.  Its `agent-remotion-farm-v2-9cd`
argument is the existing approved Remotion registration; `remotion-env-nodes`
is the existing base selector.  The child must be built by the normal maker.
There is no manual pip install, shared-venv `.pth`, source overlay, invented
child path, or isolation bypass.

The current Farm inputs must include the current Store owner/index, the current
registry bytes, one unchanged `agent full` row, one existing `agent full-farm`
row, the managed Remotion entry and its Node20 graph, clean exact source
receipts, and the successful D21b child receipt.  A missing child receipt is an
installation refusal, not an invitation to substitute a path.

## Guarded installer

The two angle-bracket path arguments must be literal paths copied from the
normal receipts: the child root and managed Remotion profile.  Runtime is the
clean checkout receipt, not an ambient integration worktree.  The baseline is
a fresh private copy of the current registry after the normal maker; backups
are under private `$TMPDIR`.

```bash
python3 -B -I - "$ORCH" /home/user/work/bench-store \
  "$PWD/ops-handoff/farm-agent-full-v3" \
  '<receipt-child-root>' '<receipt-managed-profile>' \
  '<authenticated-Runtime-checkout>' '<authenticated-Agent-checkout>' \
  "$TMPDIR/pre-full-farm.suites.conf" "$TMPDIR" <<'PY'
from datetime import datetime, timezone
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys

orch, store_root, packet, child, profile, runtime, agent, baseline_file, backups = map(Path, sys.argv[1:])
selection = __import__("json").loads((packet / "runtime-source-selection.json").read_text())
source = orch / "bin/bench_store.py"
assert hashlib.sha256(source.read_bytes()).hexdigest() == selection["bench_store_sha256"], "Store source drift"
spec = importlib.util.spec_from_file_location("bench_store", source)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
tests = orch / "tests"
store = api.Store(store_root, tests)
child_name = selection["child_name"]
remotion_name = selection["remotion_registration"]
agent_sha = selection["agent_commit_tested_by_checkpoint"]
runtime_sha = selection["required_runtime_source_commit"]
client = "\n".join("packages/python/" + name + "=" + digest for name, digest in sorted(selection["canonical_client_sha256"].items()))
identity = {"agent_sha": agent_sha, "backend_sha": runtime_sha,
            "client_tuple": dict(line.split("=", 1) for line in client.splitlines())}
with store.acquire([child_name, remotion_name]):
    assert store.registered(child_name), "D21b child receipt/registration missing"
    child_entries = store.registration_entries(child_name)
    children = [e for e in child_entries if e["component"] == "child"]
    assert len(children) == 1, "child receipt is not singular managed custody"
    entry = children[0]
    assert entry["identity"] == identity and entry["key"] == api.key_for("child", identity), "child registered identity/key mismatch"
    assert entry["owner"] == store.owner["id"], "child owner mismatch"
    assert Path(entry["path"]) == child and child == child.resolve() and child.is_dir() and not child.is_symlink(), "child path differs from receipt"
    assert store.registered(remotion_name), "managed Remotion registration missing"
    remotion_entries = store.registration_entries(remotion_name)
    assert len(remotion_entries) == 1 and remotion_entries[0]["component"] == "runtime" and Path(remotion_entries[0]["path"]) == profile, "Remotion profile differs from receipt"
    assert remotion_entries[0]["identity"] == {"remotion_tree": selection["remotion_tree"]}, "Remotion registered identity mismatch"
    assert hashlib.sha256((profile / "package-lock.json").read_bytes()).hexdigest() == selection["remotion_lock_sha256"], "Remotion lock drift"
    assert remotion_entries[0] in child_entries and len(child_entries) == 2, "child Remotion dependency mismatch"
    for checkout, commit, tree in ((agent, agent_sha, selection["agent_tree_tested_by_checkpoint"]), (runtime, runtime_sha, selection["required_runtime_tree"])):
        assert re.fullmatch(r"/[A-Za-z0-9_./-]+", str(checkout)) and checkout == checkout.resolve() and checkout.is_dir(), "physical source path required"
        assert subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip() == commit, "source receipt SHA mismatch"
        assert subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD^{tree}"], text=True).strip() == tree, "source receipt tree mismatch"
        assert not subprocess.check_output(["git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=all"], text=True), "source checkout dirty"
    assert hashlib.sha256((runtime / selection["required_runtime_module"]).read_bytes()).hexdigest() == selection["required_runtime_module_sha256"], "Runtime D40 source mismatch"
    assert hashlib.sha256((agent / "requirements/proof.lock").read_bytes()).hexdigest() == selection["proof_lock_sha256"], "proof lock drift"
    assert re.fullmatch(r"/[A-Za-z0-9_./-]+", str(profile)) and profile == profile.resolve() and profile.is_dir(), "physical profile path required"
    assert (child / "bin/python").is_file() and (child / "bin/python").resolve().is_relative_to(child), "child interpreter is not retained"
    assert (child / ".astrid-source-commit").read_text() == agent_sha + "\n", "Agent marker mismatch"
    assert (child / ".astrid-runtime-source-commit").read_text() == runtime_sha + "\n", "Runtime marker mismatch"
    assert (child / ".astrid-runtime-client-identity").read_text().rstrip("\n") == client, "client tuple mismatch"
    # Reuse the normal maker's read-only validation, never its build/ensure path.
    maker = orch / "bin/make-child-venv"
    assert hashlib.sha256(maker.read_bytes()).hexdigest() == selection["maker_sha256"], "maker source drift"
    maker_source = maker.read_text()
    verifier = maker_source.split("# STORE_VERIFY_BEGIN\n", 1)[1].split("# STORE_VERIFY_END", 1)[0]
    subprocess.run(["python3", "-B", "-I", "-", str(child), client, str(agent), agent_sha,
                    str(runtime), runtime_sha, str(store_root.parent), selection["maker_python"]], input=verifier, text=True, check=True, timeout=120)
    # report_bytes enforces exact status=passed, source tuple and proof-lock identity.
    # Extract only the maker's report checker; no provisioning statements execute.
    import ast
    maker_api = ast.parse(maker_source.split("<<'STORE_PY'\n", 1)[1].split("\nSTORE_PY", 1)[0])
    report_def = next(n for n in maker_api.body if isinstance(n, ast.FunctionDef) and n.name == "report_bytes")
    namespace = {"pathlib": __import__("pathlib"), "hashlib": hashlib, "agent": agent_sha,
                 "backend": runtime_sha, "client": client, "requirements": "requirements/proof.lock", "lock": selection["proof_lock_sha256"]}
    exec(compile(ast.Module(body=[report_def], type_ignores=[]), str(maker), "exec"), namespace)
    report = namespace["report_bytes"](child)
    with store.mutex():
        index = store._load()
        store._verify_projection(index)
        registration = index["registrations"][child_name]
        assert registration.get("report") == report.decode() and registration.get("report_sha256") == hashlib.sha256(report).hexdigest(), "child report registration mismatch"
        assert (tests / "provision" / (child_name + ".txt")).read_bytes() == report, "child report projection mismatch"
    snapshots = list(child.glob(".child-venv-source-*"))
    assert len(snapshots) == 1, "ambiguous retained child source snapshots"
    identity_script = maker_source.split("\nIDENTITY_SCRIPT=" + "'", 1)[1].split("'\nrun_stage", 1)[0]
    subprocess.run([str(child / "bin/python"), "-B", "-I", "-c", identity_script,
                    str(child / ".provision-report"), str(child), str(snapshots[0] / "agent"),
                    str(snapshots[0] / "runtime"), agent_sha, runtime_sha], check=True, timeout=120)
    baseline = baseline_file.read_bytes()
    row = (packet / "registration-row.txt").read_text()
    assert row.endswith("\n") and row.count("\n") == 1 and " " + "PYTHONPATH=" not in row
    row = row.replace("@REPORT_SHA256@", hashlib.sha256(report).hexdigest()).replace("@CHILD_ROOT@", str(child)).replace("@CHILD_INTERPRETER@", str(child / "bin/python")).replace("@MANAGED_PROFILE@", str(profile)).replace("@RUNTIME_CHECKOUT@", str(runtime))
    assert not re.search(r"@[A-Z_]+@", row)
    candidate = row.encode()
    full = b"agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3\n"
    rows = baseline.splitlines(keepends=True)
    assert rows.count(full) == 1, "original agent full changed"
    old = [r for r in rows if r.split(None, 2)[:2] == [b"agent", b"full-farm"]]
    assert len(old) == 1 and old[0].endswith(b"\n"), "exactly one existing full-farm row required"
    position = rows.index(old[0])
    post = b"".join(rows[:position]) + candidate + b"".join(rows[position + 1:])
    assert baseline == b"".join(rows)
    backup = backups / ("suites-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + ".conf")
    with store.mutex():
        assert (orch / "tests/suites.conf").read_bytes() == baseline, "registry drift"
        with backup.open("xb") as stream:
            stream.write(baseline)
            stream.flush()
            os.fsync(stream.fileno())
        api.sync_dir(backups)
        try:
            api.atomic(orch / "tests/suites.conf", post.decode())
            assert (orch / "tests/suites.conf").read_bytes() == post, "atomic replacement differs"
        except BaseException:
            if (orch / "tests/suites.conf").read_bytes() == post:
                api.atomic(orch / "tests/suites.conf", baseline.decode())
            raise
    try:
        assert store.registration_entries(child_name) == child_entries
        assert store.registration_entries(remotion_name) == remotion_entries
        raw = candidate.decode().split(None, 2)[2].rstrip("\n")
        assert child_name in store.names_for_suite("agent", "full-farm", raw)
    except BaseException:
        with store.mutex():
            if (orch / "tests/suites.conf").read_bytes() == post:
                api.atomic(orch / "tests/suites.conf", baseline.decode())
        raise
    print("backup=" + str(backup))
    print("pre_sha256=" + hashlib.sha256(baseline).hexdigest())
    print("post_sha256=" + hashlib.sha256(post).hexdigest())
    print("replaced=" + repr(old[0]))
    print("row=" + repr(candidate))
    print("outside_bytes=unchanged; child row source packet installed; Farm preflight still required")
PY
```

The installer runs the normal maker’s read-only child provenance probe; it runs no pytest body.
Farm must run the rendered row's parent and `python -I` child/import preflight
after installation, then use the existing `test-run` lease path for one
checkpoint.  A synthetic packet test is not an actual Farm READY result.

The installed Store has no verified-child API. Its actual interfaces are
`registration_entries(name)`, `acquire(names)`, and `names_for_suite(repo, suite,
command)`. Registration validation is read-only but does not validate installed
packages. This packet therefore invokes only the pinned normal maker's existing
`STORE_VERIFY` and freeze-identity scripts, plus its exact `report_bytes` function;
it never calls `ensure`, a builder, or a repair path. Store owner, key, entry and
report projections are checked by the existing Store and bound to the exact tuple.

The production caller remains `ORCH/bin/test-run`: line 15 selects the row with
awk, `suite_lease` binds original row bytes and acquires dependencies before the
snapshot, then the row runs from the Agent snapshot. `env -i` removes the service's
ambient `PYTHONPATH`. The snapshot's lock/client files must match the exact Agent
receipt; a different staging tree fails before pytest. Farm must submit the exact
Agent checkout, including staged changes only if they reproduce those bytes.
No full suite is authorized by this packet. Private tests replace only pytest's
body with a bounded diagnostic; no private fixture is Farm READY.
