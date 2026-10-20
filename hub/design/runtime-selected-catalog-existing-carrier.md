# Runtime selected-catalog existing carrier

## Decision

The normal carrier already exists. Runtime does not need a new endpoint, DTO,
inline authority, browser hash, or virtual admission fallback. The supported
sequence is:

1. Agent resolves the exact selected reference `{packId, id, kind, revision}`
   through its existing project-pack resolver. Its returned `binding` is the
   authoritative pin material: `{projectId, documentId, documentVersion,
   contentDigest}`. Map that to the existing `DocumentPin` fields
   `{document_id, version, content_digest}`. This is Agent/Runtime document
   identity, not a digest computed by App or by a browser. The resolver also
   verifies that exactly one admission in the pack document matches
   `id/kind/revision` and that its owner is `pack_id` (`packId` in the element
   reference). See Agent `astrid/core/element/project_packs.py:704-731`.
2. Before the first selected PARAM capture, App2 carries that exact pin in the
   existing `clip.set-params` args as optional `schema_source` alongside the
   existing `values` and `clear`. No new command or top-level DTO is needed.
3. The normal Agent provider reads the exact source and selected portable
   snapshot through its existing port calls:
   `config_source(DocumentPin)`, then
   `document_object(DocumentPin, snapshot_object.object_id)`. The pure Agent
   admission resolver checks the returned bytes against the exact
   `pack_id/id/kind/revision` admission and its descriptor; Runtime remains the
   custody authority.

If App2 has only `{packId,id,kind,revision}` and not the Agent-produced
`binding`/`DocumentPin`, it cannot legitimately call the verified reads. The
existing public document list/get reads expose the document body and version,
but are not a browser-side authority for inventing `content_digest`. That is
the remaining Agent-to-App2 selected-PARAM producer handoff, not a Runtime
gap. The App owner seam is the selected PARAM/read adapter (the existing
generated Runtime client and `paramReadClient` path), which must consume the
Agent-carried pin and emit `schema_source`; the hosted path must not call
`/api/astrid-element-admissions` or the disabled virtual module. The generic
App capture code currently fails closed for a pack element until authoritative
schema capture is supplied (`elementCapture.ts:69-75,220-234`).

## Existing Runtime operations and fields

The generated public client already exposes:

- `getProjectVerifiedDocument(projectId, pin)` -> `VerifiedDocument`, via
  `GET /v1/projects/{project_id}/document-inputs/verified` with exactly
  `document_id`, positive `version`, and `content_digest` query fields. The
  response is `{pin, document}`.
- `getProjectVerifiedDocumentObject(projectId, pin, objectId)` ->
  `VerifiedDocumentObject`, via
  `GET /v1/projects/{project_id}/document-objects/verified` with those three
  pin fields plus `object_id`. The response is the closed descriptor and
  bytes: `{object_id, digest, size, media_type: "application/json",
  bytes_base64}`.

The pack `document.content` is the existing project-pack admission record:

```json
{
  "schema": "astrid.project-pack/v1",
  "pack_id": "<owner>",
  "source_binding_key": "project-packs",
  "relative_manifest": "<realm>/<project>/packs/<owner>/pack.yaml",
  "admissions": [
    {
      "id": "<id>",
      "kind": "effect|animation|transition",
      "revision": "sha256:<admitted-source-revision>",
      "snapshot_digest": "<closure>",
      "snapshot_object": {
        "object_id": "sha256:<portable-json>",
        "digest": "sha256:<portable-json>",
        "size": 123,
        "media_type": "application/json"
      }
    }
  ]
}
```

The `DocumentPin` belongs to the containing project-pack document, not to an
individual admission. Selection is exact by `pack_id`/`packId` plus admission
`id`, `kind`, and `revision`; the object read is then exact by the selected
admission's `snapshot_object.object_id`. Runtime validates the pack's stable
document identity, project binding, schema/source binding, admission identity,
managed-project CAS association, descriptor metadata, bytes, digest, and file
identity. It never accepts a caller-supplied declaration as authority.

Runtime source of truth for this path is:

- `runtime_protocol/server.py:49-63,537-566` — exact closed query shapes and
  dispatch;
- `runtime_protocol/service.py:2532-2540` — public service methods and
  authorization wrapper;
- `runtime_protocol/timeline_commit_port.py:528-581` — project-linked
  reachability, exact source capture, and pack-object lookup;
- `runtime_protocol/timeline_commit_inputs.py:203-293,422-455` — pack
  admission/portable descriptor validation and retained/live exact capture.

## Scope, reachability, and retention

Both public reads require the project path, `projects:read`, and the existing
timeline-read authorization callback. Public reachability is the distinct set
of pins in `timeline_document_input_links` for that project, i.e. pins linked
by accepted timeline records. The public route intentionally has no
`timeline_id`; it is project-scoped. A retained binding is readable only when
that exact pin is in this accepted closure. If no retained binding exists,
Runtime may read only the current live document when its version and canonical
content digest exactly equal the requested pin. A guessed pin, foreign project,
wrong kind/schema, unlinked old pin, or object outside the captured pack is
refused without a canonical write.

The internal Agent commit port is narrower: `config_source` accepts an
explicitly declared pin or one reachable from the request's accepted closures,
shots, or history pins; `document_object` requires that exact captured pack
document first. It records the source pin in the command dependency and
manifest, and acceptance revalidates the retained document and object custody.
Replay does not resolve the latest pack.

The retained behavior is concrete. An accepted V1 pack with a max-10
declaration remains readable and usable after a live V2 max-20 document is
published, the current project document is removed, and Runtime is restarted:

- `getProjectVerifiedDocument(project, V1Pin)` returns the original V1
  document, including the original admission and `snapshot_object`;
- selecting that object through
  `getProjectVerifiedDocumentObject(project, V1Pin, object_id)` returns the
  original portable bytes, so values 4 and 8 pass while 16 is refused by V1;
- V2's object is not readable under V1's pin; it requires V2's distinct exact
  pin;
- the reads and refused PARAM attempts leave the canonical database unchanged.

The accepted fixture proving this is
`tests/test_timeline_pack_document_read.py:77-133,230-262` together with
`tests/test_timeline_pack_param_retained_read.py:72-105,190-220`. The Runtime
implementation's retained binding is the exact
`timeline_document_input_bindings`/`timeline_document_input_contents` record
linked by `timeline_document_input_links`; current-document removal does not
rewrite or revoke that accepted V1 input.

## Evidence and limits

Central targeted test service, exact command:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_timeline_pack_document_read.py \
  tests/test_timeline_pack_param_retained_read.py
```

Result: **30 passed in 13.40s**. This includes the hosted public reads and the
V1-after-V2/removal/restart fixture. A direct sandbox attempt reached those
fixtures but could not create a socket (`PermissionError: [Errno 1] Operation
not permitted`), so the socket-dependent result above is the central service
result. No full, browser, renderer, schema-generation, or broad matrix run was
made.

