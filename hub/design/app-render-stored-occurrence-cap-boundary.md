# App stored-occurrence render cap boundary

**BLOCKED at the existing command display handoff. Required exact regression retained RED; no production repair or KEEP-for-merge claim.** MAIN's stored4000/hold4/end120/f105=0.5 decision is accepted. This is the brief's explicit stop for a missing verified, constraint-compatible cap seam, not a request to reconsider that policy. `KEEP` retains the regression and proposal for review; no `DONE`.

## Source and delivered delta

- Base/current HEAD: `927545cf5`, MAIN17/public12/Runtime013. Read PLAN, latest App INBOX through12:45 relay of12:50, `viewing-main-image-cap-compiled-input-confirmation.md`, `app-main-cap-half-golden.md`, and `app-exact-main-cap-independent-audit.md`.
- Ported exactly two files from held `tl/app-m3-main-cap-confirmed-half-golden` (`a26c7ad5e9eb41185dd68a553b08ff338144fd73`): `src/tools/video-editor/data/mainImageCap.fixture.json` and `canonicalCompositionState.mainImageCap.test.ts`. Both byte-equal; ordinary required assertions unchanged, no xfail/skip. Raw fixture equals the captured source-vector closure, SHA256 `ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04`.
- No existing tracked file changed. Original editor clamp suite remains byte-identical to HEAD. Production, Viewing paths, Main17/mobile/label paths, package/lock/runtime pins, proxy and source guards untouched. Unknown/null/absence/order behavior was not rewritten; original opaque-root and immutable-source neighboring tests pass.

## Concrete seam and why the obvious small patches are incomplete

| Existing path | Exact source | Consequence |
| --- | --- | --- |
| Prepared closure | `shotCompositionAdapter.ts:224` | Original stored4000 is available as occurrence.durationMs. |
| Editor projection | `shotCompositionProjection.ts:505` and `shotCompositionTiming.ts:135` | Effective5000 replaces stored4000 before clip construction. Default editor semantics must remain unchanged. |
| Existing render-cap metadata | `shotCompositionProjection.ts:427` | canonicalTiming.durationMs is child source duration; occurrenceDurationMs is already effective5000. Neither retains the original4000. |
| Existing boundary helper | `lib/canonicalRenderBounds.ts:16` | Can correctly bound a supplied cap, but cannot recover stored4000 from effective5000. |
| Verified command projection | `hooks/useTimelineCommandSession.ts:70–112` | The original accepted graph exists inside the callback. One default editor projection builds config/resolvedConfig/rows. The installed editProjection retains IDs/generation, not the original graph or cap. Graph adoption happens separately, only without pending previews. |
| Immediate local command preview | `hooks/useTimelineCommandSession.ts:128` | Applies a patch to the installed editor data; no original stored cap is introduced. Recovery likewise starts with the default editor projection. |
| Actual command preview selection, Viewing-owned | `components/PreviewPanel/useVideoEditorPreviewComposition.ts:29–39` | A complete fact-bearing config bypasses the prepared-graph resolver and returns timelineData.resolvedConfig directly. A resolver-only fix cannot repair local/accepted command output. |
| Revision pairing, Viewing-owned | `components/PreviewPanel/useVideoEditorPreviewSurface.tsx:45` | Fact pairing currently requires previewConfig === timelineData.resolvedConfig. Returning a newly bounded copy also needs a coordinated pairing change. |

The external controlled prepared-input diagnostic changes only occurrence.durationMs from4000 to4500, and the existing projector outputs strictly identical configs. This diagnostic does not claim two accepted revisions share one immutable head. It demonstrates that the flattened geometry/timing has lost the value needed by a downstream cap option. Head IDs remain opaque identifiers, not an encoded duration.

A default min(stored,effective) would break the unchanged original stored2000→next4000 editor positive. Switching the command producer's sole config to stored-bound geometry would also change editor/read geometry. Overloading existing canonicalTiming.durationMs with a different meaning would alter its source-duration contract. Reading runtime.shots' independent current graph would not establish pairing with the retained local/accepted fact. No such shortcut was applied.

## Exact proposal / owner handoff

