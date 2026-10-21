#!/bin/sh
set -eu

# Private, test-only source preparation for normal014.  This file is called by
# the central-suite wrappers; it never writes into a source checkout.

AGENT_REPO=${AGENT_REPO:-/home/user/peteromallet/astrid-agent}
RUNTIME_REPO=${RUNTIME_REPO:-/home/user/banodoco/banodoco-workspace-runtime}

# Keep the historical private qualification as the default.  The current95
# central lanes opt into final95 explicitly; both profiles use the same normal
# checkout, updater, and checker paths below.
NORMAL014_PROFILE=${NORMAL014_PROFILE:-old202}
case "$NORMAL014_PROFILE" in
  old202)
    AGENT_SHA=3c4f6de4fa777323b3386c01c7266b619b86af6d
    AGENT_TREE=aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c
    RUNTIME_SHA=202074110717146fc7f08af2306a8dd7f695b0b1
    RUNTIME_TREE=ee39286bd0eb27d4075074cc4785d6d15e33f243
    PRODUCER_SHA=a0dca16975dfe8f5e762703b99d9791a16cf7fd7
    PRODUCER_TREE=4b7dd0fe44be973c344bab3de568eaf0bdd28476
    ARTIFACT_SHA=sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa
    MANIFEST_SHA=ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815
    MANIFEST_COUNT=75
    SCHEMA_SHA=6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
    WIRE_SHA=sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59
    APP_METADATA_SHA=9b3b8723a8d86a78d57bf83f43eb82914d1d0cd81ae89ebdf993b1560ddc57dd
    APP_GENERATED_SHA=c422ce38279e6df9eb93c5b53993d57e68339b0807d34ed69d85b2408ed98be2
    APP_TYPES_SHA=f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
    APP_SCHEMA_SHA=f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
    ;;
  final95)
    AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb
    AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556
    RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
    RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
    PRODUCER_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
    PRODUCER_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
    ARTIFACT_SHA=sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
    MANIFEST_SHA=a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
    MANIFEST_COUNT=76
    SCHEMA_SHA=6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
    WIRE_SHA=sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
    APP_METADATA_SHA=4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
    APP_GENERATED_SHA=c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
    APP_TYPES_SHA=f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
    APP_SCHEMA_SHA=f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
    ;;
  *)
    echo "unsupported NORMAL014_PROFILE: $NORMAL014_PROFILE (expected old202 or final95)" >&2
    exit 2
    ;;
esac

# final95 has two separately reviewed App roots.  The suite selects the
# existing source role; the values are closed here rather than accepted from
# the caller as arbitrary source identity.
NORMAL014_APP_SOURCE=${NORMAL014_APP_SOURCE:-bootstrap}
APP_PIN_RUNTIME_LOCK_SHA=770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
APP_PIN_METADATA_SHA=4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
APP_PIN_GENERATED_SHA=c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
APP_PIN_TYPES_SHA=f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
case "$NORMAL014_PROFILE:$NORMAL014_APP_SOURCE" in
  final95:parent)
    APP_ROOT_SHA=25155ccb22728780a3ecd6379a929cad75cc1400
    APP_ROOT_TREE=972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7
    ;;
  final95:bootstrap)
    APP_ROOT_SHA=dfdbef10f9d8ccf1a630f000cd076023918ead8a
    APP_ROOT_TREE=33674ef4bbaa4b043baed77492621095cccc28f7
    ;;
  final95:*)
    echo "unsupported NORMAL014_APP_SOURCE: $NORMAL014_APP_SOURCE (expected parent or bootstrap)" >&2
    exit 2
    ;;
esac

# Both private candidates start from the checked-in public013 App lock.  The
# selected profile is applied only by the normal updater below.
# final95's checked-in App lock already carries the final95 Runtime source.
APP_BASE_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
MARKER_SHA=150a7abb340040e45c34742bc871ef83caab0575
D05E_SHA=d05e6383f4ccaf7541698a65b2737fbc5f3f0fbb
LOCKED_GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph
LOCKED_GRAPH_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar
LOCKED_GRAPH_ARCHIVE_SHA=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
LOCKED_COMPOSITION_SHA=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738

