import { useCallback, useEffect, useRef, useState, type MutableRefObject } from 'react';
import type { DataProvider, TimelineHeadRevision } from '../data/DataProvider.ts';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { parseTimelineBundle } from '../data/typed/timelineBundle.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import type { TimelineConfig, AssetRegistry } from '../types/index.ts';
import { createTimelineCommandSession, type CommandSessionState, type TimelineCommandSession } from '../commands/commitSession.ts';
import type { UseTimelineCommitResult } from './useTimelineCommit.ts';
import type { TimelineStoreApi } from './timelineStore.ts';
import type { VideoEditorShotsHost } from '../runtime/ports.ts';
import { projectClipTrimPreview } from '../commands/clipTrimGesture.ts';

export function useTimelineCommandSession(options: {
  legacyClean: () => boolean;
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
  recoveryConfig?: ReturnType<typeof import('./useTimelineSave.draftConfig.ts').createRecoveryConfig>;
}) {
  const { provider, timelineId, snapshotWriteBlockedRef } = options;
  const latest = useRef(options);
  latest.current = options;
  const sessionRef = useRef<TimelineCommandSession | null>(null);
  const activeRef = useRef(false);
  const ownsHistoryRef = useRef(false);
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<CommandSessionState>({ status: 'loading', error: null,
    ownerId: null, recoverableOwners: [], canUndo: false });
  const enabled = !!(provider.loadTimelineCommandBasis && provider.commitTimeline && provider.getRecoverableIdentity);
  useEffect(() => {
    if (!enabled) return;
    let disposed = false;
    let session: TimelineCommandSession | undefined;
    let projectGeneration = 0;
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
      const head = latest.current.headRevisionRef.current;
      if (head?.projectId === basis.canonicalDocument.project_id && head.timelineId === timelineId
        && basis.canonicalDocument.timeline_id === timelineId
        && head.headRevisionId === basis.head.revisionId && head.headPublicationId === basis.head.publicationId) {
        latest.current.recoveryConfig?.remember(head, basis.canonicalDocument.parent_revision.payload.config);
      }
      session = await createTimelineCommandSession({
        scope: { ...identity, projectId: basis.canonicalDocument.project_id, timelineId }, initial: basis,
        send: (request, key) => provider.commitTimeline!(request, key),
        changed,
        preview: (patch) => {
          if (disposed) throw new Error('Timeline command session is closed');
          const { commit } = latest.current;
          if (!commit.dataRef.current) throw new Error('Timeline is not loaded');
          const trimmed = projectClipTrimPreview(patch, commit.dataRef.current);
          const compiled = trimmed ? { valid: true, nextData: trimmed } : compileTimelinePatch(patch, commit.dataRef.current);
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
        project: async (accepted, previews) => {
          if (disposed) return;
          const generation = ++projectGeneration;
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
            const compiled = trimmed ? { valid: true, nextData: trimmed } : compileTimelinePatch(preview, data);
            if (!compiled.valid || !compiled.nextData) throw new Error('Recovered move preview is unavailable');
            data = compiled.nextData;
          }
          if (disposed || generation !== projectGeneration) return;
          data.editProjection = accepted.head.revisionId && accepted.head.publicationId
            ? previews.length ? { kind: 'local', base: { ...accepted.head }, generation }
              : { kind: 'accepted', head: { ...accepted.head } } : undefined;
          context.configVersionRef.current = data.configVersion;
          context.headRevisionRef.current = head;
          context.recoveryConfig?.remember(head, parent.config);
          context.store.getState().setConfigVersion(data.configVersion);
          context.commit.commitData(data, { save: false, skipHistory: true, updateLastSavedSignature: previews.length === 0 });
          if (composition && !previews.length) context.shots.adoptCanonicalComposition?.(composition);
        },
      });
      if (disposed) disposeSession();
      else {
        const realPort = session.port;
        session.port = { ...realPort, capture: (input) => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before moving');
          return realPort.capture(input);
        } };
        const labelPort = session.trackLabelPort;
        const requireCleanLabelEdit = () => {
          if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing a track label');
        };
        session.trackLabelPort = {
          capture(input) { requireCleanLabelEdit(); return labelPort.capture(input); },
          finish(basis, args) { requireCleanLabelEdit(); return labelPort.finish(basis, args); },
          submit(input) { requireCleanLabelEdit(); labelPort.submit(input); },
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
    })().catch((error) => changed({ status: 'error', error: error instanceof Error ? error.message : String(error),
      ownerId: null, recoverableOwners: [], canUndo: false }));
    return () => {
      disposed = true;
      ownsHistoryRef.current = false;
      projectGeneration++;
      sessionRef.current = null;
      activeRef.current = false;
      snapshotWriteBlockedRef.current = false;
      disposeSession();
    };
  }, [provider, timelineId, enabled, attempt, snapshotWriteBlockedRef]);
  useEffect(() => {
    if (!enabled || !options.loaded?.head || !sessionRef.current) return;
    let cancelled = false;
    const priorHead = latest.current.headRevisionRef.current;
    void provider.loadTimelineCommandBasis!(timelineId).then((basis) => {
      const currentHead = latest.current.headRevisionRef.current;
      if (currentHead !== priorHead && (currentHead?.headRevisionId !== basis.head.revisionId
        || currentHead.headPublicationId !== basis.head.publicationId)) return;
      if (!cancelled) {
        if (currentHead?.projectId === basis.canonicalDocument.project_id && currentHead.timelineId === timelineId
          && basis.canonicalDocument.timeline_id === timelineId
          && currentHead.headRevisionId === basis.head.revisionId && currentHead.headPublicationId === basis.head.publicationId) {
          latest.current.recoveryConfig?.remember(currentHead, basis.canonicalDocument.parent_revision.payload.config);
        }
        sessionRef.current?.observe(basis);
      }
    }).catch((error) => {
      // A failed poll does not alter the retained command or its retry identity.
      if (!cancelled) setState((current) => ({ ...current, error: error instanceof Error ? error.message : String(error) }));
    });
    return () => { cancelled = true; };
  }, [enabled, options.loaded, provider, timelineId, state.ownerId]);
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
  return { enabled, state, activeRef, ownsHistoryRef, port: sessionRef.current?.port,
    trackLabelPort: sessionRef.current?.trackLabelPort,
    clipTrimPort: sessionRef.current?.clipTrimPort,
    retry, undo, flush, recover };
}
export type TimelineCommandSessionSurface = Pick<ReturnType<typeof useTimelineCommandSession>, 'state' | 'retry' | 'recover'>;
