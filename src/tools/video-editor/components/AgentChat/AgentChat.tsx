import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronDown, ChevronUp, Info, Loader2, Mic, Send, Square, X } from 'lucide-react';
import type { GenerationRow } from '@/domains/generation/types/index.ts';
import { EXTERNAL_AGENT_IDS, savedLocalAgentModel, sessionAgentId, type LocalAgentId } from '@/integrations/astrid/localAgents.ts';
import { isAcpUnavailable } from '@/integrations/astrid/acpRoutes.ts';
import { MediaLightbox } from '@/domains/media-lightbox/MediaLightbox.tsx';
import { Button } from '@/shared/components/ui/button.tsx';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/shared/components/ui/tooltip.tsx';
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
  useSetMainProjectSession,
  useRenameProjectSession,
  useUnassignedProjectSessions,
  useAssociateProjectSession,
  useCancelSession,
  useTakeOverSession,
  useCreateSession,
  useSendMessage,
  useAgentModels,
  useSetAgentModel,
  useLocalAgents,
  useSetLocalAgent,
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
import { AgentChatSessionSelector } from './AgentChatSessionSelector';
import { AgentChatNewChatButton, type NewChatAgentModels } from './AgentChatNewChatButton';
import { AgentIcon, agentNames } from './agentIdentity';
import { readAgentModels, readChatModels, rememberAgentModels, rememberChatModel } from './chatModelMemory';
import { ProjectChatDraftPersistence, sameProjectDraft } from './projectChatDraftPersistence';

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

