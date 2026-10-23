#!/bin/bash
# retire-child-venv NAME — bounded, fail-closed child venv/leftover retirement.
set -u -o pipefail

O=${RETIRE_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
# RETIRE_VENV_WORK_ROOT and RETIRE_VENV_PROC_ROOT are private-fixture seams;
# production defaults remain the fixed work root and the host process table.
WORK_ROOT=${RETIRE_VENV_WORK_ROOT:-/home/user/work}
PROC_ROOT=${RETIRE_VENV_PROC_ROOT:-/proc}
MIN_AGE_SECONDS=3600

declare -a CANDIDATE_NAMES=()
declare -a CANDIDATE_PATHS=()
declare -a CANDIDATE_KINDS=()
declare -a DELETE_INDEXES=()
ACTIVE_INDEX=-1

refuse() {
  local reason=$*
  if [ "${#CANDIDATE_NAMES[@]}" -gt 0 ]; then
    local i
    for i in "${!CANDIDATE_NAMES[@]}"; do
      echo "REFUSED: target=${CANDIDATE_NAMES[$i]} path=${CANDIDATE_PATHS[$i]} case=${CANDIDATE_KINDS[$i]} disposition=refused reason=$reason"
    done
  else
    echo "REFUSED: target=${N:-unknown} case=${CASE_KIND:-unknown} disposition=refused reason=$reason"
  fi
  exit 2
}

[ "$#" -eq 1 ] || refuse "exactly one venv name is required"
N=$1
CASE_KIND=completed
BASE=$N

valid_source_timestamp() {
  local stamp=$1 parsed
  parsed=$(date -u -d "${stamp:0:4}-${stamp:4:2}-${stamp:6:2} ${stamp:9:2}:${stamp:11:2}:${stamp:13:2}" +%Y%m%dT%H%M%SZ 2>/dev/null) || return 1
  [ "$parsed" = "$stamp" ]
}

valid_source_for_base() {
  local name=$1 source_base stamp
  [[ "$name" =~ ^\.child-venv-source-(venv-agent-child-[a-z0-9][a-z0-9-]*)-([0-9]{8}T[0-9]{6}Z)-([1-9][0-9]*)\.([A-Za-z0-9]{6})$ ]] || return 1
  source_base=${BASH_REMATCH[1]}
  stamp=${BASH_REMATCH[2]}
  [ "$source_base" = "$BASE" ] || return 1
  valid_source_timestamp "$stamp"
}

if [[ "$N" =~ ^agent-remotion-[0-9a-z][0-9a-z-]*$ ]]; then
  CASE_KIND=runtime
  BASE=$N
elif [[ "$N" =~ ^(venv-agent-child-[a-z0-9][a-z0-9-]*)\.partial\.[A-Za-z0-9._-]+$ ]]; then
  CASE_KIND=partial
  BASE=${BASH_REMATCH[1]}
elif [[ "$N" =~ ^\.child-venv-source-(venv-agent-child-[a-z0-9][a-z0-9-]*)-([0-9]{8}T[0-9]{6}Z)-([1-9][0-9]*)\.([A-Za-z0-9]{6})$ ]]; then
  CASE_KIND=source
  BASE=${BASH_REMATCH[1]}
  valid_source_timestamp "${BASH_REMATCH[2]}" || refuse "source name has an invalid timestamp"
elif [[ ! "$N" =~ ^venv-agent-child-[a-z0-9][a-z0-9-]*$ ]]; then
  refuse "name does not match an owned child-venv grammar"
fi

case "$BASE" in
  venv-agent|venv-runtime|runtime|agent|app|composition|runtimeproject|sourcecheckout|agent-remotion-current)
    refuse "protected path"
    ;;
esac

[ -d "$WORK_ROOT" ] || refuse "work root is unavailable"
[ ! -L "$WORK_ROOT" ] || refuse "work root is a symlink"
ROOT_CANON=$(realpath -e -- "$WORK_ROOT") || refuse "work root cannot be canonicalized"
[ -d "$ROOT_CANON" ] || refuse "work root is not a directory"

path_for_name() {
  if [ "${CASE_KIND:-}" = runtime ]; then printf '%s/%s' "$RUNTIME_ROOT" "$1"; else printf '%s/%s' "$ROOT_CANON" "$1"; fi
}

