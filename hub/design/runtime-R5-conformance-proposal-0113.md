# R5 conformance assessment

## Finding

PLAN R5’s direct 410 behavior is intentional and correctly implemented:

- `RetiredRouteError` emits HTTP `410`, code `retired_route`.
- `publish_parent_composition()` is now an unconditional stub.
- HTTP dispatch rejects before reading the body, checking idempotency, or writing.
- The current `Error` schema excludes `retired_route`.
- The OpenAPI publication route advertises `200/409`, not `410`.

Therefore this cannot be repaired wire-preservingly without violating PLAN R5. It requires a genuine public contract change.

## Recommended minimal proposal

Change only the contract/conformance surfaces:

1. Add `"retired_route"` to `contract/schemas/common.json`’s `Error.code` enum.
2. Add a reusable OpenAPI `RetiredRoute` response referencing `common.json#/$defs/Error`.
3. Add `410` responses to the declared R5-retired operations:

   - `createTimelineDocument`
   - `publishParentComposition`
   - `replaceParentCompositionMedia`
   - `replaceTimelineClip`
   - `publishTimelineRender`

   Do not add undocumented routes or new APIs.

4. Preserve 409 conformance by moving the stale-head case from the retired publication route to canonical `commitTimeline`, under a truthful case name such as `commit_conflict_409`.
5. Add a separate recorded `retired_route_410` case for the old publication route.
6. Keep the existing R5 authority tests proving HTTP 410, authentication precedence, and no writes.

Do not map the retired route to `409 conflict`; that would contradict R5 and invalidate the dedicated retirement tests.

## Wire impact

The retired-route body remains structurally:

```json
{
  "code": "retired_route",
  "message": "legacy timeline writes are retired; submit EditCommands through commitTimeline",
  "request_id": "<request_id>",
  "details": {
    "status": "refused",
    "reason": "timeline_commit_required",
    "hint": "Submit a timeline commit instead of the retired save route.",
    "suggested_command": "timeline commit",
    "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit"
  }
}
```

C0v2 is unchanged: request fields, accepted/merged replies, conflict reason/head, invalid diagnostics, preview status, receipts, and undo data remain exactly as specified.

The old `publish_conflict_409` cannot remain a 409 publication fixture because the route never reaches its old CAS logic. Its semantic 409 assertion must be preserved on the canonical commit path, not dropped or relabeled as an arbitrary error.

## Digest and adoption impact

This changes:

- `contract/schemas/common.json`
- `contract/openapi/workspace-v1.yaml`
- recorded response fixtures
- `tests/test_recorded_responses.py`
- `scripts/record_responses.py`
- `contract/artifacts.json`

Regeneration will update digest-bearing generated files:

- `runtime_protocol/contract_metadata.py`
- `packages/python/astrid_runtime_client/{generated.py,contract_metadata.py}`
- `packages/typescript/src/{generated.ts,contract-metadata.ts}`
- `conformance/typescript/{generated.ts,contract-metadata.ts}`

`contract/manifest.json`, `component-manifest.json`, C0v2 schemas, and Composition are unchanged.

Because the schema/OpenAPI digest changes, this requires a coordinated new Runtime contract tuple and Agent/App client adoption. Agent’s vendored Python client and App’s generated Runtime client/metadata pins must advance together. No adoption or release change was made here.

## Existing coverage

The retained R5 tests already cover the required behavior:

- `tests/test_timeline_legacy_authority.py`
- `tests/test_timeline_authority_door.py`
- `tests/test_timeline_shot_authority.py`
- `tests/test_timeline_reference_authority.py`

They assert direct 410 refusal, auth-before-retirement behavior, no idempotency replay, and unchanged database/CAS state.

## Evidence

No tests were run by this worker, per task instructions.

Retained census command:

```bash
env ASTRID_CHECKOUT=/home/user/work/agent \
  /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

Recorded result: `6479 passed, 36 failed, 26 skipped, 15 xfailed`; the relevant failures are stale recorded responses/schema/artifact-manifest checks caused by R5’s intentional 410 cutover.

Recommended verification after approval:

```bash
python -m pytest -q tests/test_recorded_responses.py
python -m pytest -q tests/test_timeline_legacy_authority.py tests/test_timeline_authority_door.py
python generators/generate.py --check
node tools/generate_typescript_conformance.mjs \
  --contract contract/openapi/workspace-v1.yaml \
  --schema-manifest contract/manifest.json \
  --component-manifest contract/component-manifest.json \
  --fixture-root conformance/fixtures --check
python scripts/artifact_manifest.py --check
```

No tracked edits or test runs were made.