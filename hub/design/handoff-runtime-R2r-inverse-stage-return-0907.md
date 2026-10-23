# Runtime R2r inverse-stage return handoff

Status: **PASS for the named Runtime acceptance; bounded Agent-dependent
qualification remains unverified.**

## Tree and ownership

- Worker tree: `/home/user/work/wt/rt-R2r-inverse-stage-return-0907`
- Base: `a01e9d806` (`tl/integration`), with `7ca1a2278` an ancestor.
- Author source read: `a7448678786ea9d2b7e223c76760069595d1a505` via `git show`;
  it was not merged or used as branch ancestry.
- Changed product files: `runtime_protocol/timeline_commit_auth.py`,
  `runtime_protocol/timeline_commit_store.py`.
- Changed test file: `tests/test_timeline_inverse_stage_authentication.py`.
- No Agent/schema/client/pin/config/fixture changes.

## Caller and authenticated history seam

Normal production path is `RuntimeService.commit_timeline` → commit
coordinator → `RequestCommitPort.accept` → `TimelineCommitStore._validate` →
`timeline_commit_auth.validate`. Durable replay/listing reaches
`TimelineCommitStore._verify_accepted`, which invokes the same auth validator.

The store uses its existing authenticated APIs:

- `history_entry(project_id, timeline_id, publication_id)` verifies the
  immutable receipt and event chain and returns source `records`;
- `revision_closure` supplies authenticated source/landing images;
- `_binding_continuations` supplies existing physical continuation edges;
- new `_inverse_stage_history` is only a handoff of verified `history_entry`
  values and rejects missing targets with `history_unavailable`.

Auth binds stage publication identity to exact `records.undo_of`, selected
source step identity to `records.steps`, command ordinals to the source step's
actual partition, and stage ref/policy/dependencies to the producer's fixed
stage contract. Native range lengths include source writes and the existing
word-cache derived writes; effect ranges remain the exact chronological
partition and are still checked against authenticated intermediate images,
native writes, final output, physical refs, digests, and revisions.

## Evidence

Exact required command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py
```

Result: **100 passed in 20.46s**.

The inverse-stage test has 15 real-store cases: one accepted target/inverse
with history replay, effect-image tampering, range tampering, missing binding,
wrong publication, selected step, command ordinal, native range, stage ref,
policy, dependency, and missing-history refusal.

Bounded related command:

```text
... pytest ... tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_integration.py -k 'inverse or history'
```

Result: **5 passed, 5 setup errors, 68 deselected**. Errors are the existing
Agent checkout setup assertion for missing `/home/user/work/wt/astrid`; no
Agent matrix or integrated qualification is claimed.

Compile, AST parse, and `git diff --check` passed. Ruff passes on auth and the
new test. Runtime store Ruff retains the exact parent baseline's 11 diagnostics;
Pyright auth is zero-diagnostic and store output is baseline-only.

## Limits / next step

No full, HTTP, browser, live socket, native14, crash24, or original Agent 58
matrix run was authorized. The orchestrator should merge through the Runtime
queue, then rerun the bounded integrated Agent/Runtime inverse matrix when the
Agent checkout is available. The worker commit message is in the requested
commit-msg path; `DONE` is created after final status verification.
