#!/bin/sh
set -eu

WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D09-invocation-return-2255
EVIDENCE="$WORKER/evidence"
mkdir -p "$EVIDENCE"
CHILD=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e
PYTHON="$CHILD/bin/python"
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
NODE_DIR=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
export CHILD RUNTIME PROFILE NODE SCHEMA NODE_DIR
export HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1
export PATH="$NODE_DIR:$CHILD/bin:/usr/bin:/bin" PYTHONPATH="$PWD:$RUNTIME"
export ASTRID_HOST_EXECUTION_PROFILE=source ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE" ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules" ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SCHEMA"
unset ASTRID_PACKS_PATH
if [ -z "${TMPDIR:-}" ]; then TMPDIR=$(mktemp -d /tmp/d09-current-2255.XXXXXX); export TMPDIR; fi
TMPROOT="$TMPDIR"

EXPECTED="$EVIDENCE/expected-nodeids.txt"
cat > "$EXPECTED" <<'EOF'
tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[saved]
tests/integrations/test_d09_managed_scene_only.py::test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[candidate]
tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
EOF

"$PYTHON" -P - "$EVIDENCE/preflight.json" "$EXPECTED" <<'PY'
import ast, hashlib, json, os, subprocess, sys
from pathlib import Path

out, expected_path = map(Path, sys.argv[1:])
expected_nodeids = expected_path.read_text().splitlines()
root = Path.cwd().resolve()
runtime = Path(os.environ["RUNTIME"]).resolve()
profile = Path(os.environ["PROFILE"]).resolve()
node = Path(os.environ["NODE"]).resolve()
schema = Path(os.environ["SCHEMA"]).resolve()
fixture = root / "tests/integrations/test_d09_managed_scene_only.py"
source_files = {
    "startup": root / "tests/core/execution/test_worker_startup_identity.py",
    "host": root / "tests/core/execution/test_remotion_host_session.py",
    "generic": root / "tests/core/execution/test_generic_host_actions_v3.py",
    "d09": fixture,
}
expected_source_hashes = {
    "startup": "6fc57103cb5419a3616dd6c4305774d988eb19be2233acd92ae86da4feb38c83",
    "host": "2f8c6f0d7709ae3c84bdbcaa8c275fdd4d8534ceface9926772a6247eeecf9ae",
    "generic": "32e8958cce8bbcae19f1771f131e043171d0ac5f62732bfdefe8a1dbcd54708d",
    "d09": "03d79f9ea17c6c3c899aa1268a3b9ee4f8bd21681063a2f5be018d86eb887417",
}
body_expected = {
    "test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle": "45d91993777505aae09cba6850951f49f87208339887ec6e8e6371e9d61ce6d2",
    "test_public_checkout_check_uses_retained_managed_scene_result": "a23f1d00ca84ff1c9240f881d6d16b3d545e68234d279e42f27cefa8c623c477",
}
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert runtime == Path("/home/user/work/wt/rt-pin-8ea0766f")
assert profile == Path("/home/user/work/runtimes/agent-remotion-v3-819acf-1110")
assert node.is_file() and os.access(node, os.X_OK) and schema.is_dir()
assert os.environ.get("ASTRID_HOST_EXECUTION_PROFILE") == "source"
assert os.environ.get("PYTHONNOUSERSITE") is None
assert os.environ.get("ASTRID_PACKS_PATH") is None
assert os.environ.get("PYTHONPATH") == f"{root}:{runtime}"
assert subprocess.run([str(node), "--version"], check=True, capture_output=True, text=True).stdout.strip() == "v20.19.4"
assert digest(profile / "package-lock.json") == "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"
archive = profile / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
assert digest(archive) == "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
package = json.loads((profile / "package.json").read_text())
assert package["dependencies"]["@banodoco/timeline-composition"] == "file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
assert json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())["version"] == "0.0.14"
actual_source_hashes = {name: digest(path) for name, path in source_files.items()}
assert actual_source_hashes == expected_source_hashes, actual_source_hashes
text = fixture.read_text()
tree = ast.parse(text)
actual_body_hashes = {n.name: hashlib.sha256(ast.get_source_segment(text, n).encode()).hexdigest()
                      for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in body_expected}
