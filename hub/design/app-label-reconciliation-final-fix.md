# App label-reconciliation final review fixes

Date: 2026-10-20 UTC

## Exact source identity and scope

The held candidate was commit `8a79a7bb9416302f36b6a8c104444ff609dff5e0`,
tree `19b61ebd8ec15de7ba3b656059412df5de97e913`.
The follow-up patch is uncommitted in the worker worktree; its
`git diff --binary HEAD` SHA-256 is
`8a63fdbc9c49c7343f3314f25b8dcce8d0ad3d6012765a5464b164bfe3cf39a4`.

Only the two independent review holds were fixed:

1. `rowsToConfig` now truthfully includes `clips` in the existing `Pick` type
   used by its raw authored clip carrier. No shape, runtime behavior, `any`, or
   suppression was added.
2. Two lifecycle identity assertions now compare the exact assembled input
   references (`savingEdit.resolvedConfig` and `initial.resolvedConfig`) rather
   than values captured from `player.config`.

Raw authored labels, including absent/null/opaque values, visible MAIN names,
timing/head/race/draft/metadata-only assertions, and unprojected exact config
identity remain unchanged.

## Retained 12-case expectation mapping

All twelve original failure cases remain present. No case was skipped, deleted,
marked expected-to-fail, or weakened.

### `timeline-save-utils.test.ts` (4)

1. `data.resolvedConfig.toBe(resolvedConfig)` → strict equality with the exact
   post-assembly projection containing `video.mp4` and `audio.mp3`; the raw
   `data.config.toBe(config)` assertion remains.
2. `data.signature === getConfigSignature(data.resolvedConfig)` → equality with
   the exact unprojected resolved-input signature plus explicit inequality from
   the display-labelled projection.
3. Legacy pinned-group repair → an exact resolved-input oracle with repaired
   geometry and no derived labels, retaining group order and geometry checks.
4. Inverse-transaction stable-signature case → unchanged expectation; it now
   passes because row reconstruction preserves the raw authored label state.

### `useVideoEditorPreviewSurface.lifecycle.test.tsx` (8)

1. Candidate/closure delivery: `edit`/captured output expectations →
   `localEdit.resolvedConfig`, `savingEdit.resolvedConfig`, and
   `acceptedClosure.resolvedConfig`; deferred acknowledgement, asset-entry,
   and registry identity checks remain.
2. Retained B through A acknowledgement and observed C: `b` →
   `afterA.resolvedConfig` and `afterC.resolvedConfig`; base-R and observed-C
   sequencing remains.
3. Same-content acceptance: `config`/`nextConfig` →
   `initial.resolvedConfig`/`next.resolvedConfig` across the 149ms/1ms timing
   boundary.
4. Metadata-only certification: accepted facts now use the exact initial
   assembled config reference; the unsaved label, target change, unavailable C
   notice, and clear-only-target behavior remain.
5. Independent canonical-read failure: captured `player.config` output oracle
   → the exact `initial.resolvedConfig` input reference; unavailable-target and
   recovery assertions remain.
6. Paused coalescing: `b` → exact `localB.resolvedConfig`; superseded A remains
   absent.
7. Playing coalescing: `config`/`b` → exact
   `initial.resolvedConfig`/`localB.resolvedConfig` before/after the frame;
   superseded A remains absent.
8. Scope remount: `pending` → exact `acceptedPending.resolvedConfig`; the
   committed-A label and zero-timer assertion remain.

## Verification

Using the approved private13 graph (Composition 0.0.13, 77 members, archive
SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
React 18.3.1, Remotion 4.0.509), with the required preload,
`--configLoader=runner`, `--no-cache`, one worker, and no fallback package:

```text
2 held files + timeline-data/outputProjection neighbors: 4 files, 57 passed, 0 failed
```

The earlier private13 qualification remains recorded as 10 files, 185 passed,
0 failed; the follow-up reran only the exact two files plus the two requested
closest neighbors after the fixes. `git diff --check` passed. No project
TypeScript check, full suite, browser/live sockets, build, install, or shared
dependency/cache write was run.
