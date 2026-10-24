## PASS — read-only occupancy accounting review

- Runtime: `faf6a5477f9f6e4d96829046957518fef7a0dbed`
- Tree: `5e909a876c780025c4b8aca10e42ff57cac092fd`
- `tl/integration` resolves to the same commit/tree.
- `faf6` is a merge of `2b49da8d6` and reviewed `f8051e52b`; “before/after” denotes ancestry, not a live pre-run observation.
- Only `tests/test_timeline_legacy_occupancy.py` changed from `2b49`; fixture blob matches `f805`: `c8d2e453…`.
- Authentication blob preserved: `9754e2d…`.
- Agent custody: commit `9f2da582a6767030055e54092287d40f2b8f74bb`, tree `80c4f98c…`; the logged run resolved imports from its read-only archive with no overlay.

Logged complete test invocation:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/tmp/w-5b72f0dd9c/agent-source-9f2 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_legacy_occupancy.py
```

Result: `16 passed in 45.92s`. The earlier process stopped after two dots and produced no result; it receives no credit.

Original 15 occupancy nodes credited:

- unrelated destination refusal: `[False-False]`, `[False-True]`, `[True-False]`, `[True-True]`
- `test_exact_f1_over_http`
- occupied destination without shot head: `[False]`, `[True]`
- current closure update/retry ordering
- verified current closure: `[receipt]`, `[occurrence]`, `[digest]`, `[projection]`, `[removed]`
- historical reuse preserving newer global shot head: `[False]`, `[True]`

The new direct-retirement 16th case is excluded from original-36 accounting.

D43 result: **26 closed / 10 open / 36 total / 0 unaccounted**. The remaining 10 are the headless selectors. No whole-suite PASS or extra Agent source-copy closure was claimed.

All prior 11 closure source blobs remain unchanged:

`2fff9a4c`, `297b8813`, `7a4d8e83`, `2856cab5`, `be5e7c9f`.

C0v2 contract/runtime/client paths are unchanged, and the production caller invokes `runtime.commit_timeline` (`runtime_protocol/server.py:302`).

Checks: `git diff --check` passed; logged Ruff check passed. No tests, typecheck, full suite, or tracked files were run/modified by this reviewer.