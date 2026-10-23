# F installed review — bounded correction required

Result: **FAIL; no `suites.conf` row activated and no test-service request**.

The prescribed private environment
`/tmp/w-827c512f9a/installed-runtime-ef851-1365/` no longer exists. Its
interpreter, wheelhouse, site-packages, and `profile/astrid.json` are absent.
This prevents independent verification of wheel hashes, all 164 dependency
identities/RECORD paths, isolated `python -I` origins, and profile custody.
The prior worker report is retained as historical evidence only.

Independent checks that remain available passed:

- Agent ef851 source/tree: `ef851b22c506245441b9a630c093b3460e39cbdc` /
  `b11eee891208d11e23c55950f8954ddd3377d5a8`.
- Runtime 1365 source/tree: `1365e4b17b31c4a7093d5943674637067fd2bab4` /
  `6c69c3dc47822fffbaf27cd63815d2895155ffaa`.
- Free disk: 16G reported on `/tmp` and `/home/user`.
- Proposed shell syntax: `bash -n`, exit 0.
- Current target/shared worktrees were clean; no shared file was changed.
- Existing `suites.conf` outside-bytes SHA-256:
  `df3d20c8204ff4b9b41bb381014119132b50d7dbd2fc4a47ae4ba9df7db751a8`.

The proposed command also cannot qualify D09 as written. The original D09
fixture unconditionally overwrites `ASTRID_RUNTIME_CHECKOUT` with
`/home/user/work/runtime` and `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` with
`/home/user/work/venv-agent/lib/python3.13/site-packages` (lines 90 and 105).
Those are shared/current paths, not the private installed modules. The narrow
correction required before activation is to provide an already-approved
fixture seam that resolves those two values from the private environment (or
explicit owner approval for the minimal fixture seam change); a suite-row
environment assignment alone is ignored by the fixture.

Required next step: provision/preserve the exact private environment at a
durable path, repeat the isolated import/RECORD/origin audit, then inspect the
fixture seam again. Only after that PASS may one named row be added and the
two exact original nodes be run once through the central service.

