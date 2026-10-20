Implemented the WC9 docs repair in [SKILL.md](/home/user/work/wt/agt-m2-wc9-guidance-final-fix/astrid/packs/rendering/docs/SKILL.md):

- Detached checkout edits are migration-only/held.
- Unsupported intent visibly refuses while retaining the draft.
- Publication uses captured commands, durable outbox, or settled proposal requester.
- Removed the runnable detached `publish` fallback.

Validation passed:

- Doc references: 0 errors/warnings.
- 8 fenced Python blocks parsed.
- CLI help and public signatures passed.
- `git diff --check` passed.
- No full/tests/browser suites run.

Updated handoff, WC9 ledger (`IN PROGRESS`/`HELD`), report, commit message, and `DONE` marker. Combined signature import exposed a pre-existing circular import; isolated probes passed.