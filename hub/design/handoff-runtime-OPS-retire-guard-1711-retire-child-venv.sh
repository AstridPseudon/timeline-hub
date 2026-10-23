#!/bin/bash
# retire-child-venv NAME — bounded, fail-closed child venv retirement.
set -u -o pipefail

O=${RETIRE_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
# The production default is intentionally fixed. RETIRE_VENV_WORK_ROOT exists
# only for private fixture tests; the same direct-child/canonical checks apply.
WORK_ROOT=${RETIRE_VENV_WORK_ROOT:-/home/user/work}
MIN_AGE_SECONDS=3600

refuse() {
  echo "REFUSED: $*"
  exit 2
}

[ "$#" -eq 1 ] || refuse "exactly one venv name is required"
N=$1
case "$N" in
  venv-agent-child-[a-z0-9][a-z0-9-]*) ;;
  *) refuse "name must be venv-agent-child-<suffix>" ;;
esac

case "$N" in
  venv-agent|venv-runtime|runtime|agent|runtimeproject|sourcecheckout) refuse "protected path" ;
esac

[ -d "$WORK_ROOT" ] || refuse "work root is unavailable"
[ ! -L "$WORK_ROOT" ] || refuse "work root is a symlink"
ROOT_CANON=$(realpath -e -- "$WORK_ROOT") || refuse "work root cannot be canonicalized"
[ -d "$ROOT_CANON" ] || refuse "work root is not a directory"

TARGET=$ROOT_CANON/$N
[ -e "$TARGET" ] || [ -L "$TARGET" ] || refuse "target does not exist"
[ ! -L "$TARGET" ] || refuse "target is a symlink"
[ -d "$TARGET" ] || refuse "target is not a directory"
TARGET_CANON=$(realpath -e -- "$TARGET") || refuse "target cannot be canonicalized"
[ "$TARGET_CANON" = "$ROOT_CANON/$N" ] || refuse "target escapes work root"

path_uses_target() {
  local value=$1
  case "$value" in
    "$TARGET_CANON"|"$TARGET_CANON"/*|"$TARGET_CANON (deleted)"|"$TARGET_CANON"/*" (deleted)") return 0 ;;
  esac
  return 1
}

readable_regular() {
  local file=$1
  [ -f "$file" ] && [ ! -L "$file" ] && [ -r "$file" ]
}

scan_reference_file() {
  local file=$1 rc
  readable_regular "$file" || refuse "uninspectable reference file"
  LC_ALL=C grep -aFq -- "$N" "$file"
  rc=$?
  [ "$rc" -eq 1 ] || [ "$rc" -eq 0 ] || refuse "reference scan failed"
  [ "$rc" -eq 0 ] && refuse "target is referenced"
  LC_ALL=C grep -aFq -- "$TARGET_CANON" "$file"
  rc=$?
  [ "$rc" -eq 1 ] || [ "$rc" -eq 0 ] || refuse "canonical reference scan failed"
  [ "$rc" -eq 0 ] && refuse "canonical target is referenced"
}

scan_current_references() {
  local file
  readable_regular "$O/tests/suites.conf" || refuse "suites.conf is unavailable"
  scan_reference_file "$O/tests/suites.conf"
  [ -d "$O/tests" ] || refuse "tests directory is unavailable"
  shopt -s nullglob
  local env_files=("$O/tests/"*.env)
  for file in "${env_files[@]}"; do
    scan_reference_file "$file"
  done
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
    parent=$(awk '{print $4}' "/proc/$pid/stat" 2>/dev/null) || return 0
    [ -n "$parent" ] || return 0
    [ "$parent" != "$pid" ] || return 0
    pid=$parent
  done
}

is_our_process() {
  local pid=$1 p
  [ "$pid" -eq "$$" ] && return 0
  while read -r p; do
    [ "$pid" -eq "$p" ] && return 0
  done < <(ancestor_pid "$$")
  return 1
}

scan_processes() {
  local proc pid cmdline link fd
  [ -d /proc ] && [ -r /proc ] || refuse "process table is unavailable"
  shopt -s nullglob
  local processes=(/proc/[0-9]*)
  for proc in "${processes[@]}"; do
    [ -d "$proc" ] || continue
    pid=${proc##*/}
    is_our_process "$pid" && continue
    [ -r "$proc/cmdline" ] || { [ ! -d "$proc" ] && continue; refuse "process argv is unreadable"; }
    cmdline=$(tr '\0' '\n' < "$proc/cmdline") || { [ ! -d "$proc" ] && continue; refuse "process argv cannot be read"; }
    case "$cmdline" in *"$N"*|*"$TARGET_CANON"*) refuse "live process references target" ;; esac
    link=$(readlink -- "$proc/exe") || { [ ! -d "$proc" ] && continue; refuse "process executable is unreadable"; }
    path_uses_target "$link" && refuse "live process executable uses target"
    link=$(readlink -- "$proc/cwd") || { [ ! -d "$proc" ] && continue; refuse "process cwd is unreadable"; }
    path_uses_target "$link" && refuse "live process cwd uses target"
    local fds=("$proc/fd/"*)
    for fd in "${fds[@]}"; do
      [ -e "$fd" ] || [ -L "$fd" ] || continue
      link=$(readlink -- "$fd") || { [ ! -d "$proc" ] && continue; refuse "process open files are unreadable"; }
      path_uses_target "$link" && refuse "live process has target open"
    done
  done
  shopt -u nullglob
}

