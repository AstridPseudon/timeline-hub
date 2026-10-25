#!/bin/bash
set -euo pipefail

ROOT=/home/user/work
TMP_ROOT=${TMPDIR:?TMPDIR is required}
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
EVIDENCE=$ORCH/workers/agt-OPS-inventory-E2E-portable-sol-1816/evidence
SOURCE_COMMIT=f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe
SOURCE_RUNNER_SHA=4249af6c2f99a01d3eed7fa951a3c2477c25a5e0c6a9c0f61f55f2c505ba4788
SOURCE_MANIFEST_SHA=bcb635d082fdb8835ce814ae79f8313dd27ed21f01926206ea364b01cfd08456
HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py
HELPER_SHA=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2
CANDIDATE_MAKER_SHA=c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e
MIN_RESERVE=5905580032
STOP_LINE=4000000000
ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz
RUNNER_PYTHON=/home/user/work/venv-agent/bin/python
BUILD_PYTHON=/home/user/work/venv-agent/bin/python
CHILD_PYTHON=/usr/bin/python3.13

mkdir -p "$EVIDENCE"
STAGE=prerequisites
on_exit() {
  local rc=$?
  trap - EXIT
  if [ -n "${RESULT:-}" ] && [ -s "$RESULT" ]; then
    cp "$RESULT" "$EVIDENCE/e2e-result.json"
  fi
  printf 'D128/F wrapper stage=%s exit=%s\n' "$STAGE" "$rc" >> "$EVIDENCE/progress.md"
  exit "$rc"
}
trap on_exit EXIT
test -x "$RUNNER_PYTHON" -a -x "$BUILD_PYTHON" -a -x "$CHILD_PYTHON"
test -x "$HELPER"
test "$(sha256sum "$HELPER" | awk '{print $1}')" = "$HELPER_SHA"

# Parse exactly one unsigned decimal Avail field; the df header is not data.
parse_avail() {
  awk '$1 ~ /^[0-9]+$/ { if (++n == 1) value=$1 } END { if (n != 1) exit 1; print value }'
}

assert_numeric_parser() {
  test "$(printf '%s\n' 'Avail' '5905580032' | parse_avail)" = 5905580032
  test "$(printf '%s\n' 'Filesystem Avail' '6710943744' | parse_avail)" = 6710943744
  if printf '%s\n' 'Avail' | parse_avail >/dev/null 2>&1; then return 1; fi
  if printf '%s\n' 'Avail' '5905580032x' | parse_avail >/dev/null 2>&1; then return 1; fi
  if printf '%s\n' 'Avail' '1' '2' | parse_avail >/dev/null 2>&1; then return 1; fi
  if printf '%s\n' 'Avail' '-1' | parse_avail >/dev/null 2>&1; then return 1; fi
}

numeric_avail() {
  local output value
  output=$(df -B1 --output=avail "$1") || return 1
  value=$(printf '%s\n' "$output" | parse_avail) || return 1
  case "$value" in ''|*[!0-9]*) return 1;; esac
  printf '%s\n' "$value"
}

assert_numeric_parser
for name in bash python3 git tar mktemp sha256sum cut grep sed find chmod mv df awk cp mkdir date timeout readlink cat; do
  command -v "$name" >/dev/null
done
test "$(readlink -e "$TMP_ROOT")" = "$TMP_ROOT"
test "$TMP_ROOT" = /tmp/w-f24ccbdde1
test -w "$TMP_ROOT"
test "$(sha256sum "$ARTIFACT" | awk '{print $1}')" = 443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548
test "$(sha256sum "$ORCH/bin/verify_dependency_seed.py" | awk '{print $1}')" = 116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2
test "$(sha256sum "$PWD/ops-child-custody/tests/support.py" | awk '{print $1}')" = 8e61d99631e417e39e95b845f5433525ec25a26f190cd433380ebc75f830ec42
# The unchanged support module binds MAKER and its parent Git lookup to the
# service snapshot. The source1747 runner/fixtures remain exact archived bytes.
export PYTHONPATH="$PWD/ops-child-custody/tests"
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_DISABLE_PIP_VERSION_CHECK=1
"$RUNNER_PYTHON" -c 'import build, setuptools, wheel, packaging, venv, ensurepip, fcntl, unittest.mock; import importlib.metadata as m; assert m.version("setuptools")=="80.9.0"; assert m.version("wheel")=="0.46.3"'
"$CHILD_PYTHON" -I -c 'import sys,venv,ensurepip,fcntl,tarfile; assert sys.version_info >= (3,11)'
python3 -I -c 'import fcntl,hashlib,importlib.util,json,pathlib,subprocess,sys; assert sys.version_info >= (3,11)'
"$RUNNER_PYTHON" - <<'SOURCE_CHECK'
import hashlib, json, os, pathlib, subprocess
root = pathlib.Path.cwd()
commit = 'f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe'
def blob(path, revision=commit):
    return subprocess.check_output(['git', 'show', revision + ':' + path])
