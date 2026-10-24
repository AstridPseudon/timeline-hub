## Result

- **Installed integrity: PASS.** Four reviewed hashes match live ORCH/bin, normal hub, and committed `HEAD`:
  - helper `02513492…7d68`
  - Store `bd18ef1…c44e3f`
  - maker `c1197e1…fa3b6`
  - requester `08f1b00…2fde`
- **Protected-route attribution: PASS.** The `ensure-daemons` changes were unrelated host remediation, not installer-caused:
  - `992510…` → `9c4290…` at 10:27:44, matching orchestrator `LOOPS #62` and STOPPED markers.
  - `9c4290…` → `2ef5a5…`, matching `LOOPS #63` recycle-on-finish remediation.
  No separate worker commit/review receipt exists; attribution is via orchestrator records and hub-sync provenance.
- **Committed publication: PASS for the four reviewed files.** Current hub `HEAD` is `15eee8cd`; all four reviewed files are committed and byte-identical to live/normal hub.

Current protected-route caveat: live and normal hub `ensure-daemons` are `2ef5a5…`, while committed `HEAD` still contains `9c4290…`. This is ordinary publication lag for unrelated drift, not an installer failure.

## Evidence and tests

Read-only commands passed:

- `sha256sum`, `cmp`, and `git show` across live/normal/committed copies.
- `git log/show/diff` for publication commits.
- Existing route proof in installed-review1027: requester → source carrier/wheelhouse → maker → Store → embedded verifier/helper across creation, relocation, final verification, and seeded reuse.
- Three read-only publication samples over 10 seconds: stable.

No product tests/typecheck/lint were run, as explicitly excluded by the task. No installation, process probe, daemon execution, Git mutation, source grant, Store mutation, or child request occurred.

Worktree is clean. Harness `DONE` and conventional commit message were created.