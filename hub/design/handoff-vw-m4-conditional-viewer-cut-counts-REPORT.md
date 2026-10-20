# vw-m4 conditional viewer cut counts

Updated `design/viewing-size-cut-plan.md` with a source/function-level D09/D08 map and conditional after table. The frozen census and growth columns remain unchanged. The only qualified cut is Q1 (6 NB), leaving 48,337 NB in the confirmed Viewing slice.

Key measured envelope:

- D09 `onscreen.py`: 375 NB whole file, with a 69-NB role/coverage seam that must remain or move; conditional credit is 306–375 NB only after public-query, caller, source-identity, and parity gates.
- D09a/b: mouth-state direct body 24 NB plus a separate 9-NB helper, and mouth-box 7 NB; shared `presenter_words`/`presenter_view` are retained. Combined conditional extra is 31–40 NB, not a current credit.
- D09 residual motion/geometry is a deduplicated 261-NB union; lint checks are 188 NB; presentation and pixel callers remain classified rather than credited.
- D08 `audioFade.ts` is 60 NB (27 NB executable bodies), but it is outside the confirmed Viewing row. `VisualClip.tsx` (648 NB) and `TimelineRenderer.tsx` (1,656 NB) remain host adapters.

Read-only evidence commands and results:

- `git diff --check -- design/viewing-size-cut-plan.md` — passed.
- AST/`rg`/ad-hoc read-only source counts across the live Agent, App, Composition, frozen census, and prior reports — completed; exact measurements are recorded in the plan and companion JSON.
- Tests/build/install/browser/network — not run, as required by the docs-only brief.

No blocker. The measured conditional envelope is 47,922–48,000 NB after Q1 plus D09a/b, still far above 26k. Next owner decisions are to qualify the public D09 source/caller join and motion/ROI parity, decide whether any App audio-envelope replacement is in scope, or revise the global target; retained viewer, pixel, diagnostics, generic-host, vendor/archive, and fallback behavior cannot be re-counted as deletions.
