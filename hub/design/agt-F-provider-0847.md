# F-provider 0847 — bounded R1/R2 repair

Result: **one current source defect repaired; original ten-node group remains 3 PASS / 7 FAIL**. This is not a full-suite, whole-contract, Runtime-authentication, integration-regression, or upstream-preexisting claim.

## Source and scope

- Assigned worktree: `/home/user/work/wt/agt-F-provider-0847`, branch `tl/agt-F-provider-0847`.
- Exact starting/current HEAD: `e837e18c5156e762eca05e6d9bb15779cf847b60`. No Git writes, commits, merges, fetches, checkouts, pushes, dependency changes, pin changes, or deletions performed.
- Final uncommitted binary diff SHA-256: `809f2fff19227999fad253686591f73be77992423a693efabcfba49d9416fc48`.
- Only changed files: `astrid/sdk/timeline/_commit_patch.py` (+13/-11), `tests/editing_conformance/test_recipe_m2_video_unplace.py` (+26/-1). The removed test line is import placement only; no original assertion or behavior expectation was removed or changed.
- Read PLAN §3 F/R1/R2, C0/header, classification 0815, exact sole service 4249 `summary` and relevant terminal-log trace sections, classification review 0845, R2 review 0836, Runtime peer 0845. No baseline 431 was needed or run.
- The author classification's causal label is unproven: current failing assertions establish current source-backed failures, not integration introduction. Independent classification review 0845 reaches the same conclusion. No byte-identity inference used.
- External Runtime checkout was read at `eb13b2051d4d30a4d8b7df8878bb7451701eab5a`; named tests use their existing detached ABI fixture. This is not actual Runtime acceptance evidence.
- The worker's `tmpdir` path is a harness marker file containing `/tmp/w-7138ce667f`; all scratch logs/caches were written to that resolved private directory. An initial redirect to `tmpdir/repro.log` failed before test execution; the first meaningful reproduction below used the resolved directory. No environment-worker 0840 provisioning changes were duplicated.

## Exact cause and production change

`RuntimeCommitService.commit` passes the actual request and evaluated head to `commands.execute`, which creates `CommitPatch` and calls its `finish`. ABI-1 semantic requests without explicit `label/steps/merge/reads` are active commits with synthesized authoritative steps, but `CommitPatch.v2` is false. The old `finish` gate emitted both effect bindings and `commit.materialization` bindings only when that flag was true. Native edits changed shot/internal revision pins without retaining the source-to-successor proofs. The existing inverse address resolver consequently refused with `history_unavailable: missing authenticated materialization history`.

Moved only materialization-proof emission outside the explicit-v2 gate. Every active step now derives the existing proofs from its verified input/output closures, retaining exact owners, source digests/revisions, successor edges, evaluation boundaries and inverse segments. Explicit-v2 effect binding emission remains gated as before. The original three M2 positive round trips now pass. This runs through the existing provider/SDK executor path; no unused helper or alternate executor was added.

C0 §1 normalizes omitted semantic steps rather than exempting them from authoritative metadata. C0 §2 (lines 333–354 in the read contract) requires authenticated native materialization provenance before following successors. Grouped-inverse stage unions/ranges (lines 406–413) remain intact. The change neither grants continuation from equal bytes nor bypasses a missing or damaged proof.

The existing video-unplace test still unconditionally checks exact undo/redo canonical documents. It now also checks shot and internal proof presence in all four variants. For `keep=True`, the pooled step consumes an intermediate physical image: removing its materialization proofs or changing successors must refuse with `history_unavailable` and preserve head, entries, documents and accepted state. These are negative tamper checks against the existing detached fixture, not fabricated positive authority.

A development run initially applied these new negatives to `keep=False` too (2 failed / 2 passed). That assumption was too broad: a single native command can reverse using native captures without needing the intermediate-image continuation. The final negative loop is explicitly scoped to the two original `keep=True` cases; all original success assertions and the new proof-presence assertions remain unconditional. Final four-variant result: 4 PASS.

