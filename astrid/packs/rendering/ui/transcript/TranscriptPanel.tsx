import { createElement, useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import type { ExtensionContext, PanelRenderProps, TranscriptPanelTextEdit, TranscriptSelection, TranscriptPanelTextEditResult, TranscriptSourceIdentity, TranscriptSourceRow, TranscriptSourceWordView, TranscriptProjectSourceChoice } from '@reigh/editor-sdk';

export interface TranscriptPanelProps extends PanelRenderProps { readonly context: ExtensionContext }
const EMPTY = { sources: [], occurrences: [] };
const INITIAL_SELECTION: TranscriptSelection = { assetId: null, sourceId: null, occurrenceId: null };
const sourceKey = (source: TranscriptSourceIdentity) => JSON.stringify([source.assetId, source.sourceId]);
const button = 'min-h-10 sm:min-h-8 rounded-md px-2 text-xs hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50';
const select = 'min-h-10 sm:min-h-8 min-w-0 max-w-full rounded-md border border-border/70 bg-background px-2 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';
type Fallback = NonNullable<Extract<TranscriptPanelTextEditResult, { ok: false }>['fallback']>;
type Target = { key: string; source: TranscriptSourceRow; word?: TranscriptSourceWordView };
type ProjectSourceLookup = {
  readonly status: 'loading' | 'loaded' | 'error' | 'unavailable';
  readonly choices: readonly TranscriptProjectSourceChoice[];
  readonly message?: string;
};

/** Match against the canonical string. Never reconstruct text from alignment. */
export function alignedTextParts(source: TranscriptSourceRow): Array<{ text: string; word?: TranscriptSourceWordView }> {
  if (!source.words?.length) return [{ text: source.text }];
  let cursor = 0;
  const parts: Array<{ text: string; word?: TranscriptSourceWordView }> = [];
  for (const word of source.words) {
    if (!word.text) return [{ text: source.text }];
    const at = source.text.indexOf(word.text, cursor);
    if (at < 0 || /[\p{L}\p{N}]/u.test(source.text.slice(cursor, at))) return [{ text: source.text }];
    if (at > cursor) parts.push({ text: source.text.slice(cursor, at) });
    parts.push({ text: source.text.slice(at, at + word.text.length), word });
    cursor = at + word.text.length;
  }
  if (/[\p{L}\p{N}]/u.test(source.text.slice(cursor))) return [{ text: source.text }];
  if (cursor < source.text.length) parts.push({ text: source.text.slice(cursor) });
  return parts;
}

/** Canonical document state and mutation authority stay in the host adapter. */
export function TranscriptPanel(props: TranscriptPanelProps) {
  const adapter = props.video?.transcript;
  const settingsOpen = props.settings?.open ?? false;
  const observing = props.visible;
  const [revision, refresh] = useState(0);
  const [selection, setSelection] = useState(INITIAL_SELECTION);
  const [edit, setEdit] = useState<TranscriptPanelTextEdit | null>(null);
  const [fallback, setFallback] = useState<Fallback | null>(null);
  const [following, setFollowing] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [pendingDocument, setPendingDocument] = useState<string | null>(null);
  const [association, setAssociation] = useState<string | null>(null);
  const [projectLookups, setProjectLookups] = useState<Record<string, ProjectSourceLookup>>({});
  const [targetKey, setTargetKey] = useState<string | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [hoverKey, setHoverKey] = useState<string | null>(null);
  const scroll = useRef<HTMLDivElement>(null);
  const prose = useRef<HTMLDivElement>(null);
  const editor = useRef<HTMLTextAreaElement>(null);
  const importInput = useRef<HTMLInputElement>(null);
  const settingsTrigger = useRef<HTMLButtonElement>(null);
  const settingsPopover = useRef<HTMLDivElement>(null);
  const skipFocusDetails = useRef(false);
  const programmedScroll = useRef<number | null>(null);
  const savedScrollTop = useRef(0);
  const request = useRef(0);
  const mounted = useRef(true);
  useEffect(() => () => { mounted.current = false; request.current += 1; }, []);
  useEffect(() => {
    if (!observing || !adapter) return;
    const documentSubscription = adapter.subscribe(() => refresh((value) => value + 1));
    const playbackSubscription = observing ? props.video?.view.subscribe(() => refresh((value) => value + 1)) : undefined;
    refresh((value) => value + 1);
    return () => { documentSubscription.dispose(); playbackSubscription?.dispose(); };
  }, [props.visible, observing, adapter, props.video]);
  useEffect(() => {
    if (!settingsOpen || !props.visible) return;
    const dismissOutside = (event: PointerEvent) => {
      const target = event.target;
      if (!(target instanceof Node) || settingsPopover.current?.contains(target) || settingsTrigger.current?.contains(target)) return;
      props.settings?.onOpenChange(false);
    };
    const dismissEscape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      props.settings?.onOpenChange(false);
      settingsTrigger.current?.focus();
    };
    document.addEventListener('pointerdown', dismissOutside);
    document.addEventListener('keydown', dismissEscape);
    return () => {
      document.removeEventListener('pointerdown', dismissOutside);
      document.removeEventListener('keydown', dismissEscape);
    };
  }, [settingsOpen, props.visible, props.settings]);

  const snapshot = adapter?.getSnapshot() ?? EMPTY;
  const playback = observing ? adapter?.getPlayback(selection) : undefined;
  const mediaChoices = adapter?.getMediaChoices() ?? [];
  // A media-only picker selection has an asset ID and a null source ID. That
  // state must survive playback gaps instead of snapping back to another source.
  const selectedAssetId = selection.assetId ?? playback?.assetId ?? snapshot.sources[0]?.assetId
    ?? (mediaChoices.length === 1 ? mediaChoices[0].assetId : null);
  const associationValue = association ?? selectedAssetId ?? '';
  const selectedSourceId = selection.assetId !== null ? selection.sourceId
    : playback?.sourceId ?? snapshot.sources[0]?.sourceId ?? null;
  const sources = snapshot.sources.filter((source) => source.sourceId === selectedSourceId && source.assetId === selectedAssetId);
  const sourceChoices = [...new Map(snapshot.sources.map((source) => [sourceKey(source), source])).values()];
  const projectState = adapter?.getProjectState?.();
  const documentId = sources[0]?.documentId;
  const state = projectState?.sources.find((source) => source.documentId === documentId && source.assetId === selectedAssetId);
  const referenceErrors = projectState?.sources.filter((source) => source.status === 'error' && (!selectedAssetId || source.assetId === selectedAssetId)) ?? [];
  const projectLookup = selectedAssetId
    ? projectLookups[selectedAssetId] ?? (adapter?.listProjectSources && projectState?.supported !== false
      ? { status: 'loading' as const, choices: [] }
      : { status: 'unavailable' as const, choices: [], message: projectState?.reason ?? 'Project transcript discovery is unavailable in this provider.' })
    : null;
  const focused = playback?.focused;
  const content = sources.map((source) => ({ source, parts: alignedTextParts(source) }));
  const targets: Target[] = content.flatMap(({ source, parts }) => parts.some((part) => part.word)
    ? parts.flatMap((part) => part.word ? [{ key: JSON.stringify([source.assetId, source.sourceItemId, part.word.id]), source, word: part.word }] : [])
    : [{ key: JSON.stringify([source.assetId, source.sourceItemId]), source }]);
  const target = targets.find((item) => item.key === targetKey) ?? targets[0];
  const hover = targets.find((item) => item.key === hoverKey);
  const activeEdit = Boolean(edit) && sources.some((source) => source.sourceItemId === edit?.sourceItemId && source.assetId === edit?.assetId);
  const occurrences = target ? snapshot.occurrences.filter((item) => item.sourceItemId === target.source.sourceItemId && item.assetId === target.source.assetId) : [];
  const occurrence = occurrences.find((item) => item.id === selection.occurrenceId) ?? occurrences.find((item) => item.id === focused?.id) ?? occurrences[0];
  const mediaLabel = (assetId: string | null) => assetId
    ? mediaChoices.find((media) => media.assetId === assetId)?.label
      ?? 'Selected media'
    : '';
  const sourceLabel = (sourceId: string) => /^(sha256:|transcript:|[a-f\d]{32,})/.test(sourceId) ? 'Transcript' : sourceId === 'default' ? 'Transcript' : sourceId;

  const mediaIds = JSON.stringify(mediaChoices.map((media) => media.assetId));
  const playingWordIds = JSON.stringify(playback?.playingWordIds ?? []);
  const projectLookupRequest = useRef(new Map<string, number>());
  const refreshProjectSourceChoices = useCallback(async (assetIds: readonly string[]) => {
    if (!adapter?.listProjectSources || adapter.getProjectState?.().supported === false) return;
    await Promise.all(assetIds.map(async (assetId) => {
      const requestId = (projectLookupRequest.current.get(assetId) ?? 0) + 1;
      projectLookupRequest.current.set(assetId, requestId);
      setProjectLookups((previous) => ({
        ...previous,
        [assetId]: { status: 'loading', choices: previous[assetId]?.choices ?? [] },
      }));
      try {
        const choices = await adapter.listProjectSources!(assetId);
        if (!mounted.current || projectLookupRequest.current.get(assetId) !== requestId) return;
        setProjectLookups((previous) => ({ ...previous, [assetId]: { status: 'loaded', choices } }));
      } catch (cause) {
        if (!mounted.current || projectLookupRequest.current.get(assetId) !== requestId) return;
        setProjectLookups((previous) => ({
          ...previous,
          [assetId]: {
            status: 'error',
            // Keep the last known choices for this media, and all choices for
            // other media, when one Runtime lookup fails.
            choices: previous[assetId]?.choices ?? [],
            message: cause instanceof Error ? cause.message : 'Could not load project transcripts for this media.',
          },
        }));
      }
    }));
  }, [adapter]);
  useEffect(() => {
    if (!props.visible || !adapter?.listProjectSources) return;
    void refreshProjectSourceChoices(JSON.parse(mediaIds) as string[]);
  }, [props.visible, adapter, mediaIds, refreshProjectSourceChoices]);
  useLayoutEffect(() => {
    if (observing && scroll.current) { scroll.current.scrollTop = savedScrollTop.current; programmedScroll.current = savedScrollTop.current; }
  }, [observing]);
  useEffect(() => {
    const container = scroll.current;
    if (!observing || !following || !focused || !container) return;
    const nodes = [...container.querySelectorAll<HTMLElement>('[data-source-item]')];
    const active = nodes.find((node) => node.dataset.sourceItem === focused.sourceItemId && node.dataset.sourceAsset === focused.assetId);
    if (!active) return;
    const word = [...active.querySelectorAll<HTMLElement>('[data-word-id]')].find((node) => (JSON.parse(playingWordIds) as string[]).includes(node.dataset.wordId ?? ''));
    const rect = (word ?? active).getBoundingClientRect();
    const bounds = container.getBoundingClientRect();
    if (rect.top < bounds.top || rect.bottom > bounds.bottom) {
      container.scrollTop += rect.top < bounds.top ? rect.top - bounds.top - 16 : rect.bottom - bounds.bottom + 16;
      programmedScroll.current = container.scrollTop; savedScrollTop.current = container.scrollTop;
    }
  }, [observing, following, focused, playingWordIds, revision]);
  useEffect(() => { if (activeEdit && observing) editor.current?.focus(); }, [activeEdit, observing]);

  if (typeof props.instanceId !== 'string' || typeof props.visible !== 'boolean') return createElement('div', { role: 'alert' }, 'Transcript requires a host with the panel instance API. Update the editor.');

  const run = async (operation: () => Promise<void>) => {
    if (busy) return;
    setBusy(true); setError(''); setMessage('');
    try { await operation(); }
    catch (cause) { if (mounted.current) setError(cause instanceof Error ? cause.message : 'Could not save transcript. Your draft is retained.'); }
    finally { if (mounted.current) { setBusy(false); refresh((value) => value + 1); } }
  };
  const restoreReadingFocus = () => { skipFocusDetails.current = true; prose.current?.focus(); };
  const seek = (item: Target) => {
    const choices = snapshot.occurrences.filter((candidate) => candidate.sourceItemId === item.source.sourceItemId && candidate.assetId === item.source.assetId);
    const selected = choices.find((candidate) => candidate.id === selection.occurrenceId) ?? choices.find((candidate) => candidate.id === focused?.id) ?? choices[0];
    const result = selected && adapter?.seek({ occurrenceId: selected.id, ...(item.word ? { wordId: item.word.id } : {}) });
    setTargetKey(item.key); setDetailsOpen(true);
    if (!result || !result.ok) {
      setError(result && result.reason === 'outside' ? 'This word is outside this clip trim. Choose another occurrence.' : 'No playable clip occurrence. Add this media or adjust its trim to seek.'); return;
    }
    setSelection({ assetId: item.source.assetId, sourceId: item.source.sourceId, occurrenceId: selected!.id }); setError('');
    setMessage(result.timing === 'segment' && item.word ? 'Word timing unavailable; moved to the segment start.' : '');
  };
  const startEdit = (item: Target) => {
    const identity = { sourceItemId: item.source.sourceItemId, assetId: item.source.assetId, documentId: item.source.documentId, baseVersion: item.source.documentVersion };
    setEdit(item.word ? { ...identity, type: 'word', wordId: item.word.id, text: item.word.text } : { ...identity, type: 'segment', text: item.source.text });
    setFallback(null); setError(''); setMessage(''); setDetailsOpen(true);
  };
  const importDocument = async (document: string, associationAssetId?: string) => {
    if (!adapter?.importTranscript) return;
    if (projectState?.supported !== true) throw new Error(projectState?.reason ?? 'Project transcript saving is unavailable in this provider.');
    if (!mediaChoices.length) throw new Error('Add an audio or video clip to this timeline before importing a transcript.');
    // Keep the exact selected bytes until the durable write and association succeed.
    setPendingDocument(document);
    setAssociation(associationAssetId ?? '');
    const receipt = await adapter.importTranscript({ document, ...(associationAssetId ? { associationAssetId } : {}) });
    await refreshProjectSourceChoices([receipt.assetId]);
    if (receipt.associationSaved === false) {
      setSelection({ assetId: receipt.assetId, sourceId: null, occurrenceId: null });
      throw new Error(receipt.message ?? 'Project transcript saved. Timeline association still needs retry.');
    }
    setPendingDocument(null); setAssociation(null);
    setMessage(receipt.message ?? 'Project transcript saved.');
    // The canonical receipt is the first point at which the UI selects the
    // imported source; a local file read is never treated as a saved transcript.
    setSelection({ assetId: receipt.assetId, sourceId: receipt.sourceId, occurrenceId: null });
  };
  const history = (action: 'undo' | 'redo' | 'discard' | 'reapply') => run(async () => {
    if (!documentId) return;
    const result = action === 'undo' ? await adapter?.undoSource?.(documentId) : action === 'redo' ? await adapter?.redoSource?.(documentId) : await adapter?.resolveSourceConflict?.(documentId, action);
    if (result && !result.ok) throw new Error(result.message);
    if (action === 'discard' || action === 'reapply') { setEdit(null); setFallback(null); }
    setMessage(action === 'discard' ? 'Reloaded saved transcript; local draft discarded.' : 'Project transcript saved.');
  });
  const metadata = (item: Target) => `${item.word ? 'Word' : 'Segment'} · ${(item.word?.start ?? item.source.start).toFixed(2)}–${(item.word?.end ?? item.source.end).toFixed(2)}s${item.source.speaker ? ` · ${item.source.speaker}` : ''}`;
  const status = busy || state?.status === 'saving' ? 'Saving…' : state?.status === 'conflict' ? 'Conflict' : state?.hasDraft || state?.status === 'error' ? 'Unsaved' : 'Saved';
  const importDisabled = busy || !adapter?.importTranscript || !adapter.listProjectSources || projectState?.supported !== true || mediaChoices.length === 0;
  const importDisabledReason = mediaChoices.length === 0
    ? 'Add an audio or video clip to this timeline before importing a transcript.'
    : projectState?.supported !== true
      ? projectState?.reason ?? 'Project transcript saving is unavailable in this provider.'
      : !adapter?.listProjectSources
        ? 'Project transcript selection is unavailable in this provider.'
      : null;
  const selectedMediaName = mediaLabel(selectedAssetId);
  const selectedMediaSources = selectedAssetId ? sourceChoices.filter((source) => source.assetId === selectedAssetId) : [];
  const selectedProjectChoices = selectedAssetId ? projectLookup?.choices ?? [] : [];
  const selectedSourceChoice = selectedAssetId && selectedSourceId
    ? sourceChoices.find((source) => source.assetId === selectedAssetId && source.sourceId === selectedSourceId)
    : undefined;
  const selectedRemoteChoice = selectedAssetId && selectedSourceId
    ? projectLookups[selectedAssetId]?.choices.find((choice) => choice.sourceId === selectedSourceId)
    : undefined;
  const selectorValue = selectedSourceChoice
    ? `local:${sourceKey(selectedSourceChoice)}`
    : selectedRemoteChoice
      ? `project:${JSON.stringify([selectedAssetId, selectedRemoteChoice.documentId])}`
      : selectedAssetId ? `media:${selectedAssetId}` : '';

  return <section aria-label="Transcript" data-testid="astrid-transcript-panel" data-panel-instance-id={props.instanceId} data-panel-visible={String(props.visible)} hidden={!props.visible} style={{ display: props.visible ? undefined : 'none' }}
    className="relative box-border flex h-full min-h-0 min-w-0 max-w-full flex-col text-sm">
    {!adapter ? <p role="status" className="p-3">Transcript is unavailable in this host. Open a loaded video editor timeline.</p> : <>
      <div className="shrink-0 px-3 pt-3 pb-2">
        <div className="flex min-w-0 items-center gap-1">
        <div className="flex min-w-0 flex-1 items-center gap-1">
          <label className="sr-only" htmlFor={`${props.instanceId}-source`}>Transcript source</label>
          <div className="relative min-w-0 flex-1">
          <select id={`${props.instanceId}-source`} aria-label="Transcript source" className={`${select} w-full appearance-none truncate pl-2 pr-8`} value={selectorValue}
            disabled={busy || (!mediaChoices.length && !sourceChoices.length)}
            onFocus={() => { void refreshProjectSourceChoices(mediaChoices.map((media) => media.assetId)); }}
            onClick={() => { void refreshProjectSourceChoices(mediaChoices.map((media) => media.assetId)); }}
            onChange={(event) => {
              const value = event.target.value;
              if (value.startsWith('media:')) {
                const assetId = value.slice('media:'.length);
                setSelection({ assetId, sourceId: null, occurrenceId: null });
                setTargetKey(null); setDetailsOpen(false); setError(''); setMessage('');
                return;
              }
              if (value.startsWith('local:')) {
                const source = sourceChoices.find((item) => `local:${sourceKey(item)}` === value);
                if (source) { setSelection(adapter.selectSource(selection, source)); setTargetKey(null); setDetailsOpen(false); }
              } else {
                if (!value.startsWith('project:')) return;
                const [assetId, nextDocumentId] = JSON.parse(value.slice('project:'.length)) as [string, string];
                void run(async () => {
                  const receipt = await adapter.selectProjectSource?.({ assetId, documentId: nextDocumentId });
                  if (receipt?.associationSaved === false) {
                    setSelection({ assetId, sourceId: null, occurrenceId: null });
                    await refreshProjectSourceChoices([assetId]);
                    throw new Error(receipt.message ?? 'Project transcript is available. Timeline association needs retry.');
                  }
                  if (receipt) { setSelection({ assetId, sourceId: receipt.sourceId, occurrenceId: null }); setTargetKey(null); setDetailsOpen(false); }
                  await refreshProjectSourceChoices([assetId]);
                });
              }
            }}>
            {!selectedAssetId && <option value="" disabled>{mediaChoices.length ? 'Choose media or transcript' : 'Add audio or video media first'}</option>}
            {mediaChoices.map((media) => <optgroup key={media.assetId} label={media.label}>
              <option value={`media:${media.assetId}`}>
                {projectLookups[media.assetId]?.status === 'loading' ? `Loading transcripts for ${media.label}…`
                  : projectLookups[media.assetId]?.status === 'error' ? `Transcript search failed for ${media.label}`
                    : (projectLookups[media.assetId]?.choices.length ?? 0) + sourceChoices.filter((source) => source.assetId === media.assetId).length > 0
                      ? `All transcripts for ${media.label}` : `No saved transcript for ${media.label}`}
              </option>
              {sourceChoices.filter((source) => source.assetId === media.assetId).map((source) => <option key={sourceKey(source)} value={`local:${sourceKey(source)}`}>{media.label} · {sourceLabel(source.sourceId)}{source.documentId ? '' : ' · Timeline only'}</option>)}
              {(projectLookups[media.assetId]?.choices ?? []).filter((choice) => !sourceChoices.some((source) => source.assetId === media.assetId && source.documentId === choice.documentId)).map((choice) => <option key={choice.documentId} value={`project:${JSON.stringify([media.assetId, choice.documentId])}`}>{media.label} · {sourceLabel(choice.sourceId)} · Project</option>)}
            </optgroup>)}
            {sourceChoices.filter((source) => !mediaChoices.some((media) => media.assetId === source.assetId)).map((source) => <option key={sourceKey(source)} value={`local:${sourceKey(source)}`}>{mediaLabel(source.assetId)} · {sourceLabel(source.sourceId)}</option>)}
          </select>
          <svg data-testid="transcript-source-chevron" aria-hidden="true" focusable="false" className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6" /></svg>
          </div>
          <button type="button" className={`${button} shrink-0 text-muted-foreground`} aria-label={following ? 'Following playhead' : 'Resume follow'} aria-pressed={following} onClick={() => setFollowing(!following)}>{following ? '↳ Follow' : 'Resume follow'}</button>
        </div>
        <button ref={settingsTrigger} type="button" aria-label="Transcript settings" title="Transcript settings" aria-expanded={settingsOpen} aria-controls={`${props.instanceId}-settings`} className={`${button} flex w-10 shrink-0 items-center justify-center px-0 sm:w-8 text-muted-foreground`} onClick={() => props.settings?.onOpenChange(!settingsOpen)}>
          <svg data-testid="transcript-settings-icon" aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 1.72l-.26 1.9a7.36 7.36 0 0 0-1.59.92l-1.8-.74a2 2 0 0 0-2.49.91l-.22.38a2 2 0 0 0 .5 2.6l1.52 1.18a7.9 7.9 0 0 0 0 1.84l-1.52 1.18a2 2 0 0 0-.5 2.6l.22.38a2 2 0 0 0 2.49.91l1.8-.74c.49.38 1.02.69 1.59.92l.26 1.9a2 2 0 0 0 2 1.72h.44a2 2 0 0 0 2-1.72l.26-1.9a7.36 7.36 0 0 0 1.59-.92l1.8.74a2 2 0 0 0 2.49-.91l.22-.38a2 2 0 0 0-.5-2.6l-1.52-1.18a7.9 7.9 0 0 0 0-1.84l1.52-1.18a2 2 0 0 0 .5-2.6l-.22-.38a2 2 0 0 0-2.49-.91l-1.8.74a7.36 7.36 0 0 0-1.59-.92l-.26-1.9a2 2 0 0 0-2-1.72z" /><circle cx="12" cy="12" r="3" /></svg>
        </button>
        </div>
        {!!sources.length && <p role="status" className="mt-2 text-[11px] text-muted-foreground">{documentId ? `Project transcript · ${status}` : 'Timeline only'}</p>}
        {(error || state?.message || referenceErrors.length > 0 || projectLookup?.status === 'error') && <p role="alert" className="mt-2 text-xs text-destructive">{error || state?.message || referenceErrors.map((source) => source.message).filter(Boolean).join(' ') || projectLookup?.message || 'Project transcript could not be loaded.'}</p>}
        {(referenceErrors.length > 0 || projectLookup?.status === 'error') && <button type="button" className={button} disabled={busy || !adapter.listProjectSources} onClick={() => void run(async () => { await adapter.refreshSources?.(); await refreshProjectSourceChoices(mediaChoices.map((media) => media.assetId)); })}>Refresh project transcripts</button>}
        {message && <p role="status" className="mt-2 text-xs text-muted-foreground">{message}</p>}
        {(state?.status === 'conflict' || state?.hasDraft && !activeEdit) && <div className="mt-2 flex flex-wrap gap-1 text-xs"><span className="w-full">{state.status === 'conflict' ? 'A newer saved transcript is available. Your draft is retained.' : 'An unsaved source draft is available.'}</span>{state.draftPreview && <details className="w-full"><summary className="cursor-pointer py-2">Review local draft</summary><p className="whitespace-pre-wrap break-words text-muted-foreground">{state.draftPreview.text}</p></details>}<button className={button} disabled={busy} onClick={() => void history('discard')}>Reload / discard draft</button><button className={button} disabled={busy} onClick={() => void history('reapply')}>Reapply draft</button></div>}
      </div>
      {settingsOpen && <div ref={settingsPopover} id={`${props.instanceId}-settings`} role="dialog" aria-label="Transcript settings" className="absolute right-3 top-[3.25rem] z-30 max-h-[min(70dvh,36rem)] w-[min(24rem,calc(100%-1.5rem))] overflow-y-auto overscroll-contain rounded-lg border border-border bg-popover p-4 text-popover-foreground shadow-xl">
        <div className="space-y-5">
          <div><h3 className="font-medium">Transcript settings</h3><p className="mt-1 text-xs text-muted-foreground">Edits apply everywhere this project transcript is used.</p></div>
          <label className="flex min-h-10 items-center gap-2 text-sm"><input type="checkbox" checked={adapter.getTimelineLaneVisible?.() ?? true} disabled={!adapter.setTimelineLaneVisible} onChange={(event) => { adapter.setTimelineLaneVisible?.(event.target.checked); refresh((value) => value + 1); }} />Show transcript lane</label>
          <div className="space-y-2">
            <label className="flex flex-col gap-1 text-xs">Match to video or audio
              <select className={select} value={associationValue} disabled={busy || !mediaChoices.length} onChange={(event) => setAssociation(event.target.value)}>
                <option value="">Use media named in transcript file</option>
                {mediaChoices.map((choice) => <option key={choice.assetId} value={choice.assetId}>{choice.label}</option>)}
              </select>
            </label>
            <p className="text-[11px] text-muted-foreground">If the file names a video or audio clip, it must match your choice.</p>
            <button type="button" className={`${button} border border-border`} disabled={importDisabled} title={importDisabledReason ?? undefined} onClick={() => importInput.current?.click()}>Import transcript…</button>
            <input ref={importInput} className="sr-only" tabIndex={-1} type="file" aria-label="Import transcript JSON" accept=".json,application/json" disabled={importDisabled} onChange={(event) => {
              const file = event.target.files?.[0]; event.target.value = ''; if (!file) return;
              const token = ++request.current;
              void run(async () => {
                let document: string;
                try { document = await file.text(); }
                catch { throw new Error('Could not read this file. Choose a readable transcript JSON file and try again.'); }
                if (token === request.current) await importDocument(document, associationValue || undefined);
              });
            }} /></div>
          {importDisabledReason && <p role="note" className="text-xs text-muted-foreground">{importDisabledReason}</p>}
          {pendingDocument !== null && <div className="space-y-2"><p className="text-xs text-muted-foreground">The selected file is preserved. Correct its media association or retry its pending save.</p><button className={button} disabled={busy || !mediaChoices.length || projectState?.supported !== true} onClick={() => void run(() => importDocument(pendingDocument, associationValue || undefined))}>Retry import</button><button className={button} disabled={busy} onClick={() => { setPendingDocument(null); setAssociation(null); }}>Cancel import</button></div>}
          {!documentId && sources.length > 0 && <button type="button" className={`${button} border border-border`} disabled={busy || !adapter.promoteSource} onClick={() => void run(async () => {
            const receipt = await adapter.promoteSource!({ assetId: selectedAssetId!, sourceId: selectedSourceId! });
            if (receipt.associationSaved === false) throw new Error(receipt.message ?? 'Project transcript saved. Timeline association needs retry.');
            setMessage(receipt.message ?? 'Project transcript saved.');
          })}>Save as project transcript</button>}
          {projectState?.supported === false && <p className="text-xs text-muted-foreground">{projectState.reason}</p>}
          {documentId && <div className="flex gap-2"><button className={button} disabled={busy || !state?.canUndo} onClick={() => void history('undo')}>Undo source edit</button><button className={button} disabled={busy || !state?.canRedo} onClick={() => void history('redo')}>Redo source edit</button></div>}
        </div>
      </div>}
      <div ref={scroll} data-testid="transcript-reading-area" className="mx-3 mb-3 min-h-0 flex-1 overflow-y-auto overscroll-contain rounded-lg border border-border bg-background px-4 py-4" style={{ scrollbarGutter: 'stable' }}
        onWheel={() => setFollowing(false)} onTouchMove={() => setFollowing(false)} onScroll={() => {
          if (!observing) return;
          savedScrollTop.current = scroll.current?.scrollTop ?? savedScrollTop.current;
          if (programmedScroll.current !== null && scroll.current?.scrollTop === programmedScroll.current) { programmedScroll.current = null; return; }
          programmedScroll.current = null; setFollowing(false);
        }}>
        <div>
          {!sources.length ? <div className="py-8 text-center">
            {!mediaChoices.length
              ? <p className="text-muted-foreground">Add an audio or video clip to this timeline to select or import a transcript.</p>
              : !selectedAssetId
                ? <p className="text-muted-foreground">Choose an audio or video media to view its transcripts.</p>
                : projectLookup?.status === 'loading'
                  ? <p role="status" className="text-muted-foreground">Loading saved transcripts for {selectedMediaName}…</p>
                  : projectLookup?.status === 'error'
                    ? <p role="status" className="text-muted-foreground">Could not load saved transcripts for {selectedMediaName}.</p>
                    : projectLookup?.status === 'unavailable'
                      ? <p role="status" className="text-muted-foreground">{projectLookup.message ?? 'Project transcript discovery is unavailable.'}</p>
                      : selectedProjectChoices.length || selectedMediaSources.length
                        ? <p className="text-muted-foreground">Choose a saved transcript for {selectedMediaName} above.</p>
                        : <p className="text-muted-foreground">No saved transcript for {selectedMediaName}.</p>}
            {projectLookup?.status === 'error' && <button type="button" className={`${button} mt-2`} disabled={busy} onClick={() => void run(async () => { await adapter.refreshSources?.(); await refreshProjectSourceChoices([selectedAssetId!]); })}>Retry transcript search</button>}
            {!settingsOpen && projectLookup?.status !== 'error' && <button type="button" className={`${button} mt-2`} disabled={importDisabled} title={importDisabledReason ?? undefined} onClick={() => props.settings?.onOpenChange(true)}>Import transcript…</button>}
          </div> : <>
            <p id={`${props.instanceId}-help`} className="sr-only">Use arrow keys to move between words or segments. Enter or Space seeks and opens details. Tab reaches Edit. Select and copy text normally.</p>
            <div ref={prose} role="group" aria-label="Transcript text" aria-describedby={`${props.instanceId}-help`} tabIndex={0} aria-activedescendant={target ? `${props.instanceId}-target-${targets.indexOf(target)}` : undefined}
              className="whitespace-pre-wrap break-words rounded-sm text-[14px] font-normal leading-[1.75] text-foreground outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              onFocus={() => { if (skipFocusDetails.current) { skipFocusDetails.current = false; return; } setDetailsOpen(true); }} onKeyDown={(event) => {
                if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
                const index = Math.max(0, targets.findIndex((item) => item.key === target?.key));
                if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) {
                  event.preventDefault(); setFollowing(false); setDetailsOpen(true);
                  const next = event.key === 'Home' ? 0 : event.key === 'End' ? targets.length - 1 : Math.max(0, Math.min(targets.length - 1, index + (['ArrowLeft', 'ArrowUp'].includes(event.key) ? -1 : 1)));
                  setTargetKey(targets[next]?.key ?? null);
                } else if ((event.key === 'Enter' || event.key === ' ') && target) { event.preventDefault(); seek(target); }
                else if (event.key === 'Escape') { setDetailsOpen(false); setHoverKey(null); }
              }}>
              {content.map(({ source, parts }, sourceIndex) => {
                const aligned = parts.some((part) => part.word);
                const segmentTarget = targets.find((item) => item.source === source && !item.word);
                const active = focused?.sourceItemId === source.sourceItemId && focused.assetId === source.assetId;
                const previous = content[sourceIndex - 1]?.source;
                // Existing whitespace wins; otherwise segment boundaries read as prose.
                const separator = previous && !/\s$/.test(previous.text) && !/^\s/.test(source.text) ? previous.speaker !== source.speaker && (previous.speaker || source.speaker) ? '\n\n' : ' ' : '';
                return <span key={JSON.stringify([source.assetId, source.sourceItemId])}>{separator}<span data-source-item={source.sourceItemId} data-source-asset={source.assetId} aria-current={active ? 'true' : undefined} className={`${active ? 'decoration-primary/40 underline decoration-1 underline-offset-4' : ''} ${!aligned ? `cursor-pointer hover:bg-muted ${detailsOpen && target?.key === segmentTarget?.key ? 'outline outline-1 outline-ring rounded-sm' : ''}` : ''}`}
                  {...(!aligned && segmentTarget ? { id: `${props.instanceId}-target-${targets.indexOf(segmentTarget)}`, role: 'button', tabIndex: -1, title: metadata(segmentTarget), onMouseEnter: () => setHoverKey(segmentTarget.key), onMouseLeave: () => setHoverKey(null), onClick: () => { if (window.getSelection()?.isCollapsed !== false) seek(segmentTarget); } } : {})}>
                  {parts.map((part, index) => {
                    const item = part.word && targets.find((candidate) => candidate.source === source && candidate.word?.id === part.word!.id);
                    return item ? <span key={index} id={`${props.instanceId}-target-${targets.indexOf(item)}`} data-word-id={item.word!.id} role="button" tabIndex={-1} title={metadata(item)} onMouseEnter={() => setHoverKey(item.key)} onMouseLeave={() => setHoverKey(null)} onClick={() => { if (window.getSelection()?.isCollapsed !== false) seek(item); }}
                      className={`cursor-pointer rounded-[0.28em] px-[0.1em] hover:bg-muted ${active && playback?.playingWordIds.includes(item.word!.id) ? 'bg-primary/15 text-foreground' : ''} ${detailsOpen && target?.key === item.key ? 'outline outline-1 outline-primary/40 outline-offset-1' : ''}`}>{part.text}</span> : part.text;
                  })}
                </span></span>;
              })}
            </div>
            {hover && !detailsOpen && <p role="tooltip" className="mt-2 text-[11px] text-muted-foreground">{metadata(hover)}</p>}
            {detailsOpen && target && <div className="mt-4 border-t border-border/60 pt-2" aria-label="Transcript selection details" onKeyDown={(event) => { if (event.key === 'Escape') { event.stopPropagation(); setDetailsOpen(false); restoreReadingFocus(); } }}>
              <p className="text-[11px] text-muted-foreground">{metadata(target)}</p>
              {occurrences.length > 1 && <label className="mt-2 flex min-w-0 flex-col gap-1 text-xs">Clip occurrence<select className={select} value={occurrence?.id ?? ''} onChange={(event) => setSelection({ assetId: target.source.assetId, sourceId: target.source.sourceId, occurrenceId: event.target.value })}>{occurrences.map((item, index) => <option key={item.id} value={item.id}>{mediaLabel(item.assetId)} · Clip {index + 1} · {item.timelineStart.toFixed(2)}s</option>)}</select></label>}
              {!occurrences.length && <p className="mt-1 text-xs text-muted-foreground">No playable clip occurrence.</p>}
              <div className="mt-1 flex flex-wrap gap-1"><button type="button" className={button} disabled={!occurrence} onClick={() => seek(target)}>Seek {target.word ? 'word' : 'segment'}</button><button type="button" className={button} disabled={busy || !adapter.editText} onClick={() => startEdit(target)}>Edit {target.word ? 'word' : 'segment'}</button><button type="button" className={button} onClick={() => { setDetailsOpen(false); restoreReadingFocus(); }}>Dismiss details</button></div>
            </div>}
          </>}
          {activeEdit && edit && <form className="mt-3 space-y-2 border-t border-border/60 pt-3" onSubmit={(event) => { event.preventDefault(); void run(async () => {
            if (!adapter.editText) return;
            const result = await adapter.editText(edit);
            if (!result.ok) { setFallback(result.fallback ?? null); throw new Error(result.message); }
            setEdit(null); setFallback(null); setMessage(documentId ? 'Project transcript saved.' : 'Timeline correction applied; save the timeline to keep it.'); restoreReadingFocus();
          }); }} onKeyDown={(event) => { event.stopPropagation(); if (event.key === 'Escape') { setEdit(null); setDetailsOpen(false); restoreReadingFocus(); } }}>
            <label className="flex flex-col gap-1 text-xs">{edit.type === 'word' ? 'Replacement word' : 'Replacement segment'}<textarea ref={editor} rows={3} className="w-full min-w-0 resize-y rounded-md border border-border bg-background p-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" value={edit.text} disabled={busy} onChange={(event) => {
              const next = { ...edit, text: event.target.value }; setEdit(next);
              if (next.text.trim()) { const result = adapter.stageTextDraft?.(next); if (result && !result.ok) setError(result.message); }
            }} /></label>
            {edit.type === 'segment' && <p className="text-xs text-muted-foreground">Replacing the segment retains its extent and clears word alignment.</p>}
            <div className="flex flex-wrap gap-1 pb-3"><button type="submit" className={`${button} bg-primary/10`} disabled={busy || !edit.text.trim()}>Save correction</button><button type="button" className={button} disabled={busy} onClick={() => void run(async () => {
              if (edit.documentId) { const result = await adapter.resolveSourceConflict?.(edit.documentId, 'discard'); if (result && !result.ok) throw new Error(result.message); }
              setEdit(null); setFallback(null); restoreReadingFocus();
            })}>Cancel correction</button>{fallback && <button type="button" className={button} onClick={() => { setEdit(fallback); setFallback(null); setError(''); }}>Replace whole segment instead</button>}</div>
          </form>}
        </div>
      </div>
    </>}
  </section>;
}
