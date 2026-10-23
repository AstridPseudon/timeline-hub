# F-D22 exact integrated proof

## Verdict

**PASS.** This is a proof-only qualification of the actual integrated Agent tree; no product, test, generated, pin, lock, dependency, environment, daemon, Git ref, or shared dependency changes were made.

Source under test:

- Agent HEAD: `ec43a1dc859db44bbd57965b95e744280bfd1361`
- Agent tree: `94f9e81893f4e833a1ecef2b744f753397d5e37b`
- Base: `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`
- Runtime producer for lock check: `34eac0041b0891e9011966b39bcbd26053fde5bc`
- Runtime test checkout: `3b926efab2eed122d374540baee297d4cdcec62a`

The requested `scratchpad/luna/reports` path was absent. The reviewed inventory/profile reports were found and used from `scratchpad/orch/design/` and the corresponding worker report directories.

## Scope and custody

`git diff --name-only 58316fd6..ec43a1dc8` contains exactly 7 files:

1. `docs/giant-file-rationale.md`
2. `tests/packs/rendering/test_am_snap_plate_scene_capability.py`
3. `tests/packs/rendering/test_remotion_backend.py`
4. `tests/packs/rendering/test_remotion_layer_tail_compat.py`
5. `tests/packs/rendering/test_remotion_typecheck_mappings.py`
6. `tests/sdk/test_timeline_composed_schema.py`
7. `tests/sdk/test_timeline_current_union_schema.py`

Current blobs equal independently reviewed donors:

- dca0aefaf72eb871bfedb3dfb99278ae14ce7cc1: rationale and both schema tests.
- 42476c08a6ffd318d7eb7100d48edceff7313ad6: all four profile tests.

The canonical inverse-containing schema is unchanged and SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. `runtime.lock.json`, `remotion/package-lock.json`, and the checked-in 819acf artifact are byte-identical to base. The installed profile artifact also hashes to `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. No tracked report artifact exists.

## Bounded integrated selection

Exact collection first produced 15 nodes: the inventory-review six selectors expand to 12 nodes, plus the three profile mapping parametrizations.

Final command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules \
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages \
PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden \
  tests/sdk/test_timeline_composed_schema.py::test_inverse_schema_accepts_whole_and_selected_step_forms_and_rejects_bad_shapes \
  tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort \
  tests/sdk/test_timeline_current_union_schema.py::test_every_dropped_operation_is_reported_despite_the_open_generic_envelope \
  tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions \
  tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale \
  'tests/packs/rendering/test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped[effects]' \
  'tests/packs/rendering/test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped[animations]' \
  'tests/packs/rendering/test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped[transitions]'
```

Result: **15 passed in 59.77s**, exit 0.

A setup-only first invocation without the reviewed Composition environment produced 12 pass / 3 failure because the mapping tests could not find the installed Composition manifest. The exact corrected invocation above passed all 15; no assertions or test bodies changed.

Reviewed mutation evidence was retained rather than broadening the run: exact 30-operation wire union, 31-operation provider cohort, and 31 closed-argument unknown-key refusals/missing-wrong-extra operation refusals. The six known-red geometry/audio/import nodes, old 8c qualification, broad 40-node profile run, P1/P3, and full suite were not repeated.

## Static checks

Commands and results:

- `MYPY_CACHE_DIR=/tmp/agt-fd22-mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` — **PASS**, current 1912 / baseline 1912, zero added.
- `RUFF_CACHE_DIR=/tmp/agt-fd22-ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python` — **PASS**, current 2149 / baseline 2149, zero added.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **PASS**, matches producer manifest.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — **PASS**, artifacts current.
- `git diff --check 58316fd6..ec43a1dc8` — **PASS**.
- Final `git status --short` — **clean**.

C0 request/reply production behavior remains retained because the cumulative integrated diff changes only the seven documented rationale/test files; no production caller or schema/lock/inverse bytes changed. No further qualification is claimed beyond this bounded proof.
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-F-D22-joined-integrated-1535.md
