import { describe, expect, it, vi } from 'vitest';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { normalizeTranscriptSource, TRANSCRIPT_SCHEMA_REF } from './adaptTranscript.ts';
import {
  createTranscriptImportCallback,
  TranscriptImportError,
  type TranscriptImportInput,
} from './importTranscriptHandoff.ts';
import { parseTimelineBundle } from './timelineBundle.ts';

const OTHER_SCHEMA = 'example.caption/v1';

function buildConfig(): TimelineConfig {
  return {
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'A1', kind: 'audio', label: 'A1', muted: false }],
    clips: [],
  };
}

async function buildData(sourceItemsBySchemaRef?: TimelineData['sourceItemsBySchemaRef']): Promise<TimelineData> {
  return buildTimelineData(
    buildConfig(),
    {
      assets: {
        'audio-a': { file: 'audio-a.wav', type: 'audio/wav', duration: 12 },
        'video-b': { file: 'video-b.mp4', type: 'video/mp4', duration: 30 },
        'image-c': { file: 'image-c.png', type: 'image/png' },
      },
    },
    (file) => file,
    3,
    sourceItemsBySchemaRef,
  );
}

const documentFor = (overrides: Record<string, unknown> = {}) => ({
  assetId: 'audio-a',
  sourceId: 'capture-1',
  segments: [{
    id: 'segment-1',
    start: 0.4,
    end: 2.8,
    text: 'Hello there.',
    speaker: 'speaker-a',
    words: [
      { id: 'word-1', start: 0.4, end: 0.9, text: 'Hello' },
      { id: 'word-2', start: 1.1, end: 2.8, text: 'there.' },
    ],
  }],
  ...overrides,
});

function setup(data: TimelineData) {
  const dataRef: { current: TimelineData | null } = { current: data };
  const commitData = vi.fn();
  const importTranscript = createTranscriptImportCallback({ dataRef, commitData });
  return { dataRef, commitData, importTranscript };
}

