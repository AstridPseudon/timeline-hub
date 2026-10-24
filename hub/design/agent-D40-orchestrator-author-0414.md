Implemented F-D40. The pre-fix fixture reproduced `HostError: external execution requires a discovered definition`.

The authority chain now flows through the existing paths: Runtime f320 owner capture → retained scope/profile binding → captured orchestrator manifest → exact admitted record → inherited descriptor → existing orchestrator runner/subprocess → captured source loader. Root, revision, tree, owner, channel, epoch, custody and definition remain bound. Integrity checks refuse mutation; discovery and execution use captured definitions and code.

Changes are limited to the three allowed product files and one new regression file. Existing test bodies, Runtime, clients, schemas, pins and `host_bootstrap.py` are unchanged. Captured orchestrators use static manifests and the existing Python runtime; unsupported sources fail closed.

Both pytest runs used:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.:/home/user/work/wt/rt-pin-f3208b26 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f3208b26 \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider
```

With these exact arguments:

- Pre-fix: `--basetemp=/tmp/w-6ddf9a8836/parent-red tests/core/execution/test_runtime_orchestrator_custody_d40.py::test_existing_orchestrator_invocation_uses_owner_capture` — **1 expected RED failure**.
- Final: `--basetemp=/tmp/w-6ddf9a8836/final-closure tests/core/execution/test_runtime_orchestrator_custody_d40.py tests/core/execution/test_runtime_source_custody_d40.py tests/core/execution/test_generic_host_contract.py` — **77 passed**.

Additional checks passed:

- Scoped Ruff: **105→105**, zero added identities.
- Private mypy against exact parent `69a854d82b`: **140→140**, zero added identities.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4`
- `git diff --check`

`commit-msg`, evidence and `DONE` are written. No source-fix blockers remain. Original external positive, installed child, cohort 86 and full suites were **not run**. Next: independent review, then separately authorized installed qualification.