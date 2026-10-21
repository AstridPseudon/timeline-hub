# AP2-M2 mounted parent ADD refusal cause and source

## Result

The prior HTTP 422 was a malformed-fixture refusal, not the intended semantic
"valid digest but unregistered media" refusal. The retained request changed
`object_id` to `sha256:wrong-selection`, which fails the exact digest grammar.
The retained response was HTTP 422 with `code: "validation_error"`. It did not
indicate an authentication, transport, or Runtime availability failure.

The current mounted spec already contains the smallest fixture correction: it
keeps the original five-field request and changes exactly one hex digit of the
real `sha256:<64-hex>` object ID. Its existing `[404, 409]` refusal assertion
therefore remains; no 422 assertion was added. With the frozen Runtime source,
this valid object mismatch maps to HTTP 404 / `code: "not_found"` because the
managed generation/variant/object row is absent. A catalog-digest mismatch is
the separate HTTP 409 / `code: "conflict"` case.

## Source and request evidence

The retained failed run is the bounded evidence from the earlier mounted gate:

- request: `GET /api/runtime/v1/projects/<project>/media-selection/verified`
  with the normal `asset`, `generation_id`, `variant_id`, and `catalog_digest`
  fields, but `object_id=sha256:wrong-selection`;
- response: HTTP 422, `{code: "validation_error", ...}`;
- the request was observed after the normal import and selection requests, so
  this was not an auth or transport failure.

The frozen Runtime 95bd source confirms the mapping:

- `runtime_protocol/timeline_commit_port.py:835-839` validates the complete
  five-field `MediaSelection` before the managed-media lookup;
- `runtime_protocol/timeline_commit_port.py:734-755` returns `NotFoundError`
  when a syntactically valid selection names no managed object;
- `runtime_protocol/errors.py:27-29` maps `ValidationError` to 422 and
  `validation_error`; `errors.py:45-47` maps `NotFoundError` to 404 and
  `not_found`; `errors.py:22-24` maps `ConflictError` to 409 and `conflict`.

The exact current source tuple is retained and recorded by the existing driver:

- App source `25155ccb22728780a3ecd6379a929cad75cc1400`, tree
  `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`;
- App pin bytes from `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`;
- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`;
- Runtime and producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- public13 archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.

## Change

Changed only `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`:

- corrected its expected App tree from the stale `78f...` guard to the frozen
  `972d...` tree;
- updated its retained source identity fields to App pin 10fa, Agent 6ef,
  Runtime/producer 95bd, and public13.

No product caller, media tuple authority, product guard, timing or `afterClipId`
policy, shared HOME source, native activation, or writer deletion changed.

The existing live mounted ADD callers were not changed: `useAssetManagement.ts`,
`external-drop-utils.ts`, `useExternalDrop.ts`, `useTimelineState.ts`,
`useTimelineCommandsService.ts`, and the existing commit-session/outbox path.

## Verification

Passed:

```text
sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts
  1 test collected
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts
git diff --check
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
  failuretrap probe passed
```

No real gate, browser run, localhost/live socket run, full suite, dependency
install, or central request was made. The next existing command, after the
required independent conversion review and orchestrator authorization, is the
existing mounted driver against the frozen tuple:

```text
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

That future run must retain the original valid ADD, lost-ACK, restart/retry,
reload, undo, opaque-data, duplicate, and zero-legacy assertions.
