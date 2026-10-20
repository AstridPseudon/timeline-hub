# Agent baseline recheck (109 nodes) on integration

Worker: agt-baseline-recheck (read-only; no repo changes; no commit-msg; no full* suite requested).
Tree: Agent `tl/integration` at `931d7ec5` (service label: agent tree `83462e3f…`, clean worktree). Fix groups A, B, C, D, E, F, I, K, L landed via `86d7cf9b` (fix-a-d), `7261b4ad` (fix-e), `4e40f5c4` (fix-rest), plus `e088ba2d` and `35a9899f`.
Node set: the 109 FAILED/ERROR ids from `tests/agent-full-remotion-integration-1020031037-28578/log.txt` (79 F + 30 E), extracted verbatim. One extra node was appended to every run: `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` (the false-regression candidate).

## Runs

Each was `request-test integration:agent <suite> --files "<109 ids> <TextCard id>"`.

| suite | runtime (`ASTRID_REMOTION_PROJECT_DIR`) | result dir | outcome | wall time |
|---|---|---|---|---|
| `remotion-env-nodes` | `runtimes/agent-remotion` = @banodoco/timeline-composition **0.0.8** | `agent-remotion-env-nodes-1020085216-11342` | 26 failed, 68 passed, 15 errors | 287s |
| `remotion-0010-nodes` | `runtimes/agent-remotion-0010` = **0.0.10** | `agent-remotion-0010-nodes-1020085218-18001` | 12 failed, 82 passed, 15 errors | 470s |
| `remotion-0012-nodes` | `runtimes/agent-remotion-0012` = **0.0.12** | `agent-remotion-0012-nodes-1020085219-15793` | 26 failed, 68 passed, 15 errors | 267s |
| single-node rerun, `remotion-0010-nodes --no-cache` | 0.0.10 | `agent-remotion-0010-nodes-1020090257-27970` | the 120-400 budget node: **1 passed** | 34s |

Every run executed 109 items, not 110: the admission-recovery file is deselected (see L). Counts are pytest's own summary lines. `remotion-env-nodes` and `remotion-0012-nodes` have identical counts; the 0.0.12 failure reason was checked at four sites.

## Why 0.0.10 is the right env (the key finding)

- The product pins its expected composition version: `astrid/core/rendering/remotion_runtime.py:48` `_COMPOSITION_PACKAGE_VERSION = "0.0.10"`. On 0.0.8 and 0.0.12 the bootstrap nodes stop at `RemotionValidationError: installed Remotion package manifest has unexpected version: '0.0.8' (or '0.0.12'); expected 0.0.10` (15 sites in the 0.0.8 log, same message in the 0.0.12 log).
- The snapshot pins `remotion/package.json:18` `file:artifacts/banodoco-timeline-composition-0.0.10.tgz`.
- The TextCard node asserts that the selected runtime's `package.json` equals the snapshot's (`tests/packs/rendering/test_remotion_render_contract.py:95`). It fails on 0.0.8 (`…disagrees with snapshot package.json`) and on 0.0.12 (0.0.12 pin), and **passes on 0.0.10**. So the TextCard node is a false regression only under the 0.0.8 env.
- Consequence: the 109 baseline was measured on 0.0.8 (`full-remotion-integration` line 43 of `suites.conf` uses `agent-remotion`), so about 40 of its reds were the wrong runtime, not the product. Group A's pycache failure is gone (no `PYTHONPYCACHEPREFIX` error appears in any run); on 0.0.8 the same nodes now reach the version gate instead.

## Per-group: before (109 baseline, 0.0.8) → after

Red counts per group. "pass" means the node is not in the FAILED/ERROR summary.

