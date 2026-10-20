# App selected-pack PARAM: exact public source read is missing

Source review, 2026-10-20. **BLOCKED at the public read boundary; no product
adapter staged and no full PARAM coverage claim.** The existing refusal remains.
This records the task's stop-code outcome, not a new endpoint/DTO/port proposal.

## Frozen sources

| Repo | Reviewed source |
| --- | --- |
| App | `823d078daa27081dabc360037de1aaaa2bb1a408`, tree `d205ba2a36ca4dfe0e95d2744f66da445d75aedd` |
| Agent | `027bd16d96010544331c953c0e1014e161786e71`, tree `1434f42b48fd062248faf1f4abef7ff467186377` |
| Runtime | `4c145dc62192f0e942e3ee3922a11488aefe9b41`, tree `f640ccf4aacb08e15f493bc7e3e5befe26ed0ceb`, client `0.2.3` |

Agent/Runtime anchors below are paths and line numbers **at those commits**, read
with `git show`, not today's integration sources. Their old worker directories
are absent. App's generated client/types/metadata match this Runtime byte for
byte. No `0.2.6`, D13, union, package, wire or shared Composition change is needed
or made for this finding.

The requested `_immutable_inputs.py` is absent from both frozen trees (including
Agent `astrid/sdk/timeline/_immutable_inputs.py`). The actual retained-input
implementation is Runtime `runtime_protocol/timeline_commit_inputs.py`, used by
`timeline_commit_port.py`; Agent hydration is in `astrid/sdk/timeline/commit.py`.

## Exact selected input the native capture consumes

Agent `astrid/sdk/timeline/_scalar_commands.py:65-143,150-164` selects raw
`elementRef` before `element_ref`, requires a scoped `realm_id`, and accepts the
existing `schema_source: DocumentPin` plus detached capture inputs:

```text
schema_source = {document_id, version, content_digest}
schema_inputs = [(VerifiedDocument, {selected_object_id: VerifiedDocumentObject})]
VerifiedDocument = {pin: schema_source, document: exact_project_document}
VerifiedDocumentObject = {
  object_id, digest, size, media_type: "application/json", bytes_base64
}
```

This is the native published shape, not an App wire extension. The command
contains only the pin, values and clears; snapshot inputs do not grant acceptance
authority. Existing types are App `src/integrations/runtime/timeline-commit-types.ts:37,78-79,90-91`.

Native requirements:

- The document must match the pin's exact version/content digest and project;
  its kind/schema, deterministic document identity, realm/project manifest path
  and pack owner must match the selected element. Match exactly one admission by
  `id/kind/revision`, including selected `packId` ownership.
- Use that admission's `snapshot_object` and only that object's bytes. The pure
  Agent validator verifies descriptor equality, canonical base64/JSON, size and
  hashes, bounded resource closure, build identity, manifest and exact descriptor
  revision before reading its schema. It never uses a caller's display schema.
- Record native `params.schema`/`params.snapshot` dependencies and
  `params.element` binding, retain the exact verified document in source mapping,
  and preserve all existing identity/leaf/selection guards.
- Validate only changed known properties, with native draft-2020-12 reference
  behavior and no defaults/coercion. Unchanged legacy values, unknown literal
  keys, clear-only edits, absent/null containers and opaque siblings survive.

Anchors: Agent `_scalar_commands.py:99-143`;
`astrid/core/element/project_packs.py:536-701`;
`astrid/sdk/timeline/commit.py:347-449`. The resolver fetches selected bytes at
the real command stage and caches by pin/object, including staged add→PARAM and
inverse; it does not fetch all admission objects.

## Existing reads audited

