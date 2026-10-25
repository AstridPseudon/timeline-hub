#!/usr/bin/env bash
set -euo pipefail

# D128/F receiving wrapper.  The test service snapshots this tree and supplies
# D66_OUTPUT_DIR; all disposable fixture state stays below this run's TMPDIR.
SOURCE=$PWD
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
OUTPUT=${D66_OUTPUT_DIR:-$SOURCE/evidence}
PY=/home/user/work/venv-agent/bin/python
CHILD_PY=/usr/bin/python3.13
HELPER=$ORCH/bin/bench_store.py
BOOTSTRAP=$ORCH/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz
RUNNER=$SOURCE/ops-child-custody/tests/e2e_inventory.py
MANIFEST=$SOURCE/ops-child-custody/e2e-fixtures/tiny/manifest.json
MAKER=$SOURCE/ops-child-custody/make-child-venv

EXPECTED_HEAD=60753548ebc8e69f3c84fbb28fa2e09b1ca78316
EXPECTED_RUNNER=1498a1597c058f92176a0d447b372b4791e6af345c479445b9027e0521d75085
EXPECTED_SUPPORT=e85b42ac7ffff730166443ed7d081a1a68062b828af3aa5d8e0dd9352afb6581
EXPECTED_MANIFEST=cee9435bcd6d522ddb814ef0e0679790b929f73a619dc0dc28be301b55cb68e8
EXPECTED_MAKER=c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e
EXPECTED_PARENT=0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39
EXPECTED_HELPER=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2
EXPECTED_BOOTSTRAP=443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548
RESERVE=5905580032
STOP_LINE=4000000000

mkdir -p "$OUTPUT"
printf 'stage=bind start\n' > "$OUTPUT/progress.md"

hash_file() {
  sha256sum "$1" | awk '{print $1}'
}

test "$(hash_file "$RUNNER")" = "$EXPECTED_RUNNER"
test "$(hash_file "$SOURCE/ops-child-custody/tests/support.py")" = "$EXPECTED_SUPPORT"
test "$(hash_file "$MANIFEST")" = "$EXPECTED_MANIFEST"
test "$(hash_file "$MAKER")" = "$EXPECTED_MAKER"
test "$(hash_file "$SOURCE/ops-child-custody/e2e-fixtures/tiny/makers/parent-0857/make-child-venv")" = "$EXPECTED_PARENT"
test "$(hash_file "$HELPER")" = "$EXPECTED_HELPER"
test "$(hash_file "$BOOTSTRAP")" = "$EXPECTED_BOOTSTRAP"
test -x "$PY" -a -x "$CHILD_PY" -a -x "$HELPER" -a -x "$MAKER"
SOURCE_HEAD=$(git -C "$SOURCE" rev-parse HEAD)
if [ "$SOURCE_HEAD" != "$EXPECTED_HEAD" ]; then
  test "$(git -C "$SOURCE" rev-parse HEAD^)" = "$EXPECTED_HEAD"
fi

FREE_KIB=$(df -Pk "$SOURCE" | awk 'NR == 2 && $4 ~ /^[0-9]+$/ {print $4}')
test -n "$FREE_KIB"
FREE_BYTES=$((FREE_KIB * 1024))
test "$FREE_BYTES" -ge "$RESERVE"
test "$FREE_BYTES" -ge "$STOP_LINE"
printf '{\n  "source_head": "%s",\n  "runner_sha256": "%s",\n  "support_sha256": "%s",\n  "manifest_sha256": "%s",\n  "candidate_maker_sha256": "%s",\n  "parent_maker_sha256": "%s",\n  "store_helper_sha256": "%s",\n  "bootstrap_artifact_sha256": "%s"\n}\n' \
  "$EXPECTED_HEAD" "$EXPECTED_RUNNER" "$EXPECTED_SUPPORT" "$EXPECTED_MANIFEST" "$EXPECTED_MAKER" "$EXPECTED_PARENT" "$EXPECTED_HELPER" "$EXPECTED_BOOTSTRAP" \
  > "$OUTPUT/source-manifest.json"
printf '{\n  "dispatch_admission_free_bytes": %s,\n  "normal_reserve_bytes": %s,\n  "stop_line_bytes": %s,\n  "source_review": "PASS_SOURCE_UNIT",\n  "body_started": false\n}\n' "$FREE_BYTES" "$RESERVE" "$STOP_LINE" > "$OUTPUT/admission.json"
printf 'stage=bind complete free_bytes=%s\n' "$FREE_BYTES" >> "$OUTPUT/progress.md"

# Own a fresh per-service TMPDIR.  No prior venue or Store is reused.
RUN_TMP=$(mktemp -d "${TMPDIR:-/tmp}/timeline-portable-receive-XXXXXX")
export TMPDIR=$RUN_TMP
INPUTS=$TMPDIR/tiny-inputs
WHEEL_BUILD=$TMPDIR/tiny-wheel-build
WHEELHOUSE=$TMPDIR/tiny-wheelhouse
BOOTSTRAP_INPUT=$TMPDIR/bootstrap-input
AGENT=$TMPDIR/tiny-agent
RUNTIME=$TMPDIR/tiny-runtime
ORCH_ROOT=$TMPDIR/tiny-orch
PARENT_WORK=$TMPDIR/tiny-parent-work
CANDIDATE_WORK=$TMPDIR/tiny-candidate-work
VENUE=$TMPDIR/tiny-venue.json
CHECK=$TMPDIR/check-only.json
RESULT=$TMPDIR/tiny-e2e-result.json

printf 'stage=write-inputs start\n' >> "$OUTPUT/progress.md"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --write-inputs "$INPUTS"
printf 'stage=write-inputs complete\n' >> "$OUTPUT/progress.md"