`workers/app-m3-render-stored-occurrence-cap-boundary/notes/graph-only-INCOMPLETE.patch` contains an **unapplied two-file partial diff**, deliberately named INCOMPLETE:

1. Extend existing CanonicalCompositionProjectionOptions with an invocation-only `occurrenceDuration?: 'effective' | 'stored'`; default remains effective. Select stored occurrence.durationMs before projectClip only for the stored invocation.
2. Have the render-only `resolveCanonicalComposition` invoke the existing projector with that stored option. This uses the same projector and ordinary bounded clip input; no compiler or data field is added.

This is the smallest graph-side boundary change, but it is **not a complete proposed merge**: command producers still install the editor config and the Viewing command branch still bypasses this resolver. Do not merge the graph-only patch or treat its potential exact-test pass as end-to-end repair. No production experiment was applied.

The missing shared seam is specifically `useTimelineCommandSession.ts:82–106` → `useVideoEditorPreviewComposition.ts:29–39` → `useVideoEditorPreviewSurface.tsx:45–49`. App and Viewing need a jointly reviewed way to select stored-bounded input from the original verified closure at this handoff, for immediate local previews, recovery and accepted snapshots, and pair the delivered config/vector/revision together. It must preserve the existing editor/read representation. There is no verified existing carrier at that handoff that does all of this under the no-new-field/store rule. A one-line consumer clamp would still receive5000 today; a newly returned config would also fail the identity pairing above. Request a concrete constraint-compatible shared-seam design/owner grant before implementation. TimelineData.renderConfig remains withdrawn; this report does not propose reviving it.

## Exact verification commands and results

Working directory: `/home/user/work/wt/app-m3-render-stored-occurrence-cap-boundary`. For each invocation below:

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-render-stored-occurrence-cap-boundary/notes
original_deps=$(readlink node_modules)
trap 'ln -sfn "$original_deps" node_modules' EXIT
ln -sfn /tmp/app-coherent-deps12/node_modules node_modules
```

Only this worktree's link was changed; final link restored to `/home/user/work/app/node_modules`. The retained config imports this worktree's standard config, aliases public12/React/Remotion peers to private12, and sets cacheDir to `$N/vite-cache`. No dependency-tree file/link/cache was changed, no install.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts
```

**Exit1, 1 failed file / 1 failed test, 2.88s**, `notes/exact-regression.log`. Exactly three failures: hold5 vs4; f105 opacity1 vs0.5; frame120 still has a layer. f90 opacity1, compiler presence, frame identity and raw closure preservation pass. Actual loader/adapter/resolver/public compiler/scene/opacity helpers are exercised with in-process transport; no real socket or pixel claim.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/data/canonicalCompositionState.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/video-editor/data/shotCompositionTiming.test.ts \
  src/tools/video-editor/data/shotCompositionAdapter.test.ts \
  src/tools/video-editor/data/canonicalShotViewModel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts
```

**Exit0, 13 files / 218 tests passed, 34.10s**, `notes/neighbors.log`. The shotCompositionTiming.test.ts selector names a nonexistent file and matched nothing; timing behavior is covered through the actual projection/adapter tests. This includes original editor positives, read/projection, local/accepted, delayed reads/unmount/recovery races, opaque roots, canonical vectors, sequences, opacity and cap-helper neighbors.

```sh
node /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  "$N/capSeam.test.ts"
git diff --check
```

**Both exit0.** Diagnostic: 1 file / 1 test passed, 2.64s, `notes/cap-seam.log`. It first checks the flattened cap collision, then explicitly supplies the original stored cap to the existing boundCanonicalConfigClips helper and normal compiler/opacity/scene helpers: hold4, f90=1, f105=0.5, frame120 excluded. That bounded input is a controlled test adapter, NOT a repaired production consumer. Byte checks in `notes/preservation.json` confirm both held files/captured raw match, original editor suite unchanged, and zero existing tracked files modified.

No full, central suite, actual render/browser/live socket, tsc, lint, install, build, Agent probe or Git mutation was run. No native tuple qualification, real Runtime acceptance, preview delivery, unified pixel/audio parity, owner-film result or Gate6 claim. Stop after this evidence as instructed. The next step is the shared-seam decision above; current-tuple qualification retains priority.
