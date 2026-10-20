# Verified-source extraction owner review

**APPROVE** the bounded pure extraction. No blocking regression or concrete counterexample found. This is an extraction review, not whole-product qualification. No product files, tests, shared dependencies, git metadata, or integration worktrees were modified by this review.

## Reviewed identities

| Source | Commit | Tree |
| --- | --- | --- |
| Sourcebase | `140e84cc3726fe1e81a86f6d8eb86eb9688a7301` | `64ad7432505947d98d21904983bb1132b477a6fa` |
| Committed candidate `tl/agt-m3-verified-source-host-extract` | `b22e23acd68a0fda4cbaa64bd5923b5762265663` | `73df4effc3ce7b4b0d79a07a40fa630e3ce254c2` |
| Current review worktree | `ce363f6d6d60e504dbd4d79803c2d6299f648ade` | `78af007de1d7c5a59f86fffacd9823de355cd260` |
| Runtime used for in-process integration | `b748ae723b51c6d578ba7a393209ce37d6e2b0c3` | `1711b198be7f693f11ee4640eb0922ec0d0da952` |

Read PLAN.md, including the giant-file policy and owner decisions, and the extraction worker's complete report before reviewing. Current differs from sourcebase only in four documentation/test files; its two reviewed production files are byte-identical to sourcebase. The synthetic current-plus-candidate tree is `afb2ed8506a99a088d7be3dbadaf593338d2fb5a`, calculated without writing git objects. It overlays the candidate's three changed files onto current and includes the current CLI/sheet rationale and fixture repairs.

## Findings

- Scope is exactly `generic_host.py`, the existing `core/rendering/verified_source.py`, and additive tests in the existing verified-source test file. No count, threshold, tolerance, baseline, authority schema, or source format changes. Host size is **13,816**, versus recorded **13,798**, delta **18**, within the unchanged **50** tolerance; sourcebase/current host is 13,860. The candidate removes 44 host lines.
- One existing `PreparedTimelineInputs` container receives four lifecycle methods. They preserve the checkpoints: reject reserved envelope/params/input/backend keys before validation/fetches; select the exact admitted snapshot after existing hydration; refuse caller replacement before derived-file preparation; mint only after existing materialization; clear and validate the source environment anchor at the existing child-command checkpoint. Private per-call attributes retain the old local ref/authority/snapshot values. Dictionary keys cannot set those attributes or the source attribute.
- `capture_snapshot_ref` still replaces the selected source only for admitted revision/working-copy kinds, reuses the existing authorized CAS/hash-checking hydrator, and checks the duplicate filmstrip capture. Saved snapshot/ref/authority, unsaved candidate/base identity, materialized pair, and attempt confinement retain their original checks. Leftover snapshot metadata does not independently mint authority. No projector or admission-validator copy was introduced.
- The helper adds no I/O implementation, resolver/factory, persistent state, attestation, or new authority. Existing hydration/mint/validation calls remain; the full mint, validator, binding format, and reserved-key implementation are AST-identical. All other host methods are AST-identical. The normal input mapping and mutations retain their order; the earlier shallow container copy changes no nested ownership. Non-Timeline task values remain unchanged.
- Admission `ValueError` is mapped to `HostError` with the original literal text. Missing prepared keys preserve the original quoted `KeyError` text through that mapping. Malformed capture JSON retains `JSONDecodeError`. Fourteen literal refusal cases pass on both sourcebase and candidate; failures leave no verified binding and do not mutate caller specs. The additional missing-registry probe also confirms identical `HostError 'assets_registry'` and no published binding. Ordinary staged files may remain after late refusal, as before.
- Child forwarding still clears ambient `ASTRID_VERIFIED_TIMELINE_SOURCE`, validates the exact prepared paths/bytes, and transfers only the host source attribute. Dictionary copies do not retain source authority. The real child-command regression passes; environment isolation and modified-byte refusal tests pass.
- Cold generic-host imports load **no rendering modules** before or after. Base/candidate/current-plus-candidate import-cycle snapshots are identical: seven pairs and the same SCC. The existing checked-in baseline's missing `rendering ↔ timeline` pair is unchanged.

## Independent tests

