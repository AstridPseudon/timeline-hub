# AP2 M2 selected seed-order custody review

## Decision

**APPROVE for one real selected-P1 gate.** The reviewed source is
`24165cb37b46a5c1a6676bd646d01f18e9552ee9`, compared with its direct parent
`eee191c1fe5c5bf2625ab640f17923ddabaab000`. The review is limited to the new
seed-order/provenance hunk requested by the task.

## Review findings

- `DirectHarness.seedSelectedParamDev()` now publishes the unchanged raw
  `compositionPublication` draft at lines 646–661, before
  `enableTimelineAuthoring(python)` at line 665. The restart still uses the
  existing `--authoring-profile astrid` path; no profile-at-save or route-guard
  disable was added.
- The initial carrier remains the original two clips, config/tracks, and media
  registry. It contains only `elementRef: { id, kind, revision: 'draft-1' }`:
  no P1 descriptor, `packId`, forged history, or synthetic pin is present.
  The native Agent `update-element` call, exact accepted-history assertion for
  `['clip.set-element', 'clip.set-params']`, P1 document-pin resolution, and all
  downstream P2/refusal/retry/reload/undo assertions are unchanged.
- After the restart, the selected credential is provisioned through the
  current `this.runtimeUrl`; `selectedParamCliEnv` then sets the complete
  endpoint/credential/realm/actor evaluation quartet from the current
  Runtime, current realm, selected actor, and credential-file path. The
  existing `0600` file write and `stop()` cleanup are unchanged. Browser/Door
  transport remains product-credential based and unchanged.
- Changed test-helper export: `selectedParamCliEnv` now requires the target
  `{ runtimeUrl, realmId }`. Its live callers are
  `tests/e2e/local/support/harness.ts:670` and
  `tests/e2e/local/support/selected-param-credential.test.ts:15,59`. No public
  product export or product activation changed; the candidate commit touches
  only `tests/e2e/local/support/harness.ts`.
- Frozen compatibility is exact: Agent `8130a401…` tree
  `236c3e57e0265c52b81ba8085de3193026176bff`; Runtime `2c4ac180…` tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`. Their source contracts match
  the file-backed credential and explicit evaluation quartet used here.

## Evidence

Independent read-only checks:

- `git diff --check eee191c1fe5c5bf2625ab640f17923ddabaab000..24165cb37` — passed.
- Candidate commit path check — one modified path, `tests/e2e/local/support/harness.ts`.
- Frozen Agent/Runtime commit-tree checks — passed with the exact trees above.

The candidate handoff records these targeted results (not rerun here because
this task forbids source edits, browser/socket execution, request-test, and
full suites):

- `node --import tsx tests/e2e/local/support/selected-param-credential.test.ts` — 3 passed.
- Targeted Vitest lane — 6 files, 71 passed.
- Targeted ESLint on the harness, credential control, and selected journey — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- Playwright `--list` for `three-products.selected-param-dev.spec.ts` — exactly 1 test collected.

The real browser/live selected P1/P2 journey is not claimed as verified by
this review. Recommended next step: run the single central selected gate once
against the frozen 8130/2c4 tuple.
