#!/bin/bash
# Manager-only live installer. Do not run until the receiving note says the
# sole Agent E2E has PASSed and the independent result review is complete.
set -euo pipefail

die() {
  printf 'REFUSED: %s\n' "$1" >&2
  exit 2
}

: "${ORCH:?set ORCH to the approved orchestration root}"
: "${SOURCE_CHECKOUT:?set SOURCE_CHECKOUT to the reviewed Composition checkout}"

SOURCE_COMMIT=09ed4999741b822fba7e8b3033ca28db6bcf8fa1
SOURCE_REL=ops-child-custody/make-child-venv
TARGET=$ORCH/bin/make-child-venv
BACKUP_DIR=$ORCH/backups
EXPECTED_CANDIDATE_SHA256=c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e
EXPECTED_CANDIDATE_BYTES=69516
EXPECTED_PREIMAGE_SHA256=0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39
EXPECTED_PREIMAGE_BYTES=68351
EXPECTED_MODE=755
EXPECTED_BENCH_STORE_SHA256=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2
EXPECTED_DEPENDENCY_HELPER_SHA256=116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2
EXPECTED_UID=$(id -u)

case "$ORCH:$SOURCE_CHECKOUT" in
  /*:/*) ;;
  *) die 'ORCH and SOURCE_CHECKOUT must be absolute' ;;
esac
[ "$ORCH" = "$(readlink -e -- "$ORCH" 2>/dev/null)" ] || die 'ORCH must be a physical directory'
[ "$SOURCE_CHECKOUT" = "$(readlink -e -- "$SOURCE_CHECKOUT" 2>/dev/null)" ] || die 'source checkout must be physical'
[ -d "$BACKUP_DIR" ] || die 'backup directory is missing'

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
PRIVATE_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/ops-inventory-install.XXXXXX")
git -C "$SOURCE_CHECKOUT" archive --format=tar "$SOURCE_COMMIT" "$SOURCE_REL" | tar -x -C "$PRIVATE_ROOT"
CANDIDATE=$PRIVATE_ROOT/$SOURCE_REL
regular_owned_file "$CANDIDATE" 'extracted candidate' "$EXPECTED_MODE"
[ "$(sha256 "$CANDIDATE")" = "$EXPECTED_CANDIDATE_SHA256" ] || die 'candidate hash mismatch'
[ "$(bytes "$CANDIDATE")" = "$EXPECTED_CANDIDATE_BYTES" ] || die 'candidate byte count mismatch'

STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP=$BACKUP_DIR/make-child-venv.$STAMP.bak
[ ! -e "$BACKUP" ] && [ ! -L "$BACKUP" ] || die 'backup path already exists; refusing to clobber'
BACKUP_TMP=$BACKUP_DIR/.make-child-venv.$STAMP.$$.backup.tmp
[ ! -e "$BACKUP_TMP" ] && [ ! -L "$BACKUP_TMP" ] || die 'backup temporary path already exists'
cp --preserve=mode,ownership -- "$TARGET" "$BACKUP_TMP"
regular_owned_file "$BACKUP_TMP" 'backup temporary' "$EXPECTED_MODE"
[ "$(sha256 "$BACKUP_TMP")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'backup temporary bytes mismatch'
mv -n -- "$BACKUP_TMP" "$BACKUP"
[ ! -e "$BACKUP_TMP" ] || die 'backup path appeared during install; refusing to continue'
regular_owned_file "$BACKUP" 'backup' "$EXPECTED_MODE"
[ "$(sha256 "$BACKUP")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'backup preimage mismatch'

# Recheck the CAS immediately before replacement. The replacement is a single
# same-directory rename; no alternate route or in-place write is permitted.
regular_owned_file "$TARGET" 'installed maker before replacement' "$EXPECTED_MODE"
[ "$(sha256 "$TARGET")" = "$EXPECTED_PREIMAGE_SHA256" ] || die 'installed maker changed before replacement'
REPLACEMENT_TMP=$ORCH/bin/.make-child-venv.$STAMP.$$.replacement.tmp
[ ! -e "$REPLACEMENT_TMP" ] && [ ! -L "$REPLACEMENT_TMP" ] || die 'replacement temporary path already exists'
cp --preserve=mode,ownership -- "$CANDIDATE" "$REPLACEMENT_TMP"
regular_owned_file "$REPLACEMENT_TMP" 'replacement temporary' "$EXPECTED_MODE"
[ "$(sha256 "$REPLACEMENT_TMP")" = "$EXPECTED_CANDIDATE_SHA256" ] || die 'replacement temporary bytes mismatch'
mv -T -- "$REPLACEMENT_TMP" "$TARGET"

regular_owned_file "$TARGET" 'installed maker readback' "$EXPECTED_MODE"
[ "$(sha256 "$TARGET")" = "$EXPECTED_CANDIDATE_SHA256" ] || die 'installed maker readback hash mismatch'
[ "$(bytes "$TARGET")" = "$EXPECTED_CANDIDATE_BYTES" ] || die 'installed maker readback byte count mismatch'
[ "$(sha256 "$ORCH/bin/bench_store.py")" = "$EXPECTED_BENCH_STORE_SHA256" ] || die 'Store helper changed'
[ "$(sha256 "$ORCH/bin/verify_dependency_seed.py")" = "$EXPECTED_DEPENDENCY_HELPER_SHA256" ] || die 'dependency helper changed'
cmp -- "$CANDIDATE" "$TARGET"
printf 'PASS: candidate installed with CAS preimage, no-clobber backup, atomic replacement, and helper readback\n'
