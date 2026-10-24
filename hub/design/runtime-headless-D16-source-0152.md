**Blocked; not ready to merge.** Only the allowed test file changed. Wrote `commit-msg` and `BLOCKED`; no `DONE`.

| Original operation | Final mapping/result |
|---|---|
| Authored/empty historical shell publication | Original request submitted unchanged; earlier 410 refusal; SQL/raw payload/null publication/no-write assertions retained. Passed. |
| Hidden-content publication | Original fixture request and public null-head assertion restored; stored content/retry/no-write retained. Passed. |
| Four scoped-state variants | Original setup and publication request retained; earlier 410/retry/no-write checks passed. |
| Fresh/genuinely empty creation | Supported bootstrap with real revision/publication pins. Passed. |
| Secondary creation/retry | Preserved. Passed. |
| CAS-correct authored republish | Uses original `AUTHORED` fields through guarded patches and the real provider. **Failed.** |

The exact blocker is `parent_revision.payload.registry.assets.a.object_id = "x"`. On valid bootstrap pins, Agent rejects it as `dependency_changed`: “patch references media outside Runtime-verified inputs.” See [_doc_patch.py:313](/home/user/work/agent/astrid/sdk/timeline/_doc_patch.py:313). Runtime’s media carrier requires SHA-256 identities; the original literal `"x"` cannot supply that pin.

The accepted expectation remains intact. Its downstream receipt/event/history/closure/digest/exact-retry assertions remain present but **unverified**. No fake provider, fabricated history, or production changes were introduced.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_headless_overwrite_refused.py` — **11 passed, 1 failed**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache` on original and final files — passed.
- `/root/.local/bin/pyright --project "$TMPDIR/headless-d16-checks/pyrightconfig.json" --pythonpath /home/user/work/venv-runtime/bin/python --outputjson` on separate original/final copies — original **4**, final **0** diagnostics; **zero new identities or multiplicities**.
- In-memory compilation and `git diff --check` — passed.
- AST comparison confirmed unchanged original fixtures, historical SQL helpers, and legacy empty-publication request. All original test identities remain.
- No full/browser/gate runs.

Sources: Runtime `2c3a539895`, original `458595850`, Agent `521c888023`.

D16 coverage proves **earlier retirement refusal**, not the removed `stale_head` or `headless_content_not_empty` implementation. Next step: manager resolution of the exact original media-field/carrier mismatch.