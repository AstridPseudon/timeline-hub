import type { AgentDependency, AgentState, CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';

type ObjectValue = { [key: string]: JSON };

// Internal main authoring_bundle shape, not a Runtime wire document or a display projection.
export type AuthoredBundle = ObjectValue & {
  parent: ObjectValue;
  placements: ObjectValue[];
  shots: Record<string, ObjectValue & { internal_timeline: ObjectValue }>;
};

export class ClipMoveError extends Error {
  constructor(message: string, readonly kind = 'invalid_edit_command') {
    super(message);
  }
}

export const copy = <T>(value: T): T => structuredClone(value);
export const has = (value: object, key: string): boolean => Object.prototype.hasOwnProperty.call(value, key);
export const object = (value: unknown): value is ObjectValue =>
  value !== null && typeof value === 'object' && !Array.isArray(value);
const active = (row: ObjectValue): boolean => row.enabled !== false && row.active !== false &&
  !['disabled', 'hidden', 'deleted'].some((key) => row[key] === true);
const AUDIO_KINDS = new Set(['audio', 'vo', 'music', 'sfx', 'voice', 'voiceover']);

export function equal(a: unknown, b: unknown): boolean {
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.length === b.length && a.every((value, index) => equal(value, b[index]));
  }
  if (object(a) && object(b)) {
    const keys = Object.keys(a);
    return keys.length === Object.keys(b).length &&
      keys.every((key) => has(b, key) && equal(a[key], b[key]));
  }
  return a === b;
}

function one(rows: JSON, key: string, id: string, optional = false): ObjectValue | undefined {
  if (!Array.isArray(rows)) throw new ClipMoveError('entity collection must be an array');
  const matches = rows.filter((row): row is ObjectValue => object(row) && row[key] === id);
  if (matches.length === 1) return matches[0];
  if (optional && matches.length === 0) return undefined;
  throw new ClipMoveError(`missing or ambiguous identity ${id}`, 'identity_conflict');
}

export class AuthoredState {
  constructor(readonly bundle: AuthoredBundle) {}

  occurrence(owner: string): ObjectValue {
    return one(this.bundle.placements, 'occurrence_id', owner.slice('occurrence:'.length))!;
  }

  config(owner: string): ObjectValue {
    if (owner === 'parent') return this.bundle.parent.config as ObjectValue ?? {};
    const row = this.occurrence(owner);
    const shot = this.bundle.shots[String(row.shot_id)];
    if (!shot || !object(shot.internal_timeline)) throw new ClipMoveError('missing authored owner');
    return shot.internal_timeline;
  }

  entity(ref: string, optional = false): ObjectValue | undefined {
    if (ref.includes('/clip:') || ref.includes('/track:')) {
      const slash = ref.lastIndexOf('/');
      const owner = ref.slice(0, slash);
      const entity = ref.slice(slash + 1);
      const colon = entity.indexOf(':');
      const kind = entity.slice(0, colon);
      const id = entity.slice(colon + 1);
      const rows = owner === 'parent' && kind === 'clip' && has(this.bundle.parent, 'clips')
        ? this.bundle.parent.clips : this.config(owner)[`${kind}s`] ?? [];
      return one(rows, 'id', id, optional);
    }
    if (ref === 'parent') return this.bundle.parent;
    if (ref.endsWith('/registry')) {
      const owner = ref.slice(0, -'/registry'.length);
      const nested = this.config(owner).registry;
      if (owner !== 'parent') return nested as ObjectValue ?? {};
      const direct = this.bundle.parent.registry;
      for (const registry of [direct, nested]) {
        if (registry != null && (!object(registry) ||
          (has(registry, 'assets') && !object(registry.assets)))) {
          throw new ClipMoveError('invalid parent registry');
        }
      }
      if (direct != null && nested != null && !equal(direct, nested)) {
        throw new ClipMoveError('parent.registry conflicts with parent.config.registry');
      }
      return (direct ?? nested ?? { assets: {} }) as ObjectValue;
    }
    if (ref.endsWith('/source')) return this.config(ref.slice(0, -'/source'.length));
    if (ref.endsWith('/shot')) return { shot_id: this.occurrence(ref.slice(0, -'/shot'.length)).shot_id };
    if (ref.startsWith('occurrence:') && !ref.includes('/')) return this.occurrence(ref);
    throw new ClipMoveError(`unsupported entity reference ${ref}`);
  }

