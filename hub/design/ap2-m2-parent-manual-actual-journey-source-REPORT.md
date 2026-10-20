# `ap2-m2-parent-manual-actual-journey-source`

## Result

Prepared the App source for the manual prepared-video parent-media path and added a focused durable-session journey. The production path now has the existing generated Runtime `getProjectVerifiedMedia` operation exposed through the existing `AstridRuntimeClient` and project-scoped `RuntimeDataProvider`; the timeline service can therefore perform the qualified verified GET before native `clip.add-media` commit submission.

The focused journey covers:

- the original five-field media selection captured before the verification await;
- refusal of a wrong catalog selection while retaining the draft and emitting no native intent;
- the positive exact selection after a lost acknowledgement;
- disposal/reload recovery and exact retry identity;
- guarded native undo;
- opaque-field preservation and zero legacy composition-revision POSTs.

No production writer or mock transport is used by the production path. The focused session test uses the repository's existing Runtime-bound in-memory environment, as do the surrounding session tests; it is not a claim of the central live three-product/browser gate.

## Source changes

- `src/integrations/runtime/client.ts`: restored the existing generated verified-media read through `AstridRuntimeClient`.
- `src/integrations/runtime/dataProvider.ts`: restored the existing project-scope check and verified-media read through `RuntimeDataProvider`.
- `src/integrations/runtime/dataProvider.test.ts`: verifies the exact GET path, returned verified media, and cross-project refusal.
- `src/tools/video-editor/commands/commitSession.test.ts`: expanded the existing native parent-media journey with wrong-selection refusal, reload/recovery exact retry, guarded undo, opaque preservation, and no legacy save traffic.
- `src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts`: exposes a read-only cloned server document for the opaque assertions.

The Runtime method is not a new DTO or endpoint: it is the already-generated `getProjectVerifiedMedia` operation and the previously approved App client/provider seam restored from the existing c4148a52 implementation.

## Verification

Passed:

```text
vitest dataProvider.test.ts -t 'reads exact verified media through the project-scoped Runtime facade'
  1 passed, 69 skipped

vitest dataProvider.test.ts
  70 passed

vitest parentClipAddCapture.test.ts
  6 passed

vitest commitSession.test.ts -t 'retains a wrong-selection draft'
  1 passed, 72 skipped

tsc --noEmit --pretty false
  passed

eslint [the five changed source/test files] --max-warnings 0
  passed

git diff --check
  passed
```

The Vitest config requires the repository's existing `__dirname` runner shim in this environment; the passing commands used that shim with a private worktree cache and `--no-cache`. The shared App `node_modules` was not modified.

The full `commitSession.test.ts` and filtered provider journey attempts terminated in this sandbox after Vitest's `RUN` line without a summary, so they are not claimed as passing. No full suite, browser, localhost, live socket, or central test was run.

## Source/cohort guards and pending central request

The App `runtime.lock.json` points at Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; the authoritative manager status records the corresponding Runtime tree `7ab412cc4bcbe517efcfa806e092336390312e18`, Agent `8130`, public Composition `13`, and the required fail-fast exact-source/bin guards. The local `/home/user/work/runtime` integration worktree is not that exact Runtime checkout and was not used as evidence.

The candidate is intentionally still uncommitted. After the harness commits it, the prepared targeted request is:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-parent-manual-actual-journey-source targeted \
  --files "src/integrations/runtime/client.ts src/integrations/runtime/dataProvider.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts src/tools/video-editor/commands/commitSession.test.ts") \
  && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

This was not submitted because the current worker source is uncommitted and the task explicitly forbids submitting uncommitted source. The existing `normal014` named central scripts exercise a different historical parent-media route/source tuple and must not be reported as this journey's evidence. The remaining qualification is one fresh central exact-cohort real Runtime/three-product run with fail-fast Agent8130/Runtime2c4/public013/Composition13 source and private-bin guards.

## Missing plan files

The requested `PLAN2/3/6` paths were absent in the supplied orchestration directory. I used the authoritative `PLAN.md`, current App manager `STATUS.md`, and the relevant App handoffs/reports; no settled plan decision was changed.

