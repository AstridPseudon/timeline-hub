## Report

Completed F-D86 current96 MAIN targeted body with no worktree changes.

- Immutable tuple verified: Agent `dc909681`, Runtime `6634a17`, App `043631d`, Composition `635f4de`.
- Route syntax: `bash -n .../main-affected-batch-recipe.sh` — PASS.
- Controls: positive exit `17`/7 marker bytes; poison exit `1`/0 marker bytes — PASS.
- Central request ID: `agent-fd86-current96-body-0415-1025041953-6058`.
- Command: `pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45` with 96 exact selectors.
- Result: `14 passed, 7 failed, 75 errors, 0 skipped` in 43.04s; automatic NO-GO only, no semantic verdict.
- XML, logs, argv, receipts, per-ID routing, exact counts, packet hashes, and tuple/profile evidence preserved under the worker evidence directory (4.4 MB).
- Suite configuration restored byte-for-byte. Worktree remains clean.
- No full suite, browser, build, local pytest, or rerun performed.

A prior setup-only request exited 2 before body execution; the corrected request above was the sole actual body. No blockers remain. `DONE` and the required commit message were created.