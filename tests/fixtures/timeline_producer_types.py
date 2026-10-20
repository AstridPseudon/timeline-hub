from astrid_runtime_client import (
    CanonicalRenderRevision,
    ClipMoveArgs,
    DocumentPin,
    ProducerAdmittedTarget,
    ProducerAttemptPin,
    ProducerGuardArgs,
    ProducerIdentity,
    RenderTimelineAuthority,
    SettledProducerProposal,
    TrackSetArgs,
    VerifiedDocumentObject,
)

digest = "sha256:" + "a" * 64
target: ProducerAdmittedTarget = {"project_id": "p", "timeline_id": "t", "base_revision_id": "r", "base_publication_id": "receipt"}
identity: ProducerIdentity = {"task_id": "task", "attempt_id": "attempt", "executor_id": "worker", "fence": 1, "runtime_epoch": 1}
pin: ProducerAttemptPin = {**identity, "admitted_target": target, "proposal_digest": digest}
guard: ProducerGuardArgs = {"pin": pin}
proposal: SettledProducerProposal = {"schema_version": 1, "producer": identity, "admitted_target": target, "commands": [{"schema_version": 1, "op": "clip.move", "version": "1", "select": "parent/clip:c", "args": {"on": 1.0}}], "rationale": "Reviewed — 🎬", "proposal_digest": digest}
revision: CanonicalRenderRevision = {"project_id": "p", "timeline_id": "t", "revision_id": "r", "publication_id": "receipt", "content_digest": digest}
authority: RenderTimelineAuthority = {"project_id": "p", "timeline_id": "t", "parent_revision_id": revision["revision_id"], "parent_content_digest": digest, "publication_id": revision["publication_id"]}
move: ClipMoveArgs = {"on": 1.25}
label: TrackSetArgs = {"values": {"label": ""}, "clear": []}
document: DocumentPin = {"document_id": "pack", "version": 1, "content_digest": digest}
object_value: VerifiedDocumentObject = {"object_id": digest, "digest": digest, "size": 2, "media_type": "application/json", "bytes_base64": "e30="}
copy: ProducerGuardArgs = {"pin": pin, "proposal": proposal}  # type: ignore[typeddict-unknown-key]
incomplete_target: ProducerAdmittedTarget = {"project_id": "p", "timeline_id": "t", "base_revision_id": "r"}  # type: ignore[typeddict-item]
inline_authority: CanonicalRenderRevision = {**revision, "snapshot": {}}  # type: ignore[typeddict-unknown-key]
