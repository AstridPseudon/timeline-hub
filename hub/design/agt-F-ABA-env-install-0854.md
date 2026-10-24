## F-ABA environment-install report

Installed the reviewed `authoring-current-becfe-nodes` row in the operational registry.

- Replaced exactly one authorized old row:
  - Old row SHA-256: `f7bd322a...f0593de31`
  - New row SHA-256: `61b7e27e...9e9978067d`
- Registry hash: `83ff4c2b...90902d27` → `5ada8596...1dbe851f`
- Outside-byte identity: PASS
- One live key at line 173; regular non-symlink mode `0600`
- Backup: `/tmp/w-3e12a67bae/suites.conf.pre-install.backup`
- No product-home merge or deletions.

Checks passed:

- `bash -n` candidate, registry, and `request-test`
- Synthetic candidate control: 23 guards, 59 assertions, serialization, selector propagation, and failure propagation all PASS
- `git diff --check`
- Worktree clean

No preflight, pytest, service, realm, child, browser, full-suite, or gate execution was performed. Recommended next step: request the single exact-selector service run.