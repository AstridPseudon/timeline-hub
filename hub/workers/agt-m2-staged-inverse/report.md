Implemented guarded staged reversal: own consumers reverse before created-track removal; exact order, immutable input claims, M1 compatibility, and later-dependent/ABA refusals remain guarded.

8 files changed: **+375/−39 lines**. No schema or State/root-helper changes.

Verification:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_sync.py
```

**291 passed in 15.75s.** Product/test Ruff checks and `git diff --check` passed.

Decisions: check noncontiguous history relative to each target; recover legacy inverse stages through verified boundaries; exercise composition with registered test recipes without implementing move-set.

Both `commit-msg` and `commit-msg.txt` written. No blockers. Full/socket suites remain unrun; next is manager review and central testing. Integration remains held pending recorded M1.