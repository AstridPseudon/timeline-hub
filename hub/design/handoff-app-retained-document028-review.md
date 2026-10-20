# Retained VerifiedDocument 0.2.8: App native PARAM review

**KEEP — review complete; the previous missing-document read-shape blocker is resolved in the reviewed Runtime source.** Given the approved exact V1 `DocumentPin`, the normal generated document read now returns the entire `VerifiedDocument`, and its selected admission supplies the object ID for the existing normal generated object read. Together their unmodified results supply frozen027 native selected-PARAM capture's document and selected-object inputs. No App declaration reconstruction, hash authority, new wire type, or extra object endpoint is needed.

This closes the specific 0.2.7 omission in escalation `app-20261020T0429Z-retained-param-document-still-missing.md`, **not** App writer readiness, a paired freeze, or public/native acceptance qualification. Current App remains on client 0.2.1, lacks both methods, and has no selected-PARAM capture adapter at this task's base. No product, root, generated client, pin, writer, or behavior expectation was changed.

## Fixed review inputs

All Runtime and Agent source anchors below refer to these immutable commits, read through `git show`; subsequent integration movement is outside this verdict.

| Source | Exact commit | Tree |
| --- | --- | --- |
| App task base | `cc4dff86b845432acc38dd9407ccb079a6a5a677` | `0bf2dba9590097e703bf5775f6a7fa4363184449` |
| Runtime reviewed | `1ad39f5c4bf834736bb2ee04b031eebbcdb11ce0` | `7c0817f20e4f1b8fa14696597bbb549b45184572` |
| Frozen027 Agent native contract | `027bd16d96010544331c953c0e1014e161786e71` | `1434f42b48fd062248faf1f4abef7ff467186377` |

Runtime introduction merge: `e068f27dac058b499716671db93e459fc7b656f7`. `git diff e068f27 1ad39f5 -- runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_inputs.py runtime_protocol/service.py runtime_protocol/server.py runtime_protocol/door.py contract packages tests/test_timeline_pack_document_read.py` is empty. The reviewed read, clients, contract and owner tests therefore match that introduction at the reviewed head.