normal014_cleanup_run_root() {
  normal014_status=$1
  if [ "${cleanup:-1}" = 1 ] && [ "${normal014_run_root_owned:-0}" = 1 ]; then
    rm -rf -- "$run_root" || :
  fi
  return "$normal014_status"
}

normal014_signal_trap() {
  normal014_signal=$1
  normal014_status=$2
  trap - "$normal014_signal"
  normal014_cleanup_run_root "$normal014_status" || :
  kill -"$normal014_signal" "$$"
}

normal014_start_run() {
  normal014_tmp_parent=${TMPDIR:-/tmp}
  cleanup=1
  if [ "${NORMAL014_KEEP_TEMP:-0}" = 1 ]; then cleanup=0; fi
  normal014_run_root_owned=0
  if [ -n "${NORMAL014_RUN_ROOT:-}" ]; then
    run_root=$NORMAL014_RUN_ROOT
  else
    run_root=$(mktemp -d "$normal014_tmp_parent/$1.XXXXXX")
    normal014_run_root_owned=1
  fi
  trap 'normal014_cleanup_run_root "$?"' EXIT
  trap 'normal014_signal_trap HUP "$?"' HUP
  trap 'normal014_signal_trap INT "$?"' INT
  trap 'normal014_signal_trap TERM "$?"' TERM
}

normal014_use_private_tmp() {
  mkdir -p "$run_root/tmp"
  TMPDIR=$run_root/tmp
  export TMPDIR
}

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
    EXPECTED_ARTIFACT="$ARTIFACT_SHA" EXPECTED_SCHEMA="$SCHEMA_SHA" \
    EXPECTED_MANIFEST_COUNT="$MANIFEST_COUNT" python3 - <<'PY'
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
assert len(manifest["artifacts"]) == int(os.environ["EXPECTED_MANIFEST_COUNT"])
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
print(f"verified artifacts={len(manifest['artifacts'])} manifest={digest(manifest_bytes)} schema={digest(runtime_schema)}")
PY
}

verify_app_source() {
  if [ "$NORMAL014_PROFILE" != final95 ]; then
    return 0
  fi
  app_root=$(CDPATH= cd -- "$1" && pwd)
  test -f "$app_root/package.json"
  test "$(realpath "$app_root")" = "$app_root"
  test "$(realpath "$(git -C "$app_root" rev-parse --show-toplevel)")" = "$app_root"
  test "$(git -C "$app_root" rev-parse HEAD)" = "$APP_ROOT_SHA"
  test "$(git -C "$app_root" rev-parse 'HEAD^{tree}')" = "$APP_ROOT_TREE"
  test -z "$(git -C "$app_root" status --porcelain=v1 --untracked-files=all)"
  for pin_path in \
    runtime.lock.json \
    src/integrations/runtime/generated-contract-metadata.ts \
    src/integrations/runtime/generated.ts \
    src/integrations/runtime/timeline-commit-types.ts
  do
    case "$pin_path" in
      runtime.lock.json) expected_pin_sha=$APP_PIN_RUNTIME_LOCK_SHA ;;
      src/integrations/runtime/generated-contract-metadata.ts) expected_pin_sha=$APP_PIN_METADATA_SHA ;;
      src/integrations/runtime/generated.ts) expected_pin_sha=$APP_PIN_GENERATED_SHA ;;
      src/integrations/runtime/timeline-commit-types.ts) expected_pin_sha=$APP_PIN_TYPES_SHA ;;
    esac
    test "$(sha256sum "$app_root/$pin_path" | cut -d' ' -f1)" = "$expected_pin_sha"
  done
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

