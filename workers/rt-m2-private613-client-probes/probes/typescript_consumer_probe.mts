/**
 * External consumer fixture for the normal private 357/613 client.
 * Replace __CANDIDATE_INDEX__ and __CANDIDATE_TYPES__ with absolute .js
 * source paths before invoking tsc.  Internal source definitions are imported
 * from the real timeline-commit-types module; only the documented public Args
 * and WordAnchor surface is required from the package barrel.
 */

import type {
  AssembledTargetArgs, ClipAddMediaArgs, ClipAnchorArgs, ClipMoveArgs,
  EditCommand, OccurrenceCreateArgs, TextBindingSetArgs, TimelineInitArgs,
  WordAnchor, ProducerGuardArgs, MutationReceipt as MainMutationReceipt,
} from "__CANDIDATE_INDEX__";
import type {
  AgentBinding, AgentCreatedID, AgentDependency, AgentDerivedWrite, AgentRead,
  AgentSelection, AgentState, AgentWrite, AnchorIdentity, ClipAddArgs,
  ClipDeleteArgs, ClipSetArgs, ClipSetElementArgs, ClipSetParamsArgs,
  ClipSplitArgs, ClipTrimArgs, CommandBatch, Digest, DocumentPin,
  EditCommand as DirectEditCommand, ElementRef, EntityRef, ID, Intent,
  InverseArgs, JSON as TimelineJSON, MediaSelection, OccurrenceAddMediaArgs,
  OccurrenceDeleteArgs, OccurrenceDuplicateArgs, OccurrenceSwapMediaArgs,
  PlacementCreateArgs, PlacementUnplaceArgs, ProducerAdmittedTarget,
  ProducerAttemptPin, ProducerIdentity, PropertyPath, RestoreArgs, ScopedId,
  SettledProducerProposal, ShotPoolArgs, ShotSetArgs, TargetKey, TokenPath,
  TrackCreateArgs, TrackSetArgs, MutationReceipt as DirectReceipt,
} from "__CANDIDATE_TYPES__";

type AllSourceDefinitions = [
  AgentBinding, AgentCreatedID, AgentDependency, AgentDerivedWrite, AgentRead,
  AgentSelection, AgentState, AgentWrite, AnchorIdentity, AssembledTargetArgs,
  ClipAddArgs, ClipAddMediaArgs, ClipAnchorArgs, ClipDeleteArgs, ClipMoveArgs,
  ClipSetArgs, ClipSetElementArgs, ClipSetParamsArgs, ClipSplitArgs, ClipTrimArgs,
  CommandBatch, Digest, DirectEditCommand, DocumentPin, ElementRef, EntityRef,
  ID, Intent, InverseArgs, TimelineJSON, MediaSelection, OccurrenceAddMediaArgs,
  OccurrenceCreateArgs,
  OccurrenceDeleteArgs, OccurrenceDuplicateArgs, OccurrenceSwapMediaArgs,
  PlacementCreateArgs, PlacementUnplaceArgs, ProducerAdmittedTarget,
  ProducerAttemptPin, ProducerGuardArgs, ProducerIdentity, PropertyPath,
  RestoreArgs, ScopedId, SettledProducerProposal, ShotPoolArgs, ShotSetArgs,
  TargetKey, TextBindingSetArgs, TimelineInitArgs, TokenPath, TrackCreateArgs,
  TrackSetArgs, WordAnchor,
];
declare const allSourceDefinitions: AllSourceDefinitions;

const publicArgs: [
  AssembledTargetArgs, ClipAddMediaArgs, ClipAnchorArgs, OccurrenceCreateArgs,
  TextBindingSetArgs, TimelineInitArgs, WordAnchor,
] = [
  { replace_clips: [] },
  { row: { id: "c", clipType: "media", track: "v", at: 0, hold: 1 }, media: { asset: "a", generation_id: "g", variant_id: "v", object_id: "d", catalog_digest: "d" } },
  { field: "on", declaration: null, choice: null },
  { occurrence_id: "o", shot_id: "s", name: "Shot", track: "v", on: 0, duration: 1 },
  { binding: { kind: "prompt", slot: null }, clear: true },
  { name: "Timeline", slug: "timeline", output: { resolution: "1280x720", fps: 30, file: "output.mp4", background: null, background_scale: null } },
  { source: "transcript", document: { document_id: "d", version: 1, content_digest: "sha256:" + "a".repeat(64) }, word_ids: ["w"] },
];

const clipMoveV2: EditCommand = {
  schema_version: 1, op: "clip.move", version: "2", select: "parent/clip:clip-1",
  args: { on: 4 },
};
declare const producerGuardArgs: ProducerGuardArgs;
const producerGuardV1: EditCommand = {
  schema_version: 1, op: "producer.guard", version: "1", select: null,
  args: producerGuardArgs,
};

// @ts-expect-error producer.guard is v1-only.
const producerGuardV2: EditCommand = { ...producerGuardV1, version: "2" };
// @ts-expect-error clip.move has no unsupported version branch.
const clipMoveUnsupported: EditCommand = { ...clipMoveV2, version: "3" };
// @ts-expect-error A typed field must not degrade to any.
const invalidClipMove: ClipMoveArgs = { on: true };
const invalidWordAnchor: WordAnchor = {
  // @ts-expect-error WordAnchor.source is a string, not an any fallback.
  source: 1, document: { document_id: "d", version: 1, content_digest: "d" }, word_ids: ["w"],
};

// This remains RED on a6a: the generator emits an open map for a schema
// intent whose additionalProperties is false and whose properties are empty.
// @ts-expect-error Empty operation intents are closed objects.
const openEmptyIntent: EditCommand = {
  schema_version: 1, op: "clip.delete", version: "1", select: null, args: {},
  intent: { unexpected: true },
};

declare const directReceipt: DirectReceipt;
declare const mainReceipt: MainMutationReceipt;
const directSequence: [number, number] = directReceipt.project_seq;
const mainSequence: [number, number] = mainReceipt.project_seq;
const mainFromDirect: MainMutationReceipt = directReceipt;
const directFromMain: DirectReceipt = mainReceipt;

void [
  allSourceDefinitions, publicArgs, clipMoveV2, producerGuardV1, producerGuardV2,
  clipMoveUnsupported, invalidClipMove, invalidWordAnchor, openEmptyIntent,
  directSequence, mainSequence, mainFromDirect, directFromMain,
];
