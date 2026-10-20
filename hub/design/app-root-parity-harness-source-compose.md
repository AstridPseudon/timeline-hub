# App M3 root source + integrated parity harness

## Result

Applied the approved ROOT source candidate delta to the current App base while
preserving the already-integrated, test-only viewing parity harness. No old
parity cohort was copied back and no product behavior was rewritten.

## Exact references and tree identities

| Role | Commit/ref | Tree |
| --- | --- | --- |
| Current base | `6ff21cac9deee3aae014e5c9e65d9871a3452f77` | `27d41c1b0e64ff9028f78576804f3b8cb3b9f1d5` |
| Current parent used for candidate delta | `7bb885b638838588a0dff81b64b7c34960ac07f3` | `065b46ac13026d3e3a1d760b44bab1ab8e1e930e` |
| Approved candidate commit | `256ef376f29b7804e74a5a378a77288bfcfce1ed` | `99f031ca5eccb646d038de764d417cfeea510ad0` |

The applied source operation was the exact binary-safe delta:

```sh
git diff --binary 7bb885b63 99f031ca5eccb646d038de764d417cfeea510ad0 | git apply --verbose
```

Candidate delta: 169 paths, `+6,034/-4,165` lines. The 32-path `7bb885b63 →
6ff21cac9` parity delta remains present: three Playwright configs plus 28 new
parity/spec helper sources and the existing `tests/e2e/local/support/harness.ts`
change. All 32 paths byte-match `6ff21cac9`.

## Source equivalence and preservation

- Every candidate path byte-matches the worktree except the task-injected
  guidance `CLAUDE.md` and the expected parity-owned `tests/e2e/local/support/harness.ts`.
  The remaining 5,794 of 5,796 candidate paths have zero mismatches.
- The candidate's protected product/source proof therefore carries onto this
  worktree. Current CORS and protected MAIN behavior remain sourced from the
  approved candidate/current equation; no four-case parity launch was run.
- The AST audit reports: 6 migrated journey cases preserved, 21 migrated
  helpers preserved, 1 additive case and 1 additive helper, original MAIN row
  and canvas assertions preserved, and 64 changed TS/TSX files parsed.
- The existing clamp remains. No opacity-1 promotion, transient renderConfig,
  projector/default/renderer fade-clock change, Native None/PARAM/delete/split/
  trim/auto/proxy-port cohort, or old download cohort was introduced.
- The development-only Runtime normal pin remains the candidate's existing
  `0.2.9` source `94114269d1ce23ab3224d7eca5a85138ce2b5fed` and producer
  `sha256:e02a71b5b77479bdc8035a8a8d75ec57e9f1962b7f9195126739ab0d1ed063ac`.

## Targeted evidence

All commands ran from the assigned worktree. The Vitest wrapper used a private
cache outside the worktree; no shared dependency or cache was modified.

```sh
node --import tsx --test --test-reporter=spec tests/e2e/timeline/viewing-parity/*.test.ts
```

Result: 11 tests passed, 0 failed, 0 skipped. This covered parity admission,
authority, browser-profile/helper discovery, canvas/config, comparator,
diagnostics, direct-frame safeguards, download, graph harness, media fixture,
and source-tuple checks. It did not launch a browser or localhost service.

```sh
node config/vite/timelineCompositionPackage.test.mjs
```

Result with the retained private public12 overlay: 9 tests passed, 0 failed.
The first diagnostic run against the shared read-only node_modules correctly
failed 7 resolver checks because that shared package is still 0.0.10; it was
not changed. Only this worktree's ignored node_modules symlink was pointed at
the retained private 0.0.12 overlay.

```sh
node node_modules/vitest/vitest.mjs run \
  --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-root-parity-harness-source-compose/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/trackLabelGesture.test.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/compositions/AudioTrack.test.tsx \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/installed-themes.test.ts \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts
```

Result: 15 files passed, 417 tests passed, 0 failed.

Additional checks:

```sh
node --check tests/e2e/fake-runtime/launch.mjs
node --input-type=module -e "import fs from 'node:fs'; for (const p of ['tests/e2e/fake-runtime/tsconfig.json','supabase/functions/complete_task/deno.json']) JSON.parse(fs.readFileSync(p,'utf8')); console.log('PASS: launch syntax and JSON parses')"
git diff --check
```

All passed. No full suite, build, browser, localhost/socket, install, or
project typecheck was run.

## Future tuple gate

Keep this source base and private public12 overlay only for the imminent safe
Runtime pin and final tuple qualification. The normal final pin is not ready:
Runtime must publish the safe producer, Agent must adopt the matching pair, and
App must perform one official `vendor-lock.mjs update` against that published
source. Then freeze the exact Runtime/Agent/public12/App tuple and reserve the
single project typecheck and final qualification. Do not promote the current
development-only pin or claim render/audio/pixel parity before the required
MAIN-pixel and final-pair evidence.