| Existing surface | What it provides | Why it cannot close this seam |
| --- | --- | --- |
| App generated `getDocument(projectId, documentId)` (`generated.ts:16,140`); wrapper `client.ts:589-590`; `RuntimeDataProvider.documents.get` (`dataProvider.ts:376-380`), `ProjectDocumentSurface.get` (`src/sdk/context.ts:103-109`) | Authenticated current project document with version/content | No exact version/digest selector, retained binding lookup or returned immutable pin. Runtime OpenAPI `contract/openapi/workspace-v1.yaml:136-145`, server `runtime_protocol/server.py:682-690`, service `runtime_protocol/service.py:4529-4534` read only `project_documents`. A caller-side hash cannot recover an unavailable V1. |
| Public parent/shot/internal revision reads and accepted `CanonicalDocument` | Immutable authored revisions and dependency document pins | `CanonicalDocument`/`ShotClosure` contain document pins, not verified document contents or pack-object bytes (`timeline-commit-types.ts:57-59`). Runtime generated revision methods `packages/typescript/src/generated.ts:163-166` do not expose `config_source`. |
| App `getObject(objectId, range?)` (`client.ts:850-852`, generated `generated.ts:233`) | Authenticated CAS bytes, status/headers/ETag; Runtime verifies CAS size/hash | Its selector has no project/document pin or authorized timeline closure. It cannot establish the object's membership in an exact retained pack document. Runtime `server.py:857-865`, `service.py:5436-5455`. Byte integrity is useful but does not supply the missing declaration. |
| Project object list/location (`generated.ts:227-228`, wrapper `client.ts:710-711`) | Project-managed object metadata; location verifies bytes and returns a local path | No document version/admission association or retained declaration. Location is explicitly local and not a portable receipt (`service.py:5460-5501`, OpenAPI `:210-215`). Pairing it with raw bytes still leaves the exact historical document unavailable. |
| UI `AstridElementHost.descriptors`, `resolveAstridElementParamDescriptor` | Schema matched by exact `id/kind/packId/revision` | Correct display identity does not include `DocumentPin`, exact document content or `VerifiedDocumentObject` (`astrid-element-host.ts:17-25,52-62`; `astrid-element-param-descriptor.ts:24-49`). |
| Vite project element selection / admission module | Current document + native resolver + local artifact/source verification for preview | `config/vite/projectElementSelection.ts:25-90` reads current documents, verifies a resolver binding and local snapshot paths. `config/vite/vite.config.ts:97-110` uses the existing Runtime session and a configured native process. The browser POST returns module URL/digest (`astridElementAdmissions.ts:175-189`); generated module strips snapshot fields (`:135-140`). It has no retained-pin selector or portable exact document/object read. `src/tools/video-editor/runtime/admitted-elements.ts:17-20,57-99` consumes this module, not native schema inputs. Do not promote UI registry data or its selection digest into capture authority. |

The normal `withSession` wrapper already exists (`client.ts:506-527`), so
authentication is reusable. It cannot add missing read semantics. The UI
selection/build digest, admission resource-closure `snapshot_digest`, document
`content_digest` and snapshot CAS object digest are distinct; none substitutes
for another. In particular, retained document content is stored in Runtime SQL,
not made a public CAS object by its content digest.

The current-document and authenticated object reads do carry useful first-use
data while the requested pin is still live. This review does not establish that
they are unusable for every live selection. The decisive missing fact is the
authorized **retained document content** after the live version changes. A
current-only adapter, even with correct object bytes, would leave that required
case unsupported. Whether raw object/location reads can be reused once the exact
retained declaration is available should remain part of the bounded follow-up;
this finding does not demand a new object endpoint.

## Where the required facts already exist internally

Runtime `runtime_protocol/timeline_commit.py:24-41` exposes
`config_source(pin) -> VerifiedDocument` and
`document_object(pin, object_id) -> VerifiedDocumentObject` only on the in-process
commit provider port. `timeline_commit_port.py:285-350` requires declared/reachable
pins, captures the document, checks object membership, and reads the managed
project object with custody checks. These are not generated public client reads.

