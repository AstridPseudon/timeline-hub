# App2 M2 parent mounted result — one action 0516

## Decision

HOLD. The only consumed result, `ap2-m2-parent-approved-one-mounted-case-0514`, did not run the mounted actual. Its first boundary was the independent custody review: both literal suite rows lacked the required SHA-256 pin for the external gate wrapper. This is a preflight/custody blocker, not an App behavior failure. No deletion or regression fix is justified.

The required wrapper digest is:

`2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`

The parent result explicitly reports no browser, full suite, actual, source edit, install, pin change, or second attempt. Therefore there are zero mounted behavior assertions to qualify and no fallback writer is proven dead by this case.

## Preserved proof and source identity

- Consumed report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-approved-one-mounted-case-0514/report.md`
- Source keeper: `/home/user/work/wt/ap2-m2-parent-complete-current-proof-source-0455`
- App HEAD/tree: `a304dce02a185a4774ff514d5aa451c9702aa46f` / `a3c82aa91f1336b86491191acf857d88c56179b2`, clean
- Exact test: `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`
- Test source: `tests/e2e/local/three-products.spec.ts:1440-1635`
- Central source-only preflight: `PASS`, exit 0; 76 artifacts verified, all four negative controls refused, exactly one test collected at `three-products.spec.ts:1440`
- Parent body inventory: 201 source lines and 57 `expect` call sites, including wrong-selection refusal (`404/409`), raw/opaque preservation, ordering, lost acknowledgement, reload, restart, exact body/key retry, guarded undo, and `wire.legacy === []` at lines 1618 and 1632.

The frozen proof's live path is unchanged:

`onTimelineDrop` → `useExternalDrop.ts:62,630` → `external-drop-utils.ts:300` → `useAssetManagement.ts:278` → native `commands.addClip` at `useAssetManagement.ts:303` → commit-session/outbox.

No live callers changed. Other parent forms (append, replace, after-anchor, and SWAP) remain unqualified as required by the plan; no broad parent retirement was attempted.

## Verification

Read-only checks performed in this worker:

- `git status --short --branch` — clean on `tl/ap2-m2-parent-mounted-result-one-action-0516`
- `git diff --check` — passed
- Exact source/assertion inspection with `nl -ba`/`sed` — completed; no product files changed

No new actual, browser, full suite, or unchanged audit was run. The parent central result and its custody HOLD are the only execution evidence used.

## Handoff

Smallest next step is outside this worker's authority: add the literal wrapper digest check to both registered 0508 preflight/actual commands, rerun only the approved source-only preflight, and obtain fresh custody approval. Do not run the mounted actual until both custody prerequisites approve.

Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-mounted-result-one-action-0516/commit-msg`

DONE marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-mounted-result-one-action-0516/DONE`