const unsavedProjectChatDrafts = new Map<string, { text: string; queue: QueuedMessage[]; dirty: boolean; scopeKey: string; persistence: ProjectChatDraftPersistence<QueuedMessage> }>();
type AgentSessionView = {
  durableAcceptedRequestIds?: string[];
  recordedEditorResults?: import('../../runtime/editorRequestPresentation').RecordedEditorResult[];
  id: string;
  status: AgentSessionStatus;
  turns: AgentTurn[];
  assistantDraft?: string;
  control?: { role: 'writer' | 'follower'; active: boolean; activeRequestId: string | null };
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

interface AgentChatPanelProps {
  /** Whether chat currently fills the action pane vertically. */
  isExpanded?: boolean;
  /** Keep the containing action pane visible while the session selector portal is open. */
  onSessionSelectorOpenChange?: (open: boolean) => void;
}

/** What the pane says while no chat service runs on this computer (the door's `acp_unavailable`). */
const CHAT_UNAVAILABLE = "Chat isn't running on this computer right now.";

export function AgentChatPanel({ isExpanded = false, onSessionSelectorOpenChange }: AgentChatPanelProps) {
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

  return (
    <AvailableAgentChatPanel
      key={scope.editorContext?.projectId ?? 'unscoped'}
      isExpanded={isExpanded}
      onSessionSelectorOpenChange={onSessionSelectorOpenChange}
    />
  );
}

function AvailableAgentChatPanel({
  isExpanded,
  onSessionSelectorOpenChange,
}: {
  isExpanded: boolean;
  onSessionSelectorOpenChange?: (open: boolean) => void;
}) {

  const {
    timelineId,
    editorContext,
    pendingComposerPrompt,
    clearPendingComposerPrompt,
  } = useAgentChatBridge();
  const projectId = editorContext?.projectId ?? null;
  const sessions = useAgentSessions(timelineId, projectId);
  const localAgents = useLocalAgents();
  const setLocalAgent = useSetLocalAgent();
  const projectChat = useProjectChat(projectId);
  const saveDraft = useSaveProjectDraft(projectId);
  const selectSession = useSelectProjectSession(projectId);
  const setMainSession = useSetMainProjectSession(projectId);
  const renameSession = useRenameProjectSession(projectId);
  const [showAttachSessions, setShowAttachSessions] = useState(false);
  const unassignedSessions = useUnassignedProjectSessions(projectId, showAttachSessions);
  const associateSession = useAssociateProjectSession(projectId);
  const hasMainContract = projectChat.data?.main_session_id !== undefined;
  const createSession = useCreateSession(timelineId, projectId, 'ensure');
  const createNewSession = useCreateSession(timelineId, projectId, 'new');
  // Engagement signal: when the pane is locked the user has clearly committed to
  // having chat visible, so auto-create can fire without an explicit click.
  const isTasksPaneLocked = usePanesStore((state) => state.isTasksPaneLocked);
  const setIsTasksPaneOpen = usePanesStore((state) => state.setIsTasksPaneOpen);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const modelCatalog = useAgentModels(true, activeSessionId, projectId);
  const setAgentModel = useSetAgentModel(activeSessionId, projectId);
  // A chat's agent is fixed by its session; with no chat yet, the next one uses the last-used agent.
  const defaultAgent: LocalAgentId = localAgents.data?.selectedAgent ?? 'astrid';
  const chatAgent = activeSessionId ? sessionAgentId(activeSessionId) : defaultAgent;
  const chatModelName = useMemo(() => {
    const catalog = modelCatalog.data;
    if (!catalog) return null;
    if (chatAgent !== 'astrid') return catalog.localModels?.availableModels.find(model => model.modelId === catalog.localModels?.currentModelId)?.name ?? null;
    const current = catalog.providers.flatMap(provider => provider.models.map(model => ({ id: `${provider.id}/${model.id}`, name: model.name })))
      .find(model => model.id === catalog.currentModel);
    return current?.name ?? catalog.currentModel;
  }, [chatAgent, modelCatalog.data]);
  const [chatModels, setChatModels] = useState(readChatModels);
  useEffect(() => {
    if (activeSessionId && chatModelName && chatModels[activeSessionId] !== chatModelName) setChatModels(rememberChatModel(activeSessionId, chatModelName));
  }, [activeSessionId, chatModelName, chatModels]);
  const describeSession = useCallback((sessionId: string) => ({ agent: sessionAgentId(sessionId), model: chatModels[sessionId] ?? null }), [chatModels]);
  // External agents report models per session, so remember each list for New chat's submenu.
  const [agentModelLists, setAgentModelLists] = useState(() => Object.fromEntries(
    EXTERNAL_AGENT_IDS.map(agent => [agent, readAgentModels(agent)]),
  ) as Record<typeof EXTERNAL_AGENT_IDS[number], ReturnType<typeof readAgentModels>>);
  const agentModelNames = useMemo(() => {
    const catalog = modelCatalog.data;
    const astridCurrent = catalog?.providers.flatMap(provider => provider.models.map(model => ({ id: `${provider.id}/${model.id}`, name: model.name })))
      .find(model => model.id === catalog.currentModel)?.name ?? null;
    const externalName = (agent: typeof EXTERNAL_AGENT_IDS[number]) => {
      if (chatAgent === agent && chatModelName) return chatModelName;
      const saved = savedLocalAgentModel(agent);
      return saved ? agentModelLists[agent].find(model => model.id === saved)?.name ?? null : null;
    };
    return {
      astrid: chatAgent === 'astrid' ? chatModelName : astridCurrent,
      ...Object.fromEntries(EXTERNAL_AGENT_IDS.map(agent => [agent, externalName(agent)])),
    };
  }, [agentModelLists, chatAgent, chatModelName, modelCatalog.data]);
  const rememberModelList = useCallback((agent: LocalAgentId, models: Array<{ modelId: string; name: string; description?: string | null }> | undefined) => {
    if (agent === 'astrid' || !models) return;
    const list = models.map(model => ({ id: model.modelId, name: model.name, description: model.description ?? null }));
    setAgentModelLists(current => {
      if (JSON.stringify(current[agent]) === JSON.stringify(list)) return current;
      rememberAgentModels(agent, list);
      return { ...current, [agent]: list };
    });
  }, []);
  useEffect(() => { rememberModelList(chatAgent, modelCatalog.data ? modelCatalog.data.localModels?.availableModels ?? [] : undefined); }, [chatAgent, modelCatalog.data, rememberModelList]);
  const [draft, setDraft] = useState('');
  const [draftSaveError, setDraftSaveError] = useState<string | null>(null);
  const [queue, setQueue] = useState<QueuedMessage[]>([]);
  const [pausedQueueHeadId, setPausedQueueHeadId] = useState<string | null>(null);
  const pausedQueuedIdsRef = useRef(new Set<string>());
  const [optimisticMessage, setOptimisticMessage] = useState<OptimisticMessage | null>(null);
  const [attachmentLightboxMedia, setAttachmentLightboxMedia] = useState<GenerationRow | null>(null);
  const [startingAgent, setStartingAgent] = useState<LocalAgentId | null>(null);
  const [startFailure, setStartFailure] = useState<{ agent: LocalAgentId; model?: string; details: string } | null>(null);
  // Engagement flag local to AgentChatPanel: flipped by markEngaged() (split-button click)
  // and decoupled from pane open state so the close-path bug from the rev-4
  // setIsTasksPaneOpenProgrammatic approach can't recur.
  const [userEngaged, setUserEngaged] = useState(false);
  const hasAutoCreatedSessionRef = useRef(false);
  const autoCreateOperationIdRef = useRef<string | null>(null);
  const manualCreateOperationIdRef = useRef<{ projectId: string; id: string } | null>(null);
  // A completion from an earlier project visit must never select its chat here.
  if (manualCreateOperationIdRef.current?.projectId !== projectId) manualCreateOperationIdRef.current = null;
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
  const takeOverSession = useTakeOverSession(activeSessionId, projectId);
  const sessionOptions = useMemo(() => {
    // Membership, selection and Main must share one registry snapshot. The
    // independently polled sessions query supplies status and drains events;
    // it can still be stale when New publishes its registry receipt.
    const statuses = new Map(readAgentSessions(sessions.data).map(session => [session.id, session.status]));
    return (projectChat.data?.sessions ?? []).flatMap((session, index) => session.missing ? [] : [{
      id: session.id,
      title: session.title,
      status: statuses.get(session.id) ?? 'waiting_user',
      // Count missing entries too so siblings never renumber.
      chatNumber: index + 1,
    }]);
  }, [sessions.data, projectChat.data?.sessions]);
  const showSessionSelector = sessionOptions.length > 0 && Boolean(projectChat.data) && (sessionOptions.length > 1 || hasMainContract);
  // New chat's submenu: Astrid's catalog is global (the store serves it for any Astrid-scoped key without
  // loading a chat); the other agents list models per session, so read the latest chat of that agent.
  const [browseAgent, setBrowseAgent] = useState<LocalAgentId | null>(null);
  const browseSessionId = browseAgent === null ? null
    : browseAgent === 'astrid' ? 'astrid-model-catalog'
      : activeSessionId && sessionAgentId(activeSessionId) === browseAgent ? activeSessionId
        : [...sessionOptions].reverse().find(session => sessionAgentId(session.id) === browseAgent)?.id ?? null;
  const browseModels = useAgentModels(Boolean(browseSessionId), browseSessionId, projectId);
  useEffect(() => {
    if (browseAgent) rememberModelList(browseAgent, browseModels.data ? browseModels.data.localModels?.availableModels ?? [] : undefined);
  }, [browseAgent, browseModels.data, rememberModelList]);
  // Another tab may have seen this agent's models since this one loaded.
  useEffect(() => {
    if (!browseAgent || browseAgent === 'astrid') return;
    const stored = readAgentModels(browseAgent);
    if (stored.length) setAgentModelLists(current => JSON.stringify(current[browseAgent]) === JSON.stringify(stored) ? current : { ...current, [browseAgent]: stored });
  }, [browseAgent]);
  const newChatModels = useMemo<NewChatAgentModels | null>(() => {
    if (!browseAgent) return null;
    if (browseAgent === 'astrid') {
      const catalog = browseModels.data;
      return {
        agent: 'astrid',
        models: (catalog?.providers ?? []).filter(provider => provider.signedIn || provider.models.length > 0)
          .flatMap(provider => provider.models.map(model => ({ id: `${provider.id}/${model.id}`, name: model.name, detail: provider.name }))),
        defaultModel: catalog?.currentModel ?? null,
        loading: browseModels.isLoading,
        note: browseModels.error ? 'Could not load Astrid models.' : 'No models available.',
      };
    }
    const remembered = agentModelLists[browseAgent];
    return {
      agent: browseAgent,
      models: remembered.map(model => ({ id: model.id, name: model.name, detail: model.description })),
      defaultModel: savedLocalAgentModel(browseAgent) ?? null,
      loading: remembered.length === 0 && Boolean(browseSessionId) && !browseModels.error && (browseModels.isLoading || browseModels.isFetching),
      note: `${agentNames[browseAgent]} lists its models once it has a chat. Start one, then pick a model inside it.`,
    };
  }, [agentModelLists, browseAgent, browseModels.data, browseModels.error, browseModels.isFetching, browseModels.isLoading, browseSessionId]);
  const agentCanBrowse = useMemo(() => ({
    ...Object.fromEntries(EXTERNAL_AGENT_IDS.filter(agent => agent !== 'hermes').map(agent => [agent, true])),
    hermes: agentModelLists.hermes.length > 0,
  }), [agentModelLists.hermes.length]);
  const hydratedProjectDraftRef = useRef(false);
  const draftPersistenceRef = useRef<ProjectChatDraftPersistence<QueuedMessage> | null>(null);
  const draftScopeRef = useRef<string | null>(null);
  const draftSnapshotRef = useRef({ text: draft, queue });
  draftSnapshotRef.current = { text: draft, queue };
  useEffect(() => {
    if (!projectChat.data) return;
    const restored = projectChat.data.draft.queued_messages ?? [];
    const savedQueue = restored.map((item) => ({ id: item.id, text: item.text, sessionId: item.session_id, attachments: Array.isArray(item.attachments) ? item.attachments as AgentTurnAttachment[] : [] }));
    const saved = { text: projectChat.data.draft.text, queue: savedQueue };
    if (hydratedProjectDraftRef.current) {
      draftPersistenceRef.current?.observe(projectChat.data.draft.revision, saved, draftSnapshotRef.current);
      return;
    }
    hydratedProjectDraftRef.current = true;
    draftScopeRef.current = projectChat.data.scope_key;
    const retained = unsavedProjectChatDrafts.get(projectId!);
    const local = retained?.scopeKey === projectChat.data.scope_key && retained.dirty ? retained : undefined;
    // A reopened composer continues its own in-flight save. A second mounted
    // composer keeps a separate CAS base, so divergent edits still conflict.
    const persistence = local && !local.persistence.mounted
      ? local.persistence
      : new ProjectChatDraftPersistence(projectChat.data.draft.revision, saved);
    if (local && persistence !== local.persistence) {
      persistence.revision = local.persistence.revision;
      persistence.saved = local.persistence.saved;
    }
    persistence.mounted = true;
    persistence.observe(projectChat.data.draft.revision, saved, local ?? saved);
    draftPersistenceRef.current = persistence;
    const initial = local ? { text: local.text, queue: local.queue } : saved;
    draftSnapshotRef.current = initial;
    setDraft(initial.text);
    setQueue(initial.queue);
    initial.queue.forEach(item => pausedQueuedIdsRef.current.add(item.id));
    setPausedQueueHeadId(initial.queue[0]?.id ?? null);
  }, [projectChat.data, projectId]);
  const flushDraftRef = useRef<() => Promise<void>>(async () => undefined);
  flushDraftRef.current = async () => {
    const persistence = draftPersistenceRef.current;
    if (!projectId || !persistence) return;
    const snapshot = draftSnapshotRef.current;
    const queuePayload = snapshot.queue.map((item) => ({ id: item.id, text: item.text, session_id: item.sessionId, attachments: item.attachments }));
    try {
      await persistence.save(snapshot, async (expectedRevision) => {
        const result = await saveDraft.mutateAsync({ expectedRevision, text: snapshot.text, queuedMessages: queuePayload });
        return result.draft.revision;
      });
      setDraftSaveError(null);
      const current = unsavedProjectChatDrafts.get(projectId);
      if (current?.persistence === persistence && sameProjectDraft(current, snapshot)) {
        unsavedProjectChatDrafts.set(projectId, { ...current, dirty: false });
      }
    } catch (error) {
      setDraftSaveError(error instanceof Error ? error.message : String(error));
      throw error;
    }
  };
  useEffect(() => {
    if (!projectId || !hydratedProjectDraftRef.current) return;
    const timer = window.setTimeout(() => { void flushDraftRef.current().catch(() => undefined); }, 350);
    return () => window.clearTimeout(timer);
  }, [projectId, draft, queue]);
  useEffect(() => {
    const persistence = draftPersistenceRef.current;
    if (!projectId || !persistence || !draftScopeRef.current) return;
    const snapshot = draftSnapshotRef.current;
    unsavedProjectChatDrafts.set(projectId, { ...snapshot, dirty: !sameProjectDraft(snapshot, persistence.saved), scopeKey: draftScopeRef.current, persistence });
  }, [projectId, draft, queue]);
  useEffect(() => {
    if (draftPersistenceRef.current) draftPersistenceRef.current.mounted = true;
    return () => {
      if (draftPersistenceRef.current) draftPersistenceRef.current.mounted = false;
      void flushDraftRef.current().catch(() => undefined);
    };
  }, []);
  const restoreSavedDraft = useCallback(async () => {
    const result = await projectChat.refetch();
    if (!result.data) return;
    const saved = { text: result.data.draft.text, queue: (result.data.draft.queued_messages ?? []).map((item) => ({ id: item.id, text: item.text, sessionId: item.session_id, attachments: Array.isArray(item.attachments) ? item.attachments as AgentTurnAttachment[] : [] })) };
    const persistence = new ProjectChatDraftPersistence(result.data.draft.revision, saved);
    draftPersistenceRef.current = persistence;
    draftSnapshotRef.current = saved;
    setDraft(saved.text);
    setQueue(saved.queue);
    unsavedProjectChatDrafts.set(projectId!, { ...saved, dirty: false, scopeKey: result.data.scope_key, persistence });
    setDraftSaveError(null);
  }, [projectChat, projectId]);
  const overwriteSavedDraft = useCallback(async () => {
    const result = await projectChat.refetch();
    if (!result.data || !draftPersistenceRef.current) return;
    draftPersistenceRef.current.revision = result.data.draft.revision;
    setDraftSaveError(null);
    await flushDraftRef.current();
  }, [projectChat]);
  const activeSessionData = readAgentSession(activeSession.data);
  const handleSetMainSession = useCallback(async (sessionId: string) => {
    if (!projectChat.data) return;
    await setMainSession.mutateAsync({ expectedRevision: projectChat.data.revision, sessionId });
    setActiveSessionId(sessionId);
  }, [projectChat.data, setMainSession]);
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
  const sessionControl = activeSessionData?.control;
  const isFollower = sessionControl?.role === 'follower';
  const isCancelled = activeStatus === 'cancelled';
  const isProcessing = activeStatus === 'processing' || activeStatus === 'continue' || Boolean(sessionControl?.active);
  const showKillSwitch = !isFollower && (activeStatus === 'processing' || activeStatus === 'continue' || Boolean(sessionControl?.active));
  const isFollowerRef = useRef(isFollower);
  isFollowerRef.current = isFollower;
  useEffect(() => {
    if (isFollower) voiceRef.current.cancelRecording();
  }, [isFollower]);
  const showNoProjectState = !hasProject && sessionOptions.length === 0;
  const hasQueuedMessages = queue.some((item) => item.sessionId === activeSessionId);
  const activeQueue = queue.filter((item) => item.sessionId === activeSessionId);
  // A phone or tablet has no shortcut keys to press: its way to talk is the mic.
  const [coarsePointer] = useState(() => typeof window !== 'undefined' && window.matchMedia?.('(pointer: coarse)').matches === true);
  const inputPlaceholder = showNoProjectState
    ? 'Select a project to start chatting...'
    : voice.isRecording
      ? 'Recording...'
      : (isProcessing || sendMessage.isPending || hasQueuedMessages)
        ? 'Type to queue next message...'
        : coarsePointer ? 'Type, or tap the mic to talk...' : 'Type or press Cmd+Shift+R to talk...';
  const optimisticTurnAlreadyMaterialized = optimisticMessage !== null
    && Boolean(activeSessionData?.turns.some((turn) => turn.role === 'user' && turn.request_id === optimisticMessage.id));
  const chatFailures = [activeSession.error, sendMessage.localError, createSession.error, sessions.error, projectChat.error];
  // No chat service on this computer is a state, not a failure: the pane says so in one plain line, with no alert or retry.
  const chatUnavailable = chatFailures.some(isAcpUnavailable);
  const showEmptyState = !activeSession.isLoading && renderedTurns.length === 0 && !isProcessing && !sendMessage.isPending;
  const turnFailure = chatFailures.find(Boolean);
  const turnFailureMessage = turnFailure instanceof Error ? turnFailure.message : turnFailure ? String(turnFailure) : 'Agent error. Try again or start a new conversation.';

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

  // Main is the opening default; retain explicit choices, including a New
  // selection queued before this render's opening-default updater applies.
  useEffect(() => {
    if (hasProject && !projectChat.data) return;
    setActiveSessionId(current => {
      if (current && (current === projectChat.data?.selected_session_id || sessionOptions.some(session => session.id === current))) return current;
      const preferred = projectChat.data?.selected_session_id ?? projectChat.data?.main_session_id;
      if (preferred && sessionOptions.some(session => session.id === preferred)) return preferred;
      return (sessionOptions.find(session => session.status !== 'cancelled') ?? sessionOptions[0])?.id ?? null;
    });
  }, [hasProject, hasMainContract, projectChat.data, sessionOptions]);

  // An empty engaged project gets one session. Existing project chats remain
  // selectable when Main is unset, and the host CAS claim arbitrates tabs.
  const isEngaged = userEngaged || isTasksPaneLocked || voice.isRecording || voice.isProcessing;
  const hasAvailableProjectSession = Boolean(projectChat.data?.sessions.some(session => !session.missing));
  useEffect(() => {
    if (hasAutoCreatedSessionRef.current || !projectChat.data || projectChat.isLoading || projectChat.isError
      || createSession.isPending || !hasProject
      || hasAvailableProjectSession || !isEngaged) return;
    hasAutoCreatedSessionRef.current = true;
    autoCreateOperationIdRef.current ??= createMessageId();
    createSession.mutate(autoCreateOperationIdRef.current, {
      onError: () => { /* Retain the operation ID for explicit recovery. */ },
      onSuccess: session => {
        autoCreateOperationIdRef.current = null;
        const sessionId = readSessionId(session);
        if (sessionId) setActiveSessionId(current => current ?? sessionId);
      },
    });
  }, [createSession, hasProject, hasAvailableProjectSession, projectChat.data, projectChat.isLoading, projectChat.isError, isEngaged]);

  // Cmd+Shift+R global shortcut — kept verbatim per plan_v5 Step 4.7.
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'r') {
        event.preventDefault();
        if (!hasProject || isFollower) {
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
  }, [hasProject, isFollower, voice]);

  useEffect(() => {
    sendingRef.current = false;
    setPausedQueueHeadId(draftSnapshotRef.current.queue.find(item => item.sessionId === activeSessionId)?.id ?? null);
    setOptimisticMessage(null);
  }, [activeSessionId]);

  useEffect(() => {
    if (!isFollower || !activeSessionId) return;
    const followerQueue = queue.filter(item => item.sessionId === activeSessionId);
    followerQueue.forEach(item => pausedQueuedIdsRef.current.add(item.id));
    if (followerQueue.length > 0) setPausedQueueHeadId(current => current ?? followerQueue[0].id);
  }, [isFollower, activeSessionId, queue]);

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
      && turn.request_id === optimisticMessage.id
    ));

    if (hasRealTurn) {
      setOptimisticMessage(null);
    }
  }, [activeSessionData?.turns, optimisticMessage]);

  const reconcileAcceptedQueue = useCallback((ids: readonly string[], sessionId: string) => {
    const accepted = new Set(ids);
    const snapshot = draftSnapshotRef.current;
    const removed = snapshot.queue.filter(item => item.sessionId === sessionId && accepted.has(item.id));
    if (!removed.length) return false;
    const remaining = snapshot.queue.filter(item => !(item.sessionId === sessionId && accepted.has(item.id)));
    // Recovered delivery is not permission to dispatch a subsequent saved row.
    remaining.forEach(item => pausedQueuedIdsRef.current.add(item.id));
    removed.forEach(item => pausedQueuedIdsRef.current.delete(item.id));
    draftSnapshotRef.current = { ...snapshot, queue: remaining };
    setQueue(remaining);
    setPausedQueueHeadId(remaining.find(item => item.sessionId === sessionId)?.id ?? null);
    setOptimisticMessage(previous => previous && accepted.has(previous.id) ? null : previous);
    return true;
  }, []);
  useEffect(() => {
    if (!activeSessionId || !hydratedProjectDraftRef.current) return;
    const acceptedIds = activeSessionData?.durableAcceptedRequestIds ?? [];
    const inFlightId = sessionControl?.active ? sessionControl.activeRequestId : null;
    reconcileAcceptedQueue(inFlightId ? acceptedIds.filter(id => id !== inFlightId) : acceptedIds, activeSessionId);
  }, [activeSessionId, activeSessionData?.durableAcceptedRequestIds, queue, reconcileAcceptedQueue, sessionControl?.active, sessionControl?.activeRequestId]);

  const sendingRef = useRef(false);
  const currentSessionRef = useRef(activeSessionId);
  currentSessionRef.current = activeSessionId;
  const currentContextRef = useRef(editorContext);
  currentContextRef.current = editorContext;
  const sendNow = useCallback(async (item: QueuedMessage, retryCaptured = false, checkSaved = false) => {
    if (!activeSessionId || !projectId || !editorContext || item.sessionId !== activeSessionId || isFollower || sessionControl?.active) {
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
      if (checkSaved && await sendMessage.checkAcceptedRequest(item.id)) {
        if (isCurrent()) { reconcileAcceptedQueue([item.id], item.sessionId); await flushDraftRef.current(); }
        return;
      }
      if (!isCurrent()) return;
      if (retryCaptured) await sendMessage.retryLastMessage();
      else await sendMessage.mutateAsync({
        input: { message: item.text, attachments: item.attachments, requestId: item.id },
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
  }, [activeSessionData?.turns.length, activeSessionId, editorContext, projectId, sendMessage, reconcileAcceptedQueue, isFollower, sessionControl?.active]);

  const handleSend = useCallback(async (rawText?: string) => {
    const text = (rawText ?? draft).trim();
    if (!text || !activeSessionId || !hasProject || isFollower) return;

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
      || isFollower
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
  }, [activeSessionId, clips, draft, hasProject, isProcessing, isFollower, optimisticMessage, queue, sendMessage.isPending, sendNow]);

  useEffect(() => {
    if (
      sendingRef.current
      || isFollower
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
  }, [queue, pausedQueueHeadId, isFollower, isProcessing, sendMessage.isPending, optimisticMessage, activeSessionId, projectId, sendNow]);

  const handleNewSession = useCallback(async (): Promise<string | null> => {
    if (!projectId) return null;
    manualCreateOperationIdRef.current ??= { projectId, id: createMessageId() };
    const operation = manualCreateOperationIdRef.current;
    const session = await createNewSession.mutateAsync(operation.id);
    if (!isPanelMountedRef.current || manualCreateOperationIdRef.current !== operation
      || currentContextRef.current?.projectId !== operation.projectId) return null;
    manualCreateOperationIdRef.current = null;
    const sessionId = readSessionId(session);
    if (sessionId) {
      setPausedQueueHeadId(null);
      setOptimisticMessage(null);
      setActiveSessionId(sessionId);
      setIsTasksPaneOpen?.(true);
      requestAnimationFrame(() => {
        if (isPanelMountedRef.current && currentContextRef.current?.projectId === operation.projectId) inputRef.current?.focus();
      });
    }
    return sessionId ?? null;
  }, [createNewSession, projectId, setIsTasksPaneOpen]);

  // Choosing an agent starts a chat with it; the main New click reuses the last one. A model picked in
  // the submenu is applied to the new chat as soon as it reports its models.
  const pendingModelRef = useRef<{ sessionId: string; model: string } | null>(null);
  const startChatWith = useCallback(async (agent?: LocalAgentId, model?: string) => {
    const chosen = agent ?? defaultAgent;
    setStartFailure(null);
    setStartingAgent(chosen);
    try {
      if (chosen !== defaultAgent) await setLocalAgent.mutateAsync(chosen);
      // Without a pick, Claude Code and Codex start on their remembered default when it is still on offer.
      const saved = chosen === 'astrid' ? undefined : savedLocalAgentModel(chosen);
      const target = model ?? (saved && chosen !== 'astrid' && agentModelLists[chosen].some(choice => choice.id === saved) ? saved : undefined);
      const sessionId = await handleNewSession();
      if (sessionId && target) pendingModelRef.current = { sessionId, model: target };
    } catch (error) {
      setStartFailure({ agent: chosen, model, details: error instanceof Error ? error.message : String(error) });
    } finally {
      setStartingAgent(null);
    }
  }, [agentModelLists, defaultAgent, handleNewSession, setLocalAgent]);
  useEffect(() => {
    const pending = pendingModelRef.current;
    if (!pending || pending.sessionId !== activeSessionId || !modelCatalog.data || setAgentModel.isPending) return;
    pendingModelRef.current = null;
    const current = chatAgent === 'astrid' ? modelCatalog.data.currentModel : modelCatalog.data.localModels?.currentModelId;
    if (current !== pending.model) void setAgentModel.mutateAsync(pending.model).catch(() => undefined);
  }, [activeSessionId, chatAgent, modelCatalog.data, setAgentModel]);

  // ==========================================================================
  // Actions registry — exposes stable handlers the parent (TasksPane split
  // button) can invoke. Stable identity means the registration effect runs
  // exactly once per mount, even though `voice` re-renders. Reactive state is
  // published separately so the split button mic icon flips with recording.
  // ==========================================================================
  const actionsRegistry = useAgentChatActionsRegistry();
  const stableHandlers = useMemo<AgentChatActionsHandlers>(() => ({
    toggleRecording: () => {
      if (isFollowerRef.current) return;
      const v = voiceRef.current;
      if (v.isRecording) {
        v.stopRecording();
      } else if (!v.isProcessing) {
        v.startRecording();
      }
    },
    focusComposer: () => {
      // The pane may still be sliding in: do not scroll the page to reach it.
      inputRef.current?.focus({ preventScroll: true });
    },
    markEngaged: () => {
      setUserEngaged(true);
    },
  }), []);

  // Astrid is answering: the turn is running, being sent or queued behind one. The pane shows
  // it as "Thinking..."; it is published so an editor's own Astrid entry can say so too.
  const agentWorking = isProcessing || sendMessage.isPending || (hasQueuedMessages && !pausedQueueHeadId);

  useEffect(() => {
    actionsRegistry.registerHandlers(stableHandlers);
    actionsRegistry.publishState({
      isRecording: voice.isRecording,
      isProcessing: voice.isProcessing,
      isAgentWorking: agentWorking,
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
      isAgentWorking: agentWorking,
    });
  }, [actionsRegistry, voice.isRecording, voice.isProcessing, agentWorking]);

  return (
    // No background of its own — sits on the parent pane's bg so the only
    // visible color change between halves is the divider line itself.
    <div className="flex h-full w-full flex-col overflow-hidden">
      {/* Header */}
      <div data-testid="agent-chat-header" className="@container/agent-header relative flex min-w-0 items-center justify-between gap-2 border-b border-border/70 px-3 py-2">
        <div className="flex shrink-0 items-center gap-2">
          <span className="flex min-w-0 items-center gap-1.5 text-muted-foreground">
            <AgentIcon agent={chatAgent} className="h-3.5 w-3.5 shrink-0" />
            <span data-testid="agent-chat-identity" className="truncate text-xs normal-case">
              {agentNames[chatAgent]}
            </span>
            {chatModelName && (
              <Tooltip>
                <TooltipTrigger asChild>
                  <button type="button" aria-label="Chat model information" className="-m-1 rounded-sm p-1 text-muted-foreground hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                    <Info className="h-3 w-3" aria-hidden="true" />
                  </button>
                </TooltipTrigger>
                <TooltipContent className="text-xs normal-case">
                  <div>{chatModelName}</div>
                  <div className="text-muted-foreground">To use another model, start a new chat.</div>
                </TooltipContent>
              </Tooltip>
            )}
          </span>
          {isProcessing && <Loader2 className="h-3.5 w-3.5 animate-spin text-muted-foreground" />}
        </div>
        <div className="flex min-w-0 shrink items-center justify-end gap-1">
          {showSessionSelector && projectChat.data && (
            <AgentChatSessionSelector
              sessions={sessionOptions}
              activeSessionId={activeSessionId}
              mainSessionId={projectChat.data.main_session_id ?? null}
              onOpenChange={onSessionSelectorOpenChange}
              settingMainSessionId={setMainSession.isPending ? setMainSession.variables?.sessionId ?? null : null}
              describeSession={describeSession}
              onSelectSession={(sessionId) => {
                if (!projectId) return;
                void selectSession.mutateAsync({ expectedRevision: projectChat.data.revision, sessionId }).then(() => setActiveSessionId(sessionId)).catch(() => undefined);
              }}
              onSetMainSession={hasMainContract
                ? (sessionId) => void handleSetMainSession(sessionId).catch(() => undefined)
                : undefined}
              onRenameSession={(sessionId, title) => renameSession.mutateAsync({ expectedRevision: projectChat.data.revision, sessionId, title })}
            />
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
          <AgentChatNewChatButton
            defaultAgent={defaultAgent}
            agents={localAgents.data?.agents}
            agentModelNames={agentModelNames}
            agentCanBrowse={agentCanBrowse}
            agentsLoading={localAgents.isLoading}
            agentsError={localAgents.error instanceof Error ? localAgents.error.message : null}
            disabled={startingAgent !== null || createNewSession.isPending || setLocalAgent.isPending || !hasProject}
            onMenuOpenChange={(open) => { if (open) void localAgents.refetch(); }}
            onBrowseAgent={setBrowseAgent}
            agentModels={newChatModels}
            onNewChat={(agent, model) => void startChatWith(agent, model)}
            attachExisting={projectId ? { open: showAttachSessions, toggle: () => setShowAttachSessions((open) => !open) } : undefined}
          />
        </div>
      </div>
      {startingAgent && startingAgent !== 'astrid' && <p role="status" className="border-b border-border/70 px-3 py-1.5 text-xs text-muted-foreground">Getting {agentNames[startingAgent]} ready…</p>}
      {startFailure && (
        <div role="alert" className="border-b border-destructive/40 bg-destructive/10 px-3 py-2 text-xs text-destructive">
          <p>{agentNames[startFailure.agent]} didn't start.</p>
          <p>Details: {startFailure.details}</p>
          <button type="button" className="mt-1 underline" onClick={() => void startChatWith(startFailure.agent, startFailure.model)}>Try again</button>
        </div>
      )}
      {showAttachSessions && projectId && (
        <div id="unassigned-project-chats" className="border-b border-border/70 px-4 py-2" aria-label="Unassigned existing chats">
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
        {isFollower && (
          // Stays in view while scrolling, just under the header that names the chat's agent.
          <div role="status" className="sticky top-0 z-10 mb-2 flex flex-wrap items-center justify-between gap-x-3 gap-y-1 rounded-md border border-border/70 bg-card px-3 py-2 text-xs text-muted-foreground shadow-sm">
            <span>Active in another tab</span>
            <Button
              type="button"
              size="sm"
              variant="outline"
              className="h-7 shrink-0 px-2 text-xs"
              aria-label="Active in another tab — take over"
              disabled={takeOverSession.isPending || !activeSessionId || !projectId}
              onClick={() => takeOverSession.mutate()}
            >
              Take over
            </Button>
            {takeOverSession.error && <span role="alert">Could not take over: {takeOverSession.error instanceof Error ? takeOverSession.error.message : String(takeOverSession.error)}</span>}
          </div>
        )}
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

        {showEmptyState && (
          <div className="flex min-h-full flex-col items-center justify-center py-8 text-center text-sm text-muted-foreground">
            {chatUnavailable ? (
              <p>{CHAT_UNAVAILABLE}</p>
            ) : sessions.isError ? (
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
                {coarsePointer
                  ? <p className="mt-1 text-xs">Tap the mic to talk</p>
                  : <p className="mt-1 text-xs">Press <kbd className="rounded border border-border px-1 py-0.5 text-[10px]">Cmd+Shift+R</kbd> to talk</p>}
                <p data-testid="agent-chat-runs-with" className="mt-4 flex items-center gap-1.5 rounded-md border border-border/70 px-2 py-1 text-[11px] normal-case">
                  <AgentIcon agent={chatAgent} className="h-3 w-3 shrink-0" />
                  {agentNames[chatAgent]} · {chatModelName ?? 'default model'}
                </p>
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
                recordedResults={activeSessionData?.recordedEditorResults}
                onAttachmentClick={handleAttachmentPreviewClick}
              />
            ) : (
              <div key={`${activeSessionId}:${item.key}`} className="space-y-2">
                <AgentChatToolGroup pairs={item.pairs} />
                {item.pairs.map((pair, index) => <div key={pair.call.tool_call_id ?? index} data-agent-tool-call-id={pair.call.tool_call_id}>
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

          {agentWorking && (
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
                  {sessionControl?.active && item.id === sessionControl.activeRequestId && <div className="text-muted-foreground">{isFollower ? 'In progress in another tab' : 'In progress'}</div>}
                  {item.id === pausedQueueHeadId && !isFollower && !activeSession.isLoading && !sessionControl?.active && <div className="text-muted-foreground">Delivery not confirmed. Retry checks saved history first; it may send this message again.</div>}
                </div>
                {item.attachments.length > 0 && (
                  <span className="shrink-0 rounded-full bg-background/80 px-2 py-0.5 text-[11px] text-muted-foreground">
                    {`📎 ${item.attachments.length}`}
                  </span>
                )}
                {item.id === pausedQueueHeadId && !isFollower && !sessionControl?.active && !activeSession.isLoading && (
                  <button type="button" onClick={() => { void sendNow(item, sendMessage.hasCapturedMessage?.(item.sessionId, item.id) ?? false, true).catch(() => undefined); }}>
                    Retry saved message
                  </button>
                )}
                <Button
                  type="button"
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6 shrink-0"
                  disabled={isFollower || index === 0}
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
                  disabled={isFollower || index === activeQueue.length - 1}
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
                  disabled={isFollower}
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

        {chatUnavailable && !showEmptyState && (
          <p className="mb-2 px-1 text-xs text-muted-foreground">{CHAT_UNAVAILABLE}</p>
        )}

        {!isProcessing && !sendMessage.isPending && !isCancelled && !chatUnavailable && (turnFailure || activeStatus === 'error') && (
          <div role="alert" className="mb-2 rounded-lg border border-destructive/40 bg-destructive/10 px-3 py-2 text-xs text-destructive">
            {turnFailureMessage}
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
            {/* 16px text on touch (iOS zooms the page into a smaller field); about two lines on a
                short screen (a phone on its side), so the conversation keeps the height. */}
            <textarea
              ref={inputRef}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              rows={isExpanded ? 8 : 4}
              placeholder={inputPlaceholder}
              className="min-h-10 w-full resize-none rounded-xl border border-border/70 bg-card px-3 py-2 pr-12 text-sm leading-5 [@media(pointer:coarse)]:text-base [@media(max-height:500px)]:max-h-[4.75rem] outline-none transition-colors placeholder:text-muted-foreground/70 focus:border-primary/50"
              disabled={isFollower || !hasProject || !activeSessionId || isCancelled || voice.isRecording || voice.isProcessing}
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
                  disabled={isFollower || !hasProject || !activeSessionId || isCancelled || voice.isProcessing || sendMessage.isPending}
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
                  disabled={isFollower || !hasProject || !draft.trim() || !activeSessionId || isCancelled}
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
