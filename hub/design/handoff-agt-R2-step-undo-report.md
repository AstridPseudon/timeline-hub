# R2 staged implementation — integration blocked

Implemented native whole/per-step inverse mechanics in inverse.py, _step_undo.py and the directly affected _root_inverse.py/_collections.py helpers. Added tests/editing_conformance/test_step_undo_v2.py (35 passing tests). No commands.py, commit.py, public facade, CLI, emitter, Runtime, generated schema or pins were edited. No commits, merges, fetches, pushes, dependency installs or shared-environment writes were performed.

## Behavior implemented

- Select contiguous command runs from accepted records.steps, preserving the complete original entries, command ordinals, allocation facts and boundary loader. Unknown/duplicate/incomplete step selectors or recorder history refuse. Step effect patches are descriptions and never executable inverse instructions.
- Stage all native reversals in reverse execution order, preserving repeated/equal-state writes rather than installing only their coalesced result. Keep coalescing for the landing guard. Record target-step native write ranges in existing command bindings as `key: inverse.stage` with boundary publication_id, step_id, command_ordinals and native_write_range. These are native write ranges; provider effect ranges still require R1 projection.
- Scan each target's own later suffix, including later nonselected steps, native reads/selections/bindings, persisted field/collection/scope dependencies and compiler-derived writes. Collection dependencies distinguish shape from item contents. Same-publication dependents are rechecked inside apply_inverse. A→B→A remains a conflict despite equal final values. Gaps before a newer selected target do not become that target's later history.
- Preserve disjoint later edits and invert merged captures against their actual input/landing head. Keep native semantic restoration, source recovery and accepted collection-order proof. The wider tests exposed redo of birth→track→media after staging; fixed lazy historical insertion proof and absent-owner boundary orders. The original behavior test remains unchanged and passes.
- Expose a source-bound normalization seam, including bound-owner identity guards. Physical-bound records without an authenticated provider resolver refuse with history_unavailable. No successor is inferred by entity ID, bytes, digest equality or a current alias lookup. The physical normalization tests are seam tests, not C0c provider proof.

## Exact validation

The literal brief command first failed during conftest collection (exit 4): shared venv-agent has no installed runtime_protocol. Read-only Runtime source exposure fixed collection; no shared venv was modified.

Initial requested acceptance, with the necessary source path:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py
```

Result: 265 passed in 28.05s at that stage. The final combined run below includes all three acceptance files after the final behavioral changes.

Identified existing inverse/restore neighbors using `rg --files tests` and further `rg --files tests/editing_conformance` searches. Final combined targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/editing_conformance/test_recipe_occurrence_create.py tests/editing_conformance/test_recipe_occurrence_delete.py tests/editing_conformance/test_native_word_anchor_vectors.py tests/editing_conformance/test_recipe_text_binding_native.py tests/editing_conformance/test_recipe_parent_media.py
```

Result: **548 passed in 38.45s**. An additional last bounded-owner guard test change was separately verified in the 35-test step suite before this final combined run. No assertions were weakened, skipped or xfailed. No full*, browser or socket suite was requested or run.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_collections.py tests/editing_conformance/test_step_undo_v2.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m mypy --follow-imports=skip astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_collections.py
git diff --check
```

Results: all checks passed; no mypy issues in four source files; whitespace clean.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime make ruff mypy PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime make mypy PY=/home/user/work/venv-agent/bin/python
```

Repository gates: combined make exits 2 at Ruff because current findings 2157 are below locked baseline 2159, requiring a baseline refresh. Original HEAD inverse.py/_root_inverse.py have zero scoped Ruff findings; modified files are also clean. Baseline was not changed. Independent make mypy exits 2 before checking completes: missing types-PyYAML and NumPy stub syntax requiring Python >=3.12 while repo config targets 3.11. Scoped checks are not a claim of repository-wide green.

## Decisions and integration blocker

No contract decisions were changed. Native recorder stages and accepted boundaries remain the inverse authority, rather than submitted patches or rewritten history. Existing authenticated native whole-inverse history remains supported; no historical steps are synthesized to authorize partial undo.

Early seam notes: seam-20261022T2315Z.md and progress-20261022T2320Z.md. R1's interface-progress.md confirms its new writes remain native State addresses and physical associations are in bindings (physical_ref/path/write_range/owners/boundary). The staged helper API is:

```python
selected = select_inverse_records(accepted_records, inverse_args.get('steps'),
                                  address_resolver=authenticated_resolver)
check_later_steps(selected, complete_ordered_history, state=landing_state)
# execute/replay receives selected as inverse_records.
```

The resolver receives `(capture, ref, path)` for native reads/writes, step dependencies, selection captures and bound-owner guards. It must preserve the originating boundary/owner and authenticate each continuation, including still-reachable old branches. R2 deliberately does not invent that provenance or silently retarget.

**R2 is not complete end to end.** Its remaining integration needs R1's concrete source and a manager merge-forward before work can safely finish without overlapping R1-owned files:

1. Provider dispatch selects accepted native captures and scans contiguous target→evaluated-head history on every CAS attempt, including authoritative dependencies from new later entries. The inverse args.steps validator/generated adoption must permit the selector; records.undo_steps must persist it.
2. R1 supplies authenticated physical address normalization and successor/edge provenance; current developing rebase_patch keeps continuation nested rather than exporting a reusable inverse resolver. Missing normalization currently refuses rather than restoring an arbitrary owner/image.
3. commit._inverse_media_removals and _inverse_clip_transcripts must consume `entry_records(selected, entry)` while retaining full immutable source boundaries; their current flattened-full-entry assumption rejects partial selections even for a note-only inverse.
4. Provider effect projection must use recorded inverse.stage native ranges to build each reversed target-step's verified before/after union and persist the corresponding effect ranges. A final-only diff loses transient root restoration/redo effects.
5. After that merge-forward/integration, run the actual contract two-patch reads and two-child/multiple-shot C0c creation/edit/undo/redo/provider scenarios. Current native tests and resolver seams do not qualify these requests or Runtime adoption.

Recommendation: manager merge-forward R1/U2 into this worker and resume the bounded R2 integration, preserving R1 ownership. **Merge hold is separate:** C0c approval plus R1/U2 integration remain required before landing. BLOCKED is written, DONE is not. No source safety/classifier denial occurred.
