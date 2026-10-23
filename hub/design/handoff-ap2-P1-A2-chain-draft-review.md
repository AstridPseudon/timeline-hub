# P1 / A2 chain-draft proof review

Result: **PASS**.

Reviewed the proof at App SHA `e739d880e711c3267cff5f72c172d85092fdbeee` against PLAN v2.1 and `commit-v2.md` §§1–5. The proof is truthful: it labels the result a first-draft full-chain NO-GO and does not promote the 13 local-save tests into Runtime/Agent acceptance.

Current evidence:

- `createLocalSaveSession` (`src/tools/video-editor/commands/localSaveSession.ts:63`) has only the unit-test import/caller (`localSaveSession.test.ts:8,63`); no mounted App caller exists.
- The mounted editor reaches `useTimelineSave` at `useTimelineState.ts:622`; `useTimelineSave.ts:71` constructs `useTimelinePersistence`; the save mutation at `useTimelinePersistence.ts:399-403` still calls `saveTimelineAtHead` or `saveTimeline`. `useTimelineSave.ts:64` is the preceding `useTimelineCommit` hook construction, a minor locator imprecision in the proof, not a substantive error.
- App DTOs remain pre-v2: `CommitRequest` lacks `steps`, `merge`, and reads; accepted status lacks `merged`; failure status lacks `invalid` (`src/integrations/runtime/timeline-commit-types.ts:68,86,91`). Generated commit response validation accepts only `accepted`/`rebased` (`src/integrations/runtime/generated.ts:170-178`).
- The 13 tests use `vi.fn` transport, synthetic `result(...)`, and fake IndexedDB. Split/trim, intervening-field preservation, synthetic merged/rebased, refusal/rollback, lost ACK, and restart are local outbox behavior only. No Runtime or Astrid/Agent acceptance is called. No v2 P1 browser scenario exists (`tests/e2e/local/three-products.p1-commit-v2.spec.ts` absent).

The exact required checks all passed: Vitest 1 file/13 tests, `tsc --noEmit`, targeted ESLint, and `git diff --check`. Logs are in `/tmp/ap2-p1-a2-chain-draft-review-{vitest,tsc,eslint,diffcheck}.log`.

Missing boundaries remain with App A2/U4p for mount/caller and v2 DTO adoption, and Runtime/Agent for a real provider-backed chain returning canonical `id_map` plus accepted/merged/refused structured outcomes. Preserve the existing success/refusal tests. H3 is **NO-GO** until real corpus + App/Runtime/Agent chain evidence passes.
