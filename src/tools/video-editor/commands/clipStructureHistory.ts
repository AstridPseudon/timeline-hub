import { canonicalJsonStringify } from '../data/typed/timelineBundle.ts';
import { isClipPlacementBatch } from './clipPlacementHistory.ts';
import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import { selectedMediaRegistryExpectationPath, readSelectedProjectMediaIdentity } from './selectedProjectMedia.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const clipId = (value: unknown): value is string => typeof value === 'string' && /^parent\/clip:[^/\s]+$/.test(value);
const trackId = (value: unknown): value is string => typeof value === 'string' && /^parent\/track:[^/\s]+$/.test(value);
const scopedClipId = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);
const groupId = (value: unknown): value is string => typeof value === 'string' && /^parent\/shot-group:[A-Za-z0-9_-]+$/.test(value);
export const shotGroupIdentity = (shot: string, track: string) => `parent/shot-group:${btoa(String.fromCharCode(...new TextEncoder().encode(JSON.stringify([shot, track])))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')}`;
const groupOrder = (value: unknown): value is string[] => Array.isArray(value) && value.length > 0 && value.every(groupId) && new Set(value).size === value.length;
const scopedOrder = (value: unknown): value is string[] => Array.isArray(value) && value.length > 0 && value.every(scopedClipId)
  && new Set(value).size === value.length && new Set(value.map(id => id.split('/clip:')[0])).size === 1;
const tagged = (state: unknown): state is { state: 'absent' } | { state: 'present'; value: unknown } => record(state) && (state.state === 'absent' ? Object.keys(state).length === 1
  : state.state === 'present' && Object.keys(state).length === 2 && Object.prototype.hasOwnProperty.call(state, 'value'));
const permutation = (value: unknown): value is string[] => Array.isArray(value) && value.length > 0
  && value.every(trackId) && new Set(value).size === value.length;
const capturedOrder = (command: EditCommand): string[] | undefined => {
  const order = command.expect?.track_order;
  return order?.state === 'present' && permutation(order.value) ? order.value : undefined;
};
const clipPermutation = (value: unknown): value is string[] => Array.isArray(value) && value.length > 0
  && value.every(clipId) && new Set(value).size === value.length;
const capturedClipOrder = (command: EditCommand): string[] | undefined => {
  const order = command.expect?.clip_order ?? (clipId(command.args.from) ? command.expect?.[`${command.args.from}::clip_order`] : undefined);
  return order?.state === 'present' && clipPermutation(order.value) ? order.value : undefined;
};
const literalRemoval = (command: EditCommand): boolean => {
  const captured = command.expect?.[''];
  const clip = captured?.state === 'present' && record(captured.value) ? captured.value : undefined;
  if (!clip || clip.app !== undefined && !record(clip.app)) return false;
  const app = record(clip.app) ? clip.app : {};
  if (app.canonical) return false;
  const intent = { ...app, ...(record(app.astrid) ? app.astrid : {}) };
  if (['on', 'until', 'for', 'cut', 'sequence', 'segment', 'formulas', 'loop', 'orphan'].some(key => intent[key] !== undefined)
    || ['keyframes', 'modifiers', 'keyframeOrigin'].some(key => Object.prototype.hasOwnProperty.call(clip, key))) return false;
  const groups = command.expect?.['parent::config.pinnedShotGroups'];
  return groups?.state === 'absent' || groups?.state === 'present' && Array.isArray(groups.value)
    && groups.value.every(group => record(group) && Array.isArray(group.clipIds) && !group.clipIds.includes(clip.id));
};
const wholeSource = (command: EditCommand, id: string): boolean => {
  const state = command.expect?.[`${id}::`] ?? command.expect?.[''];
  return state?.state === 'present' && record(state.value) && state.value.id === id.replace(/^.*\/(?:clip|track):/, '');
};

