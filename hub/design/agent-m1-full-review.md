# Agent M1 merged full-suite review

Status: complete evidence review; **no full-suite or M1 green claim**.
Product source was not changed in this worker. The central run was allowed to
finish once, then its saved log was compared with the classified pre-port
baseline.

## Run identity and exact counts

| run | source/snapshot | exact command | result |
|---|---|---|---|
| pre-port baseline `agent-full-1019191532-6465` | source `a650280634de105641561c3475e37b2e5f77c4ef`; test tree `e475f212efff430149cbc2e6fa834980106aaf13` | `/home/user/work/venv-agent/bin/python -m pytest -q -n 3` | 11,503 passed, 48 failed, 456 skipped, 15 errors, 13 warnings, 563 subtests, 3,433.42s (0:57:13) |
| merged `agent-full-1019193420-11899` | snapshot/tree `3c67145375d72f2507a22cdce54146ed240e45ad`; this is `HEAD^{tree}` for integration `a8eb28af525e13dc12391006b916b5cb1e60d9c4` | `/home/user/work/venv-agent/bin/python -m pytest -q -n 3` | 11,652 passed, 116 failed, 456 skipped, 15 errors, 13 warnings, 563 subtests, 2,392.19s (0:39:52) |

The merged result is 149 more passes but also 68 more failed nodes; the
runtime was 1,041.23s shorter. The current source delta from baseline is the
49-file Agent M1/Viewing integration change, `+6,784/-105` lines. No duplicate
full run, install, browser, socket, or focused-suite rerun was used for this
comparison.

## Complete node-set comparison

The saved logs were parsed by exact lines beginning `FAILED ` or `ERROR ` and
compared as node-ID sets:

| set | nodes |
|---|---:|
| old non-passing (`48 failed + 15 errors`) | 63 |
| current non-passing (`116 failed + 15 errors`) | 131 |
| resolved | 0 |
| still failing/erroring | 63 |
| added failures | 68 |

All 63 old node IDs are still present. The literal old IDs and their original
classification are the ones enumerated in `design/agent-baseline.md`; the
grouping below is a complete partition of those 63 nodes, not a rerun or an
assumption that the baseline counts were unchanged.

### Added failures — all 68

| exact node family | count | observed traceback/evidence | classification |
|---|---:|---|---|
| `tests/core/execution/test_generic_host_child_bridge_d18.py::test_discovery_acquisition_production_cap_and_error_identity` with `slack ∈ {-1,0,5}`, `chunk ∈ {1,7,65536}`, `head ∈ {{}, {Content-Length:0}, {Content-Length:999999999}}`, `http_error ∈ {False,True}` | 54 | `ValueError: refusing to send a runtime credential to non-loopback host 'runtime'` at `astrid_runtime_client/generated.py:_require_loopback`, before the fixture's monkeypatched `urllib.request.urlopen` | M1 client/fixture contract break; not a proven live product defect because `http://runtime` is outside the settled local-loopback policy |
| `...::test_discovery_acquisition_truncated_json_is_terminal_before_error_decode` with body `{"code":"private-prefix"`, `{"message":"\xc3`, `[]` and `http_error ∈ {False,True}` | 6 | same non-loopback rejection before truncated-body handling | same classification; live loopback/error-decoding behavior unverified |
| `...::test_discovery_acquisition_remaining_budget_error_shared_client_and_binary_isolation` | 1 | same non-loopback rejection before the budget assertion | same classification |
| `tests/packs/rendering/test_timeline_visualize_motion_views.py::test_visualize_prints_page_counts_timing_and_next_commands` | 1 | `lines[1]` is now `revision unavailable`, while the fixture supplies pages/timing but no revision snapshot or inspection | M1 provenance-output fixture drift; the new revision label is intentional, so no real-label defect is proved |
| `tests/sdk/test_timeline_cuts.py::test_show_prints_the_cut_table_by_default` | 1 | `error protocol_error: immutable timeline read omitted its revision identity` | M1 immutable-readback fixture drift; the fixture has envelope `revision_id` only, while the new code accepts proof only from `bundle.base_parent.revision_id` |
| `tests/sdk/test_timeline_cuts.py::test_show_unknown_shot_lists_the_shots` | 1 | same readback identity error | same classification |
| `tests/sdk/test_timeline_cuts.py::test_show_as_script_and_diff_as_code` | 1 | same readback identity error | same classification |
| `tests/test_artifact_manifest.py::test_cli_surface_is_current` | 1 | `gen_cli_surface.check()` returns `['timelines undo: changed']` | **M1 integration regression:** `cli.py` added publication undo surface but `cli-surface.json` was not regenerated |
| `tests/test_artifact_manifest.py::test_planted_cli_surface_drift_is_named` | 1 | expected only `timelines show: changed`, received that plus `timelines undo: changed` | same stale generated-artifact regression, not an independent product failure |
| `tests/test_generic_host.py::test_vendored_runtime_client_timeout_is_bounded_and_request_correlated` | 1 | `captured` has no `timeout` because the new `_urlopen_loopback` calls `build_opener().open`, bypassing the old `urllib.request.urlopen` monkeypatch | M1 transport test-seam compatibility break; source passes `self.timeout` to `opener.open`, so live timeout/request-ID behavior is unverified rather than disproved |

