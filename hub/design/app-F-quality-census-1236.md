## Report

- Base: `cca3deb361e8fbbc62ddf491d5fd09c7e542b99f`, tree `911956d49c42021f11d21e9cf69e9e9478ab569a`.
- Full run `16138`: Vitest `19,251 PASS`; Node `38 fail`. Relevant blobs match snapshot tree `3311baa...`.
- Retained blocks: `log.txt:30022–30083`.

| Node | Classification | Result |
|---|---|---|
| `capture-extension-external-evidence.test.mjs:131` | Non-core, environment | `ssh-keygen ENOENT`; absent locally and same invocation exists in frozen upstream. |
| `check-extension-ship-evidence.test.mjs` | Non-core, environment | Import-time `ssh-keygen ENOENT`; no security logic changed. |
| `check-known-failures.test.mjs:103` | Non-core, ours regression | Stale fixture expected 3 markers, but current and frozen drag tests contain 0. Fixed expectation to 0. |

Change: [check-known-failures.test.mjs](/home/user/work/wt/app-F-quality-census-1236/scripts/quality/check-known-failures.test.mjs:105)

Tests:

- `node --test .../check-known-failures.test.mjs` — PASS.
- `node scripts/quality/check-known-failures.mjs` — PASS.
- Capture and ship-evidence tests — fail only on missing `ssh-keygen`.
- `git diff --check` — PASS.

Release dependency reported, not changed: `verify-extension-ship.mjs` requires package script `test:e2e:chrome-export`; release worker owns it. No package, release, product, security, or protected-test changes.

Commit message written to the required path; `DONE` created.