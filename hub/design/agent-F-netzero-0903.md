# F / R2 net-zero recorder qualification — agt-F-netzero-0903

Result: the three assigned original nodes now PASS. This is a C0-backed oracle
adaptation with independent no-weakening approval, not a production inverse repair
or proof of actual Runtime acceptance. No contract change was needed.

## Source and delta

- Assigned worktree `/home/user/work/wt/agt-F-netzero-0903`, branch
  `tl/agt-F-netzero-0903`, starting HEAD
  `fad05679ae45ff4eb32190fdae40ae1cd1e56db6` (F-provider-0847 base). The external
  harness committed the patch as `9558fdc3111f0a56234fba70ce7a25b5cf711822`
  at 09:08:24Z while this session continued; the worktree is clean. The worker
  performed no Git writes. The committed diff from the starting HEAD matches
  the reviewed/tested binary diff hash below exactly.
- Changed only the three assigned test cases in
  `tests/editing_conformance/test_recipe_add_delete_composition.py` (+24/-4) and
  `tests/editing_conformance/test_recorded_graph_roots.py` (+36/-7, including import).
- Final binary diff SHA-256:
  `27c8e04f18241cfa61a1787525618419e6074f23f5b27fb01873722dff8c4ec9`.
- Read PLAN §3 F/R1/R2/V2/V3, C0, BOARD-HEADER, and
  `design/agt-F-provider-0847.md` in ORCH. External Runtime HEAD observed during
  testing: `7ca1a227815404252fec1e4768e550610f9c5705`; tests used the requested
  checkout and existing recipe/executor fixtures, not a live Runtime service.
- Scratch marker resolves to `/tmp/w-419a32d617`; logs/caches are private there.
  No shared dependencies, environment/service rows, pins, frozen34e/d106,
  normalmaps, baselines, or production files changed. No Git writes, fetches,
  merges, commits, checkouts, pushes, deletes, installs or service requests.

## Recorder boundary and retained behavior

C0 §2 lines 388–438 distinguishes the native command recorder from provider effect
projection and requires grouped inverse/redo segment boundaries and ordered ranges.
Lines 502–503 explicitly retain intermediate effects despite equal final values.
§5 lines 1594–1611 requires each step's sequential input/output states and inherited
allocation provenance. PLAN R2 requires whole/per-step guards and later-history
scans, including ABA. The existing inverse source already implements these rules;
coalescing it to satisfy the old raw-write assertion would discard required history.

The raw command recorder now has an exact independent oracle for every complete
intermediate write (including tagged absence, nulls, opaque fields, and order):
clip restore then remove; graph shot restore, occurrence restore, occurrence remove,
shot remove. Its coalesced boundary projection is still exactly absent→absent.
Graph coalescing follows first appearance (shot then occurrence), while raw writes
separately enforce child-before-owner creation and owner-before-child removal.
The original coalesced-only graph assertion's opposite raw ordering was not an
execution-order requirement; the boundary absence facts are retained exactly.

Exact `created` lists now describe transient restoration by the existing
`Recording.create`/`create_entity(restoring=True)` path; empty lists would erase
that recorder fact. They do not represent fresh allocations, authorize reserved-ID
reuse, or establish new source authority. Final root absence, canonical graph
documents, native authored documents (with the original fixture revision-name
normalization), native replay equality, undo/redo success and original-history
immutability all remain asserted. Added exact absent reads and atomic refusal of
intermediate-payload corruption on original, undo and redo records. Native negative
inverse/redo cases reuse the existing accepted-boundary fixture with their actual
executed input/output bundles, so they exercise the intermediate guard rather than
fail for missing legacy order context.

`inverse.py`, `_commit_patch.py`, physical bindings, stage ranges, materialization,
created reservations, equal-state/ABA and surviving-consumer logic are unchanged.
The production caller remains on its existing SDK/engine path; no helper or alternate
executor was added. The full v2 request/reply surface is unchanged: api_version,
project/timeline/base revision+publication, commands, label, complete steps
(id/label/intent/tags/command_ordinals/patch/reads), merge/reads/key/dry_run/source/
rationale/group_id; {data,receipt}, accepted|merged|historical-rebased,
head/document/records/dependencies/effects/steps/history/undo_steps,
preview.would_status, conflict reason/head and invalid code/path/hint/command.
This preservation statement does not qualify that entire surface.

## Commands and results

