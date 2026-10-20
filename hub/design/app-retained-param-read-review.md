# Retained selected-PARAM public-read readiness review

**Verdict: the decisive retained-document gap remains in candidate 0.2.7.**
`getProjectVerifiedDocumentObject(projectId, pin, objectId)` supplies the selected
object bytes, provided the caller already knows its ID. It does **not** supply
`VerifiedDocument {pin, document}`. No other generated public retained document
read was found at the reviewed candidate. Therefore this exact candidate cannot
supply all frozen027 native capture inputs after V2/removal/restart without an
additional document source. It is UNFROZEN; App selected-PARAM writer stays OPEN
and the existing explicit refusal stays intact.

This is evidence that the candidate incompletely implements the orchestrator's
03:31Z retained-read decision, not a reason to change that decision. That decision
explicitly covers both existing `config_source` and `document_object` facts.
See `managers/app/INBOX.md:660-664`, `PLAN.md`, and
`design/app-params-source-read.md`. No product, adapter, generated source, pin,
port, schema, or field is changed by this review.

## Exact reviewed sources

All Agent/Runtime anchors below are **at these commits**, read with `git show`.
They are not anchors into mutable integration worktrees.

| Source | Commit | Tree / release |
| --- | --- | --- |
| App base `tl/app-m2-ordinary-qualified-compose` | `4f79aea853a53852f50456ac295588c19016f1f7` | `2658e872d1c99ad9addcd979d8ce78803bfd4312` |
| Agent frozen027 | `027bd16d96010544331c953c0e1014e161786e71` | `1434f42b48fd062248faf1f4abef7ff467186377` |
| Runtime read-only `hub/tl/rt-m2-pack-param-retained-read2` candidate | `8308cb9c153df3d7a5fdaf492af075be5b18e670` | `3049c59990ef705e25d025167cc457d837a6149d`; generated client `0.2.7` |

Candidate metadata is `packages/typescript/src/contract-metadata.ts:3-6`:
schema `sha256:7486348fccf16b9104aa47d2076b68d1163931f765d8a4e7ec29415b5083bf22`.
This records identity only; neither artifacts nor pins were adopted or qualified.
Frozen Bundle1 Agent `3bf9e5368a956ef562c77e1beb0a745addf23daf` /
Runtime `6be970633cc82ab412428151e6bf42f3e7fc3081` / client `0.2.2`, and
Bundle2 frozen027 / Runtime `4c145dc62192f0e942e3ee3922a11488aefe9b41` /
client `0.2.3`, remain untouched. No paired 0.2.7 freeze is claimed.

## Actual native input contract

Agent `astrid/sdk/timeline/_scalar_commands.py:150-164` accepts:

```python
capture_clip_set_params(
    bundle, selected_clip_ref, values={'seed': 8},
    schema_source=pin,
    schema_inputs=[(
        {'pin': pin, 'document': exact_project_pack_document},
        {selected_object_id: verified_document_object},
    )],
    realm_id=authenticated_realm_id,
)
```

`DocumentPin` is exactly `{document_id, version, content_digest}`.
`VerifiedDocumentObject` is exactly the existing descriptor plus `bytes_base64`:
`{object_id, digest, size, media_type: "application/json", bytes_base64}`.
Runtime generated `packages/typescript/src/timeline-commit-types.ts:37,78-79`
declares these separate types; exporting `VerifiedDocument` does not provide a
method to retrieve it.

Native changed selected-pack capture requires the scoped realm, exactly one
verified input matching `schema_source`, and the document's selected admission
matching `id/kind/revision`. It takes that admission's `snapshot_object.object_id`
to index the objects map (`_scalar_commands.py:65-89,98-119`). The pure resolver
then validates document version/digest/project/kind, stable document ID, owner,
manifest path, unique admission, exact object descriptor/base64/hash/size,
bounded resource closure, build identity, pack manifest and element revision
(`astrid/core/element/project_packs.py:536-701`). The portable object's JSON is
`{files, build_receipt_base64}` (`:145-193`); it is not the project document or its
admissions list. A valid object hash does not recover that document.

