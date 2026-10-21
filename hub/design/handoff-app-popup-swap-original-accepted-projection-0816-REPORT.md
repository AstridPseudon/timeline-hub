# D01-app-popup-swap: original accepted-document projection verdict

## Verdict

**MISSING ORIGINAL ACCEPTED EVIDENCE; no qualified SWAP projection verdict.**

The exact popup SWAP packet exists, but it is a portable Agent golden, not an
accepted Runtime document. Its `swap.input` has `parent_revision.revision_id`
`parent-1`; its `swap.output` has an `authoring-parent-revision-*` identity.
Neither contains a Runtime publication/accepted-head identity or receipt. The
packet therefore cannot establish a LOCAL-versus-ACCEPTED projection pair.

Do not promote the ADD-only vector report into SWAP evidence. Do not change the
MAIN visible reference, stored cap, global clamp, or introduce another carrier
or compiler.

## Exact packet and Agent source

- Critical-path row: `orchestrator-critical-path-20261021T0800Z.md`, `D01-app-popup-swap`.
- Exact packet: `handoff-vw-m3-popup-analog-playable-vp8-native.json`, top-level
  `swap` object. The same bytes are mirrored by
  `handoff-agent-expanded-recipe_m2_occurrence_media.json`.
- Agent contract/analysis: `m2-popup-native-contract.md`.
- App ADD-only projection analysis (not SWAP):
  `handoff-app-popup-exact-vector-report.md`,
  `handoff-app-popup-exact-vector-vectors.json`, and
  `app-popup-projection-consistency.md`.

The exact Agent command is `occurrence.swap-media` v1 with raw selector
`occurrence:occ-a/clip:clip-a` and closed `old_media`/`media` five-field
selections. The native output records two authored effects:

1. create `occurrence:occ-a/asset:reserved-new`; and
2. write `occurrence:occ-a/clip:clip-a::asset`, `picture` -> `reserved-new`.

The Agent golden preserves the child’s authored timing and opaque state:
`at=1`, `hold=4`, `from=2`, `to=6`, `speed=2`, clip ID `clip-a`, and the
existing app payload. The output’s changed occurrence/shot/revision IDs are
materialization provenance, not an App timing edit. Agent’s analysis defines
these as child-relative source seconds; `hold` and `[from,to)` are source
units, and speed is applied once for playback duration. No timing field is
changed by SWAP.

## Projection seam and conditional arithmetic

The existing App accepted-path source is
`src/tools/video-editor/hooks/useTimelineCommandSession.ts:106-111`, which
calls `projectCanonicalComposition(composition)` with the default cap. The cap
is implemented at
`src/tools/video-editor/data/shotCompositionProjection.ts:442-452` and
`527-534`: it computes the effective occurrence duration, then bounds active
trimmed clips. The render-only shared boundary is
`src/tools/video-editor/lib/canonicalRenderBounds.ts:14-17,80-105`.

The prior ADD investigation identifies the local editor path as the same
projector with `clampToOccurrenceDuration: false` and the accepted path as the
default projector. For the SWAP packet’s unchanged geometry, the *conditional*
calculation would be:

| Row | Local unbounded projection | Default capped projection |
| --- | --- | --- |
| `occ-a:clip-a` | `at=9, from=2, to=6, speed=2` | `at=9, from=2, to=4, speed=2` |
| `occ-a:clip-b` | `at=13, hold=2` | omitted (starts after A’s effective end) |
| `occ-b:clip-a` | `at=11, from=2, to=6, speed=2` | unchanged |
| `occ-b:clip-b` | `at=15, hold=2` | unchanged |

This is arithmetic from the existing seam, not an observed SWAP local/accepted
vector. The first *derived* field that would differ is `occ-a:clip-a.to`
(`6` versus `4`); no authored field differs between those projections. The
same-lane successor at 10 seconds supplies A’s effective two-second cap. The
source-of-truth authored row remains `[from,to)=[2,6)`.

The ADD-only packet observed the analogous `to`/omission difference and also
reported the rational FPS object `{numerator:30000,denominator:1001}`. The App
frame helper at `src/tools/video-editor/lib/time-grid.ts:47-49` expects a
numeric FPS, so finite frame triples from that report are diagnostics only;
they are not native SWAP playback or accepted render evidence.

## Authority decision and limits

- Authored media authority: Agent’s exact `occurrence.swap-media` command and
  the Runtime-verified old/new immutable selections; the existing raw child
  and registry binding remain authoritative.
- Authored timing authority: the original accepted/source closure, if and when
  an actual accepted closure is supplied. The Agent packet preserves source
  timing and does not authorize App to rewrite it.
- Derived cap authority: the existing occurrence successor/effective-duration
  calculation consumed by `projectCanonicalComposition`; retain the MAIN
  visible reference and stored cap.
- Render boundary authority: the existing `boundCanonicalConfigClips` seam,
  not a second projector or carrier.

No Runtime acceptance, accepted reload, mounted UI, browser, Player, frame,
audio, export, or SWAP local/accepted parity run was performed. No product or
assertion files were changed. The exact next evidence needed from HOME is one
real accepted closure with its head/publication identity plus the corresponding
local and accepted SWAP projections, both traced through the one Agent/native
command source. Until then, D01-app-popup-swap remains open and must not close
the popup writer-retirement chain.
