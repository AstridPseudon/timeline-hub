Completed F-D40 consumer from WIP `f93c69bd70`. Wrote `commit-msg` and `DONE`.

The existing host now binds Runtime’s capture to retained preparation, owner grants, repository/revision and selected definitions. Commands and Python actions receive captured bytes through inherited descriptors and use the existing loader. Source/ancestor mutation, revoked custody and namespace collisions fail closed. Captured native commands are refused.

All pytest runs used:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-f3208b26 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f3208b26 /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider
```

With these exact suffixes:

- `--basetemp=/tmp/w-6172aa892a/d40-final-tested tests/core/execution/test_runtime_source_custody_d40.py` — **32 passed**.
- `--basetemp=/tmp/w-6172aa892a/d40-neighbors tests/stage1/test_pack_host_interpreter_identity.py tests/core/execution/test_generic_host_contract.py` — **56 passed, 2 failed**. Failures report missing installed VibeComfy and unset `ASTRID_VIBECOMFY_CHECKOUT`.
- Exact-parent narrow controls, run through `/tmp/w-6172aa892a/parent_controls.py` — **2 expected RED failures**; corresponding candidate controls pass.

Scoped Ruff/private mypy comparison against the exact parent: **105→105 / 143→138 diagnostics; zero added normalized identities**.

Passed:

- `git diff --check`
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4`

The legacy `34eac004` vendor probe failed because the parent lock pins `45c3a7f4`; pins remain unchanged.

Next: cumulative independent security review, then one original external positive in the managed installed candidate. Installed-host qualification remains unverified. Original guards/attack bodies and Runtime/client/schema files were untouched.