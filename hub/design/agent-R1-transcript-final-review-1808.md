# R1/G2 final review: PASS

## Scope and identity

Reviewed candidate f98dbed881fb568584c1e7d3301f71a4dea8ca4e (tl/agt-R1-transcript-return-sol-1758) against Agent base 6531622c8, under PLAN §3 R1/G2/C0. The candidate diff is limited to the expected astrid/sdk/timeline/commit.py, astrid/sdk/timeline/_commit_patch.py, and the new tests/editing_conformance/test_commit_document_input_capture.py; no existing test body was changed.

The pinned Runtime execution source was 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d; runtime_protocol/timeline_commit_auth.py SHA-256 was 3b812936efaa35a165c056fbacee6d8e699d485ca912f12e11cc4cd4bbe8f2ef. The frozen vendor source commit remained 34eac0041b0891e9011966b39bcbd26053fde5bc.

## Security finding and review result

F1 is fixed. Normal _hydrate validates every Runtime-provided source against the exact pin, project, document identity, integer version, and content digest before changing the bundle. After validation it replaces, rather than extends, any caller-supplied _copy_manifest with the authenticated Runtime document dependency manifest. The consuming command still records the verified transcript dependency; the initial command does not consume it. Refused validation leaves the input bundle unchanged.

The production carrier is trusted, not a detached fake authority: RuntimeCommitService._load obtains the closure through the request-private RequestCommitPort.revision_closure, checks the returned project/timeline/revision identity, and bundle_from_document verifies the immutable closure. Transcript hydration then reads through the request-private transcript_source, whose Runtime port captures the exact scoped document from the store. Duplicate/inverse manifest installation remains separate and authenticated. There is no self-authenticated snapshot, equal-byte pin retarget, missing project/document/version/digest check, or partial mutation on refusal.

The exact F1 forged foreign-project/version-99/wrong-digest probe passed once. Existing source-copy/inverse behavior passed without changing the inverse path.

## Evidence and commands

Permanent evidence is at:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-final-review-1808/evidence/

The D21 observer was installed before Runtime test bodies and collected once. runtime-final-captures/report-all.json has 9/9 passing setup/call/teardown reports. The 9 private packets and 10 public packets preserve actual request/context, prepared records, private original/landing captures, source/transcript manifests, native commands, effect/binding data, SQL/head/history before and after, and module hashes before/after. Common module hashes did not change; the union contained 110 loaded modules. Public execution was 8 accepted and 2 refused; the exact retry and both refusals had no writes. Runtime refusal packets contain validation_error / invalid_records and unchanged SQL/head/history.

Exact targeted commands and results:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-a6665a0b53 /home/user/work/venv-agent/bin/python -m pytest -q -ra -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_document_input_capture.py --basetemp=/tmp/w-a6665a0b53/focused
    11 passed in 0.99s

Exact F1 forged-manifest probe (one run): PASS; caller foreign document/media absent after authenticated hydration.

    PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-a6665a0b53 /home/user/work/venv-agent/bin/python -m pytest -q -ra -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_retained_inputs_whole_undo_redo tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_captured_authority_still_guards_acceptance --basetemp=/tmp/w-a6665a0b53/strict-copy-inverse
    4 passed in 3.66s

    PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-R1-transcript-final-review-1808 RUNTIME_CAPTURE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-final-review-1808/evidence/runtime-final-captures PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-final-review-1808/evidence:/home/user/work/wt/rt-pin-2a9e347f:/home/user/work/wt/agt-R1-transcript-final-review-1808:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-a6665a0b53 /home/user/work/venv-agent/bin/python -m pytest -q -ra -o addopts= -p no:cacheprovider -p runtime_observer tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[None-True] tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[before-True] tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[late-source-True] --basetemp=/tmp/w-a6665a0b53/runtime-final
    3 passed in 55.59s

    python -m scripts.reshape.compare_ruff_baseline
    Ruff findings: current=2149 baseline=2149
    python -m scripts.reshape.compare_mypy_baseline
    Mypy findings: current=1912 baseline=1912
    python -m mypy astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py
    Success: no issues found in 2 source files
    python -m ruff check astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_commit_document_input_capture.py
    All checks passed!
    python scripts/vendor_lock.py check runtime.lock.json
    ok runtime.lock.json
    python scripts/artifact_manifest.py --check
    artifacts.json is current
    git diff --check
    pass

Evidence integrity: SHA256SUMS SHA-256 is fdae55d041e779a9714ada16e3f7385d7ea64f9a0a258693d6e21beb15a79f0a. The permanent credential scan reports 0 credential-like key paths and 0 credential-value matches.

## Limits and disposition

No full suite, original-nine/cohort/SDK-four, browser/HTTP/native journey, C271/14/85/40/281/58, P1-P4, or unrelated Runtime cases were run, per the brief. No Runtime/App/Composition/Git/pin/environment/daemon writes were made. Full C0 request and reply fields remain untouched by this candidate; no new merged/preview/structured-error qualification was claimed beyond the selected controls. No blocker or plan deviation found.

Recommended next step: manager may accept this review and merge the candidate through the Agent queue; retain the permanent evidence directory with the candidate provenance.

