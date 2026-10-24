## Result: PASS

The exact D40 StageB0551 external-pack original earns closure.

Retained run (not rerun):

```text
/home/user/work/bench-store/entries/child-3b5cb98c4f2dfc20ce8747f68bf2e1124ff47b9dd5f04dabaada3a22278fdfc9/bin/python -I tools/run_d40_installed_observed.py run-original --root "$PWD" --evidence <stage-b> --reviewed-source-sha256 cddde857a154057b3bea16643a44b65a77b1b85b0043ed259d25cfb4810067db
```

- Exit `0`; JUnit: `tests=1, failures=0, errors=0, skipped=0`; `1 passed in 4.59s`.
- Observer: `calls=1`, `direct_values=1`, `observer_errors=[]`.
- Direct actual return: `imported_from=/tmp/w-badaa699e3/d40-rt_sytyf/d40-body/test_generic_host_runs_externa0/external_pack/external_pkg`.
- Production caller and return code originated from installed child `site-packages`.
- Original test file SHA: `3d8538d03b59eeb0f5cf0b397f639af0dfa3f5cbb5ce3b102001c427d6eb48ef`.
- Three assertions unchanged; independently reproduced all retained AST hashes.
- Runner SHA independently reproduced: `cddde857a154057b3bea16643a44b65a77b1b85b0043ed259d25cfb4810067db`.
- All 32 custody hashes matched. Six disposable prior-worktree paths were remapped to the same clean base commit; contents matched exactly.
- Before/after import maps preserved all prior origins; all observed production origins were under genuine child `site-packages`.
- Agent marker `ba8f0bc8`; Runtime marker `f3208b26`; direct URLs, profile lock, archive, package lock, and ownership metadata matched.
- No `PYTHONPATH` production overlay, installed edit, metadata alias, or fabricated production owner path was found.
- Current worktree is clean; no product, test, or evidence files were changed.

Evidence reviewed: [StageB0551 evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-observed-qualified-0551/evidence/stage-b>).

Limits: this closes only the exact external-pack original. It does not assert a second original pass, whole-suite/full/gate results, or any body/child/host rerun. The earlier 0520 result-only PASS and 0612 pre-body FAIL remain preserved honestly.

Read-only verification used JSON, SHA-256, AST, origin-map, custody, and git status/diff checks. Runtime `contract/commit-v2.md` was used as the repository fallback; no v2 implementation acceptance is claimed.