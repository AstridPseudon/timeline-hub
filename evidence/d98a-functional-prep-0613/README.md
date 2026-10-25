# D98a functional source preparation (Runtime)

This packet prepares one later functional proof on the existing D73 route. It
does not claim a body result, functional PASS, semantic verdict, or GO/NO-GO.
No body, preflight, provider, pytest, collection, import, fixture, CLI,
browser, observer, collector, route install, CAS, or live request was run.

The exact ready set is the three original selectors retained by the unchanged
D98 handoff: one occurrence, one placement, and one recipe case. The Agent
normal source is `a90bc7f9e1` and the latest read-only Agent head carrying the
same D98a file is `01d51620a6`; both resolve the candidate file blob
`c4f54e34536dabbf196fd9a17c337b78394506e3`. The source change replaces the
raw `occurrence.create` with the registered `capture_occurrence_create`,
preserving `occ-a`, `chapter-shot`, `Chapter One`, `picture`, `on=8`, and
`duration=10`.

The placement and recipe selectors are genuinely dependent on the changed
fixture: placement imports `_create_fixture` from the changed occurrence-media
module, and the recipe imports that module as `runtime_occurrence` for its
Runtime-backed path. They are therefore retained even though their owning
files have no source diff. The source review found the four test-function ASTs
conserved; the only top-level function change is `_create_fixture`.

The prior actual D98a request remains immutable: central ID
`rt-D98a-route-submit-0517-rt-D98a-route-submit-0517-1025052025-32278`, three
errors, no failures, and no skips. Its active observer records are historical
diagnostic input only, not a new observer budget or a reason to repeat it.

All other 48/shared-family cases remain functional-but-unqualified. This
packet does not blanket-cure them, reclassify them, or claim coverage for them.

## Body gate

The later body must first capture a fresh four-repository tuple after the
reviewed D102c context fix is released and the Agent normal tools have adopted
it. The current known-bad Runtime `689352013...` tuple is explicitly
ineligible. The packet records the current Runtime base and the reviewed future
D102c source only; it does not manually pin a lock or claim that tuple exists.

The body must use the existing central D73 runner once, with the selector file
in `inputs/selectors.txt`, a fresh captured tuple, the original authority,
ABI/ABA, no-write/no-leak, CAS, UTC, outside-byte, and 45-second controls.
Use the existing runner's normal positive control exactly once, poison control
zero times, cache off, `-n 3`, and no `-m` override. Persist the central request
ID immediately and reuse it after restart. A real accepted/merged/refused
receipt and per-ID outcomes are required before any semantic accounting.
