# R2 graph boundary independent source assessment

Verdict: `PASS_SOURCE_ASSESSMENT`.

The source claim is supported in its narrow syntactic scope: the `ab1e`
correction adds an inverse-only exception for an empty-path
`occurrence:<id>/collection:track` read. It does not match the graph's
`occurrence:new-occ/collection:clip` selection or
`occurrence:new-occ/clip:title` leaf reads. This is a proven applicability
limit, not a causal proof that Runtime or Agent emitted the wrong record.

## Exact source trace

- The reviewed branch `cd236` has no production-source delta from its parent
  `ab1e`; `runtime_protocol/timeline_commit_auth.py` is blob
  `75c290ed...`, and the store is unchanged from `5e9ad`.
- On `5e9ad`, `validate_step` proceeds from each native read to
  `native_site` (`:382-419`, especially `:403`). On `ab1e`, the inserted
  branch at `:400-421` requires all of: inverse stage context, operation
  `timeline.inverse`, a slash-bearing ref, exact
  `owner + "/collection:track"`, empty path, occurrence owner in `created`,
  authenticated owner absence at the command boundary, and one matching root
  restoration.
- `native_site` delegates ordinary occurrence child aliases to `site`
  (`:213-218`). `site` resolves collection families through the owner/source
  path (`:119-131`) and leaf aliases through the occurrence row and its
  authenticated shot/internal images (`:150-172`); it requires exactly one
  matching occurrence at `:156`.
- `validate()` computes inverse stage boundaries and passes them to
  `validate_step` (`:2938-2950`). `validate_bindings` uses those boundaries for
  effect bindings (`:506-522`) and the bound step input for materialization
  edge checks (`:588-605`). Neither change alters the native-read branch's
  `collection:track`-only predicate.
- Agent `160c`'s `child_ops` selects `collection.clips`, reads and binds
  `occurrence:new-occ/clip:title`, and repeats child writes/reads
  (`tests/editing_conformance/test_recorded_graph_roots.py:112-123`). The
  child comparator enables that fixture, while the root comparator does not
  (`tests/sdk/test_timeline_commit_graph_roots.py:297-338`). The two Agent
  graph files are byte-identical at `224de`.

## Evidence boundary

The retained graph execution is `8 PASS / 1 FAIL` on `5e9ad`; the sole failing
selector is
`test_authenticated_created_child_stages_reload_inverse_redo_exact_closure`,
with `invalid_records: provider occurrence alias is outside its boundary` at
Runtime auth line `156`. The root-only comparator passes, but it has no child
selection, child alias read/bind, or child writes and therefore cannot qualify
the child seam. The retained original `[True]` run fails on `ab1e` during
redo-birth with the same alias message. It does not expose the exact graph
read, command ordinal, stage partition, or physical binding, so the shared
line/message is not treated as proof of a shared cause.

The exact causal owner remains `UNKNOWN`. Accepted `records.commands` and
`records.steps`, the failing read ref/path/state, ordinal and undo/redo phase,
per-ordinal closure images, inverse stage ranges, effect/materialization
bindings, continuations, and paired accepted history receipts are
`EXACTMISSING`. Current accepted/stage/physical records are therefore not
asserted.

D130 SWAP/WAL remains held and untouched. No guard, retry, body, collector,
test, qualifier, or protocol change was authored.

## Checks run

All checks were read-only and passed:

```text
AST parse/compile of runtime_protocol/timeline_commit_auth.py: PASS
AST parse/compile of Agent 160c graph fixture and graph test sources: PASS (2)
Python source predicates: PASS (track-only exception; no clip or clip:title exception; inverse boundaries passed to validate_step; effect/materialization boundary hooks present)
Python graph source predicates: PASS (collection.clips selection; clip:title read; child bind; repeated child writes/reads; root comparator excludes child_ops)
Python JSON parse of evidence/applicability.json and evidence/source-manifest.json: PASS (2)
git diff --check 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 ab1e4f6141987706132916e2da16477f5a019464 -- runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py: PASS
git diff --quiet 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 ab1e4f6141987706132916e2da16477f5a019464 -- runtime_protocol/timeline_commit_store.py: PASS (store unchanged)
git diff --quiet 160c675a2d58ab9ec2dde7517860075ad85e41d2 224de4697c -- Agent graph/fixture test files: PASS (unchanged)
Review branch production source equals ab1e: PASS
```

No product/provider tests were run or requested. The retained `8 PASS / 1
FAIL` and original `[True]` failure are prior evidence, not new execution.