add_candidate() {
  local name=$1 kind=$2 path
  local i
  for i in "${!CANDIDATE_NAMES[@]}"; do
    [ "${CANDIDATE_NAMES[$i]}" = "$name" ] && return 0
  done
  path=$(path_for_name "$name")
  CANDIDATE_NAMES+=("$name")
  CANDIDATE_PATHS+=("$path")
  CANDIDATE_KINDS+=("$kind")
}

validate_leftover_name() {
  local name=$1
  if [ "$CASE_KIND" = runtime ]; then
    [[ "$name" =~ ^${BASE//./\\.}\.partial\.[A-Za-z0-9]{8}$ ]] || refuse "malformed runtime partial leftover name"
    return 0
  fi
  case "$name" in
    "$BASE.partial."*) [[ "$name" =~ ^${BASE//./\\.}\.partial\.[A-Za-z0-9._-]+$ ]] || refuse "malformed partial leftover name" ;;
    ".child-venv-source-$BASE-"*) valid_source_for_base "$name" || refuse "malformed source leftover name" ;;
    *) refuse "foreign associated leftover name" ;;
  esac
}

collect_associated() {
  local item name
  local associated_root=$ROOT_CANON
  if [ "$CASE_KIND" = runtime ]; then associated_root=$RUNTIME_ROOT; fi
  shopt -s nullglob dotglob
  for item in "$associated_root/$BASE.partial."*; do
    name=${item##*/}
    validate_leftover_name "$name"
    if [ "$CASE_KIND" = runtime ]; then add_candidate "$name" runtime-partial; else add_candidate "$name" partial; fi
  done
  if [ "$CASE_KIND" != runtime ]; then
    for item in "$ROOT_CANON/.child-venv-source-$BASE-"*; do
      name=${item##*/}
      validate_leftover_name "$name"
      add_candidate "$name" source
    done
  fi
  shopt -u nullglob dotglob
}

TARGET=$ROOT_CANON/$N
if [ "$CASE_KIND" = runtime ]; then
  [ -d "$ROOT_CANON/runtimes" ] || refuse "runtime root is unavailable"
  [ ! -L "$ROOT_CANON/runtimes" ] || refuse "runtime root is a symlink"
  RUNTIME_ROOT=$(realpath -e -- "$ROOT_CANON/runtimes") || refuse "runtime root cannot be canonicalized"
  [ "$RUNTIME_ROOT" = "$ROOT_CANON/runtimes" ] || refuse "runtime root escapes work root"
  TARGET=$RUNTIME_ROOT/$N
  collect_associated
  [ -e "$TARGET" ] || [ -L "$TARGET" ] || refuse "requested runtime does not exist"
  add_candidate "$N" runtime
elif [ "$CASE_KIND" = completed ]; then
  collect_associated
  if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
    add_candidate "$N" completed
  fi
elif [ "$CASE_KIND" = partial ] || [ "$CASE_KIND" = source ]; then
  [ -e "$TARGET" ] || [ -L "$TARGET" ] || refuse "requested leftover does not exist"
  add_candidate "$N" "$CASE_KIND"
  collect_associated
fi
[ "${#CANDIDATE_NAMES[@]}" -gt 0 ] || refuse "target or associated leftover does not exist"

for i in "${!CANDIDATE_NAMES[@]}"; do
  [ "${CANDIDATE_NAMES[$i]}" = "$N" ] && DELETE_INDEXES+=("$i")
done
if [ "$CASE_KIND" = completed ]; then
  for i in "${!CANDIDATE_NAMES[@]}"; do
    if [ "${CANDIDATE_KINDS[$i]}" = completed ] || [ "${CANDIDATE_KINDS[$i]}" = runtime ]; then continue; fi
    # Existence alone is not source custody. A young leftover is observed and
    # retained; only a stale leftover joins this request's retirement set.
    mtime=$(stat -c %Y -- "${CANDIDATE_PATHS[$i]}") || refuse "candidate age is unreadable"
    now=$(date +%s) || refuse "clock is unreadable"
    [[ "$mtime" =~ ^[0-9]+$ && "$now" =~ ^[0-9]+$ ]] || refuse "candidate age is invalid"
    if [ $((now - mtime)) -gt "$MIN_AGE_SECONDS" ]; then
      DELETE_INDEXES+=("$i")
    elif [ "${CANDIDATE_KINDS[$i]}" = partial ]; then
      # A young partial is indistinguishable from a builder still publishing;
      # source-custody existence alone is not treated as active, but partials
      # remain a live-window refusal until stale.
      refuse "partial candidate is not older than one hour"
    fi
  done
else
  for i in "${!CANDIDATE_NAMES[@]}"; do
    [ "${CANDIDATE_KINDS[$i]}" = partial ] || [ "${CANDIDATE_KINDS[$i]}" = runtime-partial ] || continue
    [ "${CANDIDATE_NAMES[$i]}" = "$N" ] && continue
    mtime=$(stat -c %Y -- "${CANDIDATE_PATHS[$i]}") || refuse "candidate age is unreadable"
    now=$(date +%s) || refuse "clock is unreadable"
    [[ "$mtime" =~ ^[0-9]+$ && "$now" =~ ^[0-9]+$ ]] || refuse "candidate age is invalid"
    [ $((now - mtime)) -gt "$MIN_AGE_SECONDS" ] || refuse "associated partial candidate is not older than one hour"
    [ "$CASE_KIND" = runtime ] && DELETE_INDEXES+=("$i")
  done
fi

path_uses_candidate() {
  local value=$1 i canon
  for i in "${!CANDIDATE_NAMES[@]}"; do
    canon=${CANDIDATE_PATHS[$i]}
    case "$value" in
      "$canon"|"$canon"/*|"$canon (deleted)"|"$canon"/*" (deleted)") return 0;;
    esac
  done
  return 1
}

readable_regular() {
  local file=$1
  [ -f "$file" ] && [ ! -L "$file" ] && [ -r "$file" ]
}

scan_reference_file() {
  local file=$1 rc i
  readable_regular "$file" || refuse "uninspectable reference file"
  for i in "${!CANDIDATE_NAMES[@]}"; do
    LC_ALL=C grep -aFq -- "${CANDIDATE_NAMES[$i]}" "$file"
    rc=$?
    [ "$rc" -eq 1 ] || [ "$rc" -eq 0 ] || refuse "reference scan failed"
    [ "$rc" -eq 0 ] && refuse "target is referenced: candidate is referenced"
    LC_ALL=C grep -aFq -- "${CANDIDATE_PATHS[$i]}" "$file"
    rc=$?
    [ "$rc" -eq 1 ] || [ "$rc" -eq 0 ] || refuse "canonical reference scan failed"
    [ "$rc" -eq 0 ] && refuse "target is referenced: canonical candidate is referenced"
  done
}

scan_current_references() {
  local file
  readable_regular "$O/tests/suites.conf" || refuse "suites.conf is unavailable"
  scan_reference_file "$O/tests/suites.conf"
  [ -d "$O/tests" ] || refuse "tests directory is unavailable"
  shopt -s nullglob
  local env_files=("$O/tests/"*.env)
  for file in "${env_files[@]}"; do scan_reference_file "$file"; done
  shopt -u nullglob
}

scan_pending_references() {
  local file base
  [ -d "$O/queue/pending" ] || refuse "pending queue is unavailable"
  shopt -s nullglob dotglob
  local pending_files=("$O/queue/pending/"*)
  for file in "${pending_files[@]}"; do
    [ -e "$file" ] || [ -L "$file" ] || continue
    readable_regular "$file" || refuse "uninspectable pending request"
    base=${file##*/}
    [ "$base" = "retire-venv-$N" ] && continue
    scan_reference_file "$file"
  done
  shopt -u nullglob dotglob
}

scan_worker_references() {
  local worker file
  [ -d "$O/workers" ] || refuse "workers directory is unavailable"
  shopt -s nullglob
  local workers=("$O/workers/"*)
  for worker in "${workers[@]}"; do
    [ -d "$worker" ] || continue
    [ -e "$worker/running" ] || continue
    [ ! -L "$worker/running" ] && [ -f "$worker/running" ] && [ -r "$worker/running" ] || refuse "uninspectable running marker"
    readable_regular "$worker/meta" || refuse "running worker metadata is unavailable"
    scan_reference_file "$worker/meta"
    for file in "$worker/brief.md" "$worker/env"; do
      [ -e "$file" ] || [ -L "$file" ] || continue
      scan_reference_file "$file"
    done
  done
  shopt -u nullglob
}

ancestor_pid() {
  local pid=$1 parent
  while [ "$pid" -gt 1 ] 2>/dev/null; do
    printf '%s\n' "$pid" 2>/dev/null || return 0
    parent=$(awk '{print $4}' "$PROC_ROOT/$pid/stat" 2>/dev/null) || return 0
    [ -n "$parent" ] || return 0
    [ "$parent" != "$pid" ] || return 0
    pid=$parent
  done
}

is_our_process() {
  local pid=$1 p
  [ "$pid" -eq "$$" ] && return 0
  while read -r p; do [ "$pid" -eq "$p" ] && return 0; done < <(ancestor_pid "$$")
  return 1
}

read_process_link() {
  local proc=$1 leaf=$2 link
  link=$(readlink -- "$proc/$leaf") || { [ ! -d "$proc" ] && return 3; return 2; }
  path_uses_candidate "$link" && refuse "live process $leaf uses candidate"
  return 0
}

scan_processes() {
  local proc pid bytes cmdline link fd
  [ -d "$PROC_ROOT" ] && [ -r "$PROC_ROOT" ] || refuse "process table is unavailable"
  shopt -s nullglob
  local processes=("$PROC_ROOT"/[0-9]*)
  for proc in "${processes[@]}"; do
    [ -d "$proc" ] || continue
    pid=${proc##*/}
    is_our_process "$pid" && continue
    [ -r "$proc/cmdline" ] || { [ ! -d "$proc" ] && continue; refuse "process argv is unreadable"; }
    bytes=$(wc -c < "$proc/cmdline") || { [ ! -d "$proc" ] && continue; refuse "process argv cannot be read"; }
    [[ "$bytes" =~ ^[0-9]+$ ]] || refuse "process argv length is invalid"
    if [ "$bytes" -eq 0 ]; then
      # A process with a verified empty cmdline and no readable executable is a
      # kernel thread/non-user. PID or zombie status is never used as a guess.
      link=$(readlink -- "$proc/exe") || { [ ! -d "$proc" ] && continue; continue; }
      path_uses_candidate "$link" && refuse "live process executable uses candidate"
    else
      cmdline=$(tr '\0' '\n' < "$proc/cmdline") || { [ ! -d "$proc" ] && continue; refuse "process argv cannot be read"; }
      for i in "${!CANDIDATE_NAMES[@]}"; do
        case "$cmdline" in *"${CANDIDATE_NAMES[$i]}"*|*"${CANDIDATE_PATHS[$i]}"*) refuse "live process references candidate";; esac
      done
      link=$(readlink -- "$proc/exe") || { [ ! -d "$proc" ] && continue; refuse "process executable is unreadable"; }
      path_uses_candidate "$link" && refuse "live process executable uses candidate"
    fi
    link=$(readlink -- "$proc/cwd") || { [ ! -d "$proc" ] && continue; refuse "process cwd is unreadable"; }
    path_uses_candidate "$link" && refuse "live process cwd uses candidate"
    local fds=("$proc/fd/"*)
    for fd in "${fds[@]}"; do
      [ -e "$fd" ] || [ -L "$fd" ] || continue
      link=$(readlink -- "$fd") || { [ ! -d "$proc" ] && continue; refuse "process open files are unreadable"; }
      path_uses_candidate "$link" && refuse "live process has candidate open"
    done
  done
  shopt -u nullglob
}

check_markers() {
  local target=$1 marker value have=0 missing=0
  for marker in .astrid-source-commit .astrid-runtime-source-commit; do
    if [ -e "$target/$marker" ] || [ -L "$target/$marker" ]; then
      have=$((have + 1))
      [ -f "$target/$marker" ] && [ ! -L "$target/$marker" ] && [ -r "$target/$marker" ] || refuse "tuple marker is unavailable"
      value=$(<"$target/$marker") || refuse "tuple marker cannot be read"
      [[ "$value" =~ ^[0-9a-f]{40,64}$ ]] || refuse "tuple marker identity is invalid"
    else
      missing=$((missing + 1))
    fi
  done
  [ "$have" -eq 0 ] || [ "$missing" -eq 0 ] || refuse "owned child marker is unavailable: tuple marker pair is incomplete"
}

check_candidate_shape_age() {
  local i=$1 path=${CANDIDATE_PATHS[$1]}
  [ -e "$path" ] || [ -L "$path" ] || refuse "candidate disappeared"
  [ ! -L "$path" ] || refuse "candidate is a symlink"
  [ -d "$path" ] || refuse "candidate is not a directory"
  local canon
  canon=$(realpath -e -- "$path") || refuse "candidate cannot be canonicalized"
  expected_root=$ROOT_CANON
  [ "$CASE_KIND" = runtime ] && expected_root=$RUNTIME_ROOT
  [ "$canon" = "$expected_root/${CANDIDATE_NAMES[$i]}" ] || refuse "candidate escapes work root"
  if [ "$CASE_KIND" = runtime ]; then
    local marker marker_count=0 value
    if [ "${CANDIDATE_KINDS[$i]}" = runtime-partial ]; then
      if [ -e "$path/.provision-failure" ] || [ -L "$path/.provision-failure" ]; then
        [ -f "$path/.provision-failure" ] && [ ! -L "$path/.provision-failure" ] && [ -r "$path/.provision-failure" ] || refuse "runtime partial marker is unavailable"
        LC_ALL=C grep -Eq '^status=failed$' "$path/.provision-failure" || refuse "runtime partial marker status is invalid"
        LC_ALL=C grep -Eq '^stage=[a-z0-9-]+$' "$path/.provision-failure" || refuse "runtime partial marker stage is invalid"
        LC_ALL=C grep -Eq '^agent_sha=[0-9a-f]{40}$' "$path/.provision-failure" || refuse "runtime partial agent marker is invalid"
        LC_ALL=C grep -Eq '^lock_sha256=[0-9a-f]{64}$' "$path/.provision-failure" || refuse "runtime partial lock marker is invalid"
      fi
      return 0
    fi
    for marker in .astrid-agent-source-commit .astrid-package-lock-sha256 .astrid-node-version .astrid-npm-version; do
      if [ -e "$path/$marker" ] || [ -L "$path/$marker" ]; then
        marker_count=$((marker_count + 1))
        [ -f "$path/$marker" ] && [ ! -L "$path/$marker" ] && [ -r "$path/$marker" ] || refuse "runtime immutable marker is unavailable"
        value=$(<"$path/$marker") || refuse "runtime immutable marker cannot be read"
        case "$marker" in
          .astrid-agent-source-commit) [[ "$value" =~ ^[0-9a-f]{40}$ ]] || refuse "runtime agent marker identity is invalid" ;;
          .astrid-package-lock-sha256) [[ "$value" =~ ^[0-9a-f]{64}$ ]] || refuse "runtime lock marker identity is invalid" ;;
          .astrid-node-version) [ "$value" = v20.19.4 ] || refuse "runtime Node marker identity is invalid" ;;
          .astrid-npm-version) [ "$value" = 10.8.2 ] || refuse "runtime npm marker identity is invalid" ;;
        esac
      fi
    done
    [ "$marker_count" -eq 0 ] || [ "$marker_count" -eq 4 ] || refuse "runtime immutable marker set is incomplete"
    for marker in .runtime-env .runtime-suite .astrid-installed-module-origins; do
      if [ -e "$path/$marker" ] || [ -L "$path/$marker" ]; then
        [ -f "$path/$marker" ] && [ ! -L "$path/$marker" ] && [ -r "$path/$marker" ] || refuse "runtime registration marker is unavailable"
      fi
    done
    [ -f "$path/package.json" ] && [ ! -L "$path/package.json" ] && [ -r "$path/package.json" ] || refuse "runtime package manifest is unavailable"
    [ -f "$path/package-lock.json" ] && [ ! -L "$path/package-lock.json" ] && [ -r "$path/package-lock.json" ] || refuse "runtime lock manifest is unavailable"
  else
    check_markers "$path"
  fi
}

