#!/bin/sh
set -eu

# The private392 consumer is an HTTP/Door test, not a hosted-page test.  Keep
# DirectHarness's existing hosted-origin listener alive with a disposable
# index.html, while refusing to run unless the reviewed producer pair and
# generated Runtime contract are present.

APP_ROOT=${1:-${PWD}}
case "$APP_ROOT" in
  /*) ;;
  *) echo "APP_ROOT must be absolute" >&2; exit 2 ;;
esac
test -f "$APP_ROOT/package.json"
test -f "$APP_ROOT/tests/integration/runtimePrivate392Consumer.test.ts"
test -x "$APP_ROOT/node_modules/.bin/vitest"

required_env() {
  name=$1
  value=$2
  test -n "$value" || { echo "$name is required" >&2; exit 2; }
  case "$value" in
    /*) ;;
    *) echo "$name must be an absolute path" >&2; exit 2 ;;
  esac
  test -e "$value" || { echo "$name does not exist: $value" >&2; exit 2; }
}

required_env ASTRID_CHECKOUT "${ASTRID_CHECKOUT-}"
required_env ASTRID_PYTHON "${ASTRID_PYTHON-}"
required_env ASTRID_RUNTIME_CHECKOUT "${ASTRID_RUNTIME_CHECKOUT-}"
required_env ASTRID_RUNTIME_PYTHON "${ASTRID_RUNTIME_PYTHON-}"
test -x "$ASTRID_PYTHON"
test -x "$ASTRID_RUNTIME_PYTHON"
test -z "${ASTRID_PUBLIC_CHECKOUT-}" || { echo 'ASTRID_PUBLIC_CHECKOUT is forbidden' >&2; exit 2; }
test -z "${ASTRID_APP_DIRECT_DIST-}" || { echo 'ASTRID_APP_DIRECT_DIST must be supplied only by this runner' >&2; exit 2; }
test -z "${PYTHONPATH-}" || { echo 'PYTHONPATH must be unset; the runner supplies exact import roots' >&2; exit 2; }

AGENT_SHA=1303ce6be32e7bd96ed5c6b35afcb15819e81b50
AGENT_TREE=2f2685d85c3f65b458795100a8045371eb19ee06
AGENT_PARENT=e010e6a3868e963471244491bb6672c3e4a5135e
AGENT_SCHEMA=39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d
RUNTIME_SHA=f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414
RUNTIME_TREE=8be43e13acb436120f8a63b1a178d64c49422461
RUNTIME_SCHEMA=242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042
RUNTIME_BUNDLE=fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3
RUNTIME_ARTIFACTS=52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d
RUNTIME_COMPONENTS=1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
DRIVER_SHA=a800a8f908a52cc74069387552636dc5bab511d7434ee50ebf3e49174c47e7af

test "$(git -C "$ASTRID_CHECKOUT" rev-parse HEAD)" = "$AGENT_SHA"
test "$(git -C "$ASTRID_CHECKOUT" rev-parse HEAD^)" = "$AGENT_PARENT"
test "$(git -C "$ASTRID_CHECKOUT" rev-parse 'HEAD^{tree}')" = "$AGENT_TREE"
test -z "$(git -C "$ASTRID_CHECKOUT" status --porcelain=v1 --untracked-files=all)"
test "$(sha256sum "$ASTRID_CHECKOUT/astrid/core/timeline/schema/edit-command.schema.json" | cut -d' ' -f1)" = "$AGENT_SCHEMA"

test "$(git -C "$ASTRID_RUNTIME_CHECKOUT" rev-parse HEAD)" = "$RUNTIME_SHA"
test "$(git -C "$ASTRID_RUNTIME_CHECKOUT" rev-parse 'HEAD^{tree}')" = "$RUNTIME_TREE"
test -z "$(git -C "$ASTRID_RUNTIME_CHECKOUT" status --porcelain=v1 --untracked-files=all)"

# Keep the Python executable and imported source roots explicit.  A qualified
# venv may contain an editable install, so the source checkout must win via an
# exact PYTHONPATH and the imported module must resolve inside that checkout.
probe_import() {
  checkout=$1
  python=$2
  module=$3
  PYTHONPATH="$checkout" EXPECTED_ROOT="$checkout" EXPECTED_PYTHON="$python" EXPECTED_MODULE="$module" \
    "$python" - <<'PY'
import importlib
import os
from pathlib import Path
import sys

expected_python = Path(os.environ['EXPECTED_PYTHON']).resolve()
actual_python = Path(sys.executable).resolve()
if actual_python != expected_python:
    raise SystemExit(f'Python executable changed: {actual_python} != {expected_python}')
module = importlib.import_module(os.environ['EXPECTED_MODULE'])
module_file = Path(module.__file__).resolve()
root = Path(os.environ['EXPECTED_ROOT']).resolve()
if root not in module_file.parents:
    raise SystemExit(f'import escaped exact checkout: {module_file} not under {root}')
PY
}

probe_import "$ASTRID_CHECKOUT" "$ASTRID_PYTHON" astrid
probe_import "$ASTRID_CHECKOUT" "$ASTRID_PYTHON" astrid_runtime_client
probe_import "$ASTRID_RUNTIME_CHECKOUT" "$ASTRID_RUNTIME_PYTHON" runtime_protocol

# This is intentionally a hard guard.  The current public 2c4 lock must not be
# relabeled as the private f8da contract.
(
  cd "$APP_ROOT"
  node scripts/vendor-lock.mjs check runtime.lock.json --producer "$ASTRID_RUNTIME_CHECKOUT"
)

APP_ROOT="$APP_ROOT" AGENT_CHECKOUT="$ASTRID_CHECKOUT" RUNTIME_CHECKOUT="$ASTRID_RUNTIME_CHECKOUT" \
  EXPECTED_SCHEMA="$RUNTIME_SCHEMA" EXPECTED_BUNDLE="$RUNTIME_BUNDLE" \
  EXPECTED_ARTIFACTS="$RUNTIME_ARTIFACTS" EXPECTED_COMPONENTS="$RUNTIME_COMPONENTS" \
  EXPECTED_DRIVER="$DRIVER_SHA" node --input-type=module <<'NODE'
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';

const root = path.resolve(process.env.APP_ROOT);
const agent = path.resolve(process.env.AGENT_CHECKOUT);
const runtime = path.resolve(process.env.RUNTIME_CHECKOUT);
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const gitShow = (checkout, spec) => execFileSync('git', ['-C', checkout, 'show', spec]);
const manifestBytes = gitShow(runtime, 'HEAD:contract/artifacts.json');
const manifest = JSON.parse(manifestBytes);
if (Object.keys(manifest.artifacts ?? {}).length !== 75) throw new Error('private392 Runtime manifest is not the reviewed 75-artifact set');
if (manifest.version !== `sha256:${process.env.EXPECTED_ARTIFACTS}`) throw new Error('private392 Runtime artifact version changed');
if (digest(manifestBytes) !== '1c684f53582a44b12a7438b79ddeace8696768b4fb98f8f704d58a640fa6cd5f') {
  throw new Error('private392 Runtime component manifest bytes changed');
}
for (const [relative, expected] of Object.entries(manifest.artifacts)) {
  const bytes = gitShow(runtime, `HEAD:${relative}`);
  if (`sha256:${digest(bytes)}` !== expected) throw new Error(`Runtime artifact hash mismatch: ${relative}`);
}
const bundle = gitShow(runtime, 'HEAD:runtime_protocol/schemas/timeline-commit-bundle.json');
if (digest(bundle) !== process.env.EXPECTED_BUNDLE) throw new Error('Runtime bundle custody mismatch');
const components = gitShow(runtime, 'HEAD:contract/component-manifest.json');
if (digest(components) !== process.env.EXPECTED_COMPONENTS) throw new Error('Runtime component custody mismatch');
const metadata = gitShow(runtime, 'HEAD:runtime_protocol/contract_metadata.py').toString('utf8');
if (!metadata.includes(`sha256:${process.env.EXPECTED_SCHEMA}`)) throw new Error('Runtime health/schema custody mismatch');
const runtimeSchema = gitShow(runtime, 'HEAD:contract/schemas/edit-command.json');
const agentSchema = readFileSync(path.join(agent, 'astrid/core/timeline/schema/edit-command.schema.json'));
if (!runtimeSchema.equals(agentSchema) || digest(agentSchema) !== '39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d') {
  throw new Error('Agent/Runtime schema source mismatch');
}
if (digest(readFileSync(path.join(root, 'tests/integration/runtimePrivate392Consumer.test.ts'))) !== process.env.EXPECTED_DRIVER) {
  throw new Error('private392 driver source changed from the reviewed case');
}
NODE

RUN_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/private392-http.XXXXXX")
DIST_ROOT="$RUN_ROOT/dist"
cleanup() {
  rm -rf -- "$RUN_ROOT"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
mkdir -p "$DIST_ROOT" "$RUN_ROOT/tmp" "$RUN_ROOT/vite-cache"
printf '%s\n' '<!doctype html><html><head><meta charset="utf-8"><title>private392 HTTP harness</title></head><body></body></html>' > "$DIST_ROOT/index.html"

export ASTRID_APP_DIRECT_DIST="$DIST_ROOT"
export TMPDIR="$RUN_ROOT/tmp"
export VITE_CACHE_DIR="$RUN_ROOT/vite-cache"
export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=4096}"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONNOUSERSITE=1

cd "$APP_ROOT"
status=0
node_modules/.bin/vitest run \
  --config config/testing/vitest.runtime-restore.integration.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  --testNamePattern='accepts the dormant visual seam member' \
  tests/integration/runtimePrivate392Consumer.test.ts || status=$?
exit "$status"
