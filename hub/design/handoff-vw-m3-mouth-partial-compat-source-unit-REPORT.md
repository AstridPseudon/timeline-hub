# D09b/c bounded presenter compatibility source unit

## Result

Updated only the am-presenter source seam and its direct registered tests. The
component's natural drawing normalization remains `mouthAnchor`/`motionAt`:
partial `{x: 151, y: 104}` still draws as `{x: 151, y: 104, w: 19}`, and the
malformed example still normalizes safely to `{x: 151, y: 104, w: 40}`. The
compatibility inspection ROI now retains the legacy input contract through the
existing `mouthInspectionRect`/`mouthEraseRect`/`pixelGeometry` seam:

| raw mouth input | registered compatibility result at frame 0 | pixel crop at 640x360 |
|---|---|---|
| explicit `{x:151,y:104,w:19}` | known, logical padded footprint | `(298,202,345,219)`, 799 px |
| partial `{x:151,y:104}` | known, legacy width 16 with actual x/y | `(298,202,339,219)`, 697 px |
| absent/default | unknown; no inspection | old consumer's `None` skip remains |
| malformed `{x:'bad',y:null,w:900}` | unknown; no fabricated crop | raw-invalid rule retained |

Mosaic and unsupported outer geometry remain unknown. `presence` remains
unknown and `opaqueSupport` remains none. The explicit four-still 799/387,
strict `>2%` proof and the private crop/statistics consumer were not changed.
No new public context/type/DTO/authored field/factory, clock/hash/geometry
copy, consumer migration, capture, or deletion was added.

## Raw-context evidence

- The existing drawing path calls `mouthAnchor(raw)` and `mouthEraseRect(m)`;
  the compatibility seam reuses those helpers and only supplies legacy width
  16 when authored `w` is absent.
- The old Python `model.mouth_box` returns `None` for an absent mouth, returns
  `(894,606,1014,654)` for the partial `{x:151,y:104}` case, and the new
  registered scene returns the matching padded logical geometry. This is why
  partial is 697 px and not the explicit 799 px denominator.
- The scene continues to publish the existing `motionAt` scalar/codebook
  independently of compatibility ROI eligibility; no blanket semantic
  unknown was introduced.

## Verification and limits

The registered scene/crop tests pass with exact explicit, partial, default and
raw-invalid assertions; the full direct targeted group is `55 passed, 2
skipped`. The skips are existing esbuild-dependent neighbour tests. No browser,
render, socket, full suite, network, install, or central capture was run.

`artifacts.json` was deliberately not regenerated because the task forbids pin
changes. Its read-only check reports the three changed am-presenter source
entries as stale; the Agent owner/integration step must regenerate that
manifest in its own allowed pin-update unit before the repository manifest gate.
