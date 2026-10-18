import { canonicalJsonStringify } from '../data/typed/timelineBundle.ts';
import { readSelectedProjectMediaIdentity, selectedMediaRegistryExpectationPath } from './selectedProjectMedia.ts';
import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';

const record = (value: unknown): value is Record<string, unknown> => value !== null && typeof value === 'object' && !Array.isArray(value);
const scoped = (value: unknown): value is string => typeof value === 'string' && /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);
const paths = (command: EditCommand): string[] => command.op === 'clip.nudge' ? ['at', 'intent.on', 'intent.fixed_start'] : command.op === 'clip.set-track' ? ['track'] : command.op === 'clip.set-duration' ? ['hold'] : command.op === 'clip.trim' ? ['from', 'to', 'hold'] : ['speed'];

const groupId = (value: unknown): value is string => typeof value === 'string' && /^parent\/shot-group:[A-Za-z0-9_-]+$/.test(value);
const trackId = (value: unknown): value is string => typeof value === 'string' && /^parent\/track:[^/\s]+$/.test(value);
const exact = (value: Record<string, unknown>, keys: string[]) => Object.keys(value).length === keys.length && keys.every(key => Object.prototype.hasOwnProperty.call(value, key));
const groupIdentity = (shotId: string, track: string) => `parent/shot-group:${btoa(String.fromCharCode(...new TextEncoder().encode(JSON.stringify([shotId, track])))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')}`;

/** One transfer plus its literal timing commands, optionally after an existing
 * guarded parent lane allocation. The ordinary receipt/inverse owner is reused.
 */
export function isShotGroupTransferBatch(commands: readonly (Omit<EditCommand, 'created' | 'resolved'> & {
  created?: readonly string[]; resolved?: readonly string[];
})[]): boolean {
  const index = commands[0]?.op === 'timeline.add' ? 1 : 0;
  const transfer = commands[index];
  if (!transfer || transfer.op !== 'shot-group.set' || transfer.select !== null
    || !exact(transfer as unknown as Record<string, unknown>, ['op', 'select', 'args'])
    || !exact(transfer.args, ['group', 'intent', 'target', 'members']) || transfer.args.intent !== 'transfer'
    || !record(transfer.args.group) || !exact(transfer.args.group, ['shotId', 'trackId'])
    || !Object.values(transfer.args.group).every(value => typeof value === 'string' && value.length > 0 && !value.includes('/'))
    || !Array.isArray(transfer.args.members) || !transfer.args.members.length
    || !transfer.args.members.every(scoped) || new Set(transfer.args.members).size !== transfer.args.members.length
    || typeof transfer.args.target !== 'string' || !/^(?:parent|occurrence:[^/\s]+)\/track:[^/\s]+$/.test(transfer.args.target)
    || transfer.args.members.some(member => member.split('/clip:')[0] !== (transfer.args.target as string).split('/track:')[0])
    || transfer.args.target.split('/track:')[1] === transfer.args.group.trackId) return false;
  if (index) {
    const add = commands[0];
    if (!trackId(add.select) || add.select !== transfer.args.target || !record(add.args.track)
      || !exact(add.args, ['track']) || add.args.track.id !== add.select.split('/track:')[1]
      || add.args.track.kind !== 'visual' || add.created?.length !== 1 || add.created[0] !== add.select
      || add.expect?.[`${add.select}::`]?.state !== 'absent') return false;
  }
  const movement = commands.slice(index + 1);
  return movement.every(call => call.op === 'clip.nudge' && scoped(call.select)
    && (transfer.args.members as string[]).includes(call.select) && exact(call.args, ['frames'])
    && Number.isSafeInteger(call.args.frames) && call.args.frames !== 0 && record(call.expect)
    && call.resolved?.length === 1 && call.resolved[0] === call.select)
    && new Set(movement.map(call => call.select)).size === movement.length;
}

