# Agent R2 ABA cumulative final review — scoped PASS

Date: 2026-10-23  
Candidate: `255751f40a38263b8a032d15b807a3a3e2742a9c`  
Base: `78738040d72ce74c42ddf7731221aecb06f9246d` (`tl/integration`)  
Source pre-ABA repair: `65a2e5aec2447d6a3a937ba2c358a1e7c1651122`  
Review worker: `agt-R2-ABA-final-review-1852`

## Verdict

**PASS for the requested Agent source/static/security review and fresh provider conformance selections.** The 787→255 cumulative six-path diff is internally compatible, and the 255 repair resolves the previously reproduced provider-produced legal zero-effect native stage. No new source defect was found in the requested guards.

This is source/provider-fixture proof only. It is not Runtime HTTP/authentication qualification, a full R2 claim, root-d146 qualification, or approval of excluded suites. The structural effect-image/first-equal partition path is unchanged and remains the stated caveat; this review found no new legal structural ABA boundary that would justify changing it.

## Diff and static review

The cumulative 787→255 diff is exactly 710 lines across these six paths: `_step_undo.py`, `inverse.py`, `test_inverse_aba_partition.py`, `test_nested_inverse_order.py`, `test_nested_native_aggregate_partition.py`, and `test_nested_parent_mirror_ranges.py`. The unique 255 repair relative to 65 is the requested 9 insertions/4 deletions in `_step_undo.py`, plus the new ABA test.

The property-only native projection uses authenticated native write order and complete before/after state transitions. Accepted effect patches are checked as observations and are never applied as live mutations. The unchanged structural path still uses its existing effect-image partitioning, as required by the settled plan.

The reviewed guards cover:

- source publication and recorded intent, step identity, command ordinals, and full command/step partitions;
- contiguous native/effect ranges, including `[0,0]` effect ranges while requiring nonempty native ranges and complete native/effect coverage;
- native site/path, derived site/path, compiler cause, previous/after observations, and mirror coverage;
- physical binding owner, revision/content digest, resolver custody, and authenticated source identity;
- exact order/membership restoration before stage writes and after guarded restoration;
- guarded before/after writes, later writes including ABA, declared consumers, surviving assets/tracks/media/documents, and no-op staged writes.

`_root_inverse.py` is byte-identical to 787 (`0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`); d146 is separate and not credited here. No source, test, schema, pin, Runtime, environment, or Git ref was changed by this review.

## Fresh test evidence

Environment: `/home/user/work/venv-agent/bin/python`, Runtime pin `/home/user/work/wt/rt-pin-2a9e347f`, private `TMPDIR=/tmp/w-cc385f8f34`, no pytest cache. The independent capture plugin is in that private TMPDIR; compressed full captures are permanent in the evidence directory below.

Fresh NEW22, run once:

```text
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_final tests/editing_conformance/test_inverse_aba_partition.py
22 passed in 28.55s
```

Exact existing author selections, rerun independently on current source:

```text
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_inverse_registry_containers.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py
110 passed in 49.28s

/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_final tests/editing_conformance/test_inverse_clip_mirrors.py -k 'split_leaf_output_undo_redo_exact_document_and_causal_records or (split_then_native_leaf_command_restores_each_command_boundary and whole)'
5 passed, 30 deselected in 5.12s

/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -p capture_final tests/editing_conformance/test_recipe_m2_parent_media.py -k 'provider_exact_reload_inverse_redo_and_retired_ids or ordered_provider_reload_inverse_redo_and_retired_ids or (missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config)'
14 passed, 71 deselected in 20.30s
```

The fresh legal positive captured production whole and selected inverse calls through the SDK commit provider and detached Runtime ABI fixture. It observed the authenticated nested partition:

```text
stage b: native_write_range [0, 9], effect_range [0, 0]
stage a: native_write_range [9, 19], effect_range [0, 2]
19 native writes; first 9 are equal before/after; 4 derived compiler mirrors
```

The same capture observed accepted replies, three dry-run previews with `would_status=accepted` and `receipt=None`, unchanged head/entry counts for previews, and exact whole/selected closure round trips. The three strict public negatives refused forged `writes`, foreign publication, and foreign step authority without changing head or entry count. The foreign-publication detached fixture preserves its legacy refusal shape (`root_code=conflict`, `reason=history_unavailable`); the other two expose structured `code`, `path`, `hint`, and `suggested_command`.

No alternate executor was used. No test was skipped, weakened, deleted, or xfailed. No full/browser/socket/HTTP suite was run.

## Scoped quality and integrity checks

```text
/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_inverse_aba_partition.py
All checks passed!

/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_inverse_aba_partition.py --hide-error-context --no-pretty
Success: no issues found in 6 source files

/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
Ruff findings: current=2149 baseline=2149

/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
exit 0
```

Source fidelity checks: all 1068 pre-existing Python test bodies at 65 are byte-exact in 255; registry `coalesce` is byte-exact; the changed-path set is exactly the six expected paths. Actual loaded module hashes and before/after hashes are recorded in `evidence/integrity.json`; `_step_undo.py` is `003fc372...b7d202` before and `459151d5...fcf21c` after, while `inverse.py`, `commit.py`, and `_commit_patch.py` are unchanged. The requested credential-pattern scan produced no matches.

Permanent evidence (including SHA256SUMS, compact capture summary, compressed full captures, command logs, module hashes, and integrity checks):

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-ABA-final-review-1852/evidence/`

The only limitation carried forward is the settled structural-path caveat; recommended next step is orchestrator review of this scoped PASS and the separate root-d146 result before any merge/qualification decision.
