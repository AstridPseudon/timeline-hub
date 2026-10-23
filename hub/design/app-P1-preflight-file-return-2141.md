## Report

READY — updated only the existing `ap2-P1-chain-h6` row in [suites.conf](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf:242>).

- Preflight logs now persist privately under verified `ORCH/tests/<.test-ID>/preflight`, mode 700.
- Captures global setup, actual beforeAll, trivialboot, and selector-collection logs with exit/timing status.
- Preserves fail-fast behavior and original body invocation unchanged.
- Added request/path/symlink containment checks.
- No actual browser, backend, seed, or body rerun.

Verification:

- `sed -n '242p' .../suites.conf | bash -n` — PASS.
- Isolated stage-failure fixture — PASS: exit `7`, durable logfile, no body marker.
- Worktree clean; no repository source changes.

Hashes:

- Row: `eebe9ff2df5e49f729aa9bd7c56839f2bcf890abb42192d803b4a7906121e724`
- Run-folder guard: `29b6bbd1de805034dabf2fb120359f63097396ecfb5b4a17e7c853341b877917`
- Stage transport: `5da779df5984505efd3d28cf7fce9f5bcee569c28a2636165080c42cd528360c`
- App source/tree: `e6d72d3d...` / `6513960e...`
- P1 body SHA256: `2bef958d775bc46f70f79733a2c6182ad73af8e8b336ffd9afc024bf3e0a4288`

Counts: 4 stage invocations, 3 fail-closed `NOTRUN` branches, 2 protected body selectors. Existing failure remains unclassified; manager may run one changed diagnostic.