function isTransferInverseWrites(writes: Array<Record<string, unknown>>): boolean {
  const groups = writes.filter(write => groupId(write.id));
  if (groups.length !== 2 || groups.some(write => write.path !== '' || !record(write.before) || !record(write.after)
    || write.before.state === write.after.state)) return false;
  if (groups.filter(write => (write.before as Record<string, unknown>).state === 'present').length !== 1) return false;
  const rows = groups.map(write => {
    const state = (write.before as Record<string, unknown>).state === 'present' ? write.before : write.after;
    return (state as Record<string, unknown>).value;
  });
  if (rows.some(row => !record(row) || typeof row.shotId !== 'string' || typeof row.trackId !== 'string'
    || !Array.isArray(row.clipIds) || !row.clipIds.length)) return false;
  const typedRows = rows as Array<{ shotId: string; trackId: string; clipIds: string[] }>;
  const [before, after] = typedRows;
  if (before.shotId !== after.shotId || before.trackId === after.trackId
    || groups.some((write, index) => write.id !== groupIdentity(typedRows[index].shotId, typedRows[index].trackId))) return false;
  const clips = writes.filter(write => scoped(write.id));
  if (!clips.length || new Set(clips.map(write => String(write.id).split('/')[0])).size !== 1
    || clips.some(write => !['track', 'at', 'intent.on', 'intent.fixed_start'].includes(String(write.path)))) return false;
  const members = [...new Set(clips.map(write => String(write.id).split('/clip:')[1]))];
  if ([before, after].some(row => row.clipIds.length !== members.length || new Set(row.clipIds).size !== members.length
    || row.clipIds.some(id => !members.includes(id.split('/clip:').at(-1)!)))) return false;
  return writes.every(write => groupId(write.id) || scoped(write.id)
    || trackId(write.id) && write.path === '' && [before.trackId, after.trackId].includes(String(write.id).split('/track:')[1]));
}

export function isSelectedCloneBatch(commands: readonly EditCommand[]): boolean {
  const call = commands[0], media = call && readSelectedProjectMediaIdentity(call.args.media);
  const child = call?.created?.[0], source = call?.args.from;
  if (!media || call.op !== 'timeline.add' || call.select !== null || !scoped(source) || !source.startsWith('parent/')
    || !scoped(child) || !child.startsWith('parent/') || call.created?.length !== 1 || child === source
    || !exact(call.args, ['from', 'at', 'media']) || typeof call.args.at !== 'number' || !Number.isFinite(call.args.at)
    || call.args.at < 0 || call.expect?.[`${child}::`]?.state !== 'absent') return false;
  const row = call.expect[`${source}::`], order = call.expect[`${source}::clip_order`], fps = call.expect['parent::config.output.fps'];
  const registry = call.expect[selectedMediaRegistryExpectationPath(media.asset)];
  if (row?.state !== 'present' || !record(row.value) || row.value.id !== source.split('/clip:')[1]
    || order?.state !== 'present' || !Array.isArray(order.value) || !order.value.every(scoped)
    || new Set(order.value).size !== order.value.length || !order.value.includes(source) || order.value.includes(child)
    || fps?.state !== 'present' || typeof fps.value !== 'number' || !Number.isFinite(fps.value) || fps.value <= 0
    || !registry || registry.state !== 'absent' && (registry.state !== 'present' || !record(registry.value)
      || registry.value.media_id !== media.object_id)) return false;
  const orderIds = order.value as string[];
  const nudges = commands.slice(1);
  return !nudges.length || isClipPlacementBatch(nudges) && nudges.every(nudge => nudge.op === 'clip.nudge'
    && nudge.select !== source && nudge.select !== child && orderIds.includes(nudge.select!)
    && nudge.args.frames === nudges[0].args.frames && Number(nudge.args.frames) > 0
    && call.expect?.[`${nudge.select}::`]?.state === 'present');
}

/** Existing ordinary move/edge producers only; relation choices have separate owners. */
export function isClipPlacementBatch(commands: readonly EditCommand[]): boolean {
  if (isShotGroupTransferBatch(commands) || isSelectedCloneBatch(commands)) return true;
  return commands.length > 0 && commands.every((command) => scoped(command.select)
    && command.resolved?.length === 1 && command.resolved[0] === command.select
    && (command.op === 'clip.trim' ? Object.keys(command.args).every((key) => ['in_s', 'out_s'].includes(key)) : Object.keys(command.args).length === 1)
    && (command.op === 'clip.nudge' ? Number.isSafeInteger(command.args.frames) && command.args.frames !== 0
      : command.op === 'clip.set-track' ? typeof command.args.track === 'string' && Boolean(command.args.track)
      : command.op === 'clip.set-duration' ? typeof command.args.seconds === 'number' && Number.isFinite(command.args.seconds) && command.args.seconds > 0
        && command.expect?.['app.astrid.until']?.state === 'absent' && command.expect?.['app.astrid.for']?.state === 'absent'
      : command.op === 'clip.trim' ? typeof command.args.out_s === 'number' && Number.isFinite(command.args.out_s) && command.args.out_s > 0
        && (command.args.in_s === undefined || typeof command.args.in_s === 'number' && Number.isFinite(command.args.in_s) && command.args.in_s >= 0 && command.args.out_s > command.args.in_s)
      : command.op === 'clip.set-look' && typeof command.args.speed === 'number' && Number.isFinite(command.args.speed) && command.args.speed > 0)
    && record(command.expect) && Object.keys(command.expect).length > 0)
    && new Set(commands.map((command) => command.select!.split('/')[0])).size === 1
    && new Set(commands.map((command) => `${command.select}::${command.op}`)).size === commands.length;
}

