Implemented OPS inventory installation preparation under `ops-child-custody/install-prep/`:

- Exact candidate/preimage/hash/mode manifest and gated runbook.
- CAS-guarded, no-clobber backup, atomic replacement command.
- Private TMPDIR-only controls for positive match, wrong preimage, backup collision, helper invariance, symlink/hardlink refusals.

Validation:

- 40/40 existing tests passed.
- Private controls passed.
- Ruff, `bash -n`, AST parse, and `git diff --check` passed.
- No live install, Store init, E2E, package acquisition, or ORCH writes performed.
- E2E1800 and independent review remain required; D125b holds installation.

Evidence:

- [install-inputs.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-inventory-install-prep-1811/evidence/install-inputs.json)
- [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-inventory-install-prep-1811/evidence/validation.md)
- [receiving-note.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-inventory-install-prep-1811/evidence/receiving-note.md)

`DONE` created; commit message provided to the harness.