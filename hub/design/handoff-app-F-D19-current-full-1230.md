# F-App-full D19 — PASS

Exact App source identity is `12ef32054524a3cce449fdcb6d94788415b9571a` / tree `4bf9a980d1d5ef38d485702006e52ee33f5dbc3d`. The worker-private normal dependency graph uses the checked-in Composition archive (73,451 bytes, 80 members, SHA-256/SRI `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`) at package version `0.0.14`; public executable imports pass. Current source differs from prior qualified `ad96a4cac` only in the three reviewed e2e/support files named in the worker report.

Exactly one App full service request was accepted with `--no-cache` at `2026-10-23T12:31:30Z`: `app-F-D19-current-full-1230-full-1023123130-3925`. The snapshotted tree was `4bf9a980d1d5ef38d485702006e52ee33f5dbc3d`; the test started at `12:31:41Z` and completed at `12:47:43Z`.

## Verdict — PASS

The exact command was `npm test -- --maxWorkers=3`. The service returned exit `0`: 1,309/1,309 test files and 18,819/18,819 tests passed. There was no zero-test condition and no exit mismatch. The full log is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-F-D19-current-full-1230-full-1023123130-3925/log.txt`. The historical baseline service was `app-full-1023100721-23537`; its `23537` suffix is a service ID, not a test total. That baseline recorded 89 failed + 18,706 passed tests (18,795 total), and 20 failed + 1,288 passed test files (1,308 total). Current D19 has no failures to classify. Expected negative-path React/jsdom diagnostics appear in the log with passing assertions. P1 remains NO-GO; this result does not infer P1 GO.
