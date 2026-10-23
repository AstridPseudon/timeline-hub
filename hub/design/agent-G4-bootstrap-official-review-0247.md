# Agent G4 bootstrap official review

Independent review of `b99b04ba89cceb0b370d54ee270e00199e81c4da` (`681f4c6e7` + official `2410c3bbb`).

**Verdict: G4 FAIL overall; source/no-wire PASS.** The first original real-Runtime bootstrap positive fails during undo with Agent’s inverse validator calling `State.entity('timeline')`. The same failure reproduces against an extracted exact official Runtime `21482a416d1f0f976ec563b9e1bf96a765f80e56`, so this is not a missing R24454 dependency.

Failure path: `tests/v10/test_timelines_create.py:617` -> `commit.py:1023` -> `commands.py:238` -> `inverse.py:478/_validate_inputs` -> `inverse.py:396-397` -> `_command_state.py:271`, `unsupported entity reference 'timeline'`. `timeline` is a read-only whole-closure scope, not an entity. The minimal fix is to exempt `ref == 'timeline'` from both inverse binding entity-existence checks in `astrid/sdk/timeline/inverse.py`; do not add it to `State.entity`.

Evidence: real Runtime first-case `1 failed, 28 deselected`; no-wire v10 `28 passed, 3 deselected`; focused no-wire `94 passed, 1 deselected`; provider/document no-wire `138 passed`; normal Ruff ratchet `2150/2150`; focused Ruff and private focused mypy pass. The unfiltered focused lane has one unchanged schema census failure (55 expected vs 58 actual). Normal mypy wrapper was environment-blocked by missing `types-PyYAML`/NumPy stubs; prior normal count was 1913/1913.

Exact official generated/client pins match 21482: `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`, `a79b2e12de96ec8f2c4bf7b6811ccb3538baf18ca839172f7a3d7bf525029aae`, `aa616ed7e9dc5708ef36fed43070b4e2e7d7c903ad791faa723dcbd4e25ccf37`, and `88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616`. Current Runtime differs from that pin only by the known 4-line merged-response decoder change. V4 deletion paths remain absent. Original assertions and parent-media helper/test are byte-identical to base. No tracked edits were made.

See the worker report for commands, callstack, hashes, and detailed findings: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-bootstrap-official-review-0247/report.md`.
