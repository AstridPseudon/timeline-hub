## Report

Installed exactly the two authorized rows in `$ORCH/tests/suites.conf` via atomic replacement under the existing bench-store mutex and full-registry CAS.

Identity:

- Review/source SHA: `3d86494f48c7fe8ccad5559e94d8bcf7b1c9caa0`
- App: `be98aac5…`, tree `2839c7e7…`
- Agent: `5492fc80…`, tree `9fce413c…`
- Runtime: `e68cf231…`, tree `a2cbedd1…`
- Pure target: `app-P2-P3-e68-current-pure-target-1409`
- Runtime locks: 14 App / 15 Agent mappings, all identify Runtime `e68cf231…`

Registry:

- Pre-hash: `52f556f8…`
- Post-hash: `2ad71f2c…`
- Outsiders: 247 rows, 465609 bytes, hash `9acf76fa…`
- Mutex inode verified physical.

Candidate hashes:

- P2 row `d898fb5d…`; body `c742ca50…`; wrapped `007cd4ad…`; tail `0839e6b5…`; native `c96b2a48…`; encoded `76107a62…`; environment `97a03bbe…`
- P3 row `26a08305…`; body `d4fe6b90…`; wrapped `961d29ed…`; tail `eddcaf27…`; native `c96b2a48…`; encoded `9c67cf12…`; environment `c21b2b74…`

Checks passed:

- Dry source and optimized dry source.
- Normal and optimized `prepare()`.
- Decoded/wrapped Bash syntax.
- `py_compile` for 5 scripts.
- JSON validation for 2 artifacts.
- `git diff --check`.
- Readback confirmed both rows and all outsiders exactly.

The installer process returned nonzero after writing because its encoded-stage verifier regex was over-escaped. Installation was not retried; corrected read-only verification passed.

No service, browser, HTTP, backend, native, build, full suite, or manager P2/P3 request was run. Only `caller-custody.json` changed in the worktree; the shared registry received the authorized two-row update.