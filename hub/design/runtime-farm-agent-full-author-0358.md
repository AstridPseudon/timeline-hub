## Completed

Created the candidate kit under [ops-handoff/farm-agent-full]( /home/user/work/wt/rt-OPS-farm-agent-full-0358/ops-handoff/farm-agent-full):

- Safe `Store.initialize` first-use helper with reopen/owner validation.
- Private fixture tests for valid reuse and all requested refusal/no-write cases.
- Byte-exact approved Remotion row/env attachments.
- `full-farm` registration candidate pinned to Runtime lock commit `45c3a7f…`.
- Transactional install/rollback instructions and SHA-256 manifest.

Tests:

- `pytest ... test_farm_agent_full.py`: **4 passed**
- `ruff check`: **passed**
- Manifest verification: **all OK**
- Exact `cmp`, decoded hashes, row parsing, env `bash -n`, in-memory compile, `git diff --check`: **passed**
- Shellcheck: N/A, no new shell files.

Unverified/blocking facts:

- `/home/user/work/wt/rt-pin-45c3a7f4` is missing; obtain it via normal `request-checkout`.
- No actual `full-farm` snapshot/log exists yet.
- No live store, registry, queue, provisioning, checkout, or full-suite operation was performed.

Commit message written and `DONE` marker created.