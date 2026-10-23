# agt-V2-map-locality-audit-0616 — D12a readonly review

**FAIL: D12a locality.** Mounted production-provider probe refuses an
unrelated same-physical-image timing edit while an unchanged legacy
`source_window` map on `clip-a` remains untouched. The strict map mutation
negative refuses correctly.

Positive request: normal `doc.patch` set on
`internal-revision:internal-1/clips/id:clip-b/at`, 5 → 6; `merge=fields`,
`reads=[]`, current base `parent-1/bootstrap`, no optimistic merge. Actual
422 `validation_error` / `invalid_document`,
`candidate.timing: ('occ-a', 'chapter-shot', 'clip-a'): unsupported explicit
map source_window`; head unchanged, no receipt/prepared record.

Negative request: same fixture/base, set
`internal-revision:internal-1/clips/id:clip-a/source_window/to`, 30 → 31.
Actual 422 refusal, head unchanged.

Probe command: `PYTHONDONTWRITEBYTECODE=1 USE_REAL_RUNTIME=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/agt-V2-map-locality-audit-0616-probe.py`.

Caller: Runtime `load_timeline_commit_provider("astrid")` → factory
`astrid.sdk.timeline.commit.create_runtime_commit_service` →
`RuntimeCommitService.commit` → `commit.py:1119` final validation →
`validation.py:607` timing validation → `_commit_timing_validation.py:411-412`
retention gate. `_timing_basis` at line 275 fingerprints every clip in the
owner timeline, so unrelated `clip-b.at` changes the basis and prevents legacy
map retention. This is whole-timeline geometry overcount, not a causal map or
target dependency.

Runtime source: `/home/user/work/runtime`, HEAD
`85dafdf46742b02ae5e4a300656cd6f5d68f0d4d`; Agent modules resolve inside the
assigned worktree.

Checks: targeted D12/P1 pytest **47 passed**; changed-file Ruff **pass**;
private mypy **pass**; `make ruff` **2150/2150**; mypy ratchet **1915/1915**;
vendor lock **ok**; artifact manifest current; `git diff --check` **pass**.

Owner treatment: narrow retention to the declaration/actual-target dependency
closure while keeping map/target writes strict; rerun both mounted probes.
