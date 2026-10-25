## D122 Report

- Read-only investigation completed; no source, tests, profiles, or suites changed.
- All 14 retained failures are `REG14`, with identical test bodies and one common cause.
- First cause: registry child stderr reports `ModuleNotFoundError: No module named 'runtime_protocol'` at `astrid/core/rendering/remotion_runtime.py:26`.
- Terminal `RemotionValidationError` at line 700 is only the custody wrapper after child exit code 1.
- Cause: source-mode worker projection drops the parent Runtime checkout from child `PYTHONPATH`. Passing upstream14 used a private overlay containing pristine Runtime modules.
- Narrow repair: update the existing source-mode child import projection or use the proven authenticated overlay. Product follow-up remains owned by `agt-D122-host14-source-1201`.

Evidence:

- [D122-host14-wholepath.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D122-host14-wholepath-1201/evidence/D122-host14-wholepath.md)
- [D122-host14-wholepath.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D122-host14-wholepath-1201/evidence/D122-host14-wholepath.json)

Validation: JSON parsing and 14-selector accounting passed; `git status` and `git diff --check` passed. No new pytest/lint/full/browser/render run, per task.

Commit message and `DONE` marker created. Design handoff was not directly written because worker rules prohibit direct `design/` writes; its contents are in the evidence packet and this report.