All commands ran from the assigned worktree. Exact final three-node command:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recorded_graph_roots.py::test_generic_net_zero_root_edges_inverse_redo_preserve_absence_and_created_facts 'tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[False]' 'tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[True]'
```

Exit 0: **3 passed in 13.64s**, `/tmp/w-419a32d617/exact-final.log`.
Initial reproduction selected the same generic node and the unparameterized native
node (both variants): exit 1, **3 failed in 4.87s**, at the old raw-write assertions.
An intermediate development run was 1 passed / 2 failed in 10.83s: the added native
negative cases used raw inverse records and got `history_unavailable` for missing
accepted insertion-order boundary before reaching the intended payload guard.
Reusing the existing actual accepted-boundary fixture fixed that negative setup;
all original positive expectations stayed unconditional.

Focused unchanged guard neighbors:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_add_delete_composition.py::test_net_zero_preserves_disjoint_change_and_guards_unchanged_address_history tests/editing_conformance/test_recipe_add_delete_composition.py::test_net_zero_refuses_changed_selection_or_declared_dependent_atomically tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_explicit_clear_between_add_and_delete_restores_original_presence tests/editing_conformance/test_recorded_graph_roots.py::test_created_root_child_same_value_and_aba_publications_refuse tests/editing_conformance/test_recorded_graph_roots.py::test_created_shot_later_occurrence_dependency_refuses tests/editing_conformance/test_recorded_graph_roots.py::test_creation_inverse_after_compiled_reload_restores_original_absence tests/editing_conformance/test_recorded_graph_roots.py::test_creation_inverse_redo_reuses_exact_roots tests/editing_conformance/test_step_undo_v2.py::test_whole_inverse_records_each_sequential_reversal_instead_of_coalescing tests/editing_conformance/test_step_undo_v2.py::test_aba_tail_refuses_even_when_the_current_guard_matches tests/editing_conformance/test_step_undo_v2.py::test_later_captured_read_blocks_whole_undo_even_if_its_write_is_disjoint tests/editing_conformance/test_recipe_m1_commands.py::test_same_value_writes_and_presence_are_authoritative
```

Exit 0: **15 passed in 29.23s**, `/tmp/w-419a32d617/neighbors.log`. This includes exact
sequential native stage ranges, equal-valued writes, explicit absent/null clears,
ABA, later captured reads, surviving consumers, disjoint preservation and reload.

Required quality commands (plus scoped Ruff), with final results:

```bash
env PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-419a32d617/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
env PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-419a32d617/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
env PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-419a32d617/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_recipe_add_delete_composition.py tests/editing_conformance/test_recorded_graph_roots.py
git diff --check
```

- Normal Ruff: exit 0, **current=2149 / baseline=2149**, `ruff.log`.
- Mypy: PENDING; completion will be recorded before DONE.
- Vendor lock: exit 0, `ok runtime.lock.json`.
- Artifact manifest: exit 0, `artifacts.json is current`.
- Scoped Ruff: exit 0, `All checks passed!`.
- Whitespace: exit 0, clean.

## Independent review, limits and handoff

User-required independent read-only reviewer `/root/no_weakening_review` approved
the final two-test adaptation, including the native boundary-fixture refinement:
no blocking weakening; exact sequential payloads/order plus coalesced absence,
restoration facts and original positives retained. Reviewer ran no tests.
Full review is in this worker's `independent-review.md` outside the worktree.

No full suite, Runtime acceptance/stage-auth matrix, P1/P4HTTP, native14, crash24,
heavy journey, browser or live-socket suite was run or requested. No skip/xfail,
positive-to-refusal conversion, budget increase, invented capture authority,
request schema or launcher/ledger work. Current failures alone establish neither
integration introduction nor upstream431 status; no such claim is made here.

No blocker or unresolved contract decision in this bounded adaptation. Recommend
lane review and serial adoption of the harness commit. Runtime wholeinverse stage
authentication remains owned by `rt-R2r-inverse-stage-0853`; `_commit_patch.py` is
parent-owned. Other F-provider0847 preview/V2/V3 residual owners remain separate;
this worker did not repair or requalify those nodes. The harness has already committed the unchanged tested patch; the intended
commit message remains in the assigned `commit-msg` file. At 09:08:22Z it wrote
STOPPED with “orphan finalized by request: died in container restart
(ensure-daemons)” and exit 143. This agent session nevertheless continued,
completed the report, and awaited the already-running mypy check (its private
cache was still advancing at 09:10Z). Do not confuse the harness lifecycle
marker with a product test failure or a safety/permission denial.
