## Report

Implemented P3 setup-only correction in the three authorized files. The observer/helper now matches the authentic mounted parent `doc.patch` request, validates reads, steps, response claims, canonical state, receipt, head, and settled outbox ownership. Added negative controls for wrong before/value/readset/claims.

Source diagnosis: current production parent path emits `doc.patch`, not the prior `clip.move` shape. Historical browser body and zero-POST cause remain unknown; no product root cause is claimed.

Validation:

- Offline acceptance test: passed.
- TypeScript root/node projects: passed.
- `tsconfig.app.json`: earlier exact run passed; duplicate final run hung silently and was cancelled.
- ESLint on all three files: passed.
- Playwright collection: passed, 15 tests.
- `git diff --check`: passed.
- Reset/tail preservation hash: `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`, matching base and `c0fe` reference.

No browser, backend, live service, or full suite was run. Commit message and `DONE` marker were created.