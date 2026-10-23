#!/bin/bash
# make-child-venv NAME AGENT_SHA [BASE_SUITE RUNTIME] — dispatcher child venv.
# RUNTIME remains the optional Remotion graph used for suite substitution.
set -u -o pipefail
O=${CHILD_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
A=${CHILD_VENV_AGENT_CHECKOUT:-/home/user/work/agent}
R=${CHILD_VENV_RUNTIME_CHECKOUT:-/home/user/work/runtime}
W=${CHILD_VENV_WORK_ROOT:-/home/user/work}
PYTHON=${CHILD_VENV_PYTHON:-python3.13}
TIMEOUT_BIN=${CHILD_VENV_TIMEOUT_BIN:-timeout}
LOCAL_TIMEOUT_SECONDS=${CHILD_VENV_LOCAL_TIMEOUT_SECONDS:-600}
PIP_TIMEOUT_SECONDS=${CHILD_VENV_PIP_TIMEOUT_SECONDS:-600}
BUILD_TIMEOUT_SECONDS=${CHILD_VENV_BUILD_TIMEOUT_SECONDS:-3600}
KILL_AFTER_SECONDS=${CHILD_VENV_KILL_AFTER_SECONDS:-30}
PIP_NETWORK_TIMEOUT_SECONDS=${CHILD_VENV_PIP_NETWORK_TIMEOUT_SECONDS:-30}
PIP_RETRIES=${CHILD_VENV_PIP_RETRIES:-2}
REQUIREMENTS_PATH=${CHILD_VENV_REQUIREMENTS_PATH:-requirements/proof.lock}
progress() { printf '%s child-venv %s\n' "$(date -u +%FT%TZ)" "$*"; }
N=${1:-}; S=${2:-}; BS=${3:-}; RT=${4:-}
case "$N" in venv-agent-child-[a-z0-9-]*) ;; *) echo 'REFUSED: name must be venv-agent-child-<suffix>'; exit 2;; esac
[ -n "$S" ] || { echo 'REFUSED: agent commit is required'; exit 2; }
D=$W/$N
[ -e "$D" ] || [ -L "$D" ] && { echo "exists: $D (child venvs are immutable; pick a new name)"; exit 0; }

missing=()
require_command() { command -v "$1" >/dev/null 2>&1 || missing+=("command:$1"); }
for c in git tar mktemp sha256sum timeout grep sed find chmod mv df awk; do require_command "$c"; done
for p in "$W" "$A" "$R" "$O/tests"; do [ -d "$p" ] || missing+=("directory:$p"); done
[ -w "$O/tests" ] || missing+=("writable:$O/tests")
check() { "$@" >/dev/null 2>&1 || missing+=("$*"); }
check git -C "$A" rev-parse --is-inside-work-tree
check git -C "$R" rev-parse --is-inside-work-tree
check git -C "$A" cat-file -e "$S^{commit}"
check git -C "$R" cat-file -e 'HEAD^{commit}'
check git -C "$A" cat-file -e "$S:$REQUIREMENTS_PATH"
check git -C "$A" cat-file -e "$S:pyproject.toml"
check git -C "$R" cat-file -e 'HEAD:pyproject.toml'
check "$PYTHON" -c 'import sys; assert sys.version_info >= (3, 11)'
check "$PYTHON" -m venv --help
check df -P -B1 "$W"
if command -v "$PYTHON" >/dev/null 2>&1; then PYTHON_ACTUAL=$($PYTHON --version 2>&1 || true); else PYTHON_ACTUAL=unavailable; fi
RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null || true)
if git -C "$A" cat-file -e "$S:$REQUIREMENTS_PATH" >/dev/null 2>&1; then LOCK_SHA=$(git -C "$A" show "$S:$REQUIREMENTS_PATH" | sha256sum | cut -d' ' -f1); else LOCK_SHA=unavailable; fi
FREE_BYTES=$(df -P -B1 "$W" 2>/dev/null | awk 'NR == 2 { print $4 }')
if [ "${#missing[@]}" -ne 0 ]; then
  printf '%s child-venv PREFLIGHT FAILED name=%s agent=%s requirements=%s\n' "$(date -u +%FT%TZ)" "$N" "$S" "$REQUIREMENTS_PATH" >&2
  printf 'inventory=python:%s runtime_sha:%s requirements_lock_sha256:%s free_bytes:%s\n' "$PYTHON_ACTUAL" "$RUNTIME_SHA" "$LOCK_SHA" "$FREE_BYTES" >&2
  printf 'missing_prerequisite=%s\n' "${missing[@]}" >&2
  exit 2
fi

if [ "${CHILD_VENV_BUILD_INNER:-0}" != 1 ]; then
  export CHILD_VENV_BUILD_INNER=1
  "$TIMEOUT_BIN" --kill-after="$KILL_AFTER_SECONDS" "$BUILD_TIMEOUT_SECONDS" "$0" "$@"
  exit $?
