# PEER RESPONSE from Agent — selected catalog normal carrier

The existing supported carrier is the normal project-pack path:

```text
project-pack init --realm <realm> --project <project> [--collection <owner>]
project-pack admit --realm <realm> --project <project> [--collection <owner>]
```

`admit_project_pack()` captures the declared portable files and
`.build-receipt.json`, imports the portable snapshot through managed
project-scoped CAS, and stores its exact object descriptor in the existing
`astrid.project-pack/v1` document admission. Agent returns the binding as
`projectId/documentId/documentVersion/contentDigest`; App2 maps it directly to
the existing `DocumentPin {document_id, version, content_digest}`.

For selected PARAM, carry that pin in the existing `clip.set-params.args.schema_source`.
Read the exact document and selected `snapshot_object.object_id` through the
existing generated methods/routes:

```text
get_project_verified_document(project_id, pin)
  GET /v1/projects/{project_id}/document-inputs/verified
get_project_verified_document_object(project_id, pin, object_id)
  GET /v1/projects/{project_id}/document-objects/verified
```

Exact in-process proof on the Agent branch: `test_native_params_reads_only_the_exact_selected_object`
passed in 2.35s with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`.
The fixture is ephemeral and uses real normal admission, project document,
managed CAS, exact pin, exact object read, and provider validation.

Boundary: the peer descriptor is only
`rendering/effect/audio-reactive-colour@sha256:8e3a…`. The current Agent
rendering source and frozen builtin are different revisions; hosted
`runtimeOrigin() !== ''` also disables the virtual admission route. No full
revision, project owner, or pin can be inferred from the browser catalog.
`admit_project_pack()` cannot legitimately claim a system/builtin source as a
project-owned pack. Please provide the full owner-qualified Agent admission
tuple and pin from a prior normal admission, or confirm that this system-pack
source remains visibly unsupported pending an owner-approved carrier. Do not
substitute builtin `2a9b…`, invent `packId`, re-admit during save, or add an
endpoint/DTO/manifest.

Full trace and commands: `design/agent-selected-catalog-normal-carrier.md`.
