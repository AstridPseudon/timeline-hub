import type {
  AssembledTargetArgs, ClipAddMediaArgs, ClipAnchorArgs, OccurrenceCreateArgs,
  TimelineInitArgs, TextBindingSetArgs, WordAnchor,
} from "../../packages/typescript/src/index.js";
import type { EditCommand, MutationReceipt } from "../../packages/typescript/src/timeline-commit-types.js";

const move1: EditCommand = { schema_version: 1, op: "clip.move", version: "1", select: "parent/clip:c", args: { on: 1 } };
const move2: EditCommand = { ...move1, version: "2" };
const anchor: EditCommand = { schema_version: 1, op: "clip.anchor", version: "1", select: "parent/clip:c", args: { field: "on", declaration: null, choice: null } };
const clear: TextBindingSetArgs = { binding: { kind: "voiceover_script", slot: null }, clear: true };
const text: TextBindingSetArgs = { binding: { kind: "prompt", slot: "prompt" }, text: { object_id: "sha256:a", digest: "sha256:a", size: 0, media_type: "text/plain; charset=utf-8" } };
const seq: MutationReceipt["project_seq"] = [1, 2];
// @ts-expect-error Operation versions remain correlated to the registered op.
const anchor2: EditCommand = { ...anchor, version: "2" };
// @ts-expect-error Unknown operation does not enter the registered DTO union.
const unknown: EditCommand = { ...move1, op: "unknown.operation" };
// @ts-expect-error Unknown version is not an admitted move branch.
const move3: EditCommand = { ...move1, version: "3" };
// @ts-expect-error An unrelated operation's args cannot satisfy the move branch.
const badArgs: EditCommand = { ...move2, args: { field: "on", declaration: null, choice: null } };
// @ts-expect-error Closed args reject unknown fields.
const extra: EditCommand = { ...move2, args: { on: 1, extra: null } };
// @ts-expect-error Closed envelope rejects unknown fields.
const extraEnvelope: EditCommand = { ...move2, extra: null };
// @ts-expect-error Move intent has no relative position.
const badIntent: EditCommand = { ...move2, intent: { position: "relative" } };
// @ts-expect-error A text binding update requires text or clear.
const noChange: TextBindingSetArgs = { binding: { kind: "prompt", slot: null } };
// @ts-expect-error A required-only union retains the typed text branch.
const badText: TextBindingSetArgs = { binding: { kind: "prompt", slot: null }, text: false };
// @ts-expect-error Mutation receipt sequence is a pair.
const shortSeq: MutationReceipt["project_seq"] = [1];
// @ts-expect-error Mutation receipt sequence remains bounded.
const longSeq: MutationReceipt["project_seq"] = [1, 2, 3];
void [move1, move2, anchor, clear, text, seq];
type PublicTypes = [AssembledTargetArgs, ClipAddMediaArgs, ClipAnchorArgs, OccurrenceCreateArgs, TimelineInitArgs, TextBindingSetArgs, WordAnchor];
