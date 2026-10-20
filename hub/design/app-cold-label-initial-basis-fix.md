# Cold first track-label edit: initial verified basis readiness

Worker: `app-m3-cold-label-initial-basis-fix` (KEEP for root gate).

## Source and exact mismatch

Base App `05b6b488d1834650c459c5c565f2530d9bea20e9`, base tree `00e9e2a92d80ee103a94fab1d976babe3ca918e1`.
Final source tree: `74130f681f6b0c87a7c61cb33d4ae6a092c03046`.
Patch SHA256: `10831ec4e2f62a4e9858a7efa296fa903b577b665f0f8e9a1979a6cc8ed8f914`.
Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`; Runtime/producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; public Composition 0.0.12 archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. No package/pin/renderer/Auth/cap/PCM edits.

The original real-browser failure was central TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-00e9e2a9-setup88888-e2e-integration-cold-open1-1020143727-26993`, at `track-label-command.spec.ts:558`: zero commits, original Unicode draft retained, visible “Displayed timeline does not match the raw authoring basis”.

Its trace has immutable parent revision `e632a812-87fe-4640-abc7-548395d297c3` and verified history publication `txn-dfd678f31ec1457f9f5ef14eacf99bf0`. The ordinary `/inspect` response has that revision but **no head_publication_id**. `readTimelineInOrder`/`loadTimeline` therefore produce a legacy display head with publication null. The command basis reads history plus pinned immutable closure and has both identifiers. Before any move, those display/capture head pairs disagree. The label guard correctly refuses them.

`useTimelineSave` originally launched command bootstrap before first poll adoption and the asynchronous one-slot recovery check. `project(basis, [], true)` could yield to the intervening raw display/head or `legacyClean() === false` during that check. That yield is correct for dirty/recovery/newer data, but no later initial projection was arranged. A prior move happened to install a verified accepted projection, concealing the cold-only defect.

## Change

Wait to initialize the command session until the first visible data adoption and its initial recovery check settle. Then reuse the existing verified `initialBasis -> project(initialBasis, [])` path. The existing loading surface stays active until the capture port is installed (or initialization reports an error). No raw read is stamped accepted.

All original projection generation, object/head identity, dirty/recovery, original captured-draft, scope and exact revision/publication guards remain unchanged. The normal path now publishes canonical projected data and its exact verified head together before label capture. Existing active outboxes/recovery keep their original ownership and explicit recovery path.

Two regressions were added: a real `useTimelineSave`/command-session hydration from no data and a publication-null display using the fresh seed's parent V1/S1 tracks, two parent clips, placed shot, three child clips and opaque roots; and an initial basis arriving after a dirty Unicode label. The cold test checks loading, verified projection, exact original head, track label presence/value, id read and binding, one commit, and zero snapshot writes. Seed identifiers/media hashes are deterministic fixture substitutes; payload structure is the real seed's normalized shape. The small shared test transport now preserves the unchanged occurrence closure and supplies the seed registry.

## Direct source checks

All commands ran in `/home/user/work/wt/app-m3-cold-label-initial-basis-fix` with a privately owned module root pointing to the read-only coherent public12 install. The `__dirname` preload is `workers/app-m3-cold-label-initial-basis-fix/notes/vitest-preload.cjs`. Runner/cache setup is retained there; shared dependencies were not modified.

Exact focused command (exit 0; **11 files, 360 tests passed**, final tree):

```bash
NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-cold-label-initial-basis-fix/notes/vitest-preload.cjs' node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx
```

`focused-exact.log` contains the result. Native move/label capture parity and strict draft/recovery/history neighbors are included.

Original-source countercheck: `python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-cold-label-initial-basis-fix/notes/check-original.py` temporarily supplies only the two original product files, executes the same Vitest runner on `useTimelineCommandSession.test.tsx -t 'cold seed hydration'`, and restores the fix in `finally`. Expected exit 1, observed **exact original capture mismatch** at `commitSession.ts:279`. `original-regression.log` retains the stack. Other tests are filtered only for this countercheck.

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts
git diff --check
```

Both exit 0; no lint diagnostics. No full suite/project tsc/install/frame/PCM lane was run.

## Central browser qualification

All browser/build/socket work is central only. The worker-owned runner copies the verified runner pattern and preserves full40 Agent/Runtime and exact App tree pre/postflight, all75 producer files, normal locks, tracked public browser source, all77 public12 files, declared peers/player/three, original serial fixture delta SHA256 `88888d44ddd375caacb7b45b74001b70428bf4404b76fe11c84a83f8b05a6cfa`, and byte/mtime cache comparisons. Only this task's five allowed source/test paths are added to the exact source-diff allowlist. Both original serial fixture fixes, native3, regularlabels3 and positive cold assertions are untouched. The frozen prior review hash is checked for the unchanged baseline; it does not claim review approval of this new fix.

The hosted bundle is built fresh with `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` unset. Browser is the existing Chromium 141 binary with its original SHA256 guard. `TMPDIR=/tmp/tl-cold-fix` is assigned last and inherited by browser and subprocess. Each central snapshot owns its module/cache root and a copied Vite package; shared installs/caches stay read-only.

Central command abbreviations use `ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`. The exact expanded commands/environments are also in each central result `summary` and `tests/suites.conf`.

Cold command:

```bash
$ORCH/bin/request-test app-m3-cold-label-initial-basis-fix e2e-cold-label-initial-basis-74130f68-cold-open
$ORCH/bin/wait-test app-m3-cold-label-initial-basis-fix-e2e-cold-label-initial-basis-74130f68-cold-open-1020145250-25068
```

This invokes `npm exec -- playwright test --config playwright.track-label.config.ts --grep 'M2 cold-open'` in the verified snapshot. **PASS, exit 0, 1 test passed, 92 s including build/postflight.** All75/all77/source/peer/cache guards passed. Snapshot commit `d136172098a0931cf51efe340554f7db0f7758ef` has the final tree above. The real fresh browser completes rename as the first edit, emits the original exact head pair/track guards, preserves opaque config, reloads and performs guarded UI undo, with no legacy writer traffic.

Because the readiness seam also initializes native moves and regular labels, those two neighbor lanes are required if cold passes. Results will be appended here. Release selection remains with source review/manager; no broader release qualification is claimed.