Capture records `params.schema`, `params.snapshot` and `params.element`, and
copies the verified document into `source_mapping.pinned_documents`
(`_scalar_commands.py:120-128`). Known changed values are validated using native
Draft202012 semantics without defaults/coercion; clears, unknown literal keys,
unchanged legacy values and unrelated opaque data retain existing behavior
(`:65-95,131-143`). The review does not loosen any identity/leaf/selection guard.

The real Agent provider already has the complete flow internally:
`astrid/sdk/timeline/commit.py:347-389` calls `port.config_source(pin)`, verifies
the exact scoped document and creates `(verified, {})`; `:392-449` finds the
selected admission and calls `port.document_object(pin, object_id)` only for
that object, including inverse and older-record handling. This is precisely
the missing document fact at the public boundary, not App hydration work.

## Public read, service and authority trace

| Candidate source anchor | Actual behavior |
| --- | --- |
| `packages/typescript/src/generated.ts:182`; Python `packages/python/astrid_runtime_client/generated.py:920-922` | Requires project, exact pin and object ID; returns only `VerifiedDocumentObject`. TypeScript has no `Promise<VerifiedDocument>` method. |
| `contract/openapi/workspace-v1.yaml:312-322` | Four required query fields (`document_id`, `version`, `content_digest`, `object_id`); 200 schema is `VerifiedDocumentObject`, not `VerifiedDocument`. |
| `runtime_protocol/door.py:168`; `runtime_protocol/server.py:520-555` | Normal GET allowlist; `projects:read`, existing timeline read authorization; strict complete query, duplicate/unknown/blank/invalid encoding and version refusals. |
| `runtime_protocol/service.py:2612-2631,2750-2760` | Requires authenticated callback and canonical project in realm, checks under the store mutex, detaches the pin, translates commit refusals to public errors. |
| `runtime_protocol/timeline_commit_port.py:463-481` | Validates pin/digest, gets reachable pins from accepted input links **in the project**, calls `capture_document_input`, then `_pack_object`; discards the captured document from its public return. It does not infer reachability from a hash. |
| `timeline_commit_port.py:449-460`; `timeline_commit_inputs.py:274-323` | Requires captured project pack, checks object membership in that document, managed project association and metadata, byte limit, CAS file identity/size/hash. |
| `timeline_commit_inputs.py:341-397,452-489` | Exact retained SQL content and binding reconstruction, canonical content hash/size checks and retained reachability; otherwise exact live version/digest. This successfully produces the document internally. |

In-process `config_source(pin) -> VerifiedDocument` remains present at
`runtime_protocol/timeline_commit.py:38` and `timeline_commit_port.py:284-326`.
The candidate shares the object read with that port, not the public exposure of
the document read. Internal availability is insufficient for browser capture.

Other public surfaces were checked rather than treating the new endpoint name
as proof:

- Generated `getDocument`/`listDocuments` have no version/digest selector
  (`generated.ts:139-140`; Python `:779-786`). Service
  `service.py:4540-4554` reads only current `project_documents`. V2 yields V2;
  deleted rows yield not-found. There is no retained lookup on this path.
- Immutable parent/shot/internal revision and history reads exist
  (`generated.ts:163-167,179`), but `CanonicalDocument`/`ShotClosure` carry
  **document pins**, not their document bodies (`timeline-commit-types.ts:57-59`).
  `timeline_commit_store.py:265-296` checks retained input integrity internally
  and returns the closure; it does not attach those SQL document bodies.
  Agent `commit.py:146-158,276-282` likewise preserves pins, without serializing
  capture-only `pinned_documents` into the canonical document.
- `inspectTimeline` is a projection of the immutable parent and children
  (`service.py:2786-2790`, `timeline_inspection.py:552-580,751-776`);
  `createTimelineView` renders that inspection (`service.py:2792-2813`). Neither
  is an exact retained project-pack document read.
- Generic object reads/list/location provide bytes or metadata, without the
  exact retained declaration/admission association. Content digests address
  retained SQL JSON (`timeline_commit_inputs.py:341-361`), not a published CAS
  copy of the project document. Enumerating objects cannot establish admission.