def digest(data):
    return hashlib.sha256(data).hexdigest()
assert subprocess.check_output(['git', 'cat-file', '-t', commit]).strip() == b'commit'
assert digest(blob('ops-child-custody/tests/e2e_inventory.py')) == '4249af6c2f99a01d3eed7fa951a3c2477c25a5e0c6a9c0f61f55f2c505ba4788'
manifest = blob('ops-child-custody/e2e-fixtures/tiny/manifest.json')
assert digest(manifest) == 'bcb635d082fdb8835ce814ae79f8313dd27ed21f01926206ea364b01cfd08456'
for role, entry in json.loads(manifest)['roles'].items():
    for name, pin in entry['files'].items():
        path = 'ops-child-custody/e2e-fixtures/tiny/' + role + '/' + name
        assert digest(blob(path)) == pin
        assert subprocess.check_output(['git', 'ls-tree', commit, '--', path]).startswith(b'100644 blob ')
from support import MAKER, block
assert MAKER == root / 'ops-child-custody/make-child-venv'
assert MAKER.is_file() and not MAKER.is_symlink() and os.access(MAKER, os.X_OK)
assert digest(MAKER.read_bytes()) == 'c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e'
parent = blob('ops-child-custody/make-child-venv', '9428f515fcd8dccaef26193438b3ac89f903f5aa')
assert digest(parent) == '0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39'
assert block(parent.decode(), 'STORE_VERIFY') == block(MAKER.read_text(), 'STORE_VERIFY')
SOURCE_CHECK
FREE_BYTES=$(numeric_avail "$ROOT")
test "$FREE_BYTES" -ge "$MIN_RESERVE"

if [ "${1:-}" = --preflight-only ]; then
  printf 'D128/F executable/import/hash/numeric preflight PASS free=%s\n' "$FREE_BYTES"
  exit 0
fi
test "$#" = 0
STAGE=source1747-extract
SOURCE_ROOT="$TMP_ROOT/source1747"
INPUTS="$TMP_ROOT/tiny-inputs"
WHEEL_BUILD="$TMP_ROOT/tiny-wheel-build"
WHEELHOUSE="$TMP_ROOT/tiny-wheelhouse"
BOOTSTRAP="$TMP_ROOT/bootstrap-input"
AGENT_FIXTURE="$TMP_ROOT/tiny-agent-fixture"
RUNTIME_FIXTURE="$TMP_ROOT/tiny-runtime-fixture"
ORCH_ROOT="$TMP_ROOT/tiny-orch"
VENUE="$TMP_ROOT/tiny-venue.json"
PARENT_WORK="$TMP_ROOT/tiny-parent-work"
CANDIDATE_WORK="$TMP_ROOT/tiny-candidate-work"
RESULT="$TMP_ROOT/tiny-e2e-result.json"

test ! -e "$SOURCE_ROOT" -a ! -e "$INPUTS" -a ! -e "$WHEEL_BUILD" -a ! -e "$WHEELHOUSE"
test ! -e "$AGENT_FIXTURE" -a ! -e "$RUNTIME_FIXTURE" -a ! -e "$ORCH_ROOT"
test ! -e "$VENUE" -a ! -e "$PARENT_WORK" -a ! -e "$CANDIDATE_WORK" -a ! -e "$RESULT"
test "$(git -C "$PWD" cat-file -t "$SOURCE_COMMIT")" = commit
mkdir -p "$SOURCE_ROOT"
git -C "$PWD" archive "$SOURCE_COMMIT" ops-child-custody/tests/e2e_inventory.py ops-child-custody/e2e-fixtures/tiny | tar -x -C "$SOURCE_ROOT"
RUNNER="$SOURCE_ROOT/ops-child-custody/tests/e2e_inventory.py"
MANIFEST="$SOURCE_ROOT/ops-child-custody/e2e-fixtures/tiny/manifest.json"
test "$(sha256sum "$RUNNER" | awk '{print $1}')" = "$SOURCE_RUNNER_SHA"
test "$(sha256sum "$MANIFEST" | awk '{print $1}')" = "$SOURCE_MANIFEST_SHA"
test "$(sha256sum "$PWD/ops-child-custody/make-child-venv" | awk '{print $1}')" = "$CANDIDATE_MAKER_SHA"

