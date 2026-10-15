# Timeline commit candidate — CONTRACT-COMMIT-001

Implementation readiness only. No configured review was invoked, no contract/card
was frozen or accepted, and no acceptance service or release/IP completion is
claimed. ACCEPT implements the service; COMMIT implements command execution and
the shared rebase. X0-EDITOR observations remain unresolved.

Source authority: the 2026-10-15 portfolio's current `cards.md#contract-commit`
and `briefs/WS-SAVE.md` §§3.3–3.7. The current card overrides the older §4.2
step 6 early preview: dry runs **rebase onto head** through the same shared rebase
as real commits, then return uncommitted commands or conflict. The App performs
no second rebase. Runtime owns the commit route and durable acceptance.

Canonical homes:

- `contract/openapi/workspace-v1.yaml`: only the specified commit POST is added.
  Existing routes are unchanged; no publish-document adapter/endpoint is added.
- `contract/schemas/timeline-commit.json`: request, final result, HTTP result
  variants and internal acceptance schemas and `x-runtime-interface` signatures.
  No copied TimelineConfig or EditCommand definition. `CommitCommand` is opaque
  until CONTRACT-COMMAND supplies its definition. `CommitExchange` is a
  conformance-only request/result pairing, never a new wire envelope.
- `generators/generate.py`: projects structural Python/TypeScript types from
  this schema, derives the commit route from OpenAPI, and syncs/checks the
  existing product artifacts. JSON Schema conditionals are validator constraints;
  generated types express structure, optionality, literals and unions.
- `conformance/fixtures/timeline-commit-candidate.json`: 93 unique **synthetic**
  contract cases, each with an exact id, schema definition, expected validity and
  note. These are not X0 App observations and do not prove service behavior.

## Invariants and executable evidence

All fixture ids below are exercised by
`tests/test_timeline_commit_contract.py::test_fixture[<id>]`. Other named tests
are in that file unless a different path is given.

| Invariant | Schema / contract location | Cases and tests | Limit / owner |
|---|---|---|---|
| Absent vs clear vs null | `CommitChange`, opaque `CommitCommand` / `CommitJson`; required envelope fields | `CC-DOCUMENT-*`, `CC-CHANGE-*`; `test_absence_clear_null_opaque_fields_and_authored_units_remain_distinct` | Exact command clears/ABSENT wire encoding belongs to CONTRACT-COMMAND; observed App clear paths pending X0. Omission is never synthesized into clear. |
| `scope.complete` | `CommitScope.complete`, required unique clips/tracks array, no default | `CC-SCOPE-MISSING-COMPLETE`, `CC-SCOPE-UNIQUE`, `CC-SCOPE-UNKNOWN`, `CC-SCOPE-COMPLETE-NULL`, `CC-SCOPE-SHARED` | [] means omission never deletes. Actual writer completeness pending X0; deletion execution belongs to COMMIT. |
| Opaque preservation | `CommitJson`, document change, opaque commands/publication payloads | `CC-DOCUMENT-*`; absence/opaque test; Python/TS transport checks | No stripping or normalization in types/client. Actual editor round trip requires X0 and preservation work. |
| Exact base/source identity | required project/timeline/request/session/base ids; nullable base publication; `CommitSource`, `CommitActor` | `CC-REQ-MISSING-*`, `CC-REQ-ACTOR`, `CC-RESULT-HASH`; `test_whole_request_hash_distinguishes_intended_change_and_exact_retry` | Request hash = SHA-256 of whole request, sorted keys, compact separators, UTF-8, ensure_ascii=False. Document digest retains existing journal exclusions (draft envelope and every `_` key). Exact hash equality and base existence are semantic checks. |
| Retry identity | `LookupCommitRequestResult`, `AcceptRequest.request_hash`, `AcceptError` | `CC-LOOKUP-*`, `CC-ACCEPT-REPLAYED`, `CC-ACCEPT-ERROR-*`; exact Python/TS retry checks | Non-dry retry is lookup-before-head; exact retry returns stored result verbatim after head moves. Different request under same tuple is refused. HTTP `X-Request-ID` remains a per-attempt diagnostic; `request_id` / Idempotency-Key is semantic identity. Durable behavior belongs to ACCEPT. |
| Occurrence scope | `CommitScope.target/content`, parent excludes occurrence-only fields; optional exact shot/internal base fields | `CC-SCOPE-OCCURRENCE`, `CC-SCOPE-SHARED`, `CC-SCOPE-CONTENT-OMITTED`, `CC-SCOPE-PARENT-*`, `CC-SCOPE-EMPTY-OCCURRENCE` | Optional content has this-occurrence meaning per §3.3, without inserting a default. Actual App values pending X0. A parent save cannot touch shot internals; nesting/canonical payload acceptance remains semantic validation. |
| Timing units | `CommitAffected.start_s/end_s`; opaque authored command values | `CC-TIMING-SECONDS`; absence/units test and WS-SAVE synthetic +9f specimen | Affected ranges use seconds. Numeric seconds vs a numerically indistinguishable millisecond value cannot be inferred by schema. TimeRef parsing/rounding and scoped-id grammar belong to CONTRACT-COMMAND/timing. |
| Security boundary | top-level closed envelopes; no request publisher; receipt publisher only Runtime output; AcceptRequest pre-result authenticated fields null; inherited bearer auth | `CC-REQ-FORGED-PUBLISHER`, `CC-ACCEPT-PUBLISHER`, `CC-ACCEPT-RESULT-PUBLISHER`; OpenAPI/security and client-header tests | Asserted actor/source is attribution, never authority. Authentication/authorization, exact path/header/body equality and capability checks belong to service/transport. Client methods derive ids and headers from the same body. |
| Dry-run rebase | commit operation description; `CommitExchange`; preview final result null revision/receipt; acceptance/lookup exclude preview | `CC-REQ-DRY-RUN`, `CC-DRY-*`, `CC-COMMIT-NOT-PREVIEW`, `CC-PREVIEW-*`, `CC-HTTP-PREVIEW-200`, `CC-HTTP-CONFLICT-200`, `CC-ACCEPT-PREVIEW`, `CC-ACCEPT-DRY-RUN`, `CC-LOOKUP-PREVIEW` | Return rebased uncommitted commands or conflict; store **nothing**, including no request-id reservation. Retry dry run after network failure; retain suffix in recovery draft. Later commit retries its original id. Rebase and no-write behavior require service tests in COMMIT/ACCEPT. |
| Atomic Runtime interface | `AcceptRequest/Response/Error`, `CommitEvidence`, `CommitNarration`, `CommitHead`, `CommitRevisionSummary`, `x-runtime-interface` | `CC-ACCEPT-*`, `CC-NO-CHANGE-REVISION`, `CC-LOOKUP-*` | Head/request/stored final result/evidence/narration are one transaction. CAS errors identify head/hash. Ancestry uses previous_revision_id/previous_publication_id/restored_from_revision_id, never publication parent_revision_id. No implementation here. |
| HTTP result mapping | `CommitHttpSuccess` / `CommitHttpBadRequest` / `CommitHttpUnavailable`, OpenAPI 200/400/503 | `CC-HTTP-*`, `test_openapi_adds_only_one_route_and_typed_http_results`, Python transport and real urllib HTTPError tests; `packages/typescript/test/timeline-commit.test.mjs` | Non-error statuses, including conflict/refused, are 200. runtime_unavailable is 503/unknown outcome; other error codes are 400. |
| Generated drift | schema-derived type blocks, tracked Python template, contract digests/operation projection, product byte comparison | `test_generation_is_deterministic_and_schema_derived`, `test_generated_drift_detection_for_python_typescript_and_openapi`, `test_product_copy_check_rejects_drift`; existing generator checks | Deliberate Python/TS/product mutations fail check. Legacy unrelated TypeScript body remains on the existing generator path; this slice has no handwritten duplicate types. |

