# App M2 shot-name native independent review

## Decision

**REJECT** `a4fb4bbb00e8c0453fdce8d311cf6a63944fc7b9` for the bounded embedded shot-name migration. This is a review only: no product source, schema, generated client, test, lockfile, branch, or ref was modified.

The candidate has positive portable-golden parity, but the required mounted-session lifecycle evidence is incomplete and the current source has an async-conflict/draft-retention gap. This review does not claim writer retirement.

## Exact source identity

- App candidate: `a4fb4bbb00e8c0453fdce8d311cf6a63944fc7b9`
- Candidate tree: `831927b41625f5029d26bc83eb1b2acca1f617e4`
- Parent/baseline: `b1ef4b9b910ba72375c34cf319692f90d22edc25`
- Agent reference: `/home/user/work/wt/app-m3-agent013-current-pair-source`, `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- Runtime schema reference: `/home/user/work/wt/app-m3-runtime013-producer-source`, `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Design/audit read: `docs/design/app-shot-name-native-session-migration.md` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-shot-set013-contract-ingress-audit.md`

## Source findings

1. The new native implementation is mostly semantically aligned on the portable golden. An independent probe against Agent's `tests/editing_conformance/fixtures/recipe_m2_shot_set.json` found the App `executeShotSet` command and authored after-bundle deeply equal to Agent's command and after-bundle. The candidate record also contains the matching occurrence read, exact source dependency pin, direct writes, occurrence binding, and empty selections/created fields. The Agent inverse/guard lane passes, but the App branch has no inverse differential test; its own `shotSetCapture.test.ts` is a self-mirroring fixture test.

2. The branch does not prove the required native capture matrix in executable App tests. The added test covers one present-name fixture and local implementation behavior. It does not compare against the Agent golden record/after bundle or test fresh present/absent root names, source-pin preservation, shared-owner materialization, exact command/record/inverse, original guards, or replay/undo controls. Independent probes for present, absent, exact source pin, and sibling preservation passed, but they are not branch evidence.

3. There is a concrete async-conflict/draft-retention defect. In `src/tools/video-editor/commands/commitSession.ts:334-344`, shot `finish` validates only `localGeneration`, computes `result` from the old captured basis, then stores `before: bundle` (the possibly newer live bundle) with `after: result.bundle` from the stale captured basis. `observe` can replace `bundle` after focus while `localGeneration` remains unchanged (`commitSession.ts:509-519`). The submit identity check therefore accepts this mixed basis. A disjoint remote change can be dropped from the local projection until acknowledgement; a conflicting remote name is refused by Runtime, but the shot UI has already closed the editor (`useNameEditing.ts:65-70`) and `ShotEditorView.tsx:361-364` has no conflict callback that restores the name draft. The required visible refusal with draft kept is neither implemented for this path nor tested.

4. The mounted route does pass the parent `shotSet` port from `AstridTimelineEditor` through `LocalTimelineShotBrowser` to `ShotEditorView`, so the intended embedded path uses the parent session/outbox when capture succeeds. However, no test proves before-focus capture, stale authority refusal, close, project switch, late ACK, restart/recovery, exact retry, or undo for a shot name. These remain required before approval.

5. Empty-name behavior remains a visible cross-contract discrepancy, not a reason to weaken a test: Agent native capture accepts `name: ""`; the Runtime `2c4ac180` `ShotPayload.name` schema requires `minLength: 1`; the App UI still trims and refuses an empty input in `useNameEditing.ts:65-70`. A direct schema probe refused `""` and accepted `"Renamed"`. No Runtime HTTP acceptance or bad-head publication was claimed or run. The candidate's local empty-string test must not be treated as end-to-end success.

6. No operation API/schema change was found in the candidate diff. `ShotSetArgs` remains the existing generated boundary; the candidate adds App helpers and ports only.

## Remaining NAME writers (not retired)

- Embedded parent-mounted shot name: the new `shotSetPort` path in `ShotEditorView.tsx:357-364`, when capture exists.
- Standalone/canonical fallback writer: `ShotEditorView.tsx:366-387` calls `updateCanonicalShotName` through `enqueueCanonicalShotPublish` and the direct canonical adapter publish. This remains the standalone legacy name writer.
- Ordinary legacy/Supabase editor writer: `ShotEditorView.tsx:390-394` calls `useUpdateShotName().mutate` when the canonical path is not active.
- Gallery/list writer: `src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.tsx:155-163` calls `useUpdateShotName().mutateAsync` directly.
- The separate canonical settings writer remains `ShotEditorView.tsx:159-210` (`updateCanonicalShotSettings` through the whole-graph CAS callback); settings were intentionally not migrated by this candidate.

The embedded candidate path is therefore not evidence for global zero legacy traffic. Standalone name/settings behavior must remain intact until its own authority and field-intent migration is qualified.

## Commands and results

From `/home/user/work/wt/app-m2-shot-name-native-independent-review`:

```text
node node_modules/vitest/vitest.mjs run --config vitest.config.ts --no-cache --maxWorkers=1 \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx
PASS: 4 files, 115 tests passed.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-m3-agent013-current-pair-source \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  /home/user/work/wt/app-m3-agent013-current-pair-source/tests/editing_conformance/test_recipe_shot_set.py
PASS: 61 passed in 2.24s.

node --import tsx --input-type=module [independent App-vs-Agent golden differential probe]
PASS: command and after-bundle deep equality; present/absent expect states, exact source pin, and shared sibling preservation observed.

/home/user/work/venv-agent/bin/python [Runtime ShotPayload schema probe]
PASS: empty name refused (`'' should be non-empty`); non-empty `Renamed` accepted.

git diff --check HEAD^ HEAD
PASS.

npx eslint --max-warnings 0 --ext ts,tsx [all 15 changed App source/test files]
PASS.
```

No full suite, project typecheck, build, browser, localhost/socket test, install, or central test-service request was run. No Runtime HTTP acceptance, reload/undo/retry/restart, or browser journey was run.

## Required remaining gate evidence

- Actual reload/restart + exact retry after lost ACK: **unverified for shot names**.
- Actual native undo/inverse and redo/rebase: **unverified for the App session path**.
- Provider empty-name refusal with unchanged head and visible draft retention: **unverified**.
- Async same-leaf conflict and disjoint remote edit with original guards and draft retained: **not proven; source gap above**.
- `onClose`, project switch, and late ACK/recovery: **unverified for shot names**.
- Zero legacy name traffic: **not achieved/claimed**; standalone and gallery writers remain.

Recommended next step: keep the candidate rejected until the owner adds a non-self-mirroring App differential/session lane that covers the above controls, fixes the mixed stale/live bundle handling and restores the name draft on asynchronous refusal, then reruns the bounded App and Agent lanes plus the central Runtime/browser journey outside this sandbox.
