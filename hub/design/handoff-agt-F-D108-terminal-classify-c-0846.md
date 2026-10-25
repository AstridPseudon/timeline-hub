# F-D108/D54a terminal failure classification — cohort C

Read-only source classification for the exact cohort C partition. The full
current terminal is 9,269 unique XML testcase nodes: 8,763 PASS, 159 FAIL,
347 ERROR, with 173 reported passing subtests. The bad-node partition is 506:
410 editing-conformance nodes owned by cohorts A/B and 96 cohort-C nodes here.
No other cohort is classified.

## Result

The 96 rows are complete and unique. Current outcomes are 72 FAILED and 24
ERROR. Category arithmetic is: PRE-EXISTING=0, KNOWN GAP=1, ENV=16, NEW-OURS CORE=71, NON-CORE=8, REGRESSION=0 (sum 96). Core scope is 72 rows,
non-core scope is 24 rows. The true core-open contribution is 71 rows; the
remaining core row is the explicitly deferred D23 known gap and is not
core-blocking. There are zero proven regressions and no independent NO-GO
verdict.

The one current node absent from the 9,268-row baseline current-joins table is
retained explicitly: `tests/sdk/test_inverse_removed_shot_owners_runtime.py::test_occurrence_add_or_swap_then_undo_restores_the_authenticated_baseline`.
Its pinned current source was checked against the upstream source/index with
the same one bounded same-function/body check and had no upstream counterpart.

## Evidence and limits

- Current XML: `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`; body log: `0f34700508bfe35c94d2811d502b442cc36d4db4c4643303d8ca5dfd8f5af001`.
- Current outcomes JSON: `c180c1c153264d09e2ae79e0ad63007d9551e43e7b72e87973f0927140a6e2eb`.
- Upstream XML: `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`; upstream commit `92443771676ef2bbb547d0a103d708fa8bec4c63`.
- Baseline upstream index: `d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a`; current joins: `0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`.
- Existing D54 rollup: `ac14855e5d8337194960d424726352c6343ca3b2f705654e9f4fc498e574a43a`. Runtime isolation remains explicitly UNCERTAIN.
- Exact upstream FAIL/current FAIL is marked PRE-EXISTING only when exception
  class and safe failure location match. The 15 bootstrap rows retain the
  existing D54 environment assignment despite their changed setup causes.
- Missing upstream selectors receive one bounded same-function/body check;
  remaining rows are NEW-OURS CORE or NON-CORE under D63. No current-only row
  is treated as a regression.
- D13 and D23 use only their named existing evidence. No blanket ENV claim is
  made for the 347 errors, and no D107 original is retired by inference.

The per-node TSV and machine-readable JSON contain exact selectors, outcomes,
source hashes, safe exception/location fields, upstream selector/status/hash or
rename method, D54 scope, category, core-blocking status, limits, owner group,
and evidence references without raw traceback/request bodies.