## Pending observations and integration questions

X0 owns actual main-editor payload fixtures, provider/writer census, completeness
values, clears vs omission/null, unknown-field survival, load/reload
normalizations, occurrence targets/base identities, session counters, request ids
and retry/recovery behavior. No values/defaults were inferred from App code shape.
The request id uses the already-established OpenAPI IdempotencyKey header format;
no session-counter starting value or lower bound is inferred.
The transitional `app-save` document form can represent its eventual observations;
no adapter behavior or second endpoint is implemented here.

CONTRACT-COMMAND must supply concrete EditCommand, ScopedId and ABSENT encoding;
those boundaries are deliberately opaque here. The current brief does not specify
an ABSENT JSON sentinel, so inventing one would make this slice incompatible.
The optional occurrence base fields remain optional exactly as §3.3 writes them;
required subsets for particular real writers need source/observation evidence.

`AcceptRequest.result` is the pre-accept template, with Runtime-owned ids,
provenance and receipt unfilled/null. `CommitResult` is the final public/stored
result; accepted/no_change require a receipt. This distinction represents §3.6's
instruction that Runtime fills its fields before storage, without allowing a
caller-supplied publisher. ACCEPT must compare top-level request identity/hash to
the embedded result and authenticate publisher independently.

The schema cannot prove equality across arbitrary fields, cryptographic digest
correctness, immutable source existence, monotonic counters, interval ordering,
conservative impact coverage, conflict-to-choice matching, authorization,
transaction atomicity or durable replay. Those are explicit service obligations,
not a claim of passing acceptance. No frozen review was run.

## Reproduction

From the Runtime worktree (use the exact isolated product roots in the handback):

```sh
python3 generators/generate.py --astrid-root <astrid-root> --app-root <app-root>
python3 generators/generate.py --check --astrid-root <astrid-root> --app-root <app-root>
python3 -m pytest tests/test_timeline_commit_contract.py -q
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root . --fixture-root conformance/fixtures
```

The TS transport test runs with an installed Node supporting TypeScript transform:
`node --experimental-transform-types --test packages/typescript/test/timeline-commit.test.mjs`.
`TIMELINE_COMMIT_CLIENT=<absolute App generated.ts>` runs the same identities
against the exact App artifact; repeated ids are not new unique tests.
