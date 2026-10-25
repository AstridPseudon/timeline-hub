# R2 graph child-boundary applicability validation

Verdict: the qualified `ab1e` grouped inverse/redo correction does not cover the
App graph child alias seam. The exact causal owner of the admitted graph failure
remains `UNKNOWN`; the only proved missing applicability is the Runtime auth
validation exception's child-alias scope.

## Source trace

- Runtime `validate()` computes per-command sequential inputs, then computes
  authenticated inverse stage boundaries, and calls `validate_step` with those
  boundaries (`runtime_protocol/timeline_commit_auth.py:2891-2950`).
- `validate_step` validates each native read against that command's
  `command_boundary` (`:393-426`). `native_site` delegates occurrence child
  aliases to `site` (`:213-218`); `site` requires exactly one matching occurrence
  row before following its shot/internal edges (`:150-162`).
- The `ab1e` exception is exact-source limited to
  `owner + "/collection:track"`, with empty path, `timeline.inverse`, a created
  owner, an absent parent occurrence at that command boundary, and one matching
  root restoration (`:400-421`). It does not cover `collection:clip` or
  `clip:title`.
- Runtime effect bindings use computed inverse stage boundaries, and
  materialization edge checks use the bound step input (`:515-522`, `:590-605`).
  Those corrections do not broaden native read alias applicability.
- The Agent graph fixture's child operation selects `collection.clips` for
  `occurrence:new-occ`, reads/binds/writes `occurrence:new-occ/clip:title`, and
  repeats child reads. The graph test imports that fixture; the root-only test
  does not enable `child_ops`.

## Evidence reconciliation

The safe App packet reports the exact graph source as PASS and the admitted
graph-nine result as 8 PASS / 1 FAIL. The sole failure is
`test_authenticated_created_child_stages_reload_inverse_redo_exact_closure`,
with `invalid_records: provider occurrence alias is outside its boundary` at
Runtime auth line 156. The root-only create/inverse/redo comparator passes, but
it lacks the graph child aliases and therefore cannot qualify them.

The separate original `[True]` run on Agent `d4ba9916` plus Runtime `ab1e4f61`
fails during `redo-birth` through `validate_step:426 -> native_site:218 ->
site:156`. Its exact records and physical closure packet are unavailable. The
shared line/message is not treated as proof of a shared cause.

## EXACTMISSING

The following are not present in the safe graph packet and prevent causal
ownership attribution:

- accepted `records.commands`/`records.steps`, failing read ref/path/state,
  command ordinal, and exact graph undo/redo phase;
- per-ordinal sequential input/output closures;
- inverse-stage native/effect ranges and before/after closure pins;
- `commit.effect` and `commit.materialization` bindings with physical refs,
  owners, edge refs, ordinals, and phases;
- source/landing closures, authenticated continuations, and paired accepted
  history receipts.

Therefore this report records a Runtime R2 applicability gap only. It does not
authorize a Runtime fix, Agent change, App guard, test change, retry, or new
record collector. D130 SWAP/WAL recovery remains held and was not inspected.

## Checks run

All checks were read-only and passed:

```text
python AST parse of runtime_protocol/timeline_commit_auth.py and the Agent graph/fixture sources: PASS
Python source predicate check: Runtime exception is collection:track-only; effect-boundary and bound-materialization hooks present: PASS
Python graph source check: root-only caller, child caller, collection selection, clip leaf read, and child binding present: PASS
Python JSON parse of the four safe App evidence JSON files: PASS (4)
git diff --check 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 ab1e4f6141987706132916e2da16477f5a019464 -- runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py: PASS
git diff --quiet 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 ab1e4f6141987706132916e2da16477f5a019464 -- runtime_protocol/timeline_commit_store.py: PASS (store unchanged)
git diff --quiet 160c675a2d58ab9ec2dde7517860075ad85e41d2 224de4697c -- Agent graph/fixture test files: PASS (unchanged)
```

No product test/body/retry was run in this read-only applicability task. The
8-pass/1-fail graph result and original `[True]` failure above are retained
results from the named safe evidence packets.
