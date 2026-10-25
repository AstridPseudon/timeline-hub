# F-D108 baseline-return rereview (0813)

Decision: **FAIL_SECOND**.

This was an independent source-only rereview of the completed 0803 return after
the 0758 failure. The full validation record is
`workers/agt-F-D108-baseline-rereview-0813/evidence/review-validation.json`.

## Checks that pass

- Authentic XML is SHA-256
  `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f):
  12,517 testcase rows, 12,396 PASS, 91 FAIL, 14 ERROR, 16 SKIP, 566
  subtests by suite-total delta, and 13,083 total. Arithmetic and zero
  duplicate raw IDs pass. Terminal remains FAIL/exit 1.
- Current membership is complete: 9,268 selectors, 2,956 exact joins,
  6,312 absent exact selectors, zero ambiguous. Selector hashes, current
  source inventory hashes, exact outcome/source/blob joins, and candidate JSON
  cardinalities pass. Parameterized rows and class/function collisions are
  retained rather than collapsed. Absent distinctions remain 65 body-equal,
  17 name-only, and 6,230 no-match.
- Historical D54a evidence remains separate: 276 rows, 75 exact (66 FAIL /
  9 PASS), 201 UNKNOWN. D63 order 129 remains observation-only; order 181
  remains body-equal counterpart observation with current proof pending, and
  its missing references are present in the successor JSON.
- Runtime full-run isolation remains UNCERTAIN; upstream FAIL, D13 ENV, D23
  deferred identities, withheld current classification, and withheld current
  core count are preserved.

## Blocking findings

1. The successor JSON is not hash-consistent with its actual evidence files:
   it claims the evidence full index is `075f630611aad412b8e2fda861e807800d8756dbd31aed19acc0c7d43fe7b456`, but the actual evidence TSV is
   `d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a`.
   It claims the summary is `e92bcf07eff73e98b2e837a9305e0bd89915a5030a52fb3b0764ce41c2eb5eb5`, but the actual summary is
   `7af40efb74bc171142e5a89f7cc25b17c710001c7dba61bb8e04c971764dbfd7`.

2. The published full index is a different byte variant from the author
   evidence. It differs in 23 rows, ordinals 12309--12331, all
   `tools/astrid-rename` tests. Those rows have file/line blanked and
   `not_resolved_in_authentic924_tree`, although the corresponding files
   exist in the real 924 tree. The published TSV hash `075f…` is therefore
   not an acceptable canonical full index for the stated source-resolution
   claim.

The published and evidence current-join TSVs are byte-identical at
`0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`.

## Minimal HARD scope

Republish one canonical full index from the authentic XML and commit
`92443771676ef2bbb547d0a103d708fa8bec4c63` tree, retaining all 12,517 source
mappings. Recompute every dependent JSON/MD hash claim and verify path/hash
pairs against actual bytes. Do not run product tests or infer current
classification/core count.

## Commands and results

- `python3` stdlib XML/CSV/JSON/AST/hash/Git audit: PASS for XML arithmetic,
  duplicate accounting, current join membership, source custody, and
  historical/D63 checks; found the two blocking custody findings above.
- `sha256sum` on published/evidence TSVs and JSONs: FAIL on the two successor
  JSON evidence claims; current joins match; published full TSV is the 23-row
  stale variant.
- `git -C /home/user/peteromallet/astrid-agent ls-tree -r --name-only 92443771676ef2bbb547d0a103d708fa8bec4c63`: all published index file
  paths exist in the real tree.
- Product tests, pytest, imports, collection, services, browser, install, and
  full suites: not run, per task boundary.

