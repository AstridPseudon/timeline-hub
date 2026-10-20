import type { AgentState, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { AuthoredState, ClipMoveError, MoveRecording, copy, equal, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

type ObjectValue = { [key: string]: JSON };
type CollectionKind = 'occurrence' | 'track' | 'clip';

export const rawIdentity = (value: unknown): value is string =>
  typeof value === 'string' && value.length > 0 && !value.includes('/') && !value.includes('::');

export class OccurrenceMediaState extends AuthoredState {
  entity(ref: string, optional = false): ObjectValue | undefined {
    if (!ref.includes('/asset:')) return super.entity(ref, optional);
    const [owner, identity] = ref.split('/asset:');
    const registry = this.config(owner).registry;
    if (!object(registry) || !object(registry.assets)) throw new ClipMoveError('asset collection must be an object');
    if (!has(registry.assets, identity)) {
      if (optional) return undefined;
      throw new ClipMoveError('missing asset identity', 'identity_conflict');
    }
    const entry = registry.assets[identity];
    if (!object(entry)) throw new ClipMoveError('asset binding must be an object');
    return entry;
  }

  rows(owner: string, kind: CollectionKind): ObjectValue[] {
    const rows = kind === 'occurrence' ? this.bundle.placements : this.config(owner)[`${kind}s`];
    const key = kind === 'occurrence' ? 'occurrence_id' : 'id';
    if (!Array.isArray(rows) || rows.some((row) => !object(row) || !rawIdentity(row[key]))
      || new Set(rows.map((row) => object(row) ? row[key] : null)).size !== rows.length) {
      throw new ClipMoveError('missing or ambiguous collection identity', 'identity_conflict');
    }
    return rows.filter(object);
  }

  get(ref: string, path: string[]): AgentState {
    if (!ref.includes('/collection:')) return super.get(ref, path);
    if (path.length) throw new ClipMoveError('collection shape requires the whole guard');
    const [owner, kind] = ref.split('/collection:');
    if (kind === 'occurrence') return { state: 'present', value: { container: 'array' } };
    const key = `${kind}s`, value = this.config(owner)[key];
    const members: AgentState = has(this.config(owner), key)
      ? { state: 'present', value: Array.isArray(value) ? [] : object(value) ? {} : value }
      : { state: 'absent' };
    return { state: 'present', value: { members } };
  }

  set(ref: string, path: string[], state: AgentState): void {
    if (path.length) return super.set(ref, path, state);
    if (ref.includes('/asset:')) {
      const [owner, identity] = ref.split('/asset:'), registry = this.config(owner).registry;
      if (!object(registry) || !object(registry.assets)) throw new ClipMoveError('asset collection must be an object');
      if (state.state === 'absent') delete registry.assets[identity];
      else if (object(state.value)) registry.assets[identity] = copy(state.value);
      else throw new ClipMoveError('asset binding must be an object');
      return;
    }
    const slash = ref.lastIndexOf('/'), owner = ref.slice(0, slash), identity = ref.slice(slash + '/clip:'.length);
    if (!ref.slice(slash).startsWith('/clip:') || (state.state === 'present'
      && (!object(state.value) || state.value.id !== identity))) throw new ClipMoveError('row identity differs from its scoped reference');
    const rows = this.config(owner).clips;
    this.rows(owner, 'clip');
    if (!Array.isArray(rows)) throw new ClipMoveError('structural edit requires an authored entity collection');
    const index = rows.findIndex((row) => object(row) && row.id === identity);
    if (state.state === 'absent') { if (index >= 0) rows.splice(index, 1); }
    else if (index < 0) rows.push(copy(state.value));
    else rows[index] = copy(state.value);
  }
}

export class OccurrenceMediaRecording extends MoveRecording {
  declare readonly state: OccurrenceMediaState;

  constructor(bundle: AuthoredBundle, command: EditCommand) {
    super(bundle, command);
    this.state = new OccurrenceMediaState(copy(bundle));
  }

  selectCollection(kind: CollectionKind, owner: string): void {
    const key = `collection.${kind}s`;
    const members = this.state.rows(owner, kind).map((row) => kind === 'occurrence'
      ? `occurrence:${row.occurrence_id}` : `${owner}/${kind}:${row.id}`);
    const value = { key, query_version: 1, owner, members, order: [...members], boundaries: [...members], policy: 'guard-membership' as const };
    if (this.command.selections!.some((prior) => equal(prior, value))) return;
    this.read(`${owner}/collection:${kind}`, []);
    if (owner !== 'parent') {
      this.read(owner, ['occurrence_id']);
      this.read(`${owner}/shot`, ['shot_id']);
      this.bind(`collection.owner:${key}`, owner);
    }
    this.command.selections!.push(value);
  }

  private birth(owner: string, kind: 'asset' | 'clip', identity: string, value: ObjectValue): void {
    const ref = `${owner}/${kind}:${identity}`;
    if (this.state.get(ref, []).state !== 'absent') throw new ClipMoveError('created identity is occupied', 'identity_collision');
    this.read(ref, []);
    this.write(ref, [], value);
    this.record.created.push({ ref, kind, owner });
    this.command.created!.push(ref);
  }

  createAsset(owner: string, identity: string, value: ObjectValue): void {
    this.read(owner, ['occurrence_id']);
    this.read(`${owner}/shot`, ['shot_id']);
    this.birth(owner, 'asset', identity, value);
  }

  createChild(owner: string, row: ObjectValue): void {
    this.state.rows(owner, 'clip');
    this.read(owner, ['occurrence_id']);
    this.read(`${owner}/shot`, ['shot_id']);
    this.bind('create.owner', owner);
    this.selectCollection('clip', owner);
    if (!rawIdentity(row.id)) throw new ClipMoveError('child requires a reserved raw identity');
    this.birth(owner, 'clip', row.id, row);
  }
}
