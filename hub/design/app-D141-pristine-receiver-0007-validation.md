# D141/F source validation

Status: source target prepared exactly; full and pristine bodies were not run.

Read-only checks and results:

- `git rev-parse HEAD` in `/home/user/work/wt/app-D141-pristine-receiver-0007` returned `7ca61bb3280beca21d98a854af266a382f7ce5df`.
- `git rev-parse HEAD^{tree}` returned `974de7cd08900872eeb0bd6f6004d44323e01fab`.
- `git status --porcelain` was empty and `git diff --quiet` passed.
- SHA-256 values of `package.json`, `package-lock.json`, and `runtime.lock.json` exactly matched the frozen values published in `app-D141-full-pristine-return-2354-source-manifest.json`.
- The existing suite registration at `tests/suites.conf:69` is exactly `npm test -- --maxWorkers=3`; no suite/config/framework was added.
- The existing request route accepts the worker metadata target; no request row was created and `request-test`/`wait-test` were not called.
- `/opt/node20/bin/node` reported `v20.20.0`; `/opt/node20/bin/npm` reported `10.8.2`. The package declares Node `>=20.19.0` and npm `10.8.2`.
- The worker `node_modules` resolves to `/home/user/work/app/node_modules`. This was treated as a shared read-only install presence check only; dependency readiness was not claimed.
- `bin/test-run` was read for its existing result paths: result request/status/exit/summary/log.txt/d66 and snapshot `/home/user/work/wt/.test-<id>`. No test-run was started.
- The live `/home/user/banodoco/reigh-app` checkout is clean but currently has HEAD `580508eed1bf6ed95caaf476c9d69a4672472a2f`, tree `ab3a5e296b01cc5458c88049c9eb5be402a05ccf`, and non-matching package/lock hashes. It is not the required comparator; no checkout or adaptation was attempted.
- `D141-cut-tuple.md` still records the App integration head as pending and does not record MAIN GO.

Not performed by scope: npm install, imports, test collection or execution, Vitest, node:test, lint, typecheck, build, browser/socket work, full suite, comparator suite, fetch, checkout, merge, commit, or source adaptation.

The source target is therefore an exact receiving target, not proof of dependencies, schema/profile readiness, test results, or comparator qualification.
