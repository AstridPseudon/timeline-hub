#!/bin/bash
# make-child-venv NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH] — dispatcher child venv.
# The fourth argument remains the optional Remotion graph used for suite substitution.
set -u -o pipefail

O=${CHILD_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
A=${CHILD_VENV_AGENT_CHECKOUT:-/home/user/work/agent}
R=${CHILD_VENV_RUNTIME_CHECKOUT:-/home/user/work/runtime}
W=${CHILD_VENV_WORK_ROOT:-/home/user/work}
PYTHON=${CHILD_VENV_PYTHON:-python3.13}
TIMEOUT_BIN=${CHILD_VENV_TIMEOUT_BIN:-timeout}

PIP_TIMEOUT_SECONDS=${CHILD_VENV_PIP_TIMEOUT_SECONDS:-600}
LOCAL_TIMEOUT_SECONDS=${CHILD_VENV_LOCAL_TIMEOUT_SECONDS:-600}
FREEZE_TIMEOUT_SECONDS=${CHILD_VENV_FREEZE_TIMEOUT_SECONDS:-120}
BUILD_TIMEOUT_SECONDS=${CHILD_VENV_BUILD_TIMEOUT_SECONDS:-3600}
KILL_AFTER_SECONDS=${CHILD_VENV_KILL_AFTER_SECONDS:-30}
PIP_NETWORK_TIMEOUT_SECONDS=${CHILD_VENV_PIP_NETWORK_TIMEOUT_SECONDS:-30}
PIP_RETRIES=${CHILD_VENV_PIP_RETRIES:-2}
REQUIREMENTS_PATH=${CHILD_VENV_REQUIREMENTS_PATH:-requirements/proof.lock}

case "$O:$A:$R:$W" in
  /*:/*:/*:/*) ;;
  *) echo 'REFUSED: child venv roots and source checkouts must be absolute' >&2; exit 2;;
esac

progress() { printf '%s child-venv %s\n' "$(date -u +%FT%TZ)" "$*"; }

N=${1:-}
S=${2:-}
BS=${3:-}
RT=${4:-}
case "$N" in
  venv-agent-child-[a-z0-9-]*) ;;
  *) echo "REFUSED: name must be venv-agent-child-<suffix>"; exit 2 ;;
esac
[[ "$N" =~ ^venv-agent-child-[a-z0-9-]+$ ]] || { echo 'REFUSED: invalid child name'; exit 2; }
[[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: exact Agent commit required'; exit 2; }
[ "$#" -le 4 ] || { echo 'REFUSED: invalid call shape'; exit 2; }

# Authenticate source state before either existing-target lookup or build setup.
source_state() {
  local checkout=$1 wanted=$2 actual status
  actual=$(git -C "$checkout" rev-parse --verify HEAD^{commit} 2>/dev/null) || return 1
  [ "$actual" = "$wanted" ] || return 1
  status=$(git -C "$checkout" status --porcelain --untracked-files=all 2>/dev/null) || return 1
  [ -z "$status" ]
}
source_state "$A" "$S" || { echo 'REFUSED: Agent checkout/commit is unavailable, mismatched or dirty'; exit 2; }
RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null) || { echo 'REFUSED: Runtime checkout unavailable'; exit 2; }
source_state "$R" "$RUNTIME_SHA" || { echo 'REFUSED: Runtime checkout is dirty'; exit 2; }

D=$W/$N
if [ -e "$D" ] || [ -L "$D" ]; then
  # The same verifier used by the requester must authenticate this exact target.
  # This runs before timeout, temporary sources, reports or any provisioning.
  SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
  REQUESTER=$SCRIPT_DIR/request-child-venv
  [ -f "$REQUESTER" ] || REQUESTER=$SCRIPT_DIR/request-child-venv.sh
  CHILD_VENV_REUSE_ONLY=1 CHILD_VENV_REUSE_TARGET="$D" "$REQUESTER" "$@"
  exit "$?"
fi

# Run the body under one bounded budget. The dispatcher invokes this script
# inline, so a timed-out child must return to its FIFO loop with a non-zero
# identity rather than being reported as an existing/successful environment.
if [ "${CHILD_VENV_BUILD_INNER:-0}" != 1 ]; then
  export CHILD_VENV_BUILD_INNER=1
  # GNU timeout creates a private process group by default. Keep this
  # background process-group mode so a timed-out descendant (including one holding
  # the dispatcher's inherited stdout/FIFO) receives the same bounded kill grace.
  "$TIMEOUT_BIN" --kill-after="$KILL_AFTER_SECONDS" "$BUILD_TIMEOUT_SECONDS" "$0" "$@"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    partial=$(find "$W" -maxdepth 1 -type d -name "$N.partial.*" -print -quit 2>/dev/null || true)
    printf '%s child-venv FAILED stage=overall-build-budget rc=%s name=%s agent=%s partial=%s\n' \
      "$(date -u +%FT%TZ)" "$rc" "$N" "$S" "${partial:-none}" >&2
  fi
  exit "$rc"
fi

RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)-$$
T=$D.partial.$RUN_ID
SRC=$(mktemp -d "$W/.child-venv-source-$N-$RUN_ID.XXXXXX")
REPORT_DIR=$O/tests/provision
REPORT_TMP=$REPORT_DIR/.${N}.freeze.$RUN_ID
F=$REPORT_DIR/$N.txt

failure() {
  rc=$1
  stage=$2
  if [ -d "$T" ]; then
    printf 'status=failed\nstage=%s\nrc=%s\nagent_sha=%s\nruntime_sha=%s\npartial=%s\nsource=%s\n' \
      "$stage" "$rc" "$S" "${RUNTIME_SHA:-unknown}" "$T" "$SRC" > "$T/.provision-failure"
  fi
  printf '%s child-venv FAILED stage=%s rc=%s name=%s agent=%s runtime=%s partial=%s source=%s\n' \
    "$(date -u +%FT%TZ)" "$stage" "$rc" "$N" "$S" "${RUNTIME_SHA:-unknown}" "$T" "$SRC" >&2
  exit "$rc"
}

run_stage() {
  stage=$1
  budget=$2
  shift 2
  CURRENT_STAGE=$stage
  progress "stage=$stage start budget=${budget}s"
  # Do not use foreground mode: it deliberately leaves descendants outside the
  # timeout's process-group termination and can wedge the inline dispatcher.
  CHILD_VENV_STAGE=$stage "$TIMEOUT_BIN" --kill-after="$KILL_AFTER_SECONDS" "$budget" "$@"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    failure "$rc" "$stage"
  fi
  progress "stage=$stage complete"
}

missing=()
require_command() { command -v "$1" >/dev/null 2>&1 || missing+=("command:$1"); }
for command_name in git tar mktemp sha256sum cut grep sed find chmod mv df awk; do
  require_command "$command_name"
done
for path in "$W" "$A" "$R" "$O/tests"; do
  [ -d "$path" ] || missing+=("directory:$path")
done
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
if command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON_ACTUAL=$($PYTHON --version 2>&1 || true)
else
  PYTHON_ACTUAL=unavailable
fi
RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null || true)
if git -C "$A" cat-file -e "$S:$REQUIREMENTS_PATH" >/dev/null 2>&1; then
  LOCK_SHA=$(git -C "$A" show "$S:$REQUIREMENTS_PATH" | sha256sum | cut -d' ' -f1)
else
  LOCK_SHA=unavailable
fi
FREE_BYTES=$(df -P -B1 "$W" 2>/dev/null | awk 'NR == 2 { print $4 }')
if [ "${#missing[@]}" -ne 0 ]; then
  printf '%s child-venv PREFLIGHT FAILED name=%s agent=%s requirements=%s\n' \
    "$(date -u +%FT%TZ)" "$N" "$S" "$REQUIREMENTS_PATH" >&2
  printf 'inventory=python:%s runtime_sha:%s requirements_lock_sha256:%s free_bytes:%s\n' \
    "$PYTHON_ACTUAL" "$RUNTIME_SHA" "$LOCK_SHA" "$FREE_BYTES" >&2
  printf 'missing_prerequisite=%s\n' "${missing[@]}" >&2
  failure 2 preflight
fi
progress "source agent=$S runtime=$RUNTIME_SHA requirements=$REQUIREMENTS_PATH lock_sha256=$LOCK_SHA"

# Keep backend custody: the D21b full-bench/client-only key decision is pending.
CLIENT_IDENTITY=$(git -C "$R" ls-tree -r --name-only "$RUNTIME_SHA" packages/python/astrid_runtime_client/ | while IFS= read -r path; do
  [ -n "$path" ] || continue
  printf '%s=' "$path"
  git -C "$R" show "$RUNTIME_SHA:$path" | sha256sum | cut -d' ' -f1
done)
[ -n "$CLIENT_IDENTITY" ] || failure 2 runtime-client-identity

run_stage venv "$LOCAL_TIMEOUT_SECONDS" "$PYTHON" -m venv --copies "$T"
P=$T/bin/python
PIP_ARGS=(--no-cache-dir --disable-pip-version-check --progress-bar off --retries "$PIP_RETRIES" --timeout "$PIP_NETWORK_TIMEOUT_SECONDS")
run_stage bootstrap-pip "$PIP_TIMEOUT_SECONDS" "$P" -m pip install "${PIP_ARGS[@]}" -q \
  'pip==26.2.1' 'setuptools==80.9.0' 'wheel==0.46.3'

run_stage requirements "$LOCAL_TIMEOUT_SECONDS" mkdir -p "$REPORT_DIR"
REQ=$T/.provision-requirements.txt
run_stage filter-requirements "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -o pipefail; git -C "$1" show "$2:$3" | grep -v -e "^astrid @" -e "^pip==" -e "^setuptools==" -e "^wheel==" > "$4"' \
  _ "$A" "$S" "$REQUIREMENTS_PATH" "$REQ"
run_stage pinned-requirements "$PIP_TIMEOUT_SECONDS" "$P" -m pip install "${PIP_ARGS[@]}" -q --no-deps -r "$REQ"

AGENT_SRC=$SRC/agent
RUNTIME_SRC=$SRC/runtime
run_stage source-directories "$LOCAL_TIMEOUT_SECONDS" mkdir -p "$AGENT_SRC" "$RUNTIME_SRC"
run_stage archive-agent "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -o pipefail; git -C "$1" archive "$2" | tar -x -C "$3"' \
  _ "$A" "$S" "$AGENT_SRC"
run_stage archive-runtime "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -o pipefail; git -C "$1" archive "$2" | tar -x -C "$3"' \
  _ "$R" "$RUNTIME_SHA" "$RUNTIME_SRC"

run_stage install-agent "$PIP_TIMEOUT_SECONDS" "$P" -m pip install "${PIP_ARGS[@]}" -q --no-deps --no-build-isolation "$AGENT_SRC"
run_stage install-runtime "$PIP_TIMEOUT_SECONDS" "$P" -m pip install "${PIP_ARGS[@]}" -q --no-deps --no-build-isolation "$RUNTIME_SRC"
printf '%s\n' "$S" > "$T/.astrid-source-commit"
printf '%s\n' "$RUNTIME_SHA" > "$T/.astrid-runtime-source-commit"
printf '%s\n' "$CLIENT_IDENTITY" > "$T/.astrid-runtime-client-identity"

PROVENANCE_SCRIPT='import importlib.util, pathlib
names = ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client")
for name in names:
    spec = importlib.util.find_spec(name)
    assert spec is not None and spec.origin, name
    origin = pathlib.Path(spec.origin).resolve()
    assert "site-packages" in origin.parts, (name, origin)
    print(f"{name}={origin}")'
run_stage import-provenance "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -e; "$1" -I -c "$2" > "$3"' _ "$P" "$PROVENANCE_SCRIPT" "$T/.astrid-import-origins"
run_stage runtime-cli "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -e; "$1" --help >/dev/null; "$2" --help >/dev/null; "$3" -I -m astrid_runtime --help >/dev/null' \
  _ "$T/bin/astrid-runtime" "$T/bin/astrid-runtime-protocol" "$P"
run_stage markers "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'test "$(cat "$1")" = "$2" && test "$(cat "$3")" = "$4" && test -s "$5"' \
  _ "$T/.astrid-source-commit" "$S" "$T/.astrid-runtime-source-commit" "$RUNTIME_SHA" "$T/.astrid-runtime-client-identity"

# PEP 610 direct_url.json is the installed distribution provenance. Local
# source installs have directory metadata; wheel installs have archive hashes.
# Record the actual names, versions, source URLs and provenance kind in the
# retained report, then validate those values against the live child venv below.
DIST_METADATA_SCRIPT='import importlib.metadata as metadata, json, pathlib, sys, tomllib
from urllib.parse import unquote, urlparse
roots = {"astrid": pathlib.Path(sys.argv[1]).resolve(), "astrid-runtime": pathlib.Path(sys.argv[2]).resolve()}
for name, root in roots.items():
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    dist = metadata.distribution(name)
    assert dist.metadata["Name"] == project["name"] == name, (name, dist.metadata["Name"], project["name"])
    assert dist.version == project["version"], (name, dist.version, project["version"])
    direct = json.loads((pathlib.Path(dist._path) / "direct_url.json").read_text())
    url = direct.get("url")
    parsed = urlparse(url or "")
    assert parsed.scheme == "file" and parsed.netloc in ("", "localhost"), (name, url)
    assert pathlib.Path(unquote(parsed.path)).resolve() == root, (name, url, root)
    if "dir_info" in direct or "directory_info" in direct:
        info = direct.get("dir_info", direct.get("directory_info"))
        assert not info.get("editable", False), (name, info)
        kind = "directory"
    else:
        archive = direct.get("archive_info") or {}
        assert archive.get("hash", "").startswith("sha256:"), (name, direct)
        kind = "wheel"
    print("{}_name={}".format(name, dist.metadata["Name"]))
    print(f"{name}_version={dist.version}")
    print(f"{name}_direct_url={url}")
    print(f"{name}_provenance={kind}")'
run_stage distribution-provenance "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -e; "$1" -I -c "$2" "$3" "$4" > "$5"' _ \
  "$P" "$DIST_METADATA_SCRIPT" "$AGENT_SRC" "$RUNTIME_SRC" "$T/.astrid-distribution-metadata"

run_stage freeze "$FREEZE_TIMEOUT_SECONDS" bash -c \
  'set -e; { printf "status=passed\nagent_sha=%s\nruntime_sha=%s\nruntime_client_identity_sha256=%s\nrequirements_path=%s\nrequirements_lock_sha256=%s\n" "$4" "$5" "$(printf %s "$6" | sha256sum | cut -d" " -f1)" "$7" "$8"; printf "installed_import_origins:\n"; cat "$3"; printf "installed_distribution_metadata:\n"; cat "$9"; printf "pip_freeze:\n"; "$1" -I -m pip freeze --all; } > "$2"' \
  _ "$P" "$REPORT_TMP" "$T/.astrid-import-origins" "$S" "$RUNTIME_SHA" "$CLIENT_IDENTITY" "$REQUIREMENTS_PATH" "$LOCK_SHA" "$T/.astrid-distribution-metadata"

IDENTITY_SCRIPT='import importlib.metadata as metadata, json, pathlib, sys, tomllib
from urllib.parse import unquote, urlparse
report = pathlib.Path(sys.argv[1])
child = pathlib.Path(sys.argv[2]).resolve()
roots = {"astrid": pathlib.Path(sys.argv[3]).resolve(), "astrid-runtime": pathlib.Path(sys.argv[4]).resolve()}
expected = {"astrid": sys.argv[5], "astrid-runtime": sys.argv[6]}
lines = report.read_text().splitlines()
def fail(message):
    raise SystemExit("freeze identity mismatch: " + message)
def value(key):
    matches = [line[len(key) + 1:] for line in lines if line.startswith(key + "=")]
    if len(matches) != 1:
        fail(f"{key} missing or duplicated")
    return matches[0]
if value("status") != "passed":
    fail("status")
if value("agent_sha") != expected["astrid"] or value("runtime_sha") != expected["astrid-runtime"]:
    fail("source commit tuple")
origins = {}
try:
    start = lines.index("installed_import_origins:") + 1
except ValueError:
    fail("import provenance section")
for line in lines[start:]:
    if line == "installed_distribution_metadata:":
        break
    if "=" in line:
        name, origin = line.split("=", 1)
        origins[name] = pathlib.Path(origin).resolve()
for name in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"):
    origin = origins.get(name)
    if origin is None or child not in origin.parents or "site-packages" not in origin.parts:
        fail(f"isolated import origin {name}")
metadata_start = lines.index("installed_distribution_metadata:") if "installed_distribution_metadata:" in lines else None
reported = {}
if metadata_start is not None:
    for line in lines[metadata_start + 1:]:
        if line == "pip_freeze:":
            break
        if "=" in line:
            key, item = line.split("=", 1)
            reported[key] = item
for name, root in roots.items():
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    dist = metadata.distribution(name)
    if dist.metadata["Name"] != project["name"] or dist.metadata["Name"] != name:
        fail(f"distribution name {name}")
    if dist.version != project["version"]:
        fail(f"distribution version {name}")
    direct = json.loads((pathlib.Path(dist._path) / "direct_url.json").read_text())
    url = direct.get("url") or ""
    parsed = urlparse(url)
    if parsed.scheme != "file" or parsed.netloc not in ("", "localhost") or pathlib.Path(unquote(parsed.path)).resolve() != root:
        fail(f"distribution source {name}")
    if "dir_info" in direct or "directory_info" in direct:
        info = direct.get("dir_info", direct.get("directory_info"))
        if info.get("editable", False):
            fail(f"editable source {name}")
        kind = "directory"
    else:
        archive = direct.get("archive_info") or {}
        if not archive.get("hash", "").startswith("sha256:"):
            fail(f"wheel provenance {name}")
        kind = "wheel"
    freeze = [line for line in lines if line.startswith(name + " @ ")]
    if len(freeze) != 1 or freeze[0].split(" @ ", 1)[1] != url:
        fail(f"pip freeze source {name}")
    if reported:
        for key, wanted in ((f"{name}_name", name), (f"{name}_version", dist.version), (f"{name}_direct_url", url), (f"{name}_provenance", kind)):
            if reported.get(key) != wanted:
                fail(f"reported {key}")'
run_stage freeze-identity "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -e; "$1" -I -c "$2" "$3" "$4" "$5" "$6" "$7" "$8"' _ \
  "$P" "$IDENTITY_SCRIPT" "$REPORT_TMP" "$T" "$AGENT_SRC" "$RUNTIME_SRC" "$S" "$RUNTIME_SHA"

# Venv launchers contain the partial path. Fix them before the atomic publish;
# no complete destination exists until all validation above has passed.
run_stage shebang-relocation "$LOCAL_TIMEOUT_SECONDS" bash -c \
  'set -e
   while IFS= read -r file; do sed -i "s#$1#$2#g" "$file"; done < <(grep -rl -- "$1" "$3/bin" 2>/dev/null || true)' \
  _ "$T" "$D" "$T"
run_stage origin-relocation "$LOCAL_TIMEOUT_SECONDS" sed -i "s#$T#$D#g" "$T/.astrid-import-origins"
source_state "$A" "$S" && source_state "$R" "$RUNTIME_SHA" || failure 2 source-changed-during-build
run_stage readonly-source "$LOCAL_TIMEOUT_SECONDS" chmod -R a-w "$SRC"
run_stage readonly-final "$LOCAL_TIMEOUT_SECONDS" chmod -R a-w "$T"

if [ -e "$D" ] || [ -L "$D" ]; then
  failure 1 immutable-publish-race
fi
run_stage publish "$LOCAL_TIMEOUT_SECONDS" mv -T "$T" "$D"
run_stage provision-report "$LOCAL_TIMEOUT_SECONDS" mv -T "$REPORT_TMP" "$F"

if [ -n "$BS" ] && [ -n "$RT" ]; then
  if ! grep -q "^agent $N-full " "$O/tests/suites.conf"; then
    L=$(grep "^agent $BS " "$O/tests/suites.conf" || true)
    if [ -n "$L" ]; then
      echo "$L" | sed "s#^agent $BS #agent $N-full #; s#venv-agent-child-[^ /]*#$N#g; s#agent-remotion-0012#$RT#g" >> "$O/tests/suites.conf"
    fi
  fi
fi

echo "created $D (astrid from ${S:0:12}, runtime from ${RUNTIME_SHA:0:12}, $(wc -l < "$F") pins, read-only)$( [ -n "$BS" ] && echo "; suite $N-full")"
echo "imports validated: astrid astrid_runtime runtime_protocol astrid_runtime_client; distribution identity and CLI validated"
