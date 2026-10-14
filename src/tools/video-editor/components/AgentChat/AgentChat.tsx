import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronDown, ChevronUp, Loader2, Mic, Send, Square, X } from 'lucide-react';
import type { GenerationRow } from '@/domains/generation/types/index.ts';
import { MediaLightbox } from '@/domains/media-lightbox/MediaLightbox.tsx';
import { Button } from '@/shared/components/ui/button.tsx';
import { useAgentChatBridge, useAgentChatActionsRegistry, type AgentChatActionsHandlers } from '@/shared/contexts/AgentChatContext.tsx';
import { composerClearAttachments, composerRemoveAttachment } from '@/shared/state/selectionStore.ts';
import { useCurrentAttachmentSet } from '@/shared/state/currentAttachmentSet.ts';
import { usePanesStore } from '@/shared/state/panesStore.ts';
import {
  isTimelineAgentSessionsAvailable,
  useAgentSession,
  useAgentSessions,
  useProjectChat,
  useSaveProjectDraft,
  useSelectProjectSession,
  useUnassignedProjectSessions,
  useAssociateProjectSession,
  useCancelSession,
  useCreateSession,
  useSendMessage,
} from '@/tools/video-editor/hooks/useAgentSession.ts';
import { useAgentVoice } from '@/tools/video-editor/hooks/useAgentVoice.ts';
import { useRenderDiagnostic } from '@/tools/video-editor/hooks/usePerfDiagnostics.ts';
import { loadGenerationForLightbox } from '@/tools/video-editor/lib/generation-utils.ts';
import type {
  AgentSessionStatus,
  AgentTurn,
  AgentTurnAttachment,
} from '@/tools/video-editor/types/agent-session.ts';
import { AgentChatAttachmentStrip, AgentChatMessage, AgentChatToolGroup, type AgentChatAttachmentPreviewItem } from './AgentChatMessage.tsx';
import { useChatScroll } from './useChatScroll';
import { AgentTaskResults } from './AgentTaskResults';

export type ToolCallPair = {
  call: AgentTurn;
  result: AgentTurn | null;
};

export type RenderedTurn =
  | { kind: 'message'; key: string; turn: AgentTurn }
  | { kind: 'tool_group'; key: string; pairs: ToolCallPair[] };

type QueuedMessage = {
  id: string;
  text: string;
  sessionId: string;
  attachments: AgentTurnAttachment[];
};

type OptimisticMessage = QueuedMessage & {
  sentAtMs: number;
  priorTurnCount: number;
};

const unsavedProjectChatDrafts = new Map<string, { text: string; queue: QueuedMessage[]; dirty: boolean }>();

type AgentSessionView = {
  id: string;
  status: AgentSessionStatus;
  turns: AgentTurn[];
  assistantDraft?: string;
};

type AgentSessionOption = Pick<AgentSessionView, 'id' | 'status'>;



function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isAgentSessionStatus(value: unknown): value is AgentSessionStatus {
  switch (value) {
    case 'waiting_user':
    case 'processing':
    case 'continue':
    case 'done':
    case 'cancelled':
    case 'error':
      return true;
    default:
      return false;
  }
}

function isAgentTurn(value: unknown): value is AgentTurn {
  if (!isRecord(value) || typeof value.content !== 'string' || typeof value.timestamp !== 'string') {
    return false;
  }

  switch (value.role) {
    case 'user':
    case 'assistant':
    case 'tool_call':
    case 'tool_result':
      return true;
    default:
      return false;
  }
}

function isAgentSessionView(value: unknown): value is AgentSessionView {
  return isRecord(value)
    && typeof value.id === 'string'
    && isAgentSessionStatus(value.status)
    && Array.isArray(value.turns)
    && value.turns.every(isAgentTurn);
}

function isAgentSessionOption(value: unknown): value is AgentSessionOption {
  return isRecord(value)
    && typeof value.id === 'string'
    && isAgentSessionStatus(value.status);
}

function readAgentSessions(value: unknown): AgentSessionOption[] {
  return Array.isArray(value) ? value.filter(isAgentSessionOption) : [];
}

function readAgentSession(value: unknown): AgentSessionView | undefined {
  return isAgentSessionView(value) ? value : undefined;
}

function readSessionId(value: unknown): string | undefined {
  if (!isRecord(value)) return undefined;
  if (typeof value.id === 'string') return value.id;
  if (typeof value.sessionId === 'string') return value.sessionId;
  return undefined;
}

export function buildRenderedTurns(turns: AgentTurn[]): RenderedTurn[] {
  const items: RenderedTurn[] = [];
  let pendingToolPairs: ToolCallPair[] = [];
  let toolGroupStartIndex = 0;

  const flushToolGroup = () => {
    if (pendingToolPairs.length === 0) return;
    items.push({
      kind: 'tool_group',
      key: `tool-group:${toolGroupStartIndex}`,
      pairs: pendingToolPairs,
    });
    pendingToolPairs = [];
  };

  for (let index = 0; index < turns.length; index += 1) {
    const turn = turns[index];

    if (turn.role === 'tool_result') {
      continue;
    }

    if (turn.role === 'tool_call') {
      const nextTurn = turns[index + 1];
      const pairedResult = turn.tool_call_id
        ? turns.find(candidate => candidate.role === 'tool_result' && candidate.tool_call_id === turn.tool_call_id) ?? null
        : nextTurn?.role === 'tool_result' && !nextTurn.tool_call_id ? nextTurn : null;

      if (pendingToolPairs.length === 0) {
        toolGroupStartIndex = index;
      }
      pendingToolPairs.push({ call: turn, result: pairedResult });
      if (pairedResult === nextTurn) index += 1;
      continue;
    }

    flushToolGroup();

    // Skip assistant messages that duplicate a preceding message_user result
    if (turn.role === 'assistant' && items.length > 0) {
      const prev = items[items.length - 1];
      if (prev.kind === 'message' && prev.turn.content === turn.content) {
        continue;
      }
    }

    items.push({
      kind: 'message',
      key: `${turn.timestamp}:${turn.role}:${index}`,
      turn,
    });
  }

  flushToolGroup();
  return items;
}

