# Capture projector and candidate forwarding: qualification

Scope: the pure optional `project_capture` provider method on `RuntimeCommitService`
(`astrid/sdk/timeline/commit.py`), the candidate forwarding in `tests/sdk/test_capture_source_runtime.py`,
and the golden against `managed_timeline._project_exact_parent_head`. No Agent-side attestation state and
no second projector.

Runtime: `/home/user/work/runtime`, branch `tl/integration`, at `4bb1d0f` (Runtime M1 integration).
Agent tree under test: `a677f1bc` (branch `tl/agt-m3-capture-paired-qualify`, on top of `3c382f4d`).

## Runs

Each run used the named suite `commit-integration` through `bin/request-test`, which runs
`env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py <file>`.
The two M1 tests in that command are the neighbour lane; they passed in every run.

| Run | Tree | `test_capture_source_runtime.py` | `test_timeline_capture_projection.py` |
|---|---|---|---|
| A: `3c382f4d` as committed | `ed203422` | 2 passed, 12 xfailed, 9 errors | 2 passed, 32 deselected, 9 errors |
| B: fixture order fixed | `a5d0dd0d` | 9 passed, 2 failed, 12 xfailed | 11 passed, 32 deselected |
| C: fixture + two candidate xfails (final) | `a677f1bc` | 9 passed, 14 xfailed | 11 passed, 32 deselected |

Run A's errors were the shared fixture: `publish_parent_composition` refused with
`tracked timeline publication requires a timeline command`. The fixture registered the commit provider
before `create_timeline`, and that bootstraps a tracked head. Run A's 12 forgery cases showed as `xfailed`
while that setup error was present, so the xfail said nothing about forgery. Their first real evidence is run C's probe below.

Probe (run D, temporary, removed from the design): a copy of the module with the `xfail` marker removed from the
12 forgery cases and the 2 candidate-certificate cases, run with the same command.
Result: `14 failed, 2 passed` (the 2 are the M1 neighbours). Every forgery failure is
`assert values.timeline_source is None`: Runtime admitted the changed config, registry, shot digest, or
authoring-preview candidate, and the host produced a `VerifiedTimelineSource`. Every candidate failure is
`DID NOT RAISE RuntimeErrorBase`: `create_task` accepted a working-copy marker with no candidate certificate.

## Fixture change (test setup only, no assertion changed)

- `open_source_runtime(tmp_path, before_provider=...)` in `test_capture_source_runtime.py` publishes the saved
  `parent-1` chain first, lets `before_provider` publish more untracked revisions, and only then registers the
  commit provider, capability and executor. Runtime's `register_timeline_commit_provider` installs an
  untracked head as a verified legacy baseline, so `parent-1` stays a saved revision for the capture tests.
- `test_timeline_capture_projection.py`: `publish_golden` publishes `parent-golden` inside `before_provider`.
  `saved_closure` only reads the closure afterwards through `commits.revision_closure`.

## Forgery cases: strict xfails kept (none passes)

The 12 cases of `test_arbitrary_capture_cannot_acquire_canonical_source` (field × inline × working_copy) still
fail when unmarked. Reason, unchanged: `Runtime admits changed capture content/pins as canonical source`.
Restored by Runtime verifying capture content (design/runtime-coordination.md "capture content certification").

## Candidate-certificate cases: new strict xfail (2 cases)

`test_missing_candidate_certificate_refuses_before_admission_writes[False|True]` expects Runtime to refuse a
working-copy capture with no candidate before any SQL, CAS or staging write. Current `tl/integration` accepts it.
Reason: `Runtime admits a working-copy capture without its candidate certificate`. Restored by Runtime's
candidate preflight, which lives in `rt-m3-capture-candidate-actual-pair` and is not yet on `tl/integration`.

## Golden

- `test_real_saved_entire_expansion_golden` (`tests/sdk/test_timeline_capture_projection.py`) asserts
  `project(document) == {"config", "registry", "expansion": {**expansion, "parent_content_digest"}}` with
  `expansion` taken from `_project_exact_parent_head`. The whole expansion is compared, including `graph`.
  No ignore list. It passes in run B and run C.
- `test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows` passes: only `created_at`
  and the duplicated parent manifest are excluded from the snapshot graph; `payload` and pins are kept.
- `test_real_candidate_matches_sdk_opener_exactly` passes for parent, child, new_shot, duplicate, remove and sdk_bundle.

## Not verified

- `ruff`/`mypy` were not run: direct local execution of tool binaries was denied in this sandbox.
- No full suite was requested (orchestrator rule for this brief).
- The `tests/sdk/test_zz_probe_forgery_unmarked.py` leftover is an empty placeholder. Local removal was denied,
  so the orchestrator should delete it before merge.