## How the caller learns the selected object ID after removal

The authored raw `elementRef` (preferred over `element_ref`) carries
`id/kind/packId/revision`, not `snapshot_object.object_id`. Element revision,
resource-closure `snapshot_digest`, object digest and document digest are distinct.
The native provider discovers the object ID by reading the exact document first
(`commit.py:421-438`). The public candidate requires it as an input before it
will return anything.

There is one useful existing discovery case: after a **native PARAM commit**,
public `listTimelineCommits` can expose the recorded `params.snapshot` dependency
`{source, element, object}` and hence its object ID (generated method `:179`,
history/record types `timeline-commit-types.ts:60,73-74`; producer
`_scalar_commands.py:121-123`). This must be matched to the original pin and
selected identity. It is not a general discovery guarantee: older PARAM records
may lack this dependency (Agent `commit.py:411-420`), and a manifest alone carries
only a pin. Prior knowledge/cached admissions may also provide the ID, but the
required cold/restarted path cannot depend on a caller retaining that cache.

Even **granting the exact original pin and correct object ID**, the new response
does not contain `verified.document`. History dependencies do not contain the
complete document either. Thus object-ID discovery does not resolve the decisive
gap. First-use selection must also obtain a Runtime-established exact pin; this
review does not authorize App to manufacture one from a current/UI descriptor.

## What the Runtime tests establish, and what they do not

Source-inspected, not executed in this review:

| Test source at 8308cb9 | Evidence encoded by the test |
| --- | --- |
| `tests/test_timeline_pack_param_retained_read.py:35-59,72-105` | Retained max-10 **object bytes**, V2/removal/restart, no SQL writes, distinct V2 object/pin. `accepts()` is the local expression `1 <= element <= decoded(value)["params"]["count"]["max"]`. |
| Same file `:108-170,190-220` | Pin/scope/unreachable/object/auth/custody refusals and generated Python plus normal-door object read after restart; unchanged SQL snapshots. |
| `tests/test_timeline_pack_inputs.py:38-83,397-417` | The new tests install a `PreparedProvider`, submit `fixture.pack-input`, and call internal config/object ports. They do not execute native `clip.set-params`. |
| `tests/test_timeline_commit_contract.py:362-390`; `packages/typescript/test/client.test.mjs:28-44` | Query/response shape and transport contract for the object response. |

The new test's declaration is `{"params":{"count":{"min":1,"max":10}}}`;
this is neither the native portable `{files, build_receipt_base64}` envelope nor
the full verified document. Its local `accepts(4/8/16)` assertions prove JSON
interpretation, not native capture or Runtime PARAM acceptance. The tests retain
value as custody/transport tests; they do not satisfy the required native public
input flow.

The materially stronger existing frozen Agent test is
`tests/sdk/test_timeline_selected_schema_runtime.py:404-460`: real native PARAM
capture/acceptance, original guarded replay, V2 max20, removed live admissions,
deleted source/build cache, restarted Runtime, exact retry, refusal of raw 16,
inverse/redo and opaque preservation. It receives complete native inputs via
the in-process port. It does **not** qualify this candidate public read. Its
identity/corruption refusal neighbors `:463-515` and the earlier selected-only
I/O/staged-command tests remain required. None were changed or rerun here.

## Executed bounded pure counterexample

