import { describe, expect, it, vi } from 'vitest';
import { setupTranscriptHost } from './transcript-panel-binding.fixture.ts';

const document = { sourceId: 'doc', segments: [{ id: 's', start: 0, end: 4, text: 'Hello world', words: [{ id: 'w', text: 'Hello', start: 0, end: 1 }] }] };

describe('app transcript panel host binding', () => {
  it('offers only registered audio/video assets actually used by timeline clips', async () => {
    const { video } = await setupTranscriptHost();
    expect(video.transcript!.getMediaChoices()).toEqual([
      { assetId: 'media', label: 'Interview.mp4', kind: 'video' },
      { assetId: 'audio', label: 'Audio.wav', kind: 'audio' },
    ]);
  });
  it('imports with explicit association, commits text edits and atomically invalidates every repeated word projection', async () => {
    const { video, commitData } = await setupTranscriptHost();
    const transcript = video.transcript!;
    const notify = vi.fn(); const subscription = transcript.subscribe(notify);
    expect(() => transcript.importTranscript!({ document })).toThrow(/assetId/);
    expect(commitData).not.toHaveBeenCalled();
    const receipt = transcript.importTranscript!({ document, associationAssetId: 'media' });
    expect(receipt).toMatchObject({ assetId: 'media', sourceId: 'doc', importedSegments: 1 });
    expect(commitData).toHaveBeenCalledWith(expect.anything(), { save: true, semantic: true });
    expect(notify).toHaveBeenCalledTimes(1);
    const row = transcript.getSnapshot().sources[0];
    const result = transcript.editText!({ type: 'word', sourceItemId: row.sourceItemId, wordId: row.words![0].id, text: 'Hi' });
    expect(result).toEqual({ ok: true, changed: true });
    expect(result).not.toHaveProperty('sourceItemsBySchemaRef');
    expect(transcript.getSnapshot().sources[0].text).toBe('Hi world');
    expect(transcript.getSnapshot().occurrences.map((item) => item.words[0].text)).toEqual(['Hi', 'Hi']);
    const oldWord = row.words![0].id;
    transcript.editText!({ type: 'segment', sourceItemId: row.sourceItemId, text: 'New segment' });
    expect(transcript.getSnapshot().sources[0].words).toBeUndefined();
    expect(transcript.getSnapshot().occurrences.every((item) => item.words.length === 0)).toBe(true);
    expect(transcript.seek({ occurrenceId: transcript.getSnapshot().occurrences[0].id, wordId: oldWord })).toMatchObject({ ok: false, reason: 'word_not_found' });
    expect(commitData).toHaveBeenLastCalledWith(expect.anything(), { semantic: true });
    subscription.dispose(); subscription.dispose();
    transcript.importTranscript!({ document, associationAssetId: 'media' });
    expect(notify).toHaveBeenCalledTimes(3);
  });
  it('imports and corrects equal logical source/segment/word IDs on two media assets independently', async () => {
    const { video } = await setupTranscriptHost();
    const transcript = video.transcript!;
    transcript.importTranscript!({ document, associationAssetId: 'media' });
    transcript.importTranscript!({ document, associationAssetId: 'audio' });
    const rows = transcript.getSnapshot().sources;
    expect(rows).toHaveLength(2);
    expect(new Set(rows.map((row) => row.sourceItemId)).size).toBe(2);
    const audio = rows.find((row) => row.assetId === 'audio')!;
    const selection = transcript.selectSource({ assetId: 'media', sourceId: 'doc', occurrenceId: transcript.getSnapshot().occurrences.find((item) => item.assetId === 'media')!.id }, { assetId: 'audio', sourceId: 'doc' });
    expect(selection).toEqual({ assetId: 'audio', sourceId: 'doc', occurrenceId: null });
    expect(transcript.getPlayback(selection).focused?.assetId).toBe('audio');
    expect(transcript.editText!({ type: 'word', sourceItemId: audio.sourceItemId, wordId: audio.words![0].id, text: 'Audio' })).toEqual({ ok: true, changed: true });
    expect(transcript.getSnapshot().sources.find((row) => row.assetId === 'audio')!.text).toBe('Audio world');
    expect(transcript.getSnapshot().sources.find((row) => row.assetId === 'media')!.text).toBe('Hello world');
  });
  it('reports host loading and importer parse/empty/association errors without a commit', async () => {
    const { video, commitData, dataRef, store } = await setupTranscriptHost();
    const transcript = video.transcript!;
    expect(() => transcript.importTranscript!({ document: 'bad' })).toThrow(/JSON/);
    expect(() => transcript.importTranscript!({ document: { assetId: 'media', segments: [] } })).toThrow(/empty|segment/i);
    expect(() => transcript.importTranscript!({ document: { ...document, assetId: 'media' }, associationAssetId: 'audio' })).toThrow(/match|different/i);
    expect(commitData).not.toHaveBeenCalled();
    dataRef.current = null;
    expect(transcript.editText!({ type: 'segment', sourceItemId: 's', text: 'Wait' })).toMatchObject({ ok: false, code: 'timeline_unavailable' });
    expect(() => transcript.importTranscript!({ document })).toThrow(/load/i);
    store.getState().syncOpsSlice({ ...store.getState().ops, transcriptHost: undefined });
    expect(() => transcript.importTranscript!({ document })).toThrow(/loading/i);
  });
  it('rechecks host editability and latest source state without committing rejected edits/imports', async () => {
    const { video, commitData, lock, dataRef } = await setupTranscriptHost();
    video.transcript!.importTranscript!({ document, associationAssetId: 'media' });
    const row = video.transcript!.getSnapshot().sources[0];
    commitData.mockClear(); lock();
    expect(video.transcript!.editText!({ type: 'segment', sourceItemId: row.sourceItemId, text: 'Denied' })).toMatchObject({ ok: false, code: 'timeline_read_only' });
    expect(() => video.transcript!.importTranscript!({ document, associationAssetId: 'media' })).toThrow(/read-only/);
    expect(commitData).not.toHaveBeenCalled();
    dataRef.current = null;
    expect(video.transcript!.getSnapshot().sources).toEqual([]);
    expect(video.transcript!.getMediaChoices()).toEqual([]);
  });
});
