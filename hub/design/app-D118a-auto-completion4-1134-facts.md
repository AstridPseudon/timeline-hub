# D118a facts

- The exact four retained nodes were run with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42aad0e9`, after the matching checkout receipt. Runtime HEAD is `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, and the checkout was clean.
- All four nodes reached the retained stale-read assertion at line 176. `at` and `hold` returned `value_conflict`; the unchanged test expects `dependency_changed`. No persistence occurred before refusal.
- A direct inspection of the genuine Agent caller’s prepared `clip.add-media` command showed anchor reads for `at`, `at_ms`, `track`, `hold`, `from`, `to`, and `speed` as field reads. The current conflict classifier therefore produces `value_conflict`; a scope read would be required for `dependency_changed`.
- Adding a scope read or changing the assertion would alter the production request/behavioral expectation and is forbidden by this task. The seam is outside the sole authorized test file.
- Target source remained byte-identical (`3138f2ac...`), so no commit is requested.

Static checks: Ruff, mypy with `--follow-imports=skip`, `PYTHONPYCACHEPREFIX=... python -m py_compile`, and `git diff --check` all passed.
