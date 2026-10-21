# D01-app-popup-swap report

Result: **missing original accepted evidence; no qualified SWAP projection
verdict**.

The exact packet is
`/home/user/timeline-hub/hub/design/handoff-vw-m3-popup-analog-playable-vp8-native.json`
(`swap` object), mirrored by
`handoff-agent-expanded-recipe_m2_occurrence_media.json`. It is a portable
Agent golden: `swap.input` uses `parent-1`, `swap.output` uses an
`authoring-parent-revision-*`, and neither has a Runtime publication/accepted
identity. It therefore cannot prove a LOCAL-versus-ACCEPTED pair.

The Agent SWAP command is `occurrence.swap-media` v1 targeting raw
`occurrence:occ-a/clip:clip-a`. Its only semantic writes are the new scoped
asset birth and the target asset binding `picture -> reserved-new`. Authored
timing is preserved (`at=1, hold=4, from=2, to=6, speed=2`); Agent’s contract
defines these as child-relative/source units. The output’s new shot/revision
IDs are materialization provenance.

Existing App seam: accepted projection calls
`projectCanonicalComposition` with default cap
(`useTimelineCommandSession.ts:106-111`); `projectClip` caps active trims at
`shotCompositionProjection.ts:442-452`, while the prior ADD investigation’s
local editor path opts out of that cap. Conditional arithmetic for this same
geometry is `occ-a:clip-a.to 6 -> 4`, with `occ-a:clip-b` omitted; B is
unchanged. This was not observed on a SWAP local/accepted pair. The first
derived difference would be `occ-a:clip-a.to`; authored timing remains `[2,6)`.

Keep MAIN visible reference/stored cap. Do not flip defaults, clamp authored
data, or add a second compiler/carrier. HOME still needs an actual accepted
closure with head/publication identity and matching local/accepted SWAP
vectors. No product/assertion changes or proof retries were made.

Evidence/limits: source inspection only; no tests, Runtime, browser, renderer,
socket, central, full, acceptance, reload, undo, retry, frame/audio/export
qualification.
