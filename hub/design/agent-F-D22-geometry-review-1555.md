# F-D22 geometry review — independent handoff

PASS — precise boundary adaptation; no test weakening.

Candidate commit 8a32f505e is limited to the exact three outer geometry
expectations in tests/packs/rendering/test_am_snap_plate_scene_capability.py.
It preserves all private positive checks (crop/scale-in private
full_frame=False, opacity=1; fade-up private full_frame=True, opacity=0),
exact fixture data, four strict unproven-backing negatives, SSR and
painted-backing positives, opaque-support and guard predicates.

The public assertions are source-backed by Composition 0.0.14's installed
artifact 819acf6b... and require precise bounds, opacity, visibility,
fullFrame, opaque support, partial coverage, frame GAP, null content, and
empty findings for cropLeft 0.2, scale-in 0.5, and fade-up 0.5. The source
packet's corrected caller citation is verified at
TimelineComposition.tsx:232-262, 258-260, 278-280. No broad UNKNOWN
allowance, GAP-only check, deletion, or weakening is present.

Locked bounded run: 4 passed in 9.30s (the three adapted cases plus one
strict negative) under Node 20.19.4, Runtime3b, Composition 0.0.14 and
artifact SHA 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234.
Mutation probes for wrong bounds, wrong opacity, and an unexpected
unknown-animation-geometry finding each exited 1. Scoped mypy passed; Ruff
matched the base's one I001 finding with zero added; diff check passed.

Author's exact seven-test evidence (7 passed in 14.56s) is reused rather than
repeated. The original full 10679 service remains FAIL/exit 1 and no whole-40
or full PASS is claimed. No pixel parity or browser/socket/media evidence is
claimed. Review made no product or dependency changes.

