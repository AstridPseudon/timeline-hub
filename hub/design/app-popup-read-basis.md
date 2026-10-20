# Occurrence popup media: production read basis

Result: **blocked on a Runtime-owned public metadata read**. The current public
contract does not expose the complete detached `VerifiedMedia` value bound to
the exact five-field selection. Follow the task's docs-only branch: no App read
adapter, popup/session wiring, generated/schema edits, or pin adoption.

## Sources inspected

- App task base: `8d3cc77f241610ec86b1b76fc07162c91700aab1`, branch
  `tl/app-m2-popup-read-basis`. Existing detached native capture is unchanged.
- Reviewed App media-read branch:
  `tl/app-m2-media-read-integration` at
  `2f2c41899fd795282fd35de2b6a52a5d307567c0`. Read the narrow DataProvider /
  RuntimeDataProvider delta and its integration fixture; did not overlay M1
  files. Its optional `getProjectMediaSelection(query)` port validates the exact
  five fields and explicit asset/generation/variant or association object match;
  the existing client wrapper uses `withSession` and the generated method.
- Runtime integration source:
  `9f9b25c000485e919f30f1411831fe2d5a3c1316`. Read
  `runtime_protocol/{service,server,timeline_commit_port}.py`, public OpenAPI and
  existing media tests. The `d691ddadb4ef3f5881a25fa893b4fb812211f102`
  generated client 0.2.3 candidate was a read-only comparison; its relevant
  public media reads have the same limits. It is not adopted or qualified here.
- Frozen Agent:
  `d4743e2984cef0908fa0b6bef166aa801f2bde8f`, read with `git show`:
  `astrid/sdk/timeline/_media_inputs.py` and
  `native_occurrence_media_commands.py`. No validation changes proposed.

## Required input and exact missing contract

The immutable identity stays exactly:

```ts
{ asset, generation_id, variant_id, object_id, catalog_digest }
```

Detached capture additionally requires `selection` equal to that entire tuple,
`media_type` with an image/video MIME prefix, and a positive integer byte `size`.
Video also requires finite, positive `duration_seconds`; capture checks the
source window against this intrinsic duration for both old and new swap inputs.
`width` and `height` are optional, not blockers for these recipes.

The five-field public selection supplies none of `media_type`, `size`, or
`duration_seconds`. Project object reads can supply the first two for the same
object. **The remaining essential video field is `duration_seconds`, and no
existing public read returns the complete metadata with Runtime verification
against the same `catalog_digest`.** An image-only object composition would not
solve this add/swap input contract for video and is not introduced here.

## Existing reads and their limits

| Existing generated read | What it establishes | Why it does not close the contract |
| --- | --- | --- |
| `getProjectMediaSelection(projectId, query)` | `GET /v1/projects/{project_id}/media-selection`; exact explicit selector or `{association_id, object_id, version}`; Runtime resolves project ownership, exact settlement/variant binding, lifecycle and catalog pin | Response is exactly five identity fields, with no metadata. Do not widen it. |
| `getProjectObjectLocation(projectId, objectId)` | Project-owned, verified CAS object ID/digest, MIME type, size; response also contains a local path | No duration or catalog pin. `verified: true` describes CAS bytes, not the catalog selection. A path is unnecessary for capture. |
| `listProjectObjects(projectId, ...)` | Managed object ID/digest, MIME type and size | No duration, exact generation/variant association, or catalog pin. |
| `getObject` / `headObject` | Object bytes or headers, ETag and range information | No intrinsic duration or catalog record. `catalog_digest` is computed over a Runtime record, not a published CAS object address; do not fetch it as an object. |
| `getProjectMediaImport(projectId, importOperationId)` | Completed import result is retained in Runtime's idempotency state; includes project, generation/variant, asset/entry object identity, MIME/size and optional duration | Requires the original import operation ID; does not cover all generated outputs or carry/check the selected catalog digest. Pending results are incomplete. Stored import details originate in import request metadata; local decoder validation does not populate a measured duration in the read response. |
| `getGeneration`, `getVariant`, generation/variant lists | Current catalog rows; generation params or variant metadata may contain duration; variant identifies an object | No retained catalog snapshot/read-by-digest or atomic binding of those separate responses to the selection. Copying metadata or reimplementing Runtime's projection/hash would introduce a second hydrator. |
| `getTask`, `listProjectTasks`, `listManagedOutputs`, `getManagedOutput` | Task scope/status/result and output identity/association/lifecycle; a settled output result may contain duration | Typed managed output has MIME/size but no required intrinsic duration. Task results are open JSON with no universal required duration or catalog pin. Runtime's catalog entry derives duration from validated generation params/variant metadata, not arbitrary task output JSON. Same object ID alone does not prove equality to that selected catalog entry. |