`timeline_commit_inputs.py:452-482` loads the exact retained binding only when
reachable from the authorized closure; otherwise it requires the live row to
match the exact version and digest (`:408-448`). Retained SQL content is checked
and rebuilt at `:341-397`. Object management/size/hash/file-identity checks are at
`:294-323`. Module lines `1-7` explicitly describe the lack of a public route.

**Missing read/input:** an authenticated public way to obtain that same exact
project document for the original `DocumentPin`, including an authorized retained
V1 after V2/selection removal/restart. Capture also needs only its selected
admission object as the existing verified object shape. Reuse existing object
reads if they can supply the same verified input. The read must preserve Runtime's
closure/reachability, managed-project association and race checks. The immutable
timeline/revision/publication context needed to authorize retained access must
come from the original session, not be inferred from object hashes. First-use
selection also needs a Runtime-established exact pin; do not manufacture it
from anonymous registry descriptors. This describes the missing facts, not new
wire fields or a chosen route design. Runtime/Agent owners must settle exposure;
App cannot implement it by adding a second hydrator.

Concrete failure: accept PARAM against V1 (maximum 10), publish V2 (maximum 20),
remove live admissions, delete native source/build caches, restart. Native code
still reads the retained V1 and refuses 16; public `getDocument` returns the
newer empty selection. App cannot reconstruct V1 from its manifest pin, replace
it with V2, or recover it by hashing/falling back to a preview snapshot.

## Preserved behavior and future qualification

No App product/test/fixture change. `clipParamsCapture.ts:33-54` continues to
refuse changed selected-pack values; `:97-106` still rejects `schema_source`
because the adapter does not yet support it. This is an explicit coverage gap,
not native selected PARAM parity. Existing builtin/null/clear/opaque/no-op paths,
native golden bytes and every original guard remain unchanged. In particular,
the existing selected refusal test (`clipParamsCapture.test.ts:99-106`) is not
evidence that supported selected editing is complete.

Permanent native cases inspected (not executed here):

| Required future App/central evidence | Frozen Agent source anchors |
| --- | --- |
| Changed known property 4→8, bounds/type rejection, unknown keys and unchanged legacy write, clear/null/absent behavior | `tests/sdk/test_timeline_selected_schema.py:72-198`; `tests/editing_conformance/test_recipe_scalar_commands.py:109-150,216-248,326-337`; `_scalar_commands.py:130-143` for unresolved refs |
| Exact identity/owner/revision changes and forged/stale/missing/corrupt/unadmitted/foreign inputs refuse atomically | `test_timeline_selected_schema.py:118-208`; `test_recipe_scalar_commands.py:72-106`; `test_timeline_selected_schema_runtime.py:463-515` |
| Only selected object I/O, unselected missing/corrupt bytes irrelevant, staged refs/pins, inverse/rebase with original inputs | `tests/sdk/test_timeline_selected_schema_runtime.py:300-402` |
| Retained V1 after V2/selection removal/cache deletion/restart; reload, exact retry, undo/redo; no launcher/renderer/cache fallback | `tests/sdk/test_timeline_selected_schema_runtime.py:404-460` |

After owners expose/review an existing-contract-compatible exact read, stage a
small `withSession` adapter and native capture extension, export goldens from
the exact frozen/published native source, and add meaningful App cases for all
rows above plus local/external reference behavior and full original guard
comparison. Fake input/golden parity qualifies capture only; actual public
Runtime reads + Agent acceptance/reload/retry/inverse are required to qualify
authority. Keep original positive expectations; do not redefine them as refusals.

**Execution UNRUN:** tests, native code, tsc, build, install, browser, sockets,
full suite and test service were prohibited by active full10022. Only source
inspection, byte comparison and whitespace checks were performed. Future central
qualification must use the exact reviewed source tuple and real public reads;
the prior native 207-pass report is not execution evidence for this App worker.
All M2/M3 integration remains held; Composition `0.0.8` is unchanged.
