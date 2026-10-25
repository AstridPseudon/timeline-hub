PASS

Reviewed `67dc61b693` against base `34d4644`. Only the intended test file changed; existing predicates/input remain intact.

Evidence:

- Targeted suite: 6 files, 105 tests — PASS (exact-tree cached result).
- Typecheck — PASS.
- Scoped ESLint — PASS.
- `git diff --check` — PASS.
- Mounted panel → real adapter/hooks → provider → handoff/session → IndexedDB outbox → generated decoder verified.
- Five controls cover pending, accepted/merged canonical adoption, refusal rollback, panel reopen reset, and restart replay of identical body/key.
- No source or test changes made by reviewer.

D121 limitation preserved: no claim is made about Runtime receipt within five seconds. The unassigned 1.75-second replay is not correlated browser evidence. React duplicate-key warnings appeared in the mounted fixture, but all tests passed.