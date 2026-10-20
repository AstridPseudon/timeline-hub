## Suggested addition to design/app-popup-projection-consistency.md

Manager-owned proposal only; this worker has not edited the shared document.

### Exact native ADD confirmation — response to orchestrator 04:57

The unchanged actual `recipe_m2_occurrence_media.json:add.output` authors A at [8,18) seconds and B at [10,20), both on `picture`. RuntimeDataProvider's actual raw graph adapter and the normal shot adapter preserve those 10-second occurrence durations. App's existing timing functions derive effective spans [8,10) for A (next same-lane blocker B) and [10,17) for B (7-second child content extent). This is actual overlapping fixture content, not a hypothetical overhang beyond A's authored end.

The reported 270/330/60 and 330/390/60 identify the existing `clip-a` children in the local **unbounded** projection when the real frame helpers receive numeric 30000/1001. They do not identify the newly added `reserved-child`, which has occurrence-local at .125 and global at 8.125; its corresponding unbounded numeric diagnostic is 244/304/60.

Clamp IS exercised: default accepted-path App projection yields A clip-a at9/from2/to4/speed2 and the new child at8.125/from2/to5.75/speed2; A clip-b at13 is omitted. The raw [2,6) source windows and all authored rows remain unchanged. The local helper preserves seven unbounded rows in config/resolvedConfig. Applying the existing renderer boundary helper to local rows yields the same six row geometries as applying it to default accepted-path rows. Numerically converted frame diagnostics are A clip-a 270/300/30, new child 244/300/56, B clip-a 330/390/60. Therefore the earlier 7-vs-6 config comparison does not establish different rendered pixels/audio.

There is also an input-format mismatch: the actual native FPS object `{numerator:30000,denominator:1001}` survives buildTimelineData; the App's numeric frame helpers return NaN when given that unchanged value. All finite triples above explicitly use a diagnostic numeric argument conversion, without changing the fixture or any config. They are not actual native playable UI frames or an Agent-compiled artifact.

This is production-function evidence, not real mouse/mounted UI, public-scene evaluation, Runtime acceptance or pixels/audio. No accepted revision/publication pair was fabricated. The exact new probe plus four focused existing suites passed 228 tests; the original unchanged parity reproduction still fails both soft equality checks and remains in notes. Fixture SHA256 remains `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46`.

No fixture correction or policy flip follows from this evidence. Agent/Viewing should reconcile the exact closure, row identities, FPS input shape and projection stage through the ONE compiler/reference qualification before popup retirement. Worker report: `workers/app-m2-popup-exact-vector-confirm-r1` worktree `notes/report.md`; shared dependencies were not changed and do not certify the base's locked Composition release.
