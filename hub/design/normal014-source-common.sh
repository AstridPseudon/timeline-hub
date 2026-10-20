#!/bin/sh
set -eu

# Private, test-only source preparation for normal014.  This file is called by
# the central-suite wrappers; it never writes into a source checkout.

AGENT_REPO=${AGENT_REPO:-/home/user/peteromallet/astrid-agent}
RUNTIME_REPO=${RUNTIME_REPO:-/home/user/banodoco/banodoco-workspace-runtime}
AGENT_SHA=3c4f6de4fa777323b3386c01c7266b619b86af6d
AGENT_TREE=aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c
RUNTIME_SHA=202074110717146fc7f08af2306a8dd7f695b0b1
RUNTIME_TREE=ee39286bd0eb27d4075074cc4785d6d15e33f243
PRODUCER_SHA=a0dca16975dfe8f5e762703b99d9791a16cf7fd7
PRODUCER_TREE=4b7dd0fe44be973c344bab3de568eaf0bdd28476
ARTIFACT_SHA=sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0
MANIFEST_SHA=ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815
SCHEMA_SHA=6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
WIRE_SHA=sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59
MARKER_SHA=150a7abb340040e45c34742bc871ef83caab0575
D05E_SHA=d05e6383f4ccaf7541698a65b2737fbc5f3f0fbb
LOCKED_GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph
LOCKED_GRAPH_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar
LOCKED_GRAPH_ARCHIVE_SHA=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
LOCKED_COMPOSITION_SHA=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738

prepare_checkout() {
  source_repo=$1
  source_sha=$2
  destination=$3
  git clone --quiet --shared --no-checkout "$source_repo" "$destination"
  git -C "$destination" checkout --quiet --detach "$source_sha"
  test "$(git -C "$destination" rev-parse HEAD)" = "$source_sha"
  test "$(git -C "$destination" show -s --format=%T HEAD)" = "$4"
  test -z "$(git -C "$destination" status --porcelain=v1 --untracked-files=all)"
}

verify_artifacts() {
  runtime=$1
  producer=$2
  RUNTIME="$runtime" PRODUCER="$producer" EXPECTED_MANIFEST="$MANIFEST_SHA" \
    EXPECTED_ARTIFACT="$ARTIFACT_SHA" EXPECTED_SCHEMA="$SCHEMA_SHA" python3 - <<'PY'
import hashlib, json, os, subprocess
from pathlib import Path

runtime = Path(os.environ["RUNTIME"])
producer = Path(os.environ["PRODUCER"])
def git_show(repo, spec):
    return subprocess.check_output(["git", "-C", str(repo), "show", spec])
def digest(data):
    return hashlib.sha256(data).hexdigest()

manifest_bytes = git_show(runtime, "HEAD:contract/artifacts.json")
manifest = json.loads(manifest_bytes)
assert manifest["producer"] == "astrid-runtime"
assert manifest["version"] == os.environ["EXPECTED_ARTIFACT"]
assert len(manifest["artifacts"]) == 75
assert digest(manifest_bytes) == os.environ["EXPECTED_MANIFEST"]
for relative, expected in manifest["artifacts"].items():
    candidate = git_show(runtime, f"HEAD:{relative}")
    original = git_show(producer, f"HEAD:{relative}")
    assert candidate == original, relative
    assert f"sha256:{digest(candidate)}" == expected, relative

runtime_schema = git_show(runtime, "HEAD:contract/schemas/edit-command.json")
agent_schema = git_show(Path(os.environ["AGENT"]), "HEAD:astrid/core/timeline/schema/edit-command.schema.json")
assert digest(runtime_schema) == os.environ["EXPECTED_SCHEMA"]
assert agent_schema == runtime_schema
print(f"verified artifacts=75 manifest={digest(manifest_bytes)} schema={digest(runtime_schema)}")
PY
}

