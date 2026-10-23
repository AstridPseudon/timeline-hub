# F-D22 geometry fixture

Status: **PASS**.

The sole product diff is the scoped test adaptation in
`tests/packs/rendering/test_am_snap_plate_scene_capability.py`. It preserves
the three private positives and exact fixture, while the public Composition
0.0.14 caller result is asserted with known crop/entrance bounds, opacity,
visibility, `GAP`/null frame coverage, and no findings. The four unproven
backing negatives remain unchanged.

Evidence: exact three-case collection passed; the pinned Node 20.19.4 /
Composition artifact SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` targeted
run passed `7 passed in 14.56s`; private mypy, compile, and diff checks passed.
Ruff has one identical pre-existing import-order finding before and after
(zero added). Base is `d682c5977e0d5a7627ca04852980a2d65ca899d4`; edited test
file SHA-256 is
`d9c9b23722f3b49d8f8c4eba5e9789f60be26da70bd8f4f47fe5053a7243db98`.

No product source, JS, artifact, pin, fixture-data, schema, or contract change;
no full suite or browser/socket/pixel-parity claim. Worker report:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D22-geometry-fixture-1550/report.md`.
