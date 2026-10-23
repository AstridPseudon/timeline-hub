# R1 integrated transcript proof: PASS

## Identity and tree reuse

This was a readonly proof on Agent commit `440cc1e702c3967a4f95d89c44b462f9c14a750f`, requested against base `440cc1e702c3967a4f95d89c44b462f9c14a750f`. The current tree is `60445c9c3aca520d2e6144fd95672a61a7603aa5`, exactly equal to reviewed current commit `f078d02297dd136b9d02850cfbdcfa15abaf8789` (same tree and `git diff` empty).

The merge delta is exactly the reviewed three-path R1 port:

```text
M astrid/sdk/timeline/_commit_patch.py
M astrid/sdk/timeline/commit.py
A tests/editing_conformance/test_commit_document_input_capture.py
```

Protected registry, A4 witness, inverse, timing/validation, final-validation tests, `runtime.lock.json`, and `artifacts.json` blobs are unchanged from the merge parent. The prior quality ratchets are therefore reused by exact-tree identity: Ruff `2149/2149` and mypy `1912/1912`, with no source edits in this proof.

## Pinned Runtime proof

The one permitted genuine Runtime run used the existing Runtime checkout `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, the existing `venv-agent`, the normal public service/provider/store fixtures, and the Agent source from this worktree. `runtime_protocol/timeline_commit_auth.py` SHA-256 was `3b812936efaa35a165c056fbacee6d8e699d485ca912f12e11cc4cd4bbe8f2ef`.

The prepared final-review observer was reused byte-for-byte (SHA-256 `6a4c2e0a1360e9d9fc0a689f9bf998da6bf6464c77006281a10c9eff84913aed`). Its output root was preflighted before test collection and was this worker's permanent `evidence/` directory. The observer wrote actual context/request/prepared/private carrier data, source and transcript manifests, native command records, effect/write and binding records, SQL/head/history before and after, and module hashes before and after.

Exact corrected command:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-R1-transcript-integrated-1818 RUNTIME_CAPTURE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-integrated-1818/evidence PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-integrated-1818/evidence:/home/user/work/wt/rt-pin-2a9e347f:/home/user/work/wt/agt-R1-transcript-integrated-1818:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-ef8b9b17fc timeout 900s /home/user/work/venv-agent/bin/python -m pytest -q -ra -o addopts= -p no:cacheprovider -p runtime_observer --timeout=25 tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[None-True] tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[before-True] tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[late-source-True] --basetemp=/tmp/w-ef8b9b17fc/r1-transcript-integrated-runtime
```

Result: `3 passed in 55.46s`. A preceding selector-order typo collected zero tests and executed no body; it is retained as `runtime-test.log` and was not a test-body rerun.

The permanent capture packet contains 9 private Runtime-port packets and 10 public service packets. The exact positive path has an accepted canonical transcript dependency manifest. The exact retry returns an identical full reply and leaves SQL/head/history unchanged. Both strict tamper cases (`before`, `late-source`) return `validation_error` / `invalid_records` and leave SQL/head/history unchanged. All 9 setup/call/teardown reports passed. Common module hashes were unchanged; observed Agent and Runtime module paths resolved only under the own Agent worktree and pinned Runtime checkout.

Full C0 request fields are present in every captured request. Accepted packets retain the full `{data, receipt}` shape, canonical document, records/steps, bindings/effects/dependencies, and history snapshots. The selected run does not newly exercise dry-run preview/null receipt or every structured-error path/hint field; those remain source-preserved by the exact reviewed tree and are not claimed as newly tested here.

## Evidence and limits

Permanent evidence is in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-integrated-1818/evidence/`

It includes the bounded flat capture packet, preflight/source identity, corrected and zero-test logs, tree audit, `capture-summary.json`, `credential-scan.json`, and `SHA256SUMS`. Credential scan result: zero credential-like key paths and zero credential-value matches.

No source, test, Git ref, Runtime checkout, environment, daemon, pin, merge, deletion, or shared dependency was modified. No full suite, browser, HTTP/socket, native journey, SDK-four, cohort, or unrelated Runtime lane was run. No blocker or plan deviation was found.