verify_locked_graph() {
  test -d "$LOCKED_GRAPH/node_modules"
  test -f "$LOCKED_GRAPH_ARCHIVE"
  test "$(sha256sum "$LOCKED_GRAPH_ARCHIVE" | cut -d' ' -f1)" = "$LOCKED_GRAPH_ARCHIVE_SHA"
  test "$(node -p "require('$LOCKED_GRAPH/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13
  test "$(tar -xOf "$LOCKED_GRAPH_ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | sha256sum | cut -d' ' -f1)" = "$LOCKED_COMPOSITION_SHA"
  test "$(realpath "$LOCKED_GRAPH/node_modules")" = "$LOCKED_GRAPH/node_modules"
  test -z "$(find -P "$LOCKED_GRAPH" -type f -perm /022 -print -quit)"
  GRAPH="$LOCKED_GRAPH" node --input-type=module - <<'JS'
const { computeMediaTrim } = await import(`file://${process.env.GRAPH}/node_modules/@banodoco/timeline-composition/dist/evaluation.js`);
if (typeof computeMediaTrim !== 'function') throw new Error('locked public13 graph lacks computeMediaTrim');
const trim = computeMediaTrim({ from: 0.5, to: 1.5 }, 30);
if (trim.trimBefore !== 15 || trim.trimAfter !== 45) throw new Error(`unexpected public13 trim: ${JSON.stringify(trim)}`);
JS
}

prepare_private_python() {
  run_root=$1
  base=${NORMAL014_PYTHON_BASE:-/home/user/work/venv-app2-native/bin/python}
  test -x "$base"
  python_root="$run_root/python-runtime"
  "$base" -m venv --copies "$python_root"
  PIP_CACHE_DIR="$run_root/pip-cache" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    "$python_root/bin/python" -m pip install --disable-pip-version-check --no-input \
      'jsonschema>=4.18' 'referencing>=0.30' 'PyYAML>=6.0' 'pytest>=8' 'pytest-timeout>=2.4' >/dev/null
  NORMAL014_PYTHON="$python_root/bin/python"
}

verify_python_imports_and_collection() {
  python=$1
  agent=$2
  runtime=$3
  PYTHONPATH="$agent:$runtime:$runtime/packages/python" \
    "$python" - <<'PY'
import importlib
for module in (
    "astrid.core.gateway",
    "astrid.core.dev.cross_client",
    "astrid.sdk.client",
    "astrid.sdk.timeline.capture",
    "astrid.sdk.timeline._command_state",
    "astrid.sdk.timeline._clip_scalar_commands",
    "astrid.sdk.timeline.commands",
    "astrid.sdk.timeline.commit",
    "astrid.sdk.timeline.native_occurrence_create",
    "astrid.sdk.timeline.native_occurrence_media_commands",
    "astrid.sdk.timeline.native_parent_media_commands",
    "runtime_protocol.timeline_commit_provider",
    "runtime_protocol.daemon",
    "runtime_protocol.store",
    "runtime_protocol.errors",
    "runtime_protocol.service",
    "astrid_runtime_client",
):
    importlib.import_module(module)
PY
  ASTRID_CHECKOUT="$agent" PYTHONPATH="$agent:$runtime:$runtime/packages/python" \
    "$python" -m astrid --help >/dev/null
  PYTHONPATH="$agent:$runtime:$runtime/packages/python" \
    ASTRID_CHECKOUT="$agent" "$python" -m pytest --collect-only -q -c /dev/null -p no:cacheprovider \
      "$runtime/tests/test_timeline_clip_replacement.py" | grep -F \
      'test_native_parent_clip_swap_route_replaces_parent_media'
}

prepare_sources() {
  root=$1
  mkdir -p "$root"
  prepare_checkout "$AGENT_REPO" "$AGENT_SHA" "$root/agent-3c4" "$AGENT_TREE"
  prepare_checkout "$RUNTIME_REPO" "$RUNTIME_SHA" "$root/runtime-202" "$RUNTIME_TREE"
  prepare_checkout "$RUNTIME_REPO" "$PRODUCER_SHA" "$root/producer-a0" "$PRODUCER_TREE"
  git -C "$root/runtime-202" merge-base --is-ancestor "$PRODUCER_SHA" "$RUNTIME_SHA"
  AGENT="$root/agent-3c4" verify_artifacts "$root/runtime-202" "$root/producer-a0"
  test "$(git -C "$root/agent-3c4" show -s --format=%T HEAD)" = "$AGENT_TREE"
  test "$(git -C "$root/runtime-202" show -s --format=%T HEAD)" = "$RUNTIME_TREE"
  test "$(git -C "$root/producer-a0" show -s --format=%T HEAD)" = "$PRODUCER_TREE"
}
