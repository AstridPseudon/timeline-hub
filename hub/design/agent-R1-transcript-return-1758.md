# R1 immutable-capture return 1758

Fixed F1 on the required Agent base `eb2f3eb161a1435cba1e8516b27d0bd37e108331`, not integration. Only `astrid/sdk/timeline/commit.py` and `tests/editing_conformance/test_commit_document_input_capture.py` changed. Candidate requires a new independent review; no merge was performed or recommended before that review.

## Source finding and repair

The failed review was correct: `_hydrate` retained a supplied `_copy_manifest` through `setdefault`, and the recorder appended genuine consumed pins to that untrusted manifest. The exact `transcript:foreign-project:media:source`, version 99, digest `sha256:` plus 64 `f` characters survived into the compiled output before this repair.

Normal hydration now replaces an existing manifest, or initializes one for newly requested inputs, using only `_runtime_document.dependency_manifest`, after source validation succeeds. Existing immutable source pins and retained media remain. The initial-input/causal-consumption correction and `_commit_patch.py` are unchanged. Duplicate and inverse handlers still install their authenticated manifests during execution; four direct controls cover those paths, including retained documents/media through whole undo/redo and source authority damage. No blanket filtering of legitimate source-copy documents was added.

The mounted production boundary is `RuntimeService.commit_timeline` → request-private `RequestCommitPort.revision_closure` / `transcript_source` (`_document` → `capture_document_input`) → Agent `RuntimeCommitService` / `_load` / `bundle_from_document` / `_hydrate`. The port verifies the exact accepted base pair and scopes source reads to the authenticated project. `_runtime_document` comes from this closure. Internal `document_from_bundle` still consumes execution-installed duplicate/inverse manifests; it is not a public admission interface. Direct detached helper tests establish the F1 regression only; the separate public Runtime service/provider/store tests below establish real acceptance and rollback behavior. No HTTP/browser/daemon claim is made.

## Commands and results

Exact commands, selectors, environment values, and working directories are saved in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-return-sol-1758/evidence/verification-commands.sh`. Every final command exited 0:

| Command (see the script for full arguments) | Result |
| --- | --- |
| `python -m pytest ... test_commit_document_input_capture.py` | **11 passed**: original five unchanged, plus six F1/source-validation regressions. |
| `python -m pytest ... test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo ...::test_source_copy_retained_inputs_whole_undo_redo ...::test_source_copy_captured_authority_still_guards_acceptance` | **4 passed**, including both authority-damage parameters. |
| Runtime `python -m pytest ... test_created_child_public_captured_transcript_advances_sequential_manifest[None-True] [before-True] [late-source-True]` | **3 passed in 59.89s**, report-all includes setup/call/teardown. Exact Runtime source **2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d**. |
| `python -m scripts.reshape.compare_mypy_baseline` | **1912 / 1912** |
| `python -m scripts.reshape.compare_ruff_baseline` | **2149 / 2149** |
| `python -m mypy astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py ...` | **0 issues**, two source files |
| `python -m ruff check astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_commit_document_input_capture.py` | **0 diagnostics** |
| `python scripts/vendor_lock.py check runtime.lock.json` | **ok** |
| `python scripts/artifact_manifest.py --check` | **current** |
| `git diff --check` | **pass** |

Red-before-fix: **3 failed, 8 passed**, all three exact forged-manifest variants failed (`focused-red-real.log`). The final focused run passed all 11 in 0.97s. An earlier setup-only attempt mistakenly used the dispatcher `tmpdir` pointer file as a directory (11 setup errors, no behavior exercised); the corrected runs used its actual `/tmp/w-8718cb769d` value. One preliminary Runtime run passed 3 in 64.26s; it was repeated solely to fill observer omissions in structured exception details and before/after module hashes. Only `runtime-final-captures` is authoritative for the full Runtime packet.

## Permanent evidence

All evidence is outside TMPDIR/worktree at **/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-return-sol-1758/evidence**.

- `runtime-final-captures/`: nine full private accept packets, ten full public service packets, plus `report-all.json`. Full requests, prepared canonical documents, records/bindings/effects/dependencies/steps, receipts/results, private carrier, SQL/head/history before and after, and structured refusal details are preserved.
- `capture-summary.json`: accepted public call 03 changes SQL/head/history; exact retry 04 returns the same full reply and leaves all three unchanged. Refusal calls 07 (`before`) and 10 (`late-source`) return `validation_error` / `invalid_records` and leave SQL/head/history unchanged. Private packets preserve the tampered prepared inputs and captures used by Runtime.
- `runtime-2a9e.tar` and `runtime-2a9e-source/`: permanent exact Runtime source archive, not a checkout over another worker. Auth module SHA-256 is `3b812936efaa35a165c056fbacee6d8e699d485ca912f12e11cc4cd4bbe8f2ef`.
- `loaded-source-manifest.json` and `loaded-source/`: **110** exact loaded module files with their actual mount paths and SHA-256. Every module shared by before/after capture sets was unchanged; every saved module matched its recorded hash.
- `source-base/`, `source-before/`, `source-after/`, their hash JSON files, and `candidate.diff`: original base and final candidate source. Final source hashes below remained identical across the Runtime tests.
- `credential-scan.json`: 40 initial/final packet/report JSON files scanned, **0 credential-like key paths, 0 common credential-value matches**. `SHA256SUMS` covers all permanent source and evidence files except itself and the generated report hashes.

Final Agent SHA-256:

```text
018a116ce473a474cb081af5ff514c123582da0c2698a1cca49a548ab7981ec1  astrid/sdk/timeline/commit.py
baf524346b6b0d408a2d91683eb02dc600430145c5a18cb56e13d946ccfcbae1  astrid/sdk/timeline/_commit_patch.py
20ae264e920c39c124ff6c98a5e05af89fef6632e8efda1a6c9e7c58c37e5266  tests/editing_conformance/test_commit_document_input_capture.py
```

## Decisions, limits, and next step

I chose authenticated replacement after validation, rather than rejecting an otherwise valid command solely for a supplied internal manifest. This preserves genuine retained inputs and source-copy/inverse behavior while removing caller authority at the specified normal hydration boundary. No plan deviation or new blocker was found.

No existing test body changed; no skips, xfails, weakening, schema/client/pin/storage/final-validation/inverse changes, or dependency/environment/Git writes were made. The frozen vendor lock still points to `34eac0041b0891e9011966b39bcbd26053fde5bc`; d106/819acf artifacts were untouched. No prohibited original-nine/full/cohort/SDK-four/c271/40/281/58/P1–P4/browser suite ran. Full C0 wire/reply fields are unmodified; merged, preview, and structured-error variants beyond these targeted controls were not newly qualified.

Recommended next step: independent F1/R1 review of this own-branch candidate and permanent captures, then the manager's merge decision. The harness will create the commit using `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-return-sol-1758/commit-msg`; this worker did not commit.
