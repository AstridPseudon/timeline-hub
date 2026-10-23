# F-agent D22 terminal inventory

## Result

The sole authorized service `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679` is terminal: **fail**, exit **1**, elapsed **3712.16 s**. The service summary reports **185 failed, 16,733 passed, 4 skipped, 19 errors, 86 warnings, and 565 passed subtests**. The terminal marker census is `.=16,733, F=185, E=19, s=4, u=565`; `u` is resolved by the summary as passed subtests, not unknown failures.

This report and the adjacent hashed JSON inventory preserve the exact 204 failed/error node IDs and one classification for every node. The raw terminal output is preserved at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D22-terminal-classify-1442/raw-terminal.log` with SHA-256 `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.

## Identity and recipe

- Actual Agent snapshot: commit `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`; never relabelled as comparison base `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`.
- Runtime pin: `3b926efab2eed122d374540baee297d4cdcec62a`; protocol SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`.
- Profile: `agent-remotion-v3-819acf-1110`, lock SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`, archive SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, composition version `0.0.14`.
- Test recipe: isolated `HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1`, Agent plus Runtime3b on `PYTHONPATH`, Node 20.19.4, profile node_modules, `pytest -q -n 3`. Full environment and import identities are in JSON.

## Classification groups

- **child-probe** (17 nodes; unconfirmed_probe_or_child_environment_failure; status: unconfirmed; owner: Agent/runtime child-environment qualification). Evidence: Remotion original_wait_exit_code=1 or child launch failure; one trace reports missing runtime_protocol. Missing fact: child stderr, child environment, and exact import path at process launch.
- **child-import-or-recipe** (97 nodes; environment_recipe_blocker; status: unconfirmed; owner: Full-suite recipe/child environment owner). Evidence: predominant trace is ModuleNotFoundError: runtime_protocol, missing result.json after child failure, or missing profile/binding. Missing fact: node-specific child stderr and the exact effective child environment; terminal summary alone cannot prove a product regression.
- **fixture-declared-gap** (2 nodes; known_fixture_declared_gap_not_d14_or_d23; status: unconfirmed_existing_fixture_gap; owner: Compile-contract fixture/test owner). Evidence: audio_compile_contract.json describes an xfail-like gap, but the test applies no pytest xfail and audio.render_source is None. Missing fact: explicit owner and disposition for this fixture gap; it was not D14 or D23.
- **g5-inverse** (23 nodes; source_backed_existing_owner_failure; status: not_proven_new_regression; owner: G5 physical/native comparison (Agent1434; Runtime handback1439), with R2 inverse guard). Evidence: inverse needs authenticated physical binding normalization or reports ambiguous successors. Missing fact: re-run against the settled base/current source and owner handback to distinguish preexisting behavior from a new regression.
- **profile-fixture** (38 nodes; environment_profile_fixture_mismatch; status: existing_profile_fixture_mismatch_not_product_regression; owner: Composition/profile qualification). Evidence: profile is locked at composition 0.0.14 while backend expects 0.0.13; legacy layer chunk is absent; @banodoco type mappings are unmapped. Missing fact: whether profile lock/archive and these test expectations are meant to be qualified together.
- **child-import** (9 nodes; environment_recipe_blocker; status: unconfirmed; owner: Agent test recipe/isolated-child environment). Evidence: python -I child cannot import astrid under the service recipe. Missing fact: intended isolated-child source binding and whether the test harness must inject it.
- **d13-preflight** (1 nodes; environment_recipe_blocker; status: unconfirmed; owner: D13 preflight environment owner). Evidence: required ASTRID_D13_SOURCE_PROFILE, ASTRID_D13_EXPECTED_BINDINGS, source_checkout, or runtime_environment inputs are absent. Missing fact: authoritative D13 binding values for this full recipe.
- **r1-private** (7 nodes; source_backed_existing_owner_failure; status: not_proven_new_regression; owner: R1 private Agent67ba; Runtime verifier1428; R2 inverse guard). Evidence: forbidden authority/capture keys, expected CommitRejected not raised, or graph expected intervening_write but observed inverse_conflict. Missing fact: owner requalification on the actual 8c355 snapshot with the locked Runtime3b recipe.
- **g5-publisher** (2 nodes; source_test_mismatch_existing_owner; status: not_proven_new_regression; owner: G5 duplicate/publisher owner). Evidence: duplicate archive/history path uses a fake client lacking the required history/archive surface. Missing fact: authoritative duplicate-save contract and whether helper fixture must provide history/archives.
- **g5-schema** (2 nodes; source_test_contract_mismatch_existing_owner; status: not_proven_new_regression; owner: G5/D20 command inventory owner). Evidence: timeline.duplicate is missing from one expected schema and occurrence.place-shared plus timeline.duplicate are extra versus the frozen inventory. Missing fact: authoritative current command/schema inventory for the 8c355 snapshot.
- **r3-docs** (1 nodes; source_docs_mismatch_existing_owner; status: not_proven_new_regression; owner: Agent commit/R3 documentation owner). Evidence: giant-file inventory requires docs/giant-file-rationale.md for the >1200-line commit module. Missing fact: whether the rationale is expected to land for this snapshot before requalification.
- **d09-probe** (3 nodes; unconfirmed_probe_failure; status: unconfirmed; owner: F/D09 environment probe). Evidence: RemotionValidationError during registry_discovery with original_wait_exit_code=1. Missing fact: child/probe stderr and exact child environment are not retained in the terminal artifact.
- **r5-retired-route** (2 nodes; retired_route_contract_mismatch; status: existing_runtime_contract_mismatch; owner: Runtime R5/orchestrator contract). Evidence: publish_parent_composition raises RetiredRouteError from the test helper. Missing fact: authoritative disposition of the stale legacy test (retain, update, or expected-failure).