/** A group delete owns only its explicit clip roots and the stored group row. */
export function isShotGroupDeletionBatch(commands: readonly EditCommand[]): boolean {
  const command = commands[0];
  if (commands.length !== 1 || command.op !== 'shot-group.remove' || command.select !== null
    || !record(command.args.group) || Object.keys(command.args).length !== 2
    || Object.keys(command.args.group).length !== 2
    || typeof command.args.group.shotId !== 'string' || !command.args.group.shotId || command.args.group.shotId.includes('/')
    || typeof command.args.group.trackId !== 'string' || !command.args.group.trackId || command.args.group.trackId.includes('/')
    || !Array.isArray(command.args.remove_clip_ids) || !command.args.remove_clip_ids.length
    || !command.args.remove_clip_ids.every(scopedClipId) || new Set(command.args.remove_clip_ids).size !== command.args.remove_clip_ids.length) return false;
  const sid = shotGroupIdentity(command.args.group.shotId, command.args.group.trackId);
  const row = command.expect?.[`${sid}::`]; const order = command.expect?.[`${sid}::group_order`];
  if (row?.state !== 'present' || !record(row.value) || row.value.shotId !== command.args.group.shotId
    || row.value.trackId !== command.args.group.trackId || !Array.isArray(row.value.clipIds) || !row.value.clipIds.length
    || new Set(row.value.clipIds).size !== row.value.clipIds.length || order?.state !== 'present' || !groupOrder(order.value) || !order.value.includes(sid)) return false;
  const scope = command.args.remove_clip_ids[0].split('/clip:')[0];
  const members = row.value.clipIds.map(id => `${scope}/clip:${id}`);
  const clipOrder = Object.entries(command.expect!).find(([key]) => members.includes(key.split('::')[0]) && key.endsWith('::clip_order'))?.[1];
  if (clipOrder?.state !== 'present' || !scopedOrder(clipOrder.value)) return false;
  const captured = clipOrder.value;
  return command.args.remove_clip_ids.every(id => members.includes(id))
    && members.every(id => wholeSource(command, id) && captured.includes(id));
}

function isGroupDeletionInverse(command: EditCommand): boolean {
  const writes = command.args.writes as Array<Record<string, unknown>>;
  const groups = writes.filter(write => groupId(write.id)); const clips = writes.filter(write => scopedClipId(write.id));
  if (groups.length !== 1 || !clips.length || groups.length + clips.length !== writes.length
    || new Set(writes.map(write => write.id)).size !== writes.length) return false;
  const group = groups[0]; const row = [group.before, group.after].find(state => record(state) && state.state === 'present') as { value?: unknown };
  if (!record(row?.value) || typeof row.value.shotId !== 'string' || typeof row.value.trackId !== 'string'
    || group.id !== shotGroupIdentity(row.value.shotId, row.value.trackId) || !Array.isArray(row.value.clipIds)
    || !groupOrder(group.order) || !group.order.includes(String(group.id))) return false;
  const members = row.value.clipIds;
  const scope = String(clips[0].id).split('/clip:')[0];
  return clips.every(write => String(write.id).startsWith(`${scope}/clip:`) && members.includes(String(write.id).split('/clip:')[1])
    && scopedOrder(write.order) && write.order.includes(String(write.id)))
    && writes.every(write => write.path === '' && Object.keys(write).length === 5
      && Object.keys(write).every(key => ['id', 'path', 'before', 'after', 'order'].includes(key))
      && tagged(write.before) && tagged(write.after) && write.before.state !== write.after.state
      && record(group.before) && write.before.state === group.before.state
      && (groupId(write.id) || [write.before, write.after].every(state => state.state === 'absent' || record(state.value)
        && state.value.id === String(write.id).split('/clip:')[1])));
}

/** Exact existing managed-media producer; Redo replays this original command. */
export function isSelectedMediaCreation(command: EditCommand | undefined): boolean {
  if (!command) return false;
  const child = command.created?.[0];
  const selection = readSelectedProjectMediaIdentity(command.args.media);
  const registry = selection ? command.expect?.[selectedMediaRegistryExpectationPath(selection.asset)] : undefined;
  return command.op === 'timeline.add' && trackId(command.select) && selection !== null
    && (registry?.state === 'absent' || registry?.state === 'present' && record(registry.value) && registry.value.media_id === selection.object_id)
    && Object.keys(command.args).length === 4 && command.created?.length === 1 && clipId(child)
    && command.args.clip_id === child.slice('parent/clip:'.length)
    && typeof command.args.at === 'number' && Number.isFinite(command.args.at) && command.args.at >= 0
    && typeof command.args.duration === 'number' && Number.isFinite(command.args.duration) && command.args.duration > 0
    && command.expect?.[`${child}::`]?.state === 'absent';
}

