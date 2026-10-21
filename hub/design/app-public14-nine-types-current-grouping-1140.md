# App public14 r26: nine TypeScript diagnostics

Date: 2026-10-21 UTC

## Verdict

The retained r26 qualification is an actual TypeScript 5.9.3 run of the
committed `tl/app-m3-composition14-normal-app-pin-stage-r26` tree, with the
original App flags and the isolated actual-14 leaf. It reported exactly nine
non-duration diagnostics. The leaf had 2,558 roots, not the historical 2,549
root manifest; therefore this report does not claim the historical program
shape or `wholeprogram0`.

All nine diagnostics are from App source that is byte-identical on the
public13 parent (`HEAD^` here). The public14 pin commit changed only:

```text
config/vite/timelineCompositionPackage.test.mjs
package-lock.json
package.json
vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz
```

The five affected App files have equal SHA-256 at `HEAD` and `HEAD^`:

```text
src/tools/video-editor/commands/clipScalarGesture.ts       74eb7372061c32b179dac01788592dbc8ad102bc0e623b77fa6efe0fc0cc79d4
src/tools/video-editor/commands/commitSession.ts            49048350e766da471cd82f3c34ad01bf0106aa19ed7e8d5c9119457247af5e71
src/tools/video-editor/commands/occurrenceMediaCapture.ts   5d320f0c8aea06d97cabd18f90b0918a5e5f71b58b963e58f0f43dd2d8077456
src/tools/video-editor/commands/sessionPlacement.ts         89bbf06a7953a79dd8d311fe761ffff0912dd203a72ecbcb4409c421f380531d
src/tools/video-editor/contexts/VideoEditorProvider.tsx     71126e5b8e84b39a6c43a100301311e892462229891cc94edcf268392c0ff797
```

The seven old duration diagnostics are a separate Viewing/package issue. The
public14 archive changes `package/dist/lib/duration.d.ts` only from
`getTimelineDurationInFrames(timeline: TimelineConfig, fps: number)` to the
generic `T extends Pick<TimelineConfig, "clips">` form. The r26 stderr reports
no duration diagnostics after that pin. This is why the seven are gone; it is
not evidence that the App program is clean.

## Exact nine and ownership

| # | Diagnostic | Provenance on public13 | Owner | Smallest valid direction / test |
|---:|---|---|---|---|
| 1 | `src/tools/video-editor/commands/clipScalarGesture.ts:26:37` — **TS2322**, `clear` can contain `"elementRef"` but `TimelinePatchOperation.clear` permits only `"hold" \| "asset" \| "transition"`. | Same source; introduced by `59146ad410` (the dormant App2 scalar carrier). The local patch type at `src/sdk/video/timeline/patch.ts:95-96` is unchanged. | **App2** | App2 must supply the exact peer hunk for `clipScalarGesture.ts:23-29`: preserve the four-key command input and paired transition/reference semantics, but emit only the public `TimelinePatch` clear shape unless and until the matched Agent contract changes it. Do not widen the SDK patch type or add a cast. Run `clipScalarGesture.test.ts`, `clipScalarCapture.test.ts`, and `commitSession.clipScalar.test.ts`; retain explicit paired-clear/preview expectations. |
| 2 | `src/tools/video-editor/commands/commitSession.ts:1243:15` — **TS18046**, `originalDocument.parent_revision.payload.occurrences` is `unknown`. | Same source; the block was introduced by HOME automatic-placement commit `4c57cde9f5`. `ParentComposition` is `Record<string, unknown>` in the unchanged generated local types. | **HOME** | Narrow the collection with an existing structural guard (`Array.isArray` or the existing accepted-document helper) before reading `.length`; preserve the empty/non-empty graph decision. Run `commitSession.placement.test.ts` and its recovery/empty-occurrence neighbors. |
| 3 | `src/tools/video-editor/commands/occurrenceMediaCapture.ts:128:34` — **TS2345**, `ObjectValue` selection is not assignable to generated `AgentSelection`. | Same source; popup capture commit `56bcf8780f` is present in both public13 and r26. | **HOME** | Give `selectionValue` the generated `AgentSelection` return type (or construct the same typed value) rather than asserting a cast. Run `occurrenceMediaCapture.test.ts` and direct command-session occurrence-media tests. |
| 4 | `src/tools/video-editor/commands/occurrenceMediaCapture.ts:136:16` — **TS18048**, `row` may be `undefined`. | Same source and same popup capture commit as #3. `AuthoredState.entity` is intentionally optional. | **HOME** | Refuse a missing owner row before reading `shot_id`, preserving the existing identity-conflict refusal. Run the same occurrence capture/command-session neighbors, including missing-owner coverage. |
| 5 | `src/tools/video-editor/commands/occurrenceMediaCapture.ts:142:103` — **TS2345**, second selection push has the same `ObjectValue` → `AgentSelection` mismatch. | Same source and same commit as #3/#4. | **HOME** | Same single typed `selectionValue` repair as #3; no duplicate type widening. Run the same occurrence capture tests. |
| 6 | `src/tools/video-editor/commands/occurrenceMediaCapture.ts:357:35` — **TS2345**, `basis.command` is still JSON at the `has()` call, while `has` requires an object. | Same source and same popup capture commit as #3–#5. `object()` narrowing is not retained through the callback expression. | **HOME** | Bind a locally narrowed command object after the existing `object(basis.command)` check, then call `has` on that value. Keep the finite-JSON and incomplete-basis refusal; no cast. Run `occurrenceMediaCapture.test.ts` including serialized-basis/rejection cases. |
| 7 | `src/tools/video-editor/commands/sessionPlacement.ts:13:5` — **TS2322**, the capture callback returns domain objects (`OutboxHead`, `CanonicalDocument`, bundles) where `OutboxPlacementCapture` requires `Promise<OutboxJson>`. | Same source; automatic placement commit `4c57cde9f5`, not the package pin. | **HOME** | Serialize the returned capture through the existing outbox JSON boundary while preserving `commands`, `before`, `after`, `preview`, and `displayBasis` shape; do not relax `OutboxJson`. Run `commitSession.placement.test.ts` and native placement capture tests, including reload/recovery serialization. |
| 8 | `src/tools/video-editor/contexts/VideoEditorProvider.tsx:103:45` — **TS2724**, `clientLocalAdapter.ts` does not export `EditorImagePlacementHost` (only the binding function is exported there). | Same source; automatic placement commit `4c57cde9f5`. The type is declared in unchanged `commands/editorImagePlacement.ts`. | **HOME** | Import the type from its defining module and keep the adapter import for the function, or add only a deliberate type re-export if that is the established boundary. Do not alter runtime behavior. Run `VideoEditorProvider.test.tsx` and automatic-placement session tests. |
| 9 | `src/tools/video-editor/contexts/VideoEditorProvider.tsx:867:21` — **TS7006**, `notify` has implicit `any`. | Same source and same automatic-placement commit as #7/#8. | **HOME** | Annotate the callback as `() => void` (matching `subscribeRuntimeTaskUpdates`) or restore direct contextual typing without changing subscription behavior. Run Provider and placement-session neighbors. |

