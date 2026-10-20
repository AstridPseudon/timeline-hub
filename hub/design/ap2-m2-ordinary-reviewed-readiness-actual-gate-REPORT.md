# AP2 M2 ordinary reviewed readiness actual gate

## Result

Adopted the exact reviewed App initialization fix into the private ordinary
candidate. The change is byte-for-byte identical to the diff of reviewed App
commit `741c785399b0954544b9992215f952a621739ea2` against its parent
`ed48d92d2a8bb8d9f013060e420eba646d88ace4`.

The readiness candidate parent is App commit
`44ddbbd1f74ff09accab9ab3b27f8706132fc571` (`tl/ap2-m2-ordinary-final-committed-runner`).
Only these two reviewed files changed:

- `src/tools/video-editor/hooks/useTimelineSave.ts`
- `src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx`

The published risk review
`app-initial-recovery-generation-risk-review.md` is **APPROVE** with no
data-safety finding. It confirms the existing recovery generation remains the
stale-work fence, the checked-scope marker is cleared on canonical reload, and
readiness stays closed until the current-generation read settles.

## Native path verification

The ordinary path is internally wired and does not need duplicate/parent
provider ports:

`useTimelineState` → `save.commands.genericPatchPort` →
`useTimelineCommandSession`’s guarded generic port → `useTimelineOps` native
classification/capture/finish/submit.

No provider-port, DTO, dependency, public pin, or legacy guard change was made.
The committed ordinary runner remains unchanged (SHA-256
`6f0e76501a28057d0fec0be7e5e8c1648872847275acf61203706739dc181026`).

## Verification

Passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx
# 2 files, 12 tests passed

node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
# 3 files, 57 tests passed

node_modules/.bin/eslint src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx --ext ts,tsx --max-warnings 0 --no-cache
git diff --check
# pass

exact reviewed diff comparison against 741c785^..741c785
# pass
```

The existing public13 environment preflight remains valid:
`ap2-m2-public13-integration-preflight-1020184006-23865`, exit 0. It is not
the actual browser/native gate.

## Actual gate hold

The central actual ordinary browser/native journey was not queued from this
worker because the App source join is intentionally uncommitted here; the
harness commits the candidate only when this worker exits. This is a precise
hold, not an approval claim. After the harness reports the clean committed App
SHA, run exactly once:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-reviewed-readiness-actual-gate e2e-m2-ordinary-integration --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That suite uses the existing ordinary runner and its exact Agent
`8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and Composition 0.0.13 guards.
No full suite, local browser/socket run, or repeat source qualification was
performed.
