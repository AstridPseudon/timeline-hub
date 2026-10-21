# App2 parent viewport: run-on-main handoff

Status: NOT READY for execution from this worker. The test source is prepared,
but the harness has not created the final commit, so the parent role SHA/tree
cannot be closed here.

## Source and frozen inputs

Current HOME before the harness commit:

```text
app_head=0cc2583aaf07e89190b9344b5ac82849d6279586
app_tree=320e74a93676c781e83885b86ec237b4a1465d80
app_source_file=tests/e2e/local/three-products.spec.ts
app_source_file_at_HOME=18fc9a5a1e81b1f76dfd6bfd14e30b09631b9585
pointer_ancestor=44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0
donor=9018c733c429f3ad176bebf26c6351fce0414da1
donor_spec_after_composition=e612c18cac2a651e855e75388498762f034dc63a
```

The `donor_spec_after_composition` value is the donor blob and is recorded as
an identity check, not as a proposed source commit. The working file is byte
identical to that donor file after composition.

Frozen R4 inputs, resolved from the named frozen branches:

```text
agent origin/codex/handover-timeline-r4-20261019-candidate-sdk        11caf1d9de291d76f491cf69f7942606b7471d7a
runtime origin/codex/handover-timeline-r4-20261019-candidate-runtime  31c7ac3a00f7a205f507bf5bd4d4625628d429bd
app origin/codex/handover-timeline-r4-20261019-candidate-app-qualified 8f0c2484463e9b666d184a744d52e252984e551a
composition origin/codex/handover-timeline-r4-20261019-candidate-composition c82eb7c459d0a41263954bf007071a6a0e8e0a6a
```

The current test graph remains the approved public13 graph: Node `v22.22.0`,
Vite `5.4.21`, Playwright `1.60.0`; locked graph package count `532`, binary
count `34`, Runtime artifact manifest count `76`, and Composition archive
member count `77`.

## What is being run

The original test title is unchanged:

```text
M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data
```

The row-local setup now waits for V1, both rendered calibration clips, and the
mounted wrapper; clicks the existing accessible `Zoom out timeline` control
once; then measures the same two anchors and asserts that the unchanged
`22.5`-second pointer is inside the wrapper. Main's five-second centered drop
therefore remains `22.5 - 5/2 = 20`, on V1 and after the seeded `15..18` clip.
No browser viewport, timeout, selector, production offset, helper, or expected
native value changed.

The strict refusal remains the original full body:

```json
{
  "code": "not_found",
  "message": "selected media is not a managed project generation/variant/object",
  "request_id": "<one-to-128-character-safe-id>"
}
```

The existing real File/DataTransfer drop, wrong-selection refusal, native
`clip.add-media`, exact lost-ACK retry, restart/recovery, undo, opaque fields,
order, source/epoch, ACK, raw/hold, and zero-legacy assertions all remain in
the same test. The file contains one pointer declaration and two drop-helper
calls; `wire.legacy` remains asserted throughout the original journey.

## Closed parent role fields

The harness must first commit this worktree and report the resulting 40-hex
commit and tree. Until then these fields are intentionally pending and this
packet must not be labelled READY:

```text
parent_role_sha=PENDING_HARNESS_FINAL_COMMIT
parent_role_tree=PENDING_HARNESS_FINAL_TREE
```

Exact remaining step: harness commit, then resolve both fields with
`git -C /home/user/work/app rev-parse HEAD` and
`git -C /home/user/work/app rev-parse HEAD^{tree}` (or the exact committed
main checkout used by the orchestrator), verify clean status, and data-bind
those values into the private gate copy described below. Do not hand-type
either value.

## Existing guarded command

Use the existing 0939 gate/driver/helper logic and one private data-bound copy
of its closed source values. Do not modify the shared helper or driver. The
private copy is disposable and must be trap-cleaned; durable evidence is kept
outside it. The gate must retain its existing zero-test refusal, title check,
wrong-tree refusal, helper/driver hash checks, source ancestry check, and
evidence-before-cleanup trap.

After the harness commit, bind only these data fields in that private copy:

```text
KEEPER=/home/user/work/app
FINAL_HEAD=<parent_role_sha>
FINAL_TREE=<parent_role_tree>
APP_ROOT_SHA=<parent_role_sha>
APP_ROOT_TREE=<parent_role_tree>
NORMAL014_PRIVATE_SPEC=/home/user/work/app/tests/e2e/local/three-products.spec.ts
```

The existing 0939 helper and driver must still hash to:

```text
normal014-source-common.sh  e081b0736e5c9341044d24cbda4f727dbf89f85b6300f8ec9e544c11dcd5992c
run-parent-manual-drop-evidence.sh  0c310d9e906dfbfab8202dd0f17edca9509ad8239150c50eb5a48cabfb478a0c
final-keeper-gate.sh  80f1b52230115134c58f2ae0d7e11394f9628b855f2083b743caccebc9eb39c9
```

Run from the committed App root with a short disposable root and an explicit,
sanitized environment. Replace only the angle-bracket fields after the
harness commit and use one fresh evidence directory:

