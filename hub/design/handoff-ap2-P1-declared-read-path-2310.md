Implemented the single P1 oracle correction:

- Changed only `tests/e2e/local/three-products.p1-chain.spec.ts`, replacing `app.astrid` with `at`.
- Base: `4ded7eefdbcbeaf0d6cecc58e55f7083004167d2`
- First-case hash unchanged: `4b04ad7e…a72ea8b7f`
- New second-case hash: `947cbf32197121acc0d16eb39e230608a4c238e86ac00b9e2717349fc93262ac`
- Gate-5 unchanged: `37caf285…e74b1`

Checks:

- Node v20.19.4: pass
- All three serialized TypeScript checks: pass
- ESLint with `--max-warnings 0`: pass (`--max-warnings0` is invalid syntax)
- Playwright `--list`: pass, exactly 2 tests, no bodies run
- `git diff --check`: pass
- Outside-target byte audit: pass

No browser, HTTP, socket, service, or full suite was run. D16 adaptation and commit message were recorded; `DONE` marker created.