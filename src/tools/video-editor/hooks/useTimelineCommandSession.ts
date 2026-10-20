import { useCallback, useEffect, useRef, useState, type MutableRefObject } from 'react';
import type { DataProvider, TimelineCommandBasis, TimelineHeadRevision } from '../data/DataProvider.ts';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { parseTimelineBundle } from '../data/typed/timelineBundle.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { projectGenericPatchPreview } from '../commands/genericPatchCapture.ts';
import { projectClipTrimPreview } from '../commands/clipTrimGesture.ts';
import type { TimelineConfig, AssetRegistry } from '../types/index.ts';
import { createTimelineCommandSession, type CommandSessionState, type TimelineCommandSession } from '../commands/commitSession.ts';
import type { UseTimelineCommitResult } from './useTimelineCommit.ts';
import type { TimelineStoreApi } from './timelineStore.ts';
import type { VideoEditorShotsHost } from '../runtime/ports.ts';
import { createSelectedParamPort, type SelectedParamCapture, type SelectedParamLiveBasis } from '../commands/selectedParamPort.ts';
import type { DocumentPin } from '@/integrations/runtime/timeline-commit-types.ts';

export function useTimelineCommandSession(options: {
  legacyClean: () => boolean;
  initialReadReady?: boolean;
  snapshotWriteBlockedRef: MutableRefObject<boolean>;
  provider: DataProvider;
  timelineId: string;
  commit: UseTimelineCommitResult;
  resolveAssetUrl: (file: string) => Promise<string>;
  loaded: TimelineData | undefined;
  configVersionRef: MutableRefObject<number>;
  headRevisionRef: MutableRefObject<TimelineHeadRevision | undefined>;
  lastSavedSignatureRef: MutableRefObject<string>;
  store: TimelineStoreApi;
  shots: VideoEditorShotsHost;
  paramReadClient?: Parameters<typeof createTimelineCommandSession>[0]['paramReadClient'];
  recoveryConfig?: ReturnType<typeof import('./useTimelineSave.draftConfig.ts').createRecoveryConfig>;
}) {
  const { provider, timelineId, snapshotWriteBlockedRef } = options;
  const latest = useRef(options);
  latest.current = options;
  const sessionRef = useRef<TimelineCommandSession | null>(null);
  const activeRef = useRef(false);
  const ownsHistoryRef = useRef(false);
  const readGenerationRef = useRef(0);
  const basisRef = useRef<SelectedParamLiveBasis>();
  const basisGenerationRef = useRef(0);
  const selectedParamPort = useRef(createSelectedParamPort(() => basisRef.current)).current;
  const selectedAuthorityCaptureRef = useRef<SelectedParamCapture>();
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<CommandSessionState>({ status: 'loading', error: null,
    ownerId: null, recoverableOwners: [], canUndo: false });
  const initialReadReady = options.initialReadReady ?? true;
  const enabled = !!(provider.loadTimelineCommandBasis && provider.commitTimeline && provider.getRecoverableIdentity);
  const clearSelectedBasis = useCallback(() => {
    basisGenerationRef.current++;
    basisRef.current = undefined;
    selectedAuthorityCaptureRef.current = undefined;
  }, []);
  const publishSelectedBasis = useCallback((basis: TimelineCommandBasis) => {
    basisGenerationRef.current++;
    basisRef.current = {
      basis,
      head: { ...basis.head },
      generation: basisGenerationRef.current,
    };
  }, []);
  useEffect(() => {
    if (!enabled || !initialReadReady) return;
    clearSelectedBasis();
    let disposed = false;
    let session: TimelineCommandSession | undefined;
    let projectGeneration = 0;
    const initialData = latest.current.commit.dataRef.current;
    const initialHead = latest.current.headRevisionRef.current;
    const invalidateReads = () => { readGenerationRef.current++; };
    const disposeSession = () => {
      void session?.dispose().catch((error) => console.error('[TimelineCommandSession] Unsaved moves on close', error));
    };
    const changed = (next: CommandSessionState) => {
      if (disposed) return;
      activeRef.current = next.status !== 'saved' && (!!next.ownerId || next.recoverableOwners.length > 0);
      snapshotWriteBlockedRef.current = activeRef.current;
      if (activeRef.current || next.canUndo) ownsHistoryRef.current = true;
      setState(next);
    };
    void (async () => {
      const [identity, basis] = await Promise.all([
        provider.getRecoverableIdentity!(), provider.loadTimelineCommandBasis!(timelineId),
      ]);
      if (disposed) return;
      if (basis.canonicalDocument.timeline_id !== timelineId
        || !basis.head.revisionId || !basis.head.publicationId
        || basis.canonicalDocument.parent_revision.revision_id !== basis.head.revisionId
        || (initialHead?.timelineId === timelineId && initialHead.projectId !== basis.canonicalDocument.project_id)) {
        throw new Error('Initialization requires a verified closure in the current project and timeline');
      }
      publishSelectedBasis(basis);
      const project = async (accepted: TimelineCommandBasis, previews: TimelinePatch[], initial = false) => {
        if (disposed) return;
        clearSelectedBasis();
        const generation = initial ? projectGeneration : ++projectGeneration;
        const context = latest.current;
        const document = accepted.canonicalDocument;
        const parent = document.parent_revision.payload;
        let config = { ...(parent.config as TimelineConfig), clips: parent.clips as TimelineConfig['clips'] };
        let registry = parent.registry as AssetRegistry;
        let composition;
        if (Array.isArray(parent.occurrences) && parent.occurrences.length) {
          if (!accepted.graph || !provider.shotComposition) throw new Error('Accepted shot closure cannot be projected');
          composition = createShotCompositionAdapter(provider.shotComposition).prepare(accepted.graph);
          const projection = projectCanonicalComposition(composition);
          config = projection.config;
          registry = { assets: projection.config.registry };
        }
        const rawBundle = (parent.config as Record<string, unknown>).bundle;
        const source = rawBundle == null ? undefined : parseTimelineBundle(rawBundle);
        const head = { projectId: document.project_id, timelineId, headRevisionId: accepted.head.revisionId,
          headPublicationId: accepted.head.publicationId };
        const resolve = provider.resolveTimelineCommandAsset
          ? (file: string) => provider.resolveTimelineCommandAsset!(file, registry) : context.resolveAssetUrl;
        let data = await buildTimelineData(config, registry, resolve,
          context.configVersionRef.current + 1, source?.itemsBySchemaRef, head, source?.transcriptReferences);
        for (const preview of previews) {
          const trimmed = projectClipTrimPreview(preview, data);
          const native = trimmed ?? projectGenericPatchPreview(preview, data);
          const compiled = trimmed ? { valid: true, nextData: trimmed }
            : native ? { valid: true, nextData: native } : compileTimelinePatch(preview, data);
          if (!compiled.valid || !compiled.nextData) throw new Error('Recovered move preview is unavailable');
          data = compiled.nextData;
        }
        if (disposed || generation !== projectGeneration) return;
        // Bootstrap yields to any intervening display, head, local edit or recovery.
        if (initial && (context.commit.dataRef.current !== initialData || initialData?.editProjection
          || context.headRevisionRef.current !== initialHead || (initialHead && initialHead.timelineId !== timelineId)
          || !latest.current.legacyClean())) return;
        publishSelectedBasis(accepted);
        data.editProjection = accepted.head.revisionId && accepted.head.publicationId
          ? previews.length ? { kind: 'local', base: { ...accepted.head }, generation }
            : { kind: 'accepted', head: { ...accepted.head } } : undefined;
        context.configVersionRef.current = data.configVersion;
        context.headRevisionRef.current = head;
        context.recoveryConfig?.remember(head, parent.config, composition);
        context.store.getState().setConfigVersion(data.configVersion);
        context.commit.commitData(data, { save: false, skipHistory: true, updateLastSavedSignature: previews.length === 0 });
        if (composition && !previews.length) context.shots.adoptCanonicalComposition?.(composition);
      };
      session = await createTimelineCommandSession({
        scope: { ...identity, projectId: basis.canonicalDocument.project_id, timelineId }, initial: basis,
        paramReadClient: latest.current.paramReadClient,
        loadLatest: async () => {
          if (disposed) throw new Error('Timeline command session is closed');
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before resolving commands');
          projectGeneration++;
          invalidateReads();
          clearSelectedBasis();
          const fresh = await provider.loadTimelineCommandBasis!(timelineId);
          invalidateReads();
          if (disposed) throw new Error('Timeline command session is closed');
          publishSelectedBasis(fresh);
          return fresh;
        },
        send: (request, key) => provider.commitTimeline!(request, key),
        changed,
        preview: (patch) => {
          if (disposed) throw new Error('Timeline command session is closed');
          const { commit } = latest.current;
          if (!commit.dataRef.current) throw new Error('Timeline is not loaded');
          const trimmed = projectClipTrimPreview(patch, commit.dataRef.current);
          const native = trimmed ?? projectGenericPatchPreview(patch, commit.dataRef.current);
          const compiled = trimmed ? { valid: true, nextData: trimmed }
            : native ? { valid: true, nextData: native } : compileTimelinePatch(patch, commit.dataRef.current);
          if (!compiled.valid || !compiled.nextData) throw new Error('Move preview is unavailable');
          projectGeneration++;
          ownsHistoryRef.current = true;
          const current = commit.dataRef.current;
          const base = current.editProjection?.kind === 'local' ? current.editProjection.base
            : current.head?.headRevisionId && current.head.headPublicationId
              ? { revisionId: current.head.headRevisionId, publicationId: current.head.headPublicationId } : undefined;
          compiled.nextData.editProjection = base ? { kind: 'local', base, generation: projectGeneration } : undefined;
          commit.commitData(compiled.nextData, { save: false, skipHistory: true });
        },
        project,
      });
      if (disposed) disposeSession();
      else {
        const head = latest.current.headRevisionRef.current;
        if (latest.current.commit.dataRef.current === initialData && head === initialHead
          && head?.projectId === basis.canonicalDocument.project_id && head.timelineId === timelineId
          && head.headRevisionId === basis.head.revisionId && head.headPublicationId === basis.head.publicationId) {
          latest.current.recoveryConfig?.remember(head, basis.canonicalDocument.parent_revision.payload.config,
            basis.graph && provider.shotComposition ? createShotCompositionAdapter(provider.shotComposition).prepare(basis.graph) : undefined);
        }
        // A retained outbox owns its original display basis until explicit recovery.
        if (session.getState().status === 'saved') await project(basis, [], true);
        if (disposed) return;
        const realPort = session.port;
        session.port = { ...realPort, capture: (input) => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before moving');
          return realPort.capture(input);
        } };
        const realClipParamsPort = session.clipParamsPort;
        session.clipParamsPort = {
          resolveAuthority(input) {
            const capture = selectedParamPort.capture(input);
            selectedAuthorityCaptureRef.current = capture;
            return selectedParamPort.resolve(capture);
          },
          capture(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing selected parameters');
            return realClipParamsPort.capture(input);
          },
          async prefetch(basis, pin) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before loading selected parameter schema');
            const authorityCapture = selectedAuthorityCaptureRef.current;
            if (!authorityCapture) throw new Error('Selected PARAM authority is unavailable; draft preserved');
            const currentPin = selectedParamPort.resolve(authorityCapture);
            if (JSON.stringify(currentPin) !== JSON.stringify(pin)) {
              throw new Error('Selected PARAM authority basis changed; draft preserved');
            }
            const result = await realClipParamsPort.prefetch!(basis, pin);
            selectedParamPort.resolve(authorityCapture);
            return result;
          },
          invalidatePrefetch() { realClipParamsPort.invalidatePrefetch?.(); },
          finish(basis, args) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing selected parameters');
            return realClipParamsPort.finish(basis, args);
          },
          submit(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing selected parameters');
            realClipParamsPort.submit(input);
          },
        };
        const realElementPort = session.elementPort;
        session.elementPort = {
          capture(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element');
            return realElementPort.capture(input);
          },
          finish(basis, edit) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element');
            return realElementPort.finish(basis, edit);
          },
          submit(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element');
            realElementPort.submit(input);
          },
        };
        const realElementOverlay = session.elementOverlay;
        session.elementOverlay = {
          capture(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element overlay');
            return realElementOverlay.capture(input);
          },
          finish(basis) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element overlay');
            return realElementOverlay.finish(basis);
          },
          submit(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element overlay');
            realElementOverlay.submit(input);
          },
        };
        const genericPatchPort = session.genericPatchPort;
        const requireCleanGenericPatch = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before applying a native patch');
        };
        session.genericPatchPort = {
          capture(input) { requireCleanGenericPatch(); return genericPatchPort.capture(input); },
          finish(basis) { requireCleanGenericPatch(); return genericPatchPort.finish(basis); },
          submit(input) { requireCleanGenericPatch(); genericPatchPort.submit(input); },
        };
        const parentClipAddMediaPort = session.parentClipAddMediaPort;
        const requireCleanParentClipAddMedia = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before adding prepared parent media');
        };
        session.parentClipAddMediaPort = {
          prepare() { requireCleanParentClipAddMedia(); return parentClipAddMediaPort.prepare(); },
          assertPreparationCurrent(preparation) {
            requireCleanParentClipAddMedia();
            parentClipAddMediaPort.assertPreparationCurrent(preparation);
          },
          capture(input) { requireCleanParentClipAddMedia(); return parentClipAddMediaPort.capture(input); },
          finish(basis, verifiedMedia) { requireCleanParentClipAddMedia(); return parentClipAddMediaPort.finish(basis, verifiedMedia); },
          submit(input) { requireCleanParentClipAddMedia(); parentClipAddMediaPort.submit(input); },
        };
        const parentClipSwapMediaPort = session.parentClipSwapMediaPort;
        const requireCleanParentClipSwapMedia = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before preparing parent media swap');
        };
        session.parentClipSwapMediaPort = {
          prepare() { requireCleanParentClipSwapMedia(); return parentClipSwapMediaPort.prepare(); },
          assertPreparationCurrent(preparation) {
            requireCleanParentClipSwapMedia();
            parentClipSwapMediaPort.assertPreparationCurrent(preparation);
          },
        };
        const occurrenceDuplicatePort = session.occurrenceDuplicatePort;
        const requireCleanDuplicate = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before duplicating a shot');
        };
        session.occurrenceDuplicatePort = {
          capture(input) { requireCleanDuplicate(); return occurrenceDuplicatePort.capture(input); },
          finish(basis) { requireCleanDuplicate(); return occurrenceDuplicatePort.finish(basis); },
          submit(input) { requireCleanDuplicate(); occurrenceDuplicatePort.submit(input); },
        };
        const labelPort = session.trackLabelPort;
        const requireCleanLabelEdit = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing a track label');
        };
        session.trackLabelPort = {
          capture(input) { requireCleanLabelEdit(); return labelPort.capture(input); },
          finish(basis, args) { requireCleanLabelEdit(); return labelPort.finish(basis, args); },
          submit(input) { requireCleanLabelEdit(); labelPort.submit(input); },
        };
        const shotSetPort = session.shotSetPort;
        session.shotSetPort = {
          capture(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing a shot name');
            return shotSetPort.capture(input);
          },
          finish(basis, args) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing a shot name');
            return shotSetPort.finish(basis, args);
          },
          submit(input) {
            if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing a shot name');
            return shotSetPort.submit(input);
          },
        };
        const scalarPort = session.clipScalarPort;
        const requireCleanScalarEdit = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing clip fields');
        };
        session.clipScalarPort = {
          capture(input) { requireCleanScalarEdit(); return scalarPort.capture(input); },
          finish(basis, args) { requireCleanScalarEdit(); return scalarPort.finish(basis, args); },
          submit(input) { requireCleanScalarEdit(); scalarPort.submit(input); },
          finishBatch(bases, args) { requireCleanScalarEdit(); return scalarPort.finishBatch!(bases, args); },
          submitBatch(input) { requireCleanScalarEdit(); scalarPort.submitBatch!(input); },
        };
        const trimPort = session.clipTrimPort;
        const requireCleanTrim = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before trimming');
        };
        session.clipTrimPort = {
          capture(input) { requireCleanTrim(); return trimPort.capture(input); },
          finish(basis, args) { requireCleanTrim(); return trimPort.finish(basis, args); },
          submit(input) { requireCleanTrim(); trimPort.submit(input); },
        };
        sessionRef.current = session;
        setState({ ...session.getState() });
      }
    })().catch((error) => {
      clearSelectedBasis();
      disposeSession();
      changed({ status: 'error', error: error instanceof Error ? error.message : String(error),
        ownerId: null, recoverableOwners: [], canUndo: false });
    });
    return () => {
      disposed = true;
      invalidateReads();
      clearSelectedBasis();
      ownsHistoryRef.current = false;
      projectGeneration++;
      sessionRef.current = null;
      activeRef.current = false;
      snapshotWriteBlockedRef.current = false;
      disposeSession();
    };
  }, [clearSelectedBasis, initialReadReady, publishSelectedBasis, provider, selectedParamPort, timelineId, enabled, attempt, snapshotWriteBlockedRef]);
  useEffect(() => {
    if (!enabled || !options.loaded?.head || !sessionRef.current) return;
    clearSelectedBasis();
    let cancelled = false;
    const session = sessionRef.current;
    const generation = readGenerationRef.current;
    const priorHead = latest.current.headRevisionRef.current;
    void provider.loadTimelineCommandBasis!(timelineId).then((basis) => {
      if (cancelled || sessionRef.current !== session || generation !== readGenerationRef.current) return;
      const currentHead = latest.current.headRevisionRef.current;
      if (currentHead !== priorHead && (currentHead?.headRevisionId !== basis.head.revisionId
        || currentHead.headPublicationId !== basis.head.publicationId)) return;
      if (!cancelled) {
        if (currentHead?.projectId === basis.canonicalDocument.project_id && currentHead.timelineId === timelineId
          && basis.canonicalDocument.timeline_id === timelineId
          && currentHead.headRevisionId === basis.head.revisionId && currentHead.headPublicationId === basis.head.publicationId) {
          latest.current.recoveryConfig?.remember(currentHead, basis.canonicalDocument.parent_revision.payload.config,
            basis.graph && provider.shotComposition ? createShotCompositionAdapter(provider.shotComposition).prepare(basis.graph) : undefined);
        }
        publishSelectedBasis(basis);
        session.observe(basis);
      }
    }).catch((error) => {
      // A failed poll does not alter the retained command or its retry identity.
      if (!cancelled && sessionRef.current === session && generation === readGenerationRef.current) {
        setState((current) => ({ ...current, error: error instanceof Error ? error.message : String(error) }));
      }
    });
    return () => { cancelled = true; };
  }, [clearSelectedBasis, enabled, options.loaded, provider, publishSelectedBasis, timelineId, state.ownerId]);
  const requireSession = useCallback(() => {
    const session = sessionRef.current;
    if (!session) throw new Error(state.error ?? 'Timeline command session is not ready');
    return session;
  }, [state.error]);
  const retry = useCallback(async () => {
    if (sessionRef.current) await sessionRef.current.retry();
    else {
      setState((current) => ({ ...current, status: 'loading', error: null }));
      setAttempt((current) => current + 1);
    }
  }, []);
  const undo = useCallback(async () => { await requireSession().undo(); }, [requireSession]);
  const flush = useCallback(async () => { await requireSession().flush(); }, [requireSession]);
  const recover = useCallback(async (ownerId: string) => { await requireSession().recover(ownerId); }, [requireSession]);
  const resolve = useCallback(async (keep: boolean) => {
    const session = requireSession();
    readGenerationRef.current++;
    try { await (keep ? session.keepLabelChanges() : session.useLatest()); }
    finally { readGenerationRef.current++; }
  }, [requireSession]);
  const useLatest = useCallback(() => resolve(false), [resolve]);
  const keepLabelChanges = useCallback(() => resolve(true), [resolve]);
  const resolveSelectedParamAuthority = useCallback((input: {
    select: string;
    rawClip: Record<string, unknown> | null | undefined;
  }): DocumentPin => selectedParamPort.resolve(selectedParamPort.capture(input)), [selectedParamPort]);
  const resolveSelectedParamAuthorityAsync = useCallback(<T,>(
    input: { select: string; rawClip: Record<string, unknown> | null | undefined },
    resolveScope: (basis: SelectedParamLiveBasis) => Promise<T>,
  ): Promise<T> => {
    const capture = selectedParamPort.capture(input);
    return selectedParamPort.resolveAsync(capture, async () => resolveScope(capture.live));
  }, [selectedParamPort]);
  return { enabled, state, activeRef, ownsHistoryRef, port: sessionRef.current?.port,
    genericPatchPort: sessionRef.current?.genericPatchPort,
    elementPort: sessionRef.current?.elementPort,
    elementOverlay: sessionRef.current?.elementOverlay,
    trackLabelPort: sessionRef.current?.trackLabelPort, shotSetPort: sessionRef.current?.shotSetPort,
    clipScalarPort: sessionRef.current?.clipScalarPort,
    clipTrimPort: sessionRef.current?.clipTrimPort,
    clipParamsPort: sessionRef.current?.clipParamsPort,
    selectedParamPort, resolveSelectedParamAuthority, resolveSelectedParamAuthorityAsync,
    parentClipAddMediaPort: sessionRef.current?.parentClipAddMediaPort,
    parentClipSwapMediaPort: sessionRef.current?.parentClipSwapMediaPort,
    occurrenceDuplicatePort: sessionRef.current?.occurrenceDuplicatePort,
    retry, undo, flush, recover, useLatest, keepLabelChanges };
}
export type TimelineCommandSessionSurface = Pick<ReturnType<typeof useTimelineCommandSession>, 'state' | 'retry' | 'recover'>
  & Partial<Pick<ReturnType<typeof useTimelineCommandSession>, 'useLatest' | 'keepLabelChanges' | 'elementOverlay'>>;
