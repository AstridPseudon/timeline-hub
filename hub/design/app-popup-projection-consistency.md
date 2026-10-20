# Popup local/accepted projection consistency

2026-10-20. Source-only investigation at App `309cb7a463833126e3af730fb3c6ff536d9e457c`.
Product unchanged. M2/M3 integration and popup writer retirement remain held.

## Finding

**The same native ADD after-document produces different local and accepted-path
config/resolved-config vectors. Authored data remains intact.** This is an
executable representation gap, not evidence of different pixels or audio, and
not sufficient evidence to change film policy.

The native fixture is `src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json`.
Both original input and actual `add.output` were used without editing pins,
rows, manifests or fixture output. The focused case opens BOTH documents with
`authoringBundleFromDocument`, captures ADD from the original input, and checks
exact native command/record equality plus complete per-occurrence internal
payload equality against the reopened output. This includes the untouched
shared-shot occurrence and full registry/opaque/null data.

Both graphs come from `RuntimeDataProvider.shotComposition.loadAtHead`, with a
bounded transport serving the fixture's normal raw parent/shot/internal revision
images. This exercises the actual private `runtimeGraphToContract` and normal
asset normalization, followed by `createShotCompositionAdapter.prepare`.
It does not use `occurrenceMediaFixtureGraph`: that helper takes occurrences and
asset descriptors from the original fixture input and cannot model output's
materialized shot identity accurately. No product graph adapter was exported or
modified for the test.

The local path applies `occurrenceMediaPreview`/`projectOccurrenceMediaPreview`
to the captured bundle over the input graph. Independently, the case reopens the
actual output and applies the local helper over the output graph. Their selected
clip vectors agree. The accepted-path comparison uses the SAME prepared output
graph with `projectCanonicalComposition(prepared)` and `buildTimelineData`, the
exact projection/build operations used at `useTimelineCommandSession.ts:83-95`.
This avoids the original session test's project double, which resets to the
original basis and reapplies only unsent previews.

## Observed vectors

These differences occur in both `config.clips` and `resolvedConfig.clips`:

| Row | Local full authored projection | Default accepted-path projection |
| --- | --- | --- |
| `occ-a:reserved-child` | at 8.125, from 2, to 6, speed 2 | at 8.125, from 2, to 5.75, speed 2 |
| `occ-a:clip-a` | at 9, from 2, to 6, speed 2 | at 9, from 2, to 4, speed 2 |
| `occ-a:clip-b` | at 13, hold 2 | omitted from this derived output |
| Parent rows and occurrence B | unchanged | unchanged |

There are seven local clip vectors and six default projection vectors. Selected
media identities agree on surviving rows; the new asset resolves to the original
native selection's `sha256:222…222` object. The output graph uses the actual new
shot/internal IDs, not the base's original IDs. The comparisons exclude canonical
revision provenance, which legitimately changes after materialization.

The fixture places A at 8000 ms and B at 10000 ms on the same lane. Existing
`timelineOccurrenceEffectiveDurationMs` derives A's 2000 ms hard boundary.
`projectClip` at `shotCompositionProjection.ts:437-447` caps its render-facing
trim to `from + remainingSeconds * speed`: `2 + (10 - 8.125) * 2 = 5.75`.
The default projector removes rows starting beyond that bound. The local helper
at `occurrenceMediaGesture.ts:102-103` opts out of the clamp. `canonicalTiming`
still records the pre-clamp duration and occurrence bound; it is not evidence
that Player or audio duration actually follows either source endpoint.

**Raw authored row stays exactly** `{at:0.125, hold:4, from:2, to:6, speed:2,
params:null, opaque:[null,false,{}], ...}` in the fixture after-document and
reopened authoring bundle before AND after both projections. The default `to`
5.75 is a derived visible cut bound, not a rewrite of the authored source window.
The prior qualification report's “silently shortened the ADD source window”
needs this narrower interpretation: it observed a projected field, not lost
canonical data. Its original full-source-window tests must remain unchanged.

## Projection facts and limits

The local display basis is the fixture input revision `parent-1`; submission
ACK must not rewrite this original local base fact. The output graph's actual
head is `authoring-parent-revision-42658224c1e68d235fde4217283034a46083238d6c9b5b4f4075d12360536a6f`.
The native fixture has NO publication receipt. The test deliberately gives neither
head a publication ID, fabricates no accepted identity or `editProjection`, and
asserts that no `accepted_identity` appears. Thus “accepted-path” here means its
actual deterministic projector, not a claim that Runtime accepted this fixture.
In production the hook distinguishes `{kind:local, base, generation}` from
`{kind:accepted, head}` only with the real revision/publication pair
(`useTimelineCommandSession.ts:107-109`). Live ACK/accepted fact adoption is UNRUN.

No mounted accepted closure, Runtime acceptance, outbox browser recovery, frame,
audio, export or physical film parity is established. No policy/authority field,
renderer bypass, fixture overlay or inline authority was added.

## Regression and smallest follow-up

One focused regression was executed with both config and resolved-config parity
assertions. All fixture/raw/binding/normal-adapter/no-snapshot assertions passed;
BOTH parity assertions failed with the differences above. Under the task's
explicit rule for a source-only red regression, the exact test is retained in
[worker notes](../workers/app-m2-popup-projection-consistency/notes/occurrenceMediaProjectionConsistency.test.ts),
outside the main suite pending contract review. No failing test was committed,
no `it.fails`/skip was introduced, and no expectation was inverted to bless the
gap. Restore it at `src/tools/video-editor/commands/occurrenceMediaProjectionConsistency.test.ts`
for the next owner qualification; imports are relative to that original path.

The narrow App seam is local helper `projectCanonicalComposition` at line 102
versus accepted hook projection at line 84. Both already call the same projector;
the caller's clamp option differs. This evidence does not settle whether popup
authoring geometry and film-visible bounds should be separate representations,
or which film interval the one compiler should emit. There is consequently NO
clear settled App-only product fix to propose as ready to land.

Recommended owner follow-up: give Agent + Viewing this exact unchanged closure
and the two vectors; have their existing compiler/domain playback path determine
the render-facing vector for both local candidate and accepted closure. Then
wire that same compiled result at the two existing App projection callsites,
while preserving the raw `AuthoringBundle` for editing. Review the existing
`project_runtime_parent_composition`/one-compiler work; do not add a second
projector or infer new policy from this test. If a distinct local authoring view
is intended, qualify its render consumer explicitly. Do not switch the global
clamp or trim canonical data to force this equality test green. No UI writer
retirement before that review and real popup acceptance/reload/undo/retry/zero-
legacy qualification. PLAN's M1 record and M2/M3 merge holds remain in force.
