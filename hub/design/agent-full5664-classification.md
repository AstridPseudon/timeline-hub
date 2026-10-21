# Agent full c13 5c5173dc classification

Date: 2026-10-21 UTC

## Exact run

Classified the existing run only: `agent-full-c13-5c5173dc-integration-1021001510-5664`.

- Agent commit: `5c5173dcb57669a9d43e5add2674543333f1c6d2`; tree:
  `8626f868a3869b23baaca9814adb930e8952e4c7`.
- Runtime: immutable commit `9d1c43c647301da48a6e86ad82e466b501bd2418`,
  tree `50e74e3243c5da4cf77b6e6cc76605fae8aeb649`, checkout
  `/home/user/work/wt/rt-pin-9d1c43c6`.
- Installed child profile: `/home/user/work/venv-agent-child-c13-5c5173dc`.
- Remotion: `/home/user/work/runtimes/agent-remotion-0013`, public Composition
  `0.0.13`, Node `v20.19.4`.
- Full command was the preflight-registered command: `env -i ...
  /home/user/work/venv-agent-child-c13-5c5173dc/bin/python -m pytest -q -n 3`
  with the exact paths recorded in
  `agent-current5c-full-preflight.md`.

## Result

**6 failed, 14,884 passed, 452 skipped, 4 xfailed, 84 warnings, 565 subtests
passed; exit 1; 3,879.05s (1:04:39).** No collection errors and no error nodes.

There were no setup-only failures in this run. The six failed nodes are:

| Exact node | Classification | Evidence and smallest next repair unit |
|---|---|---|
| `tests/core/rendering/test_production_callers.py::test_no_production_backend_imports_outside_allowlist` | **New source/product topology regression** | The new `2b020eaef` Scene work adds three direct concrete-Remotion imports outside the gate allowlist: two in `astrid/core/timeline/scene_answers.py` (`lock`, `_prepared_remotion_root`) and one in `astrid/packs/rendering/actions/timeline_visualize/scene_only.py` (`run`). This is not setup: the gate found exactly those three violations. Smallest unit: route the prepared Scene operations and composition-id lookup through an approved neutral Remotion-runtime seam, or explicitly document/add these two legitimate owners to the allowlist if that is the settled architecture; rerun this gate. |
| `tests/packs/test_composition_elements.py::CompositionElementTest::test_bundled_element_registries_generate_together` | **Assertion conflict exposed by an intended product repair** | `52437515d` correctly retains the public Composition-owned `text-card` in generated `EFFECT_IDS` and resolves it through `PUBLIC_EFFECT_REGISTRY`. This older test still asserts that `"'text-card'"` is absent, so it conflicts with the repaired public-registry requirement. It is not an environment failure and is not evidence that `52437515d` is wrong. Smallest unit: align this test's expectation with the public-owned registry contract while retaining the no-retired-import assertion; no assertion was changed here. |
| `tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_occurrence_move_keeps_legacy_owner_resolution` | **New source/product regression** | `b1013c0ad` broadened `astrid/packs/timeline/cli_native.py::commit_move` from parent-only selectors to every selector. With this test's non-translation occurrence bundle, native `clip.move` now refuses (`clip.move v1 requires a translation-only occurrence map`) instead of returning `NotImplemented` and preserving legacy owner resolution; `_edit_checkout` is never reached. Smallest unit: keep native dispatch for supported translation-only occurrence maps but return to the legacy owner-resolution path for unsupported occurrence maps; rerun this node and the rational explicit-occurrence native lanes. |
| `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current` | **Old 4555 debt reintroduced by a merge** | The exact check returns the same ten stale entries: `astrid/packs/rendering/elements/catalog.ts: changed` plus nine retired wrapper component paths marked `removed`. The correct refresh landed as `b3c2f8515`, but merge `1acfa42dc` restored the stale parent `artifacts.json` (catalog hash `1018...`, old component entries), so this is not a name-only baseline relabel. Smallest unit: regenerate the manifest on the final merged tree with the prescribed `python scripts/gen_cli_surface.py && python scripts/artifact_manifest.py`, then rerun this node. |
| `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale` | **New documentation/source drift** | The old `astrid/sdk/remote.py` mismatch was repaired by `00d84bc4d` (rationale now records 2,655). The current exact failure is different: `astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py` is 2,072 lines while the rationale claims 2,015, a 57-line drift beyond the 50-line tolerance. Smallest unit: refresh the rationale entry after the final source tree is settled; rerun this node. |
| `tests/timeline/test_timeline_kernel_kinds.py::DoctorV10ChecksTest::test_public_doctor_route_fails_closed_without_runtime` | **New Agent–Runtime output-contract regression** | Under the exact pinned Runtime9d1c43 environment, `collect_diagnostic()` supplies `observed.data` without an `ok` key, and current Agent `dispatch._dispatch_doctor` only defaults `effects` and `authorization_required`; the test therefore raises `KeyError: 'ok'` after receiving a valid failure report. The old a8 run used a different mutable Runtime and did not expose this exact contract mismatch. A known Agent-side repair candidate, `f6d3e9346` (`Preserve doctor JSON outcome fields for unavailable Runtime`), adds the missing `ok`/`problem_code` normalization but is not in current 5c. Smallest unit: port that normalization (or equivalent) in Agent and rerun this node against Runtime9d1c43. |

## Old 19-node mapping

The 4555 run had 19 failures: 3 backend fixture nodes, 11 layer-tail
compatibility nodes, TextCard SSR, the Scene-host `end` boundary, artifact
manifest, giant-file inventory, and public-owned effects registry.

- The 3 backend fixture nodes, all 11 layer-tail nodes, and TextCard SSR (15
  nodes total) were repaired by `26842a4dc`; its bounded targeted evidence was
  15 passed. None of those old nodes failed in this exact 5c run.
- The old Scene-host `end` boundary and effects-registry omission were repaired
  by `52437515d`. The old effects node is no longer failing; the current
  `test_bundled_element_registries_generate_together` failure is the opposite
  stale assertion exposed by retaining `text-card`.
- The old artifact repair landed as `b3c2f8515`, but `1acfa42dc` reintroduced
  the stale manifest during a later merge. The current artifact node is the
  one old cause genuinely reappearing.
- The old `remote.py` rationale mismatch was repaired by `00d84bc4d`; the
  current structure node is a different file and different 57-line drift.

Thus the final six are: two new product/source regressions, one assertion
conflict caused by an intended repair, one reintroduced generated-artifact
debt, one new rationale drift, and one new Agent–Runtime output-contract
regression. No full rerun, test edit, assertion weakening, product edit, or
shared-dependency mutation was performed by this worker.

## Recommended repair order

1. Reapply the final-tree artifact manifest refresh and the small doctor
   output normalization; these are isolated and have exact existing repair
   precedents.
2. Repair occurrence-move fallback and rerun its exact node plus rational
   occurrence lanes.
3. Resolve the Scene import topology through the approved seam/allowlist and
   rerun the production-caller gate.
4. Align the Composition registry test with the settled public-owned behavior,
   then refresh the giant-file rationale and rerun both contract nodes.