check_delete_age() {
  local i=$1 path=${CANDIDATE_PATHS[$1]} mtime now age
  mtime=$(stat -c %Y -- "$path") || refuse "candidate age is unreadable"
  now=$(date +%s) || refuse "clock is unreadable"
  [[ "$mtime" =~ ^[0-9]+$ && "$now" =~ ^[0-9]+$ ]] || refuse "candidate age is invalid"
  age=$((now - mtime))
  [ "$age" -gt "$MIN_AGE_SECONDS" ] || refuse "candidate is not older than one hour"
}

check_all() {
  local i j
  [ "$ROOT_CANON" = "$(realpath -e -- "$WORK_ROOT")" ] || refuse "work root changed containment"
  for i in "${!CANDIDATE_NAMES[@]}"; do check_candidate_shape_age "$i"; done
  for j in "${DELETE_INDEXES[@]}"; do check_delete_age "$j"; done
  scan_current_references
  scan_pending_references
  scan_worker_references
  scan_processes
}

check_all
declare -a FINGERPRINTS=()
for i in "${!CANDIDATE_NAMES[@]}"; do
  FINGERPRINTS+=("$(stat -c '%d:%i:%Y:%s' -- "${CANDIDATE_PATHS[$i]}")") || refuse "candidate fingerprint is unreadable"