All classifications are source/evidence-based but deliberately do not claim a new product regression unless proven. The current snapshot differs from the readonly comparison base, and environment/profile/child-process failures prevent adjacent passing tests from clearing any failure.

The four skipped node IDs are unavailable in the retained `-q` output; they are recorded as `count=4, node_ids=null, classification=unknown_missing_terminal_identity`. No xfail/xpass or deselection lines were retained. D14 exact two-equal-text-anchor undo and D23 child-word anchor nodes do not appear in this full log, so neither is marked deferred or passed.

## Dispatch-ready handoffs

1. **G5 physical/native inverse (23 nodes)** — exact node list is in JSON group `g5-inverse`. Command:
   `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider_scalar.py`
   Allowed files: `astrid/sdk/timeline/inverse.py`, `astrid/sdk/timeline/_commit_patch.py`, and focused tests only if the manager authorizes. Needs Agent1434, Runtime handback1439, and the R2 inverse guard owner. This worker did not dispatch it.

2. **R1 private capture/inverse (7 nodes)** — exact node list is in JSON group `r1-private`. Command:
   `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_capture_closure_source.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_commit_graph_roots.py`
   Allowed files: `astrid/sdk/invocation.py`, `astrid/sdk/timeline/_commit_patch.py`, `astrid/sdk/timeline/inverse.py`, and focused tests only if authorized. Needs Agent67ba and Runtime1428. Not dispatched.

3. **G5 duplicate/publisher/schema (4 nodes)** — exact node list is in JSON groups `g5-publisher` and `g5-schema`. Command:
   `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/timeline/test_authoring_media.py`
   Allowed files: duplicate/save/schema/publisher sources only after contract confirmation. Needs G5 current-source authority; no draft merge/deletion assumed. Not dispatched.

4. **R3 documentation (1 node)** — command:
   `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`
   Allowed file: `docs/giant-file-rationale.md` (or the manager-approved rationale source). Verify 58316 versus 8c355 before dispatch. Not dispatched.

The remaining profile, child-probe, D09, D13, compile-gap, and generic recipe groups are not source-fix handoffs from this evidence. They require the missing environment/fixture facts first. D14/D23 are not deferred for this run because neither exact node was exercised.

## Evidence limitations

No test command was invoked by this worker. No full/targeted/public-body service was requested, stopped, retried, or relabelled. Current terminal traces are authoritative; prior 1416 progress and old 4249 inventory are comparison context only.