/** Only publication-owned authored placement fields, never resolved consequences. */
export function isClipPlacementInverse(command: EditCommand | undefined): boolean {
  if (!command || command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || typeof command.args.publication !== 'string' || !command.args.publication
    || Object.keys(command.args).length !== 2 || !Array.isArray(command.args.writes) || !command.args.writes.length) return false;
  const writes = command.args.writes;
  const transfer = writes.every(record) && isTransferInverseWrites(writes);
  return writes.every((write: unknown) => record(write) && (transfer || scoped(write.id)
    && ['at', 'track', 'hold', 'speed', 'from', 'to', 'intent.on', 'intent.fixed_start'].includes(String(write.path)))
    && (transfer && groupId(write.id)
      ? Array.isArray(write.order) && write.order.length > 0 && write.order.every(groupId)
        && new Set(write.order).size === write.order.length
        && (record(write.after) && write.after.state === 'absent' || write.order.includes(write.id))
        && Object.keys(write).length === 5 && Object.keys(write).every(key => ['id', 'path', 'before', 'after', 'order'].includes(key))
      : Object.keys(write).length === 4 && Object.keys(write).every((key) => ['id', 'path', 'before', 'after'].includes(key)))
    && [write.before, write.after].every((state) => record(state)
      && (state.state === 'absent' ? Object.keys(state).length === 1
        : state.state === 'present' && Object.prototype.hasOwnProperty.call(state, 'value') && Object.keys(state).length === 2)))
    && (transfer || new Set(writes.map((write) => write.id.split('/')[0])).size === 1)
    && new Set(writes.map((write) => `${write.id}::${write.path}`)).size === writes.length;
}

/** Selected generation clones share the ordinary publication-owned inverse.
 * Validate every captured child/follower write before enabling whole-batch Undo.
 */
function selectedCloneInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | undefined {
  if (!isSelectedCloneBatch(commands)) return undefined;
  const call = commands[0], media = readSelectedProjectMediaIdentity(call.args.media)!;
  const child = call.created![0], from = String(call.args.from);
  const expect = call.expect!;
  const captured = expect[`${from}::`] as { state: 'present'; value: Record<string, unknown> };
  const order = (expect[`${from}::clip_order`] as { state: 'present'; value: string[] }).value;
  const fps = Number((expect['parent::config.output.fps'] as { state: 'present'; value: number }).value);
  const nudges = commands.slice(1);
  const writes = result.change.direct_writes;
  if (result.status !== 'accepted' || !result.accepted_publication_id || writes.length !== commands.length
    || new Set(writes.filter(record).map(write => `${write.id}::${write.path}`)).size !== writes.length) return undefined;
  const root = writes.find((write): write is Record<string, unknown> => record(write) && write.id === child && write.path === '');
  if (!root || !exact(root, ['id', 'path', 'before', 'after']) || !record(root.before) || !exact(root.before, ['state'])
    || root.before.state !== 'absent' || !record(root.after) || !exact(root.after, ['state', 'value'])
    || root.after.state !== 'present' || !record(root.after.value)) return undefined;
  const payload = structuredClone(captured.value);
  payload.id = child.split('/clip:')[1]; payload.at = call.args.at; payload.asset = media.asset;
  if (record(payload.app) && record(payload.app.astrid)) delete payload.app.astrid.media_registry_insert;
  const registration = expect[selectedMediaRegistryExpectationPath(media.asset)];
  if (registration?.state === 'absent') {
    const actualApp = root.after.value.app;
    const mark = record(actualApp) && record(actualApp.astrid) && actualApp.astrid.media_registry_insert;
    if (!record(mark) || !exact(mark, ['asset', 'entry_digest']) || mark.asset !== media.asset
      || typeof mark.entry_digest !== 'string' || !/^sha256:[0-9a-f]{64}$/.test(mark.entry_digest)) return undefined;
    const app: Record<string, unknown> = record(payload.app) ? payload.app : {};
    const astrid: Record<string, unknown> = record(app.astrid) ? app.astrid : {};
    astrid.media_registry_insert = mark; app.astrid = astrid; payload.app = app;
  } else if (registration?.state !== 'present' || !record(registration.value) || registration.value.media_id !== media.object_id) return undefined;
  const equal = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);
  if (!equal(root.after.value, payload)) return undefined;
  for (const nudge of nudges) {
    const original = expect[`${nudge.select}::`];
    const write = writes.find((write): write is Record<string, unknown> => record(write) && write.id === nudge.select && write.path === 'at');
    // The producer captured each follower in exact order with an explicit frame delta.
    const before = nudge.expect?.at;
    if (!original || original.state !== 'present' || !record(original.value) || !write
      || !exact(write, ['id', 'path', 'before', 'after']) || before?.state !== 'present'
      || !equal(original.value.at, before.value) || !equal(write.before, before) || !record(write.after) || write.after.state !== 'present'
      || !equal(write.after, { state: 'present', value: Number(nudge.args.frames) / fps + Number(before.value) })) return undefined;
  }
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: { publication: result.accepted_publication_id,
    writes: writes.map(value => { const write = value as Record<string, unknown>; return { ...structuredClone(write),
      before: structuredClone(write.after), after: structuredClone(write.before),
      ...(write.path === '' ? { order: [...order, child] } : {}) }; }) } };
  validateEditCommand(inverse); return inverse;
}