check_markers() {
  local marker value
  for marker in .astrid-source-commit .astrid-runtime-source-commit; do
    marker=$TARGET/$marker
    [ -f "$marker" ] && [ ! -L "$marker" ] && [ -r "$marker" ] || refuse "owned child marker is unavailable"
    value=$(<"$marker") || refuse "owned child marker cannot be read"
    [[ "$value" =~ ^[0-9a-f]{40,64}$ ]] || refuse "owned child marker identity is invalid"
  done
}

check_builder_artifacts() {
  local item
  shopt -s nullglob
  for item in "$ROOT_CANON/$N.partial."*; do
    [ -e "$item" ] || [ -L "$item" ] || continue
    refuse "partial or active builder exists"
  done
  shopt -u nullglob
}

check_age_and_fingerprint() {
  local mtime now age
  mtime=$(stat -c %Y -- "$TARGET") || refuse "target age is unreadable"
  now=$(date +%s) || refuse "clock is unreadable"
  [[ "$mtime" =~ ^[0-9]+$ && "$now" =~ ^[0-9]+$ ]] || refuse "target age is invalid"
  age=$((now - mtime))
  [ "$age" -gt "$MIN_AGE_SECONDS" ] || refuse "target is not older than one hour"
}

check_all() {
  [ "$TARGET_CANON" = "$ROOT_CANON/$N" ] || refuse "target changed containment"
  [ -d "$TARGET" ] && [ ! -L "$TARGET" ] || refuse "target changed type"
  check_age_and_fingerprint
  check_markers
  check_builder_artifacts
  scan_current_references
  scan_pending_references
  scan_worker_references
  scan_processes
}

check_all
FINGERPRINT=$(stat -c '%d:%i:%Y:%s' -- "$TARGET") || refuse "target fingerprint is unreadable"
check_all
[ "$(stat -c '%d:%i:%Y:%s' -- "$TARGET")" = "$FINGERPRINT" ] || refuse "target replacement race detected"

command -v python3 >/dev/null 2>&1 || refuse "bounded removal API is unavailable"
python3 - "$ROOT_CANON" "$N" "$TARGET_CANON" "$FINGERPRINT" <<'PY'
import os
import shutil
import stat
import sys

root, name, target, fingerprint = sys.argv[1:]
expected = os.path.join(root, name)

def refuse(message):
    print("REFUSED: " + message)
    raise SystemExit(2)

try:
    if os.path.realpath(root) != root or os.path.realpath(target) != target:
        refuse("final path canonicalization changed")
    if target != expected or not os.path.isdir(target) or os.path.islink(target):
        refuse("final target validation failed")
    st = os.stat(target, follow_symlinks=False)
    current = f"{st.st_dev}:{st.st_ino}:{int(st.st_mtime)}:{st.st_size}"
    if current != fingerprint:
        refuse("target replacement race detected")
except (OSError, ValueError):
    refuse("final target inspection failed")

def onerror(function, path, _exc_info):
    try:
        lexical = os.path.abspath(path)
        if os.path.commonpath((lexical, target)) != target or os.path.islink(path):
            refuse("removal path escaped target")
        mode = os.lstat(path).st_mode
        os.chmod(path, mode | stat.S_IWUSR)
        function(path)
    except (OSError, ValueError):
        refuse("immutable target removal failed")

def prepare_directories():
    def walk_error(_error):
        refuse("target directory is unreadable")
    for current, directories, _files in os.walk(target, topdown=True, followlinks=False, onerror=walk_error):
        lexical = os.path.abspath(current)
        if os.path.commonpath((lexical, target)) != target:
            refuse("directory walk escaped target")
        safe_directories = []
        for directory in directories:
            path = os.path.join(current, directory)
            if os.path.islink(path):
                continue
            lexical = os.path.abspath(path)
            if os.path.commonpath((lexical, target)) != target:
                refuse("directory walk escaped target")
            mode = os.lstat(path).st_mode
            os.chmod(path, mode | stat.S_IWUSR)
            safe_directories.append(directory)
        directories[:] = safe_directories
        mode = os.lstat(current).st_mode
        os.chmod(current, mode | stat.S_IWUSR)

try:
    prepare_directories()
    shutil.rmtree(target, onerror=onerror)
except (OSError, ValueError):
    refuse("target removal failed")
print(f"retired {target}")
PY
