import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import layeringFixture from './shot-layering-v1.fixture.json';
import compositionFixture from './shotComposition.fixture.json';
import { createShotCompositionAdapter } from './shotCompositionAdapter.ts';
import { CanonicalCompositionProjectionError, projectCanonicalComposition } from './shotCompositionProjection.ts';
import type { ResolvedTimelineConfig, TimelineClip } from '@/tools/video-editor/types/index.ts';

// Runtime commit 5a7a2059c37c6ccd33e66839095756697468ea46.
const canonicalPath = 'conformance/fixtures/shot-layering-v1.json';
const canonicalSha256 = '3c75d3ede4f868bedc46bfebe1c6988e159a58d4edf444986509e9a87f8fba1e';

type LayeringCase = typeof layeringFixture.cases[number];

function projectCase(testCase: LayeringCase, app?: ResolvedTimelineConfig['app']) {
  const composition = createShotCompositionAdapter({ load: async () => testCase.input }).prepare(testCase.input);
  const parent = testCase.input.parent_composition.config;
  const base: ResolvedTimelineConfig = {
    output: { resolution: '1920x1080', fps: 30, file: 'layers.mp4' },
    tracks: parent.tracks.map((track) => ({ ...track, kind: track.kind as 'visual' | 'audio', label: track.id })),
    clips: parent.clips.map((clip) => ({
      ...clip, clipType: clip.clip_type, asset: clip.asset_id, at: clip.at_ms / 1000, hold: clip.duration_ms / 1000,
    })),
    registry: parent.registry.assets as ResolvedTimelineConfig['registry'],
    app,
  };
  return projectCanonicalComposition(composition, base);
}

describe('shared Runtime shot-layering projection cases', () => {
  it('keeps an exact-byte Runtime fixture copy with a pinned canonical hash', () => {
    const bytes = readFileSync(resolve('src/tools/video-editor/data/shot-layering-v1.fixture.json'));
    expect(createHash('sha256').update(bytes).digest('hex')).toBe(canonicalSha256);
    // A Runtime checkout is optional for standalone App tests, as with other
    // colocated projection fixtures. Qualification also compares canonical bytes.
    const checkout = process.env.ASTRID_RUNTIME_CHECKOUT;
    if (checkout) {
      const file = resolve(checkout, canonicalPath);
      if (existsSync(file)) expect(bytes.equals(readFileSync(file))).toBe(true);
    }
    const canonicalFile = process.env.SHOT_LAYERING_CANONICAL_FIXTURE;
    if (canonicalFile) {
      expect(bytes.equals(readFileSync(canonicalFile))).toBe(true);
    }
  });

  it('retains parent-lane gap admission and authored pauses between separate groups', () => {
    const testCase = layeringFixture.cases.find((entry) => entry.id === 'two-shots-one-row')!;
    const report = (app?: ResolvedTimelineConfig['app']) => projectCase(testCase, app).config.app?.visualSeamContract as {
      report: { structuralIssues: string[]; blocked: boolean };
    };
    expect(report().report.structuralIssues).toHaveLength(1);
    expect(report().report.blocked).toBe(true);
    const gaps = [{ kind: 'pause', track: 'picture', startFrame: 60, endFrame: 75 }];
    expect(report({ visualSeamContract: { gaps } }).report.structuralIssues).toEqual([]);
    expect(report({ visualSeamContract: { gaps: [{ ...gaps[0], endFrame: 76 }] } }).report.blocked).toBe(true);
  });

  it.each(layeringFixture.cases)('$id', (testCase) => {
    const before = JSON.stringify(testCase);
    const projection = projectCase(testCase);
    const { config } = projection;
    expect(config.tracks.map((track) => track.id)).toEqual(testCase.expected.track_order);
    expect(config.tracks.filter((track) => track.app?.group).map(({ id, app }) => ({ id, app })))
      .toEqual(testCase.expected.group_tracks);
    expect(projection.warnings).toEqual(testCase.expected.warnings);
    expect(config.app?.canonicalComposition).toMatchObject({ warnings: testCase.expected.warnings });
    for (const [id, track] of Object.entries(testCase.expected.clip_tracks)) {
      const clip = config.clips.find((entry) => entry.id === id || projection.clipIdentities.get(entry.id)?.rawClipId === id);
      expect(clip?.track, id).toBe(track);
    }
    for (const occurrence of testCase.input.occurrences) {
      const shot = testCase.input.shot_revisions.find((revision) => revision.shot_id === occurrence.shot_id && revision.revision_id === occurrence.revision_id)!;
      const timeline = shot.internal_timeline_revision.timeline;
      const group = config.tracks.filter((track) => (track.app?.group as { id: string } | undefined)?.id === occurrence.occurrence_id);
      const indices = group.map((track) => config.tracks.indexOf(track));
      expect(indices).toEqual(indices.map((_, index) => indices[0] + index));
      for (const rawClip of timeline.clips) {
        const clip = config.clips.find((entry) => entry.id === `${occurrence.occurrence_id}:${rawClip.id}`)!;
        expect(clip).toMatchObject({ at: (occurrence.at_ms + rawClip.at_ms) / 1000, hold: rawClip.duration_ms / 1000 });
        if (rawClip.track === 'audio') {
          expect(clip.track).toBe('audio');
          expect(clip.volume).toBeUndefined();
          expect(clip.speed).toBeUndefined();
          expect(config.tracks.filter((track) => track.id === 'audio')).toHaveLength(1);
          expect(config.tracks.find((track) => track.id === 'audio')?.app?.group).toBeUndefined();
        }
      }
    }
    if ('transparent_windows_ms' in testCase.expected) {
      for (const [start, end] of testCase.expected.transparent_windows_ms) {
        const groupIds = new Set(testCase.expected.group_tracks.map((track) => track.id));
        const visuals = config.clips.filter((clip) => groupIds.has(clip.track));
        expect(visuals.some((clip) => clip.at * 1000 < end && (clip.at + (clip.hold ?? 0)) * 1000 > start)).toBe(false);
      }
    }
    expect(JSON.stringify(testCase)).toBe(before);
  });
});

