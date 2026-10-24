# Farm Codex handoff: OPS-farm-agent-full-v3

Source review only.  This packet authorizes no live operation.  Do not invoke
the request, installer, `test-run`, or a checkpoint until the exact normal
D21b child receipt exists and the Farm-owned parent plus isolated-child
preflight has passed.

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
  '<authenticated-Runtime-checkout>' \
  "$TMPDIR/pre-full-farm.suites.conf" "$TMPDIR" <<'PY'
from datetime import datetime, timezone
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys

orch, store_root, packet, child, profile, runtime, baseline_file, backups = map(Path, sys.argv[1:])
source = orch / "bin/bench_store.py"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8", "Store source drift"
spec = importlib.util.spec_from_file_location("bench_store", source)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
tests = orch / "tests"
store = api.Store(store_root, tests)
child_name = "venv-agent-child-farm-v3-9cd"
remotion_name = "agent-remotion-farm-v2-9cd"
agent_sha = "9cd3dbe865a941c052bda04ae0d61306d18f8f26"
runtime_sha = "1d9ddba546f8fb1300f55ff62607ed492719cbaa"
assert store.registered(child_name), "D21b child receipt/registration missing"
child_entries = store.registration_entries(child_name)
assert len(child_entries) == 1 and child_entries[0]["component"] == "child", "child receipt is not singular managed custody"
assert Path(child_entries[0]["path"]) == child and child == child.resolve() and child.is_dir() and not child.is_symlink(), "child path differs from receipt"
assert store.registered(remotion_name), "managed Remotion registration missing"
remotion_entries = store.registration_entries(remotion_name)
assert any(e["component"] == "runtime" and Path(e["path"]) == profile for e in remotion_entries), "Remotion profile differs from receipt"
assert re.fullmatch(r"/[A-Za-z0-9_./-]+", str(profile)) and profile == profile.resolve() and profile.is_dir(), "physical profile path required"
assert re.fullmatch(r"/[A-Za-z0-9_./-]+", str(runtime)) and runtime == runtime.resolve() and runtime.is_dir(), "physical Runtime path required"
assert subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD"], text=True).strip() == runtime_sha, "Runtime receipt SHA mismatch"
assert not subprocess.check_output(["git", "-C", str(runtime), "status", "--porcelain", "--untracked-files=all"], text=True), "Runtime checkout dirty"
assert hashlib.sha256((runtime / "runtime_protocol/external_pack_sources.py").read_bytes()).hexdigest() == "8931d2ae530ff1d6eccbb28dadec4349641fd4e1c19f231dba2616b93be2234e", "Runtime D40 source mismatch"
assert (child / "bin/python").is_file() and (child / "bin/python").resolve().is_relative_to(child), "child interpreter is not retained"
assert (child / ".astrid-source-commit").read_text() == agent_sha + "\n", "Agent marker mismatch"
assert (child / ".astrid-runtime-source-commit").read_text() == runtime_sha + "\n", "Runtime marker mismatch"
client = "\n".join("packages/python/" + name + "=" + digest for name, digest in {
    "astrid_runtime_client/__init__.py": "d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2",
    "astrid_runtime_client/contract_metadata.py": "a79b2e12de96ec8f2c4bf7b6811ccb3538baf18ca839172f7a3d7bf525029aae",
    "astrid_runtime_client/generated.py": "9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904",
    "astrid_runtime_client/timeline_commit_types.py": "88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616",
}.items()) + "\n"
assert (child / ".astrid-runtime-client-identity").read_text().rstrip("\n") + "\n" == client, "client tuple mismatch"
receipt = child / ".provision-report"
assert receipt.is_file() and "status=passed" in receipt.read_text() and agent_sha in receipt.read_text() and runtime_sha in receipt.read_text(), "normal child receipt incomplete"
origins = {}
for line in (child / ".astrid-import-origins").read_text().splitlines():
    name, origin = line.split("=", 1)
    assert name not in origins
    origins[name] = Path(origin).resolve()
assert set(origins) == {"astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"}, "child import proof incomplete"
assert all(path.is_relative_to(child) for path in origins.values()), "child import escaped"
baseline = baseline_file.read_bytes()
row = (packet / "registration-row.txt").read_text()
assert row.endswith("\n") and row.count("\n") == 1 and "PYTHONPATH" not in row
row = row.replace("@CHILD_ROOT@", str(child)).replace("@CHILD_INTERPRETER@", str(child / "bin/python")).replace("@MANAGED_PROFILE@", str(profile)).replace("@RUNTIME_CHECKOUT@", str(runtime))
assert "@" not in row
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

The installer intentionally performs no child import or pytest body itself.
Farm must run the rendered row's parent and `python -I` child/import preflight
after installation, then use the existing `test-run` lease path for one
checkpoint.  A synthetic packet test is not an actual Farm READY result.