No `inverse.py`, Runtime auth, request/reply schema, client, tuple, pin, adoption, renderer, launcher, ledger, or process rules changed. Existing R1 mirror, G2 hydration, fork, V2 and G234 sources are untouched. The full C0 request/reply surface is unchanged: api_version/scope/base pair/commands/label/steps (including id,label,intent,tags,command_ordinals,patch,reads)/merge/reads/key/dry_run/source/rationale/group_id; replies retain data/receipt, accepted/merged/historical rebased, head/document/records/dependencies/effects/steps/history/undo_steps, preview would_status, conflict reason/head and invalid code/path/hint/command. This is a preservation statement, not qualification of every surface.

## Commands and results

All commands ran from the assigned worktree. No full suite, live socket/browser, renderer-heavy, tour, Gate 5, P1/P4 HTTP, native14 or crash24 run was requested or run. Collection and body results are separate.

Exact original ten-node command (same command for initial reproduction and final bounded rerun):

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recorded_graph_roots.py::test_generic_net_zero_root_edges_inverse_redo_preserve_absence_and_created_facts 'tests/editing_conformance/test_producer_insertion.py::test_provider_preview_reads_exact_parent_media_selections_without_accepting[False]' 'tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[False]' 'tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[True]' tests/editing_conformance/test_recipe_m2_shot_pool.py::test_promotion_and_keep_as_pooled_round_trip_through_the_provider 'tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order[True-image]' 'tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order[True-video]' tests/sdk/test_timeline_commit_provider_scalar.py::test_provider_refuses_old_param_basis_after_admitted_element_update tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_created_child_stages_reload_inverse_redo_exact_closure tests/editing_conformance/test_compile_contracts.py::test_render_pin_gives_element_clips_the_clip_look
```

- Exact-base first meaningful reproduction: exit 1, **10 failed in 12.16s**; `/tmp/w-7138ce667f/repro.log`.
- After source repair, three original M2 nodes: exit 0, **3 passed in 14.44s**; `/tmp/w-7138ce667f/repair-three.log`, command below.
- Intermediate ten-node run after new negatives: exit 1, **7 failed, 3 passed in 14.58s**; `after-ten.log`.
- A pre-final-import/conditional ten-node run also had 7 failed / 3 passed; superseded for final-tree credit.
- Final exact tree: exit 1, **7 failed, 3 passed in 23.02s**; `/tmp/w-7138ce667f/final-bounded-ten.log`.

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_shot_pool.py::test_promotion_and_keep_as_pooled_round_trip_through_the_provider 'tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order[True-image]' 'tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order[True-video]'
```

Exact final collection-only command: exit 0, **10 tests collected in 3.61s**; `final-collect.log`:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recorded_graph_roots.py::test_generic_net_zero_root_edges_inverse_redo_preserve_absence_and_created_facts 'tests/editing_conformance/test_producer_insertion.py::test_provider_preview_reads_exact_parent_media_selections_without_accepting[False]' 'tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[False]' 'tests/editing_conformance/test_recipe_add_delete_composition.py::test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[True]' tests/editing_conformance/test_recipe_m2_shot_pool.py::test_promotion_and_keep_as_pooled_round_trip_through_the_provider 'tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order[True-image]' 'tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order[True-video]' tests/sdk/test_timeline_commit_provider_scalar.py::test_provider_refuses_old_param_basis_after_admitted_element_update tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_created_child_stages_reload_inverse_redo_exact_closure tests/editing_conformance/test_compile_contracts.py::test_render_pin_gives_element_clips_the_clip_look
```

All variants of the touched named test: exit 0, **4 passed in 12.56s**, `final-video-all-params.log`:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order
```

Required quality commands, all run on the final source/test diff (scratch cache locations are private):

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-7138ce667f/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_recipe_m2_video_unplace.py
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-7138ce667f/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-7138ce667f/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

- Scoped Ruff: exit 0, all checks passed (`final-scoped-ruff.log`). Initial import sorting failed once and was corrected with scoped Ruff import formatting; no suppression or baseline edit.
- Normal Ruff: exit 0, **current=2149 / baseline=2149** (`final-make-ruff.log`).
- Mypy: exit 0, **current=1912 / baseline=1912** (`final-mypy.log`).
- Vendor: exit 0, `ok runtime.lock.json` (`final-vendor.log`).
- Artifacts: exit 0, `artifacts.json is current` (`final-artifacts.log`).
- Whitespace: exit 0, clean. No budget increased.

## Remaining seven nodes and exact next slices