/** Existing literal split/clone, selected-media creation and empty-track removal. */
export function isClipStructureBatch(commands: readonly EditCommand[]): boolean {
  if (!commands.length) return false;
  if (isShotGroupDeletionBatch(commands)) return true;
  if (commands.length === 1 && isSelectedMediaCreation(commands[0])) return true;
  if (commands.length > 1 && commands[0].op === 'timeline.add' && clipId(commands[0].args.from)) {
    const clone = commands[0]; const nudges = commands.slice(1); const order = capturedClipOrder(clone);
    return isClipStructureBatch([clone]) && Boolean(order) && order!.includes(String(clone.args.from))
      && !order!.includes(clone.created![0]) && isClipPlacementBatch(nudges)
      && nudges.every(command => command.op === 'clip.nudge' && clipId(command.select)
        && command.select !== clone.args.from && command.select !== clone.created![0] && order!.includes(command.select)
        && command.args.frames === nudges[0].args.frames && Number(command.args.frames) > 0
        && command.expect?.['app.astrid.on']?.state === 'absent' && command.expect?.['app.astrid.until']?.state === 'absent');
  }
  if (commands.every(command => command.op === 'clip.remove' && clipId(command.select)
    && Object.keys(command.args).length === 0 && wholeSource(command, command.select) && literalRemoval(command) && capturedClipOrder(command))) {
    const initial = capturedClipOrder(commands[0])!; const removed = new Set<string>();
    return commands.every(command => {
      const expected = initial.filter(id => !removed.has(id));
      if (!expected.includes(command.select!) || JSON.stringify(capturedClipOrder(command)) !== JSON.stringify(expected)) return false;
      removed.add(command.select!); return true;
    });
  }
  if (commands.every(command => command.op === 'timeline.remove' && trackId(command.select)
    && Object.keys(command.args).length === 0 && wholeSource(command, command.select)
    && capturedOrder(command))) {
    const initial = capturedOrder(commands[0])!;
    const removed = new Set<string>();
    return commands.every(command => {
      const order = capturedOrder(command)!;
      const expected = initial.filter(id => !removed.has(id));
      if (!expected.includes(command.select!) || JSON.stringify(order) !== JSON.stringify(expected)) return false;
      removed.add(command.select!); return true;
    });
  }
  if (!commands.every(command => (command.op === 'timeline.split' && clipId(command.select)
    && Object.keys(command.args).length === 1 && typeof command.args.at === 'number' && Number.isFinite(command.args.at)
    && wholeSource(command, command.select))
    || (commands.length === 1 && command.op === 'timeline.add' && command.select === null
      && Object.keys(command.args).length === 2 && clipId(command.args.from)
      && typeof command.args.at === 'number' && Number.isFinite(command.args.at) && command.args.at >= 0
      && wholeSource(command, command.args.from)))) return false;
  const sources = commands.map(command => String(command.select ?? command.args.from));
  const children = commands.flatMap(command => command.created ?? []);
  return commands.every(command => command.created?.length === 1 && clipId(command.created[0]))
    && new Set(sources).size === sources.length && new Set(children).size === commands.length
    && children.every(id => !sources.includes(id));
}

