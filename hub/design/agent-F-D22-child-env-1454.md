# F-D22 child-env handoff

Disposition: no supported harness correction is proven on the available environments. Do not edit production code, test bodies, fixtures, pins, dependencies, or weaken `-I`/guards. The failed full result is terminal for this task; no full retry was made.

## Exact source-backed result

Failed full service:

- Agent snapshot `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`
- Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, protocol SHA256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`
- Result: `185 failed, 16733 passed, 4 skipped, 19 errors`
- Classifier groups: child-probe 17, child-import-or-recipe 97, child-import 9, d09-probe 3, d13-preflight 1
- Raw terminal SHA256: `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`

Current retained child stderr shows `ModuleNotFoundError: No module named 'runtime_protocol'`; the raw terminal contains 68 such fingerprints and 9 `ModuleNotFoundError: No module named 'astrid'` fingerprints. The source path in `astrid/core/execution/generic_host.py` admits source-mode dependency roots only when their basenames are `site-packages`/`dist-packages`; the Runtime3b checkout is therefore available to the parent but not to a source child. The representative original child body then overwrites `PYTHONPATH`, so adding site-packages to the test-service row cannot fix it.

## Bounded probes

1. `tests/core/execution/test_generic_host_actions_v3.py::test_private_child_command_preserves_entrypoint_and_original_bridge[-c]`
   - Run with current worktree, Runtime3b, and F1012 site-packages in the parent `PYTHONPATH`; `/home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider ...`.
   - Exit 1: child `ModuleNotFoundError: runtime_protocol` after original body replaced `PYTHONPATH`.
   - stdout SHA256 `10726e37e06f148d35cdd41352346bdfa931fc26be2548f636a779a2617cb340`; stderr SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

2. `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]`
   - Run with existing installed F1012 venv, no `PYTHONNOUSERSITE`.
   - `python -I -B` import probe exit 0; pytest exit 0.
   - stdout SHA256 `c29966ed8ce7f13239fdbbc2025365baed757f71eb8ad5c1296066f1dec50d6b`; stderr empty SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
   - This is mechanism-only: F1012 Agent is `ef851b22c506245441b9a630c093b3460e39cbdc`, not the failed `8c355a...`.

## Exact next dispatcher request

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-child-venv \
  venv-agent-child-d22-8c3b926e \
  8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe \
  full-current-v3-1229 \
  /home/user/work/wt/rt-pin-3b926efa
```

Once that immutable installed pair exists, run no more than four bounded original nodes (one per distinct proven child cause), retaining exact argv/env, `python -I` import origins, source/profile hashes, and stderr. Only a passing bounded qualification supports dispatch to the remaining product owner. The current worktree has no tracked changes.
