Prepared the [farm Codex brief](/home/user/work/wt/rt-OPS-farm-normal-init-sol-0413/ops-handoff/farm-agent-full/FARM-CODEX-BRIEF.md) and exact normal commands. Archived selected Agent lock `aa480e04…`, confirming Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. Full row and authentic template attachments remain unchanged.

Used existing `Store.initialize`; added no wrapper or Store changes. Preserved all six held replacement fixtures. Owner/index inode identity is not recorded by Store; index replacement is normal transaction behavior.

Tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp "$TMPDIR/normal-setup-tests" ops-handoff/farm-agent-full/test_normal_setup.py
```

**6 passed.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp "$TMPDIR/held-helper-tests" ops-handoff/farm-agent-full/test_farm_agent_full.py
```

**8 passed, 2 failed**: identical-byte owner/index replacement. Optional helper remains **HELD**; no full-artifact PASS claimed.

Ruff, manifest verification, template hashes, Python compile, `bash -n`, and `git diff --check` passed.

**Blocked:** a fresh Store has an empty index, so the existing Runtime maker invokes its builder rather than reusing legacy graphs. A private fixture confirms this. Independent review must resolve whether the no-rebuild constraint permits that first managed build. The recorded registry baseline also needs refreshing.

Wrote commit message and `BLOCKED`; no `DONE`. No live farm operations, installation, provisioning, full suite, or Git writes occurred.