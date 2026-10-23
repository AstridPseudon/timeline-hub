# U2b final independent review — PASS

## Verdict

PASS for the cumulative U2b candidate at `c64b900a21062789c01673c0a033b236bcda0eeb`, tree
`3020d0a43a6174b627bef13a5337d06ed1e40881`. The sanctioned central acceptance passed
99/99 tests. The current candidate resolves the four obsolete inventory-test failures by
following upstream's deletion; it does not restore the retired inventory document, add a
policy waiver, or alter product behavior.

## Provenance reviewed

The complete upstream ancestry is present and live-tip ancestry is proven by
`git merge-base --is-ancestor 74f3f7edba35230d0a01824eae7b663143e6aa5b HEAD`:

1. `f9e58fbdb6def0339cccea9d768f482e19223af3` — no-invisible-skips lane registry and guard.
2. `feddcebad238b37ccfd8211c8466a557bc709b3e` — fail when no test passes.
3. `ecbef248423384231d7ebb8f4e5cd28cf4e2de83` — Darwin collection, Node 24 shards, POSIX lane declarations.
4. `3a8c47f41d1e66631084ace88b6901183b5d034e` — clean-install schema check and journey giant-file row.
5. `a08912dd312ec97fdfbf6a6bbdbedef6f1be0a56` — named lane deselection/import reporting and pinned shards.
6. `6ebf2921ddecac85d480f99c78f00bf90e0742c2` — lane-only left-out attribution and Darwin Node version.
7. `74f3f7edba35230d0a01824eae7b663143e6aa5b` — Remotion launch proof and real product-tree guard.

Every U2b-owned commit was reviewed:

- `55c1e7aa782239ce8001ea0b6cf7d2795c6d1c89`, merge of `ef851b22c` and upstream `74f3f7edb`, introduced the upstream policy merge result and the temporary stale inventory-test retention.
- `6c3d9264564bd533995e35c2b8f1f44bb1161cf6`, parent `55c1e7aa7`, removed the three tracked `.pyc` files and orphan inspector test, repaired EOF whitespace, and ported the stale publication assertion. Its inventory change was whitespace-only.
- `c64b900a21062789c01673c0a033b236bcda0eeb`, parent `6c3d92645`, deletes only `tests/test_runtime_correctness_inventory.py`.

No stale 1034-only or other-worker WIP ancestry was imported. The current commit's
product-source delta is empty; its sole path delta is the named test deletion.

## Inventory causality and coverage

The document `docs/runtime-correctness-m3-inventory.md` was legitimately retired by
`d90c6818b`; its completed inventory had no deferred ticket remaining. Upstream
`f9e58fbdb` explicitly deleted the document-only test because both the document and its
tested source inventory were retired. The merge `55c1e7aa7` retained that parent test
while the no-invisible-skips policy changed its missing-document behavior from skip to
failure. The return `6c3d92645` did not create or hide that failure. The solution commit
therefore matches upstream intent exactly.

The prior collection comparison, reused because this review made no test-source change,
was 103 nodes before deletion and 99 after, with exactly the four inventory nodes removed
and no other node changes. Current acceptance-file accounting is:

| File | Nodes |
| --- | ---: |
| `tests/test_lanes.py` | 5 |
| `tests/test_lane_registry.py` | 13 |
| `tests/test_skip_policy.py` | 13 |
| `tests/test_skip_guard.py` | 24 |
| `tests/packs/runpod/test_worker_process.py` | 44 |
| **Total** | **99** |

The acceptance command used default pytest selection, with no `-m` bypass and no
`--deselect`; it reported 99 passed, zero skipped, and zero deselected. Pass count is
strictly greater than zero. No new launcher, guard, registry, test, environment, or
contract edit was made.

## Central acceptance

One and only one allow-list row was added to `ORCH/tests/suites.conf`:

```text
agent u2b-policy-runpod-1053 env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" timeout 180 /home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q tests/test_lanes.py tests/test_lane_registry.py tests/test_skip_policy.py tests/test_skip_guard.py tests/packs/runpod/test_worker_process.py
```

Exact request and wait commands:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-U2b-inventory-final-review-1053 u2b-policy-runpod-1053
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-U2b-inventory-final-review-1053-u2b-policy-runpod-1053-1023105524-22522 10
```

Result: **PASS, 99 passed in 24.25s, exit 0**, central tree
`3020d0a43a6174b627bef13a5337d06ed1e40881`; service wall time 26s. The prior blocked
worker's async probe was not rerun, and no unchanged retry or second submission was made.

## Preservation checks

Read-only checks passed:

- `git diff --check ef851b22c..HEAD`.
- `git merge-base --is-ancestor 74f3f7edb HEAD`.
- no tracked `.pyc` or `__pycache__` paths.
- current parent-to-HEAD diff is exactly `D tests/test_runtime_correctness_inventory.py`.
- D14 original audio compile-contract cases remain visible and byte-identical from the
  solution parent, including both prepared-envelope expectations and their existing
  rationale. No D14 test was skipped, deleted, or rewritten. The known two D14 positives
  remain outside this task's acceptance and were not rerun here.
- `runtime.lock.json` still names source commit
  `34eac0041b0891e9011966b39bcbd26053fde5bc` and contains 15 files.
- edit-command schema SHA-256 remains
  `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- frozen Composition artifact
  `remotion/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`
  remains SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- the current 0.0.14 artifact is also unchanged at SHA-256
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`.

No full suite, HTTP/live-socket, browser, native 14/58, daemon, render-20, or duplicate
acceptance run was performed. No shared dependency or other worktree was modified.

## Recommendation

Accept the U2b inventory resolution and merge through the normal orchestrator queue.
Retain the D14 visible failures and the separate prepared-envelope follow-up; do not
restore the retired document/test or weaken the no-invisible-skips policy.
