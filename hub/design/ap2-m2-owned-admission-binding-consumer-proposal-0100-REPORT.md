# App2 M2 project-owned admission binding consumer proposal

## Disposition

Proposal only. No App product source was changed.

This is the project-owned normal-admission case. It is separate from the
SYSTEM8e hosted/system gap. The existing Agent `clip.add` source carrier is
the approved `args.schema_source` `DocumentPin`, but Public013/Main014 does
not contain the f83 `clip.add.args.schema_source` field. Therefore any future
add-consumer branch described here must remain dormant until that source
contract is present. No shared session, Provider, plugin route, admission at
save, new endpoint, DTO, result store, pin adoption, activation, or writer
retirement is proposed.

## Existing normal local-development path

The current path is:

1. `VideoEditorProvider.tsx:260-272` collects exact owner-qualified refs from
   resolved clips, calls `setAdmittedElementScope(projectId, refs)`, and then
   refreshes the admission.
2. `runtime/admitted-elements.ts:41` limits this path to local development
   with no Runtime origin. `refreshAdmittedElements` at `:57-107` POSTs the
   existing scope to `/api/astrid-element-admissions` at `:64`:

   ```json
   {"projectId":"<project>","refs":[{"packId":"<pack>","kind":"effect","id":"<id>","revision":"sha256:..."}]}
   ```

   The route result is only the existing host receipt:

   ```json
   {"digest":"<selection digest>","projectId":"<project>","moduleUrl":"/@id/__x00__virtual:astrid-element-admissions?v=<digest>"}
   ```

3. `config/vite/astridElementAdmissions.ts:177-189` owns that POST route.
   It calls `selectProjectElements`, stores the verified selection in the
   existing Vite plugin lifetime, and returns the receipt above. It does not
   return a new admission DTO.
4. The App then imports the existing virtual module. Its `elements` and
   `projects` exports become `current` in `admitted-elements.ts:42-50,80-99`.
   The virtual module is generated at
   `astridElementAdmissions.ts:135-140`. It intentionally removes local
   snapshot paths, but its spread preserves the resolver's existing extra
   `binding` metadata in the raw element record.

The upstream calls used to build that module are also existing calls:

- `config/vite/vite.config.ts:98-111` configures the canonical resolver and
  Runtime document reader.
- The resolver command is the existing Agent CLI
  `python3 -m astrid.core.element.cli project-pack resolve` with the exact
  `--realm`, `--project`, `--pack`, `--element`, `--kind`, and `--revision`
  arguments (`vite.config.ts:102-108`).
- The document reader is `AstridRuntimeClient.getDocument`, whose generated
  route is `GET /v1/projects/{project_id}/documents/{document_id}`
  (`src/integrations/runtime/generated.ts:140`).

The normal Agent producer already establishes the required project-owned
identity. `project_packs.py:392-505` admits the immutable project-pack source
and writes the selected admission, including its `snapshot_object`, into the
project document. `resolve_admitted_element` at `:704-731` returns the
owner-qualified record plus `binding.{projectId,documentId,documentVersion,contentDigest}`.
The CLI emits that existing record at `astrid/core/element/cli.py:30-43`.
The exact App-side DocumentPin is therefore:

```text
{
  document_id: binding.documentId,
  version: binding.documentVersion,
  content_digest: binding.contentDigest
}
```

The exact object is the matching
`document.content.admissions[].snapshot_object`, selected by
`{packId,id,kind,revision}`. It is not the element revision, the Vite
`selectionDigest`, or the catalog/config revision.

## Current loss and actual callers

The existing raw carrier and its loss points are:

- `config/vite/projectElementSelection.ts:62-90` reads the exact project
  document, matches the exact admission, validates the resolver's existing
  `binding`, and passes the resolver record through. The local `Admission`
  type at `:7` and the selection flow retain `snapshot_digest`, but do not
  retain the already-read `snapshot_object` from the matching document
  admission.
- `src/tools/video-editor/runtime/admitted-elements.ts:13-20` types
  `AdmittedElement` without the raw binding. At `:128-135`,
  `admittedCatalogEntries` projects only `id`, owner, kind, revision,
  presentation metadata, schema/defaults, capabilities, and authoring. The
  existing raw `binding` is dropped here.
- `VideoEditorProvider.tsx:274-301` builds the public element context from
  that catalog projection. It does not carry an admission pin or object.
