import type { EditCommand } from '@/integrations/runtime/generated.ts';
import type { TimelineHeadRevision } from '../data/DataProvider.ts';
import type { TimelineData } from './timeline-data.ts';
import type { TimelineOps } from '@/sdk/index';
import type { TimelinePatch, TimelinePreviewResult, TimelineDiff } from '@/sdk/video/timeline/patch.ts';
import { propertyGestureCommands, deleteGestureCommands, attachGestureCommands, gestureCommandsFor, gestureOccurrenceFor } from '../commands/semanticGestures.ts';
import { trackPropertyGesture } from '../commands/trackGestures.ts';
import { compileTimelinePatch } from './timeline-patch.ts';

/** Host-captured intent. Source labels are attribution, never routing authority. */
export interface ProposalCommandBinding {
  readonly proposalId: string;
  readonly source: string;
  readonly transactionId: string;
  readonly base: TimelineHeadRevision;
  readonly baseVersion: number;
  readonly providerContext: string | null;
  readonly signature: string;
  readonly patch: TimelinePatch;
  readonly commands: readonly EditCommand[];
  readonly occurrence?: ReturnType<typeof gestureOccurrenceFor>;
  readonly preview: TimelinePreviewResult;
}

/** Internal host capability; ordinary SDK patch producers retain their API. */
export type ProposalTimelineOps = TimelineOps & {
  proposalContext?: () => string;
  captureProposal?: (patch: TimelinePatch, source: string, proposalId: string) => ProposalCommandBinding | undefined;
  previewProposal?: (binding: ProposalCommandBinding) => TimelinePreviewResult;
  acceptProposal?: (binding: ProposalCommandBinding) => Promise<TimelineDiff>;
};

export function orderedPatchCommands(patch: TimelinePatch, current: TimelineData): readonly EditCommand[] | undefined {
  let captured = current;
  const commands: EditCommand[] = [];
  const supported = patch.operations.length > 0 && patch.operations.every((operation) => {
    if (operation.op === 'track.update') {
      const { mode, ...properties } = operation.payload ?? {};
      // The existing patch compiler merges only these scalar track fields.
      if ((mode !== undefined && mode !== 'merge')
        || Object.keys(properties).some((key) => !['label', 'role', 'muted'].includes(key))) return false;
      const gesture = trackPropertyGesture(captured, operation.target, properties);
      if (!gesture?.commands.length) return false;
      commands.push(...gesture.commands);
      const step = compileTimelinePatch({ ...patch, operations: [operation] }, captured);
      if (!step.valid || !step.nextData) return false;
      captured = step.nextData;
      return true;
    }
    if (!captured.config.clips.some((clip) => clip.id === operation.target)) return false;
    if (operation.op === 'clip.remove') {
      commands.push(...deleteGestureCommands(captured, [operation.target]));
    } else {
      if (operation.op !== 'clip.update') return false;
      const { mode, ...properties } = operation.payload ?? {};
      if (mode !== undefined && mode !== 'merge') return false;
      const produced = propertyGestureCommands(captured, operation.target, properties);
      if (!produced?.length) return false;
      commands.push(...produced);
    }
    const step = compileTimelinePatch({ ...patch, operations: [operation] }, captured);
    if (!step.valid || !step.nextData) return false;
    captured = step.nextData;
    return true;
  });

  return supported ? commands : undefined;
}

export function commandContext(data: TimelineData, commands: readonly EditCommand[]) {
  const owner = { ...data };
  attachGestureCommands(owner, commands, data);
  if (!gestureCommandsFor(owner)) throw new Error('Proposal commands have an unsupported source context.');
  return gestureOccurrenceFor(owner);
}

export function freezeProposal<T>(value: T): T {
  if (value && typeof value === 'object') {
    for (const child of Object.values(value)) freezeProposal(child);
    Object.freeze(value);
  }
  return value;
}

// The existing persistence attempt owns this metadata, including exact retries.
const owners = new WeakMap<TimelineData, { base: TimelineHeadRevision; acknowledge: () => void }>();
export function bindProposalSave(data: TimelineData, base: TimelineHeadRevision, acknowledge: () => void) {
  let acknowledged = false;
  owners.set(data, { base: structuredClone(base), acknowledge() {
    if (acknowledged) return;
    acknowledged = true;
    acknowledge();
  } });
}
export const proposalSaveFor = (data: TimelineData) => owners.get(data);
