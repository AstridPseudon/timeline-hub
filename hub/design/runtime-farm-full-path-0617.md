## Result

Source-only investigation completed. Runtime worktree remains clean at `1d9ddba546f8fb1300f55ff62607ed492719cbaa`; no product edits, tests, Store actions, dispatcher actions, installs, or network work were performed.

The corrected literal recipe plus a genuine receipt is mechanically sufficient for the existing lease path, but packet `1a1ccab` is not yet publishable:

- Production selection is `request-test:10,13-15` → `test-run:15`; `request-test` only queues and does not render receipt values.
- `test-run:54-73` validates the exact row, calls `Store.names_for_suite`, then `Store.acquire`; `test-run:94,101-103` passes lease FDs to the child.
- Snapshot execution occurs at `test-run:194-205`.
- Packet fixtures manually replace the row and call `names_for_suite` (`test_farm_agent_full.py:106-128`); they do not exercise production extraction or `Store.acquire`.
- The candidate row still contains unresolved `${FARM_RECEIPT_MANAGED_PROFILE}` and omits `ASTRID_TEST_NODE_MODULES` and npm `10.8.2` preflight.

A reachable child-import seam remains to qualify. Agent’s sanitizer (`subprocess_env.py:57-72,90-123,167-208`) does not retain arbitrary `PYTHONPATH` or `ASTRID_RUNTIME_CHECKOUT`; generic-host worker variants reconstruct `PYTHONPATH` only on specific routes (`generic_host.py:1837-1907`). Therefore xdist-origin evidence alone does not prove sanitized generic-host children import the selected Runtime. A genuine receipt must capture parent and sanitized-child origins.

Runtime source identity is explicit:

- Runtime `1d9ddba5` contains `runtime_protocol/external_pack_sources.py`; Runtime `45c3a7f` does not.
- All four canonical client hashes remain equal.
- The prior `288 failed / 17,335 passed / 187 setup errors` checkpoint used Runtime `45c3a7f`; it cannot establish the original cause or attribute all timeline failures to environment handling.

Required Farm receipts/source facts:

- Authenticated Agent/Runtime revisions and trees, including `external_pack_sources.py` hash and four client hashes.
- Managed profile path, peer `node_modules` path, `ASTRID_TEST_NODE_MODULES`, Node `v20.19.4`, npm `10.8.2`, lock/archive/composition/schema facts.
- Existing Store owner/index/mutex identity, registration report/dependencies, and exact pre/post full-row plus outside-byte preservation.
- Production `test-run` evidence showing row extraction, `names_for_suite`, `acquire`, lease FDs, snapshot, parent imports, and sanitized-child imports.

Tests: none run, as explicitly prohibited by the task. Source inspection commands completed successfully, including `git show`, `git grep`, `git diff --stat`, `nl`, and worktree status checks.

Commit message written and `DONE` marker created at the assigned worker paths.