1. **R2 / existing inverse owner review0836 — three net-zero nodes**: `test_generic_net_zero_root_edges_inverse_redo_preserve_absence_and_created_facts` and both `test_native_add_delete_net_zero_inverse_redo_retains_unchanged_write[False/True]`. Their first failing assertion requires one coalesced absent→absent `records[0].writes` row; current `apply_inverse` records ordered intermediate reversals (e.g. absent→present, then present→absent). `inverse.py:690–730` deliberately retains sequential guards/stage ranges. Do not treat this alone as proof of a behavior regression, erase sequential provenance, or change the assertions without C0 justification and independent no-weakening review. Exact owner finding is the raw-write oracle versus retained sequential recording; the original created-history/absence/redo expectations remain unchanged. **Recommended next bounded slice**: these three net-zero recorder/oracle cases under the existing R2 owner, preserving created reservations and explicit equal-state/ABA guards. `inverse.py` was not edited.
2. **R1 preview capture oracle — one node**: provider preview differs only by the context-derived `commit.input` physical binding on command ordinal 2. The direct recipe `plan.records` has no request/evaluated-head context; the provider has `boundary.base_revision_id=parent-1`, `base_publication_id=bootstrap`, `evaluated_head` same, `step_id=edit`, `phase=input`, and the intermediate compiled parent revision/digest. `CommitPatch.before` emits this for a prior command's changed image. C0 requires evaluation-boundary facts. Next slice should establish a context-aware expected recorder and retain exact selections, authoritative records, canonical document and zero-accept checks; no oracle change made here.
3. **V2 / scalar fixture owner — one node**: `test_provider_refuses_old_param_basis_after_admitted_element_update` fails on the initial `clip.add` before reaching the intended stale-schema refusal. The newly selected project element has no unique retained schema; the test installs its `schema_options` source/snapshot inputs only after adding it. Next slice must supply authentic retained project-pack schema metadata at the creation boundary and at the replacement, then preserve the original `dependency_changed` and no-state-change assertions. No schema validator relaxation or fake authority is appropriate.
4. **V2 / graph fixture owner — one node**: `test_authenticated_created_child_stages_reload_inverse_redo_exact_closure` fails final validation on initial creation: `child_ops` ends with title hold=3 seconds while the new occurrence has duration_ms=2000. This violates final half-open bounds. Next slice should repair authentic fixture timing for that intended child-stage positive, preserving hold=3, exact reload/undo/redo closure and creation facts. No positive was converted to refusal, skipped or xfailed.
5. **V3 / Composition adoption-test owner — one node**: `test_render_pin_gives_element_clips_the_clip_look` calls `.groups()` on a regex that accepts semver tarball URLs; the existing pin is a file artifact identified by commit SHA (`file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`). It fails before checking ClipLook behavior. Resolve through existing adopted-artifact metadata/behavior in a separate bounded test slice. No new pin, schema or adoption made, and no renderer behavior claim inferred from filename identity.

Runtime peer0845 remains the separate whole-multi-step inverse stage-authentication owner. Its exact error is `invalid_records: provider binding differs from its authenticated input image`; current Runtime authenticates intermediate before/after images against enclosing-step endpoints. Preserve native/effect ranges, exact stage unions, digests, owners, allocation history and forgery guards. This worker neither repaired nor bypassed Runtime authentication and did not rerun the existing 53/58 matrix.

## Independent review and handoff

A separate read-only Luna reviewer (`/root/independent_review`) reviewed the source change and the final test conditional. Verdict: safe/in scope; no inverse-stage/range, physical-ref, created-history or null/absence weakening found. It explicitly approved that only `keep=True` needs the added continuation-refusal checks; original exact undo/redo assertions stay unconditional. Reviewer did not run tests; the command results above are this worker's evidence. This does not turn the seven remaining failures or actual Runtime authentication into PASS.

The bounded source repair and required checks are complete within the 25-minute useful-work limit. The harness must create the worker's own commit only; no merge was attempted. Commit message is in this worker's `commit-msg`. Agent merge queue/orchestrator decides adoption with the seven failures and Runtime limitation visible. Recommended next work is the three-node R2 net-zero slice above, without touching that owner's source concurrently. No frozen-authority decision was guessed or required for the completed repair.
