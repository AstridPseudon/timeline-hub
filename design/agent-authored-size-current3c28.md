# Agent Timeline authored-size census — current3c28

Measured 2026-10-21 UTC from committed Git blobs only. The current source is
`3c28d3e01de55c8006a217887af4d89433fb42d0` (`current3c28`). At measurement
start, `origin/main` resolved to
`497714c73531f164082555ec81b61ca5bc8b6554`; that is also the named frozen
`Main497` baseline already used by the existing Agent size design. Thus the
two baseline columns below are intentionally identical, not independent
measurements.

## Method and boundary

The count is tracked Python source under `astrid/sdk/timeline/`, Python files
matching `astrid/sdk/timeline_*.py`, `astrid/core/timeline/`,
`astrid/core/extensions/`, and `astrid/packs/timeline/` except
`cli_visualize.py`. Files under tests, generated/vendor/receipt/doc paths are
excluded. Non-Python schema/data files and generated artifacts are also
excluded (`*.json`, `*.yaml`, and `*.generated.*` in the selected paths).
Physical means `splitlines()` including blank and comment lines; nonblank is
reported as context. This is a reproducible source-footprint count, not a
semantic claim that every line is newly authored Timeline behavior.

## Counts

| disjoint Agent-owned area | Main497 / origin/main files | Main497 / origin/main physical | Main497 / origin/main nonblank | current3c28 files | current3c28 physical | current3c28 nonblank | delta physical | delta nonblank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `astrid/sdk/timeline/` | 18 | 7,415 | 6,484 | 56 | 16,488 | 14,620 | +9,073 | +8,136 |
| `astrid/sdk/timeline*` flat files | 15 | 7,555 | 6,773 | 16 | 8,315 | 7,487 | +760 | +714 |
| `astrid/core/timeline/` | 57 | 15,480 | 13,452 | 57 | 14,725 | 12,809 | -755 | -643 |
| `astrid/core/extensions/` | 6 | 1,637 | 1,432 | 0 | 0 | 0 | -1,637 | -1,432 |
| `astrid/packs/timeline/` minus `cli_visualize.py` | 14 | 5,775 | 5,127 | 15 | 6,260 | 5,540 | +485 | +413 |
| **Total** | **110** | **37,862** | **33,268** | **144** | **45,788** | **40,456** | **+7,926** | **+7,188** |

The `core/extensions` reduction is the already-ledgered D06 deletion, not a
new proposed cut. The size target in PLAN is a rough guide, not a limit or
gate; this report does not recommend changing product code to approach it.

## Shared helpers outside the strict total

Known Timeline-facing shared code is reported separately and is not added to
the table above:

- `astrid/core/execution/generic_host.py`: 14,005 physical / 13,245
  nonblank on Main497 versus 13,973 / 13,218 currently; the exact diff is
  35 added and 67 deleted lines. Its ledgered D13
  `_publish_assembled_timeline` span is still 91 physical / 89 nonblank
  lines (`:8457-8547`).
- `astrid/core/rendering/scene_answers.py`: current-only 204 physical / 176
  nonblank lines. Existing design treats this as the Timeline See handoff,
  while the path is operationally shared/rendering-owned, so it is disclosed
  rather than silently charged to the strict Agent path.

Other current-only rendering/source-authority helpers are not attributed here;
this is deliberately not an exhaustive repository census.

## Existing deletion-ledger debt

No new ledger row is proposed. Rows already marked DELETED were not counted as
remaining debt (D05, D06, D07, WC2, WC4, WC6, WC9, AG-RECOVER, and
AG-M2-DEAD-LEAF-01). For rows still open, held, or in progress, the following
live spans were measured at current3c28. They are raw inventories of code
still present, not promises that every line disappears; rows overlap at the
same caller/helper and replacements will add code.

| existing rows | live current span(s) | physical / nonblank |
|---|---|---:|
| AG01 / WC7 | `sdk/timeline/publish.py:30-90,116-131` | 77 / 73 |
| AG-M2-TB01 | `sdk/timeline/publish.py:201-224` (`pin_narration`) | 24 / 24 |
| AG02 / AG03 / WC7 / WC8 | `sdk/timeline/store.py:187-374,629-678` | 238 / 220 |
| AG03 / WC8 | `sdk/timeline/checkout.py:234-288` and `sdk/timeline_checkout.py:133-154` | 77 / 71 |
| AG02 / WC7 | `packs/timeline/cli.py:2760-2829,2944-3006` | 133 / 125 |
| WC1 | `core/timeline/authoring_bundle.py:1571-1606` | 36 / 33 |
| **strict-scope raw span inventory** | **overlapping rows; do not sum as a deletion claim** | **585 / 546** |

Additional ledgered Agent-owned spans outside the strict boundary are D13's
91 lines above, WC3 `sdk/remote.py:1212-1455` (244 / 231), WC5
`sdk/authoring_remote.py:230-326` (97 / 94), and the direct text-binding
writers in `sdk/remote.py:2347-2359` (13 / 12): 445 physical / 426
nonblank raw span inventory. D01a/D01b are shared App-side rows; AG-M3-CAP-01
through -04 are test-only; AG05 is shared rendering code; and WC10 is a
Runtime-owned route. None is converted into an Agent product deletion count
here. The ledger therefore does not support one additive “lines remaining”
number: the measured 585-line strict-scope inventory is the honest upper-bound
surface of the currently live named spans, with overlap and retained behavior
explicitly preserved.

## Limitations

The count does not execute imports, infer dynamic ownership, distinguish
comments from authored logic beyond the nonblank companion number, or estimate
replacement-code size. It also does not count mixed-file transport slices,
renderer-owned files other than the disclosed shared helper, tests, fixtures,
generated clients/contracts, vendored Composition, receipts, or docs. No
pytest, full suite, browser/live-socket run, install, or product/test rewrite
was performed for this measurement.
