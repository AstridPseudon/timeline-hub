## Verdict: FAIL as written

A public contract/digest change is genuinely required: runtime emits `410 retired_route`, but the shared Error schema does not permit that code ([errors.py:50](/home/user/work/wt/rt-R5-conformance-review-0119/runtime_protocol/errors.py:50), [common.json:30](/home/user/work/wt/rt-R5-conformance-review-0119/contract/schemas/common.json:30)). This is the older route-error taxonomy, not a C0v2 request/reply change. C0v2 and canonical `commitTimeline` 409 remain unchanged ([OpenAPI:282](/home/user/work/wt/rt-R5-conformance-review-0119/contract/openapi/workspace-v1.yaml:282)).

The proposed five-route/OpenAPI change is not minimal or fully truthful:

- Those five routes are unconditional retired stubs, so retaining their advertised `200`/`409` success semantics and old publication eligibility description is incorrect. The source gates them through `_require_timeline_command()` ([service.py:1650](/home/user/work/wt/rt-R5-conformance-review-0119/runtime_protocol/service.py:1650)); the OpenAPI still describes the old behavior ([workspace-v1.yaml:360](/home/user/work/wt/rt-R5-conformance-review-0119/contract/openapi/workspace-v1.yaml:360)).
- The documented contract omits other real 410 outcomes: `getDocument`, `createDocument`, `updateDocument`, and historical `recoverTimeline` ([server.py:722](/home/user/work/wt/rt-R5-conformance-review-0119/runtime_protocol/server.py:722), [service.py:3747](/home/user/work/wt/rt-R5-conformance-review-0119/runtime_protocol/service.py:3747)).
- Project-shot mutation operations also return 410 for placed shots and are currently documented only as successful operations ([service.py:2833](/home/user/work/wt/rt-R5-conformance-review-0119/runtime_protocol/service.py:2833), [test_timeline_shot_authority.py:230](/home/user/work/wt/rt-R5-conformance-review-0119/tests/test_timeline_shot_authority.py:230)). `promoteProjectShotCandidate` is different: it does not use that retirement gate and should not receive 410 merely by association.

### Corrected minimal proposal

After orchestrator approval:

1. Add `retired_route` to `contract/schemas/common.json`.
2. Add a reusable `RetiredRoute` response to `contract/openapi/workspace-v1.yaml`.
3. For the five unconditional routes, replace stale success/409 declarations with the actual 410 response and rewrite the obsolete publication description.
4. Add conditional 410 responses to the documented document/recovery operations and the placed-shot mutation operations listed above. Do not add undocumented legacy paths.
5. Update `tests/test_client_parity.py` only to assert the corrected retired-route description; preserve all authority/no-write/authentication tests.
6. Change recording only as follows:
   - replace the impossible old `publish_conflict_409` fixture with `retired_route_410`;
   - add a genuine canonical `commit_conflict_409` fixture using `commitTimeline`;
   - preserve `code: conflict`, `details.reason: stale_head`, and the existing 409 expectations;
   - update `scripts/record_responses.py`, `tests/test_recorded_responses.py`, fixtures, and `contract/artifacts.json`.
7. Regenerate digest-bearing artifacts only after approval.

Expected changed files/metadata:

- Hand-authored: `contract/schemas/common.json`, `contract/openapi/workspace-v1.yaml`, recorder/tests, response fixtures, `contract/artifacts.json`.
- Generated: `runtime_protocol/contract_metadata.py`, Python/TypeScript client generated files and metadata, and TypeScript conformance generated files/metadata.
- Unchanged: `contract/manifest.json` path list, `contract/component-manifest.json`, `contract/schemas/timeline-commit.json`, and all C0v2 request/reply schemas.

The schema digest will change; exact digest values are intentionally uncomputed because this review is read-only. Runtime/Agent/App metadata adoption is therefore required by the tuple handshake, but no caller request/reply or product API shape changes are required.

One wording correction: HTTP dispatch prefetches raw request bytes before routing ([server.py:1205](/home/user/work/wt/rt-R5-conformance-review-0119/runtime_protocol/server.py:1205)). The accurate claim is that retirement gates run before JSON decoding, idempotency lookup, and writes—not before raw body prefetch. Existing malformed-body and auth-precedence tests must remain intact.

No tracked files were changed and no tests were run, per task instructions. Retained full result: `6479 passed, 36 failed, 26 skipped, 15 xfailed`; relevant known failures were recorded-response/schema/artifact-manifest mismatches.