import { describe, expect, it } from 'vitest';
import type { TimelineData } from '../lib/timeline-data.ts';
import type { TimelineClip, TrackDefinition } from '../types/index.ts';
import type { AstridElementHost, AstridElementDescriptor } from '../runtime/astrid-element-host.ts';
import { compositeEffectGestureCommands, fadeGestureCommand } from './semanticGestures.ts';

const track: TrackDefinition = { id: 'V1', kind: 'visual', label: 'V1' };

function timeline(clips: TimelineClip[], tracks: TrackDefinition[] = [track]) {
  return { config: { clips } as TimelineData['config'], tracks } as Pick<TimelineData, 'config' | 'tracks'>;
}

function descriptor(overrides: Partial<AstridElementDescriptor> = {}): AstridElementDescriptor {
  return {
    id: 'cross-fade', kind: 'transition', revision: 'sha256:transition-r1',
    packId: 'rendering', componentPath: 'transitions/cross-fade', ...overrides,
  };
}

function elementHost(descriptors = [descriptor()]): AstridElementHost {
  const component = () => null;
  return {
    descriptors,
    sequenceRegistry: {},
    resolveComponent: (id, kind, packId) => descriptors.some((item) => item.id === id
      && item.kind === kind && item.packId === packId) ? component : undefined,
    resolveSequenceClipEntry: () => undefined,
    describeClipCapability: () => undefined,
  };
}

function transitionFixture(overrides: Partial<TimelineClip> = {}) {
  const predecessor: TimelineClip = {
    id: 'before', at: 0, hold: 2, track: 'V1', clipType: 'hold',
    app: { astrid: { on: 'beat 1', until: 'beat 2' } },
  };
  const destination: TimelineClip = {
    id: 'after', at: 2, hold: 2, track: 'V1', clipType: 'hold',
    params: { sibling: { retained: true } }, app: { clipSentinel: true }, ...overrides,
  };
  return timeline([predecessor, destination]);
}