function createMessageId() {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`;
}

function getTurnTimestampMs(turn: AgentTurn) {
  const timestampMs = Date.parse(turn.timestamp);
  return Number.isNaN(timestampMs) ? 0 : timestampMs;
}

interface AgentChatPanelProps {
  /** Whether chat currently fills the action pane vertically. */
  isExpanded?: boolean;
}

export function AgentChatPanel({ isExpanded = false }: AgentChatPanelProps) {
  useRenderDiagnostic('AgentChatPanel');
  const scope = useAgentChatBridge();

  if (!isTimelineAgentSessionsAvailable()) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
        <img
          src="/astrid-avatar.png"
          alt=""
          aria-hidden="true"
          className="h-8 w-8 rounded-full object-cover"
        />
        <p className="text-sm font-medium text-foreground">Timeline agent chat is managed in Astrid</p>
        <p className="max-w-sm text-xs text-muted-foreground">
          Run the agent workflow in Astrid, then refresh this editor to load the updated timeline.
        </p>
      </div>
    );
  }

  return <AvailableAgentChatPanel key={scope.editorContext?.projectId ?? 'unscoped'} isExpanded={isExpanded} />;
}

function AvailableAgentChatPanel({ isExpanded }: { isExpanded: boolean }) {

  const {
    timelineId,
    editorContext,
    pendingComposerPrompt,
    clearPendingComposerPrompt,
  } = useAgentChatBridge();
  const projectId = editorContext?.projectId ?? null;
  const sessions = useAgentSessions(timelineId, projectId);
  const projectChat = useProjectChat(projectId);
  const saveDraft = useSaveProjectDraft(projectId);
  const selectSession = useSelectProjectSession(projectId);
  const [showAttachSessions, setShowAttachSessions] = useState(false);
  const unassignedSessions = useUnassignedProjectSessions(projectId, showAttachSessions);
  const associateSession = useAssociateProjectSession(projectId);
  const createSession = useCreateSession(timelineId, projectId);
  const createNewSession = useCreateSession(timelineId, projectId, 'new');
  // Engagement signal: when the pane is locked the user has clearly committed to
  // having chat visible, so auto-create can fire without an explicit click.
  const isTasksPaneLocked = usePanesStore((state) => state.isTasksPaneLocked);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [draft, setDraft] = useState('');
  const [draftSaveError, setDraftSaveError] = useState<string | null>(null);
  const [queue, setQueue] = useState<QueuedMessage[]>([]);
  const [pausedQueueHeadId, setPausedQueueHeadId] = useState<string | null>(null);
  const pausedQueuedIdsRef = useRef(new Set<string>());
  const [optimisticMessage, setOptimisticMessage] = useState<OptimisticMessage | null>(null);
  const [attachmentLightboxMedia, setAttachmentLightboxMedia] = useState<GenerationRow | null>(null);
  // Engagement flag local to AgentChatPanel: flipped by markEngaged() (split-button click)
  // and decoupled from pane open state so the close-path bug from the rev-4
  // setIsTasksPaneOpenProgrammatic approach can't recur.
  const [userEngaged, setUserEngaged] = useState(false);
  const hasAutoCreatedSessionRef = useRef(false);
  const autoCreateOperationIdRef = useRef<string | null>(null);
  const manualCreateOperationIdRef = useRef<string | null>(null);
  const lightboxRequestIdRef = useRef(0);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const hasProject = Boolean(projectId);

  useEffect(() => {
    if (!pendingComposerPrompt) return;
    setDraft(pendingComposerPrompt);
    clearPendingComposerPrompt?.();
    requestAnimationFrame(() => inputRef.current?.focus());
  }, [clearPendingComposerPrompt, pendingComposerPrompt]);

  const activeSession = useAgentSession(activeSessionId, projectId);
  // Non-editor hosts may still provide the legacy settings-backed timeline
  // bridge. Preserve that path with a timeline-only context while the loaded
  // editor supplies the full project/timeline snapshot above.
  const sendMessage = useSendMessage(activeSessionId, editorContext, projectId);
  const cancelSession = useCancelSession(activeSessionId);
  const sessionOptions = useMemo(() => readAgentSessions(sessions.data), [sessions.data]);
  const hydratedProjectDraftRef = useRef(false);
  const draftRevisionRef = useRef<number | null>(null);
  const draftSaveChainRef = useRef<Promise<unknown>>(Promise.resolve());
  useEffect(() => {
    if (!projectChat.data || hydratedProjectDraftRef.current) return;
    hydratedProjectDraftRef.current = true;
    draftRevisionRef.current = projectChat.data.draft.revision;
    const restored = projectChat.data.draft.queued_messages ?? [];
    const savedQueue = restored.map((item) => ({ id: item.id, text: item.text, sessionId: item.session_id, attachments: Array.isArray(item.attachments) ? item.attachments as AgentTurnAttachment[] : [] }));
    const local = unsavedProjectChatDrafts.get(projectId!);
    if (local?.dirty) {
      setDraft(local.text);
      setQueue(local.queue);
      local.queue.forEach(item => pausedQueuedIdsRef.current.add(item.id));
      setPausedQueueHeadId(local.queue[0]?.id ?? null);
    } else {
      setDraft(projectChat.data.draft.text);
      setQueue(savedQueue);
      savedQueue.forEach(item => pausedQueuedIdsRef.current.add(item.id));
      setPausedQueueHeadId(savedQueue[0]?.id ?? null);
    }
  }, [projectChat.data, projectId]);
  const draftSnapshotRef = useRef({ text: draft, queue });
  draftSnapshotRef.current = { text: draft, queue };
  const flushDraftRef = useRef<() => Promise<void>>(async () => undefined);
  flushDraftRef.current = async () => {
    if (!projectId || !hydratedProjectDraftRef.current || draftRevisionRef.current === null) return;
    const snapshot = draftSnapshotRef.current;
    const queuePayload = snapshot.queue.map((item) => ({ id: item.id, text: item.text, session_id: item.sessionId, attachments: item.attachments }));
    draftSaveChainRef.current = draftSaveChainRef.current.catch(() => undefined).then(async () => {
      try {
        const result = await saveDraft.mutateAsync({ expectedRevision: draftRevisionRef.current!, text: snapshot.text, queuedMessages: queuePayload });
        draftRevisionRef.current = result.draft.revision;
        setDraftSaveError(null);
        const current = unsavedProjectChatDrafts.get(projectId);
        if (current && current.text === snapshot.text && JSON.stringify(current.queue) === JSON.stringify(snapshot.queue)) {
          unsavedProjectChatDrafts.set(projectId, { ...current, dirty: false });
        }
      } catch (error) {
        setDraftSaveError(error instanceof Error ? error.message : String(error));
        throw error;
      }
    });
    await draftSaveChainRef.current;
  };
  useEffect(() => {
    if (!projectId || !hydratedProjectDraftRef.current) return;
    const timer = window.setTimeout(() => { void flushDraftRef.current().catch(() => undefined); }, 350);
    return () => window.clearTimeout(timer);
  }, [projectId, draft, queue]);
  useEffect(() => {
    if (!projectId || !hydratedProjectDraftRef.current) return;
    unsavedProjectChatDrafts.set(projectId, { text: draft, queue, dirty: true });
  }, [projectId, draft, queue]);
  useEffect(() => () => { void flushDraftRef.current().catch(() => undefined); }, []);
  const restoreSavedDraft = useCallback(async () => {
    const result = await projectChat.refetch();
    if (!result.data) return;
    draftRevisionRef.current = result.data.draft.revision;
    setDraft(result.data.draft.text);
    setQueue((result.data.draft.queued_messages ?? []).map((item) => ({ id: item.id, text: item.text, sessionId: item.session_id, attachments: Array.isArray(item.attachments) ? item.attachments as AgentTurnAttachment[] : [] })));
    unsavedProjectChatDrafts.set(projectId!, { text: result.data.draft.text, queue: (result.data.draft.queued_messages ?? []).map((item) => ({ id: item.id, text: item.text, sessionId: item.session_id, attachments: Array.isArray(item.attachments) ? item.attachments as AgentTurnAttachment[] : [] })), dirty: false });
    setDraftSaveError(null);
  }, [projectChat, projectId]);
  const overwriteSavedDraft = useCallback(async () => {
    const result = await projectChat.refetch();
    if (!result.data) return;
    draftRevisionRef.current = result.data.draft.revision;
    setDraftSaveError(null);
    await flushDraftRef.current();
  }, [projectChat]);
  const activeSessionData = readAgentSession(activeSession.data);
  useEffect(() => {
    const selected = projectChat.data?.selected_session_id;
    if (!selected) return;
    setActiveSessionId(selected);
  }, [projectChat.data?.selected_session_id]);
  const { scrollContainerRef, scrollContentRef, onScroll } = useChatScroll(
    activeSessionId,
    !activeSession.isLoading && activeSessionId !== null && activeSessionData?.id === activeSessionId,
    activeSessionData?.turns.length ?? 0,
  );
  const { clips, summary } = useCurrentAttachmentSet();

  const voice = useAgentVoice({
    onTranscription: (text) => {
      if (isPanelMountedRef.current) void handleSend(text);
    },
  });
  // Stable ref so registered handlers always invoke the current voice closure
  // without re-registering when useVoiceRecording returns new function identities.
  const voiceRef = useRef(voice);
  voiceRef.current = voice;
  const isPanelMountedRef = useRef(true);
  useEffect(() => {
    isPanelMountedRef.current = true;
    return () => {
      isPanelMountedRef.current = false;
      voiceRef.current.cancelRecording();
    };
  }, []);

  const renderedTurns = useMemo(
    () => buildRenderedTurns(activeSessionData?.turns ?? []),
    [activeSessionData?.turns],
  );
  const activeStatus = activeSessionData?.status;
  const isCancelled = activeStatus === 'cancelled';
  const isProcessing = activeStatus === 'processing' || activeStatus === 'continue';
  const showKillSwitch = activeStatus === 'processing' || activeStatus === 'continue';
  const showNoProjectState = !hasProject && sessionOptions.length === 0;
  const hasQueuedMessages = queue.some((item) => item.sessionId === activeSessionId);
  const activeQueue = queue.filter((item) => item.sessionId === activeSessionId);
  const inputPlaceholder = showNoProjectState
    ? 'Select a project to start chatting...'
    : voice.isRecording
      ? 'Recording...'
      : (isProcessing || sendMessage.isPending || hasQueuedMessages)
        ? 'Type to queue next message...'
        : 'Type or press Cmd+Shift+R to talk...';
  const optimisticTurnAlreadyMaterialized = optimisticMessage !== null
    && Boolean(activeSessionData?.turns.some((turn) => turn.role === 'user' && turn.content === optimisticMessage.text));

  const handleAttachmentPreviewClick = useCallback(async (attachment: AgentChatAttachmentPreviewItem) => {
    if (!attachment.generationId) {
      return;
    }

    const requestId = lightboxRequestIdRef.current + 1;
    lightboxRequestIdRef.current = requestId;
    setAttachmentLightboxMedia(null);

    try {
      const media = await loadGenerationForLightbox(attachment.generationId);
      if (lightboxRequestIdRef.current !== requestId) {
        return;
      }

      setAttachmentLightboxMedia(media);
    } catch (error) {
      if (lightboxRequestIdRef.current === requestId) {
        setAttachmentLightboxMedia(null);
      }
      console.warn('[AgentChat] Failed to open attachment lightbox', error);
    }
  }, []);

  const handleCloseAttachmentLightbox = useCallback(() => {
    lightboxRequestIdRef.current += 1;
    setAttachmentLightboxMedia(null);
  }, []);

  const handleRemoveAttachment = useCallback((attachment: AgentChatAttachmentPreviewItem) => {
    composerRemoveAttachment({
      url: attachment.url,
      mediaType: attachment.mediaType,
      generationId: attachment.generationId,
      clipId: attachment.clipId,
    });
  }, []);

  const handleRemoveShot = useCallback((shotId: string) => {
    clips
      .filter((clip) => clip.shotId === shotId)
      .forEach((clip) => composerRemoveAttachment({
        url: clip.url,
        mediaType: clip.mediaType,
        generationId: clip.generationId,
        clipId: clip.clipId,
      }));
  }, [clips]);

  const moveQueuedMessageUp = useCallback((index: number) => {
    if (index <= 0) {
      return;
    }

    setQueue((prev) => {
      if (index >= prev.length) {
        return prev;
      }
      const previous = prev[index];
      let siblingIndex = index - 1;
      while (siblingIndex >= 0 && prev[siblingIndex].sessionId !== previous.sessionId) siblingIndex -= 1;
      if (siblingIndex < 0) return prev;
      const next = [...prev];
      [next[siblingIndex], next[index]] = [next[index], next[siblingIndex]];
      return next;
    });
  }, []);

  const moveQueuedMessageDown = useCallback((index: number) => {
    setQueue((prev) => {
      if (index < 0 || index >= prev.length - 1) {
        return prev;
      }
      const current = prev[index];
      let siblingIndex = index + 1;
      while (siblingIndex < prev.length && prev[siblingIndex].sessionId !== current.sessionId) siblingIndex += 1;
      if (siblingIndex >= prev.length) return prev;
      const next = [...prev];
      [next[index], next[siblingIndex]] = [next[siblingIndex], next[index]];
      return next;
    });
  }, []);

  const removeQueuedMessage = useCallback((id: string) => {
    pausedQueuedIdsRef.current.delete(id);
    if (pausedQueueHeadId === id) {
      setPausedQueueHeadId(null);
    }
    setQueue((prev) => prev.filter((item) => item.id !== id));
  }, [pausedQueueHeadId]);

  // Auto-select session — always picks the latest non-cancelled session if available.
  useEffect(() => {
    const persistedSelection = projectChat.data?.selected_session_id;
    if (persistedSelection && sessionOptions.some((session) => session.id === persistedSelection)) {
      setActiveSessionId(persistedSelection);
      return;
    }
    if (!sessionOptions.length) {
      setActiveSessionId(null);
      return;
    }

    setActiveSessionId((current) => {
      const currentSession = current
        ? sessionOptions.find((session) => session.id === current) ?? null
        : null;
      if (currentSession && currentSession.status !== 'cancelled') {
        return current;
      }

      const preferredSession = sessionOptions.find((session) => session.status !== 'cancelled');
      if (preferredSession) {
        return preferredSession.id;
      }

      if (currentSession) {
        return currentSession.id;
      }

      return sessionOptions[0]?.id ?? null;
    });
  }, [projectChat.data?.selected_session_id, sessionOptions]);

  // Auto-create session — gated on user engagement, never on mount alone.
  // Engagement signals: pane locked, voice activity, or markEngaged() called via
  // the split message button. Decoupled from pane open state per plan_v5 Option C.
  const isEngaged = userEngaged || isTasksPaneLocked || voice.isRecording || voice.isProcessing;
  useEffect(() => {
    if (
      hasAutoCreatedSessionRef.current
      || sessions.isLoading
      || sessions.isError
      || createSession.isPending
      || sessionOptions.length > 0
      || !hasProject
      || !isEngaged
    ) {
      return;
    }

    hasAutoCreatedSessionRef.current = true;
    autoCreateOperationIdRef.current ??= createMessageId();
    createSession.mutate(autoCreateOperationIdRef.current, {
      onError: () => { /* Retain the operation ID; recovery requires an explicit retry. */ },
      onSuccess: (session) => {
        autoCreateOperationIdRef.current = null;
        const sessionId = readSessionId(session);
        if (sessionId) setActiveSessionId(sessionId);
      },
    });
  }, [createSession, hasProject, sessionOptions.length, sessions.isError, sessions.isLoading, isEngaged]);

  // Cmd+Shift+R global shortcut — kept verbatim per plan_v5 Step 4.7.
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'r') {
        event.preventDefault();
        if (!hasProject) {
          return;
        }
        if (voice.isRecording) {
          voice.stopRecording();
        } else if (!voice.isProcessing) {
          voice.startRecording();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [hasProject, voice]);

  useEffect(() => {
    sendingRef.current = false;
    setPausedQueueHeadId(draftSnapshotRef.current.queue.find(item => item.sessionId === activeSessionId)?.id ?? null);
    setOptimisticMessage(null);
  }, [activeSessionId]);

  useEffect(() => {
    if (pausedQueueHeadId && !queue.some((item) => item.id === pausedQueueHeadId)) {
      setPausedQueueHeadId(null);
    }
  }, [pausedQueueHeadId, queue]);

  // Clear optimistic message only when the matching turn appears in real data
  useEffect(() => {
    if (!optimisticMessage || !activeSessionData?.turns) return;
    if (activeSessionData.turns.length <= optimisticMessage.priorTurnCount) return;

    const hasRealTurn = activeSessionData.turns.some((turn, index) => (
      index >= optimisticMessage.priorTurnCount
      && turn.role === 'user'
      && turn.content === optimisticMessage.text
      && getTurnTimestampMs(turn) >= optimisticMessage.sentAtMs - 1000
    ));

    if (hasRealTurn) {
      setOptimisticMessage(null);
    }
  }, [activeSessionData?.turns, optimisticMessage]);

  const sendingRef = useRef(false);
  const currentSessionRef = useRef(activeSessionId);
  currentSessionRef.current = activeSessionId;
  const currentContextRef = useRef(editorContext);
  currentContextRef.current = editorContext;
  const sendNow = useCallback(async (item: QueuedMessage, retryCaptured = false) => {
    if (!activeSessionId || !projectId || !editorContext || item.sessionId !== activeSessionId) {
      return;
    }

    const isCurrent = () => isPanelMountedRef.current && currentSessionRef.current === item.sessionId
      && currentContextRef.current?.projectId === projectId && currentContextRef.current?.timelineId === editorContext.timelineId;
    const priorTurnCount = activeSessionData?.turns.length ?? 0;
    const sentAtMs = Date.now();

    sendingRef.current = true;
    pausedQueuedIdsRef.current.add(item.id);
    // Persist the exact captured submission before an ownership lookup or ACP
    // dispatch can fail. A reopened panel pauses this durable head for retry.
    const retainedQueue = draftSnapshotRef.current.queue.some(row => row.id === item.id)
      ? draftSnapshotRef.current.queue : [...draftSnapshotRef.current.queue, item];
    draftSnapshotRef.current = { text: draftSnapshotRef.current.text, queue: retainedQueue };
    setQueue(retainedQueue);
    setOptimisticMessage({
      id: item.id,
      sessionId: item.sessionId,
      text: item.text,
      attachments: item.attachments,
      sentAtMs,
      priorTurnCount,
    });

    try {
      await flushDraftRef.current();
      if (!isCurrent()) return;
      if (retryCaptured) await sendMessage.retryLastMessage();
      else await sendMessage.mutateAsync({
        input: { message: item.text, attachments: item.attachments },
        projectId,
        sessionId: item.sessionId,
        context: editorContext,
      });
      if (!isCurrent()) return;
      pausedQueuedIdsRef.current.delete(item.id);
      const remaining = draftSnapshotRef.current.queue.filter(row => row.id !== item.id);
      draftSnapshotRef.current = { ...draftSnapshotRef.current, queue: remaining };
      setQueue(remaining);
      setPausedQueueHeadId(prev => prev === item.id ? null : prev);
      setOptimisticMessage(prev => prev?.id === item.id ? null : prev);
      await flushDraftRef.current();
    } catch (error) {
      if (!isCurrent()) return;
      setPausedQueueHeadId(item.id);
      setOptimisticMessage((prev) => (prev && prev.id === item.id ? null : prev));
      throw error;
    } finally {
      if (isCurrent()) sendingRef.current = false;
    }
  }, [activeSessionData?.turns.length, activeSessionId, editorContext, projectId, sendMessage]);

  const handleSend = useCallback(async (rawText?: string) => {
    const text = (rawText ?? draft).trim();
    if (!text || !activeSessionId || !hasProject) return;

    const attachments: AgentTurnAttachment[] = clips.map((clip) => ({
      clipId: clip.clipId,
      url: clip.url,
      mediaType: clip.mediaType,
      isTimelineBacked: clip.isTimelineBacked,
      generationId: clip.generationId,
      variantId: clip.variantId,
      shotId: clip.shotId,
      shotName: clip.shotName,
      shotSelectionClipCount: clip.shotSelectionClipCount,
      trackId: clip.trackId,
      at: clip.at,
      duration: clip.duration,
    }));

    if (rawText === undefined) {
      setDraft('');
      draftSnapshotRef.current = { ...draftSnapshotRef.current, text: '' };
    }
    const item: QueuedMessage = {
      id: createMessageId(),
      text,
      sessionId: activeSessionId,
      attachments,
    };
    composerClearAttachments();

    if (
      sendingRef.current
      || isProcessing
      || sendMessage.isPending
      || optimisticMessage
      || queue.some((item) => item.sessionId === activeSessionId)
    ) {
      setQueue((prev) => [...prev, item]);
      return;
    }

    try { await sendNow(item); } catch {
      // The durable queue and visible recovery retain the failed submission.
    }
  }, [activeSessionId, clips, draft, hasProject, isProcessing, optimisticMessage, queue, sendMessage.isPending, sendNow]);

  useEffect(() => {
    if (
      sendingRef.current
      || isProcessing
      || sendMessage.isPending
      || optimisticMessage
      || queue.length === 0
      || !activeSessionId
      || !projectId
    ) {
      return;
    }

    const next = queue.find((item) => item.sessionId === activeSessionId);
    if (!next || next.id === pausedQueueHeadId || pausedQueuedIdsRef.current.has(next.id)) {
      return;
    }

    void (async () => {
      try {
        await sendNow(next);
        setQueue((prev) => prev.filter((item) => item.id !== next.id));
      } catch {
        // Leave the failed head in place; pausedQueueHeadId will prevent further drains.
      }
    })();
  }, [queue, pausedQueueHeadId, isProcessing, sendMessage.isPending, optimisticMessage, activeSessionId, projectId, sendNow]);

  const handleNewSession = useCallback(async () => {
    if (!hasProject) {
      return;
    }
    setPausedQueueHeadId(null);
    setOptimisticMessage(null);
    manualCreateOperationIdRef.current ??= createMessageId();
    const session = await createNewSession.mutateAsync(manualCreateOperationIdRef.current);
    manualCreateOperationIdRef.current = null;
    const sessionId = readSessionId(session);
    if (sessionId) setActiveSessionId(sessionId);
  }, [createNewSession, hasProject]);

  // ==========================================================================
  // Actions registry — exposes stable handlers the parent (TasksPane split
  // button) can invoke. Stable identity means the registration effect runs
  // exactly once per mount, even though `voice` re-renders. Reactive state is
  // published separately so the split button mic icon flips with recording.
  // ==========================================================================
  const actionsRegistry = useAgentChatActionsRegistry();
  const stableHandlers = useMemo<AgentChatActionsHandlers>(() => ({
    toggleRecording: () => {
      const v = voiceRef.current;
      if (v.isRecording) {
        v.stopRecording();
      } else if (!v.isProcessing) {
        v.startRecording();
      }
    },
    focusComposer: () => {
      inputRef.current?.focus();
    },
    markEngaged: () => {
      setUserEngaged(true);
    },
  }), []);

  useEffect(() => {
    actionsRegistry.registerHandlers(stableHandlers);
    actionsRegistry.publishState({
      isRecording: voice.isRecording,
      isProcessing: voice.isProcessing,
    });
    return () => actionsRegistry.unregister();
    // stableHandlers and actionsRegistry are both referentially stable, so this
    // effect runs exactly once per mount despite voice churn.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actionsRegistry, stableHandlers]);

  useEffect(() => {
    actionsRegistry.publishState({
      isRecording: voice.isRecording,
      isProcessing: voice.isProcessing,
    });
  }, [actionsRegistry, voice.isRecording, voice.isProcessing]);

  return (
    // No background of its own — sits on the parent pane's bg so the only
    // visible color change between halves is the divider line itself.
    <div className="flex h-full w-full flex-col overflow-hidden">
      {/* Header */}
      <div data-testid="agent-chat-header" className="flex min-w-0 items-center justify-between gap-2 border-b border-border/70 px-3 py-2">
        <div className="flex shrink-0 items-center gap-2">
          <span className="text-sm font-medium">Agent</span>
          {isProcessing && <Loader2 className="h-3.5 w-3.5 animate-spin text-muted-foreground" />}
        </div>
        <div className="flex min-w-0 shrink items-center justify-end gap-1">
          {sessionOptions.length > 1 && (
            <select
              aria-label="Project chat session"
              title="Choose chat session"
              className="h-7 w-[4.75rem] min-w-0 shrink truncate rounded-md border border-border bg-background px-1.5 text-xs"
              value={activeSessionId ?? ''}
              onChange={(event) => {
                const sessionId = event.currentTarget.value;
                if (!projectId || !projectChat.data || !sessionId) return;
                void selectSession.mutateAsync({ expectedRevision: projectChat.data.revision, sessionId }).then(() => setActiveSessionId(sessionId)).catch(() => undefined);
              }}
            >
              {sessionOptions.map((session, index) => <option key={session.id} value={session.id}>Chat {index + 1}</option>)}
            </select>
          )}
          {showKillSwitch && (
            <Button
              type="button"
              size="icon"
              variant="destructive"
              className="h-7 w-7"
              onClick={() => {
                setQueue([]);
                setPausedQueueHeadId(null);
                setOptimisticMessage(null);
                cancelSession.mutate();
              }}
              disabled={cancelSession.isPending}
              title="Stop agent"
            >
              <Square className="h-3.5 w-3.5" />
            </Button>
          )}
          {projectId && (
            <Button type="button" size="sm" variant="ghost" className="h-7 px-2 text-xs text-muted-foreground" onClick={() => setShowAttachSessions((open) => !open)}>
              {showAttachSessions ? 'Hide chats' : 'Attach existing'}
            </Button>
          )}
          <Button
            type="button"
            size="sm"
            variant="ghost"
            className="h-7 px-2 text-xs text-muted-foreground"
            onClick={() => void handleNewSession().catch(() => undefined)}
            disabled={createNewSession.isPending || !hasProject}
          >
            New
          </Button>
        </div>
      </div>
      {showAttachSessions && projectId && (
        <div className="border-b border-border/70 px-4 py-2" aria-label="Unassigned existing chats">
          <div className="flex max-h-28 flex-col gap-1 overflow-y-auto">
            {unassignedSessions.data?.map((session) => (
              <button
                key={session.id}
                type="button"
                className="truncate rounded px-2 py-1 text-left text-xs hover:bg-muted disabled:opacity-50"
                disabled={associateSession.isPending || !projectChat.data}
                onClick={() => {
                  if (!projectChat.data) return;
                  associateSession.mutate({ expectedRevision: projectChat.data.revision, sessionId: session.id }, {
                    onSuccess: (chat) => setActiveSessionId(chat.selected_session_id),
                  });
                }}
                title={session.title ?? session.id}
              >
                {session.title || session.id}
              </button>
            ))}
            {unassignedSessions.isLoading && <span className="px-2 py-1 text-xs text-muted-foreground">Loading sessions…</span>}
            {!unassignedSessions.isLoading && !unassignedSessions.data?.length && <span className="px-2 py-1 text-xs text-muted-foreground">No unassigned OMP sessions.</span>}
          </div>
        </div>
      )}
      {/* Messages */}
      <div ref={scrollContainerRef} onScroll={onScroll} className="flex-1 overflow-y-auto overscroll-contain px-4 py-3">
        {draftSaveError && (
          <div role="alert" className="mb-2 rounded-md border border-destructive/40 p-2 text-xs text-destructive">
            <p>Draft or queued messages could not be saved: {draftSaveError}</p>
            <div className="mt-1 flex gap-2">
              <button type="button" className="underline" onClick={() => void overwriteSavedDraft()}>Keep local and overwrite saved draft</button>
              <button type="button" className="underline" onClick={() => void restoreSavedDraft()}>Load saved draft</button>
            </div>
          </div>
        )}
        {activeSession.isLoading && (
          <div className="flex items-center gap-2 py-6 text-sm text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            Loading...
          </div>
        )}

        {!activeSession.isLoading && renderedTurns.length === 0 && !isProcessing && !sendMessage.isPending && (
          <div className="flex min-h-full flex-col items-center justify-center py-8 text-center text-sm text-muted-foreground">
            {sessions.isError ? (
              <>
                <p>Local Astrid chat is unavailable.</p>
                <p className="mt-1 text-xs">Start the Astrid ACP bridge, then reopen this pane.</p>
              </>
            ) : showNoProjectState ? (
              <>
                <p>Select a project to start chatting.</p>
                <p className="mt-1 text-xs">Open a project to create a conversation.</p>
              </>
            ) : (
              <>
                <p>✨ I can do almost anything</p>
                <p className="mt-1 text-xs">Press <kbd className="rounded border border-border px-1 py-0.5 text-[10px]">Cmd+Shift+R</kbd> to talk</p>
              </>
            )}
          </div>
        )}

        <div ref={scrollContentRef} className="flex flex-col gap-2.5">
          {renderedTurns.map((item) =>
            item.kind === 'message' ? (
              <AgentChatMessage
                key={item.key}
                turn={item.turn}
                onAttachmentClick={handleAttachmentPreviewClick}
              />
            ) : (
              <div key={item.key} className="space-y-2">
                {item.pairs.map((pair, index) => <div key={pair.call.tool_call_id ?? index} data-agent-tool-call-id={pair.call.tool_call_id}>
                  <AgentChatToolGroup pairs={[pair]} />
                  <AgentTaskResults refs={pair.result?.task_refs ?? pair.call.task_refs ?? []} projectId={projectId} />
                </div>)}
              </div>
            ),
          )}

          {optimisticMessage && !optimisticTurnAlreadyMaterialized && (
            <div className="flex w-full justify-end">
              <div className="max-w-[85%] rounded-2xl bg-primary px-4 py-2.5 text-sm leading-relaxed text-primary-foreground shadow-sm">
                <div>{optimisticMessage.text}</div>
                {optimisticMessage.attachments.length > 0 && (
                  <AgentChatAttachmentStrip
                    attachments={optimisticMessage.attachments}
                    isUser
                  />
                )}
              </div>
            </div>
          )}

          {(isProcessing || sendMessage.isPending || (hasQueuedMessages && !pausedQueueHeadId)) && (
            <div className="flex items-center gap-2 py-1 text-xs text-muted-foreground">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              Thinking...
            </div>
          )}
        </div>

      </div>

      {/* Input bar */}
      <div className="border-t border-border/70 px-3 py-3">
        {activeQueue.length > 0 && (
          <div className="mb-2 flex flex-col gap-2">
            {activeQueue.map((item, index) => (
              <div
                key={item.id}
                className="flex items-center gap-2 rounded-lg bg-muted/50 px-3 py-2 text-xs"
              >
                <div className="flex-1 text-foreground">
                  <div className="line-clamp-2 break-words leading-relaxed">{item.text}</div>
                </div>
                {item.attachments.length > 0 && (
                  <span className="shrink-0 rounded-full bg-background/80 px-2 py-0.5 text-[11px] text-muted-foreground">
                    {`📎 ${item.attachments.length}`}
                  </span>
                )}
                {item.id === pausedQueueHeadId && (
                  <button type="button" onClick={() => { void sendNow(item, sendMessage.hasCapturedMessage?.(item.sessionId, item.text) ?? false).catch(() => undefined); }}>
                    Retry saved message
                  </button>
                )}
                <Button
                  type="button"
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6 shrink-0"
                  disabled={index === 0}
                  onClick={() => moveQueuedMessageUp(queue.indexOf(item))}
                  title="Move queued message up"
                >
                  <ChevronUp className="h-3.5 w-3.5" />
                </Button>
                <Button
                  type="button"
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6 shrink-0"
                  disabled={index === activeQueue.length - 1}
                  onClick={() => moveQueuedMessageDown(queue.indexOf(item))}
                  title="Move queued message down"
                >
                  <ChevronDown className="h-3.5 w-3.5" />
                </Button>
                <Button
                  type="button"
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6 shrink-0"
                  onClick={() => removeQueuedMessage(item.id)}
                  title="Remove queued message"
                >
                  <X className="h-3.5 w-3.5" />
                </Button>
              </div>
            ))}
          </div>
        )}

        {clips.length > 0 && (
          <div className="mb-2 rounded-lg bg-muted/50 px-3 py-2 text-xs text-muted-foreground">
            <AgentChatAttachmentStrip
              attachments={clips}
              isUser={false}
              className="mt-0"
              onAttachmentClick={handleAttachmentPreviewClick}
              onRemoveAttachment={handleRemoveAttachment}
              onRemoveShot={handleRemoveShot}
              maxPreviewCount={null}
            />
            <div className="mt-2 flex items-center justify-between gap-2">
              <span>{summary}</span>
              {clips.length > 1 && (
                <Button
                  type="button"
                  size="sm"
                  variant="ghost"
                  className="h-6 px-2 text-xs text-muted-foreground hover:text-foreground"
                  onClick={() => {
                    // Clear both surfaces. Gallery is always available; the
                    // timeline-side replace is bridge-nullable when no
                    // VideoEditorProvider is mounted (e.g. /shots, /art routes).
                    composerClearAttachments();
                  }}
                >
                  Clear
                </Button>
              )}
            </div>
          </div>
        )}

        {voice.isRecording && (
          <div className="mb-2 flex items-center justify-between rounded-lg bg-red-500/10 px-3 py-2 text-sm">
            <div className="flex items-center gap-2 text-red-400">
              <span className="inline-flex h-2 w-2 animate-pulse rounded-full bg-red-500" />
              Recording... {voice.remainingSeconds}s
            </div>
            <Button
              type="button"
              size="sm"
              variant="ghost"
              className="h-7 px-2 text-xs text-red-400 hover:text-red-300"
              onClick={() => voice.stopRecording()}
            >
              Done
            </Button>
          </div>
        )}

        {voice.isProcessing && (
          <div className="mb-2 flex items-center gap-2 rounded-lg bg-muted/50 px-3 py-2 text-xs text-muted-foreground">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            Transcribing...
          </div>
        )}

        {!isProcessing && !sendMessage.isPending && isCancelled && (
          <div className="mb-2 rounded-lg border border-border/70 bg-muted/40 px-3 py-2 text-xs text-muted-foreground">
            Session stopped. Start a new conversation to continue.
          </div>
        )}

        {!isProcessing && !sendMessage.isPending && !isCancelled && (activeSession.error || sendMessage.localError || createSession.error || createNewSession.error || sessions.error || projectChat.error || activeStatus === 'error') && (
          <div role="alert" className="mb-2 rounded-lg border border-destructive/40 bg-destructive/10 px-3 py-2 text-xs text-destructive">
            {activeSession.error?.message ?? sendMessage.localError ?? createSession.error?.message ?? createNewSession.error?.message ?? sessions.error?.message ?? projectChat.error?.message ?? 'Agent error. Try again or start a new conversation.'}
            {(sessions.error || projectChat.error) && (
              <button type="button" className="ml-2 underline" disabled={sessions.isFetching || projectChat.isFetching}
                onClick={() => { void sessions.refetch(); void projectChat.refetch(); }}>
                Retry
              </button>
            )}
            {createSession.error && (
              <button type="button" className="ml-2 underline" disabled={createSession.isPending}
                onClick={() => createSession.mutate(autoCreateOperationIdRef.current ?? undefined)}>
                Retry
              </button>
            )}
            {activeSession.error && (
              <button type="button" aria-label="Retry saved chat" className="ml-2 underline" disabled={activeSession.isFetching} onClick={() => { void activeSession.refetch(); }}>
                Retry
              </button>
            )}
          </div>
        )}

        <div className="flex items-end gap-2">
          <div className="relative flex-1">
            <textarea
              ref={inputRef}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              rows={isExpanded ? 8 : 4}
              placeholder={inputPlaceholder}
              className="min-h-10 w-full resize-none rounded-xl border border-border/70 bg-card px-3 py-2 pr-12 text-sm leading-5 outline-none transition-colors placeholder:text-muted-foreground/70 focus:border-primary/50"
              disabled={!hasProject || !activeSessionId || isCancelled || voice.isRecording || voice.isProcessing}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault();
                  void handleSend();
                }
              }}
            />

            <div className="absolute inset-y-4 right-2 z-10 flex w-8 flex-col gap-2">
              <div className="relative flex min-h-0 flex-1 items-center justify-center">
                <Button
                  type="button"
                  size="icon"
                  variant="ghost"
                  className={voice.isRecording
                    ? 'relative h-full w-full rounded-xl bg-red-500 text-white transition-colors hover:bg-red-600'
                    : 'relative h-full w-full rounded-xl bg-muted/80 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground'}
                  onClick={() => voice.isRecording ? voice.stopRecording() : voice.startRecording()}
                  disabled={!hasProject || !activeSessionId || isCancelled || voice.isProcessing || sendMessage.isPending}
                  title={voice.isRecording ? 'Stop recording' : 'Voice input (Cmd+Shift+R)'}
                >
                  {voice.isRecording ? <Square className="h-3 w-3" /> : <Mic className="h-3.5 w-3.5" />}
                </Button>
                {voice.isRecording && (
                  <Button
                    type="button"
                    size="icon"
                    variant="ghost"
                    className="absolute -right-2 -top-2 h-5 w-5 rounded-full bg-muted hover:bg-destructive hover:text-destructive-foreground"
                    onClick={() => voice.cancelRecording()}
                    title="Cancel recording"
                  >
                    <X className="h-3 w-3" />
                  </Button>
                )}
              </div>

              <div className="flex min-h-0 flex-1 items-center justify-center">
                <Button
                  type="button"
                  size="icon"
                  variant="default"
                  className="h-full w-full rounded-xl"
                  onClick={() => void handleSend()}
                  disabled={!hasProject || !draft.trim() || !activeSessionId || isCancelled}
                  title="Send"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {attachmentLightboxMedia && (
        <MediaLightbox
          media={attachmentLightboxMedia}
          initialVariantId={attachmentLightboxMedia.primary_variant_id ?? undefined}
          onClose={handleCloseAttachmentLightbox}
          features={{ showDownload: true, showTaskDetails: true }}
        />
      )}
    </div>
  );
}
