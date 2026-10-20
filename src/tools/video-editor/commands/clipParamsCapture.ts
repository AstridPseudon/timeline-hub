import type { CommandRecord, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { ClipMoveError, MoveRecording, assertFiniteJson, copy, equal, freezeJson, has, object } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

export type ClipParamsArgs = {
  values: Record<string, JSON>;
  clear: string[];
};

export type ClipParamsBasis = {
  readonly bundle: AuthoredBundle;
  readonly command: EditCommand;
};

export type ClipParamsResult = {
  command: EditCommand;
  bundle: AuthoredBundle;
  record: CommandRecord;
};

const CLAIMS = ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'] as const;

function propertyToken(key: string): string {
  return /^[A-Za-z_][\w-]*$/.test(key) ? key : `[${JSON.stringify(key)}]`;
}

function canonicalTarget(ref: string, path: string[]): string {
  return `${ref}::${path.map(propertyToken).reduce((result, token, index) =>
    index === 0 || token.startsWith('[') ? result + token : `${result}.${token}`, '')}`;
}

function canonicalizeParamClaims(ctx: MoveRecording, ref: string): void {
  for (const path of Object.keys(ctx.command.expect ?? {})) {
    if (!path.startsWith(`${ref}::params.`)) continue;
    const key = path.slice(`${ref}::params.`.length);
    const canonical = canonicalTarget(ref, ['params', key]);
    if (canonical !== path) {
      ctx.command.expect![canonical] = ctx.command.expect![path];
      delete ctx.command.expect![path];
      ctx.command.authorship![canonical] = ctx.command.authorship![path];
      delete ctx.command.authorship![path];
    }
  }
}

function assertArgs(args: unknown): asserts args is ClipParamsArgs {
  const clear = object(args) ? args.clear : undefined;
  if (!object(args) || !equal(Object.keys(args).sort(), ['clear', 'values']) || !object(args.values) ||
    !Array.isArray(clear) || clear.some((key) => typeof key !== 'string') ||
    new Set(clear).size !== clear.length ||
    Object.keys(args.values).some((key) => clear.includes(key)) ||
    (Object.keys(args.values).length === 0 && clear.length === 0)) {
    throw new ClipMoveError('clip parameters require non-empty values or explicit clears');
  }
  assertFiniteJson(args.values);
}

function assertTarget(select: unknown): asserts select is string {
  if (typeof select !== 'string' || select.includes('::') ||
    !/^(?:parent|occurrence:[^/]+)\/clip:[^/]+$/.test(select)) {
    throw new ClipMoveError('clip parameters require a stable scoped clip identity');
  }
}

// Agent _scalar_commands.py::clip_set_params, with the native handler's raw
// top-level params semantics. Agent remains the schema/registry authority.
function apply(bundle: AuthoredBundle, supplied: EditCommand): ClipParamsResult {
  assertTarget(supplied.select);
  if (supplied.schema_version !== 1 || supplied.op !== 'clip.set-params' || supplied.version !== '1') {
    throw new ClipMoveError('unsupported clip.set-params v1 command');
  }
  if (has(supplied, 'intent') && !equal(supplied.intent, {})) {
    throw new ClipMoveError('clip parameters have no intention overrides');
  }
  assertArgs(supplied.args);
  if (!object(bundle.parent) || !object(bundle.base_parent)) {
    throw new ClipMoveError('clip parameters require an authored parent source pin');
  }

  const ctx = new MoveRecording(bundle, { ...supplied, intent: {} });
  if (ctx.read(supplied.select, ['id']) == null) {
    throw new ClipMoveError('scalar target disappeared', 'identity_conflict');
  }
  const owner = supplied.select.slice(0, supplied.select.lastIndexOf('/'));
  if (owner !== 'parent') {
    ctx.read(owner, ['occurrence_id']);
    ctx.read(`${owner}/shot`, ['shot_id']);
    const source = ctx.state.occurrence(owner).shot_id;
    const mapping = object(bundle.source_mapping) && object(bundle.source_mapping.shots)
      ? bundle.source_mapping.shots : undefined;
    const pin = mapping?.[String(source)];
    if (!object(pin)) throw new ClipMoveError('missing occurrence source pin', 'identity_conflict');
    ctx.bind('scalar.owner', owner);
    ctx.dependency('scalar.images', 'entity', { parent: copy(bundle.base_parent), source: copy(pin) });
  } else {
    ctx.dependency('scalar.images', 'entity', { parent: copy(bundle.base_parent) });
  }
  ctx.bind('scalar.target', supplied.select, ['scalar.images']);

  for (const key of ['clipType', 'clip_type', 'asset', 'asset_id', 'media_id', 'object_id']) {
    ctx.read(supplied.select, [key]);
  }

  ctx.object(supplied.select, ['params']);
  const values = supplied.args.values;
  for (const key of Object.keys(values).sort()) ctx.write(supplied.select, ['params', key], values[key]);
  for (const key of [...supplied.args.clear].sort()) ctx.clear(supplied.select, ['params', key]);
  canonicalizeParamClaims(ctx, supplied.select);
  ctx.compile();

  for (const key of CLAIMS) {
    if (has(supplied, key) && !equal(supplied[key], ctx.command[key])) {
      throw new ClipMoveError(`submitted ${key} does not match original capture`, 'capture_mismatch');
    }
  }
  return { command: ctx.command, bundle: ctx.state.bundle, record: ctx.record };
}

/** Capture the immutable authored basis before a local preview can mutate it. */
export function captureClipParams(bundle: AuthoredBundle, select: string, args: ClipParamsArgs): ClipParamsBasis {
  assertFiniteJson(bundle);
  assertFiniteJson(select);
  assertFiniteJson(args);
  assertArgs(args);
  const snapshot = copy(bundle);
  const { command } = apply(snapshot, {
    schema_version: 1,
    op: 'clip.set-params',
    version: '1',
    select,
    args: copy(args),
  });
  return freezeJson({ bundle: snapshot, command });
}

/** Finish against the original basis; no ACK or refreshed display state is consulted. */
export function finishClipParams(basis: unknown, args: ClipParamsArgs): ClipParamsResult {
  assertFiniteJson(basis);
  assertFiniteJson(args);
  assertArgs(args);
  if (!object(basis) || !object(basis.bundle) || !object(basis.command) ||
    !CLAIMS.every((key) => has(basis.command as object, key))) {
    throw new ClipMoveError('incomplete clip parameters basis');
  }
  return apply(basis.bundle as AuthoredBundle, {
    ...copy(basis.command as EditCommand),
    args: copy(args),
  });
}
