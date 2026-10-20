# normal014 runner temp hygiene

## Result

Fixed the three owned normal014 harness files:

- `normal014-source-common.sh`
  - Added the shared per-run lifecycle helper.
  - Default roots are created with `mktemp -d` below the inherited
    `${TMPDIR:-/tmp}`; the inherited parent is never removed.
  - The `EXIT` trap is installed immediately after root creation, with HUP,
    INT, and TERM handlers that clean the exact owned root and re-raise the
    signal.
  - `NORMAL014_KEEP_TEMP=1` still retains evidence.
  - An explicitly supplied `NORMAL014_RUN_ROOT` remains caller-owned and is
    not removed; this avoids deleting retained or externally prepared evidence.
  - Private child `TMPDIR` is rooted at `$run_root/tmp`.
- `normal014-app-central.sh`
  - Uses the common lifecycle and private `TMPDIR` setup.
  - Replaced the final `exec flock ...` with a status-preserving conditional
    invocation so the shell `EXIT` trap runs after the browser command.
- `normal014-parent-media-central.sh`
  - Uses the common lifecycle and private `TMPDIR` setup.
  - Replaced the final `exec pytest ...` with the same status-preserving
    conditional invocation so failures retain their original status while the
    root is cleaned.

No source, authority, lock, generated-byte, artifact, schema, or marker guard
was removed or changed. The existing browser lock remains in place.

## Evidence

All commands below were run from the assigned App worktree. No exact normal014
runner was executing when inspected (`pgrep -af
'normal014-(app|parent-media)-central\\.sh|normal014-app-central\\.sh|normal014-parent-media-central\\.sh'` returned no match).

- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh` — PASS.
- Tiny fake-command lifecycle fixture using the sourced common helper — PASS:
  - success exit: generated App root was below the supplied `TMPDIR`, then
    removed;
  - exit status 23: generated parent-media root was removed and status 23 was
    preserved;
  - inherited `TMPDIR` parent remained after both runs;
  - SIGTERM fixture: exact root was removed and status 143 was preserved.

The success/error fixture used these command shapes (with the full path shown
to make the evidence reproducible):

```sh
source_common=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
fixture=$(mktemp -d /tmp/normal014-runner-fake-command.XXXXXX)
success_root=$(TMPDIR="$fixture" sh -c '. "$1"; normal014_start_run timeline-normal014-app; root=$run_root; case "$root" in "$normal014_tmp_parent"/timeline-normal014-app.*) ;; *) exit 90;; esac; if sh -c "exit 0"; then status=0; else status=$?; fi; test "$status" -eq 0; printf "%s\\n" "$root"; exit "$status"' sh "$source_common")
test ! -e "$success_root"
if error_root=$(TMPDIR="$fixture" sh -c '. "$1"; normal014_start_run timeline-normal014-parent; root=$run_root; test -d "$root"; if sh -c "exit 23"; then status=0; else status=$?; fi; printf "%s\\n" "$root"; exit "$status"' sh "$source_common"); then exit 91; else error_status=$?; fi
test "$error_status" -eq 23
test ! -e "$error_root"
test -d "$fixture"
rmdir "$fixture"
```

The signal check used the same sourced helper with `kill -TERM "$$"`; it
returned 143, removed the generated root, and left the inherited parent.
- Static guard audit — PASS: exact Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`,
  Runtime `202074110717146fc7f08af2306a8dd7f695b0b1`, producer
  `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, 75-artifact manifest,
  schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  d05e marker, generated-byte checks, and `/home/user/work/.app-m1-browser.lock`
  checks remain present. No hard-coded normal014 `mktemp` path or final `exec`
  remains.
- `git status --short --branch` — PASS: assigned App worktree clean; these
  harnesses are the allowed external design files.

## Not run / blocked

No real normal014 preflight, browser, localhost/socket, native, Runtime, full,
or central test-service run was made. The task explicitly limited validation to
shell syntax and the tiny fake-command lifecycle fixture. No old `/tmp` copy
was inspected for deletion or removed, and no shared dependency, graph, venv,
lock, or product/API file was touched.

## Next step

The manager should review the flat harness diff and run the normal central
qualification only when the suite lease is available. Its run will now clean
its own generated root on success, failure, or termination while preserving
`NORMAL014_KEEP_TEMP=1` evidence.
