# EXACTAPPROVE — Agent PRIVATE017 placement-oracle repair review

Date: 2026-10-21 UTC

## Disposition

**EXACT APPROVE for the assertion conversion. No repair is required.** The
corrected reload oracle is physically grounded and does not weaken or replace
the accepted source/owner/id-map, undo, or exact-retry assertions. This is a
source and test review only: the placement lifecycle is still unqualified
until one later manager-authorized diagnosed body run passes.

The reviewed Agent source is `86d1e6da200884ba660ea435c90dac801f8f1c7e`,
tree `5b6dc1c4eed688bdfc2c7f53b21607b0f169683d`, over private6c
`6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
`cc0a8dd1360324a1b440ba7d318a083e7f8814cc`. The only source diff is the
100-line addition to
`tests/editing_conformance/test_commit_runtime_identity.py`; no product,
pin, schema, fixture, or Runtime source was changed.

## Oracle and assertion review

The identity fixture's captured source is `S = shot-1`, and the shared
occurrence's materialized physical destination is `D =
shot-placement-271ff5ac6e7f5c9457f24655a71debca8383cec79839f3a52381233be3abb738`.
The fixture has no source shot items, so its source pin has
`item_id_map == {}`. The proof correctly states that this is shot-only and
that global/item allocation remains a separate gap.

The accepted-history assertions remain the authoritative checks:

- the returned `id_map` is exactly `{'shot:D': 'D'}`;
- the accepted dependency `materialization.source:shot:D` retains source `S`
  and its empty item map;
- the fixed owner binding is `materialization.owner:shot:D` to
  `occurrence:occurrence-1`, dependent on that source dependency;
- the accepted canonical document physically places occurrence-1 at `D` and
  applies the clip edit at `0.5`.

After restart, `bundle_from_document` receives only the current canonical
document. It therefore derives a fresh authoring projection for physical `D`,
not a history record, so `source_mapping.shots[D].shot_id == D` is the correct
reload expectation. The new one-for-one comparison with the pure
`bundle_from_document(document_from_bundle(expected.bundle))` projection,
followed by explicit `D` and `{}` checks, is the right conversion. It does not
assert that reload reconstructs historical `S`; the accepted dependency check
above still does that.

The remainder of the added test retains the real lifecycle assertions: real
Runtime admission and readback, restart, an own-slot edit to `0.75`, receipt
inverse restoring the accepted canonical document exactly, and same-key retry
returning the original accepted result with the Agent provider forbidden.
The pre-existing private6c tests for unrelated occupancy/atomic refusal and
the normal shared-occurrence retry, own move, historical restore, and world
preservation remain unchanged. The new retry guard is therefore a placement
specific assertion layered beside the existing stronger generic retry guard;
it is not a replacement for that normal test.

## Historical failures and boundary

- Central result `...1021102411-25065` failed before admission at
  `next(iter(item_id_map.values()))`. That is a genuine fixture gap and is
  not erased by the correction.
- Authorized follow-up `...1021103708-3710` reached acceptance, readback, and
  restart, then failed only because reload expected `S` while the physical
  projection correctly contained `D`. It stopped before own-slot reuse,
  inverse, and exact-retry assertions, so those remain unqualified by history.

No third/native body execution, whole-node execution, full suite, HTTP/socket
run, pin, activation, or schema override was performed in this review.

## Evidence

Passed on the reviewed source with the approved Runtime 42a checkout at
`/home/user/work/wt/rt-pin-42a7203f`:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_materialization_version_boundary.py tests/editing_conformance/test_materialization_map.py` — **66 passed in 8.32s**.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_commit_runtime_identity.py` — **passed**.
- `git diff --check 6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79 HEAD` — **passed**.
- The exact integration node collection command with Runtime 42a — **1 test collected**; its body was not run.

Reused diagnosis evidence also records byte-identical Agent/Runtime
EditCommand schemas, the exact 42a lock/artifact cohort, and the normal
provider/import preflight. The historical 25065 and 3710 results remain
failures, not qualification evidence.

## Readiness for one later diagnosed run

**Ready for exactly one later manager-authorized run**, subject to all of these
prerequisites being checked together immediately before execution:

1. Use this exact Agent tree and Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c`
   checkout, with lock/artifact/schema hashes unchanged and the normal
   vendored Agent client selected.
2. Run only
   `tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_placement_materializes_own_slot_reload_inverse_and_exact_retry[fresh]`
   under `-m integration`, with the explicit Runtime checkout and isolated
   environment used by the prior central results.
3. Confirm collection is exactly one node, the shot-only empty item map is
   expected, and no shared dependency or cache is writable before spending the
   body run.
4. Do not retry automatically. A passing body run qualifies this one-node
   placement proof only for the stated shot-only fixture; it does not close
   the global/item allocation gap or qualify other placement shapes.

