# Agent → Viewing/App — 2026-10-21 12:09 UTC — D09 legacy fade targeted cut

Agent worktree `c9ac7c7b0e862ad32a919db33859c5fcbf58ad99` remains on the
public13 pin. The bounded patch stages the dormant same-film public14
replacement in:

- `tests/packs/rendering/d09_same_film_public.mjs`
- `tests/packs/rendering/test_d09_same_film_public.py`

The old private assertion
`tests/core/timeline/test_onscreen_more.py::test_a_cross_fade_of_two_full_plates_is_covered_not_dip`
is unchanged. The replacement retains the exact same independent-fade film
and asserts public14 `COVERED/CONTENT [0,16)`, `DIP/None [16,30)`,
`COVERED/CONTENT [30,45)`, followed by GAP. A separate canonical incoming
transition control remains `COVERED/CONTENT [0,60)` with the frame-22 opacity
control and frame-60 GAP.

The qualified Composition14 identity is source `df7b86308902fae90eda1dc3080d17d8fc30ea78`
(tree `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`), archive SHA-256
`21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`.
Agent stage `255b6856cc1c96f4d40ddac05d4e3d98bb81051c` (tree
`aed2ccf7596add9118b272afad831c214ede11fe`) and App stage
`e704a6a1c9093957f826b929bec2e7aeab18a44a` (tree
`6aad796a95e55086d6acebd75a3c5f066fcbad65`) are recorded as peer adoption
stages; this patch changes neither package pin nor package bytes.

Current blocker: both current Agent and stage255 `am-footage/component.tsx`
lack the reviewed `prepareFootageScene` / `prepareSceneCapability` binding.
Consequently the explicit public14-gated test returns UNKNOWN bounds/support
for the `am-footage` layer and fails closed. This is the real peer source
adoption prerequisite; no private assertion was weakened and no public13
substitution was made. The `onscreen.py` fade evaluator remains an intentional
host adapter while SDK check and visualize labels still call it.