fi
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)-$$
T=$D.partial.$RUN_ID; SRC=$(mktemp -d "$W/.child-venv-source-$N-$RUN_ID.XXXXXX")
REPORT_DIR=$O/tests/provision; REPORT_TMP=$REPORT_DIR/.${N}.freeze.$RUN_ID; F=$REPORT_DIR/$N.txt
failure() { rc=$1; stage=$2; [ -d "$T" ] && printf 'status=failed\nstage=%s\nrc=%s\nagent_sha=%s\nruntime_sha=%s\npartial=%s\n' "$stage" "$rc" "$S" "$RUNTIME_SHA" "$T" > "$T/.provision-failure"; printf '%s child-venv FAILED stage=%s rc=%s name=%s partial=%s\n' "$(date -u +%FT%TZ)" "$stage" "$rc" "$N" "$T" >&2; exit "$rc"; }
stage() { name=$1; shift; progress "stage=$name start"; CHILD_VENV_STAGE=$name "$TIMEOUT_BIN" --kill-after="$KILL_AFTER_SECONDS" "$LOCAL_TIMEOUT_SECONDS" "$@" || failure $? "$name"; progress "stage=$name complete"; }
progress "source agent=$S runtime=$RUNTIME_SHA requirements=$REQUIREMENTS_PATH lock_sha256=$LOCK_SHA"
stage venv "$PYTHON" -m venv "$T"; P=$T/bin/python
PIP_ARGS=(--no-cache-dir --disable-pip-version-check --progress-bar off --retries "$PIP_RETRIES" --timeout "$PIP_NETWORK_TIMEOUT_SECONDS")
stage bootstrap-pip "$P" -m pip install "${PIP_ARGS[@]}" -q pip==26.2.1 setuptools==80.9.0 wheel==0.46.3
stage requirements mkdir -p "$REPORT_DIR"; REQ=$T/.provision-requirements.txt
stage filter-requirements bash -c 'set -o pipefail; git -C "$1" show "$2:$3" | grep -v -e "^astrid @" -e "^pip==" -e "^setuptools==" -e "^wheel==" > "$4"' _ "$A" "$S" "$REQUIREMENTS_PATH" "$REQ"
stage pinned-requirements "$P" -m pip install "${PIP_ARGS[@]}" -q --no-deps -r "$REQ"
AGENT_SRC=$SRC/agent; RUNTIME_SRC=$SRC/runtime; stage source-directories mkdir -p "$AGENT_SRC" "$RUNTIME_SRC"
stage archive-agent bash -c 'set -o pipefail; git -C "$1" archive "$2" | tar -x -C "$3"' _ "$A" "$S" "$AGENT_SRC"
stage archive-runtime bash -c 'set -o pipefail; git -C "$1" archive "$2" | tar -x -C "$3"' _ "$R" "$RUNTIME_SHA" "$RUNTIME_SRC"
stage install-agent "$P" -m pip install "${PIP_ARGS[@]}" -q --no-deps --no-build-isolation "$AGENT_SRC"
stage install-runtime "$P" -m pip install "${PIP_ARGS[@]}" -q --no-deps --no-build-isolation "$RUNTIME_SRC"
printf '%s\n' "$S" > "$T/.astrid-source-commit"; printf '%s\n' "$RUNTIME_SHA" > "$T/.astrid-runtime-source-commit"
stage import-provenance bash -c 'set -e; "$1" -I -c '\''import importlib.util, pathlib
for name in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"):
 spec=importlib.util.find_spec(name); assert spec is not None and spec.origin, name
 origin=pathlib.Path(spec.origin).resolve(); assert "site-packages" in origin.parts, (name, origin); print(f"{name}={origin}")'\'' > "$2"' _ "$P" "$T/.astrid-import-origins"
stage runtime-cli bash -c 'set -e; "$1" --help >/dev/null; "$2" --help >/dev/null; "$3" -I -m astrid_runtime --help >/dev/null' _ "$T/bin/astrid-runtime" "$T/bin/astrid-runtime-protocol" "$P"
stage freeze bash -c 'set -e; { printf "status=passed\nagent_sha=%s\nruntime_sha=%s\nrequirements_path=%s\nrequirements_lock_sha256=%s\n" "$4" "$5" "$6" "$7"; printf "installed_import_origins:\n"; cat "$3"; printf "pip_freeze:\n"; "$1" -I -m pip freeze --all; } > "$2"' _ "$P" "$REPORT_TMP" "$T/.astrid-import-origins" "$S" "$RUNTIME_SHA" "$REQUIREMENTS_PATH" "$LOCK_SHA"
stage freeze-identity bash -c 'grep -q "^status=passed$" "$1" && grep -q "^astrid==" "$1" && grep -q "^astrid-runtime==" "$1"' _ "$REPORT_TMP"
stage shebang-relocation bash -c 'set -e; while IFS= read -r file; do sed -i "s#$1#$2#g" "$file"; done < <(grep -rl -- "$1" "$3/bin" 2>/dev/null || true)' _ "$T" "$D" "$T"; stage readonly-final chmod -R a-w "$T"
[ -e "$D" ] || [ -L "$D" ] && failure 1 immutable-publish-race
stage publish mv -T "$T" "$D"; stage provision-report mv -T "$REPORT_TMP" "$F"
if [ -n "$BS" ] && [ -n "$RT" ] && ! grep -q "^agent $N-full " "$O/tests/suites.conf"; then L=$(grep "^agent $BS " "$O/tests/suites.conf" || true); [ -z "$L" ] || echo "$L" | sed "s#^agent $BS #agent $N-full #; s#venv-agent-child-[^ /]*#$N#g; s#agent-remotion-[^ /]*#$RT#g" >> "$O/tests/suites.conf"; fi
echo "created $D (astrid from ${S:0:12}, runtime from ${RUNTIME_SHA:0:12}, read-only)"