| Grp | Nodes | Before (baseline, 0.0.8) | After 0.0.8 (`remotion-env-nodes`) | After 0.0.10 (`remotion-0010-nodes`) | After 0.0.12 (`remotion-0012-nodes`) | Status now |
|---|---:|---|---|---|---|---|
| A | 27 | 27 red | 13 red: 12 bootstrap nodes hit the version gate, the 120-400 node hits the registry fence (flake); 14 host-recovery nodes pass | 0 red after rerun (1 red in the full run: the 120-400 budget node, flaky, see below); 26 pass | 13 red (version gate) | **DONE** (on 0.0.10) |
| B | 4 | 4 red | 0 | 0 | 0 | **DONE** |
| C | 3 | 3 red | 3 red (version gate, masks C) | 2 red: `assert 2 == 1` on inventory reads; `pack_root` error gone; 1 pass | 3 red (version gate) | **DECIDE** (2 nodes, see below) |
| D | 11 | 11 red | 0 | 0 | 0 | **DONE** |
| E | 34 | 34 red | 0 | 0 | 0 | **DONE** (the runpod-lifecycle prerequisite in the cutlist is not blocking any run) |
| F | 3 | 3 red | 0 | 0 | 0 | **DONE** |
| G | 1 | 1 red | 1 red | 1 red | 1 red | **ENV** (provisional → strongly supported, not run-confirmed) |
| H | 7 | 7 red | 7 red | 7 red | 7 red | **ENV** (confirmed in logs) |
| I | 1 | 1 red | 0 | 0 | 0 | **DONE** |
| J | 1 | 1 red | 1 red | 1 red | 1 red | **DECIDE**, recommend FIX test |
| K | 1 | 1 red | 0 | 0 | 0 | **DONE** |
| L | 1 | 1 ERROR (collection) | not executed (deselected) | not executed | not executed | **UNVERIFIED** (import fixed; tests never run in named suites) |
| M | 15 | 15 ERROR | 15 ERROR | 15 ERROR | 15 ERROR | **ENV** (confirmed in logs) |
| **Total** | **109** | **109 red** | **40 red, 68 pass, 1 not run** | **27 red, 81 pass, 1 not run** (26 red after rerun) | **40 red, 68 pass, 1 not run** | |
| TextCard (extra) | 1 | red | **red** (snapshot mismatch) | **pass** | **red** (snapshot mismatch) | the false regression goes away on 0.0.10 |

No new reds outside the 109 set in any env. The TextCard node is the only out-of-set node, and it is green only on 0.0.10.

## Remaining reds (0.0.10, the recommended env)

