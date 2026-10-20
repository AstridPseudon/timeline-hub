import { describe, expect, it } from 'vitest';
import { audioEnvelopeAt, compileAudioEnvelope } from '@banodoco/timeline-composition/evaluation';

import fixture from './shotComposition.fixture.json';
import vectors from './shotCompositionAudio.fixture.json';
import { createShotCompositionAdapter } from './shotCompositionAdapter.ts';
import { projectCanonicalComposition } from './shotCompositionProjection.ts';
import type { ResolvedTimelineClip } from '../types/index.ts';

type Vector = (typeof vectors)[number];
type AudioFields = Pick<ResolvedTimelineClip, 'from' | 'to' | 'hold' | 'speed' | 'volume' | 'params' | 'effects'>;

// Exact sound fields from Agent 4a75f68f3 project_shot_composition, without
// defaults or time-map conversion. The same JSON vectors feed its public helper.
const agentAudio: Record<string, AudioFields> = {
  'unity occurrence gain': { from: 0.125, to: 1.125, volume: 0.8 },
  'missing child volume': { from: 0.125, to: 1.125, volume: 0.5 },
  'occurrence mute': { from: 0.125, to: 1.125, volume: 0 },
  'child times occurrence gain': { from: 0.125, to: 1.125, volume: 0.4 },
  'boost times occurrence gain': { from: 0.125, to: 1.125, volume: 3 },
  'occurrence source offset': { from: 0.125, to: 1.125, volume: 0.8 },
  'occurrence speed without child speed': { from: 0.125, to: 1.125, volume: 0.8 },
  'source hold capped at next occurrence': { hold: 7.5, speed: 2, volume: 0.8 },
  'source trim capped at next occurrence': { from: 0.125, to: 7.625, speed: 2, volume: 0.8 },
  'params fades': { from: 0.05, to: 0.55, volume: 0.8, params: { fadeIn: 0.1, fadeOut: 0.1 } },
  'fixture effects shape': { from: 0.05, to: 0.55, volume: 0.8, effects: [{ fade_in: 0.1, fade_out: 0.1 }] },
};

function projectAudio(vector: Vector): ResolvedTimelineClip {
  const graph = JSON.parse(JSON.stringify(fixture)) as typeof fixture;
  Object.assign(graph.occurrences[0], { duration_ms: 4000 }, vector.occurrence);
  const revision = graph.shot_revisions.find(row => row.shot_id === 'shot-alpha' && row.revision_id === 'rev-a')!;
  const clips = revision.internal_timeline_revision.timeline.clips as Array<Record<string, unknown>>;
  clips[1] = { id: 'alpha-audio', clip_type: 'media', track: 'audio', at: 0.25, ...vector.clip };
  const original = JSON.stringify(graph);
  const prepared = createShotCompositionAdapter({ load: async () => graph }).prepare(graph);
  const projected = projectCanonicalComposition(prepared).config.clips.find(clip => clip.id === 'occ-1:alpha-audio');
  expect(JSON.stringify(graph)).toBe(original);
  expect(projected).toBeDefined();
  return projected!;
}

describe('App / exact Agent audio projection contract (review only)', () => {
  // Parity requirements deliberately remain ordinary failing tests until the
  // projection owners reconcile them; controls must continue to pass.
  it.each(vectors)('$lane: $name', vector => {
    const projected = projectAudio(vector);
    const reference = agentAudio[vector.name];
    expect(projected.id).toBe('occ-1:alpha-audio');
    expect(projected.at).toBe(0.25);
    for (const field of ['volume', 'from', 'to', 'speed', 'hold', 'params', 'effects'] as const) {
      expect.soft(projected[field], field).toEqual(reference[field]);
    }
  });
});

describe('public audio envelope controls on actual App projection', () => {
  it.each([30, 30000 / 1001])('compiles params fades with frame-rounded endpoints at fps %s', fps => {
    const vector = vectors.find(row => row.name === 'params fades')!;
    const projected = projectAudio(vector);
    const reference = { id: projected.id, at: 0.25, track: 'audio', ...agentAudio[vector.name] };
    const envelope = compileAudioEnvelope(projected, fps)!;
    expect(envelope).toBeDefined();
    expect(envelope).toEqual(compileAudioEnvelope(reference, fps));
    for (const [frame, gain] of [[0, 0], [1, 1 / 3], [3, 1], [7, 1], [12, 1], [14, 1 / 3], [15, 0]]) {
      expect(audioEnvelopeAt(envelope, frame / fps)).toBeCloseTo(gain, 12);
    }
    expect(projected.volume).toBe(0.8);
    expect(projected.params).toEqual(vector.clip.params);
  });

  it('preserves effects fields without mistaking the fixture for an envelope fade proof', () => {
    const vector = vectors.find(row => row.name === 'fixture effects shape')!;
    const projected = projectAudio(vector);
    expect(projected.effects).toEqual(vector.clip.effects);
    expect(compileAudioEnvelope(projected, 30)).toBeUndefined();
  });
});
