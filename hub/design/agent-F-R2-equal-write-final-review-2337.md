## PASS — cumulative R2 review

Reviewed `c36ca8c94 → d7db17a60 → 97ce625cfc9f6434776d91474595e77cb22af1a`.

- d7 alone reproduces the prior missing-internal-binding failure (`inverse UNEXPECTED_ACCEPT False`).
- 97ce adds complete, unique materialization validation against authenticated execution boundaries.
- Cumulative scope is exactly:
  - `astrid/sdk/timeline/inverse.py`
  - `tests/sdk/test_timeline_inverse_fork_guard.py`
- Final `inverse.py` SHA256: `2491a97d9c9cf262834d12524eb7935312ae24ff6afa5f258883f18633d570b1`.

Tests, using the pinned runtime/venv:

- Fork/original regression: **31 passed**
- Scalar provider lane: **45 passed**
- Immediate negatives: **16 passed**
- History/root/ABA controls: **8 passed**
- Four child-scope graph cases: **4 passed**
- No skips or xfails.

Quality checks passed:

```text
ruff check --no-cache
mypy --follow-imports=silent --no-incremental
vendor_lock.py check --producer rt-pin-34eac004
artifact_manifest.py --check
git diff --check
```

Current-tree public Runtime probe passed: accepted/merged replies, explicit steps/patch/reads, preview null receipt with no writes, canonical history readback, and selected undo refusal with no writes.

`_commit_patch.py` and `_root_inverse.py` are unchanged from c36. The retained-sibling `binding_changed` ambiguity is pre-existing and remains a separate follow-up, not a regression from this patch.

No full suite was run; run 25691 remains untouched. No blockers. DONE marker and commit message were written.