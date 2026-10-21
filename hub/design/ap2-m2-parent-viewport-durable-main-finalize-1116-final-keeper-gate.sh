#!/bin/sh
set -eu

KEEPER=${APP_ROOT:?set APP_ROOT to the exact detached freeze checkout}
FINAL_HEAD=6707a30f14bf3a5ee19cb9e481b7dbd95b77522a
FINAL_TREE=6ff32d797f0e774b8574274a3494ce8755fa160c

HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-source-common.bound.sh
HELPER_SHA=2b3b67bfd29e76d66f05e7c473eff80b6bd9f9609b4dcba4bf2d4cd2dcac59b1
DRIVER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-run-parent-manual-drop-evidence.sh
DRIVER_SHA=a91bef93c84b1ae8cc2dcfaf9afcc29ce46f1878214fe2b9f8c67968843abe65
SOURCE_RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-viewport-durable-main-finalize-1116-normal014-parent-media-central.bound.sh
EVIDENCE_ROOT=${NORMAL014_RECORD_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-durable-main-finalize-1116/evidence}
RUN_ROOT_PARENT=${NORMAL014_RUN_ROOT_PARENT:-/tmp/tl-pv-parent}

MODE=${1:?usage: $0 preflight|run}
case "$MODE" in
  preflight|run) ;;
  *) echo "usage: $0 preflight|run" >&2; exit 2 ;;
esac

SERVICE_ROOT=$PWD
EVIDENCE_DIR=$EVIDENCE_ROOT/$MODE
NEGATIVE_DIR=$EVIDENCE_DIR/negatives
mkdir -p "$NEGATIVE_DIR"
chmod 700 "$EVIDENCE_ROOT" "$EVIDENCE_DIR" "$NEGATIVE_DIR"

check_captured_tree() {
  root=$1
  test "$(git -C "$root" show -s --format=%T HEAD)" = "$FINAL_TREE" || return 1
  test -z "$(git -C "$root" status --porcelain=v1 --untracked-files=all)" || return 1
}

check_keeper() {
  root=$1
  test "$(git -C "$root" rev-parse HEAD)" = "$FINAL_HEAD" || return 1
  test "$(git -C "$root" show -s --format=%T HEAD)" = "$FINAL_TREE" || return 1
  test -z "$(git -C "$root" status --porcelain=v1 --untracked-files=all)" || return 1
  test -f "$root/KEEP" || return 1
  test "$(readlink "$root/node_modules")" = /home/user/work/app/node_modules || return 1
}

check_bound_hashes() {
  helper=$1
  helper_sha=$2
  driver=$3
  driver_sha=$4
  printf 'bound helper observed=%s expected=%s\n' "$(sha256sum "$helper" | cut -d' ' -f1)" "$helper_sha"
  printf 'bound driver observed=%s expected=%s\n' "$(sha256sum "$driver" | cut -d' ' -f1)" "$driver_sha"
  test "$(sha256sum "$helper" | cut -d' ' -f1)" = "$helper_sha" || return 1
  test "$(sha256sum "$driver" | cut -d' ' -f1)" = "$driver_sha" || return 1
}

expected_failure() {
  name=$1
  shift
  log="$NEGATIVE_DIR/$name.log"
  if "$@" >"$log" 2>&1; then
    echo "expected refusal did not occur: $name" >&2
    return 1
  fi
  printf '%s status=refused\n' "$name" >>"$NEGATIVE_DIR/summary.txt"
}

check_captured_tree "$SERVICE_ROOT"
echo "captured service tree guard passed tree=$FINAL_TREE"
check_keeper "$KEEPER"
echo "protected keeper guard passed head=$FINAL_HEAD tree=$FINAL_TREE"
echo "observed helper=$(sha256sum "$HELPER" | cut -d' ' -f1) driver=$(sha256sum "$DRIVER" | cut -d' ' -f1)"
check_bound_hashes "$HELPER" "$HELPER_SHA" "$DRIVER" "$DRIVER_SHA"
echo "helper and driver hash guards passed helper=$HELPER_SHA driver=$DRIVER_SHA"

if [ "$MODE" = run ]; then
  cd "$KEEPER"
  NORMAL014_RECORD_DIR="$EVIDENCE_DIR" \
    exec sh "$DRIVER" run "$KEEPER"
fi

mkdir -p "$RUN_ROOT_PARENT"
RUN_ROOT=$(mktemp -d "$RUN_ROOT_PARENT/source-run.XXXXXX")
TMP_ROOT=$(mktemp -d "$RUN_ROOT_PARENT/tmp.XXXXXX")
trap 'status=$?; rm -rf -- "$RUN_ROOT" "$TMP_ROOT"; exit "$status"' EXIT

if env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  NORMAL014_USE_BASE_PYTHON=1 NORMAL014_RUN_ROOT="$RUN_ROOT" TMPDIR="$TMP_ROOT" \
  sh "$SOURCE_RUNNER" preflight "$KEEPER" >"$EVIDENCE_DIR/source-preflight.log" 2>&1; then
  printf '%s\n' 'source-preflight status=passed' >"$EVIDENCE_DIR/result.txt"
else
  status=$?
  printf 'source-preflight status=failed exit=%s\n' "$status" >"$EVIDENCE_DIR/result.txt"
  cat "$EVIDENCE_DIR/source-preflight.log"
  exit "$status"
fi
cat "$EVIDENCE_DIR/source-preflight.log"

: >"$NEGATIVE_DIR/summary.txt"
WRONG_CAPTURED_ROOT=/home/user/work/app
test "$(git -C "$WRONG_CAPTURED_ROOT" show -s --format=%T HEAD)" != "$FINAL_TREE"
expected_failure wrong-captured-tree check_captured_tree "$WRONG_CAPTURED_ROOT"
expected_failure wrong-keeper check_keeper "$WRONG_CAPTURED_ROOT"
expected_failure wrong-helper-hash check_bound_hashes "$HELPER" wrong "$DRIVER" "$DRIVER_SHA"
expected_failure wrong-argv sh "$DRIVER" unsupported

LIST_TMP=$(mktemp -d "$RUN_ROOT_PARENT/list-tmp.XXXXXX")
trap 'status=$?; rm -rf -- "$RUN_ROOT" "$TMP_ROOT" "$LIST_TMP"; exit "$status"' EXIT
(
  cd "$KEEPER"
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR="$LIST_TMP" \
    node node_modules/playwright/cli.js test \
      --config playwright.three-products.config.ts \
      --grep 'M2 real mounted manual video drop' --list
) >"$EVIDENCE_DIR/list.log" 2>&1
test "$(grep -Ec 'three-products\.spec\.ts:[0-9]+' "$EVIDENCE_DIR/list.log")" -eq 1
grep -F 'three-products.spec.ts:1410' "$EVIDENCE_DIR/list.log" >/dev/null
printf '%s\n' 'list status=passed collected=1 test=three-products.spec.ts:1410' >>"$EVIDENCE_DIR/result.txt"
cat "$EVIDENCE_DIR/list.log"

