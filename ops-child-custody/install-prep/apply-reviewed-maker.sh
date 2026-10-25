#!/bin/bash
# Manager-only installer. It refuses unless the exact D137 decision input is
# supplied. This worker never invokes this route.
set -euo pipefail

die() {
  printf 'REFUSED: %s\n' "$1" >&2
  exit 2
}

: "${ORCH:?set ORCH to the approved orchestration root}"
: "${SOURCE_CHECKOUT:?set SOURCE_CHECKOUT to the reviewed Composition checkout}"
: "${D137_DECISION:?set D137_DECISION to the exact D137 decision JSON}"

SOURCE_COMMIT=
SOURCE_REL=ops-child-custody/make-child-venv
TARGET=$ORCH/bin/make-child-venv
BIN_DIR=$ORCH/bin
BACKUP_DIR=$ORCH/backups
LOCK_DIR=$BIN_DIR/.make-child-venv.install.lock
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ATOMIC_HELPER=$SCRIPT_DIR/install_atomic.py
GATE_HELPER=$SCRIPT_DIR/verify_gate_artifacts.py
EXPECTED_CANDIDATE_SHA256=7905232e0dc4b77921ecf257f89f2a951614e0dcbc9eea547c08c992062e5792
EXPECTED_CANDIDATE_BYTES=81516
EXPECTED_PREIMAGE_SHA256=4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36
EXPECTED_PREIMAGE_BYTES=75503
EXPECTED_MODE=755
EXPECTED_BENCH_STORE_SHA256=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2
EXPECTED_DEPENDENCY_HELPER_SHA256=116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2
EXPECTED_UID=$(id -u)

