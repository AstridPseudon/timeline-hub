# App M2 native `None` candidate on final root

Status: source candidate ready for the manager’s primary current-tuple root gate. The real two-case browser/Runtime gate is intentionally unrun; no ledger row is marked deleted, no old writer is retired, and no merge or activation is claimed.

## Exact source and tree

| Item | Value |
| --- | --- |
| Worktree | `/home/user/work/wt/app-m2-finalroot-none-qualified-candidate` |
| Branch | `tl/app-m2-finalroot-none-qualified-candidate` |
| Base HEAD | `b1ef4b9b910ba72375c34cf319692f90d22edc25` |
| Base tree | `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Candidate working tree | `26ffc29bce7f147c546530c6728bb61d70691092` (computed in memory; uncommitted worktree) |
| Approved product delta | `12e4e629d8b31df40af052657899159aefeac5f1` vs `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` |
| Current-lineage source used | `77ef266c2a87548adf6f50bd8931594a3e916210` (the approved delta composed onto Main17/Root013) |
| E2E source lineage | `546fd8464e6ccc1ddf46be2c56c2ca3471df112a` plus binding repair `eef2c88122d863b2010d38f8a0d12011529a7407` |
| Frozen Agent | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` |
| Frozen Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `0.2.13` |
| Composition | `0.0.12`, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` |

The 26 product paths are byte-identical to the current-lineage `77ef` source and therefore to the approved `12e` product delta. Main17 touch/desktop label behavior, b1 live local policy, cold-label behavior, normal13/public12 pins, wrapper/server proxy, and existing journeys were not overwritten. No older Root cohort code was copied. The static parent-clear fixture metadata now names current-lineage App `77ef` and Agent `d874`; its command and record are byte-for-byte equal to Agent d874’s frozen scalar-clear command.

## What changed

The selected single-clip and bulk transition `None`/Remove controls now capture raw clip state through the existing command session and submit `clip.set` v1 with the exact arguments `{ values: {}, clear: ['transition'] }`. Capture occurs before finish, bulk capture finishes every selected target before one durable batch, and a failed capture refuses visibly without snapshot fallback or partial submission. The existing outbox, pending-ACK fence, original guards, preview, retry, recovery, and inverse machinery remain the owner of durability.

The two staged journeys cover exactly:

1. single clear: raw `transition` is ABSENT in both mirrors, reload preserves it, Runtime inverse restores the original object, lost ACK/restart recovery retries identical body/key/receipt, and legacy save traffic is zero;
2. bulk clear: one atomic original-basis batch preserves unknown revision/opaque/prototype-shaped data, exact retry and reload hold, Runtime inverse restores the full original, and a real guarded conflict retains the full draft/request identity with no legacy traffic.

Those are source assertions only until the central gate executes them against the current App tree, Agent d874, Runtime 0.2.13 and public12. The original seven journey bodies and the four cold/live-policy assertion paths remain present and were exercised by the targeted neighbor suite.

## Exact legacy-branch retirement boundary

The replaced production branch is the `NO_TRANSITION`/Remove path in `ClipTransitionSection` and its bulk equivalent in `BulkClipPanelBody`: production `PropertiesPanel` and `PropertiesPanelBody` now always provide `onScalarEditStart`/`onScalarEditsStart`, so those controls use `submitClipScalarEdit`/`submitClipTransitionClears` and never call the legacy whole-document callback.

Remaining callers are deliberate compatibility/unsupported paths:

- `ClipTransitionSection` retains `onChange({ transition: undefined })` only when a standalone caller omits `onScalarEditStart`.
- `BulkClipPanelBody` retains `onChangeDeep(() => ({ transition: undefined }))` only when a standalone caller omits `onScalarEditsStart`.
- Existing parameter, duration, type-change, reset, effect and other unsupported writers continue their pre-existing callback paths; they are not native-qualified by this unit and must remain until their own replacements pass.
- Preservation tests intentionally exercise the standalone callback fallback so the fallback is not confused with production App routing.

This is a reviewable one-writer unit: the native control path is used by both real production inspector entry points, and the fallback is explicitly guarded by a missing capture port rather than hidden behind an opaque callback.

## Evidence run

All Vitest commands used the read-only worktree `node_modules` link, `--no-cache`, the runner preload, one worker, and a private `TMPDIR` under this worker’s orchestration notes. No build, project-wide TypeScript check, browser, socket, install, or full suite was run.

| Command/result | Evidence |
| --- | --- |
| Vitest scalar/session core: `clipScalarCapture`, `clipScalarGesture`, `commitSession.clipScalar`, `commitSession`, `TransitionPreservation`, `useTimelineCommandSession`, `clip-scalar-preview`, `ClipPanel.nativeNone` | 8 files / **213 passed**, 0 failed |
| Vitest neighbors: `commitOutbox`, session projection, `ClipPanel.transition`, `ClipPanelBody`, `PropertiesPanel`, serialize, timeline-patch, track-label gesture/management, recovery | 10 files / **485 passed**, 0 failed |
| Vitest preservation neighbors: `TrackLabel.command`, `mediaCrossOrigin` | 2 files / **76 passed**, 0 failed |
| `node --test --test-concurrency=1 scripts/testing/current013-integration.test.mjs` | **12 passed**, source/identity/launcher guard controls |
| `node --experimental-vm-modules --test --test-concurrency=1 tests/e2e/local/support/current013-native-none.test.mjs` | **6 passed**, launcher controls |
| `node --test --test-concurrency=1 tests/e2e/local/support/native-transition-clear.contract.test.mjs` | **2 passed**, strict binding matcher; rejects invented `scalar.owner` |
| Scoped ESLint over all changed TS/TSX paths, `--max-warnings 0` | Passed |
| `git diff --check` | Passed |
| `node scripts/vendor-lock.mjs check runtime.lock.json` | Passed; Runtime 0.2.13 pin |
| `node scripts/quality/check-known-failures.mjs` | 3 pre-existing authorized markers, 0 forbidden |
| Static source audit | 26 current-lineage product paths exact; d874 command/record exact; Runtime pin and Composition 0.0.12 archive exact (77 regular members); helper binding is strict `{ 'scalar.target': command.select }` |

An initial targeted import run failed because my path-limited source apply omitted the two `clip-scalar-preview` files. I restored those exact approved files, reran the complete core selection, and it passed 213/213. An initial combined Node invocation omitted `--experimental-vm-modules`; the unchanged six-test matcher then passed with that required Node 22 flag. These were assembly/runner corrections, not changed behavior expectations.

The exact Vitest runner form was:

```sh
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-finalroot-none-qualified-candidate/notes/tmp \
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-finalroot-parent-delete013-source-port/notes/runner.cjs \
node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts \
src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/commands/commitSession.test.ts \
src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx \
src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/lib/clip-scalar-preview.test.ts \
src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx
```

The same exact runner/config flags were used for the 10-file neighbor list in the table, then for `src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx src/shared/lib/media/mediaCrossOrigin.test.ts`. Static commands were exactly `node node_modules/eslint/bin/eslint.js <the changed TS/TSX paths> --max-warnings 0`, `git diff --check`, `node scripts/vendor-lock.mjs check runtime.lock.json`, and `node scripts/quality/check-known-failures.mjs`.

## Central real gate, ready after primary root PASS

Do not run this until the manager’s primary current-root gate is green and the central service has snapshotted this exact candidate tree. Use the private12 dependency overlay and short temporary directory supplied by the central runner; do not point it at shared caches. The literal native-None child command is:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-finalroot-none-qualified-candidate/notes/short \
  TIMELINE_CURRENT013_RUN=1 \
  TIMELINE_CURRENT013_APP_TREE=26ffc29bce7f147c546530c6728bb61d70691092 \
  TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
  ASTRID_PUBLIC_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 \
  node scripts/testing/current013-native-none.mjs
```

The wrapper performs exact pre/post source checks and delegates only `npm run test:e2e:three-products -- --grep 'M2 native None'`, i.e. the two new cases. The central runner must bind its private12 overlay/cache identity to App tree `26ffc29bce7f147c546530c6728bb61d70691092`, Agent d874, Runtime 2c4, public12, and Chromium 141; a moving integration checkout or old cache is not equivalent.

## Remaining gate and retirement delta

Unverified: actual browser UI capture, Runtime acceptance and publication identity, raw reload in both mirrors, process death/restart, exact retry after real lost ACK, real 409 conflict draft retention, other-author guarded inverse, renderer-off behavior, and representative zero-legacy traffic. The native source path is ready for that proof; unsupported callback writers remain intentionally live. Only after this two-case gate and the manager’s primary root gate pass should the manager consider the specific transition-None legacy branch for retirement and update the M2 ledger. No broader writer retirement follows from this candidate.
