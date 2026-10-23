# U2b inventory merge resolution

Worker: `agt-U2b-inventory-sol-1042`. Base: `6c3d9264564bd533995e35c2b8f1f44bb1161cf6`.

## Change and causal evidence

The only worktree change deletes `tests/test_runtime_correctness_inventory.py`
(125 lines), following the actual upstream deletion. There is no coverage port:
all four tests assert properties of a retired documentation inventory, not
product behavior. No active behavior expectation is removed or rewritten.

Read PLAN.md and the independent 1019, return 1026, and independent final 1034
reports before choosing the resolution. Inspected the actual relevant blobs
and diffs:

- `d90c6818b6e11e3a437ab9d6041ab02c2cb45df2` legitimately retired the completed
  inventory document. Its parent document blob was
  `257fa69a8d002349fcee51fcb7d454e10d6d4360`; its final deferred-ticket section
  says `None`, and the four planned assert conversions are marked completed.
- `310fce540` subsequently added a missing-document skip to the stale test.
- `ef851b22c` and `f9e58fbdb^` have the identical inventory-test blob
  `34fcdb898a8d081be35501d751923a6b8cdab697`, including that skip.
- Upstream `f9e58fbdb6def0339cccea9d768f482e19223af3` explicitly deletes this
  test as dead because its document was removed by `d90c6818b` and every test
  skipped. Both this test and its document are absent at `f9e58fbdb` and at
  the merged upstream tip `74f3f7edb`.
- Merge `55c1e7aa7` retained the obsolete test and changed only the
  missing-document skip to a failure, plus an EOF blank line. Return `6c3d92645`
  removed the blank line; its retained test blob is
  `f6d3cfde5cf2241b2bcb861ba43e97ed8bce5114`.

The four assertions checked AST rows against the document, lexical grep counts
against the document, documentation status/reason/ticket formatting, and the
document's completed-conversion list. None invoked the four formerly referenced
product sites. Those historic source paths no longer exist in the current
tree; repository searches find no other surviving M3 inventory/ticket promise.
Inventing a new broad source policy would add a requirement rather than
preserve behavior. Following upstream's deletion preserves both the deliberate
documentation retirement and the no-invisible-skips policy. It does not restore
the document, a skip, or a fake-green replacement.

## Collection and current coverage

Before deletion:

```
/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest --collect-only -q tests/test_runtime_correctness_inventory.py tests/test_lanes.py tests/test_lane_registry.py tests/test_skip_policy.py tests/test_skip_guard.py tests/packs/runpod/test_worker_process.py
```

Result: **103 collected**. After deletion, the identical command with only the
deleted filename omitted collected **99**. A set comparison of the node IDs
confirms exactly the four inventory nodes removed, zero new nodes, and every
other node retained. Neither collection has a skip, deselection, or suppressed
module report. Current node counts:

| File | Nodes |
| --- | ---: |
| `tests/test_lanes.py` | 5 |
| `tests/test_lane_registry.py` | 13 |
| `tests/test_skip_policy.py` | 13 |
| `tests/test_skip_guard.py` | 24 |
| `tests/packs/runpod/test_worker_process.py` | 44 |

The document and inventory test are both absent in the working tree. Collection
logs and the node-set comparison are in the worker scratch directory.

## Validation

All commands run from `/home/user/work/wt/agt-U2b-inventory-sol-1042` with
`PYTHONDONTWRITEBYTECODE=1`. The dispatcher-provided `workers/.../tmpdir` is a
text pointer to `/tmp/w-8d046da1d4`, also the existing `$TMPDIR`; logs and tool
caches use that assigned scratch directory. No shared install was modified.

Required acceptance command:

```
/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q tests/test_lanes.py tests/test_lane_registry.py tests/test_skip_policy.py tests/test_skip_guard.py tests/packs/runpod/test_worker_process.py
```

Result: pending; run is still active after 89 completed nodes, near the RunPod
adapter test. This report will be finalized with the actual outcome.

Other commands and results:

- `RUFF_CACHE_DIR="$TMPDIR/ruff-cache" make PY=/home/user/work/venv-agent/bin/python ruff` — exit 0, **2149/2149** findings.
- `MYPY_CACHE_DIR="$TMPDIR/mypy-cache" make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — exit 0, **1912/1912** findings.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — `ok runtime.lock.json`.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — `artifacts.json is current`.
- `/home/user/work/venv-agent/bin/python scripts/reshape/check_repo_hygiene.py` — exit 0.
- `git diff --check` and `git diff --check ef851b22c` — pass.
- `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python -m pytest -q tests/editing_conformance/test_compile_contracts.py::test_audio_vector tests/editing_conformance/test_compile_contracts.py::test_visual_vector` — exit 1, **22 passed, 2 failed**, no skips or deselections. The original `fade-in-needs-prepared-envelope-source` and `fade-out-needs-prepared-envelope-source` positives remain visibly failing at the original `audio.render_source` expectation. No D14 file or assertion was changed.

Requester port unchanged: reused independent final review 1034's **2 passed,
11 deselected** evidence for the two selected requester/legacy-admission
tests, as explicitly permitted by the brief. Did not rerun or modify that port.
All caller/request/reply contract coverage remains byte-identical to the base;
this task does not claim new production contract qualification.

## Protected scope and ancestry

`git diff --exit-code ef851b22c -- runtime.lock.json astrid_runtime_client astrid/core/timeline/schema remotion/package.json remotion/package-lock.json remotion/artifacts`
passes. Policy/guard files, all editing-conformance files, and the requester
publication test also compare byte-identical against the task base/HEAD.

- Runtime lock source: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Edit-command schema SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Pinned Composition tarball SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- `git merge-base --is-ancestor 74f3f7edba35230d0a01824eae7b663143e6aa5b HEAD` passes; locally available `origin/main` is exactly that commit. No fetch or Git mutation performed; remote freshness remains the lead's responsibility.
- Final source delta is exactly one named test deletion. No product, policy,
  schema/client/pin, Composition, environment, or service edits.

Not run: full suite, HTTP/browser/live-socket suites, native 14/58 suites,
environment installs, or daemons. No automatic approval/safety denial occurred.

## Disposition

Pending the required acceptance command. The scoped merge resolution is
source-backed. The unrelated D14 positives remain red and need their existing
owner's implementation work; they were not waived here.
