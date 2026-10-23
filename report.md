# F-D22 child runtime/source-admission diagnosis

## Disposition

No production, test-body, fixture, pin, dependency, or testservice recipe change is justified by the available evidence. The current failure is a child-process admission/environment problem. The smallest supported next step is an authenticated installed Agent/Runtime pair matching the failed full run, followed by bounded original-node validation. I did not retry the full suite.

## Full-run identity and evidence

The failed service result is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679/`

It ran Agent snapshot `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`, with Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, and reported `185 failed, 16733 passed, 4 skipped, 19 errors`. The Runtime protocol source hash was `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`.

The raw terminal log and classifier are retained at:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D22-terminal-classify-1442/raw-terminal.log` (SHA256 `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`)
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-F-D22-terminal-classify-1442-e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5.json`

The classifier groups were child-probe 17, child-import-or-recipe 97, child-import 9, d09-probe 3, and d13-preflight 1. The retained current-run probe stderr contains `ModuleNotFoundError: No module named 'runtime_protocol'`; the raw terminal has 68 such fingerprints and 9 `ModuleNotFoundError: No module named 'astrid'` fingerprints. The child-probe group itself remains unconfirmed where the original child stderr was not retained.

## Source-backed cause

`astrid/core/execution/generic_host.py` builds source-mode child environments through `build_child_subprocess_env` and `_command_worker_pythonpath`. The source-mode dependency path helper only retains `site-packages`/`dist-packages` entries. The Runtime3b checkout at `/home/user/work/wt/rt-pin-3b926efa` is therefore available to the full parent through its explicit `PYTHONPATH`, but is not admitted as a source child import root.

The representative `child-import-or-recipe` test also constructs its child environment with `dict(os.environ, PYTHONPATH=source_root:tmp_path)`, replacing the parent overlay. Consequently, adding installed site-packages to the test-service row does not repair this original body; the child needs Runtime installed in its interpreter environment.

The `child-import` representative confirms the other side of the boundary: the current `venv-agent` has no installed Agent package, so a direct `python -I` probe fails with `ModuleNotFoundError: No module named 'astrid'`. An authentic installed interpreter is required for isolated children.

## Bounded representative probes

### Source-mode child-import-or-recipe

Original node:

`tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]`

Command shape (all environment values are retained in the wrapper report):

```sh
env -i HOME=/tmp/agt-F-D22-child-env-1454-home LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PATH=/usr/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH=/home/user/work/wt/agt-F-D22-child-env-1454:/home/user/work/wt/rt-pin-3b926efa:/home/user/work/venv-agent-child-f1012-installed/venv/lib/python3.13/site-packages \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-f1012-installed/venv/lib/python3.13/site-packages \
  /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider \
  tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]
```

Result: exit 1. The child failed with `ModuleNotFoundError: No module named 'runtime_protocol'` after the test body replaced `PYTHONPATH`. Captured stdout is `/tmp/agt-F-D22-child-env-1454/child-import-representative.stdout.log` (SHA256 `10726e37e06f148d35cdd41352346bdfa931fc26be2548f636a779a2617cb340`); captured stderr is `/tmp/agt-F-D22-child-env-1454/child-import-representative.stderr.log` (SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

### Installed isolated-child reference

Original node:

`tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]`

It was run with the existing F1012 installed environment and no `PYTHONNOUSERSITE`, using `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -P -m pytest`. The `python -I -B` child import probe returned 0 and the pytest node returned 0. Captured stdout is `/tmp/agt-F-D22-child-env-1454/child-import-isolated-reference.stdout.log` (SHA256 `c29966ed8ce7f13239fdbbc2025365baed757f71eb8ad5c1296066f1dec50d6b`); stderr is empty (SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

This is only a mechanism reference, not current-run qualification: F1012 contains Agent `ef851b22c506245441b9a630c093b3460e39cbdc`, while the failed full run contains Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`.

The prior successful bf40 D09 run used the same installed-environment route and omitted `PYTHONNOUSERSITE`; the installed F1012 preflight also showed the correct import/profile shape. Its D09 safety failure when `PYTHONNOUSERSITE=1` was supplied is why that variable is not part of the reference invocation.

## Required dispatcher action

Do not repair this by changing the row `PYTHONPATH`, weakening `-I`, or editing the original bodies. Request an immutable installed environment matching the failed pair:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-child-venv \
  venv-agent-child-d22-8c3b926e \
  8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe \
  full-current-v3-1229 \
  /home/user/work/wt/rt-pin-3b926efa
```

After that request completes, run at most one bounded original node per independently distinct child cause (up to four), with report-all argv/env/python-`-I` import origins, source/profile hashes, and retained stderr. Do not retry the full suite until those nodes qualify. No such matching pair was available locally, so I did not dispatch or run that follow-up.

## Changes and verification

No tracked source, test body, fixture, pin, dependency, or harness file was changed; the only worktree change is this untracked `report.md`. No full suite was retried and no central test-service request was submitted.
