# R1 integrated mirror proof — PASS

Integrated HEAD `d462103985e3d4c4591ed76c5d5f261b2398fb36`, tree `eee66dc206817b16f0621087a12505389ec41630`. Reviewed source `b8e5076250cc37cadf88c1ce699f2a05511fb909` has the same tree. Relative to integrated base `e49a6e76b3ab363e312c55b313714af1f845f54b`, exactly two paths differ: `astrid/sdk/timeline/_doc_patch.py` and `tests/editing_conformance/test_doc_patch_mirrors.py`.

Exact blob equality:

```text
_doc_patch.py                  e780e7abf3baf7aca1315fbc8a54c3a9e13feef2
test_doc_patch_mirrors.py      d2c0e15105256cba5867cf509bd1df2e533759da
```

The integrated targeted command passed `219 passed in 15.81s`. `git diff --check`, vendor-lock check, and artifact-manifest check passed. Reviewed-tree quality evidence is reused exactly: Ruff `2149/2149`, Mypy `1912/1912`.

Import origins were the integrated Agent worktree for `astrid.sdk.timeline.commands`, `_doc_patch`, and `commit`; Runtime authentication was `/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py`. No source or metadata changes were made. No original P1 HTTP replay is claimed; R2 separately owns the pre-existing split-insert inverse limitation.