const placementMessage = 'Shot opacity and transforms are not supported yet. Remove them from the shot placement to render this timeline.';

describe('shot placement compositing admission', () => {
  it.each([{ transform: { opacity: 0.5 } }, { transform: { x: 0 } }, { transform: { scale: 1 } }, { opacity: 0 }, { opacity: 1 }])('refuses non-empty %j', (placement) => {
    const graph = structuredClone(compositionFixture);
    Object.assign(graph.occurrences[0], placement);
    const composition = createShotCompositionAdapter({ load: async () => graph }).prepare(graph);
    expect(() => projectCanonicalComposition(composition)).toThrow(placementMessage);
    try { projectCanonicalComposition(composition); } catch (error) {
      expect(error).toBeInstanceOf(CanonicalCompositionProjectionError);
      expect(error).toMatchObject({ code: 'unsupported_placement', occurrenceId: 'occ-1' });
    }
  });

  it.each([{}, { transform: {} }, { transform: null, opacity: null }, { transform: '', opacity: '' }, { transform: [], opacity: {} }])('accepts empty %j and keeps child opacity', (placement) => {
    const graph = structuredClone(compositionFixture);
    Object.assign(graph.occurrences[0], placement);
    const composition = createShotCompositionAdapter({ load: async () => graph }).prepare(graph);
    const first = composition.occurrences[0];
    const timeline = first.revision.internal_timeline_revision as { timeline: { tracks: unknown[] } };
    const local = {
      ...composition,
      occurrences: [{ ...first, revision: { ...first.revision, internal_timeline_revision: {
        timeline: { ...timeline.timeline, clips: [{ id: 'child', clipType: 'media', track: 'video', at: 0, hold: 1, opacity: 0.4, width: 100 }] },
      } } }],
    };
    const child = projectCanonicalComposition(local).config.clips[0] as TimelineClip;
    expect(child).toMatchObject({ opacity: 0.4, width: 100, track: 'occ-1~video' });
  });
});
