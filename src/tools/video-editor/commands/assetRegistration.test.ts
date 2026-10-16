import { describe, expect, it } from 'vitest';
import { assetRegistrationCommand, isAssetRegistrationCommand } from './assetRegistration.ts';
import { attachGestureCommands, gestureCommandsFor, gestureOccurrenceFor } from './semanticGestures.ts';
import type { TimelineData } from '../lib/timeline-data.ts';

const media = 'sha256:' + 'a'.repeat(64);
const entry = { media_id: media, type: 'image/png', opaque: { null: null, literal: { op: 'clear' } } };

describe('W09 explicit managed entry assignment', () => {
  it.each([
    [undefined, 'parent::registry'],
    [{}, 'parent::registry.assets'],
    [{ assets: {} }, 'parent::registry.assets["literal.key"]'],
  ])('captures first missing authored registry container or entry (%j)', (registry, path) => {
    expect(assetRegistrationCommand(registry, 'literal.key', entry)).toEqual({
      op: 'timeline.register-asset', select: null, args: { asset_id: 'literal.key', entry }, expect: { [path as string]: { state: 'absent' } },
    });
  });

  it('captures the complete old entry including null and opaque values, independently of later mutation', () => {
    const old = { media_id: media, opaque: null };
    const next = structuredClone(entry);
    const call = assetRegistrationCommand({ assets: { 'literal.key': old } }, 'literal.key', next)!;
    old.opaque = {} as never; next.opaque.literal.op = 'changed';
    expect(call.expect).toEqual({ 'parent::registry.assets["literal.key"]': { state: 'present', value: { media_id: media, opaque: null } } });
    expect(call.args.entry).toEqual(entry);
  });

  it('retains file-only compatibility, but refuses malformed or disagreeing declared managed authority', () => {
    expect(assetRegistrationCommand({ assets: {} }, 'legacy', { file: 'old.png', content_sha256: 'a'.repeat(64) })).toBeUndefined();
    for (const invalid of [{ ...entry, object_id: 'sha256:' + 'b'.repeat(64) }, { ...entry, media_id: 'file:///private/asset' }, { ...entry, path: '/private/asset' }]) {
      expect(() => assetRegistrationCommand({ assets: {} }, 'bad', invalid)).toThrow();
    }
  });

  it('admits only explicit parent registration across canonical occurrence render clips', () => {
    const source = { config: { clips: [{ app: { canonical: { occurrenceId: 'occ-A' } } }] } } as unknown as TimelineData;
    const next = {} as TimelineData;
    const call = assetRegistrationCommand({ assets: {} }, 'poster', entry)!;
    attachGestureCommands(next, [call], source);
    expect(gestureCommandsFor(next)).toEqual([call]);
    expect(gestureOccurrenceFor(next)).toBeUndefined();
    expect(isAssetRegistrationCommand({ ...call, select: 'occurrence:occ-A' })).toBe(false);
    attachGestureCommands(next, [call, { op: 'unknown.snapshot', select: null, args: {} }], source);
    expect(gestureCommandsFor(next)).toBeUndefined();
  });
});
