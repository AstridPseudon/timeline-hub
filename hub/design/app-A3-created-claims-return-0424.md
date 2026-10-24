## Completed

- Added Agent-ordered `created` claims to popup `occurrence.add-media` commands:
  - asset claim only when absent from the verified pre-edit registry;
  - clip claim always.
- Covered new assets, already-registered assets, and shared ADD behavior.
- Modified only the provider and focused A3 test.

## Tests

- A3 provider: **29 passed**
- Exact 12-file neighbor suite: **342 passed**
- Serialized TypeScript checks (`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`): **passed**
- Scoped ESLint (`--max-warnings 0`): **passed**
- `git diff --check`: **passed**

No full suite, browser, backend, or live transport tests run.

Commit message and `DONE` marker written.