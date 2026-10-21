# AP2 M2 selected copy-failure explicit-return correction — 0948

## Result

Applied the minimal owned-runner correction for the 0941 HOLD. The immutable
0927 runner was copied byte-for-byte before editing:

```text
source-0927-run-owned-selected-final95.sh
SHA-256 ff79ff6f32d248989b6227790cebbe34c1ffd4711b8b3dc90c0708fe6e7a8c8e

run-owned-selected-final95.sh
SHA-256 96629aa9dbb00c6bb7ad23591a98229e56e6a6c0184a2ac254e2b825174707c9
```

Artifacts are under:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts/
```

Only the owned runner artifact changed. No App source, spec, helper, pin,
selector, budget, DTO, launcher, or shared dependency changed. The App
worktree is clean.

## Exact reverse diff

This is the complete `diff -u run-owned-selected-final95.sh
source-0927-run-owned-selected-final95.sh`; there are 34 changed lines (17
removed and 17 added), all in retention failure handling:

```diff
@@ -114,10 +114,10 @@
   source=$1
   destination=$2
   limit_bytes=$3
-  test -f "$source" || return 1
-  size=$(wc -c <"$source") || return 1
-  test "$size" -le "$limit_bytes" || return 1
-  cp -p -- "$source" "$destination" || return 1
+  test -f "$source"
+  size=$(wc -c <"$source")
+  test "$size" -le "$limit_bytes"
+  cp -p -- "$source" "$destination"
 }

@@ -168,7 +168,7 @@
     printf 'trace_retained=%s\n' "${trace_retained:-false}"
     printf 'child_command=npm run test:e2e:three-products -- --grep %s\n' "$TEST_TITLE"
     printf 'run_root=%s\n' "$run_root"
-  } >"$durable_root/identity.txt" || return 1
+  } >"$durable_root/identity.txt"
 }