assert actual_body_hashes == body_expected, actual_body_hashes
facts = {
    "status": "preflight-passed",
    "agent_sha": subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip(),
    "runtime_sha": subprocess.run(["git", "-C", str(runtime), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip(),
    "child": os.environ["CHILD"], "child_python": str(Path(sys.executable).resolve()),
    "runtime_checkout": str(runtime), "source_execution_profile": "source", "profile": str(profile),
    "node": str(node), "node_version": "v20.19.4", "schema": str(schema),
    "source_hashes": actual_source_hashes, "test_body_hashes": actual_body_hashes,
    "pytest_argv": [str(Path(sys.executable).resolve()), "-P", "-m", "pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider", *expected_nodeids],
    "context": {name: os.environ.get(name) for name in (
        "ASTRID_HOST_EXECUTION_PROFILE", "ASTRID_RUNTIME_CHECKOUT", "ASTRID_REMOTION_PROJECT_DIR",
        "ASTRID_NODE_EXECUTABLE", "ASTRID_TEST_NODE_MODULES", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH",
        "PYTHONPATH", "PYTHONNOUSERSITE", "ASTRID_PACKS_PATH", "PATH", "TMPDIR")},
    "exact_three_nodeids": expected_nodeids,
}
out.write_text(json.dumps(facts, indent=2, sort_keys=True) + "\n")
print(json.dumps(facts, indent=2, sort_keys=True))
PY

"$PYTHON" -P - <<'PY' > "$EVIDENCE/source-import-before.json"
import importlib.metadata, json, os, sys
from pathlib import Path
import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol
root, runtime = Path.cwd().resolve(), Path(os.environ["RUNTIME"]).resolve()
origins = {name: str(Path(module.__file__).resolve()) for name, module in {
    "astrid": astrid, "astrid_runtime": astrid_runtime,
    "astrid_runtime_client": astrid_runtime_client, "runtime_protocol": runtime_protocol}.items()}
assert Path(origins["astrid"]).is_relative_to(root)
assert Path(origins["astrid_runtime_client"]).is_relative_to(root)
assert Path(origins["runtime_protocol"]).is_relative_to(runtime)
assert Path(origins["astrid_runtime"]).is_relative_to(runtime)
assert os.environ.get("PYTHONNOUSERSITE") is None
print(json.dumps({"python": str(Path(sys.executable).resolve()), "origins": origins,
                  "astrid_version": importlib.metadata.version("astrid"),
                  "astrid_runtime_version": importlib.metadata.version("astrid-runtime"),
                  "PYTHONPATH": os.environ.get("PYTHONPATH"),
                  "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE")}, sort_keys=True))
PY

git status --porcelain=v1 > "$EVIDENCE/no-write-status-before.txt"
set +e
"$PYTHON" -P -m pytest -q -o addopts= -p no:cacheprovider --basetemp="$TMPROOT/d09-pytest" $(cat "$EXPECTED") > "$EVIDENCE/pytest.log" 2>&1
test_status=$?
set -e

"$PYTHON" -P - "$EVIDENCE/probe-stderr-index.json" "$EVIDENCE" <<'PY'
import json, re, shutil, sys
from pathlib import Path
index, evidence = map(Path, sys.argv[1:])
log = evidence / "pytest.log"
names = sorted(set(re.findall(r"/tmp/astrid-probe-logs/[A-Za-z0-9_.-]+\\.stderr\\.log", log.read_text())))
retained = []
for number, raw in enumerate(names):
    source = Path(raw)
    if source.is_file() and source.stat().st_size <= 5 * 1024 * 1024:
        target = evidence / f"probe-stderr-{number}-{source.name}"
        shutil.copyfile(source, target)
        retained.append(str(target))
index.write_text(json.dumps({"referenced": names, "retained": retained}, indent=2) + "\n")
PY

"$PYTHON" -P - <<'PY' > "$EVIDENCE/source-import-after.json"
import json, os, sys
from pathlib import Path
import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol
root, runtime = Path.cwd().resolve(), Path(os.environ["RUNTIME"]).resolve()
origins = {name: str(Path(module.__file__).resolve()) for name, module in {
    "astrid": astrid, "astrid_runtime": astrid_runtime,
    "astrid_runtime_client": astrid_runtime_client, "runtime_protocol": runtime_protocol}.items()}
assert Path(origins["astrid"]).is_relative_to(root)
assert Path(origins["astrid_runtime_client"]).is_relative_to(root)
assert Path(origins["runtime_protocol"]).is_relative_to(runtime)
assert Path(origins["astrid_runtime"]).is_relative_to(runtime)
assert os.environ.get("PYTHONNOUSERSITE") is None
print(json.dumps({"python": str(Path(sys.executable).resolve()), "origins": origins,
                  "PYTHONPATH": os.environ.get("PYTHONPATH"),
                  "PYTHONNOUSERSITE": os.environ.get("PYTHONNOUSERSITE")}, sort_keys=True))
PY

"$PYTHON" -P - "$EVIDENCE/manifest-receipt.json" <<'PY'
import json, os, sys
from pathlib import Path
out = Path(sys.argv[1])
root = Path(os.environ.get("TMPDIR", "/tmp")).resolve()
matches = sorted(path for path in root.rglob("*.json") if path.name.startswith(("remotion-validation-", "failed-validation-")) and path.is_file() and path.stat().st_size <= 10 * 1024 * 1024)
retained = []
for index, path in enumerate(matches):
    target = out.parent / f"manifest-{index}-{path.name}"
    target.write_bytes(path.read_bytes())
    retained.append(str(target))
out.write_text(json.dumps({"tmp_root": str(root), "files": [str(path) for path in matches], "retained": retained, "bytes": sum(path.stat().st_size for path in matches)}, indent=2) + "\n")
PY

git status --porcelain=v1 > "$EVIDENCE/no-write-status.txt"
cmp "$EVIDENCE/no-write-status-before.txt" "$EVIDENCE/no-write-status.txt"
printf 'pytest_exit=%s\n' "$test_status" > "$EVIDENCE/result.txt"
if [ "$test_status" -eq 0 ]; then grep -Eq '3 passed' "$EVIDENCE/pytest.log"; fi
exit "$test_status"
