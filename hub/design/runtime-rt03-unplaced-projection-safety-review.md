# RT03 accepted unplaced-reference projection safety review

## Verdict

**APPROVE** for the Runtime candidate `449d13d291cc3b62ebbdd780d38d8c58732e4e1b`,
tree `47d5f06df25618b45a95293c5217e6454f6ae69c`, based on
`f53bf588bf70b090ce8e0bed5ccb7d91157771b6`.

I found no concrete data-loss or cross-area custody counterexample in the
actual diff. This is an independent safety review only; no Runtime or Agent
source was changed here.

## Review findings

- The Agent handoff `d1f5f7824a5ede5587088735fad6e6870f0b95db` is the bounded
  parent-scoped carrier described by the fit design. Runtime reads only
  `parent_revision.payload.config.app.astrid.timeline_references`; it does not
  normalize the parent, create placement, consult the catalog, or introduce a
  second writer.
- `_desired()` requires the closed v1 leaf, literal `role: source`, lowercase
  equal `media_id`/`content_digest`, and exactly one matching entry in the
  accepted `dependency_manifest.media`. This runs after the existing closure,
  raw-media capture, managed-project ownership, and CAS byte checks.
- Occupancy is global across `timeline_references` and therefore includes
  rows on foreign timelines and archived timelines. A pre-existing ID is
  accepted only when the immediately previous accepted carrier contains the
  same ID and the target live row exactly matches that prior projection
  (`reference_id`, object identity, and role); equal media bytes alone do not
  authorize an overwrite.
- Removals are derived only from the previous carrier. They require an exact
  current row match and delete both the row and its state only under the same
  timeline/project/object/role predicate. The projected snapshot starts from
  all live target rows, so unrelated references survive.
- The legacy snapshot is written with sorted reference IDs and the current
  legacy shots, in the same SQLite transaction as closure persistence,
  receipt/event publication, head movement, and timeline-version increment.
  Any projection failure rolls back the externally visible acceptance. The
  ledger lookup remains first, so an exact retry after restart returns the
  original receipt without provider execution or a second projection.
- Ordering and history cannot drift through this helper: reference rows in
  the snapshot are sorted by ID, shots are copied from the existing live
  projection, and the catalog/history readers compare live rows with the
  latest `timeline_revisions` snapshot.

The focused discriminator inserted the same reference ID on a foreign active
timeline and on a foreign archived timeline. Both attempts refused with
`timeline reference identity is already occupied`, and `iterdump()` was
unchanged in each case.

## Evidence

Reused predecessor evidence on the candidate:

- projection tests: **4 passed**;
- closure/history/raw-capture neighbors: **21 passed, 4 deselected**;
- catalog/projection/restore neighbors: **17 passed, 12 deselected**.

The four HTTP history nodes that failed locally with
`PermissionError: [Errno 1] Operation not permitted` were submitted alone to
the central test service on this exact tree:

```text
tests/test_timeline_history_boundaries.py::test_http_history_keeps_fixed_head_and_distinct_same_revision_edges
tests/test_timeline_history_boundaries.py::test_http_history_scope_auth_and_limits_refuse_without_leaking_data
tests/test_timeline_history_boundaries.py::test_http_dry_run_needs_write_scope_and_reserves_nothing
tests/test_timeline_history_boundaries.py::test_http_revision_reads_keep_manifest_pinned_children_after_new_head
```

Central result: **4 passed in 5.03s**, run
`rt-m2-review-rt03-unplaced-projection-0244-targeted-1021024601-15107`.

Focused local discriminator:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" /home/user/work/venv-runtime/bin/python - <<'PY'
# foreign active and archived timeline-reference occupancy probe
PY
```

Result: both cases refused; no database changes.

`git diff --check` is clean. No full, render, browser, schema-generation,
pin, or normal-provider source-generation suite was run.

## Remaining dependency

The source tests intentionally use the approved ephemeral trusted acceptance
setup and prove Runtime projection behavior, not the real Agent provider
generation path. The original strict normal-pair positive remains open: a
current Agent `timeline.reference` provider must emit the d1f5 carrier through
the normal `/v1` acceptance path and prove its raw capture, unplaced result,
restart-safe exact retry, inverse removal/restoration, and occupied-ID refusal.
This review preserves that dependency and does not convert source-only
evidence into native qualification.
