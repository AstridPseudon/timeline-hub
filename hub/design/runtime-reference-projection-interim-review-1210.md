# Runtime reference-projection interim review

## Verdict

**APPROVE — bounded independent diff review only.**

Reviewed Runtime commit `a6e88ac5faa09b80092d04177948987fbfd3cdac`
(tree `300a1e4e41b621cbe1eb4ad9ba51dc0d9829e67d`), directly descended from
raw-custody parent `d6c58babc6bf35bcdbc4a6f7bade177c97075268`.
No product or test changes were made by this review.

## Scope and diff result

The parent-to-commit diff contains exactly these three paths:

- `runtime_protocol/timeline_commit_reference_projection.py` (new helper)
- `runtime_protocol/timeline_commit_store.py` (acceptance hook)
- `tests/test_timeline_unplaced_reference_projection.py` (five direct tests)

The helper is semantically identical to the previously approved 449 source;
the only source difference from frozen 449 is `json`/`re` import ordering.
The store hook keeps ledger lookup first, performs projection preflight after
the existing closure/raw-capture validation and before `_persist_closure`, and
applies the existing read-model rows/snapshot in the same acceptance
transaction. A projection refusal therefore rolls back closure, publication,
head, and version changes.

Specific checks:

- `_desired()` accepts only the namespaced parent leaf at
  `config.app.astrid.timeline_references`, with exact v1/source shape,
  lowercase equal `media_id`/`content_digest` SHA-256 pins, and exactly one
  equal entry in the accepted `dependency_manifest.media`.
- Occupancy is global by reference identity. A pre-existing identity is
  accepted only when the previous accepted carrier and exact prior live row
  prove the same timeline/project, object identity, and role; otherwise it
  refuses before persistence and does not disclose foreign scope.
- The projected snapshot starts from every live row in the target timeline,
  removes only IDs in the prior carrier, and preserves unrelated rows.
- Removal checks the prior object and role, deletes the state row only through
  an exact scoped live-reference predicate, then deletes the exact owned
  reference row. No placement, catalog/latest lookup, alternate writer,
  endpoint, DTO, table, or public schema was added.
- `accept()` calls `_lookup()` before validation/provider work, preserving
  ledger-first exact retry behavior. Raw custody remains delegated to the
  existing capture/closure validation.

The published014 manifest was independently enumerated and compared by
content between the parent and this commit: **76 paths checked, 0 SHA-256
mismatches**. No artifact, schema, generated client, release, or public
contract path is in the diff.

The focused test fixture contains an unused `malformed` option, so its direct
suite does not invoke a non-source-role case. Source review plus the minimal
in-memory negative below confirms that `role: catalog` refuses as
`reference_projection_invalid`; this is a coverage note, not a product defect.
No RT08/item-map finding is made here; that line is outside this delta.

## Evidence

Reused the prior Agent449 semantic/source approval at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-runtime449-reference-projection-review.md`.
Reused the author’s report and command evidence at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-reference-projection-interim-current-port-1204/report.md`:
the bounded command reported **39 passed, 5 deselected**, the focused
projection suite reported **5 passed**, Ruff passed on new files, and
`git diff --check` passed.

Independent targeted run on this exact tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" \
/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
--timeout=60 tests/test_timeline_raw_capture.py \
tests/test_timeline_unplaced_reference_projection.py \
tests/test_timeline_projection_occupancy.py \
tests/test_timeline_commit_closure_invariants.py \
tests/test_timeline_history_boundaries.py -k 'not http'
```

Result: **39 passed, 5 deselected in 7.80s**.

Independent minimal role negative:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-runtime/bin/python - <<'PY'
# in-memory _desired() probe with role="catalog"
PY
```

Result: **non-source role refused: `reference_projection_invalid`**.

`git diff --check` passed. No full, socket/HTTP, browser, renderer,
installed, real-journey, generation, pin, publication, or live-activation
proof was run or claimed. Normal Agent-provider/native qualification remains
separate and open.