printf 'stage=build-wheels start\n' >> "$OUTPUT/progress.md"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --build-wheels "$WHEEL_BUILD" --build-python "$PY" > "$TMPDIR/wheel-build.json"
printf 'stage=build-wheels complete\n' >> "$OUTPUT/progress.md"

mkdir -p "$WHEELHOUSE" "$BOOTSTRAP_INPUT"
tar -xzf "$BOOTSTRAP" -C "$BOOTSTRAP_INPUT"
cp "$BOOTSTRAP_INPUT/timeline-bootstrap-wheel-input-0932/wheelhouse/pip-26.2.1-py3-none-any.whl" "$WHEELHOUSE/"
cp "$BOOTSTRAP_INPUT/timeline-bootstrap-wheel-input-0932/wheelhouse/setuptools-80.9.0-py3-none-any.whl" "$WHEELHOUSE/"
cp "$BOOTSTRAP_INPUT/timeline-bootstrap-wheel-input-0932/wheelhouse/wheel-0.46.3-py3-none-any.whl" "$WHEELHOUSE/"
cp "$WHEEL_BUILD/custody_b-0.1.0-py3-none-any.whl" "$WHEELHOUSE/"
cp "$WHEEL_BUILD/custody_a-0.1.0-py3-none-any.whl" "$WHEELHOUSE/"

# These are the normal receiving-service fixture commits; no production Git
# repository, branch, ref, or source checkout is touched.
fixture_git() {
  GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$1" -c user.name='Timeline fixture' -c user.email='timeline-fixture@example.invalid' -c credential.helper= "${@:2}"
}
fixture_commit() {
  local checkout=$1
  shift
  fixture_git "$checkout" init --quiet
  fixture_git "$checkout" add -- "$@"
  fixture_git "$checkout" commit --quiet -m 'test: publish tiny fixture'
}
mkdir -p "$AGENT" "$RUNTIME"
cp -a "$INPUTS/agent/." "$AGENT/"
cp -a "$INPUTS/runtime/." "$RUNTIME/"
fixture_commit "$AGENT" LICENSE astrid astrid_runtime_client pyproject.toml requirements/proof.lock
fixture_commit "$RUNTIME" LICENSE astrid_runtime packages/python/astrid_runtime_client pyproject.toml runtime_protocol
test -z "$(fixture_git "$AGENT" status --porcelain --untracked-files=all)"
test -z "$(fixture_git "$RUNTIME" status --porcelain --untracked-files=all)"
printf '{\n  "agent_fixture_commit": "%s",\n  "runtime_fixture_commit": "%s",\n  "wheelhouse_pins": "manifest-authenticated",\n  "git_mutation_scope": "two-private-tiny-source-carriers"\n}\n' \
  "$(fixture_git "$AGENT" rev-parse HEAD)" "$(fixture_git "$RUNTIME" rev-parse HEAD)" > "$OUTPUT/inputs.json"

printf 'stage=check-only start\n' >> "$OUTPUT/progress.md"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --check-only \
  --helper "$HELPER" --bootstrap-artifact "$BOOTSTRAP" \
  --runner-python "$PY" --build-python "$PY" --python "$CHILD_PY" \
  --wheelhouse "$WHEELHOUSE" --agent "$AGENT" --runtime "$RUNTIME" \
  --orch-root "$ORCH_ROOT" --parent-work "$PARENT_WORK" \
  --candidate-work "$CANDIDATE_WORK" --result "$CHECK" > "$TMPDIR/check-only.stdout"
cp "$CHECK" "$OUTPUT/check-only.json"
printf 'stage=check-only PASS exit=0\n' >> "$OUTPUT/progress.md"

printf 'stage=prepare-venue start\n' >> "$OUTPUT/progress.md"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --prepare-venue "$VENUE" \
  --helper "$HELPER" --bootstrap-artifact "$BOOTSTRAP" \
  --runner-python "$PY" --build-python "$PY" --python "$CHILD_PY" \
  --wheelhouse "$WHEELHOUSE" --agent "$AGENT" --runtime "$RUNTIME" \
  --orch-root "$ORCH_ROOT" --parent-work "$PARENT_WORK" --candidate-work "$CANDIDATE_WORK"
printf 'stage=prepare-venue complete exit=0\n' >> "$OUTPUT/progress.md"

FREE_KIB=$(df -Pk "$SOURCE" | awk 'NR == 2 && $4 ~ /^[0-9]+$/ {print $4}')
FREE_BYTES=$((FREE_KIB * 1024))
test "$FREE_BYTES" -ge "$STOP_LINE"
printf 'stage=whole-maker start free_bytes=%s\n' "$FREE_BYTES" >> "$OUTPUT/progress.md"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --venue-manifest "$VENUE" --result "$RESULT"
cp "$RESULT" "$OUTPUT/e2e-result.json"

# Publish only safe stage/result fields to the service log.  The raw result
# remains in the service-private evidence directory.
"$PY" -B -I - "$RESULT" <<'PY'
import json
import sys

result = json.load(open(sys.argv[1]))
safe = {key: result.get(key) for key in (
    'whole_make_e2e', 'parent_red', 'candidate_green', 'adversarial_checks',
    'store_initialized_by_worker', 'admission_changed',
)}
safe['command_exits'] = [item.get('exit_code') for item in result.get('commands', [])]
print('D128/F whole-maker result=' + json.dumps(safe, sort_keys=True, separators=(',', ':')))
PY
printf 'stage=whole-maker complete exit=0\n' >> "$OUTPUT/progress.md"
