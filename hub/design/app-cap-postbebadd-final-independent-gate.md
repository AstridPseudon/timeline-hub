# App cap postbebadd final independent gate

Decision: **HOLD — narrow Viewing peer review required for one changed consumer semantic.**

## Source identity and applicability

- Original reviewed candidate: commit `6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214`, tree `32dc0de053ffb98d718077a111994181ae03ea15`, based on current-root `0d5009e18bee8e29f894dabf5db501a0fcea750f`.
- The candidate’s serializer repair/join is commit `dca891972840f502c974fbf3c3b1d585855842c1`, a merge of candidate `6b7afe3ad` and parent `c57dcc26162642f503532f143ceb96bb185273aa`.
- Current composed root is `b0efbffae569a8af11b2ebf1998dc5174c184b9b` (`c57dcc261` plus the exact App2 commits `bf485152`/`3ba595693`).
- `c57→dca` is exactly the reviewed 30-file cap delta: 22 producer files plus 11 corrected consumer files, with three shared paths. The private materialization applies that patch to `b0efbffae`; comparison with the candidate differs in exactly the five App2 typing files and no others.
- Private source archive: `workers/app-m3-cap-postbebadd-final-independent-gate/app-cap-postbebadd-b0efbffae-source-v1.tar`, SHA-256 `3b57139b8b91973e2a12fd14350b5bceb074c6e68d7f9be8aa197d6ff1739159`. Patch SHA-256: `0db451f20004a0035753c7f04317787e4ff07c33678c6b19d5fe958dae0a853f`.
- All 30 materialized cap paths hash byte-for-byte to `dca891972`; all five App2 paths hash byte-for-byte to `b0efbffae`. No tracked worktree edits were made.

The joined source retains native `None`, Generic/Element, and label `INPUT` references, corrected media carrier behavior, and existing source/PCM guards. The producer is present across bootstrap, local preview, recovery, and accepted projection. The scalar remains a derived render hint; it is not a Runtime/command/timeline-data authored field.

## Review findings

The serializer repair closes the prior HOLD. With a verified raw graph it removes only `storedOccurrenceDurationMs`, restores raw same-name `canonical`/`canonicalTiming` values, and preserves null, opaque keys, own `__proto__`, and key ordering. With no verified raw basis, `serializeForDisk`, `serializeResolvedTimelineEdit`, and projected serialization refuse visibly without mutating the draft.

The consumer carries the selected config, projection fact, compiled transition vector, and duration extent atomically through Player, still/`TimelineFramePreview`, and client render. The render-only bound leaves editor/read geometry unchanged; malformed, negative, non-finite, missing, or overlong stored values use the effective per-clip bound.

Viewing approval `8488f9c1c2e3eafd924720e5bcd49a950798ffed` is reusable for the seven consumer files whose bytes are unchanged in the candidate: `TimelineFramePreview.test.tsx`, `TimelineFramePreview.tsx`, `useVideoEditorPreviewComposition.ts`, `useVideoEditorPreviewSurface.tsx`, `VideoEditorAssetPanelSurface.tsx`, `useClientRender.ts`, and `useRenderState.ts`.

There is one actual semantic delta that cannot inherit that approval: `canonicalRenderBounds.ts` now treats a negative stored cap as invalid and falls back to the effective occurrence bound, whereas `8488f9c` clamped that case to zero. This is the correction requested by the earlier Viewing rejection and is covered by the current tests, but it needs an explicit Viewing peer review before merge. The remaining `useTimelineState` difference is the cap-specific `save.data` handoff into the already-reviewed render-state path; lifecycle changes are test-wrapper identity updates only.

## Evidence

Using the private public13 overlay and private Vite cache (`--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`):

- Cap, render-bound, and serializer lane: **4 files, 51 passed**.
- Nearest lifecycle/session/persistence/label/popup lane: **8 files, 216 passed**.
- Producer omission negative: a private transform removing only the producer’s `storedOccurrenceDurationMs` emission made both paused and playing cap tests fail as intended (`expected 5, received 4`), exit 1. Repository source was unchanged.
- Scoped ESLint over all 30 cap paths: exit 0.
- `git diff --check c57dcc261..dca891972`: exit 0.

Exact targeted command prefix:

```text
env -u ASTRID_CHECKOUT node --require .../dirname-preload.cjs .../private13/node_modules/vitest/vitest.mjs run --config .../private-cache-v13.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

The central `app-full-postbebadd-public13-c57dcc26-agent8130-runtime2c4-1020173410-17473` result was still non-terminal (no `summary` file; log continued growing) at review completion, so the one permitted public13 project `tsc` was **not run**. No full suite, browser, build, install, live socket, render, or pixel/audio parity claim is made.

## Required next step

Viewing should review the negative/non-finite stored-cap fallback delta against `8488f9c`, then rerun its narrow consumer gate. If that review approves the correction, this source gate can be reconsidered without changing the cap delta or synthesizing any App2 typing files.
