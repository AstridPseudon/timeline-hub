import { describe, expect, it, vi } from 'vitest';
import { normalizeTranscriptSource, TRANSCRIPT_SCHEMA_REF } from '@/tools/video-editor/data/typed/adaptTranscript.ts';
import { assembleDataLanes } from '@/tools/video-editor/data/typed/assembleDataLanes.ts';
import type { TranscriptTextEdit } from '@/tools/video-editor/data/typed/editTranscript.ts';
import { assembleTimelineData, type TimelineData } from './timeline-data.ts';
import { commitTranscriptTextEdit } from './transcript-text-edit.ts';
import { buildDataFromCurrentRegistry } from './timeline-save-utils.ts';

const makeData = (text = 'Hello, world!'): TimelineData => {
  const entry = { file: 'media.mp4', type: 'video/mp4', duration: 10 };
  const config: TimelineData['config'] = {
    output: { resolution: '1920x1080', fps: 30, file: 'output.mp4' },
    tracks: [{ id: 'v1', kind: 'visual', label: 'Video', scale: 1, fit: 'manual', opacity: 1, blendMode: 'normal', app: { scaleAppliesToPositionedClips: true } }],
    clips: [
      { id: 'c1', at: 0, track: 'v1', asset: 'media', from: 0, to: 5, speed: 1 },
      { id: 'c2', at: 10, track: 'v1', asset: 'media', from: 0, to: 5, speed: 1 },
    ],
  };
  const assembled = assembleTimelineData({
    config, configVersion: 7,
    head: { projectId: 'p1', timelineId: 't1', headRevisionId: 'head-original' },
    registry: { assets: { media: entry } },
    resolvedConfig: { ...config, tracks: config.tracks!, clips: config.clips.map((clip) => ({ ...clip, assetEntry: { ...entry, src: 'media.mp4' } })), registry: { media: { ...entry, src: 'media.mp4' } } },
    output: config.output, assetMap: { media: 'media.mp4' },
    sourceItemsBySchemaRef: { [TRANSCRIPT_SCHEMA_REF]: normalizeTranscriptSource({
      assetId: 'media', sourceId: 'transcript', segments: [{
        id: 's1', start: 1, end: 3, text, speaker: 'Nova',
        words: [{ id: 'w1', start: 1, end: 2, text: 'Hello' }, { id: 'w2', start: 2, end: 3, text: 'world' }],
      }],
    }) },
  });
  return buildDataFromCurrentRegistry(assembled.config, assembled);
};
const wordEdit = (data: TimelineData): TranscriptTextEdit => {
  const item = data.sourceItemsBySchemaRef![TRANSCRIPT_SCHEMA_REF][0];
  return { type: 'word', sourceItemId: item.id, wordId: (item.payload as { words: { id: string }[] }).words[1].id, text: 'Earth' };
};

describe('commitTranscriptTextEdit', () => {
  it('commits exactly once through the existing semantic history/save path, retaining CAS head and all clip geometry', () => {
    const current = makeData();
    const dataRef = { current };
    const commitData = vi.fn((next: TimelineData) => { dataRef.current = next; });
    const result = commitTranscriptTextEdit({ dataRef, commitData }, wordEdit(current));
    expect(result).toMatchObject({ ok: true, changed: true });
    expect(commitData).toHaveBeenCalledExactlyOnceWith(dataRef.current, { semantic: true });
    expect(dataRef.current.head).toEqual(current.head);
    expect(dataRef.current.configVersion).toBe(7);
    expect(dataRef.current.config).toEqual(current.config);
    expect(dataRef.current.rows).toEqual(current.rows);
    expect(dataRef.current.stableSignature).not.toBe(current.stableSignature);
    expect(dataRef.current.sourceItemsBySchemaRef![TRANSCRIPT_SCHEMA_REF][0].id).toBe(current.sourceItemsBySchemaRef![TRANSCRIPT_SCHEMA_REF][0].id);

    // Both clip views use the corrected canonical source, never independent copies.
    const lanes = assembleDataLanes({
      kinds: [{ kindId: 'transcript', schemaRef: TRANSCRIPT_SCHEMA_REF, shape: 'interval', domain: 'source_seconds', label: 'Transcript', laneRenderer: () => null }],
      clips: dataRef.current.resolvedConfig.clips,
      segmentsByAsset: {},
      sourceItemsBySchemaRef: dataRef.current.sourceItemsBySchemaRef,
    });
    expect(lanes[0].items).toHaveLength(2);
    expect(lanes[0].items.map((view) => (view.item.payload as { text: string }).text)).toEqual(['Hello, Earth!', 'Hello, Earth!']);
    expect(lanes[0].items.map((view) => [view.timelineStart, view.timelineEnd])).toEqual([[1, 3], [11, 13]]);
    expect(lanes[0].items[0].item.sourceItemId).toBe(lanes[0].items[1].item.sourceItemId);
  });

  it('reads current data at submission and leaves ambiguous edits out of history/save entirely', () => {
    const stale = makeData();
    const current = makeData('world world');
    const before = JSON.stringify(current);
    const commitData = vi.fn();
    const dataRef = { current };
    expect(commitTranscriptTextEdit({ dataRef, commitData }, wordEdit(stale)))
      .toMatchObject({ ok: false, code: 'segment_replacement_required' });
    expect(commitData).not.toHaveBeenCalled();
    expect(dataRef.current).toBe(current);
    expect(JSON.stringify(current)).toBe(before);
  });

  it('commits segment text and alignment removal as a single semantic step', () => {
    const current = makeData();
    const commitData = vi.fn();
    const result = commitTranscriptTextEdit({ dataRef: { current }, commitData }, {
      type: 'segment', sourceItemId: current.sourceItemsBySchemaRef![TRANSCRIPT_SCHEMA_REF][0].id, text: 'Corrected sentence.',
    });
    expect(result).toMatchObject({ ok: true, changed: true });
    expect(commitData).toHaveBeenCalledTimes(1);
    const next = commitData.mock.calls[0][0] as TimelineData;
    expect(next.sourceItemsBySchemaRef![TRANSCRIPT_SCHEMA_REF][0].payload).toMatchObject({ text: 'Corrected sentence.', speaker: 'Nova' });
    expect(next.sourceItemsBySchemaRef![TRANSCRIPT_SCHEMA_REF][0].payload).not.toHaveProperty('words');
    expect(next.config).toEqual(current.config);
  });

  it('does not commit a no-op, an empty replacement, an unavailable timeline, or a host read-only state', () => {
    const current = makeData();
    const commitData = vi.fn();
    expect(commitTranscriptTextEdit({ dataRef: { current }, commitData }, { ...wordEdit(current), text: 'world' })).toMatchObject({ ok: true, changed: false });
    expect(commitTranscriptTextEdit({ dataRef: { current }, commitData }, { ...wordEdit(current), text: ' ' })).toMatchObject({ ok: false, code: 'invalid_input' });
    expect(commitTranscriptTextEdit({ dataRef: { current: null }, commitData }, wordEdit(current))).toMatchObject({ ok: false, code: 'timeline_unavailable' });
    expect(commitTranscriptTextEdit({ dataRef: { current }, commitData, editability: { check: () => ({ allowed: true }), checkTimeline: () => ({ allowed: false, reason: 'canonical_shot_draft_active' }) } }, wordEdit(current)))
      .toMatchObject({ ok: false, code: 'timeline_read_only' });
    expect(commitData).not.toHaveBeenCalled();
  });
});
