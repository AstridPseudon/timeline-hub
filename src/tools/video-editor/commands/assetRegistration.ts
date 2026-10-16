import { validateEditCommand, type EditCommand } from '@/integrations/runtime/generated.ts';
import type { AssetRegistryEntry } from '../types/index.ts';

const own = (value: object, key: string) => Object.prototype.hasOwnProperty.call(value, key);
const record = (value: unknown): value is Record<string, unknown> => Boolean(value) && typeof value === 'object' && !Array.isArray(value);

/** Explicit whole-entry assignment. A file-only legacy entry has no admitted command. */
export function assetRegistrationCommand(registry: unknown, assetId: string, entry: AssetRegistryEntry): EditCommand | undefined {
  const keys = ['media_id', 'object_id', 'digest', 'content_digest', 'content_sha256'];
  if (!record(entry)) throw new Error('Asset registration requires an asset object');
  if (!['media_id', 'object_id'].some((key) => own(entry, key))) return undefined;
  if (!assetId) {
    throw new Error('Asset registration requires an explicit managed source identity');
  }
  const identities = keys.filter((key) => own(entry, key)).map((key) => {
    const value = entry[key];
    if (typeof value !== 'string' || !/^(?:sha256:)?[0-9a-f]{64}$/.test(value)) {
      throw new Error(`Asset registration ${key} must be a SHA-256 media identity`);
    }
    return value.replace(/^sha256:/, '');
  });
  if (new Set(identities).size !== 1 || own(entry, 'path') || own(entry, 'local_path')) {
    throw new Error('Asset registration has conflicting identity or an unsupported local path');
  }
  let path = 'registry';
  let before: unknown;
  let present = registry !== undefined;
  if (present) {
    if (!record(registry)) throw new Error('Parent registry must be an object');
    path += '.assets';
    present = own(registry, 'assets');
    if (present) {
      if (!record(registry.assets)) throw new Error('Parent registry.assets must be an object');
      path += /^[A-Za-z_][\w-]*$/.test(assetId) ? `.${assetId}` : `[${JSON.stringify(assetId)}]`;
      present = own(registry.assets, assetId);
      before = registry.assets[assetId];
    }
  }
  const command: EditCommand = { op: 'timeline.register-asset', select: null,
    args: { asset_id: assetId, entry: structuredClone(entry) },
    expect: { [`parent::${path}`]: present ? { state: 'present', value: structuredClone(before) } : { state: 'absent' } } };
  validateEditCommand(command);
  return command;
}

/** Only this exact admitted parent aggregate may cross occurrence render projections. */
export function isAssetRegistrationCommand(command: EditCommand): boolean {
  if (command.op !== 'timeline.register-asset' || command.select !== null
    || typeof command.args?.asset_id !== 'string' || !record(command.args.entry)
    || Object.keys(command.args).some((key) => !['asset_id', 'entry'].includes(key))) return false;
  try { return Boolean(assetRegistrationCommand({ assets: {} }, command.args.asset_id, command.args.entry as AssetRegistryEntry)); }
  catch { return false; }
}

/** Only Runtime-recorded parent registry writes can supply this history inverse. */
export function isAssetRegistrationInverse(command: EditCommand): boolean {
  if (command.op !== 'timeline.inverse' || command.select !== null || !record(command.args)
    || typeof command.args.publication !== 'string' || !command.args.publication
    || Object.keys(command.args).some((key) => !['publication', 'writes'].includes(key))
    || !Array.isArray(command.args.writes) || command.args.writes.length !== 1) return false;
  return command.args.writes.every((write: unknown) => {
    if (!record(write) || write.id !== 'parent' || typeof write.path !== 'string'
      || Object.keys(write).some((key) => !['id', 'path', 'before', 'after'].includes(key))
      || !/^registry(?:\.assets(?:\.[A-Za-z_][\w-]*|\["(?:[^"\\]|\\.)*"\])?)?$/.test(write.path)) return false;
    return [write.before, write.after].every((state) => record(state)
      && (state.state === 'absent' ? Object.keys(state).length === 1
        : state.state === 'present' && own(state, 'value') && Object.keys(state).length === 2));
  });
}

/** Authenticated accepted receipt data, never a diff of optimistic UI snapshots. */
export function assetRegistrationInverse(commands: readonly EditCommand[], result: {
  status: string; accepted_publication_id: string | null; change: { direct_writes: unknown[] };
}): EditCommand | undefined {
  if (commands.length !== 1 || !(isAssetRegistrationCommand(commands[0]) || isAssetRegistrationInverse(commands[0]))
    || result.status !== 'accepted' || !result.accepted_publication_id) return undefined;
  const writes = result.change.direct_writes.map((write) => record(write)
    ? { ...structuredClone(write), before: structuredClone(write.after), after: structuredClone(write.before) } : write);
  const inverse: EditCommand = { op: 'timeline.inverse', select: null,
    args: { publication: result.accepted_publication_id, writes } };
  if (!isAssetRegistrationInverse(inverse)) return undefined;
  validateEditCommand(inverse);
  return inverse;
}