Reproducible probe:
`workers/app-m2-retained-param-read-review/notes/probe.py`. Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-retained-param-read-review/notes/probe.py
```

**Exit 0; 8 bounded checks passed** on the final script. It reads frozen Agent
source via `git archive` into a self-cleaning temporary directory, uses an
existing native bundle fixture, and constructs in-memory document/resources/
synthetic receipt in the actual published shapes. Native code derives and
checks descriptor revision, hashes, portable envelope and admission. A synthetic
receipt here is test data, not evidence of a real build or Runtime authority.
Runtime/renderer imports are tripwired; no service or socket is used.

1. Complete `(VerifiedDocument, {object_id: VerifiedDocumentObject})`: native
   4→8 capture/execute succeeds, opaque value survives, original bundle unchanged,
   exact pinned document plus `params.schema`/`params.snapshot` recorded.
2. Same complete V1: 16 refuses, `16 is greater than the maximum of 10`.
3. Correct object available but no verified document input: 8 refuses,
   `selected pack snapshot input unavailable`.
4. Pin plus public object fields in place of the document: refuses,
   `Unsupported project pack payload schema/source binding`.
5. Complete verified document without selected object: refuses,
   `Invalid verified pack snapshot object`.
6. Current document with removed admissions and a different current pin cannot
   match V1: refuses, `selected pack snapshot input unavailable`.
7. Relabelling that removed document with the old pin cannot restore admission:
   refuses, `Element owner/revision is not admitted for this project`.
8. Candidate generated source confirms object-only return and no public
   `Promise<VerifiedDocument>` method.

The pure probe establishes native sufficiency/refusal of the **input shapes**,
not actual V2 persistence or public read execution. No end-to-end native golden
equality or public Runtime acceptance claim is made.

## Smallest owner reconciliation and remaining qualification

Runtime/Agent owners should complete the already-approved exposure of the
existing exact retained **`config_source(pin) -> VerifiedDocument` fact**, under
the established project/closure/reachability checks. The document then supplies
the selected admission's object ID; the reviewed object read can supply its
bytes. Preserve the existing native DTOs and capture contract. This review does
not choose a new route/port/schema/field or propose a workaround, and gives App
no new authority, hydrator, reconstructed declaration or caller-hashed pin.

Before a paired freeze, prove that the normal generated public reads alone
supply the exact document and selected object after V2/removal/restart, then
feed those unmodified inputs into frozen/reviewed native capture: full command,
guards and record golden equality; 4→8 acceptance and raw 16 refusal under V1
max10; actual Runtime reload/retry/inverse/redo and existing adversarial refusals.
After owners ship/freeze that pair, App can stage the bounded adapter and perform
the required browser journey before retiring the writer.

App `src/tools/video-editor/commands/clipParamsCapture.ts:33-43,97-106` remains
unchanged: changed selected-pack values refuse, and the unsupported
`schema_source` argument is not silently accepted. No positive behavior test was
rewritten into a refusal, skipped, deleted or weakened. Native/current product
files and all frozen pairs remain untouched.

**Unrun by task restriction:** installs, builds, tsc, full suites, browser,
sockets, services/test-service requests, live candidate public reads, real
candidate Runtime PARAM acceptance and App adapter/golden/browser qualification.
This source review is complete; selected-PARAM readiness remains blocked on the
owner reconciliation above.

## 05:42 NEWRuntime0.2.8 readshape reviewed, previousspecificblockerCLOSED
ExactRuntime1ad39f5/tree7c0817f2, normalclient0.2.8/schemaa4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a/artifact4010d93be2a8bfc7cc051c383e165ff81835c3d12ba9a137279741b7883748a7. OfficialgetProjectVerifiedDocument(projectId,pin)->{pin,document} andgetProjectVerifiedDocumentObject(projectId,pin,objectId)->existingVerifiedDocumentObject nowprovidecompleteinputs. Sourceownerreadreusesauthorizedacceptedclosure/configSource binding/retainedcapture/custody/mutex andacceptancerecheck; no Apphydrator/hashauthority. Exactnormalpublishedcalls+source/10filehashes+native027mappingandlimitsin design/handoff-app-retained-document028-review.md. Previous0.2.7object-onlyfindingstillaccuratehistorical, new0.2.8resolvesit; NOTAppselectedPARAMwriterready. GivenoriginalapprovedexactV1pin, findunique selectedadmission+readoneobject, forwardunmodifiedresults toexistingnativecapture. Apppin0.2.1lacksbothmethods; normalofficial0.2.8source stagingdispatched, normalAgentownedpin+reviewedcohortfreeze+adapter/nativegoldens/actual4→8/max16refusalafterV2/removal/restart/browserretry+inverse remainrequired. No mixedfrozenpair/inlineauthority/retirementclaim.
