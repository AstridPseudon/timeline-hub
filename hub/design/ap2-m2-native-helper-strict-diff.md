# AP2 M2 native-helper strict-TypeScript differential

## Snapshot location

The finished baseline/current snapshots used for this differential are
retained outside the synced design root at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-hub-large-artifact-repair/artifacts/ap2-m2-native-helper-strict-diff/`

The old `design/ap2-m2-native-helper-strict-diff/` path is intentionally
absent. Snapshot contents and shared dependency symlinks were not changed.

## Result

The four helper units introduce **5 new TypeScript diagnostics** under the real
App ES2020 project check. The ordinary `typecheck:strict-probe` command passes,
but it does not include any of these helpers. No source, config, dependency,
test, or worktree file was changed.

## Compared trees and environment

- Baseline: `590c19795111fd1891bbd50a5f8d48bef3505a26`.
- Current: `ea38656fe62950440b36cafee780698cff2c3f9c`.
- Both were extracted with `git archive` into private directories under this
  report's design workspace and compiled with the same read-only
  `/home/user/work/app/node_modules` (`@banodoco/timeline-composition` reports
  version `0.0.8`).
- `tsconfig.app.json` uses `target: ES2020`, `module: ESNext`, bundler module
  resolution, and strict mode.

## Exact differential

Command in each private archive:

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

| Tree | Exit | Diagnostics |
|---|---:|---:|
| `590c19795` | 2 | 11 |
| `ea38656fe` | 2 | 21 |

All 11 baseline diagnostics remain unchanged in the current tree:

- `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:1`
  (`CompiledCanonicalTransitions` export missing).
- `src/tools/video-editor/compositions/TimelineRenderer.tsx:1,1309,1607`
  (missing export and two implicit-`any` parameters).
- `src/tools/video-editor/compositions/VisualClip.tsx:642`
  (`DrawPlan.incomingPolicy` missing).
- `src/tools/video-editor/compositions/playerEvaluation.ts:1,3,7,79,84`
  (missing exports, implicit-`any`, and an arity mismatch).
- `src/tools/video-editor/lib/config-utils.ts:43` (`computeMediaTrim` export
  missing).

The 10 current-only diagnostics split as follows:

### New helper diagnostics: 5

- `elementCapture.ts:236` — `supplied.select` remains `string | null` at the
  `state.entity` call despite the preceding assertion.
- `genericPatchCapture.ts:306` — `command.args.values.hold` remains `JSON`
  when passed to `clipHold`, whose parameter is `number`.
- `occurrenceDuplicateCapture.ts:83` — the replacement `state.get` function's
  inferred object-literal union is not assignable to `AgentState`; nested
  `state` literals widen and the nested `value` shape does not satisfy `JSON`.
- `occurrenceDuplicateCapture.ts:195` — `documentId` can still be `JSON`, not
  `string`, for `stableOccurrenceDeepLink`.
- `occurrenceDuplicateCapture.ts:199` — the same `documentId` narrowing issue
  for `stableOutputIdentity`.

`parentClipAddCapture.ts` produces no TypeScript diagnostic.

### Unrelated current-only Composition/package diagnostics: 5

- `src/tools/video-editor/compositions/AudioTrack.tsx:15,16,18` — three
  exports/types absent from the installed Composition package.
- `src/tools/video-editor/compositions/compiledAudioSourceClock.ts:1` — two
  absent Composition exports (`getSanitizedPlaybackRate`, `computeMediaTrim`).

These five are outside the helper delta and are consistent with the current
source/package skew: the current `package.json` and lockfile request the
vendored `0.0.13` artifact while the shared local install is `0.0.8`.

## Strict-probe scope and packet claim check

Exact command in both private archives:

```text
npm run typecheck:strict-probe
```

Result: **exit 0** for both baseline and current. The command expands to:

```text
npm run typecheck:strict-islands
tsc -p tsconfig.strict-islands.json --noEmit
```

The strict-islands `include` list names only these project files:

```text
src/app/hooks/useAppExternalDrop.ts
src/integrations/supabase/bootstrap/createSupabaseClient.ts
src/integrations/supabase/bootstrap/fetchWithTimeout.ts
src/integrations/supabase/config/env.ts
src/shared/components/MediaGallery/hooks/useMediaGalleryDebugTools.ts
```

plus the two declaration files `src/vite-env.d.ts` and
`src/types/browser-extensions.d.ts`. None of the four helper units, their
command directory, or Composition files are in that configured root scope.
The duplicate packet's claim that its private candidate passed
`npm run typecheck:strict-probe` is therefore accurate as a strict-islands
result, but it is not helper qualification. The ordinary packet's separate
private `tsc --noEmit --pretty false` claim applies to its distinct candidate;
it is not evidence that current `ea38656fe` is clean, where the real App check
has the 21 diagnostics above.

## Minimal repair recommendations

1. In `elementCapture.ts`, assign `supplied.select` to a local, assert that
   local, and use the narrowed local for subsequent entity/registry reads.
2. In `genericPatchCapture.ts`, retain the result of the existing numeric
   validator in a `number` local and pass that value to `clipHold` and `write`.
3. In `occurrenceDuplicateCapture.ts`, give the `state.get` replacement an
   explicit `AgentState` return type (with explicit nested state typing where
   needed), and validate/narrow `bundle.timeline_id` to a string before using
   it as the `documentId` fallback.

These are type-narrowing repairs only; no behavior change is recommended. The
Composition/package diagnostics need the separately owned package alignment
or a qualified `0.0.13` dependency environment.

## Tests and limits

Not run, per task scope: Vitest, full App suite, browser, localhost, socket,
Runtime, or matrix tests. The focused build-result commands above were run
directly; no test expectations were changed or weakened.

Recommended next step: apply the three minimal helper typing repairs, rerun
the exact ES2020 App check and `npm run typecheck:strict-probe`, then separately
resolve the Composition artifact/install mismatch before treating the full App
typecheck as green.
