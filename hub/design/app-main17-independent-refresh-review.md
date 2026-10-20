# MAIN17 independent refresh review — APPROVE

Reviewed the canonical `ORCH/design/app-main17-true-refresh.md` against `ORCH/PLAN.md` and the actual Git objects. **APPROVE** the exact refresh below for the manager's merge queue. No blocking discrepancy found; no product or test changes made.

## Exact ancestry and tree

- Refresh/worker HEAD: `751f7703d22f0e8026e2926f93f64d69c65212fd`.
- Actual tree: `3340e128af4dd8fe79a8fe1016b23666c6ea8eb5`.
- Exactly two parents, in order: `35820a603a623e83c16a59cc397dd3079b228011`, `17e46de99b7cef52fe494de1703a9865a8d4be24`.
- MAIN17's sole parent: `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`.
- `git merge-base --is-ancestor 17e46de99b7cef52fe494de1703a9865a8d4be24 751f7703d22f0e8026e2926f93f64d69c65212fd`: exit 0.
- `git show --no-patch --format='%H%n%T%n%P%n%s' 751f7703`: confirmed the identities above.

Independent Python/subprocess checks enumerated all four trees with `git ls-tree -r -z`. The refresh changes exactly the eight upstream paths; every change hunk matches `44f0b9ca9 → 17e46de99` after removing blob IDs and hunk line offsets from `git diff --unified=0`. All **5,903 unrelated paths** have identical mode, object type and blob ID to `35820a603`. All **5,911 tracked working-tree files**, including executable modes and symlink targets, also match the reviewed refresh blobs (Git blob SHA-1 recalculated from local bytes). No tracked additions/deletions exist beyond upstream's added `mobile-sheet.ts`.

| Changed path (under `src/tools/video-editor/`) | Equality |
| --- | --- |
| `components/TimelineEditor/TimelineCanvas.tsx` | Exact MAIN17 |
| `components/TimelineEditor/TrackLabel.tsx` | Exact MAIN17 |
| `components/TimelineEditor/TrackListRenderer.test.tsx` | Exact MAIN17 |
| `components/TimelineEditor/TrackListRenderer.tsx` | Exact MAIN17 |
| `components/TimelineMobileInspectorDialog.tsx` | Exact MAIN17 |
| `lib/mobile-sheet.ts` | Exact MAIN17 |
| `components/TimelineEditorShellCore.tsx` | MAIN17 plus unchanged prior command recovery |
| `components/TimelineEditorShellCore.test.tsx` | MAIN17 plus unchanged three prior recovery tests |

For both shell paths, the normalized `MAIN17 → refresh` diff exactly equals the prior `44f0b9ca9 → 35820a603` diff. Read every upstream file diff and recovery reconciliation: the retained product changes are the recovery import/render, command-conflict exclusion from legacy conflict UI, and nothing else. The three retained tests assert explicit persisted-session selection, exact retry and retained conflict without snapshot replacement.

## Behavior and safety preservation

MAIN17 owns the touch track sheet: name editing, shared desktop settings, add video/audio and confirmed deletion. Its selected armed-clip tap releases Move/Trim and reopens the sheet; its touch bar offers Gallery and Ask Astrid without Text. These upstream changes and tests are accepted as instructed; this review introduces no mobile policy or rewritten expectation.

The 5,903-path equality check includes all server proxy/CORS code, public aliases, Composition root 0.0.8 package/lock/archive, Runtime generated contract/client 0.2.1 and provider parity. Specifically, `config/vite/{runtimeProxy,astridProxySecurity}.ts`, `scripts/runtime-discovery-proxy.mjs`, `src/integrations/runtime/{client,generated-contract-metadata}.ts` and `dataProvider.parity.test.ts` remain identical to integration. This proves preservation, not new runtime/browser qualification.

`src/tools/video-editor/hooks/useClipDrag.test.tsx` is entirely blob-identical to integration, including exactly three authorized `it.fails` markers at lines 774, 1120 and 1230 (new-bottom-track config edit and two pinned-group cross-track/new-track cases). No additional expected failures, skips or weakened assertions were introduced by this review.

## Test evidence

Original refresh evidence was read directly from `ORCH/workers/app-m2-main17-true-refresh/targeted.log` and the canonical design command: **14 files passed; 455 passed; 3 expected fail (458 total), 65.28s**, Vitest 4.1.5. The committed source tree and every original test input are preserved exactly. This is retained original evidence, not a new 14-file rerun.

Independent rerun from `/home/user/work/wt/app-m2-main17-independent-refresh-review`:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-independent-refresh-review/vitest-preload.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-independent-refresh-review/vitest.private.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditorShellCore.test.tsx
```

Result: **exit 0; 2 files passed; 139 tests passed; 20.26s**. Full output: `ORCH/workers/app-m2-main17-independent-refresh-review/targeted.log`. This was the single independent test invocation, limited to the directly changed track/shell suites.

Private `standard8/node_modules` borrowed dependency entries read-only from `/tmp/app-m2-coherent-deps8/node_modules`; Composition 0.0.8 was extracted privately from this tree's archive. Verified archive SHA256 `93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa`, 77 extracted files, React/React DOM 18.3.1, Remotion/player 4.0.509 and Vitest 4.1.5. Runner config loading, `--no-cache`, private cacheDir and `--maxWorkers=1` were used. The ignored local node_modules link was restored; private dependency overlay/cache were removed. No shared dependency files, links or caches were written.

`git diff --check 35820a603a623e83c16a59cc397dd3079b228011 751f7703d22f0e8026e2926f93f64d69c65212fd`: exit 0. No full suite, build, tsc, browser, socket/live-server suite or install run.

## Readiness and limits

Ready for the manager to accept this exact refresh through its merge queue. No blocker or deviation from the settled decisions. Downstream root/package/mobile-label capture composition remains a separate step: preserve the MAIN17 sheet and route its Name input through the later capture port as the canonical design specifies, then qualify that resulting tree. This approval does not cover those later changes or a real touch/browser/Runtime round trip. The manager retains ownership of the post-batch full gate.

The requested report is saved both here in canonical ORCH design and in the worker's `design/app-main17-independent-refresh-review.md`, with a durable copy in its ORCH worker directory. Existing repo `*.md` ignore means the local report will not enter a plain harness `git add -A`; no ignore rules or Git metadata were changed and no KEEP marker was created. Commit message and DONE are supplied in the assigned worker directory.