| # | Node(s) | Cause (evidence) | Class | Owner | Recommendation |
|---|---|---|---|---|---|
| 1 | G: `tests/packs/runpod/test_worker_process.py::test_linux_owned_host_survives_launcher_and_exact_stop` | The launcher starts `sys.executable worker_process.py --owned-host` with `stderr=DEVNULL` (`astrid/packs/runpod/worker_process.py:529-534`). That file imports `astrid` at module top (line 42). `venv-agent` has no `astrid` (no dist-info, no `.pth`), and the env-i recipe sets no `PYTHONPATH`. The parent then raises `WorkerOwnerConflict: host did not acquire physical pod ownership` (`worker_process.py:549`; seen in the 0.0.10 log at line 1165). | ENV | Env owner | Make `astrid` importable for the supported venv (editable install), the same decision as H. Test-side alternative: `monkeypatch.setenv("PYTHONPATH", <repo root>)` in the test. **Not run-confirmed**: I could not run pytest locally (approval needed), and no suite sets `PYTHONPATH`. |
| 2 | H: 7 × `tests/packs/h3_av/test_character_swap_cpu_boundary.py::…real_installed_guard[…]` | Child runs `sys.executable -I -c "import astrid"` → `ModuleNotFoundError: No module named 'astrid'` (7/7, every env). | ENV | Env owner (or agent: test-owned installed overlay) | Install `astrid` into the supported venv, or build a throwaway overlay in the test. Do not delete the child check. |
| 3 | M: 15 × `tests/packs/runpod/test_worker_staging.py` (ERROR) | `source_fixture` needs a VibeComfy checkout at `/home/vibecomfy/vibecomfy`; `FileNotFoundError` in all 15 (0.0.10 log lines 76-1084). No such checkout exists. | ENV | Env owner (provision the checkout) or agent (explicit override env var, test-side) | Either provision the checkout or add an explicit path override. Do not skip the fixture. |
| 4 | J: `tests/test_generic_host.py::test_failed_worker_release_retains_original` | Test expects `CleanupUncertainError` from `invoke_capability` (line 4268-4269). Product raises `CommandCleanupUnresolved(HostError)` with `from exc` (`generic_host.py:8387-8393`, the `except BaseException` branch at 8388). The chain in the log is `CleanupUncertainError` (direct cause) → `CommandCleanupUnresolved: capability 'test.echo' cleanup unresolved: retained worker release failure`. The retention assertion at line 4270 still holds: `_latch_cleanup_uncertainty` (line 5444-5452) appends the note to `_unresolved_task_scopes`, and the process stays in `_active_processes` because `_untrack_process` is not reached. | DECIDE → recommend **FIX (test)** | Agent | See the J recommendation below. |
| 5 | C: 2 × `tests/sdk/test_host_bootstrap_source_identity.py`: `test_bootstrap_passes_inventory_identity_and_restarts_on_change`, `test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter` (both `assert len(inventory_calls) == 1` → `2 == 1`, line 219) | The `pack_root` fake fix works (the records now carry `pack_root`). The second read is deliberate: `remotion_runtime.py:606` calls `active_source_inventory(verify=True)` inside the Remotion probe, and `host_bootstrap.py:1355` reads it once more. The extra read happens only when the Remotion env is set. Under 0.0.8 these nodes stop earlier at the version gate, so they mask this. | DECIDE → recommend **FIX (test)** | Agent | Replace the exact-count assertion with "at least one read, and every read returns the identity the launch records" (keeps the TOCTOU intent). If the owner wants one read, that is a product change: the probe reuses the bootstrap's inventory. The probe's own `verify=True` argues against that. |
| 6 | A (flaky): `test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400]` | Failed in the full 0.0.10 run with `RemotionValidationError: registry corpus changed during owned discovery` (`remotion_runtime.py:680`, mtime fence). The same message appears in the 0.0.8 log (line 4202, in this case's block). **Passes alone** on 0.0.10 (rerun `…-27970`, 34s). | FLAKY (fence trips under concurrent suites) | Agent (investigate; do not loosen the fence) | Not a baseline fix. If it recurs in a solo full run, open it separately. Likely cause: concurrent suites sharing the runtime checkout. Unproven. |
| 7 | L: `tests/sdk/test_admission_recovery.py` | The collection ERROR is gone (the module now imports; no ERROR line in any log). But the file is `pytestmark = pytest.mark.integration` (line 18), and `pyproject.toml:264` `addopts` deselects `integration`. So the named suites run 0 items from it, which accounts for the 109-vs-110 count. | UNVERIFIED | Orchestrator (add a suite) + agent | Add an `-m integration` suite for this one file, e.g. `agent admission-recovery-integration env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime … -m integration tests/sdk/test_admission_recovery.py`. I did not request one (suites.conf is orchestrator-owned). |

### J: recommendation (FIX the test; keep the product)

- The wrapper is intentional and load-bearing. `CommandCleanupUnresolved` carries `execution_error` and `from exc`, and the task-level path catches it explicitly (`generic_host.py:9814-9815`, `command_cleanup_error = exc`). Raising the raw `CleanupUncertainError` would break that consumer.
- The test's intent (cleanup failure propagates with its message, the process and scope stay retained) still holds under the wrapper. Only the exception type in `pytest.raises` is stale.
- Suggested change at `tests/test_generic_host.py:4268`: expect `CommandCleanupUnresolved` with the same `match=`, then assert `isinstance(info.value.__cause__, CleanupUncertainError)`. Keep lines 4270's retention assertions unchanged.
- This changes an expectation, not a removed behaviour. The orchestrator rule (never weaken a passing behaviour test) does not apply, since the node is failing now. Flag it in the commit anyway.

## Recommended env for the default Agent Remotion suites: **0.0.10** (`agent-remotion-0010`)

Reasons (all verified above):
1. It is the only env the product accepts: `_COMPOSITION_PACKAGE_VERSION = "0.0.10"` (`remotion_runtime.py:48`). 0.0.8 and 0.0.12 fail the version gate for about 40 nodes.
2. It matches the snapshot pin (`remotion/package.json:18`). The TextCard visible-markup node compares the runtime's `package.json` to the snapshot, so it is green only here.
3. 0.0.12 would need the Agent pin (`remotion/package.json:18`) and `_COMPOSITION_PACKAGE_VERSION` bumped together. That is a product/pin decision for the owner, not a test change. Do not repoint to 0.0.12 without it.

Action for the orchestrator (suites.conf is orchestrator-owned; I did not edit it): repoint `full-remotion-integration` (line 43), `consumer-regressions-integration` (line 31, which contains the TextCard node) and `real-pack-host-integration` (line 38) from `runtimes/agent-remotion` to `runtimes/agent-remotion-0010`. The plain `agent full` suite (line 6) sets no Remotion env at all; I did not test it (full* is off-limits to me).

## Cutlist update (what changed since 109)

- Fixed and verified in the 0.0.10 run: A (host-recovery 14, bootstrap 12 of 13), B, D, E, F, I, K. Verified by pytest summary, not by reading.
- Still red, all on 0.0.10: G (1), H (7), M (15) = **23 ENV**; J (1) + C count (2) = **3 DECIDE/FIX (agent)**; the A flake (1) = **FLAKY**; L = **UNVERIFIED** (not executed in any named suite).
- The cutlist's G "provisional" is now supported by code (`worker_process.py:42`, no `astrid` in venv-agent) but still not run-confirmed.

## Unverified / limits

- No local pytest run: direct approval was denied for `env -i … pytest`, so every result here comes from the test service.
- G's env cause is from code and environment facts, not a run with `PYTHONPATH` set.
- L's fix is verified only at import level (no ERROR line); its tests never ran.
- The 120-400 flake: one failure in one full run (plus a fence message in the 0.0.8 run), one pass alone. Not enough to call it deterministic or to call it fixed.
- The count assertions (C) on 0.0.10 are read from the log. The fix suggestion is untested.