- `ElementsLibraryPanel.tsx:58-65` reads the public catalog. Its current
  normal owned row path is `:121-160`, which calls the legacy
  `elementOperationAdapter` (`timeline.apply_element` or
  `timeline.apply_transition`). The literal no-pack branch at `:84-119`
  uses the existing native overlay session and is not the project-owned
  binding case.

Actual live callers in scope:

| Caller | Role |
| --- | --- |
| `VideoEditorProvider.tsx:260-272` | exact ref scope and local admission refresh |
| `admitted-elements.ts:57-107` | existing POST receipt, virtual-module import, and raw selection lifetime |
| `admitted-elements.ts:128-158` | catalog projection and existing pack helpers |
| `VideoEditorProvider.tsx:274-301` | catalog/context projection |
| `ElementsLibraryPanel.tsx:58-65` | catalog lookup and row rendering |
| `ElementsLibraryPanel.tsx:67-164` | apply caller; owned rows currently use the adapter, literal rows use native overlay |
| `AstridElementParams.tsx:51-75` | existing selected-parameter consumer; it already resolves retained authority separately and is not the missing catalog carrier |

## Minimal HOME proposal

Keep the current route and source carrier. Make one row-local accessor over
the already-loaded `current.elements` raw record, keyed by the exact
`{packId,kind,id,revision}`. The accessor should return the existing binding
as a `DocumentPin` and the matching admission `snapshot_object`; it should not
read the latest catalog, hash a browser document, or create a second store.

The smallest App-side source preparation is in
`config/vite/projectElementSelection.ts`: when the exact admission is found,
carry its existing `snapshot_object` beside the resolver's existing `binding`
on that same raw element record. This is an adapter preservation of data
already returned by the Runtime document read and Agent resolver; it is not a
new wire DTO, endpoint, result type, persisted field, or admission operation.
The existing virtual module already carries raw element metadata, so no
plugin-route change is needed. The public catalog should remain presentation
data; the row-local consumer can resolve the raw source by exact ref at apply
time.

For a future project-owned add consumer, the row-local sequence is:

1. Match the catalog row and raw source on all four owner-qualified ref
   fields. Require the raw binding's project to equal the active project.
2. Validate the existing DocumentPin and the exact matching
   `snapshot_object` descriptor. Use the existing generated retained reads
   (`getProjectVerifiedDocument` and
   `getProjectVerifiedDocumentObject`) only through the existing source/session
   seam when that consumer is activated.
3. Pass that same DocumentPin as the existing `schema_source` on the native
   `clip.add` operation. Preserve the exact object association for later
   parameter edits, retry, inverse, and replay.
4. If the binding is absent, belongs to another project, does not match the
   exact row revision, or its object is missing/mismatched, refuse before
   capture/submit and leave the row/draft untouched. Do not reinterpret the
   catalog's element `revision` or the catalog/selection revision as a
   DocumentPin.

Because f83 `clip.add.args.schema_source` is absent in Public013/Main014,
steps 2-3 are a dormant proposal only. The current owned row continues on
its existing adapter path. No Provider or shared-session edit belongs in this
HOME proposal, and no admission is performed during save.

## Producer-gap assessment and smallest peer request

There is no Agent producer gap for the normal project-owned source: the exact
pin components are in the existing resolver `binding`, and the exact object
is in the existing Runtime project document admission. The missing field is
at the App Vite selection adapter boundary, specifically the omission of
`document.content.admissions[].snapshot_object` from the raw selected element
after `projectElementSelection.ts:62-69`.

If the App owner requires a peer request, it is this bounded request to the
HOME/Vite owner:

> Preserve the matching existing `snapshot_object` alongside the existing raw
> resolver `binding` while building the selected element record in
> `projectElementSelection.ts`; expose it only through the existing raw
> admission source accessor. Do not add a route, DTO, public catalog contract,
> Provider field, store, or save-time admission.

The only positive acceptance witness needed for this proposal is one exact
project-owned row whose raw binding produces the same DocumentPin and object
from the admission document. The negative witness is one missing or
mismatched-project binding that refuses atomically and preserves the draft.
No SYSTEM8e authority investigation or hosted substitution is part of either
witness.

## Verification and boundaries

- `git diff --check` — passed.
- `git status --short --branch` — clean; no App product source changed.
- No product test was rerun. This was a proposal-only task, and the brief
  explicitly excludes repeating the existing 28-test/system investigation.
- No full, browser, localhost, live-socket, Runtime-door, generation,
  dependency, pin/activation, or shared-dependency suite was run.