done
check_all
for i in "${!CANDIDATE_NAMES[@]}"; do
  [ "$(stat -c '%d:%i:%Y:%s' -- "${CANDIDATE_PATHS[$i]}")" = "${FINGERPRINTS[$i]}" ] || refuse "target replacement race detected: candidate replacement race detected"
done

for i in "${!CANDIDATE_NAMES[@]}"; do
  found=0
  for j in "${DELETE_INDEXES[@]}"; do [ "$i" = "$j" ] && found=1; done
  if [ "$found" -eq 1 ]; then
      echo "ELIGIBLE target=${CANDIDATE_NAMES[$i]} path=${CANDIDATE_PATHS[$i]} case=${CANDIDATE_KINDS[$i]} disposition=retire"
  else
    echo "ELIGIBLE target=${CANDIDATE_NAMES[$i]} path=${CANDIDATE_PATHS[$i]} case=${CANDIDATE_KINDS[$i]} disposition=retained-associated"
  fi
done

command -v python3 >/dev/null 2>&1 || refuse "bounded removal API is unavailable"
DELETE_ROOT=$ROOT_CANON
[ "$CASE_KIND" = runtime ] && DELETE_ROOT=$RUNTIME_ROOT
python3 - "$DELETE_ROOT" "${#CANDIDATE_NAMES[@]}" "${CANDIDATE_NAMES[@]}" "${FINGERPRINTS[@]}" "${DELETE_INDEXES[@]}" <<'PY'
import os
import shutil
import stat
import sys

