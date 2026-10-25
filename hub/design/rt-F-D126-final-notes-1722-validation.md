# D126 delivery-notes validation

The installed inputs are the existing builder-consumed files under
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/`.
The approved line was absent from both predecessors and appears exactly once in
each candidate. Each candidate is its predecessor plus that line and one LF
(90 bytes); all other bytes are preserved. Both installed files are regular
`0644` files.

Installation used predecessor SHA-256 CAS guards, mode guards, fsynced same-filesystem
temporary candidates, and `os.replace` installation. No delivery builder was active
before installation. The installed candidate hashes and modes are recorded in
`receipt.json`; the evidence predecessor/candidate files are byte copies of the
installed inputs before/after installation.

Source disposition consumed:

- `design/app-D126-normal-home-1437.json`: normal `84857c4...`, tree `7feb5b1...`,
  independently reviewed candidate `9d75477...`, same tree, `PASS_SOURCE_ONLY`.
- The four exact authored `app-D124-bounds-final-review-1414-*` documents were read
  and hashed in `receipt.json`.
- Historical `design/app-D126-ledger-zip-note-1359-report.md` is explicitly FAIL and
  was not promoted.

Validation commands and results:

- `git diff --check` in the Runtime worktree: PASS; worktree remained clean.
- `git diff --no-index --check --unified=0 evidence/predecessor-* evidence/candidate-*`:
  PASS; expected sentence-only differences and no whitespace diagnostics.
- Installed `delivery-build` `render_readme()` with the controlled four-repository
  stub (`agent`, `runtime`, `app`, `composition`): PASS; exact line present, zero
  unresolved `{{...}}` placeholders, balanced fences, and normal summary/applying
  sections present.
- Candidate equality/hash, exact-one-line count, predecessor preservation, `0644`
  mode, and no active `delivery-build` process: PASS.

No Runtime product tests, typecheck, lint, full suite, native/browser/server run,
build, final pin, gate, ZIP, or release claim was made. C0 request/reply shape,
trust, authority, schema, pins, generated files, tests, and D130 SWAP/WAL remain
untouched.
