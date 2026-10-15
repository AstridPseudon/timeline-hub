// @vitest-environment jsdom
import { createElement } from 'react';
import { act, cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { ExtensionContext, PanelVideoAdapter, TranscriptMediaChoice, TranscriptPanelAdapter, TranscriptPanelSnapshot } from '@reigh/editor-sdk';
import { alignedTextParts, TranscriptPanel } from '../../../astrid/packs/rendering/ui/transcript/TranscriptPanel';
afterEach(cleanup);
function setup() {
  let mediaChoices: TranscriptMediaChoice[] = [{ assetId: 'asset', label: 'Interview.mp4', kind: 'video' }];
  let snapshot: TranscriptPanelSnapshot = { sources: [{ sourceItemId: 's', sourceId: 'default', assetId: 'asset', documentId: 'document', documentVersion: 4, start: 0, end: 4, speaker: 'Alex', text: 'Hello, world!  Hello.', words: [{ id: 'w', text: 'Hello', start: 0, end: 1 }, { id: 'w2', text: 'world', start: 1, end: 2 }, { id: 'w3', text: 'Hello', start: 2, end: 3 }] }], occurrences: [{ id: 'o', sourceItemId: 's', sourceId: 'default', assetId: 'asset', clipId: 'clip', timelineStart: 0, timelineEnd: 4, words: [] }, { id: 'repeat', sourceItemId: 's', sourceId: 'default', assetId: 'asset', clipId: 'clip-repeat', timelineStart: 8, timelineEnd: 12, words: [] }] };
  const documents = new Set<() => void>(), playback = new Set<() => void>();
  const subscribe = (set: Set<() => void>) => (listener: () => void) => { set.add(listener); return { dispose: () => { set.delete(listener); } }; };
  let active = true;
  let lane = true;
  const seek = vi.fn<TranscriptPanelAdapter['seek']>(() => ({ ok: true, seconds: 0, timing: 'word' }));
  const editText = vi.fn<NonNullable<TranscriptPanelAdapter['editText']>>(async () => ({ ok: true, changed: true }));
  const importTranscript = vi.fn<NonNullable<TranscriptPanelAdapter['importTranscript']>>(async () => ({ assetId: 'asset', sourceId: 'default', importedSegments: 1, replacedSegments: 0, replacedExistingSource: false, documentId: 'document', version: 4, associationSaved: true }));
  const stageTextDraft = vi.fn<NonNullable<TranscriptPanelAdapter['stageTextDraft']>>(() => ({ ok: true, changed: true }));
  const resolveSourceConflict = vi.fn<NonNullable<TranscriptPanelAdapter['resolveSourceConflict']>>(async () => ({ ok: true, changed: true }));
  const adapter: TranscriptPanelAdapter = {
    getSnapshot: () => snapshot, subscribe: subscribe(documents), getMediaChoices: () => mediaChoices,
    getPlayback: () => ({ playing: active ? snapshot.occurrences : [], focused: active ? snapshot.occurrences[0] : null, sourceId: 'default', assetId: 'asset', playingWordIds: active ? ['w'] : [] }),
    getProjectState: () => ({ supported: true, sources: [{ assetId: 'asset', documentId: 'document', sourceId: 'default', version: 4, status: 'clean', hasDraft: false, canUndo: true, canRedo: false }] }),
    listProjectSources: vi.fn(async (_assetId: string) => [{ documentId: 'other-document', sourceId: 'Alt take', version: 1 }]),
    selectProjectSource: vi.fn(async () => ({ assetId: 'asset', sourceId: 'Alt take', importedSegments: 1, replacedSegments: 0, replacedExistingSource: false, associationSaved: true })),
    getTimelineLaneVisible: () => lane, setTimelineLaneVisible: vi.fn((value) => { lane = value; }),
    selectSource: (_selection, source) => ({ ...source, occurrenceId: null }), seek, editText, importTranscript, stageTextDraft, resolveSourceConflict,
  };
  const video = { transcript: adapter, view: { subscribe: subscribe(playback) } } as unknown as PanelVideoAdapter;
  const onOpenChange = vi.fn();
  const panel = (visible = true, settingsOpen = false) => createElement(TranscriptPanel, { context: {} as ExtensionContext, instanceId: 'editor:transcript', visible, video, settings: { open: settingsOpen, onOpenChange } });
  const view = render(panel());
  return { ...view, adapter, panel, documents, playback, seek, editText, stageTextDraft, importTranscript, resolveSourceConflict, onOpenChange,
    setMediaChoices: (next: TranscriptMediaChoice[]) => { mediaChoices = next; },
    publish: (next: TranscriptPanelSnapshot) => act(() => { snapshot = next; documents.forEach((listener) => listener()); }),
    stop: () => act(() => { active = false; playback.forEach((listener) => listener()); }), getSnapshot: () => snapshot };
}
const inspect = (view: ReturnType<typeof setup>) => { fireEvent.focus(view.getByRole('group', { name: 'Transcript text' })); };

describe('continuous transcript panel', () => {
  it('separates flowing text in one inset scrolling reading surface below controls', () => {
    const view = setup();
    const area = view.getByTestId('transcript-reading-area');
    const text = view.getByRole('group', { name: 'Transcript text' });
    expect(area).toContainElement(text);
    expect(area).toHaveClass('mx-3', 'mb-3', 'min-h-0', 'flex-1', 'overflow-y-auto', 'overscroll-contain', 'rounded-lg', 'border', 'border-border', 'bg-background', 'px-4', 'py-4');
    expect(text.textContent).toBe('Hello, world!  Hello.');
    expect(area).not.toContainElement(view.getByRole('combobox', { name: 'Transcript source' }));
    expect(area).not.toContainElement(view.getByRole('button', { name: 'Following playhead' }));
    expect(area).not.toContainElement(view.getByRole('button', { name: 'Transcript settings' }));
    expect(area).not.toContainElement(view.getByText('Project transcript · Saved'));
    area.scrollTop = 88; fireEvent.scroll(area);
    view.rerender(view.panel(true, true));
    expect(view.getByTestId('transcript-reading-area')).toBe(area);
    expect(area.scrollTop).toBe(88);
    const settings = view.getByRole('dialog', { name: 'Transcript settings' });
    expect(area).not.toContainElement(settings);
    expect(settings.parentElement).toBe(area.parentElement);
    expect(settings).toHaveClass('absolute', 'z-30');
  });

  it('renders canonical punctuation, repeated words and spacing exactly once with segment fallback for uncertain alignment', () => {
    const view = setup();
    expect(view.getByRole('group', { name: 'Transcript text' }).textContent).toBe('Hello, world!  Hello.');
    expect(view.queryByLabelText('Aligned words')).toBeNull();
    expect(view.getByLabelText('Transcript source').textContent).toContain('Interview.mp4');
    const source = view.getSnapshot().sources[0];
    expect(alignedTextParts({ ...source, words: [{ ...source.words![0], text: 'missing' }] })).toEqual([{ text: source.text }]);
    expect(alignedTextParts({ ...source, words: [source.words![0]] })).toEqual([{ text: source.text }]);
  });
  it('reserves a padded chevron area while keeping a long source label focusable and truncated', () => {
    const view = setup();
    const longSourceId = 'Interview transcript with a deliberately long source label';
    const source = view.getSnapshot().sources[0];
    view.publish({ ...view.getSnapshot(), sources: [...view.getSnapshot().sources, {
      ...source, sourceItemId: 'long-source-item', sourceId: longSourceId, text: 'Long source text.', words: undefined,
    }] });

    const selector = view.getByRole('combobox', { name: 'Transcript source' });
    fireEvent.change(selector, { target: { value: `local:${JSON.stringify(['asset', longSourceId])}` } });
    act(() => selector.focus());

    expect(selector).toHaveFocus();
    expect(selector).toHaveClass('appearance-none', 'truncate', 'pl-2', 'pr-8', 'focus-visible:ring-2');
    expect(selector.selectedOptions[0].textContent).toContain(longSourceId);
    expect(selector.parentElement).toHaveClass('relative', 'min-w-0', 'flex-1');
    const chevron = view.getByTestId('transcript-source-chevron');
    expect(chevron).toHaveAttribute('aria-hidden', 'true');
    expect(chevron).toHaveClass('pointer-events-none', 'absolute', 'right-2', 'h-4', 'w-4');
    expect(view.getByRole('button', { name: 'Following playhead' })).toHaveClass('shrink-0');
  });
  it('offers one roving region, contextual detail/seek/edit and occurrence choice without word tab stops', () => {
    const view = setup(); const region = view.getByRole('group', { name: 'Transcript text' });
    expect([...region.querySelectorAll('[tabindex]')].every((node) => node.getAttribute('tabindex') === '-1')).toBe(true);
    expect(view.queryByText(/0.00–1.00/)).toBeNull();
    fireEvent.focus(region); fireEvent.keyDown(region, { key: 'ArrowRight' }); fireEvent.keyDown(region, { key: 'Enter' });
    expect(view.seek).toHaveBeenCalledWith({ occurrenceId: 'o', wordId: 'w2' });
    expect(view.getByText(/1.00–2.00s · Alex/)).toBeTruthy();
    fireEvent.change(view.getByLabelText('Clip occurrence'), { target: { value: 'repeat' } });
    fireEvent.click(view.getByRole('button', { name: 'Seek word' }));
    expect(view.seek).toHaveBeenLastCalledWith({ occurrenceId: 'repeat', wordId: 'w2' });
    fireEvent.click(view.getByRole('button', { name: 'Edit word' }));
    expect(view.getByRole('textbox', { name: 'Replacement word' })).toHaveValue('world');
  });
  it('awaits a save, stages the full displayed identity/base and retains failed text', async () => {
    const view = setup(); let finish!: (value: {ok:true;changed:boolean}) => void;
    view.editText.mockImplementationOnce(() => new Promise((resolve) => { finish = resolve; }));
    inspect(view); fireEvent.click(view.getByRole('button', { name: 'Edit word' }));
    fireEvent.change(view.getByRole('textbox'), { target: { value: 'Hi' } });
    expect(view.stageTextDraft).toHaveBeenCalledWith(expect.objectContaining({ assetId: 'asset', documentId: 'document', baseVersion: 4, text: 'Hi', wordId: 'w' }));
    fireEvent.click(view.getByRole('button', { name: 'Save correction' }));
    expect(view.getByText('Project transcript · Saving…')).toBeTruthy();
    expect(view.getByRole('textbox')).toHaveValue('Hi');
    await act(async () => finish({ok:true,changed:true}));
    expect(view.queryByRole('textbox')).toBeNull();
    inspect(view); fireEvent.click(view.getByRole('button', { name: 'Edit word' }));
    fireEvent.change(view.getByRole('textbox'), { target: { value: 'Unsent' } });
    view.editText.mockResolvedValueOnce({ ok: false, code: 'conflict', message: 'Newer document; draft retained.' });
    fireEvent.click(view.getByRole('button', { name: 'Save correction' }));
    await waitFor(() => expect(view.getByRole('alert')).toHaveTextContent('draft retained'));
    expect(view.getByRole('textbox')).toHaveValue('Unsent');
  });
  it('retains draft/source/scroll and live observation through settings and visibility', async () => {
    const view = setup(); inspect(view); fireEvent.click(view.getByRole('button', { name: 'Edit word' }));
    fireEvent.change(view.getByRole('textbox'), { target: { value: 'Draft' } });
    const scroller = view.getByRole('group', { name: 'Transcript text' }).parentElement!.parentElement!;
    scroller.scrollTop = 88; fireEvent.scroll(scroller);
    expect(view.getByRole('button', { name: 'Resume follow' })).toBeTruthy();
    view.rerender(view.panel(true, true)); expect(view.documents.size).toBe(1); expect(view.playback.size).toBe(1);
    expect(view.getByRole('dialog', { name: 'Transcript settings' })).toBeTruthy();
    expect(view.getByRole('group', { name: 'Transcript text' })).toBeVisible();
    expect(view.getByLabelText('Show transcript lane')).toBeChecked();
    fireEvent.click(view.getByLabelText('Show transcript lane'));
    expect(view.adapter.setTimelineLaneVisible).toHaveBeenCalledWith(false);
    view.rerender(view.panel(false, true)); expect(view.getByTestId('astrid-transcript-panel')).not.toBeVisible();
    view.rerender(view.panel()); expect(view.getByRole('textbox')).toHaveValue('Draft'); expect(scroller.scrollTop).toBe(88);
    expect(view.documents.size).toBe(1); expect(view.playback.size).toBe(1);
    view.unmount(); expect(view.documents.size).toBe(0); expect(view.playback.size).toBe(0);
  });
  it('clears subtle playback highlight in a gap without losing prose', () => {
    const view = setup(); expect(view.container.querySelector('[data-word-id="w"]')).toHaveClass('bg-primary/15');
    view.stop(); expect(view.container.querySelector('[data-word-id="w"]')).not.toHaveClass('bg-primary/15');
    expect(view.getByRole('group', { name: 'Transcript text' }).textContent).toBe('Hello, world!  Hello.');
  });
  it('gives the focused word highlight steady inline padding and a softer offset outline without changing source text', () => {
    const view = setup();
    const region = view.getByRole('group', { name: 'Transcript text' });
    const word = view.container.querySelector('[data-word-id="w"]')!;
    expect(word).toHaveClass('px-[0.1em]');
    fireEvent.focus(region);
    expect(word).toHaveClass('outline-primary/40', 'outline-offset-1', 'rounded-[0.28em]');
    expect(region.textContent).toBe('Hello, world!  Hello.');
  });
  it('opens anchored settings from its own header without removing prose', () => {
    const view = setup();
    const settingsButton = view.getByRole('button', { name: 'Transcript settings' });
    expect(settingsButton).toHaveClass('hover:bg-muted', 'focus-visible:ring-2');
    expect(view.getByTestId('transcript-settings-icon')).toHaveAttribute('width', '18');
    fireEvent.click(settingsButton);
    expect(view.onOpenChange).toHaveBeenCalledWith(true);
    view.rerender(view.panel(true, true));
    expect(view.getByRole('dialog', { name: 'Transcript settings' })).toBeVisible();
    expect(view.getByRole('group', { name: 'Transcript text' })).toBeVisible();
    expect(view.getByLabelText('Import transcript JSON')).toBeTruthy();
  });
  it('dismisses the settings popover on outside pointer or Escape and restores gear focus', () => {
    const view = setup();
    view.rerender(view.panel(true, true));
    fireEvent.pointerDown(view.getByRole('group', { name: 'Transcript text' }));
    expect(view.onOpenChange).toHaveBeenLastCalledWith(false);
    view.rerender(view.panel(true, false));
    view.rerender(view.panel(true, true));
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(view.onOpenChange).toHaveBeenLastCalledWith(false);
    expect(view.getByRole('button', { name: 'Transcript settings' })).toHaveFocus();
  });
  it('keeps import in settings and selected file bytes available after failed write then retries asynchronously', async () => {
    const view = setup(); view.rerender(view.panel(true, true));
    const document = JSON.stringify({ segments: [{ text: 'Imported', start: 0, end: 1 }] });
    view.importTranscript.mockRejectedValueOnce(new Error('Choose media association'));
    fireEvent.change(view.getByLabelText('Import transcript JSON'), { target: { files: [{ text: async () => document }] } });
    await waitFor(() => expect(view.getByRole('alert')).toHaveTextContent('Choose media association'));
    expect(view.getByLabelText('Match to video or audio')).toHaveValue('asset');
    fireEvent.click(view.getByRole('button', { name: 'Retry import' }));
    await waitFor(() => expect(view.importTranscript).toHaveBeenLastCalledWith({ document, associationAssetId: 'asset' }));
    await waitFor(() => expect(view.queryByRole('button', { name: 'Retry import' })).toBeNull());
  });
  it('reports partial association accurately and does not discard retry bytes', async () => {
    const view = setup(); view.rerender(view.panel(true, true));
    view.importTranscript.mockResolvedValueOnce({ assetId: 'asset', sourceId: 'default', importedSegments: 1, replacedSegments: 0, replacedExistingSource: false, associationSaved: false });
    fireEvent.change(view.getByLabelText('Import transcript JSON'), { target: { files: [{ text: async () => '{}' }] } });
    await waitFor(() => expect(view.getByRole('alert')).toHaveTextContent('association still needs retry'));
    expect(view.getByRole('button', { name: 'Retry import' })).toBeTruthy();
  });
  it('loads existing project source choices without making playback trigger list requests', async () => {
    const view = setup(); await waitFor(() => expect(view.getByRole('option', { name: /Alt take/ })).toBeTruthy());
    const count = vi.mocked(view.adapter.listProjectSources!).mock.calls.length;
    view.stop(); expect(vi.mocked(view.adapter.listProjectSources!).mock.calls.length).toBe(count);
    fireEvent.change(view.getByLabelText('Transcript source'), { target: { value: `project:${JSON.stringify(['asset', 'other-document'])}` } });
    await waitFor(() => expect(view.adapter.selectProjectSource).toHaveBeenCalledWith({ assetId: 'asset', documentId: 'other-document' }));
  });
  it('preserves unsent text and exposes explicit conflict discard/reapply choices', async () => {
    const view = setup(); view.adapter.getProjectState = () => ({ supported: true, sources: [{ assetId: 'asset', documentId: 'document', sourceId: 'default', version: 5, status: 'conflict', hasDraft: true, canUndo: false, canRedo: false }] });
    view.publish(view.getSnapshot());
    expect(view.getByText('Project transcript · Conflict')).toBeTruthy();
    fireEvent.click(view.getByRole('button', { name: 'Reapply draft' }));
    await waitFor(() => expect(view.resolveSourceConflict).toHaveBeenCalledWith('document', 'reapply'));
  });
  it('shows unresolved canonical-reference errors without cached transcript truth and offers refresh', async () => {
    const view = setup(); const refreshSources = vi.fn(async () => {}); view.adapter.refreshSources = refreshSources;
    view.adapter.getProjectState = () => ({ supported: true, sources: [{ assetId: 'asset', documentId: 'missing', sourceId: '', version: 0, status: 'error', message: 'Missing project transcript. Retry Refresh.', hasDraft: false, canUndo: false, canRedo: false }] });
    view.publish({ sources: [], occurrences: [] });
    expect(view.getByRole('alert')).toHaveTextContent('Missing project transcript');
    await waitFor(() => expect(view.getByText('Choose a saved transcript for Interview.mp4 above.')).toBeTruthy());
    fireEvent.click(view.getByRole('button', { name: 'Refresh project transcripts' }));
    await waitFor(() => expect(refreshSources).toHaveBeenCalledOnce());
  });

  it('names the selected media in an empty state and opens transcript settings from Import', async () => {
    const view = setup();
    view.publish({ sources: [], occurrences: [] });
    vi.mocked(view.adapter.listProjectSources!).mockResolvedValueOnce([]);
    fireEvent.focus(view.getByLabelText('Transcript source'));
    await waitFor(() => expect(view.getByText('No saved transcript for Interview.mp4.')).toBeTruthy());
    const lookupCount = vi.mocked(view.adapter.listProjectSources!).mock.calls.length;
    fireEvent.click(view.getByLabelText('Transcript source'));
    await waitFor(() => expect(vi.mocked(view.adapter.listProjectSources!).mock.calls.length).toBeGreaterThan(lookupCount));
    fireEvent.click(view.getByRole('button', { name: 'Import transcript…' }));
    expect(view.onOpenChange).toHaveBeenCalledWith(true);
    view.rerender(view.panel(true, true));
    expect(view.getByLabelText('Import transcript JSON')).toBeTruthy();
  });

  it('keeps saved choices for one media when another media lookup fails', async () => {
    const view = setup();
    view.publish({ sources: [], occurrences: [] });
    view.adapter.getPlayback = () => ({ playing: [], focused: null, sourceId: null, assetId: null, playingWordIds: [] });
    view.setMediaChoices([
      { assetId: 'good-media', label: 'Interview.mp4', kind: 'video' },
      { assetId: 'bad-media', label: 'Notes.wav', kind: 'audio' },
    ]);
    vi.mocked(view.adapter.listProjectSources!).mockImplementation(async (assetId) => {
      if (assetId === 'bad-media') throw new Error('Notes.wav is unavailable.');
      if (assetId === 'good-media') return [{ documentId: 'good-doc', sourceId: 'Main take', version: 2 }];
      return [];
    });
    view.rerender(view.panel());
    await waitFor(() => expect(view.getByRole('option', { name: 'Interview.mp4 · Main take · Project' })).toBeTruthy());
    fireEvent.change(view.getByLabelText('Transcript source'), { target: { value: 'media:bad-media' } });
    await waitFor(() => expect(view.getByRole('alert')).toHaveTextContent('Notes.wav is unavailable.'));
    expect(view.getByRole('option', { name: 'Interview.mp4 · Main take · Project' })).toBeTruthy();
  });

  it('disables import with the concrete media reason when the timeline has no audio or video', async () => {
    const view = setup();
    view.publish({ sources: [], occurrences: [] });
    view.adapter.getPlayback = () => ({ playing: [], focused: null, sourceId: null, assetId: null, playingWordIds: [] });
    view.setMediaChoices([]);
    view.rerender(view.panel());
    expect(view.getByText('Add an audio or video clip to this timeline to select or import a transcript.')).toBeTruthy();
    fireEvent.click(view.getByRole('button', { name: 'Transcript settings' }));
    view.rerender(view.panel(true, true));
    expect(view.getByRole('button', { name: 'Import transcript…' })).toBeDisabled();
    expect(view.getByRole('note')).toHaveTextContent('Add an audio or video clip');
  });

  it('disables project import when the provider lacks durable transcript authority', () => {
    const view = setup();
    view.adapter.getProjectState = () => ({ supported: false, reason: 'Reconnect to the Runtime project to save transcripts.', sources: [] });
    view.publish(view.getSnapshot());
    fireEvent.click(view.getByRole('button', { name: 'Transcript settings' }));
    view.rerender(view.panel(true, true));
    expect(view.getByRole('button', { name: 'Import transcript…' })).toBeDisabled();
    expect(view.getByRole('note')).toHaveTextContent('Reconnect to the Runtime project');
  });

});