@@ -190,14 +190,14 @@
   case "$durable_parent" in
     "$run_root"/*) echo 'selected failure evidence root must be outside RUN_ROOT' >&2; return 1 ;;
   esac
-  mkdir "$durable_root" || return 1
+  mkdir "$durable_root"
   durable_root=$(realpath "$durable_root")
   test "$durable_root" != "$run_root"
   case "$durable_root" in
     "$run_root"/*) echo 'selected failure evidence root resolved inside RUN_ROOT' >&2; return 1 ;;
   esac
-  chmod 700 "$durable_root" || return 1
-  copy_bounded "$child_log" "$durable_root/child.log" 10485760 || return 1
+  chmod 700 "$durable_root"
+  copy_bounded "$child_log" "$durable_root/child.log" 10485760

@@ -218,30 +218,28 @@
     phase=BODY
   fi
   if test -n "$trace" || test -n "$context" || test -n "$dom"; then
-    mkdir "$durable_root/browser-output" || return 1
+    mkdir "$durable_root/browser-output"
   fi
   if test -n "$dom"; then
-    copy_bounded "$dom" "$durable_root/browser-output/dom.html" 5242880 || return 1
+    copy_bounded "$dom" "$durable_root/browser-output/dom.html" 5242880
     dom_retained=true
   fi
   if test -n "$context"; then
-    copy_bounded "$context" "$durable_root/browser-output/error-context.md" 1048576 || return 1
+    copy_bounded "$context" "$durable_root/browser-output/error-context.md" 1048576
     context_retained=true
   fi
   if test -n "$trace"; then
-    copy_bounded "$trace" "$durable_root/browser-output/trace.zip" 52428800 || return 1
+    copy_bounded "$trace" "$durable_root/browser-output/trace.zip" 52428800
     trace_retained=true
   fi
-  write_failure_identity "$durable_root" "$run_root" "$status" "$phase" "$output_dir" || return 1
-  if ! (
+  write_failure_identity "$durable_root" "$run_root" "$status" "$phase" "$output_dir"
+  (
     cd "$durable_root"
     find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | while IFS= read -r path; do
       sha256sum -- "$path"
     done
-  ) >"$durable_root/SHA256SUMS"; then
-    return 1
-  fi
-  test -s "$durable_root/SHA256SUMS" || return 1
+  ) >"$durable_root/SHA256SUMS"
+  test -s "$durable_root/SHA256SUMS"
 }
```

The forward correction adds explicit `|| return 1` checks to `copy_bounded`
file/size/limit/cp operations, both newly-created directories, child-log and
each available artifact copy, identity write, manifest generation, and
nonempty-manifest verification. Each `*_retained=true` remains after its
successful copy. Independent available-artifact retention and the no-DOM
behavior remain unchanged.

## RED: immutable 0927 runner

The private test shim failed only the `error-context.md` destination; it did
not alter the runner, App, or shared dependencies. The existing real
run-mode launch-only seam was used with the existing trace/context/no-DOM
fixture; no direct helper call was used.

Command:

```sh
ART=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts
PATH="$ART/bin:$PATH" NORMAL014_USE_BASE_PYTHON=1 \
APP_KEEPER_ROOT=/home/user/work/wt/app-pin-a50ca4a0 \
SELECTED_FINAL95_MODE=run \
SELECTED_FINAL95_LAUNCH_STUB="$ART/fixture-failure-trace-context-only.sh" \
SELECTED_FINAL95_DURABLE_ROOT="$ART/red-old-copy-failure-evidence" \
sh "$ART/source-0927-run-owned-selected-final95.sh" "$PWD"
```

Observed `RED_COPY_FAILURE_RC=17`. The runner printed the deterministic copy
failure, but the old bare copy continued under the `if`-condition context.
It falsely wrote `identity.txt` with
`error_context_retained=true` even though `error-context.md` was absent, then
wrote a manifest that passed `sha256sum -c SHA256SUMS`. The packet retained
`trace.zip`, `child.log`, and `identity.txt`; this is the expected negative
behavior that establishes RED.

## GREEN: corrected runner

Command, through the same launch-only seam and same deterministic copy
failure:

```sh
ART=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts
PATH="$ART/bin:$PATH" NORMAL014_USE_BASE_PYTHON=1 \
APP_KEEPER_ROOT=/home/user/work/wt/app-pin-a50ca4a0 \
SELECTED_FINAL95_MODE=run \
SELECTED_FINAL95_LAUNCH_STUB="$ART/fixture-failure-trace-context-only.sh" \
SELECTED_FINAL95_DURABLE_ROOT="$ART/green-new-copy-failure-evidence" \
sh "$ART/run-owned-selected-final95.sh" "$PWD"
```

Observed `GREEN_COPY_FAILURE_RC=1`, with visible:

```text
deterministic test copy failure: error-context.md
selected failure retention FAILED status=1 run_root=/tmp/w-5aec29224b/ap2-m2-selected-final95-owned.E14ddg
```

The child fixture's original status is 17 (its retained `child.log` records
the fixture's original nonzero exit); the existing cleanup contract returns 1
when retention itself fails. The durable failure root contains only
`child.log`; `identity.txt` and `SHA256SUMS` are absent, so no false retained
flag or verified manifest exists. The printed temporary `RUN_ROOT` was absent
after exit. No browser, build, daemon, socket, selected actual, or service
submission ran.

## Unchanged success control

Using the same corrected runner and fixture without the failing `cp` shim:

```sh
ART=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts
NORMAL014_USE_BASE_PYTHON=1 APP_KEEPER_ROOT=/home/user/work/wt/app-pin-a50ca4a0 \
SELECTED_FINAL95_MODE=run \
SELECTED_FINAL95_LAUNCH_STUB="$ART/fixture-failure-trace-context-only.sh" \
SELECTED_FINAL95_DURABLE_ROOT="$ART/green-new-success-control" \
sh "$ART/run-owned-selected-final95.sh" "$PWD"
```

Observed `GREEN_SUCCESS_CONTROL_RC=17`. `sha256sum -c SHA256SUMS` passed for
the retained trace, error context, child log, and identity. Identity recorded
`child_status=17`, `dom_present=false`, `dom_retained=false`,
`error_context_retained=true`, and `trace_retained=true`; its `run_root` was
absent after exit. `BODY` and `body_started` here mean launch/output phase
markers only; they are not evidence that P1/P2, page/DOM setup, selected
behavior, or the full test body executed.

Success-control packet hashes:

```text
error-context.md d27b851969fe1e1e39c93c8a5da46095f747c1a6a934562d50619caa0e83d0c0
trace.zip        0efb3d7a43af40edf8d47cefe23876939ea22b0bbde9c847819562e98f9eafd2
child.log        356db59611b56b8da4226db632ad14922a6b58409bf9d42f06b019407445c724
identity.txt     88f4de0f39e5a6e9369727c89b82e1b600056aca304dd54a44de66baa20e3143
SHA256SUMS       9cc3f8a0eb01809521162bf5cfdc09cf4c98547ba7fc8db8a04c8080f02ca866
```

## Checks

```sh
sh -n "$ART/source-0927-run-owned-selected-final95.sh"
# PASS
sh -n "$ART/run-owned-selected-final95.sh"
# PASS
```

Independent final-hunk negative-control command:

```sh
ART=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-copy-failure-explicit-return-0948/artifacts
OLD="$ART/source-0927-run-owned-selected-final95.sh"
NEW="$ART/run-owned-selected-final95.sh"
for line in \
  '  test -f "$source"' \
  '  size=$(wc -c <"$source")' \
  '  test "$size" -le "$limit_bytes"' \
  '  cp -p -- "$source" "$destination"' \
  '  copy_bounded "$child_log" "$durable_root/child.log" 10485760'; do
  grep -Fxq "$line" "$OLD" && ! grep -Fxq "$line" "$NEW"
done
```

Result: PASS for all five removed unguarded lines; required guarded lines
were also present. The worktree check returned clean. No full suite or central
test-service submission was requested because the brief explicitly forbids
them; no install or shared-dependency write was performed.

## Decisions and status

- Kept independent trace/context/DOM copying and no standalone-DOM
  requirement from 0927.
- Used explicit returns because the retention function is evaluated as an
  `if` condition and therefore cannot rely on `set -e`.
- Kept the original child status and EXIT cleanup logic; retention failure
  still returns the existing wrapper status 1 while the child remains 17.
- HOME fixture phase-order correction remains separate and no selected actual
  was run.

No blockers.