root = sys.argv[1]
count = int(sys.argv[2])
names = sys.argv[3:3 + count]
fingerprints = sys.argv[3 + count:3 + count * 2]
delete_indexes = {int(value) for value in sys.argv[3 + count * 2:]}

def refuse(message):
    print("REFUSED: final " + message)
    raise SystemExit(2)

if os.path.realpath(root) != root or len(names) != count or len(fingerprints) != count:
    refuse("removal arguments are invalid")

for index, name in enumerate(names):
    target = os.path.join(root, name)
    if os.path.realpath(target) != target or not os.path.isdir(target) or os.path.islink(target):
        refuse("candidate containment changed")
    try:
        st = os.stat(target, follow_symlinks=False)
        current = f"{st.st_dev}:{st.st_ino}:{int(st.st_mtime)}:{st.st_size}"
    except (OSError, ValueError):
        refuse("candidate inspection failed")
    if current != fingerprints[index]:
        refuse("candidate replacement race detected")

def onerror(function, path, _exc_info):
    try:
        lexical = os.path.abspath(path)
        target = os.path.abspath(os.path.join(root, names[active]))
        if os.path.commonpath((lexical, target)) != target or os.path.islink(path):
            refuse("removal path escaped candidate")
        mode = os.lstat(path).st_mode
        os.chmod(path, mode | stat.S_IWUSR)
        function(path)
    except (OSError, ValueError):
        refuse("candidate removal failed")

for active in sorted(delete_indexes):
    if active < 0 or active >= count:
        refuse("removal index is invalid")
    try:
        shutil.rmtree(os.path.join(root, names[active]), onerror=onerror)
    except (OSError, ValueError):
        refuse("candidate removal failed")
    print(f"retired target={names[active]} path={os.path.join(root, names[active])} disposition=retired")
PY
