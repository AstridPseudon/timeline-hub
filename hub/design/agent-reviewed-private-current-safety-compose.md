# Agent private current-safety source composition

Date: 2026-10-21 UTC  
Worker: `agt-m2-reviewed-private-current-safety-compose`

## Result

Prepared one new private, source-only current-preserving successor in the
assigned worktree. The resolved base is:

- base commit: `2b0e6dc2feaaf0879d4817946bfaae5b143f1411`
- base tree: `a158cb5822c41ee2a8951a8446cd07e1af5c6846`
- provisional final worktree tree (computed without mutating `.git`):
  `8623434a542452c286ab3398b51a676279c2b4f8`
- base merge resolution: `a905fa29b1bb47739df438f4203ed987be588e46`
- frozen published014/Main497 integration merge parent:
  `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`

The harness merge-parent file requests `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`
as the second parent. The final harness commit/tree are not available until
the harness commits the uncommitted worktree.

## Composed source

Added the approved transcript source/test files byte-for-byte from
`85e3bef7103680fdf96a8f123717bccbd95df7f3`:

- `astrid/sdk/timeline/native_transcript_association.py`
- `tests/editing_conformance/test_recipe_film_transcript_association.py`

Applied the approved staged-inverse changes from
`f6485dc4e7fe0da5cace94df9fc69b72fa3706b1`:

- `astrid/sdk/timeline/_recording.py`
- `astrid/sdk/timeline/inverse.py`
- `tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py`

The final worktree changes are exactly those five paths. The rawOLD
schema/lock/generated paths and the current integration resolution were not
reset or regenerated.

## Identity and preservation

- Raw schema SHA-256:
  `9e4b4421ebbba94f13f8f286c7ea1df5eb9ca128142ed904c92a993985954cfd`
  (`64` definitions, `36` EditCommand clauses).
- Private C3d `runtime.lock.json` SHA-256:
  `07c7be425e8b5595006db280541c97d6e3dd174ae92f54b8550340e21167ec32`.
- Private generated client SHA-256:
  - `astrid_runtime_client/__init__.py`:
    `4069c15e93b72d504cc882b18dbae119fcd9e7a5186f3c06238bad304276a206`
  - `astrid_runtime_client/contract_metadata.py`:
    `40d329430bf40c36876b12adc08c6c59f2a4b7e980da8b963305b6b375a43aea`
  - `astrid_runtime_client/generated.py`:
    `61b55a2e14127a9cc360054a67f6c0b6259ff7eb75bcf58e9c788da344c234ca`
  - `astrid_runtime_client/timeline_commit_types.py`:
    `f33a509da59352fed877d2c0ccc5e2e150d17494a0a28e4de811d2c268382644`

The resolved merge audit found no lost donor assertions: `27/27`
non-overlapping current-integration blobs and `93/93` non-overlapping
approved-source blobs matched their respective donors exactly. The three
added donor test/source files also matched their donor blobs exactly.

## Tests and checks

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_inverse_clear_batches.py \
  tests/editing_conformance/test_recipe_scalar_commands.py -k 'inverse_' \
  tests/editing_conformance/test_grouped_clip_cache_inverse.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/editing_conformance/test_raw_old_swap_successor.py
# 106 passed, 146 deselected in 7.48s
```

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache \
  astrid/sdk/timeline/native_transcript_association.py \
  astrid/sdk/timeline/_recording.py astrid/sdk/timeline/inverse.py \
  tests/editing_conformance/test_recipe_film_transcript_association.py \
  tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py
# All checks passed

git diff --check
# passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/artifact_manifest.py --check
# artifacts.json is current
```

## Boundary and unverified evidence

The new transcript test was run once and produced `11 failed` at the expected
unsupported-operation boundary: rawOLD intentionally has no admitted
`transcript.associate` registry/schema operation, and no live caller was
added. I did not add registry/schema admission because that would violate the
exact rawOLD `9e4b` schema and the settled `live callers NONE` boundary.
Therefore transcript order-repair behavior remains dormant/unverified in this
successor until its later approved schema/registry composition.

Excluded: unACKed effects, position, producer, mixed-track operations, WC10
unmerged markers, D13 unsafe code, after-anchor pending source, native/HTTP
qualification, full/browser/render suites, new schema/version, pin/freeze,
generation, activation, Runtime/App/Composition changes, and live callers.

