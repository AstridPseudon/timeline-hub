Completed the observer-only capture on Agent `9cd3dbe8` + Runtime `2b49da8d`: **2 passed in 20.90s**, in exactly one diagnostic run.

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider -p source_copy_observer --timeout=60 --tb=short \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo \
  tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_retained_inputs_whole_undo_redo
```

Exact environment and source paths: [command.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-source-copy-capture-sol-0502/evidence/command.json).

- Preserved both previous instrumentation failures and recovered the exact 0454 observer. Its partial trace lacked completed inverse acceptance, requiring the authorized run.
- Synthetic preflight passed **400 signature/value/result/exception cases**, plus guard tracing and intentional serialization-failure checks.
- Captured **54 original guards**, four accepted inverse operations, full prepared records, replies, history, manifests and scoped store snapshots. Actual production calls forwarded the **same authenticated `SelectedRecords` object** through `apply_inverse → CommitPatch.after → inverse_closure`. Native/effect ranges were `[0,3)` / `[0,4)`.
- Source and test-body hashes matched before/after. No real-run logger exception occurred. `git diff --check` passed; worktree remains clean. No product, test, guard or shared-environment changes.

Capture limits are explicit: ordinal-keyed auxiliary maps and opaque iterator/callback contents are incomplete; media file bytes were not exported. Fixtures retain their original no-op authorization callbacks, so this does not qualify HTTP/bearer authentication. Merged/conflict/invalid replies remain untested.

Detailed evidence and limitations: [capture-summary.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-source-copy-capture-sol-0502/evidence/capture-summary.json).

No current product failure was reproduced, so no source fix is justified by this run. Return the bounded green capture to the orchestrator; any remaining inverse defect belongs in a separate Agent R1/R2 author task. Nothing blocked. Commit message and `DONE` written.