  get(ref: string, path: string[]): AgentState {
    const entity = this.entity(ref, true);
    if (entity === undefined) return { state: 'absent' };
    let value: JSON = entity;
    for (const key of path) {
      if (object(value) && has(value, key)) value = value[key];
      else if (Array.isArray(value) && /^\d+$/.test(key) && Number(key) < value.length) value = value[Number(key)];
      else return { state: 'absent' };
    }
    return { state: 'present', value: copy(value) };
  }

  set(ref: string, path: string[], state: AgentState): void {
    let target = this.entity(ref)!;
    for (const key of path.slice(0, -1)) {
      if (!object(target[key])) throw new ClipMoveError('write requires recorded container creation');
      target = target[key];
    }
    const key = path[path.length - 1];
    if (state.state === 'absent') delete target[key];
    else target[key] = copy(state.value);
  }
}

// These are the built-in Recording/selection primitives in Agent _recording.py.
// Metadata comes from executed reads/writes, including absent and unchanged writes.
export class MoveRecording {
  readonly state: AuthoredState;
  readonly command: EditCommand;
  readonly record: CommandRecord;

  constructor(bundle: AuthoredBundle, command: EditCommand) {
    this.state = new AuthoredState(copy(bundle));
    this.command = { ...copy(command), resolved: [command.select!], reads: [], selections: [],
      expect: {}, authorship: {}, bindings: {}, created: [] };
    this.record = { ordinal: 0, command: this.command, writes: [], reads: this.command.reads!,
      selections: this.command.selections!, bindings: [], created: [], dependencies: [], derived_writes: [] };
  }

  read(ref: string, path: string[]): JSON | undefined {
    const state = this.state.get(ref, path);
    const read = { ref, path, state };
    if (!this.command.reads!.some((other) => equal(read, other))) this.command.reads!.push(copy(read));
    return state.state === 'present' ? copy(state.value) : undefined;
  }

  select(key: 'move.target' | 'move.blockers', owner: string, members: string[] = []): string[] {
    let result: string[];
    if (key === 'move.target') result = members.filter((ref) => this.state.entity(ref, true) !== undefined);
    else {
      const row = this.state.occurrence(owner);
      const lane = object(row.placement) && has(row.placement, 'track') ? row.placement.track : row.track;
      const track = typeof lane === 'string' ? this.state.entity(`parent/track:${lane}`, true) : undefined;
      const output = !track || (!AUDIO_KINDS.has(String(track.kind)) && !AUDIO_KINDS.has(String(track.role)) && active(track));
      result = this.state.bundle.placements.filter((other) => {
        const otherLane = object(other.placement) && has(other.placement, 'track')
          ? other.placement.track : other.track;
        return output && active(other) && equal(lane, otherLane);
      }).map((other) => `occurrence:${other.occurrence_id}`);
    }
    this.command.selections!.push({ key, query_version: 1, owner, members: [...result],
      order: [...result], boundaries: [...result], policy: 'guard-membership' });
    return result;
  }

  bind(key: string, ref: string, dependencies: string[] = []): void {
    if (ref.includes('/clip:') || ref.includes('/track:') || (ref.startsWith('occurrence:') && !ref.includes('/'))) {
      this.command.bindings![key] = ref;
    }
    this.record.bindings.push({ key, ref, policy: 'fixed', dependencies });
  }

  dependency(key: string, kind: AgentDependency['kind'], pin: ObjectValue): void {
    this.record.dependencies.push({ key, kind, pin: copy(pin), policy: 'exact' });
  }

  assign(ref: string, path: string[], after: AgentState): void {
    const address = `${ref}::${path.join('.')}`;
    if (!has(this.command.expect!, address)) this.command.expect![address] = this.state.get(ref, path);
    this.command.authorship![address] = 'direct';
    this.record.writes.push({ ref, path: [...path], before: this.state.get(ref, path), after: copy(after) });
    this.state.set(ref, path, after);
  }

  write(ref: string, path: string[], value: JSON): void {
    this.assign(ref, path, { state: 'present', value });
  }

  clear(ref: string, path: string[]): void {
    this.assign(ref, path, { state: 'absent' });
  }

  object(ref: string, path: string[]): void {
    const state = this.state.get(ref, path);
    if (state.state === 'present' && object(state.value)) return;
    this.read(ref, path);
    if (state.state === 'present' && state.value !== null) throw new ClipMoveError('intent container must be object or null');
    this.write(ref, path, {});
  }
}