export function clipPlacementInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[]; commands?: EditCommand[] };
}): EditCommand | null | undefined {
  const selectedClone = selectedCloneInverse(commands, result);
  if (selectedClone) return selectedClone;
  const sourceInverse = commands.length === 1 && isClipPlacementInverse(commands[0]);
  if (!sourceInverse && !isClipPlacementBatch(commands)) return undefined;
  if (result.status === 'no_change') return null;
  if (result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const transfer = commands.find(call => call.op === 'shot-group.set' && call.args.intent === 'transfer');
  const group = transfer?.args.group as { shotId: string; trackId: string } | undefined;
  const groupWrites = result.change.direct_writes.filter((write): write is Record<string, unknown> => record(write) && groupId(write.id));
  // Collection order comes from D's accepted recorder, never a config diff.
  const recorded = transfer && result.change.commands?.find(call => call.op === 'shot-group.set'
    && call.args.intent === 'transfer' && record(call.args.group)
    && call.args.group.shotId === group?.shotId && call.args.group.trackId === group?.trackId
    && call.args.target === transfer.args.target && JSON.stringify(call.args.members) === JSON.stringify(transfer.args.members));
  const captured = group && recorded?.expect?.[`${groupIdentity(group.shotId, group.trackId)}::group_order`];
  const prior = sourceInverse ? commands[0].args.writes as Array<{ id: string; order?: string[] }> : [];
  let order = captured?.state === 'present' && Array.isArray(captured.value) && captured.value.every(groupId)
    ? captured.value as string[] : prior.find(write => groupId(write.id))?.order;
  if (sourceInverse && groupWrites.length === 2 && order) {
    const removed = groupWrites.find(write => record(write.after) && write.after.state === 'present');
    const restored = groupWrites.find(write => record(write.before) && write.before.state === 'present');
    if (removed && restored) order = order.map(id => id === removed.id ? String(restored.id) : id);
  }
  const inverse: EditCommand = { op: 'timeline.inverse', select: null, args: {
    publication: result.accepted_publication_id,
    writes: result.change.direct_writes.map((write) => record(write)
      ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before),
        ...(groupId(write.id) && order ? { order: [...order] } : {}) } : write),
  } };
  if (!isClipPlacementInverse(inverse)) return undefined;
  const writes = inverse.args.writes as Array<{ id: string; path: string }>;
  const allowed = sourceInverse ? commands[0].args.writes as Array<{ id: string; path: string }>
    : transfer && group ? [
      ...[group.trackId, String(transfer.args.target).split('/track:')[1]].map(track => ({ id: groupIdentity(group.shotId, track), path: '' })),
      ...(transfer.args.members as string[]).map(id => ({ id, path: 'track' })),
      ...commands.filter(call => call.op === 'clip.nudge').flatMap(call => paths(call).map(path => ({ id: call.select!, path }))),
      ...(commands[0].op === 'timeline.add' ? [{ id: commands[0].select!, path: '' }] : []),
    ] : commands.flatMap((command) => paths(command).map((path) => ({ id: command.select!, path })));
  if (writes.some((write) => !allowed.some((row) => row.id === write.id && row.path === write.path))) return undefined;
  validateEditCommand(inverse);
  return inverse;
}