Counts: HOME 8, App2 1, Viewing 0. Viewing's ownership is limited here to
the seven removed package-duration diagnostics; no current nine should be
changed in Composition or by a package declaration override.

## App2 peer request

Do not edit #1 in this branch. Request from App2 one exact, source-only hunk
for `src/tools/video-editor/commands/clipScalarGesture.ts:23-29`, with the
following constraints:

1. `ClipScalarArgs.clear` remains the existing four-key command-side shape;
2. the local `TimelinePatch` remains the current public13/public14 shape and
   does not gain `elementRef` by cast or assertion;
3. transition-only RESET remains `clear: ["transition"]`, while paired
   transition/reference behavior stays represented by the command carrier;
4. existing preview and atomic batch tests remain assertions, not weakened
   or converted to skips/expected failures.

If App2's intended hunk requires an Agent/Runtime schema change, return that
as a matched peer request instead of widening this App-only type. HOME must
not compete on this file.

## Known-invalid environment and limits

The historical 2,549-root claim is not reproducible from this committed
current integration snapshot without changing the source/program manifest;
the retained actual leaf parsed 2,558 roots. That count mismatch is an
environment/manifest distinction, not grounds to discard the nine diagnostics.
Conversely, the nine are not artifacts of the public14 archive: the source
files are byte-identical to public13, and the pin diff contains no source
changes. The only archive type difference relevant to the earlier duration
errors is the generic duration declaration documented above.

No product source was changed in this diagnosis. No new TSC/program run,
install, browser, build, graph, full suite, generated edit, cast, assertion
weakening, or private declaration override was performed.

## Evidence commands and retained results

Retained qualification log:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-composition14-normal-app-pin-stage-r26/log.txt`

The recorded actual leaf command used TypeScript `5.9.3`, original
`tsconfig.app.json` flags, 4 GB heap, and serialized locks; it reported the
nine diagnostics above and exited nonzero. The r26 worker also recorded
private 0.0.14 package/export/Scene-clock/PCM qualification **PASS**, package
boundary **10/10**, public13 preflight **5/5**, and `git diff --check`
**PASS**. Those are retained r26 results, not re-run here.

Read-only checks performed for this report:

```text
git diff --name-status HEAD^ HEAD
git diff --quiet HEAD^ HEAD -- <each of the five affected files>
sha256sum <each affected file>; git show HEAD^:<file> | sha256sum
git blame -L <diagnostic lines> <affected file>
diff -u <public13 archive duration.d.ts> <public14 archive duration.d.ts>
```

All five source comparisons returned identical SHA-256 values; the pin-only
path list and the one-line duration declaration diff support the provenance
classification above. No tests were run for this read-only diagnosis.

## Next step

App2 should return the exact #1 hunk and its focused test result. HOME may
then repair only its eight owned groups in separate bounded source tasks,
with focused tests per the table. Viewing need not change the package pin or
the current nine-diagnostic fixes.
