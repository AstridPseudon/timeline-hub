# Agent PRIVATE017 placement-oracle review

Date: 2026-10-21 UTC

## Disposition

The 1029 correction is source/oracle-correct for the captured identity
fixture, but the one authorized native retry is **not qualified**. It reached
Runtime admission and then failed at the first reload source-map assertion.
No product, schema, lock, pin, provider, or fixture changes were made in this
review worktree.

## Exact identities

- Agent source: commit `95e1ada1953d40710039d8e70525387cc64d065b`, tree
  `50cb3fcaf0a2ece1c0d320f5cca7948b32eac92f`.
- 1029/base: `tl/agt-m2-private017-placement-first-fixture-cause-1029`;
  this review branch is clean and identical to that source.
- Approved Runtime 42a: commit
  `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e` at
  `/home/user/work/wt/rt-pin-42a7203f`.
- EditCommand schema raw SHA-256, Agent and Runtime byte-identical:
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`;
  65 `$defs`, 37 `EditCommand.allOf` clauses.
- Runtime artifact manifest: 76 artifacts, producer version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
  All 15 locked Agent artifact hashes matched `runtime.lock.json`, whose
  source commit is exactly 42a.

## Oracle/source review

The corrected new assertion is grounded: reproducing the identity fixture
setup without executing the native body yielded `source shot payload items=[]`
and `source_mapping.shots[destination].item_id_map == {}`. The generated v2
command therefore has the genuine shot-only allocation map
`{'shot:<destination>': '<destination>'}`. There is no unsupported global-item
qualification; item allocation remains explicitly outside this proof.

The two original occupancy/atomic-refusal and shared-occurrence retry/restore
tests remain present and unchanged. The new test still retains own-slot,
reload, inverse, and exact-retry assertions. The only source delta from 6c is
the placement-proof test file; no assertion was removed beyond correcting the
ungrounded item-map premise.

## Schema/import investigation

The 1029 note that “Runtime rejects v2” is not supported by the exact 42a
resources. Normal imports resolved Agent from this worktree and
`runtime_protocol` from `/home/user/work/wt/rt-pin-42a7203f`; the normal
`astrid` provider loaded with ABI `astrid-v1`/interface 1. A v2 command
generated from the identity source bundle passed
`runtime_protocol.timeline_commit_validation.validate_commit_value(command,
"EditCommand")` against the loaded 42a schema. The earlier local public014
import is not evidence against 42a and was not used.

## Checks

Passed:

- Exact 42a lock, 15-file artifact, byte-identical schema, loaded import,
  provider, and v2 schema-validation preflight.
- Identity fixture setup-only reproduction: empty item map confirmed.
- `pytest --collect-only ...test_fresh_shared_placement... [fresh]`: 1
  collected.
- `pytest --setup-plan ...test_fresh_shared_placement... [fresh]`: setup
  closure resolved; no test body ran.
- `pytest -q -o addopts= -p no:cacheprovider
  tests/editing_conformance/test_materialization_version_boundary.py
  tests/editing_conformance/test_materialization_map.py`: **66 passed**.
- `ruff check tests/editing_conformance/test_commit_runtime_identity.py`.
- `git diff --check 6c1989adf...HEAD`.

The first central result was preserved:

- `...private017-placement-one42a-integration-1021102411-25065`: **1 failed**
  before admission at the unguarded `next(iter(item_id_map.values()))`
  (`StopIteration`).

The one permitted diagnosed retry was:

- `...private017-placement-one42a-integration-1021103708-3710`, exact source
  tree `50cb3fcaf0a2ece1c0d320f5cca7948b32eac92f`: **1 failed** in 1.92s.
- It reached `accepted`, readback, restart, and the first reload placement
  assertion. Failure at line 316:
  expected `source_pin['shot_id'] == 'shot-1'`, observed reloaded source-map
  `shot_id == 'shot-placement-271ff5ac6e7f5c9457f24655a71debca8383cec79839f3a52381233be3abb738'`.

## Limits and next step

No local native body, old12/66/76 lane, ordered/RT03 duplicate, full suite,
schema override, or further retry was run. The placement lifecycle proof is
held at the reload provenance mismatch. The manager should decide, with a
fresh narrow review, whether the reload assertion’s expected source identity
or the Runtime materialized source-map identity is the intended contract;
neither should be weakened based on this result alone.