`MediaReads._selected_project_media` constructs and hashes the authoritative
record under Runtime's mutex. It joins exact managed project/generation/variant/
object state, reconciles MIME/size and intrinsic metadata, and includes eligible
managed-output settlement/provenance/lifecycle in the record. It rejects missing
audio/video duration and contradictory intrinsic values. The record is not
published as a retained catalog object through an existing public read.

Reading metadata between two selection reads does not return a Runtime-verified
metadata tuple; reproducing all projection, normalization, association checks
and digest logic in App is outside this task's minimal-adapter boundary. Popup
mutable metadata, registry duration guesses, source-window lengths, and caller
provenance cannot supply the missing authority.

## Recommended minimal Runtime-owned reuse

Reuse the already implemented `MediaReads.selected(project_id, selection)` from
`runtime_protocol/timeline_commit_port.py:618`. It accepts exactly the five-field
`MediaSelection`, calls the existing authoritative reconstruction, rejects an
object/catalog mismatch, and returns the existing `VerifiedMedia` DTO:

```ts
{ selection, media_type, size, duration_seconds?, width?, height? }
```

Runtime should make that existing read available through its normal authenticated,
project-scoped read surface and generate the official public client contract.
This is a recommendation for its owner, **not an existing endpoint or a proposed
App-owned route spelling**. Keep the current selection response unchanged. Reuse
the existing local-door origin/credential/project checks and `projects:read`
policy, mutex and error behavior; no new authority or caller provenance fields.

Then App can compose only selection -> exact metadata read using `withSession`:
retain the explicit asset alias or association-resolved selection verbatim,
check the returned complete selection and object/digest consistency, and return
the detached input for capture. Preserve the original association/version query
and both swap inputs; never resolve a mutable primary/latest fallback or refresh
an already captured pin after a refusal. Runtime's `RequestCommitPort.selected_media`
remains the final verifier during acceptance, including its revalidation.

## Validation and limits

Executed on the unchanged App base:

```bash
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/occurrenceMediaCapture.test.ts src/tools/video-editor/commands/occurrenceMediaPrimitives.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts --pool=threads --maxWorkers=1
```

Exit 0: **5 files / 354 tests passed**, 7.24 seconds. This revalidates detached
native helpers and neighbors, not a production read adapter or Runtime acceptance.
No tests/assertions/expected failures were changed; the three authorized journey
expected failures remain untouched. No project tsc was needed for this docs-only
result; no full suite, browser, socket, network, install, build or Runtime test ran.

The existing named central `media-selection-integration` suite and reviewed
`tests/integration/runtimeMediaSelection.test.ts` are the bounded future proof
location. Its current fixture proves five-field reads for settled PNG imports,
not a complete video `VerifiedMedia` read. Once the official read exists, extend
that lane with actual settled image/video inputs, old/new swap identities,
cross-project/object/digest/association-version refusal, catalog changes between
selection and metadata read, unchanged aliases and zero timeline writes. Current
runtime `test_media_selection_uses_main_settlement_identity_and_rechecks_lifecycle`
was inspected, not executed; it exercises the internal verifier and does not
expose the missing public read. No central run was submitted for this docs-only
task because there is no new valid adapter to exercise.

Next: Runtime owns the public reuse/official generation, then an App worker adds
the narrow adapter and unit captured-shape tests plus that central fixture proof.
Popup/session write wiring remains the following worker's scope. All M2
integration remains held until the orchestrator records M1.
