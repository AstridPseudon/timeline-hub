# Receiving handoff

The canonical script is the branch-owned author/reviewer command. An
independent reviewer must run that same command unchanged after the harness
commits the branch and must resolve the pending final commit/tree before any
receiving admission.

Current authenticated inputs:

- Base commit `60753548ebc8e69f3c84fbb28fa2e09b1ca78316`, tree
  `dd4347a933103bbfc17c3e3237d52ea13ac1f677`.
- Final harness commit/tree: pending; the script reports this explicitly.
- Agent runner `/home/user/work/venv-agent/bin/python`.
- Child Python `/usr/bin/python3.13`.
- Governing Ruff `/root/.local/bin/ruff` 0.16.8.
- No Main-venv runtime dependency or package acquisition.

The canonical result is not permission to run the production caller or a real
whole-maker E2E. Those remain gated on canonical PASS, the unchanged
5905580032-byte reserve, the independent review, and the existing Agent-only
receiving process. The stopped 1933 duplicate is not relabeled as a final
failure.