describe('mounted composite-effect callback construction', () => {
  it('writes one fade side in seconds and leaves the other side omitted', () => {
    const data = timeline([{
      id: 'clip', at: 1, hold: 2, track: 'V1', clipType: 'hold',
      effects: { fade_out: 0.2, preserved: 8 }, exit: { type: 'fade-out', duration: 0.2 },
      app: { preserved: { opaque: true } },
    }]);
    const result = compositeEffectGestureCommands(data, 'clip', {
      entrance: { type: 'fade', duration: 0.37 },
    });

    expect(result.commands).toEqual([{
      op: 'clip.set-fade', select: 'parent/clip:clip', resolved: ['parent/clip:clip'],
      args: { fade_in: 0.37 },
      expect: {
        entrance: { state: 'absent' },
        effects: { state: 'present', value: { fade_out: 0.2, preserved: 8 } },
        exit: { state: 'present', value: { type: 'fade-out', duration: 0.2 } },
      },
    }]);
    expect(result.localPatch).toEqual({
      entrance: { type: 'fade', duration: 0.37 },
      effects: { fade_out: 0.2, preserved: 8, fade_in: 0.37 },
    });
  });

  it('keeps null and clear distinct and removes only the requested coupled fade fields', () => {
    const data = timeline([{
      id: 'clip', at: 1, hold: 2, track: 'V1', clipType: 'hold',
      entrance: { type: 'fade', duration: 0.4 }, effects: { fade_in: 0.4, preserved: 8 },
    }]);
    const presentNull = compositeEffectGestureCommands(data, 'clip', { entrance: null });
    const clear = compositeEffectGestureCommands(data, 'clip', { entrance: undefined });

    expect(presentNull.commands?.[0].args).toEqual({ fade_in: null });
    expect(presentNull.localPatch).toEqual({ entrance: null, effects: { fade_in: null, preserved: 8 } });
    expect(clear.commands?.[0].args).toEqual({ clear: ['fade_in'] });
    expect(clear.localPatch).toEqual({ entrance: undefined, effects: { preserved: 8 } });
    expect(fadeGestureCommand(data, 'clip', { fade_in: 0.3, clear: ['fade_in'] })).toBeUndefined();
    expect(fadeGestureCommand(data, 'clip', { fade_in: null, clear: ['fade_in'] })).toBeUndefined();
    expect(fadeGestureCommand(data, 'clip', { fade_out: Number.NaN })).toBeUndefined();
    expect(fadeGestureCommand(data, 'clip', { fade_out: true as unknown as number })).toBeUndefined();
  });

  it('sends the exact selected transition, resource reference and unique adjacent predecessor', () => {
    const data = transitionFixture();
    const reference = {
      id: 'cross-fade', revision: 'sha256:transition-r1', kind: 'transition' as const,
      packId: 'rendering', opaque: { keep: null },
    };
    const result = compositeEffectGestureCommands(data, 'after', {
      transition: {
        type: 'cross-fade', revision: 'sha256:transition-r1', duration: 0.731,
        params: null, opaqueTransition: { keep: true },
      } as never,
      elementRef: reference,
    }, { elementHost: elementHost() });

    expect(result.commands).toEqual([{
      op: 'clip.set-transition', select: 'parent/clip:after', resolved: ['parent/clip:after'],
      args: {
        from_clip: 'parent/clip:before', elementRef: reference,
        transition: {
          type: 'cross-fade', revision: 'sha256:transition-r1', duration: 0.731,
          params: null, opaqueTransition: { keep: true },
        },
      },
      expect: expect.objectContaining({
        transition: { state: 'absent' }, elementRef: { state: 'absent' },
        'parent/clip:before::track': { state: 'present', value: 'V1' },
        'parent/clip:before::at': { state: 'present', value: 0 },
        'parent/track:V1::kind': { state: 'present', value: 'visual' },
      }),
    }]);
    expect(result.commands?.[0].args).not.toHaveProperty('duration_frames');
    expect(result.localPatch).toEqual({ transition: expect.any(Object), elementRef: reference });
  });

  it.each([
    ['absent params', undefined],
    ['null params', null],
    ['empty params', {}],
  ])('retains captured reference and the %s distinction on a property update', (_label, params) => {
    const reference = {
      id: 'cross-fade', revision: 'sha256:transition-r1', kind: 'transition', packId: 'rendering', opaque: { keep: null },
    };
    const existing = {
      type: 'cross-fade', revision: 'sha256:transition-r1', duration: 0.5,
      opaqueTransition: { sibling: 'preserved' },
      ...(params === undefined ? {} : { params }),
    };
    const data = transitionFixture({ transition: existing as unknown as TimelineClip['transition'], elementRef: reference as unknown as TimelineClip['elementRef'] });
    const result = compositeEffectGestureCommands(data, 'after', {
      transition: { ...existing, duration: 0.83 } as never,
    }, { elementHost: elementHost() });

    expect(result.commands).toHaveLength(1);
    expect(result.commands?.[0].args).toEqual({
      transition: { ...existing, duration: 0.83 }, elementRef: reference,
    });
    expect(result.commands?.[0].expect).toEqual(expect.objectContaining({
      transition: { state: 'present', value: existing },
      elementRef: { state: 'present', value: reference },
    }));
    expect(result.commands?.[0].args).not.toHaveProperty('from_clip');
  });

  it('keeps transition clear and present-null exact and refuses invalid bindings or placement', () => {
    const reference = { id: 'cross-fade', revision: 'sha256:transition-r1', kind: 'transition' as const, packId: 'rendering' };
    const existing = { type: 'cross-fade', revision: 'sha256:transition-r1', duration: 0.5, params: {} };
    const data = transitionFixture({ transition: existing, elementRef: reference as unknown as TimelineClip['elementRef'] });
    const options = { elementHost: elementHost() };
    const clear = compositeEffectGestureCommands(data, 'after', { transition: undefined }, options);
    const presentNull = compositeEffectGestureCommands(data, 'after', { transition: null }, options);
    expect(clear.commands?.[0].args).toEqual({ clear: true });
    expect(presentNull.commands?.[0].args).toEqual({ transition: null });

    const assignment = {
      transition: { type: 'cross-fade', revision: 'sha256:transition-r1', duration: 0.5 },
      elementRef: reference,
    };
    const pluralKindReference = { ...reference, kind: 'transitions' };
    expect(compositeEffectGestureCommands(transitionFixture(), 'after', {
      transition: assignment.transition, elementRef: pluralKindReference as never,
    }, options).commands?.[0].args).toEqual({
      from_clip: 'parent/clip:before', elementRef: pluralKindReference, transition: assignment.transition,
    });
    expect(compositeEffectGestureCommands(data, 'after', {
      transition: { ...assignment.transition, revision: 'stale' }, elementRef: reference,
    }, options).commands).toBeUndefined();
    expect(compositeEffectGestureCommands(data, 'after', {
      transition: assignment.transition, elementRef: { ...reference, kind: 'effect' } as never,
    }, options).commands).toBeUndefined();
    expect(compositeEffectGestureCommands(data, 'after', {
      transition: assignment.transition, elementRef: { ...reference, id: 'foreign' },
    }, options).commands).toBeUndefined();

    const noPredecessor = timeline([{ id: 'after', at: 2.01, hold: 2, track: 'V1', clipType: 'hold' }]);
    expect(compositeEffectGestureCommands(noPredecessor, 'after', assignment, options).commands).toBeUndefined();
    const tooLong = { ...assignment, transition: { ...assignment.transition, duration: 2.01 } };
    expect(compositeEffectGestureCommands(transitionFixture(), 'after', tooLong, options).commands).toBeUndefined();
    const shortPredecessor = timeline([
      { id: 'before', at: 0, hold: 0.3, track: 'V1', clipType: 'hold' },
      { id: 'after', at: 0.3, hold: 2, track: 'V1', clipType: 'hold' },
    ]);
    expect(compositeEffectGestureCommands(shortPredecessor, 'after', assignment, options).commands).toBeUndefined();
    const overlapping = transitionFixture();
    overlapping.config.clips.push({ id: 'overlap', at: 1, hold: 1.5, track: 'V1', clipType: 'hold' });
    expect(compositeEffectGestureCommands(overlapping, 'after', assignment, options).commands).toBeUndefined();
    const nonVisualTrack = transitionFixture();
    expect(compositeEffectGestureCommands(timeline(nonVisualTrack.config.clips, [
      { ...track, kind: 'audio' },
    ]), 'after', assignment, options).commands).toBeUndefined();
    const unqualifiedReferenceAssignment = {
      ...assignment,
      elementRef: { id: reference.id, revision: reference.revision, kind: 'transition' as const },
    };
    expect(compositeEffectGestureCommands(transitionFixture(), 'after', unqualifiedReferenceAssignment, {
      elementHost: elementHost([descriptor(), descriptor({ packId: 'foreign-pack' })]),
    }).commands).toBeUndefined();
  });
});