describe('createTranscriptImportCallback', () => {
  it('imports a rich handoff through the canonical commit path and round-trips the source bundle', async () => {
    const { commitData, importTranscript } = setup(await buildData());

    const receipt = importTranscript({ document: JSON.stringify(documentFor()) });
    const [nextData, options] = commitData.mock.calls[0] as [TimelineData, unknown];
    const [item] = nextData.sourceItemsBySchemaRef?.[TRANSCRIPT_SCHEMA_REF] ?? [];

    expect(receipt).toEqual({
      assetId: 'audio-a',
      sourceId: 'capture-1',
      importedSegments: 1,
      replacedSegments: 0,
      replacedExistingSource: false,
    });
    expect(item).toMatchObject({
      id: 'transcript-source:audio-a:source:capture-1:segment:segment-1',
      schemaRef: TRANSCRIPT_SCHEMA_REF,
      extent: { start: 0.4, end: 2.8 },
      payload: {
        sourceId: 'capture-1',
        segmentId: 'transcript-source:audio-a:source:capture-1:segment:segment-1',
        text: 'Hello there.',
        speaker: 'speaker-a',
        words: [
          { id: 'transcript-source:audio-a:source:capture-1:segment:segment-1:word:word-1', start: 0.4, end: 0.9, text: 'Hello' },
          { id: 'transcript-source:audio-a:source:capture-1:segment:segment-1:word:word-2', start: 1.1, end: 2.8, text: 'there.' },
        ],
      },
      sourceArtifactRef: { assetId: 'audio-a' },
    });
    expect(options).toEqual({ save: true, semantic: true });
    expect(commitData).toHaveBeenCalledTimes(1);

    // This is the exact envelope shape T1b saves and reloads from TimelineBundle.
    const persisted = JSON.parse(JSON.stringify({
      schema_version: 1,
      itemsBySchemaRef: nextData.sourceItemsBySchemaRef,
    })) as unknown;
    expect(parseTimelineBundle(persisted).itemsBySchemaRef[TRANSCRIPT_SCHEMA_REF]).toEqual([item]);
  });

  it('replaces only the same asset and logical source while preserving other sources and schemas', async () => {
    const sameSource = normalizeTranscriptSource({
      assetId: 'audio-a', sourceId: 'capture-1',
      segments: [{ id: 'old-segment', start: 0, end: 1, text: 'old version' }],
    });
    const otherSourceOnSameAsset = normalizeTranscriptSource({
      assetId: 'audio-a', sourceId: 'capture-2',
      segments: [{ id: 'other-segment', start: 1, end: 2, text: 'keep take two' }],
    });
    const sameSourceOnOtherAsset = normalizeTranscriptSource({
      assetId: 'video-b', sourceId: 'capture-1',
      segments: [{ id: 'video-segment', start: 2, end: 3, text: 'keep video source' }],
    });
    const otherSchemaItem = {
      id: 'caption-1',
      shape: 'interval' as const,
      domain: 'source_seconds' as const,
      extent: { start: 0, end: 1 },
      schemaRef: OTHER_SCHEMA,
      payload: { text: 'keep unrelated schema' },
      sourceArtifactRef: { assetId: 'audio-a' },
      provenance: { adapterId: 'test', adapterVersion: '1' },
    };
    const { commitData, importTranscript } = setup(await buildData({
      [TRANSCRIPT_SCHEMA_REF]: [...sameSource, ...otherSourceOnSameAsset, ...sameSourceOnOtherAsset],
      [OTHER_SCHEMA]: [otherSchemaItem],
    }));

    const receipt = importTranscript({ document: documentFor() });
    const [nextData] = commitData.mock.calls[0] as [TimelineData];
    const transcriptItems = nextData.sourceItemsBySchemaRef?.[TRANSCRIPT_SCHEMA_REF] ?? [];

    expect(receipt).toMatchObject({ replacedSegments: 1, replacedExistingSource: true });
    expect(transcriptItems.map((item) => item.id)).toEqual([
      otherSourceOnSameAsset[0].id,
      sameSourceOnOtherAsset[0].id,
      'transcript-source:audio-a:source:capture-1:segment:segment-1',
    ]);
    expect(nextData.sourceItemsBySchemaRef?.[OTHER_SCHEMA]).toEqual([otherSchemaItem]);
  });

  it('requires an explicit legacy-file association and rejects mismatched or non-media assets', async () => {
    const { commitData, importTranscript } = setup(await buildData());

    const noAssociation = { document: { segments: documentFor().segments } };
    expect(() => importTranscript(noAssociation)).toThrowError(TranscriptImportError);
    expect(() => importTranscript(noAssociation)).toThrow(/Select the source media in the editor/);
    expect(() => importTranscript({
      document: { segments: documentFor().segments }, associationAssetId: ' ',
    })).toThrow(/selected media association is empty/);
    expect(() => importTranscript({
      document: documentFor(), associationAssetId: 'video-b',
    })).toThrow(/names media asset “audio-a”/);
    expect(() => importTranscript({
      document: documentFor({ assetId: 'missing' }),
    })).toThrow(/not registered in this timeline/);
    expect(() => importTranscript({
      document: documentFor({ assetId: 'image-c' }),
    })).toThrow(/not registered as audio or video/);
    expect(commitData).not.toHaveBeenCalled();
  });

  it.each([
    ['invalid JSON', { document: '{oops' }, 'invalid_json'],
    ['missing segments', { document: { assetId: 'audio-a' } }, 'invalid_document'],
    ['invalid segment range', { document: documentFor({ segments: [{ start: 2, end: 1, text: 'bad' }] }) }, 'invalid_content'],
    ['conflicting word text', {
      document: documentFor({ segments: [{
        start: 0, end: 1, text: 'hello',
        words: [{ start: 0, end: 1, text: 'hello', word: 'different' }],
      }] }),
    }, 'invalid_content'],
    ['empty transcript', { document: documentFor({ segments: [] }) }, 'empty_transcript'],
  ])('reports actionable validation for %s without committing', async (_label, input, code) => {
    const { commitData, importTranscript } = setup(await buildData());
    let error: unknown;
    try {
      importTranscript(input as TranscriptImportInput);
    } catch (caught) {
      error = caught;
    }
    expect(error).toBeInstanceOf(TranscriptImportError);
    expect(error).toMatchObject({ code });
    expect(commitData).not.toHaveBeenCalled();
  });

  it('uses an explicitly associated registered media asset for legacy exports', async () => {
    const { commitData, importTranscript } = setup(await buildData());
    const receipt = importTranscript({
      document: { segments: documentFor().segments },
      associationAssetId: 'audio-a',
    });
    expect(receipt).toMatchObject({ assetId: 'audio-a', sourceId: 'transcript:audio-a' });
    expect(commitData).toHaveBeenCalledTimes(1);
  });
});
