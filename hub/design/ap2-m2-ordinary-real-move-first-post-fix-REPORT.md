# AP2-M2 ordinary move first-post fix

## Result

Fixed the first real failure in the App producer path. `Move existing shots to markers` now emits same-track hold members as the exact ordinary `{ hold }` shape. That shape uses the existing generic ordinary capture path, which preserves an existing transition; the previous `{ values: { hold }, clear: [] }` shape entered `ordinaryScalarMember`, whose intentional transition guard refused the batch before enqueue, leaving `wire.posts` empty.

The authoring-enable guard, timeline-ready snapshot path, conflict guard, outbox/session code, command schema, and cross-track legacy shape are unchanged. No shared core path needed a proposal or edit.

## First causal evidence

The authoritative central run reached `three-products.spec.ts:1222`: Chromium smoke and hosted build passed, but after the button click `wire.posts` stayed at 0. Source tracing showed `buildAlignShotsPatch` produced a same-track `clip.update` values/clear member; `captureGenericPatch` routed that member to `captureOrdinaryScalarMember`, and `holdExtent` refused the seeded transition. The generic exact-hold branch instead calls `executeClipSet`, which retains the transition and produces the same `clip.set` command expected by the journey.

## Changed paths

- `src/tools/video-editor/dev/scene-phase-markers/extension.ts`: same-track hold producer shape changed to `{ hold }`.
- `src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts`: updated focused producer expectations.
- `src/tools/video-editor/commands/genericPatchCapture.test.ts`: regression covering move + exact hold while retaining a transition.

## Verification

- `npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts` — PASS, 2 files / 60 tests.
- `npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/commands/ordinaryScalarMember.test.ts` — PASS, 1 file / 7 tests.
- `npm exec eslint -- --max-warnings 0 src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts` — PASS.
- `git diff --check` — PASS.

The fresh central browser/socket gate was not run here, per the no-local-browser rule and because the harness requires the finished source tree to be committed first.

## Exact next gate

After the harness commits this worktree, run exactly once:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-real-move-first-post-fix e2e-m2-ordinary-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test $R
```

