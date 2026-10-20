# Runtime parent/config clip agreement after refresh

Verdict: **neither main nor the refresh dropped agreement validation. No product fix is needed.** Audited Runtime `8609333` against old integration `c0dcd38`, refresh `557a28a`/`a5a4f6b`, and main `fc7979e`/`29d0954`. Contradictory populated parent/config clip lists cannot be newly accepted through commit or preview. Current render and inspection independently refuse correctly hashed contradictory retained bytes. Historical render refuses corruption against its accepted publication.

## Before/after and source

- Main `fc7979e` (`fix(render): the visual seam check advises render admission and never blocks it`) removes only the `report["blocked"]` exception in `visual_seam.admit_closure`. Its service/store changes are explanatory comments. **Its `parent_clips` disagreement exception remains**, as does the store's then-duplicated check. Main `29d0954` changes disk estimation and its tests, not agreement validation.
- Our reviewed `e8b0302` (combined into `5ef5c56`) added pure `parent_clips(parent["payload"])` to `TimelineCommitStore._validate_closure`, translating malformed/disagreeing aliases to `422 invalid_closure` before persistence. That call remains at `8609333` in `runtime_protocol/timeline_commit_store.py:410`; `_validate` invokes it at line 536; `revision_closure` invokes it for retained documents at lines 273/290. No scene evaluation is needed.
- Our `ed22079` extracted the existing disagreement condition into **one `agreed_clips` helper**, replaced the duplicate store check with `parent_clips(payload)`, and routed inspection through `agreed_clips`. This was a deduplication, before the refresh, not removal by main.
- `git diff c0dcd38 8609333 -- runtime_protocol/visual_seam.py runtime_protocol/timeline_commit_store.py runtime_protocol/timeline_inspection.py` contains **only** main's advisory `admit_closure` change. The agreement helper, commit check, and inspection call sites are unchanged. `store.py` retains `parent_clips(payload)` at line 1943 after materialization; normalization also calls it at `visual_seam.py:254`. Publication's advisory evaluation remains before its first mutation (`RuntimeService._publish_parent_composition` in `service.py`); tracked legacy publication is refused in favor of commit.
- Refresh test adaptation in `test_canonical_render_admission.py` changes the new upstream advisory fixture to use current canonical acceptance, then evaluates the **saved CanonicalDocument**. The existing contradictory-list refusal test was not removed. No tests or product code were changed by this audit.

## Actual probes

Reproducer and complete output: `workers/rt-m2-parent-mirror-refresh-audit/probe.py` / `probe.log` under the orchestrator directory. Run from the assigned Runtime worktree:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:$PWD/tests:$PWD/packages/python /home/user/work/venv-runtime/bin/python "$ORCH/workers/rt-m2-parent-mirror-refresh-audit/probe.py"
```

Result: **PASS**, 14 historical refusals, 2 public service commit refusals, 6 supported alias render/inspection projections, 12 retained-corruption refusals. Every refusal compared complete database dump and CAS files before/after; no writes. Temporary realms are removed by the probe.

| Boundary | Observed result |
| --- | --- |
| Historical module source from `fc7979e^`, `fc7979e`, `29d0954`, `c0dcd38`, `557a28a`, `a5a4f6b`, `8609333` | Both `parent_clips` and `admit_closure(materialize=True)` refuse contradictory populated lists with `ConflictError`, reason `canonical_payload_mismatch`. Real module bodies loaded with `git show`; shared stable support imports from current Runtime. |
| Public `RuntimeService.commit_timeline`, dry run false and true | Provider supplies validly rehashed contradictory prepared candidate; both return validation error `422 invalid_closure`, exact disagreement message; no DB/CAS mutation. This uses the prepared fixture provider, not Agent semantics. |
| Supported parent-only, config-only and equal-populated aliases | Save/reload preserves exact authored payload; inspection and BOTH current/historical render select `scene-a, scene-b, music` consistently (six render admissions). Empty list means absent mirror under established semantics; it is not a second contradictory authority. |
| Current `create_task(rendering.render)` after stored payload AND content digest changed to contradictory lists | `409 conflict`, reason `canonical_payload_mismatch`; zero task/run/CAS/database changes. Not merely a stale digest failure. |
| `inspect_timeline` on those bytes | Same `canonical_payload_mismatch`; no mutation. |
| `TimelineCommitStore.revision_closure` on those bytes | `422 invalid_closure`, exact disagreement message; no mutation. |
| Historical `create_task` using original accepted five-field revision selector | `409 conflict`, reason `render_revision_integrity`; original accepted publication protects against subsequently altered bytes. This intentionally does not forge an accepted ledger/receipt. |

## Permanent test evidence and gates

Existing regressions retained: `test_canonical_conflicting_populated_clip_lists_fail_closed` (commit + preview and complete DB/CAS preservation), `test_canonical_payload_mismatch_conflict_carries_machine_readable_reason` (shared helper and inspection), `test_parent_clip_aliases_preserve_opaque_values_and_exact_retry` (renderer unavailable, opaque values, reload, exact-retry precedence), `test_parent_clip_projection_uses_one_canonical_list`, and `test_render_materialization_still_rejects_invalid_timing`.

Direct command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_canonical_render_admission.py::test_canonical_conflicting_populated_clip_lists_fail_closed tests/test_shot_composition_runtime.py::test_canonical_payload_mismatch_conflict_carries_machine_readable_reason tests/test_timeline_commit_acceptance.py::test_parent_clip_aliases_preserve_opaque_values_and_exact_retry tests/test_timeline_native_inspection.py::test_parent_clip_projection_uses_one_canonical_list tests/test_visual_seam_admission.py::test_render_materialization_still_rejects_invalid_timing
```

