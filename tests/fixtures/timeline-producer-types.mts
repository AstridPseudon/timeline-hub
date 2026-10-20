import type {
  CanonicalRenderRevision, ClipMoveArgs, DocumentPin, ProducerAdmittedTarget,
  ProducerAttemptPin, ProducerGuardArgs, ProducerIdentity, RenderTimelineAuthority,
  SettledProducerProposal, TrackSetArgs, VerifiedDocumentObject,
} from "@astrid/runtime-client";

const digest = "sha256:" + "a".repeat(64);
const target: ProducerAdmittedTarget = { project_id: "p", timeline_id: "t", base_revision_id: "r", base_publication_id: "receipt" };
const identity: ProducerIdentity = { task_id: "task", attempt_id: "attempt", executor_id: "worker", fence: 1, runtime_epoch: 1 };
const pin: ProducerAttemptPin = { ...identity, admitted_target: target, proposal_digest: digest };
const guard: ProducerGuardArgs = { pin };
const proposal: SettledProducerProposal = { schema_version: 1, producer: identity, admitted_target: target, commands: [{ schema_version: 1, op: "clip.move", version: "1", select: "parent/clip:c", args: { on: 1.0 } }], rationale: "Reviewed — 🎬", proposal_digest: digest };
const revision: CanonicalRenderRevision = { project_id: "p", timeline_id: "t", revision_id: "r", publication_id: "receipt", content_digest: digest };
const authority: RenderTimelineAuthority = { project_id: "p", timeline_id: "t", parent_revision_id: revision.revision_id, parent_content_digest: digest, publication_id: revision.publication_id, future: null };
const move: ClipMoveArgs = { on: 1.25 };
const label: TrackSetArgs = { values: { label: "" }, clear: [] };
const document: DocumentPin = { document_id: "pack", version: 1, content_digest: digest };
const object: VerifiedDocumentObject = { object_id: digest, digest, size: 2, media_type: "application/json", bytes_base64: "e30=" };
// @ts-expect-error Guard forwards only the pin, never a proposal copy.
const copy: ProducerGuardArgs = { pin, proposal };
// @ts-expect-error The admitted original publication is required.
const incompleteTarget: ProducerAdmittedTarget = { project_id: "p", timeline_id: "t", base_revision_id: "r" };
// @ts-expect-error Booleans cannot stand in for a fence.
const booleanFence: ProducerAttemptPin = { ...pin, fence: true };
// @ts-expect-error The historical selector is closed.
const inlineAuthority: CanonicalRenderRevision = { ...revision, snapshot: {} };
// @ts-expect-error The immutable historical publication is required.
const incompleteRevision: CanonicalRenderRevision = { project_id: "p", timeline_id: "t", revision_id: "r", content_digest: digest };