```sh
set -eu
APP_ROOT=/home/user/work/app
RUN_ID=ap2-m2-parent-viewport-<parent_role_sha_short>
RUN_ROOT=/tmp/tl-pv-<parent_role_sha_short>
EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-current-main-packet-1110/evidence/$RUN_ID
BOUND_GATE=/tmp/tl-pv-<parent_role_sha_short>/final-keeper-gate.bound.sh
cd "$APP_ROOT"
env -i \
  PATH=/opt/node22/bin:/usr/bin:/bin \
  HOME=/home/user \
  NORMAL014_PROFILE=final95 \
  NORMAL014_APP_SOURCE=parent \
  NORMAL014_USE_BASE_PYTHON=1 \
  NORMAL014_PRIVATE_SPEC="$APP_ROOT/tests/e2e/local/three-products.spec.ts" \
  NORMAL014_RECORD_DIR="$EVIDENCE_ROOT" \
  NORMAL014_RUN_ROOT="$RUN_ROOT" \
  TMPDIR="$RUN_ROOT/tmp" \
  sh "$BOUND_GATE" run
```

The command is intentionally not run in this task. It is one actual only:
the bound driver must perform its aggregate preflight first, then one browser
actual under the existing nonblocking `/home/user/work/.app-m1-browser.lock`.
No retry or second actual is allowed after a new unexplained prerequisite.

## Preflight checklist before that one actual

Run all checks as one aggregate and stop on the first new unexplained failure.

- Source: exact 40-hex `parent_role_sha/tree`, clean root, `package.json`,
  `tests/e2e/local/three-products.spec.ts`, and existing `node_modules`
  resolving to `/home/user/work/app/node_modules`; no install or shared-file
  write. Verify ancestry from `44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0`.
- Frozen inputs: exact Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`,
  Runtime/producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, all 76 artifact
  bytes, schema digest, and locked public13 graph/archive hashes. Keep the
  listed R4 branch SHAs above as provenance only.
- Toolchain: `/opt/node22/bin/node` reports `v22.22.0`, Vite reports
  `5.4.21`, Playwright reports `1.60.0`, Chromium is executable under
  `/opt/pw-browsers`, `/home/user/work/venv-app2-native/bin/python` is
  executable, and `ffmpeg`/`ffprobe` are available. Do not reinstall.
- Graph: graph realpath is not a private overlay destination; the actual
  runner creates its private graph only under its disposable run root. Verify
  532 packages/34 bins, Composition archive SHA
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`, and
  the 76/77 artifact counts.
- Argv/list: use exactly
  `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts:1410 --list`
  (private `TMPDIR`, no browser launch); require exactly one listed test and
  the exact title. Also exercise the existing zero-test refusal and wrong-argv
  refusal controls. Do not add a wrapper or a second selector.
- Socket roots: use the short `/tmp/tl-pv-<short>/` root for disposable run,
  TMP, Vite, Playwright, npm, and Runtime socket/discovery material. Check
  `realpath` for every root and enforce the Linux Unix-socket path limit before
  starting any service; the long durable evidence path is never a socket root.
- Remotion: this is renderer-independent save coverage. Under `env -i`, assert
  no `REMOTION_*`, renderer, browser-debug, credential, or inherited runtime
  variables are present; no Remotion process may be started. The child env is
  limited to the existing runner's `ASTRID_CHECKOUT`, `ASTRID_PYTHON`,
  `ASTRID_RUNTIME_CHECKOUT`, `ASTRID_RUNTIME_PYTHON`, bundle heads,
  `PLAYWRIGHT_BROWSERS_PATH`, private cache/output paths, `TMPDIR`,
  `PYTHONDONTWRITEBYTECODE`, and `PYTHONNOUSERSITE`.
- Resources: `flock -n /home/user/work/.app-m1-browser.lock -c :` must pass;
  keep at most one normal disposable App copy; require at least 10 GiB free
  on both `/tmp` and `/home/user/work` (`df -Pk`); do not touch another
  worker's root or shared dependencies.
- Retention: reserve a fresh evidence directory, prove trace/error-context/
  bounded summary/runner log/source identity can be copied before disposable
  cleanup, preserve earlier 31285/25174 packets byte-for-byte, and record
  source/helper/driver hashes. Cleanup must be trap-driven and happen only
  after evidence copy.
- Credentials: require the existing credential-file checks and ensure no
  credential value is in argv, logs, browser evidence, or the sanitized
  summary. The manual-drop test's page-wide token sniff must remain active.

## Main portability failures to resolve together

These are known handoff blockers, not reasons to alter the test:

1. The harness final commit/tree is not available in this worker, so the
   literal closed parent role is pending.
2. The frozen 0939 gate/helper currently closes App `7419eccbbbaaed09d520845366255a9a87af5679` / tree
   `971e8ff779a2e6d3df651a30d37bb8bc7e285a83`; those old App identity fields
   and the old keeper marker must be data-bound in one private gate copy to
   the new committed HOME source. The shared final95 helper remains unchanged.
3. The existing source identity record also names the old parent pin and must
   be updated as data only; all Agent/Runtime/producer/profile/graph/argv/
   retention guards stay byte-identical.
4. The actual service snapshot must use the committed HOME tree and the
   private test spec; a stale synthetic service tree or the old keeper is a
   refusal, not a test result.

If any of these fields cannot be closed together, stop and report the exact
field; do not run a partial actual. A successful actual must reach the strict
404, native ADD, exact retry, restart, undo, and zero-legacy assertions before
the parent role is considered qualified.