case "$ORCH:$SOURCE_CHECKOUT" in
  /*:/*) ;;
  *) die 'ORCH and SOURCE_CHECKOUT must be absolute' ;;
esac

physical_owned_dir() {
  local path=$1 label=$2 info
  [ -d "$path" ] && [ ! -L "$path" ] || die "$label is not a physical directory"
  [ "$path" = "$(readlink -e -- "$path" 2>/dev/null)" ] || die "$label is not a physical directory"
  info=$(stat -c '%u %a %h' -- "$path") || die "$label stat failed"
  [ "${info%% *}" = "$EXPECTED_UID" ] || die "$label owner mismatch"
  info=${info#* }
  info=${info%% *}
  [ $((8#$info & 022)) -eq 0 ] || die "$label is broadly writable"
}

physical_ancestry() {
  local path=$1 label=$2 current info owner mode
  current=$(readlink -e -- "$path" 2>/dev/null) || die "$label cannot be resolved"
  while :; do
    [ -d "$current" ] && [ ! -L "$current" ] || die "$label ancestry is not physical"
    info=$(stat -c '%u %a' -- "$current") || die "$label ancestry stat failed"
    owner=${info%% *}
    mode=${info#* }
    [ "$owner" = 0 ] || [ "$owner" = "$EXPECTED_UID" ] || die "$label ancestry owner mismatch"
    [ $((8#$mode & 022)) -eq 0 ] || die "$label ancestry is broadly writable"
    [ "$current" = / ] && break
    current=$(dirname -- "$current")
  done
}

physical_owned_dir "$ORCH" 'ORCH'
physical_owned_dir "$BIN_DIR" 'ORCH/bin'
physical_owned_dir "$BACKUP_DIR" 'ORCH/backups'
physical_owned_dir "${TMPDIR:?set TMPDIR to a private owned directory}" 'TMPDIR'
physical_ancestry "$SOURCE_CHECKOUT" 'source checkout'
[ "$SOURCE_CHECKOUT" = "$(readlink -e -- "$SOURCE_CHECKOUT" 2>/dev/null)" ] || die 'source checkout must be physical'
physical_owned_dir "$SOURCE_CHECKOUT" 'source checkout'

path_overlaps() {
  local left=$1 right=$2
  if [[ "$left" == "$right" || "$left" == "$right"/* ||
    "$right" == "$left" || "$right" == "$left"/* ]]; then
    return 0
  fi
  return 1
}

ORCH_REAL=$(readlink -e -- "$ORCH")
SOURCE_REAL=$(readlink -e -- "$SOURCE_CHECKOUT")
TMPDIR_REAL=$(readlink -e -- "$TMPDIR")
path_overlaps "$TMPDIR_REAL" "$ORCH_REAL" && die 'TMPDIR overlaps ORCH'
path_overlaps "$TMPDIR_REAL" "$SOURCE_REAL" && die 'TMPDIR overlaps source checkout'

D137_GATE_OUTPUT=$(PYTHONDONTWRITEBYTECODE=1 python3 -B "$GATE_HELPER" "$D137_DECISION") || die 'D137 decision input refused'
SOURCE_COMMIT=$(printf '%s\n' "$D137_GATE_OUTPUT" | sed -n 's/^source_commit=//p')
[[ "$SOURCE_COMMIT" =~ ^[0-9a-f]{40}$ ]] || die 'D137 decision source commit missing'

regular_owned_file() {
  local path=$1 label=$2 expected_mode=${3:-}
  [ -f "$path" ] && [ ! -L "$path" ] || die "$label is not a regular non-symlink file"
  [ "$(stat -c '%h' -- "$path")" = 1 ] || die "$label is hardlinked"
  [ "$(stat -c '%u' -- "$path")" = "$EXPECTED_UID" ] || die "$label owner mismatch"
  if [ -n "$expected_mode" ]; then
    [ "$(stat -c '%a' -- "$path")" = "$expected_mode" ] || die "$label mode mismatch"
  fi
}

sha256() { sha256sum -- "$1" | cut -d' ' -f1; }
bytes() { stat -c '%s' -- "$1"; }

regular_owned_file "$TARGET" 'installed maker' "$EXPECTED_MODE"
[ "$(sha256 "$TARGET")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'installed maker preimage CAS mismatch'
[ "$(bytes "$TARGET")" = "$EXPECTED_PREIMAGE_BYTES" ] || die 'installed maker preimage byte count mismatch'
regular_owned_file "$ORCH/bin/bench_store.py" 'protected Store helper' 755
regular_owned_file "$ORCH/bin/verify_dependency_seed.py" 'protected dependency helper' 755
[ "$(sha256 "$ORCH/bin/bench_store.py")" = "$EXPECTED_BENCH_STORE_SHA256" ] || die 'protected Store helper hash mismatch'
[ "$(sha256 "$ORCH/bin/verify_dependency_seed.py")" = "$EXPECTED_DEPENDENCY_HELPER_SHA256" ] || die 'protected dependency helper hash mismatch'

git -C "$SOURCE_CHECKOUT" cat-file -e "$SOURCE_COMMIT^{commit}" || die 'reviewed source commit is unavailable'
SOURCE_STATUS=$(git -C "$SOURCE_CHECKOUT" status --porcelain --untracked-files=all)
[ -z "$SOURCE_STATUS" ] || die 'source checkout is dirty'

# Extract into a private TMPDIR replica. This never writes the protected source
# checkout and preserves the Git-recorded 0755 mode in the extracted candidate.
PRIVATE_ROOT=$(mktemp -d "$TMPDIR_REAL/ops-inventory-install.XXXXXX")
[ "$PRIVATE_ROOT" = "$(readlink -e -- "$PRIVATE_ROOT")" ] || die 'private root is not physical'
physical_owned_dir "$PRIVATE_ROOT" 'private extraction root'
path_overlaps "$PRIVATE_ROOT" "$ORCH_REAL" && die 'private root overlaps ORCH'
path_overlaps "$PRIVATE_ROOT" "$SOURCE_REAL" && die 'private root overlaps source checkout'
git -C "$SOURCE_CHECKOUT" archive --format=tar "$SOURCE_COMMIT" "$SOURCE_REL" | tar -x -C "$PRIVATE_ROOT"
CANDIDATE=$PRIVATE_ROOT/$SOURCE_REL
chmod -- "$EXPECTED_MODE" "$CANDIDATE"
regular_owned_file "$CANDIDATE" 'extracted candidate' "$EXPECTED_MODE"
[ "$(sha256 "$CANDIDATE")" = "$EXPECTED_CANDIDATE_SHA256" ] || die 'candidate hash mismatch'
[ "$(bytes "$CANDIDATE")" = "$EXPECTED_CANDIDATE_BYTES" ] || die 'candidate byte count mismatch'

STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP=$BACKUP_DIR/make-child-venv.$STAMP.bak
[ ! -e "$BACKUP" ] && [ ! -L "$BACKUP" ] || die 'backup path already exists; refusing to clobber'
BACKUP_TMP=$BACKUP_DIR/.make-child-venv.$STAMP.$$.backup.tmp
if ! mkdir -- "$LOCK_DIR"; then
  die 'receiving lock is held or was pre-created'
fi
LOCK_HELD=1
trap 'if [ "${LOCK_HELD:-0}" = 1 ]; then rmdir -- "$LOCK_DIR" 2>/dev/null || true; fi' EXIT
physical_owned_dir "$LOCK_DIR" 'receiving lock'

# The initial preflight ran before the lock existed. Revalidate the exact
# preimage after taking the receiving boundary and before creating a backup.
regular_owned_file "$TARGET" 'installed maker under receiving lock' "$EXPECTED_MODE"
[ "$(sha256 "$TARGET")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'installed maker changed before receiving lock'
TARGET_DEVICE=$(stat -c '%d' -- "$TARGET")
TARGET_INODE=$(stat -c '%i' -- "$TARGET")
python3 -B "$ATOMIC_HELPER" copy "$TARGET" "$BACKUP_TMP" "$EXPECTED_UID" "$EXPECTED_MODE"
regular_owned_file "$BACKUP_TMP" 'backup temporary' "$EXPECTED_MODE"
[ "$(sha256 "$BACKUP_TMP")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'backup temporary bytes mismatch'
[ ! -e "$BACKUP" ] && [ ! -L "$BACKUP" ] || die 'backup path appeared during install; refusing to continue'
mv --no-clobber -- "$BACKUP_TMP" "$BACKUP"
[ ! -e "$BACKUP_TMP" ] || die 'backup path appeared during install; refusing to continue'
regular_owned_file "$BACKUP" 'backup' "$EXPECTED_MODE"
[ "$(sha256 "$BACKUP")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'backup preimage mismatch'

# Hold the receiving lock across the final identity check and rename. All
# approved receiving writers use this boundary; an uncoordinated writer is not
# an allowed manager route.
regular_owned_file "$TARGET" 'installed maker before replacement' "$EXPECTED_MODE"
[ "$(sha256 "$TARGET")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'installed maker changed before replacement'
CURRENT_DEVICE=$(stat -c '%d' -- "$TARGET")
CURRENT_INODE=$(stat -c '%i' -- "$TARGET")
[ "$CURRENT_DEVICE:$CURRENT_INODE" = "$TARGET_DEVICE:$TARGET_INODE" ] || die 'installed maker identity changed before replacement'
REPLACEMENT_TMP=$ORCH/bin/.make-child-venv.$STAMP.$$.replacement.tmp
python3 -B "$ATOMIC_HELPER" copy "$CANDIDATE" "$REPLACEMENT_TMP" "$EXPECTED_UID" "$EXPECTED_MODE"
regular_owned_file "$REPLACEMENT_TMP" 'replacement temporary' "$EXPECTED_MODE"
[ "$(sha256 "$REPLACEMENT_TMP")" = "$EXPECTED_CANDIDATE_SHA256" ] || die 'replacement temporary bytes mismatch'
python3 -B "$ATOMIC_HELPER" rename "$BIN_DIR" "$(basename -- "$TARGET")" "$(basename -- "$REPLACEMENT_TMP")" "$TARGET_DEVICE" "$TARGET_INODE" "$EXPECTED_UID" "$EXPECTED_MODE"

postcommit_regular_owned_file() {
  local path=$1 expected_mode=$2 info
  [ -f "$path" ] && [ ! -L "$path" ] || return 1
  info=$(stat -c '%h %u %a' -- "$path") || return 1
  [ "${info%% *}" = 1 ] || return 1
  info=${info#* }
  [ "${info%% *}" = "$EXPECTED_UID" ] || return 1
  [ "${info#* }" = "$expected_mode" ] || return 1
}

postcommit_readback() {
  postcommit_regular_owned_file "$TARGET" "$EXPECTED_MODE" || return 1
  [ "$(sha256 "$TARGET")" = "$EXPECTED_CANDIDATE_SHA256" ] || return 1
  [ "$(bytes "$TARGET")" = "$EXPECTED_CANDIDATE_BYTES" ] || return 1
  postcommit_regular_owned_file "$ORCH/bin/bench_store.py" 755 || return 1
  postcommit_regular_owned_file "$ORCH/bin/verify_dependency_seed.py" 755 || return 1
  [ "$(sha256 "$ORCH/bin/bench_store.py")" = "$EXPECTED_BENCH_STORE_SHA256" ] || return 1
  [ "$(sha256 "$ORCH/bin/verify_dependency_seed.py")" = "$EXPECTED_DEPENDENCY_HELPER_SHA256" ] || return 1
  cmp -- "$CANDIDATE" "$TARGET"
}

if ! postcommit_readback; then
  LOCK_HELD=0
  printf 'INSTALLED_BUT_UNVERIFIED: replacement committed; do not retry or use an alternate route\n' >&2
  exit 3
fi
LOCK_HELD=0
trap - EXIT
if ! rmdir -- "$LOCK_DIR"; then
  printf 'INSTALLED_BUT_UNVERIFIED: replacement committed; receiving lock cleanup failed; do not retry or use an alternate route\n' >&2
  exit 3
fi
printf 'PASS: candidate installed with CAS preimage, no-clobber backup, atomic replacement, and helper readback\n'