The bridge family count is 54 + 6 + 1 = 61; the remaining seven rows total
68. These are the only added node IDs in the merged summary.

### Still failing — all 63 baseline nodes

| baseline classification | exact current family | count | current evidence |
|---|---|---:|---|
| external VibeComfy fixture/setup | `tests/packs/runpod/test_worker_staging.py` (all 15 baseline nodes) | 15 errors | module fixture still raises `FileNotFoundError` for `/home/vibecomfy/vibecomfy` |
| uninstalled-source child probe | `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[...]` for the seven baseline parameters | 7 | child `python -I -c` still cannot import `astrid` from the dependency-only environment |
| Runtime checkout/package exposure | `tests/packs/runpod/test_worker_preparation.py::test_runtime_activation_checkpoints_restore_only_the_exact_process` | 1 | `runtime_protocol.remote_worker_activation` remains unavailable in the full-suite environment |
| xdist/execnet reporting/toolchain | `tests/packs/test_vibecomfy_metadata.py::VibeComfyStructuredMetadataTest::test_run_rejects_missing_or_empty_engine_inventory` | 1 | xdist still cannot serialize the parameter `PosixPath` (`execnet.gateway_base.DumpError`) |
| pre-existing RunPod/main path drift | `tests/packs/runpod/test_ensure_storage.py` (2) and `tests/packs/runpod/test_pack_executors.py` (30), plus `tests/packs/runpod/test_provision_ports.py` (2) | 34 | same missing `astrid.packs.runpod.executors[...]` path/shape mismatch as baseline; no changed source in the M1 delta |
| pre-existing test-code import issue | `tests/packs/runpod/test_worker_process.py::test_stop_pins_process_and_never_signals_after_identity_drift`, `::test_stop_requires_pinned_exit_proof_before_stopped_receipt[True]`, `[False]` | 3 | `signal` remains omitted by the test while the product module imports it |
| pre-existing generic-host contract mismatch | `tests/test_generic_host.py::test_failed_worker_release_retains_original` | 1 | unchanged cleanup path still raises `CommandCleanupUnresolved` instead of the test's `CleanupUncertainError` |
| structure gate | `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale` | 1 | node persists, but its cause changed to the M1-induced missing rationale for `astrid/sdk/workspace_client.py`; see below |

The eight rows total 63. There were no resolved baseline nodes. The current
RunPod, VibeComfy, H3, Runtime-import, xdist, worker-process, and generic-host
release tracebacks preserve the baseline classifications. The structure node
is the one exception: it is still a non-passing old node, but its current
failure is M1-caused rather than the baseline's inherited generic-host line
count mismatch.

## M1 source inspection and manager action

The exact source comparison was `git diff
e475f212efff430149cbc2e6fa834980106aaf13..3c67145375d72f2507a22cdce54146ed240e45ad`.
Relevant findings:

* `astrid/packs/timeline/cli.py` adds publication undo options and changes the
  generated CLI surface, but `cli-surface.json` is unchanged. This is an
  actual M1 integration/delivery regression and was appended to
  `design/m1-agent-coordination.md` for the manager.
