# F-D108/D54a terminal classification — cohort B

Read-only source classification for the exact cohort assigned by the D108b
terminal outcome. No product, test, generated, pin, ledger, registry, or
foreign output was changed.

## Exact membership

- Terminal XML: 9,269 unique testcase nodes; 8,763 passed, 159 failed, 347 errors.
- Non-passed nodes: 506. Independent prescribed partition: A=184, B=226, C=96.
- This return contains exactly cohort B: 226 unique selectors, 63 failed and 163 error nodes.
- Every B node is an `tests/editing_conformance/` path outside the A regex.

## Upstream comparison and disposition

All 226 B selectors are absent from the qualified upstream index/XML. The
bounded same-function rename check found zero upstream function-name matches;
therefore no upstream selector, status, blob hash, or exact/renamed behavior
comparison exists for these rows. Per D63/D54a, current-only nodes become
NEW-OURS after that check, not UNKNOWN regression candidates. Every row is in
the D54 core editing caller scope (commit door/provider/rebase/inverse/native
sheet) and is therefore core-blocking/open.

| category | rows |
|---|---:|
| PRE-EXISTING | 0 |
| KNOWN GAP | 0 |
| ENV | 0 |
| NEW-OURS CORE | 226 |
| NON-CORE | 0 |
| REGRESSION | 0 |

This is not an independent NO-GO verdict. It records current terminal facts
and the settled current-only disposition; it does not prove source causality.

## Existing owner groups

- Agent command-validation owner (existing R1/V2 route): 17
- Agent document/emitter owner (existing G3 route): 1
- Agent editing-conformance caller/fixture owner (named test family): 86
- Agent provider/commit owner (existing R1/R2 route): 23
- Agent sync/rebase owner (existing commit route): 1
- Runtime commit-provider/admission owner (existing service route): 98

## Limits and custody

Current exception class and safe source location are extracted from the current
XML/controller metadata; no traceback or request body is copied here. The
authentic upstream XML is SHA-256 `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`; current XML is
`72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`. The qualified upstream index is SHA-256 `d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a` and
current joins are SHA-256 `0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`. Baseline custody review is PASS, while
upstream Runtime isolation remains explicitly UNCERTAIN. D13/D23 identities
are not present in cohort B. No test rerun, environment substitution, body
repeat, assertion relaxation, or source-fault claim was made.

Machine-readable complete per-node rows are in the adjacent JSON and TSV.
