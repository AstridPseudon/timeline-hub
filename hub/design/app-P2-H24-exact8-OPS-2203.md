Implemented the H24 P2 `full-e2e-three-products` suite-row adaptation in shared `tests/suites.conf`.

- Updated App source/tree, current P2 body hashes, managed Agent/Runtime receipts, Node/npm paths, private graph, preflight evidence, and mounted-readiness guard.
- Preserved the original eight-test invocation and assertions.
- `bash -n` validation: PASS.
- Full service run: `app-P2-H24-exact8-OPS-2203-full-e2e-three-products-1023220704-3502` — FAIL-fast before body. Initial row built after private graph mount, causing `vite: not found`; retained logs confirm all eight tests were NOT RUN. Corrected afterward; no resubmission per run limit.
- Worktree clean. Commit message and `DONE` marker created.
- No P3 row modified or run.