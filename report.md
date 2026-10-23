# V2 bounded D12a locality audit — agt-V2-map-locality-audit-0616

## Disposition

**FAIL for D12a locality.** The strict negative is correct, but the required
positive production-provider counterexample is refused. No product files,
tests, fixtures, schemas, pins, or generated files were changed by this audit.

The failure is an over-counted timing basis, not an affected dependency:
the request writes only an unrelated clip's `at` field while the retained
legacy `source_window` map, its declaration, and its source/target inputs are
untouched.

## Bounded production probes

Source fixture and normal engine: `legacy_document("map")` from
`tests/editing_conformance/test_commit_boundaries_d12.py`, submitted through
`tests.sdk.test_p1_doc_patch_provider._service_call`, the existing
`DetachedRealm`/`DetachedPort`, and `doc.patch` normal command execution.
The probe used the mounted Runtime provider loader (`astrid`) at Runtime
worktree HEAD `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d`.

Exact probe command (both cases run in one ephemeral script):

`PYTHONDONTWRITEBYTECODE=1 USE_REAL_RUNTIME=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/agt-V2-map-locality-audit-0616-probe.py`

1. Positive locality case — **FAIL**

   - Request: `doc.patch`, `ref=internal-revision:internal-1`,
     `path=["clips", "id:clip-b", "at"]`, `before=5`, `value=6`.
   - `merge="fields"`, request `reads=[]`, step `reads=[]`, current base
     `revision_id=parent-1`, `publication_id=bootstrap`; no optimistic merge
     or stale-base path.
   - The map-bearing `clip-a` and `source_window={"from":20,"to":30}` were
     not addressed. The request has no causal read of that declaration or its
     target.
   - Actual result: HTTP 422 `validation_error`, details
     `status=invalid`, `reason/code=invalid_document`, empty path,
     message `candidate.timing: ('occ-a', 'chapter-shot', 'clip-a'):
     unsupported explicit map source_window`.
   - Head remained `parent-1/bootstrap`; accepted and prepared counts were 0.

2. Negative strictness case — **PASS**

   - Request: `doc.patch`, same retained fixture/base, changing the map itself:
     `ref=internal-revision:internal-1`,
     `path=["clips", "id:clip-a", "source_window", "to"]`, `before=30`,
     `value=31`.
   - Actual result: the same 422 `invalid_document` refusal; no receipt,
     accepted publication, or head change.

The positive request is independently a valid guarded field patch and reaches
the production final-validation boundary. Its refusal is therefore not a
malformed request or a legitimate map-target conflict.

## Caller trace and cause

Mounted caller:

`runtime_protocol.timeline_commit_provider.load_timeline_commit_provider("astrid")`
→ factory `astrid.sdk.timeline.commit.create_runtime_commit_service`
→ `RuntimeCommitService.commit`
→ `validate_final_candidate(..., baseline=...)` at
`astrid/sdk/timeline/commit.py:1119`
→ `validate_candidate_timing` at
`astrid/sdk/timeline/validation.py:607`
→ unsupported-map retention check at
`astrid/sdk/timeline/_commit_timing_validation.py:411-412`.

The retention gate compares `_timing_basis(candidate)` with the baseline.
`_timing_basis` at `_commit_timing_validation.py:275` fingerprints every clip
in each physical timeline via `_reference_shape`; changing unrelated
`clip-b.at` therefore changes the whole owner basis. The equality gate does
not fire, and the compiler's retained `source_window` error is returned.
This distinguishes whole-document/same-image geometry overcount from a real
write or dependency on `clip-a`'s map.

Import origins used by the mounted probe:

- `runtime_protocol`: `/home/user/work/runtime/runtime_protocol/__init__.py`
- `runtime_protocol.timeline_commit_provider`:
  `/home/user/work/runtime/runtime_protocol/timeline_commit_provider.py`
- mounted provider: `astrid.sdk.timeline.commit.RuntimeCommitService`
- `commit.py`, `validation.py`, `_commit_timing_validation.py`: this assigned
  worktree

## Checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_boundaries_d12.py tests/sdk/test_p1_doc_patch_provider.py` — **47 passed**.
- Scoped Ruff on `astrid/sdk/timeline/validation.py`,
  `astrid/sdk/timeline/_commit_timing_validation.py`, and
  `tests/editing_conformance/test_commit_boundaries_d12.py` — **All checks passed**.
- Scoped mypy with `/home/user/work/venv-agent-typecheck-v2/bin/python` and
  `--follow-imports=skip` — **Success: no issues found**.
- `make ruff PY=/home/user/work/venv-agent/bin/python` — **current=2150,
  baseline=2150; pass**.
- `scripts.reshape.compare_mypy_baseline` — **current=1915,
  baseline=1915; pass**.
- `scripts/vendor_lock.py check runtime.lock.json` — **ok**.
- `scripts/artifact_manifest.py --check` — **artifacts.json is current**.
- `git diff --check` — **pass**.

An initial pytest invocation without the Runtime source on `PYTHONPATH` failed
at collection with `ModuleNotFoundError: runtime_protocol`; the exact command
above supplies the existing Runtime worktree and is the qualifying result.
A broader Ruff invocation including `tests/sdk/test_p1_doc_patch_provider.py`
reported four pre-existing F811 fixture-parameter findings; the changed-file
scope is clean.

## Readonly review status

| Review | Status |
|---|---|
| Production caller exercised | PASS |
| Unchanged legacy map survives unrelated same-image timing edit | **FAIL** |
| Map mutation remains refused | PASS |
| Atomic/current-base/optimistic-merge guards preserved in probe | PASS |
| Product implementation changed | PASS (none) |

## Owner action

Existing owner should narrow D12a's retained-legacy comparison to the changed
declaration/actual target closure (or equivalent dependency-local timing basis),
while retaining strict refusal for map/target writes and preserving all
request/reply metadata. Re-run the same mounted positive and negative probes
after the correction. No implementation was attempted here per the audit
brief.
