# Validation

Result: `PASS_EVIDENCE`.

## Read-only checks completed

- Read the settled `PLAN.md`, C0 `design/commit-v2.md`, D141ee full/controlling decisions, the candidate `per-id.json`, `source-manifest.json`, `validation.md`, `handoff.md`, the bound restoration manifest, and retained D120 reports. Candidate `report.md` was absent.
- Parsed the candidate per-ID JSON, candidate source manifest, bound restoration manifest, and this review's JSON with Python JSON parsing. Bound manifest count is exactly 2 and IDs are unique.
- Compared pristine, supported-parent, and review-commit Git blobs with `git show`; verified review commit tree `6806fec5`, parent tree `d362fe9d`, and pristine tree `6c0488b3`.
- Parsed the pristine/current/review installer test source with Python AST only. Exact original function source/assertion hashes and review line relocation match the assigned evidence. The original protected assertion sets do not occur as exact sets in any current candidate.
- Verified review commit diff is test-only (`git diff --name-status ecdc242e..445b9c1`) and no production/lock/schema source was changed by the restoration commit.
- Read current Agent installer production paths and current Runtime source paths with `git show`; verified the local canonical schema digest matches both Agent and Runtime source bytes.
- Verified history evidence for `b4f79d12e0` (local canonical schema verification/removal of obsolete npm schema install) and `3b61e8ef78` (local Composition/Runtime-pin test migration). These are source-history facts, not owner retirement approval.

## Commands and results

| Command | Result |
|---|---|
| `python3` JSON/AST/hash checker (read-only) | PASS |
| `git show`, `git rev-parse`, `git diff --name-status` checks | PASS |
| `git -C /home/user/work/runtime show` writer/provider/schema checks | PASS |
| pytest / test collection / body execution / imports | NOT RUN by instruction |
| typecheck / lint / full suite / browser / live request / install / render | NOT RUN by instruction |

The review's fresh continuous sampler is `disk-trace.txt`; it sampled `/tmp` available bytes every 5 seconds for the review lifetime, with a 4,000,000,000-byte stop threshold. It was stopped at review exit while still above the threshold (32 records; minimum observed 6,593,691,648 bytes); no historical trace was copied or backfilled.
