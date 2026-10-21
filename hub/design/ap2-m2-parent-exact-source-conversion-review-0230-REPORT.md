# AP2 M2 parent exact source-conversion review

## Verdict

**HOLD. Do not approve or run the mounted gate yet.** The source worker did not
produce a committed final output during this review. Its provisional worktree
was dirty, had no `commit-msg`, `DONE`, or `BLOCKED` marker, and was removed by
the time this report was finalized. The only inspectable source commit remains
the earlier `7e85...` commit below; no final source/tree identity was available.

The prior committed state was App `7e85d89120227f336a2e8dbf8e0ea44d98311da0`
with tree `20bf7411c9ebbcbbb7a3fc10846e66cb0573b0f3`. That commit only updated
the existing evidence-driver pins/tree guard and still had two review defects:

1. The mounted negative asserted `expect([404, 409]).toContain(...)` and did
   not check the semantic body. The required final95 assertion is exactly HTTP
   404 and:

   ```json
   {"code":"not_found","message":"selected media is not a managed project generation/variant/object"}
   ```

2. It claimed frozen App commit `25155ccb22728780a3ecd6379a929cad75cc1400`
   / tree `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`, although the committed
   driver change itself made a new consumer tree (`20bf...`).

The source worker's provisional dirty edits contained the required exact
404/body assertion and added `expected_app_commit`, ancestry, and clean-state
checks. However, that provisional driver contained literal
`REPLACE_AFTER_COMMIT_TREE` and `REPLACE_AFTER_COMMIT_SHA` placeholders. Do not
fill these with a guessed hash: putting a commit/tree identity into the same
file whose contents determine that tree is self-referential. After the worker
is harness-committed, HOME must finalize a non-self-referential source
identity mechanism and rerun the source preflight. The final guard must name
the actual corrected consumer source/tree, not silently retain `25155/972d` or
accept an arbitrary override.

## Cohort and source controls

The closed final95 selectors and frozen tuple are correct in the existing
shared source helper:

- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime and producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- App pin `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`.
- Public13 archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Runtime artifact `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
  manifest `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
  76 entries, schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

The helper keeps exact detached Agent/Runtime/producer checkouts, verifies
artifact/schema/import collection, locked public13 graph, vendor-lock bytes,
postflight build/collection, and rejects unsupported profile/source selectors.
No arbitrary source override was found.

## Existing driver and retained behavior

The correct existing driver remains:

```text
tests/e2e/local/support/run-parent-manual-drop-evidence.sh
```

It selects the existing Playwright case:

```text
M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data
```

The original valid ADD path and its five-field media tuple, imported-entry
identity, parent `clip.add-media`, no `afterClipId`/remove/replace fields,
lost-ACK, dependent edit, reload, Runtime restart, exact retry key/body/
receipt, guarded undo, raw/opaque preservation, duplicate prevention, and
`wire.legacy === []` assertions remain in the candidate spec. No product code,
timeout, retry, wrapper, or caller was changed.

Live caller chain reviewed: `handleFileDrop` → `dispatchTimelineDrop` →
`useTimelineState`/`parentMediaCommands` → `useAssetManagement` native
`commands.addClip` → the existing commit-session/outbox path. Relevant files
remain `external-drop-utils.ts`, `useExternalDrop.ts`, `useAssetManagement.ts`,
`useTimelineState.ts`, `useTimelineCommandsService.ts`, and the existing
three-products driver.

## Checks run

Against the prior committed `7e85...` tree:

- `node node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts` — PASS.
- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts` — PASS, 1 test collected.
- `git diff --check 25155ccb2 HEAD` — PASS.
- `sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe` — PASS.
- `env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh preflight /home/user/work/wt/ap2-m2-parent-exact-negative-source-finish-0230` — FAIL before source preparation: the guard saw App tree `20bf7411...` but required frozen tree `972d2ed2...`. This confirms the stale-tree defect; no browser/socket was started.

The source worker's provisional dirty edits were inspected read-only after
that failure. No browser, localhost/socket, full suite, actual gate, product
code, dependency install, or new wrapper was run.

## Next step

Wait for the source worker's harness commit. Then HOME should finalize the
source identity without a self-referential commit/tree hash, rerun the existing
source-only preflight and targeted collection/lint checks, and only then hand
off the exact committed source/tree plus the existing driver command for the
single central mounted gate. No App writer deletion or qualification is
supported by this review.