Normal release metadata (`packages/typescript/src/contract-metadata.ts:3-6`): client **0.2.8**, schema `sha256:a4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a`, component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`. Artifact producer version (`contract/artifacts.json`): `sha256:4010d93be2a8bfc7cc051c383e165ff81835c3d12ba9a137279741b7883748a7`.

Reviewed file identities, computed from `git show 1ad39f5:<path>` with SHA-256:

| Runtime path | SHA-256 |
| --- | --- |
| `contract/artifacts.json` | `e747db225aa37553b10bfc9c5b36ad6e360ed4f3a052cabb012b83d051dd1e17` |
| `contract/openapi/workspace-v1.yaml` | `578cf2336dcc9ff12f68738a91608fbc13f606964ae1bdc48219ea467f37a07d` |
| `contract/schemas/timeline-commit.json` | `7676f0112799fe4bd140b88e49590d5c0789c229c4702235a4f6e705187b05b8` |
| `contract/schemas/edit-command.json` | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| `packages/typescript/src/generated.ts` | `449ece47770caaded1fba0f141433485272d7380756e69f98621389552117592` |
| `packages/typescript/src/timeline-commit-types.ts` | `2e788219cda7f25c9bb88e84e7d2ccaabc9a4fe49c7aef1f3e199977cc73022e` |
| `packages/typescript/src/contract-metadata.ts` | `f47783153a81f139887bd13816b4a53d2e300ba72c8681ff1183863552f084d9` |
| `packages/python/astrid_runtime_client/generated.py` | `48fe21b010b73a9e7108af78afff2fade31594e4bf6be312511a8fa3b8675095` |
| `runtime_protocol/timeline_commit_port.py` | `eaaff2727c9fbee8285607962f35c38e8281d138503c4a9c114af78bf759bd54` |
| `tests/test_timeline_pack_document_read.py` | `cbbb1696a376215eb067ab3febf27df6b82b2d62ad317d9dc1d52ddf3b3b0702` |

Read PLAN first, the 03:31 owner decision at `managers/app/INBOX.md:660-664`, prior worker report/probe and `design/app-retained-param-read-review.md`, escalation0429, and `design/app-bootstrap-init-adoption-review.md` for boundaries only. Bootstrap/publisher adoption and its holds are separate and remain unchanged.

## Actual published calls and response mapping

Runtime `packages/typescript/src/generated.ts:182-183` publishes exactly:

```ts
getProjectVerifiedDocument(projectId: string, pin: DocumentPin): Promise<VerifiedDocument>
getProjectVerifiedDocumentObject(projectId: string, pin: DocumentPin, objectId: string): Promise<VerifiedDocumentObject>
```

Python `packages/python/astrid_runtime_client/generated.py:920-926` publishes `get_project_verified_document(project_id: str, pin: DocumentPin) -> VerifiedDocument` and `get_project_verified_document_object(project_id: str, pin: DocumentPin, object_id: str) -> VerifiedDocumentObject`.

These are ordinary authenticated GETs, with no mutation receipt wrapper or idempotency key:

| Call | Route and required query | Direct JSON result |
| --- | --- | --- |
| document | `/v1/projects/{project_id}/document-inputs/verified`; `document_id, version, content_digest` | `{pin, document}` |
| selected object | `/v1/projects/{project_id}/document-objects/verified`; same pin plus `object_id` | `{object_id, digest, size, media_type: 'application/json', bytes_base64}` |

`DocumentPin` is only `{document_id: string, version: positive integer, content_digest: sha256 digest}`. OpenAPI is `contract/openapi/workspace-v1.yaml:312-335`; its response refs lead to `contract/schemas/timeline-commit.json:360,1272,1288`. Generated TS types are `timeline-commit-types.ts:37,78-79`; the broader generated `Document` type does not authorize the caller to fabricate its body. Both methods are generated by the normal generator (`generators/generate.py:222-223`), not local client additions.

For a valid original pin and the selected clip's canonical `elementRef` (fallback `element_ref`), the complete mapping is:

1. `verified = await client.getProjectVerifiedDocument(projectId, originalPin)`.
2. In `verified.document.content`, require the pack owner to match selected `packId`, and find the unique admission matching selected `id/kind/revision`. Its `snapshot_object.object_id` is the object ID; element revision, snapshot digest and document digest are distinct identities.
3. `snapshot = await client.getProjectVerifiedDocumentObject(projectId, originalPin, objectId)`. Read only this selected object, not every pack admission.
4. Feed the unmodified `verified` and `{[objectId]: snapshot}` into frozen027's existing `capture_clip_set_params(bundle, selectedClipRef, values={'seed': 8}, schema_source=originalPin, schema_inputs=[(verified, objects)], realm_id=authenticatedRealmId)`. This is a mapping to the existing Python native signature, **not** an assertion that this App already exports a TS equivalent.

Exact native consumers: `_scalar_commands.py:98-128,150-164`, `project_packs.py:536-701`, and provider `commit.py:347-449`. Native code checks pin/version/content digest/project, stable document ID/realm/owner/manifest path, unique admission, exact selected object descriptor/base64/size/hash, bounded resource closure, successful build identity and selected element revision. It records `params.schema`, `params.snapshot`, `params.element` and the verified pinned document. Those existing checks retain native authority; App merely assembles read results for capture.

The unchanged actual fixture/provider inputs were inspected, rather than substituted with the Runtime range-test fixture: frozen027 `tests/editing_conformance/test_recipe_scalar_commands.py:35-69` produces `schema_options` from real native admission and managed object bytes; `tests/sdk/test_timeline_selected_schema_runtime.py:28-140,404-515` uses those same input shapes, real provider, max10/max20/removal/cache deletion/restart/retry/inverse/redo and identity/corruption negatives. Runtime's portable `VerifiedDocumentObject` shape is exactly what the frozen resolver accepts. No detached or synthetic capture probe was needed or run for this source-shape conclusion.

## Authorized closure, retention, custody and races

| Runtime anchor at reviewed SHA | Review finding |
| --- | --- |
| `door.py:168-169`; `server.py:520-566` | Both normal Door reads require `projects:read`. Query parsing refuses malformed percent/UTF-8 encoding, missing/extra/duplicate/blank fields and nonpositive/noninteger version. The document call does not accept `object_id`. |
| `server.py:264-268`; `service.py:2365-2383,2503-2525` | Authenticated actor is rechecked through the existing timeline read callback; canonical project must belong to the realm. Pin is detached. Authorization runs before reads and again under the store mutex. No timeline/publication argument was added to either public method. |
| `timeline_commit_port.py:437-477,493-511` | Both use pins linked by accepted records **within this project**, then `capture_document_input`. Document kind must be a registered config or project pack. The new method returns `{pin: capture.pin, document: capture.document}` instead of discarding the document as the object-only method did. |
| `timeline_commit_inputs.py:341-397,452-489` | Retained binding lookup is exact project/document/version/digest and requires linked reachability; retained SQL content is checked for canonical bytes, size and digest and binding/source identity. Capture uses a DB transaction; absent retained binding falls back only to an exact live version/digest. It cannot substitute V2 for V1. |
| `timeline_commit_inputs.py:233-323`; `timeline_commit_port.py:479-491` | Pack scope/owner/document identity, unique admissions and managed project-object metadata are validated. Selected object must belong to captured document; bytes are bounded, CAS size/hash checked, file identity compared before/after read. No source/cache/UI descriptor is authority. |
| `timeline_commit_port.py:284-326,328-369` | Normal commit independently captures its declared/base/history-authorized inputs and revalidates documents, object bytes/file identities, manifest and recorded dependencies before acceptance. A public project read does not grant commit authority for another timeline's historical pin. |

Public reads use project-wide accepted-record reachability, as documented by their OpenAPI and prior approved object read. The commit port instead uses its authorized base/shot/history closures and declarations. These are not interchangeable claims of authority. A caller with an exact pin can read retained project data, but cannot make a pin usable by a particular timeline merely by reading it.

The document and object reads are two separate transactions, not a new multi-read snapshot. Every response is bound to the same original pin; a live document change/removal between calls either permits the still-retained V1 or fails explicitly. Object changes/custody loss refuse. Normal commit rechecks its own inputs and history; no App read result waives those checks. This is source-reviewed protection, not a new executed concurrency claim. Destructive deletion of managed custody is a refusal case, not a promise to recover missing bytes; removal of live document/source/cache is the retained case.

## What the NEW owner tests actually prove

Source-inspected only, **not executed by this worker**, at `1ad39f5`:

- `tests/test_timeline_pack_document_read.py:76-109`: real Runtime port/service commits using `install_param_provider`, retained V1 max10, V2 max20, document deletion and service restart, with 8 accepted and 16 refused and no SQL change on refusal. Despite the test name `test_native_capture_commits_against_retained_v1_after_v2_removal_and_restart`, this is **not the actual native PARAM engine**: the command is `fixture.pack-param`, provider is `PreparedProvider`, and validation is `1 <= value <= maximum` over a simplified `{params: {count: ...}}` object (`:35-73`). Do not cite it as native `clip.set-params` acceptance or native goldens.
- Same file `:112-164`: public service read equals `{pin, document}` and the port's captured source after V2/removal/restart, no SQL writes; generic retained config also covered. This supplies the exact fact missing from 0.2.7.
- Same file `:167-210`: bad/stale/wrong-digest/foreign/unreachable/unknown/wrong-kind/tampered/removed-without-binding cases refuse, as does revoked authorization; SQL snapshots unchanged.
- Same file `:213-262`: actual normal generated Python client and Door document read after V2/removal/restart; selected object ID discovered from the response and object read returns V1 bytes; malformed query and scope/digest negatives. The bytes are the simplified range fixture, not a real native portable pack envelope.
- `tests/test_timeline_commit_contract.py:393-421` and `packages/typescript/test/client.test.mjs:29-44`: schema/signature, exact GET/query and unwrapped response transport contracts. TS public request is covered with a fake transport; do not call it live App qualification.
- Existing `tests/test_timeline_pack_param_retained_read.py` retains object custody, mismatch/unreachable/auth/scope negatives. Frozen027 native `test_timeline_selected_schema_runtime.py` retains the stronger actual native behavior requirements. Neither suite was changed or rerun here.

Thus the **read API is now shape-complete**; the missing end-to-end proof is the new public responses carrying actual native admission fixtures through native capture/acceptance on an official owner-frozen cohort. Do not report the simplified owner test and the old native suite as one paired execution.

## Remaining required owner/client and App steps

1. **Owner matching cohort and authority:** publish/freeze the exact matching Agent/provider + Runtime + generated Python/TS artifacts with schema/artifact digests and supported runtime. Frozen027 is the input-contract reference, not automatically a compatible install with current Runtime; this review makes no current-cohort compatibility claim. Prior Bundle1 (`3bf9e536`/`6be97063`, client0.2.2) and Bundle2 (`027bd16d`/`4c145dc6`, client0.2.3) remain unchanged. Do not override an installed/vendored Runtime via `PYTHONPATH` and describe it as paired.
2. **Original pin selection:** retain exact session project/timeline/revision/publication authority. For an already pinned source, use the verified accepted dependency manifest/history and selected element identity; the returned V1 document now discovers the selected object even if old PARAM records lack `params.snapshot`. If first-use selection has no Runtime-established exact source pin, this read cannot discover it from only `elementRef`; the owners must identify/qualify that existing authoritative pin flow. Neither latest `getDocument` followed by an App hash nor a UI registry digest qualifies. No new route/field is proposed here.
3. **Official client adoption, then bounded App adapter:** current task App `generated-contract-metadata.ts:3` is 0.2.1, `runtime.lock.json` source is `182a7dd8446456162a452a25c8493256c5da29fe`; neither read exists in its generated client. Only after the owner paired freeze should the manager sync normal generated artifacts/pins. Then implement the two-read selected-input adapter and native-compatible capture, preserving exact authored leaf/identity/selection guards and staging commands in sequence. Do not manually patch generated source, invent local DTOs, or hydrate/rebuild an authored document to authorize the schema.
4. **Required proof before cutting selected-PARAM writer:** actual unchanged native admission/provider fixture; normal public document+selected-object reads; complete native captured command/guards/records goldens; 4→8 under retained V1 max10 and refusal of raw16 after V2 max20/removal/source-cache deletion/restart; exact retry, reload, inverse/redo, unknown literal/clear/opaque preservation and selected-only I/O. Keep all pin/owner/id/kind/revision/missing/mismatched/corrupt/foreign/unreachable/authorization/object custody negatives. Then qualify App browser reload/retry/inverse centrally when authorized and retire the writer with its ledger row. Current explicit changed-selected-pack refusal and writer OPEN status remain requirements; no behavior test was rewritten to encode a lost positive.

No new decision was needed. Applied the settled 03:31 boundary; chose source review instead of an artificial fixture probe because native fixtures already show the exact contract and the new Runtime fixture is deliberately not that contract. The owner-test name overstates native coverage; this is a reported evidence limitation, not a deviation from the plan.

## Executed evidence and limits

Cwd `/home/user/work/wt/app-m2-retained-document028-review`:

```sh
node node_modules/vitest/vitest.mjs run src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx --maxWorkers=1 --no-file-parallelism
```

**Exit 0; 2 files, 5 tests passed; 4.44 seconds.** Existing App parameter inspector/selection/literal/draft behavior only, with jsdom and mocked hosts; not native capture or public-read acceptance. This cc4 App base has no `clipParamsCapture.ts` or native selected-PARAM test to run. Prior reports' later adapter file anchors must not be applied to this base.

`git diff --check` → exit 0, no diagnostics; `git status --short` → exit 0, empty (App worktree unchanged). Seven reviewed generated/schema artifact byte digests were independently compared with the fixed normal artifact manifest: all match. No App tracked source/test changes, no extracted source copies or build outputs. No Runtime edits, duplicate Runtime full, runtime suite, detached native probe, service/localhost/socket/browser run, install, build, project tsc or full-suite request. Runtime owner tests were inspected only. Actual new public-read/native integration, current matched-cohort acceptance, first-use unpinned selection and App adapter/browser behavior remain **unverified**.

Review deliverables are retained here and exported flat to `design/handoff-app-retained-document028-review.md` for manager review before any copy/adoption. The review task is complete; the writer task remains open on the explicit steps above.
