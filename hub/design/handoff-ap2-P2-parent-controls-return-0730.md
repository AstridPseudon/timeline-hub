## P2 report

Changed only `tests/e2e/local/support/p2-parent-oracle.test.mjs` (+13 lines).

Added strict refusal controls for:

- Wrong request/step read path, value, and state
- Extra top-level, command, step, select, and args keys
- Altered base revision/publication metadata

Production spec remains unchanged.

Checks:

- `/opt/node20/bin/node --test ...p2-parent-oracle.test.mjs ...p2-transition-oracle.test.mjs` — exit 0
- ESLint control file — exit 0
- `git diff --check` — exit 0

Hashes:

- Parent control: `a0bfad5dfa9c2ae14c36508543ccce00c53d459a5c4c3569198c2411407dfc5f`
- Production spec unchanged: `2eb041e18711db0e9e81966604fd8616ad3819e75e3798ed1c1f2c32cfff0b8e`

No browser, full suite, TypeScript rerun, product/helper changes, or deletions. Commit message and `DONE` marker written.