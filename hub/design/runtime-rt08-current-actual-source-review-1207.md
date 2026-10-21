# Runtime RT08 actual-source review — 2026-10-21

## Verdict

**APPROVE** for the dormant, source-only internal join in the exact range
`b92d3e7a05eec65c142294ef4873edd059e9b31d..52e6c01c1bb630f28fe3d694dbc8298bd1478c80`.
No real counterexample was found. This is an independent review of the
actual current source, not a review of the withdrawn 1157 finding.

The range is exactly:

- `07dc1d05f011556540881595f7b00b901c191321` — dormant RT08 source port;
- `504c9241ceed77daff9a44bb11c4e73a99ccea3e` — item-pair iteration and direct
  item-bearing helper control;
- `52e6c01c1bb630f28fe3d694dbc8298bd1478c80` — retains the useful test and
  removes the unnecessary cosmetic source rewrite.

## Source review

- `runtime_protocol/timeline_materialization.py` is byte-identical to the
  reviewed `42a7203f49bb89f299ec854cfbf2b1444e815a7c` provenance source. The
  join authenticates project/timeline scope, parent and source digests,
  source-owner occurrence edges, source item membership, destination/item
  binding pairs, distinct owners and global raw-item allocation collisions.
  The returned mapping is derived from the authenticated source item map;
  caller-provided `id_map` is checked against it and is not an authority.
- `RequestCommitPort` requires a private captured parent closure for a
  source-bound materialization and checks sealed request bindings. The
  closed-port guard is preserved.
- `TimelineCommitStore` preserves the current catalog-head fence, same-owner
  slot proof, destination occupancy checks, cross-project/global shot and item
  collision checks, and inherited inverse provenance checks. Durable ledger
  lookup precedes provider execution, and accepted replay verification also
  revalidates source-bound materializations.
- The current public v1 floor is preserved. No schema, DTO, version, client,
  generated artifact, pin, activation, keeper, or private017 operation was
  changed or activated.

The 1157 item-map assertion is withdrawn: the claimed `for i,j in
items.values()` defect is absent from both the actual `07dc` source and the
reviewed `42a` provenance. The 1205 correction is consistent with this source
review.

The new item test is genuinely additive helper coverage: it was added in
`504c924`, has no pre-existing failing expectation, and is not a RED-to-GREEN
repair. The author-provided retained evidence is acknowledged without broad
replay: 14 occupancy, 10 legacy, 230 neighboring tests; the new item control
and selected 12 neighbors remain retained evidence.

## Verification

All commands ran against the assigned worktree at commit
`52e6c01c1bb630f28fe3d694dbc8298bd1478c80`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt08-current-source-review-1207 tests/test_timeline_projection_occupancy.py::test_item_bearing_materialization_uses_validated_destination_pairs
1 passed in 0.76s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
contract/artifacts.json is current

76 published artifact paths checked against b92d3e7..52e6c01; changed=0

git diff --check b92d3e7..52e6c01
passed
```

The range changed only the three internal Runtime source files above and
`tests/test_timeline_projection_occupancy.py`. No full, socket, browser,
native, render, install, or broad-neighbor replay was run, as directed.

## Disposition

This is sufficient for the owner-11:48 lighter interim merge rule: one
independent actual-source review plus the changed-behavior targeted pass.
It does not claim public adoption, private017 activation, or a full RT08
consumer qualification; those remain separate follow-up work.