Private source archives were created under the worker notes directory, without checkout/index/ref mutations. Shared Python dependencies and Remotion peers were read-only. Native scene fixtures build their own private temporary package and links and use no renderer/socket. No full suite, browser, live-socket suite, or `make check` was run or requested.

For the commands below, `notes` means the absolute directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-verified-source-extraction/notes
```

Run in `notes/candidate`, the exact committed candidate archive:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m 'integration or not integration' tests/packs/rendering/test_verified_source.py tests/sdk/test_capture_source_runtime.py tests/sdk/test_capture_closure_source.py tests/test_snapshot_reference_handoff.py
```

**111 passed, 6 xfailed, 301.22s.** Includes normal child-command forwarding, exact saved/candidate capture, real Runtime admission/claim/witness positives and forged capture refusals, authorized snapshot hydration, caller replacement, numeric identity, path/byte substitution, mutation checks, literal refusals, and environment handoff. Four existing strict xfails require downstream `RenderRequest` propagation; two require Runtime capture publication absent from the admission double. None were changed.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_generic_host.py -k 'input_materialization or hc04 or unified_edit_materialization or materialize_inputs or child_environment_carries' tests/packs/rendering/test_scene_source_carry.py tests/sdk/test_timeline_capture_projection.py
```

**11 passed, 335 deselected, 5.65s.** The global selection tests ordinary host materialization, typed parameters, CAS authorization/order/limits, registry media, optional mask, and runtime connection environment. Projection tests deselected here were run explicitly next:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_source_carry.py tests/sdk/test_timeline_capture_projection.py
```

**93 passed, 9 deselected, 63.10s.** Both native scene-query and transport cases pass; default lane excludes nine integration cases. Real Runtime capture integration is covered separately above.

Run in `notes/base`, sourcebase production with only the candidate's additive verified-source test file overlaid:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_verified_source.py -k 'literal_source_refusals or does_not_mutate or non_timeline or existing_json_error_type'
```

**19 passed, 38 deselected, 2.03s.** Independently confirms literal refusals, mutations, non-Timeline behavior, and JSON exception expectations already pass before extraction.

Run in `notes/current-pair`, the synthetic current-plus-candidate tree:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_structure_contracts.py
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_structure_baseline
```

**32 passed, 1 failed, 2.46s**; **structure baseline passed: current=14, new=0, fixed=0**. The failed inventory assertion reaches existing `astrid/core/rendering/service.py`: actual 2,367 versus recorded 2,314, delta 53. An independent enumeration also finds existing `remotion/run.py`: 1,929 versus 1,851, delta 78. Both production counts are identical on sourcebase, candidate, and current. Current CLI is correctly recorded at 4,127 and sheet at 1,313; neither is misclassified as unresolved. No threshold or inventory changes are recommended in this review.

On untouched current, the same inventory node was also run with the exact pytest command above restricted to `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`: **1 failed, 1.44s**, first on the unextracted host delta 62. The synthetic pair proves this extraction removes that blocker and exposes the separate Viewing drift.

Additional commands:

```sh
# From the review worktree, using the absolute notes path:
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-verified-source-extraction/notes/static_review.py
# From both notes/base and notes/candidate:
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python ../missing_prepared_key.py
# From notes/candidate:
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/core/rendering/verified_source.py
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.import_cycles --baseline scripts/reshape/baselines/import_cycles.json
# From the review worktree:
git diff --check 140e84cc b22e23ac
```

Static/differential probes, Ruff, and diff check **pass**. Import-cycle baseline command **exits 1** for the pre-existing pair noted above; independent before/after snapshots prove no regression. Logs and probe source are retained beside the worker report; private source archives/build caches are removed after review.

## Decision and remaining gaps

Proceed with the bounded candidate. The helper is a relocation of existing host admission steps, with no new source authority or behavioral loss found. No product decisions were changed and no permission escalation was needed. Nothing blocks completion of this review.

Viewing should resolve its existing service/run inventory drift through the PLAN policy; the existing import-cycle baseline drift and six downstream strict xfails remain separate qualification work. Full repository, browser/pixel rendering, and macOS behavior are unverified here. This approval does not claim those gates are green.
