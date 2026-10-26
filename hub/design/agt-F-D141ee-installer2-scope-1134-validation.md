# U2 F D141ee installer2 validation

Result: `PASS_EVIDENCE`. This is source evidence and owner-scope analysis, not a behavior PASS, REG0, or ship claim.

## Identity and conservation

- Review commit: `445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf`, tree `6806fec5657f26097d0d0f3da29082907e6faadd`; parent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`.
- Pristine Agent: `64197afa297f86f1e738238d5e80aff6d33e303a`, tree `6c0488b3efdfa47479b0ad1b7bd20608383be26e`.
- Current Runtime: `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`; retained pristine Runtime: `fa9cd5464a8b37b02f971de375e56be846cd69e2`, tree `124e10dbcd54fb90219e783ec11aa34f8c91590c`.
- `git diff --name-status ecdc242ed9b673f641759ecf029f95e89a2c6f92 445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf` reports only test paths; no production or lock file was changed by the restoration commit.
- Assigned manifest parsed with exactly two unique IDs. Its SHA-256 is `ebfa4f9def71aa3bf7656a31ea759068bd6946e735f5e007040048c5b61bea2d`.

## Static Git/AST/source checks

- Read `tests/test_installer_schema.py` from pristine Git blob `ede759060078ab18a9eac75fd682ddb429073518` and current supported parent blob `00ba669033726fc84b305144acd2c9c40eb314df`; parsed both with Python AST only (no imports or test collection). Both assigned pristine functions were byte/source and assertion enumerated. The review commit contains the exact original functions at lines 199–283 and 286–304.
- Original function source SHA-256 values: staging `a918238932392fdab15be4cd797092af1d14853e3060a9efab48dfb4d43c60d6`; lock `c10befe3af82a12a9bb69c04a7fc919506ac6bef39341576c254b14c99540069`.
- Current supported replacement source values: local staging `a9fb4fd8a033f64731f091a7cb44eace5871f5e7e9ad8a0405cc8f896f2bef2e`; Runtime/Composition lock `14de8f2cddec2c90f7f2d82a9ea744085e392de59f8f1ec29415ce3ab0d771a8`. Neither has the original assertion set.
- Retained schema8 review reports the two current replacement groups PASS and the two assigned originals as `DROPPED_BY_OUR_PATCHES_REG`; no exact same body/assertions PASS move was found.
- Read-only source-history check found `b4f79d12e0` (“fix(installer): return D72 staging to local canonical schema”), which explicitly adds `_verify_local_timeline_schema`, removes the npm schema Python install, and describes the old installation as obsolete. Commit `3b61e8ef78` migrates the lock assertion to the approved local Composition artifact and Runtime-owned canonical schema. These historical commits are evidence of the current path, not a new retirement approval.

## Path and contract checks

- Current `Backend.stage` checks the Agent-local schema against `runtime.lock.json` before the ordinary Python installs, then runs locked Remotion dependency staging, then service declaration (`astrid/installer/backend.py:432-466`).
- Current `remotion/package.json` points to the local Composition artifact; current `remotion/package-lock.json` contains Composition `0.0.14` and no `@banodoco/timeline-schema` package. The old pristine values are Composition `v0.0.6` and transitive schema `v0.0.1` with the old integrity.
- Current Agent schema SHA-256 is `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`; current Runtime contract source at `contract/schemas/timeline-config.schema.json` has the same digest. This is the approved single source map.
- Runtime’s supported writer coordinates are `runtime_protocol/service.py:2477-2565` (`commitTimeline` / `_execute_timeline_commit`) and `runtime_protocol/timeline_commit_provider.py:16-93`; the schema/package issue is installer/render staging, not a second timeline writer.

## Test policy and retained results

- No pytest, test collection, import-dependent execution, install, render, browser, child, request/CAS/service, full suite, or manual integration was run in this worker, as required.
- Prior retained evidence only: `agt-F-D141ee-schema8-full-decision-next/evidence/review.json`, `findings.md`, `validation.md`, and `map.json`. The prior independent restoration review recorded 15 executed installer/writer failures and 40 collection-error nodes in its separate mixed run; those results were not rerun here. The reviewer's private XML is not claimed as retained raw output.
- The fresh disk trace at `disk-trace.txt` recorded six samples over five seconds, all above the 4,000,000,000-byte stop line; the minimum observed value was `6992437248` bytes.
