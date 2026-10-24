## PASS

- Reviewed commit `6859c4035ae5da72adb7b7e27eddf02177b70c58`, tree `7ca87cedc8d06bed3de8980c806eb567b170fa3e`.
- No product/test changes needed; finalized authorbase is correct.
- All four protected upstream assertions retained:
  - shell portal parent
  - `absolute` class
  - chat Escape ignored
  - shell Escape exits once
- Frozen test body hash matches: `40564bab4179dbcf0165fe652658abb43f6b2c13a34a8c06ac078c29b44b6339`.

Checks:

- Node 20 targeted Vitest, serialized: 15/15 passed.
- `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`: passed.
- Scoped ESLint and `git diff --check`: passed.
- Author regression check: old source was RED (7/8); restored source GREEN (15/15).
- Production caller verified in `ExtensionPanelHost.tsx`, including controlled exit and state-preserving panel movement.
- Standalone, shell, cleanup, Escape, focus, state, and host lifecycle cases accounted for.

No browser, e2e, full-suite, or service checks run. Commit message and `DONE` marker written.