Result: **11 passed in 6.30s**.

Central TestIDs/results are recorded below. Requested scope: ordinary render/seam, inspection, legacy authority, commit acceptance/closure/schema/port; legacy HTTP authority with the real Agent environment; real Agent commit integration. No full suite requested. Advisory custom-track/gap/overlap materialization and renderer-independent saves remain live expectations. No speculative stricter alias policy, schema or route change.

## Limits and follow-up

Evidence-only result: worktree product/test diff is empty. No new permanent test is necessary because the guard and permanent regressions already exist. Keep main's accepted advisory rendering behavior. This does not qualify the entire project, capture-host pair, real pixels/audio, owner films or macOS. Historical module probes are focused function probes, not historical full-suite replays. The prepared-provider boundary probes isolate Runtime validity; real Agent coverage is the separate central commit gate.

### Central results (initial requests)

All initial snapshots: Runtime tree `2ae8508a1d3dac62e99c27056585eedc62bf5ff6`, HEAD `8609333456b9537339ee1a5dfc7ffd9609242de8`.

| TestID | Result |
| --- | --- |
| `rt-m2-parent-mirror-refresh-audit-targeted-1020105948-9565` | 397 passed, 2 deselected, 65 setup errors; exit 1, 122.65s. All errors require `ASTRID_CHECKOUT`, absent from plain targeted lane; no assertion failures. |
| `rt-m2-parent-mirror-refresh-audit-occupancy-integration-1020105949-4913` | 58 deselected, exit 5, 0.50s; wrong marker lane, no tests executed. |
| `rt-m2-parent-mirror-refresh-audit-commit-integration-1020105949-18146` | 9 passed, exit 0, 13.91s; real Agent semantics, including renderer-unavailable commit/retry/undo and real door lost-ack restart. |

The 65 setup-error cases are 58 legacy-authority tests and 7 shot-composition restore/HTTP tests. They alone were re-requested with the documented `restore-integration` environment. The two dispatch mistakes are retained here explicitly; neither changes the source verdict. Exact request, executed pytest and wait commands are in the worker's `DetailedReport.md`; central results live under `tests/TEST_ID/{request,snap,summary,log.txt}`. No full suite requested.

### Final corrected gates

| TestID | Result |
| --- | --- |
| `rt-m2-parent-mirror-refresh-audit-restore-integration-1020110152-26597` | **58 passed in 22.51s**, exit 0; all legacy-authority service/HTTP cases. |
| `rt-m2-parent-mirror-refresh-audit-restore-integration-1020110232-10583` | **7 passed in 3.07s**, exit 0; exact restore/HTTP cases requiring the Agent checkout. |

All snapshots record the same Runtime tree above. Combined affected evidence: **397 + 58 + 7 = 462 distinct ordinary tests passed, plus 9 real-Agent commit integration tests**; 11 focused direct cases also passed. The original request's 65 setup errors were fully covered by the two corrected selections. The no-tests marker request provides no pass evidence. The two marked cases deselected by the ordinary selection were not silently counted as passes.

**Final: close the 10:46 parent/config agreement finding as disproved.** Agreement validity survived main and refresh; main's advisory track/overlap/custom-picture render behavior remains. No product fix, new permanent regression, policy change or integration patch is needed. Detailed commands, honest failed-dispatch records and limits are in `workers/rt-m2-parent-mirror-refresh-audit/DetailedReport.md`. Worktree clean; no full suite requested.
