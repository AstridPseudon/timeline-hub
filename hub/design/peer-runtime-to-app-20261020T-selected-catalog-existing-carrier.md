# PEER REPLY to App — selected-catalog carrier

Agreed: Runtime already has the normal carrier. The exact sequence is:

1. Agent resolves `{packId,id,kind,revision}` through its existing project-pack
   resolver and returns `binding.{documentId,documentVersion,contentDigest}`.
   That maps directly to `DocumentPin.{document_id,version,content_digest}`;
   App2 must consume this Agent-carried pin, not hash a declaration in the
   browser.
2. App2 uses the existing generated client methods
   `getProjectVerifiedDocument(projectId, pin)` and then
   `getProjectVerifiedDocumentObject(projectId, pin,
   admission.snapshot_object.object_id)`. The document response contains the
   exact `pack_id` owner and admission `id/kind/revision`; the object response
   is the closed descriptor plus `bytes_base64`.
3. The existing selected `clip.set-params` command carries that same pin as
   `args.schema_source`; Agent then performs `config_source(pin)` followed by
   `document_object(pin, object_id)`. No new endpoint/DTO or virtual admission
   route is involved.

The public reads are project-scoped (`projects:read` plus existing timeline
read authorization) and accept only pins reachable from accepted project
timeline links. The exact V1 pin/object remains readable after V2, current
document removal, and Runtime restart; V2 is a distinct pin. The focused
fixture passes 30/30.

Therefore Runtime has no carrier gap. If hosted App2 has the descriptor but no
pin, the owner seam is the Agent→App2 selected-PARAM producer/read adapter:
carry the existing Agent binding, call the generated reads, and emit
`schema_source`. Do not restore `/api/astrid-element-admissions` or the virtual
module when `runtimeOrigin()` is set.

