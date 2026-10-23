# agt-R1-transcript-current-port-1810

## Result

Ported the exact cumulative R1 transcript-capture delta from Agent source candidate `f98dbed881fb568584c1e7d3301f71a4dea8ca4e` (base `6531622c8f198c3efb509217e303fcad0126c47b`) onto current integration HEAD `1962a2413095a2f82bf927e7c42c532072b5c812`.

Only these three paths changed:

- `astrid/sdk/timeline/commit.py`: authenticated `_copy_manifest` replacement in `_hydrate`; current d1d legacy-final-validation block preserved.
- `astrid/sdk/timeline/_commit_patch.py`: add consumed authenticated source/transcript pins at the causal command boundary.
- `tests/editing_conformance/test_commit_document_input_capture.py`: the candidate's 11 focused tests.

No source behavior was authored, and no Runtime/schema/client/pin/G5/test-body changes were made.

## Mechanical comparison

Permanent evidence is under the worker `evidence/` directory.

- Source patch: `evidence/source-cumulative-653-to-f98.patch`; SHA-256 `5d9d815243685e85e19c4c2462eab77513ff81a24cf3c59a71498b23e32ed6ac`.
- Own actual diff: `evidence/own-tracked-diff.patch`; SHA-256 `ff274fb4323a439cbeda0063d29ea77dc400d43e7f9386c54cafe0849607307a`.
- `_commit_patch.py` and the new test file are byte-identical to `f98dbed88).
- `commit.py` differs only because current HEAD retains the unrelated d1d final-validation block; the target `_hydrate` AST/body hash is identical to `f98dbed88`: `685571fda66d8c46acbd225316cb54d220e468ca5641565116344125d0fda058`.
- `CommitPatch.after` AST/body hash is identical: `2bdabaa4e7cfc449429190438cb5f098f78556746bd6eb4acbf783d6ab7a90e9`.
- New test module AST hash is identical: `308a2c044a25ce391cf40cc83ff7b19d7e3a6b957fac10051d244e921a798770`.
- Complete owned before/after/source hashes: `evidence/owned-before-after-hash-map.tsv`.
- Complete tracked-file outside-change map: `evidence/complete-file-hash-map.tsv`; no outside-owned file changed.
- Structured comparison: `evidence/source-comparison.json`.

## Tests and checks

All commands ran from this worktree with caches/basetemps under `/tmp/w-f7077cfe8f` and logs retained in `evidence/`.

- Focused new test:
  `... pytest ... tests/editing_conformance/test_commit_document_input_capture.py` — **11 passed**.
- Existing duplicate/inverse controls against final-review Runtime source `runtime-2a9e-source` — **4 passed**.
- Affected private sequential controls:
  `test_private_sequential_capture.py test_private_sequential_capture_runtime.py` — **16 passed**.
- Ruff baseline — **2149/2149**.
- Mypy baseline — **1912/1912**.
- Scoped mypy on `commit.py _commit_patch.py` — **0 issues**.
- Scoped Ruff on the three changed paths — **0 diagnostics**.
- `scripts/vendor_lock.py check runtime.lock.json` — **ok**.
- `scripts/artifact_manifest.py --check` — **current**.
- `git diff --check` — **pass**.

Per task scope, no original Runtime-3 transcript node, full suite, browser, cohort, SDK-four, P1/P4, or other prohibited suite was run. Runtime acceptance remains owned by the integrated proof worker; this report does not claim it.

## Safety and disposition

Credential scan: `evidence/credential-scan.json` reports **0 credential-like key paths** and **0 credential-value pattern matches**.

The source candidate's independent final-review process was not re-run or independently claimed here; this worker followed the instructed start-on-branch mechanical port. If that source review is classified FAIL, this port must remain held and is not an approval bypass. No new semantic choice or conflict occurred.

## Next step

Harness commit message is recorded separately. The orchestrator/merge worker should review the permanent captures and apply its normal merge decision.