* `astrid/sdk/workspace_client.py` is 1,191 lines at the baseline and 1,243
  lines in the merged tree. The structure contract correctly detects that the
  new >1,200-line file has no `docs/giant-file-rationale.md` entry. This is an
  actual M1 documentation/structure-gate regression and was appended to
  `design/m1-agent-coordination.md`.
* `astrid_runtime_client/generated.py` adds `_require_loopback` and routes
  requests through a proxy-free opener. The bridge fixtures' `http://runtime`
  alias and the timeout test's `urlopen` monkeypatch no longer reach their
  intended assertions. This is a concrete M1 compatibility break in the full
  suite, but the saved full run does not distinguish a stale test seam from a
  live supported-loopback defect; it remains explicitly unverified.
* `astrid/packs/timeline/cli_visualize.py` now emits provenance/revision lines,
  and `astrid/packs/timeline/cli_show.py` rejects an immutable read unless the
  loaded bundle proves `base_parent.revision_id`. Those changes match the
  settled readback/provenance contract; the added failures use old fixtures
  that do not supply the required proof. Do not weaken the contract or rewrite
  the expectations to accept an unpinned read.

No newly non-passing node came from the M1 registry/provider/outbox,
editing-conformance, commit-runtime, sync, or workspace-client M1 test files.
That observation is only a failure-set fact; it is not evidence that M1's
seven gates are green. Browser, live socket, renderer-off, and full-suite
claims beyond this central run remain unverified.

## Reproduction and evidence boundary

Reproduce the merged full run from the central Agent worktree with:

```bash
cd /home/user/work/agent
/home/user/work/venv-agent/bin/python -m pytest -q -n 3
```

The saved authoritative artifacts are
`tests/agent-full-1019193420-11899/log.txt`, `status`, `summary`, `snap`, and
`exit` under the ORCH directory. This review used those artifacts and the
baseline artifacts only; no tests were rerun, no fixtures were relaxed, and no
expected failures or suppressions were added.

## Manager review — 2026-10-19T20:57Z
Exact added node set68 and persisting63 independently reproduced. More than one cause can hide behind an old failing node: current structure failure newly lacks workspace_client.py entry1243 (baseline1191). Independent audit also finds M1cli.py3993→4045 (+52) beyond±50 drift. agt-m1-structure-metadata handles ONLY these2owned inventory entries with honest decomposition seam, no threshold/skip/baseline changes. Inherited count drift generic_host.py13598→13798, remotion/run.py2158→1868, host_bootstrap.py1601→1717 are ALL identical baseline→current source and deliberately untouched; gate staysRED. No product refactor during App tuple freeze. Other followups: read-fixtures branch3cut/showfixtures+normal CLI/artifact generators; client-fixtures62cases under explicitorchestrator/Runtimegrant after productionloopback audit; Viewingowns1summaryfixture. All68mustbe proven fixed or inheritedbeforeM1exit; this doc alone does notclose them.

## Reviewed corrections ready, integration held — 2026-10-19T21:19Z
All68addedfailure nodes now have passing corrections, preserving required assertions and production safety.62clientnodes:30d7c56b, local62pass, central2files445pass401skip2deselected+1unchangedinheritedcleanupfailure/203.31s.3show+2CLIartifactnodes:990914e9 cumulative descendant7a68b7ed/bcd851c2, worker40pass and manager40pass on byte-identicalCLI/show changes.1summarynode:990914e9, wholefile31pass2oldoptional-element-maths skips, managerexactnode1pass0.63s; real committedR1 label explicitlybeforetiming, alloldassertionskept.
M1-owned workspaceclient/CLI inventory metadata is documented honestly in1361af92; inherited generic_host/remotionrun/hostbootstrap drift remains red. Package consumer's10boundsource hashes plusCLIhash refreshed bynormalgenerator inbcd851c2 (ancestor990914e9), patterns/negative testsunchanged. Allbranches reviewed/HELD because App requiresfrozenintegrationa8eb28af. Noneofthese corrections is integratedyet; no secondfull or full-greenclaim. Preferred merges afterrelease:990914e9 package+metadata/readfixtures/summary,30d7c56b clienttests,1361af92 owninventory. Original319 andbcd standalone merge superseded.
