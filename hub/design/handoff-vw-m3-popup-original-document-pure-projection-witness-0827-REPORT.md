# Original popup SWAP pure projection witness

## Verdict

**PURE projector comparison completed on the original supplied `swap.output`.**

This is a source projection witness only. It is not Runtime acceptance, an
accepted publication/head, a SWAP qualification, browser/player evidence, or
full-suite evidence. The supplied output has parent revision
`authoring-parent-revision-d35a5f7f583efa7dfd35b1d753cb32828cc5883957a1b396696c1e433871e09b`
and no Runtime publication receipt or accepted-head identity. That authority gap
remains open; none was fabricated.

## Exact source and retained authored data

- Native handoff file SHA256: `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46`.
- Parsed `swap.output` compact-JSON SHA256: `4d6c769a1e958af371b6b86a9d7137486a10a32156ba956140f4ae90e9ddc0ee`.
- Occurrence A: `occ-a`, materialized shot `shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f`, start 8000 ms, duration 10000 ms.
- Occurrence B: `occ-b`, shot `chapter-shot`, start 10000 ms, duration 10000 ms.
- Raw child data was retained: `track=picture`, `at=1`, `hold=4`, `from=2`, `to=6`, `speed=2`. A's swapped asset is `reserved-new`; B retains `picture`.
- Output FPS remained the rational object `{numerator:30000,denominator:1001}`.

The flat actual vectors are in
`handoff-vw-m3-popup-original-document-pure-projection-witness-0827-vectors.json`.

## Actual local versus accepted projection

The local function was called with `clampToOccurrenceDuration: false`; the
accepted function was called with its default cap. Both were the existing
`projectCanonicalComposition` implementation, followed by the existing
`buildTimelineData` resolver. Resolved vectors matched their corresponding
projected config vectors.

| projected row | local | accepted |
|---|---|---|
| `occ-a:clip-a` | `at=9, from=2, to=6, speed=2, asset=reserved-new` | `at=9, from=2, to=4, speed=2, asset=reserved-new` |
| `occ-a:clip-b` | present: `at=13, hold=2` | omitted |
| `occ-b:clip-a` | `at=11, from=2, to=6, speed=2` | unchanged |
| `occ-b:clip-b` | `at=15, hold=2` | unchanged |

The first differing derived field is **`occ-a:clip-a.to`**, local `6` versus
accepted `4`. The cap is applied at
`src/tools/video-editor/data/shotCompositionProjection.ts:442-448`; the
derived omission of a child starting at the effective end is at lines 442-444.
The effective A duration is 2000 ms because the same-lane B occurrence starts
at 10000 ms. The authored source window remains `[from,to)=[2,6)`; projection
does not rewrite it.

The accepted projection call used by the command-session path is visible at
`src/tools/video-editor/hooks/useTimelineCommandSession.ts:106-120`. The
local popup/recovery path uses the unclamped option at
`src/tools/travel-between-images/components/shotTimelineDataProvider.ts:438`
and `:476-480`.

## Evidence and limits

Passed:

```text
TMPDIR="$PWD/.tmp-vw-m3" node node_modules/vitest/vitest.mjs run --no-cache --silent=false --reporter=verbose --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/data/popupProjectionWitness.temp.test.ts
1 test file passed; 1 test passed; exit 0
```

Also checked `git diff --check` after removing the temporary probe. No full
suite, browser, localhost/live socket, Runtime, helper, renderer, mounted UI,
install, package change, or retry was run. No product/test assertion/pin/API/
DTO/store change was made.

## Handoff decision

Pass the vectors to Agent/App as a **PURE projector comparison on the supplied
golden**. Keep the original raw timing and child references, the rational FPS,
and the existing effective-duration cap. Do not call this Runtime acceptance or
full SWAP qualification until HOME supplies an actual accepted closure with
head/publication identity and corresponding accepted/local projections.