prepare_private_node_graph() {
  source_node_modules=$1
  private_node_modules=$2
  test "$source_node_modules" != "$private_node_modules"
  test "$(realpath "$source_node_modules")" = "$source_node_modules"
  test ! -e "$private_node_modules"
  SOURCE_NODE_MODULES="$source_node_modules" PRIVATE_NODE_MODULES="$private_node_modules" node --input-type=module - <<'JS'
import { lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, statSync, symlinkSync } from 'node:fs';
import path from 'node:path';

const source = realpathSync(process.env.SOURCE_NODE_MODULES);
const destination = path.resolve(process.env.PRIVATE_NODE_MODULES);
if (source === destination) throw new Error('private node graph must not be the locked source graph');
mkdirSync(destination, { recursive: true });
const binDirectory = path.join(destination, '.bin');
mkdirSync(binDirectory);

const packageDirectories = [];
for (const entry of readdirSync(source, { withFileTypes: true })) {
  if (entry.name === '.bin') continue;
  if (entry.name.startsWith('@')) {
    const scopeSource = path.join(source, entry.name);
    if (!statSync(scopeSource).isDirectory()) continue;
    const scopeDestination = path.join(destination, entry.name);
    mkdirSync(scopeDestination);
    for (const scopedEntry of readdirSync(scopeSource, { withFileTypes: true })) {
      if (scopedEntry.name === '.bin') continue;
      const sourcePackage = path.join(scopeSource, scopedEntry.name);
      const destinationPackage = path.join(scopeDestination, scopedEntry.name);
      symlinkSync(sourcePackage, destinationPackage, 'dir');
      packageDirectories.push([`${entry.name}/${scopedEntry.name}`, destinationPackage]);
    }
    continue;
  }
  const sourcePackage = path.join(source, entry.name);
  const destinationPackage = path.join(destination, entry.name);
  symlinkSync(sourcePackage, destinationPackage, 'dir');
  packageDirectories.push([entry.name, destinationPackage]);
}

let bins = 0;
for (const [directoryName, packageDirectory] of packageDirectories) {
  let packageJson;
  try {
    packageJson = JSON.parse(readFileSync(path.join(packageDirectory, 'package.json'), 'utf8'));
  } catch (error) {
    if (error?.code === 'ENOENT') continue;
    throw error;
  }
  const declaration = packageJson.bin;
  if (!declaration) continue;
  const declaredBins = typeof declaration === 'string'
    ? { [String(packageJson.name ?? directoryName).split('/').pop()]: declaration }
    : declaration;
  if (!declaredBins || typeof declaredBins !== 'object' || Array.isArray(declaredBins)) {
    throw new Error(`invalid bin declaration in ${directoryName}`);
  }
  for (const [command, target] of Object.entries(declaredBins)) {
    if (!command || typeof target !== 'string' || !target) {
      throw new Error(`invalid bin declaration in ${directoryName}`);
    }
    const resolvedTarget = path.resolve(packageDirectory, target);
    const packageRoot = path.resolve(packageDirectory);
    if (resolvedTarget !== packageRoot && !resolvedTarget.startsWith(`${packageRoot}${path.sep}`)) {
      throw new Error(`bin target escapes ${directoryName}: ${target}`);
    }
    lstatSync(resolvedTarget);
    const link = path.join(binDirectory, command);
    if (lstatSync(link, { throwIfNoEntry: false })) continue;
    symlinkSync(path.relative(binDirectory, path.join(packageDirectory, target)), link);
    bins += 1;
  }
}

console.log(`private node graph: packages=${packageDirectories.length} bins=${bins}`);
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
  prepare_checkout "$AGENT_REPO" "$AGENT_SHA" "$root/agent-6ef" "$AGENT_TREE"
  prepare_checkout "$RUNTIME_REPO" "$RUNTIME_SHA" "$root/runtime-95" "$RUNTIME_TREE"
  prepare_checkout "$RUNTIME_REPO" "$PRODUCER_SHA" "$root/producer-95" "$PRODUCER_TREE"
  git -C "$root/runtime-95" merge-base --is-ancestor "$PRODUCER_SHA" "$RUNTIME_SHA"
  AGENT="$root/agent-6ef" verify_artifacts "$root/runtime-95" "$root/producer-95"
  test "$(git -C "$root/agent-6ef" show -s --format=%T HEAD)" = "$AGENT_TREE"
  test "$(git -C "$root/runtime-95" show -s --format=%T HEAD)" = "$RUNTIME_TREE"
  test "$(git -C "$root/producer-95" show -s --format=%T HEAD)" = "$PRODUCER_TREE"
}
