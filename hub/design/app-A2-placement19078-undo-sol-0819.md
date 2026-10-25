Found the precise boundary: **Undo never receives a click.** Both retained attempts leave the embedded modal open; the enabled parent Undo sits beneath `aria-hidden="true"`, so its role locator remains unresolved. The response wait times out, then teardown ends the pending click with `TargetClosedError`.

- No product repair justified; product source and protected originals remain unchanged.
- Wrote [cause notes](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A2-placement19078-undo-sol-0819/notes/placement-Undo-cause.md>), companion JSON, and an unapplied one-line proposal to close the dialog before Undo, matching passing ADD19078.
- Both trace archives and protected source hashes verified.
- `git diff --check`: PASS.
- `git diff --exit-code 04beedcd18b8abb49502f65cd3facaafbe93db4e -- tests/e2e/local src`: PASS.
- Proposal `git apply --check`: PASS; worktree clean.
- Tests, tsc, lint, browsers and services: **NOT RUN**, per the read-only finding rule.

Next: protected-original owner authorization and review, then an authorized placement run. Inverse acceptance after dismissal remains unverified; no newGREEN claimed.

Commit message and `DONE` created.