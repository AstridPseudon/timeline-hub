# D52 report

Implemented the smallest proved correction in `tests/test_sdk_public_surface.py`: the test double now accepts the live runner’s `_captured_source` keyword. Assertions and behavior remain unchanged.

Validation:

- Exact seven-node pytest run: **1 passed, 6 failed**.
- Public-surface node now passes.
- Remaining failures all share one live cause: `music.duck` is discovered by `GenericPackHost` but absent from the approved matrix/lock (`105 vs 104` discovered; `108 vs 107` pack labels).
- Generator dry run: unchanged catalog.
- `ruff --select F`: pass.
- `git diff --check`: pass.
- Test-body AST parity: pass; hash `a2467b5d92dab7994782e66575fc67e4ffa05d35e6788547bc9db205fd08e111`.
- Durable XML: `/tmp/w-95d8385977/current-seven-after.xml`, SHA-256 `b1cfd9c373b98d212cdfdd1c3c466a9fe2d686bb481e71b84121ada88a5b208b`.

Decision/blocker: no matrix, lock, baseline, or generator changes were made. `music.duck` is a live registered capability, not obsolete scope; its missing approved matrix row requires source-owner handback. Next PR-sized action: approve the `music.duck` matrix entry and regenerate the census lock, then update the corresponding count expectations under review.

No full/gate suite run. Completion marker and commit message were created.