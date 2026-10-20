import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { remapItems } from './authoringBundle.ts';
import {
  assertFiniteJson, ClipMoveError, copy, equal, freezeJson, has, MoveRecording, object, sha256,
  type AuthoredBundle,
} from './clipMovePrimitives.ts';

type ObjectValue = { [key: string]: JSON };
export type OccurrenceDuplicateArgs = { occurrence_id: string; shot_id: string };
export type OccurrenceDuplicateBasis = { readonly bundle: AuthoredBundle; readonly command: EditCommand };
const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;
const stableId = (value: unknown): value is string => typeof value === 'string' && value.length > 0
  && !value.includes('/') && !value.includes('::');

function apply(bundle: AuthoredBundle, supplied: EditCommand) {
  const allowed = ['schema_version', 'op', 'version', 'select', 'args', 'intent', 'rationale', 'group_id', ...CLAIMS];
  if (Object.keys(supplied).some((key) => !allowed.includes(key))
    || supplied.schema_version !== 1 || supplied.op !== 'occurrence.duplicate' || supplied.version !== '1'
    || typeof supplied.select !== 'string' || !/^occurrence:(?!.*::)[^/]+$/.test(supplied.select)
    || !equal(supplied.intent, { ownership: 'occurrence' })
    || !object(supplied.args) || !equal(Object.keys(supplied.args).sort(), ['occurrence_id', 'shot_id'])
    || !stableId(supplied.args.occurrence_id) || !stableId(supplied.args.shot_id)
    || (has(supplied, 'rationale') && typeof supplied.rationale !== 'string')
    || (has(supplied, 'group_id') && (typeof supplied.group_id !== 'string' || !supplied.group_id))) {
    throw new ClipMoveError('duplicate requires one explicit occurrence and two reserved identities');
  }
  const owner = supplied.select;
  const { occurrence_id: occurrenceId, shot_id: shotId } = supplied.args as OccurrenceDuplicateArgs;
  const ctx = new MoveRecording(bundle, supplied);
  const groups = ctx.read('parent', ['config', 'pinnedShotGroups']);
  if (groups !== undefined && groups !== null && !equal(groups, [])) {
    throw new ClipMoveError('legacy groups require recorded migration', 'migration_needed');
  }
  const row = ctx.read(owner, []);
  if (!object(row)) throw new ClipMoveError('duplicate source disappeared', 'identity_conflict');
  const sourceShot = ctx.read(`${owner}/shot`, ['shot_id']);
  for (const kind of ['clip', 'track']) {
    const rows = ctx.state.config(owner)[`${kind}s`];
    if (!Array.isArray(rows) || !rows.every((row) => object(row) && stableId(row.id))) {
      throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
    }
    const members = rows.map((row) => `${owner}/${kind}:${(row as ObjectValue).id}`);
    if (new Set(members).size !== members.length) throw new ClipMoveError('ambiguous collection identity', 'identity_conflict');
    ctx.read(`${owner}/collection:${kind}`, []);
    ctx.read(owner, ['occurrence_id']);
    ctx.read(`${owner}/shot`, ['shot_id']);
    ctx.bind(`collection.owner:collection.${kind}s`, owner);
    ctx.command.selections!.push({ key: `collection.${kind}s`, query_version: 1, owner,
      members, order: [...members], boundaries: [...members], policy: 'guard-membership' });
  }
  const internal = ctx.read(`${owner}/source`, []);
  const payload = ctx.read(`${owner}/shot`, ['payload']);
  if (!object(internal) || !object(payload)) throw new ClipMoveError('missing authored source', 'identity_conflict');
  if (occurrenceId === row.occurrence_id || shotId === sourceShot) {
    throw new ClipMoveError('duplicate requires reserved identities distinct from the source', 'identity_collision');
  }
  const remap = new Map<string, string>();
  const items = has(payload, 'items') ? payload.items : [];
  if (!Array.isArray(items)) throw new ClipMoveError('shot payload.items must be a list');
  for (const item of items) {
    const id = object(item) ? has(item, 'item_id') ? item.item_id : item.id : undefined;
    if (typeof id !== 'string' || !id || remap.has(id)) throw new ClipMoveError('missing or ambiguous shot item identity');
    remap.set(id, 'shot-item-placement-' + sha256(['shot-item-placement',
      ...[bundle.project_id, bundle.timeline_id, occurrenceId, shotId, id].map((part) => JSON.stringify(part))].join('\0')));
  }
  const occupied = new Set(Object.values(bundle.shots).flatMap((shot) =>
    ((shot.payload as ObjectValue).items as ObjectValue[] ?? []).map((item) => item.item_id ?? item.id)));
  if ([...remap.values()].some((id) => occupied.has(id))) throw new ClipMoveError('duplicate item identity is occupied', 'identity_collision');
  ctx.bind('duplicate.owner', owner);
  const created = copy(row);
  delete created.shot_revision_id;
  delete created.revision_id;
  Object.assign(created, { occurrence_id: occurrenceId, shot_id: shotId });
  const document = (bundle.source_mapping as ObjectValue)._runtime_document as ObjectValue | undefined;
  const mapping = bundle.source_mapping as ObjectValue;
  for (const [kind, id, value] of [
    ['shot', shotId, { payload: remapItems(payload, remap), internal_timeline: copy(internal) }],
    ['occurrence', occurrenceId, created],
  ] as const) {
    const ref = `${kind}:${id}`;
    const retained = document ? kind === 'shot'
      ? (document.shot_revisions as ObjectValue[]).some((row) => row.shot_id === id)
      : (((document.parent_revision as ObjectValue).payload as ObjectValue).occurrences as ObjectValue[])
        .some((row) => row.occurrence_id === id)
      : kind === 'shot' ? Object.values(mapping.shots as ObjectValue).some((row) => (row as ObjectValue).shot_id === id)
        : has(mapping.placements as ObjectValue, id);
    if (retained || ctx.state.get(ref, []).state !== 'absent') throw new ClipMoveError('created identity is occupied', 'identity_collision');
    ctx.read(ref, []);
    const before = { state: 'absent' as const };
    const after = { state: 'present' as const, value: copy(value) };
    ctx.command.expect![`${ref}::`] = before;
    ctx.command.authorship![`${ref}::`] = 'direct';
    ctx.command.created!.push(ref);
    ctx.record.writes.push({ ref, path: [], before, after });
    ctx.record.created.push({ ref, kind, owner: kind === 'shot' ? null : 'parent' });
    if (kind === 'shot') Object.defineProperty(ctx.state.bundle.shots, id, { value: {
      shot_id: id, ...copy(value), _created: true,
    }, enumerable: true, writable: true, configurable: true });
    else ctx.state.bundle.placements.push(copy(value));
  }
  ctx.compile();
  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  // Compiled revision IDs and the two root identity fields belong to Agent's compiler.
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

export function executeOccurrenceDuplicate(bundle: AuthoredBundle, command: EditCommand) {
  assertFiniteJson(bundle);
  assertFiniteJson(command);
  return apply(bundle, command);
}

export function captureOccurrenceDuplicate(bundle: AuthoredBundle, ownerRef: string, args: OccurrenceDuplicateArgs): OccurrenceDuplicateBasis {
  const snapshot = copy(bundle);
  const result = executeOccurrenceDuplicate(snapshot, {
    schema_version: 1, op: 'occurrence.duplicate', version: '1', select: ownerRef,
    args: copy(args), intent: { ownership: 'occurrence' },
  });
  return freezeJson({ bundle: snapshot, command: result.command });
}

export function finishOccurrenceDuplicate(basis: unknown) {
  assertFiniteJson(basis);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command)
    || !CLAIMS.every((key) => has(basis.command as object, key))) throw new ClipMoveError('incomplete duplicate basis');
  return executeOccurrenceDuplicate(basis.bundle as AuthoredBundle, basis.command as EditCommand);
}
