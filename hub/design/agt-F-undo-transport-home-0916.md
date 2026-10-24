## Report — F-undo-transport-home

- Qualified integrated Agent `ba55ac1e9e`; merge parent `f966c9ea6a`.
- Tree: `c13d368666e710bb911ff448b86251b516867c03`.
- New test blob: `f45dc55c6f906f45c0b4c331cb8d44b4912b40a8`.
- Runtime pin: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`.

Tests:

```text
17 passed in 0.98s
```

JUnit XML: 17 tests, 0 failures/errors/skips. SHA-256:

```text
7a156b4ecb5614aa82ebb80d9aff227b128e7adca2d45ce82ff73832ab858458
```

Static checks passed:

```text
ruff check --no-cache: All checks passed
mypy --python-version 3.12 --follow-imports=silent: Success
git diff --check: passed
```

`WorkspaceClient`, `commit_session`, `sync`, `outbox`, generated transport, and original target tests are byte-identical to `0c2c28da4f`. No product or existing-test edits were made. Working tree is clean.

This is offline fake-transport qualification only; it does not claim Runtime authorization, origin acceptance, guarded inverse, or live lost-ack behavior. No blockers.