STAGE=write-inputs
PYTHONDONTWRITEBYTECODE=1 "$RUNNER_PYTHON" "$RUNNER" --write-inputs "$INPUTS"
STAGE=build-wheels
PYTHONDONTWRITEBYTECODE=1 "$RUNNER_PYTHON" "$RUNNER" --build-wheels "$WHEEL_BUILD" --build-python "$BUILD_PYTHON"
STAGE=offline-wheelhouse
mkdir -p "$WHEELHOUSE" "$BOOTSTRAP"
tar -xzf "$ARTIFACT" -C "$BOOTSTRAP"
BOOTSTRAP_WHEELHOUSE="$BOOTSTRAP/timeline-bootstrap-wheel-input-0932/wheelhouse"
cp "$BOOTSTRAP_WHEELHOUSE/pip-26.2.1-py3-none-any.whl" "$WHEELHOUSE/"
cp "$BOOTSTRAP_WHEELHOUSE/setuptools-80.9.0-py3-none-any.whl" "$WHEELHOUSE/"
cp "$BOOTSTRAP_WHEELHOUSE/wheel-0.46.3-py3-none-any.whl" "$WHEELHOUSE/"
cp "$WHEEL_BUILD/custody_b-0.1.0-py3-none-any.whl" "$WHEELHOUSE/"
cp "$WHEEL_BUILD/custody_a-0.1.0-py3-none-any.whl" "$WHEELHOUSE/"
test "$(sha256sum "$WHEELHOUSE/pip-26.2.1-py3-none-any.whl" | awk '{print $1}')" = 71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e
test "$(sha256sum "$WHEELHOUSE/setuptools-80.9.0-py3-none-any.whl" | awk '{print $1}')" = 062d34222ad13e0cc312a4c02d73f059e86a4acbfbdea8f8f76b28c99f306922
test "$(sha256sum "$WHEELHOUSE/wheel-0.46.3-py3-none-any.whl" | awk '{print $1}')" = 4b399d56c9d9338230118d705d9737a2a468ccca63d5e813e2a4fc7815d8bc4d
test "$(sha256sum "$WHEELHOUSE/custody_b-0.1.0-py3-none-any.whl" | awk '{print $1}')" = 1e3759d3710d3d92e31f10df3abe7ee8003532a19c1686fa5c2fbc75c407531e
test "$(sha256sum "$WHEELHOUSE/custody_a-0.1.0-py3-none-any.whl" | awk '{print $1}')" = 7997736a950ea3c6a4fbe32ca5cde306ced6610cbb0a4baa392cb402c59a3a14

fixture_git() {
  GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$1" -c user.name='Timeline fixture' -c user.email='timeline-fixture@example.invalid' -c credential.helper= "${@:2}"
}

fixture_commit() {
  local checkout="$1"
  shift
  fixture_git "$checkout" init --quiet
  fixture_git "$checkout" add -- "$@"
  fixture_git "$checkout" commit --quiet -m 'test: publish tiny fixture'
}

STAGE=fixture-git
mkdir -p "$AGENT_FIXTURE" "$RUNTIME_FIXTURE"
cp -a "$INPUTS/agent/." "$AGENT_FIXTURE/"
cp -a "$INPUTS/runtime/." "$RUNTIME_FIXTURE/"
fixture_commit "$AGENT_FIXTURE" LICENSE astrid astrid_runtime_client pyproject.toml requirements/proof.lock
fixture_commit "$RUNTIME_FIXTURE" LICENSE astrid_runtime packages/python/astrid_runtime_client pyproject.toml runtime_protocol
test "$(fixture_git "$AGENT_FIXTURE" status --porcelain --untracked-files=all)" = ''
test "$(fixture_git "$RUNTIME_FIXTURE" status --porcelain --untracked-files=all)" = ''

FREE_BYTES=$(numeric_avail "$ROOT")
test "$FREE_BYTES" -ge "$MIN_RESERVE"
STAGE=prepare-venue
PYTHONDONTWRITEBYTECODE=1 "$RUNNER_PYTHON" "$RUNNER" \
  --prepare-venue "$VENUE" --helper "$HELPER" --orch-root "$ORCH_ROOT" \
  --python "$CHILD_PYTHON" --wheelhouse "$WHEELHOUSE" \
  --agent "$AGENT_FIXTURE" --runtime "$RUNTIME_FIXTURE" \
  --parent-work "$PARENT_WORK" --candidate-work "$CANDIDATE_WORK"
FREE_BYTES=$(numeric_avail "$ROOT")
test "$FREE_BYTES" -ge "$MIN_RESERVE"
test "$FREE_BYTES" -gt "$STOP_LINE"

STAGE=whole-maker
PYTHONDONTWRITEBYTECODE=1 "$RUNNER_PYTHON" "$RUNNER" \
  --venue-manifest "$VENUE" --result "$RESULT"
test -s "$RESULT"
cp "$RESULT" "$EVIDENCE/e2e-result.json"

STAGE=complete
printf 'D128/F whole-maker E2E PASS; see e2e-result.json\n'
