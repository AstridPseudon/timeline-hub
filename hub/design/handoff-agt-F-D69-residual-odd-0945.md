# D108/D69 residual ODD original-membership review

Status: **COMPLETE SUBSET WITH REMAINING CONSTRAINTS**. This is a read-only
independent semantic predicate review. It is not a whole-audit PASS.

## Exact scope and arithmetic

Input membership is the recovered `original-membership.json`, SHA-1
`5f21b1b73393d85d100208793d90bcf06e48326a`, whose authoritative membership
payload is SHA-256 `1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0`.
The recovered master handoff is SHA-256
`af04bc82117976029346a9a6646b956ab16390627a9d764be6a30ef668ee0411`.

Sorted immutable original index ODD (partition 0) contains 65 functions,
including 31 zero-delta functions, with 46 removed and 109 added assertion
multiplicity. The six odd-partition functions covered by the 15-function
core/stage/writers maps were excluded exactly. The 34 already-approved rows
from the 0902 partition were also excluded exactly. The returned residual is:

- 25 functions;
- 66 fingerprint records;
- 24 removed multiplicity;
- 42 added multiplicity;
- verdict multiplicity: 16 FAIL, 50 UNRESOLVED.

Conservation: `46 = 13 mapped + 9 approved + 24 residual`; `109 = 42 mapped
+ 25 approved + 42 residual`. The EVEN complement is disjoint and was not
reviewed.

## Exact source identity

| source | commit | tree |
|---|---|---|
| old upstream | `08e6b905114a3ee2b05c3e7980421f26b4abf15c` | `2694ae8d2709526b40fa037bda8b159cf412769d` |
| captured new | `d6294843286c18e57af3c1874cf1996be42212d2` | `6aeae30f0892a424104a4348bca6fd74ba1315d6` |
| current normal | `d0ecf1d69a7b37f86034bc52004f73f6c6231603` | `e9845f8cf5a6ba80210336d0e2452f80a0918762` |

All selected current-normal function blobs resolve to their captured-new blobs.
Each returned row records old/new/current path, blob, line, body hash, exact
AST fingerprint, source text where present, purpose, approval state, current
applicability, and verdict in the JSON/TSV evidence.

## Verdict boundaries

The FAIL rows are purpose losses visible from the exact old/new predicates:
render-status inversion; removal of a generator non-vacuity guard; removal of
coverage blocking/invalidity predicates; removal of the cycle-stop assertion;
and replacement of the original document-publish feedback/head scenario by a
different timing scenario. No repair, retirement, or test change was made.

The UNRESOLVED rows are source-current or API-shape candidates without an
exact approved C0/G4/G5/D72 replacement/retirement receipt. Passing tests,
operator resemblance, and current-source identity were not treated as proof.
The D18, D07, D107, Windows, and other owner boundaries remain separate.
Where a replacement changes the public route, this handoff does not claim a
registered production caller; that requires the exact caller receipt and the
full `commitTimeline` request/reply contract review.

Render behavior remains blocked for any residual closure/render purpose not
preserved. No unrelated residual was silently cleared. The referenced
`f480`/`e9e` shorthand does not provide an additional exact receipt in the
available inputs, so it was not used as approval.

## Evidence and checks

Machine-readable row evidence is in `workers/agt-F-D69-residual-odd-0945/evidence/`:

- `residual-odd-source-checks.json`
- `residual-odd-source-checks.tsv`
- `residual-odd-checks.txt`

JSON/TSV parsing, AST parsing, old/new/current Git blob checks, current-normal
source matching, and arithmetic passed. `git diff --check` on the unchanged
Composition worktree passed. Tests, typecheck, and lint are N/A by the
read-only brief.

Historical XML is not a new qualification run: `handoff-agt-F-D69-23762-d69-restored47.xml`
SHA-256 `005ea787fce46efbba6e5637a6e92ab8e9fb5f83f62e3d48649f0522bf06e2a5`
records 49 tests with 39 failures; it is retained only as a non-green context
receipt, not as evidence for clearing any row.