/** Root membership is guarded by its exact tagged payload; no aggregate arrays. */
export function isClipStructureInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || Object.keys(command.args).length !== 2 || typeof command.args.publication !== 'string' || !command.args.publication
    || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  if (writes.every(record) && isGroupDeletionInverse(command)) return true;
  const tracks = writes.every((write: unknown) => record(write) && trackId(write.id));
  if (!writes.every((write: unknown) => record(write) && (tracks ? trackId(write.id) : clipId(write.id))
    && typeof write.id === 'string' && Object.keys(write).every(key => ['id', 'path', 'before', 'after', 'order'].includes(key))
    && tagged(write.before) && tagged(write.after)
    && (write.path === '' ? write.before.state !== write.after.state
      && [write.before, write.after].every(state => state.state === 'absent' || record(state.value) && state.value.id === String(write.id).split(':')[1])
      && (tracks ? permutation(write.order) && write.order.includes(write.id) : write.order === undefined || clipPermutation(write.order) && write.order.includes(write.id))
      : !tracks && ['to', 'hold', 'at'].includes(String(write.path)) && write.order === undefined))) return false;
  return writes.some(write => write.path === '')
    && new Set(writes.map(write => `${write.id}::${write.path}`)).size === writes.length;
}

export function isShotGroupDeletionInverse(command: EditCommand | undefined): boolean {
  return isClipStructureInverse(command) && (command!.args.writes as Array<{ id: string }>).some(write => groupId(write.id));
}

export function clipStructureInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | null | undefined {
  const undo = commands.length === 1 && isClipStructureInverse(commands[0]);
  if (!undo && !isClipStructureBatch(commands)) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const prior = undo ? commands[0].args.writes as Array<{ id: string; path: string; order?: string[] }> : [];
  if (isShotGroupDeletionBatch(commands) || undo && isGroupDeletionInverse(commands[0])) {
    const call = commands[0];
    const group = call.args.group as { shotId: string; trackId: string } | undefined;
    const sid = group && shotGroupIdentity(group.shotId, group.trackId);
    const selected = undo ? prior.map(write => write.id) : [sid!, ...call.args.remove_clip_ids as string[]];
    const writes = result.change.direct_writes;
    if (undo && result.accepted_publication_id === call.args.publication) return undefined;
    if (writes.length !== selected.length || writes.some(write => !record(write) || write.path !== '' || !selected.includes(write.id as string))
      || new Set(writes.map(write => (write as Record<string, unknown>).id)).size !== selected.length) return undefined;
    const inverted = writes.map(value => {
      const write = value as Record<string, unknown>;
      const source = undo ? prior.find(row => row.id === write.id) : undefined;
      const expected = undo ? source as unknown as { before: unknown; after: unknown }
        : { before: call.expect![`${write.id}::`], after: { state: 'absent' } };
      if (canonicalJsonStringify(write.before) !== canonicalJsonStringify(expected.before) || canonicalJsonStringify(write.after) !== canonicalJsonStringify(expected.after)) return null;
      const captured = groupId(write.id) ? call.expect?.[`${sid}::group_order`]
        : Object.entries(call.expect ?? {}).find(([key]) => key.endsWith('::clip_order'))?.[1];
      const order = undo ? source!.order : captured?.state === 'present' ? captured.value : undefined;
      return { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before), order: structuredClone(order) };
    });
    if (!inverted.every(record)) return undefined;
    const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id, writes: inverted } };
    if (!isClipStructureInverse(inverse)) return undefined;
    validateEditCommand(inverse); return inverse;
  }
  const allowed = undo ? prior : commands.flatMap(command => command.op === 'clip.nudge'
    ? [{ id: command.select!, path: 'at' }] : ['timeline.remove', 'clip.remove'].includes(command.op)
    ? [{ id: command.select!, path: '' }]
    : [{ id: command.created![0], path: '' }, ...(command.op === 'timeline.split'
      ? ['to', 'hold'].map(path => ({ id: command.select!, path })) : [])]);
  if (result.change.direct_writes.some(write => !record(write) || !allowed.some(row => row.id === write.id && row.path === write.path))) return undefined;
  const order = undo ? undefined : commands[0].op === 'timeline.remove' ? capturedOrder(commands[0])
    : commands[0].op === 'clip.remove' ? capturedClipOrder(commands[0]) : undefined;
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map(write => {
      if (!record(write)) return write;
      const capturedOrder = undo ? prior.find(row => row.id === write.id && row.path === write.path)?.order : order;
      return { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before),
        ...(capturedOrder ? { order: structuredClone(capturedOrder) } : {}) };
    }),
  } };
  if (!isClipStructureInverse(inverse)) return undefined;
  validateEditCommand(inverse); return inverse;
}
