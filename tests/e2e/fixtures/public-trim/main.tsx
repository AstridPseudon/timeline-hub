import { useMemo, useState, type ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import { AgentChatProvider, useAgentChatRegistry } from '@/shared/contexts/AgentChatContext';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider';
import { BrowserVideoEditor } from '@/tools/video-editor/browser/BrowserVideoEditor';
import { createVideoEditorEffectCatalog } from '@/tools/video-editor/browser-provider';
import type { VideoEditorScopedServices } from '@/tools/video-editor/browser/scopedServices';
import { PUBLIC_TIMELINE_SERVICE_HOOKS } from '@/tools/video-editor/runtime/timelineHostServiceHooks';
import { useTimelineChromeContext, useTimelineEditorData } from '@/tools/video-editor/hooks/timelineStore';
import { useTimelineCommandsService } from '@/tools/video-editor/hooks/useTimelineCommandsService';
import { getClipEndSeconds, roundTimelineValue } from '@/tools/video-editor/lib/editor-utils';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import '@/index.css';

const params = new URLSearchParams(window.location.search);
const projectId = params.get('project');
const timelineId = params.get('timeline');
if (!projectId || !timelineId) throw new Error('The public trim fixture requires project and timeline query parameters.');

const provider = new RuntimeDataProvider({ projectId });
const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });

function FixtureControls() {
  const data = useTimelineEditorData();
  const chrome = useTimelineChromeContext();
  const commands = useTimelineCommandsService();
  const [result, setResult] = useState('');
  const clip = data.resolvedConfig.clips.find((candidate) => candidate.id === 'f2-transition-clip');
  const trim = () => {
    if (!clip) return setResult(JSON.stringify({ ok: false, error: { code: 'clip_not_found' } }));
    const endTime = roundTimelineValue(getClipEndSeconds(clip) - 0.5);
    setResult(JSON.stringify(commands.trimClip({ clipId: clip.id, endTime })));
  };
  const recoveryOwners = chrome.commandSession?.state.recoverableOwners ?? [];
  return <main>
    <button type="button" data-testid="public-trim-trigger" disabled={!clip} onClick={trim}>Run public trim</button>
    {recoveryOwners.map((ownerId) => <button key={ownerId} type="button" data-testid="public-trim-recover" data-owner-id={ownerId} onClick={() => void chrome.commandSession?.recover(ownerId)}>Recover saved edits</button>)}
    <button type="button" data-testid="public-trim-undo" disabled={!chrome.canUndo} onClick={chrome.undo}>Undo</button>
    <output data-testid="public-trim-result">{result}</output>
    <output data-testid="public-trim-status">{chrome.commandSession?.state.status ?? chrome.saveStatus}</output>
  </main>;
}

function HostServices({ children }: { children: ReactNode }) {
  const registry = useAgentChatRegistry();
  const [owner] = useState(() => Symbol('public-trim-fixture'));
  const services = useMemo<VideoEditorScopedServices>(() => ({
    contract: 'astrid.video-editor.scoped-services.v1',
    scope: { instanceId: 'public-trim-fixture', projectId, projectSlug: projectId, timelineId },
    shots: { shots: [], isLoading: false, error: null, refetchShots() {}, finalVideoMap: new Map(), dismissFinalVideo() {} },
    mediaLightbox: { Lightbox: () => null, loadGenerationForLightbox: async () => null },
    agentChat: {
      registerTimeline: (value) => registry.register({ timelineId: value.timelineId, editorContext: { tool: 'video-editor', ...value } }, owner),
      unregisterTimeline: () => registry.unregister(owner),
      activateTimeline: () => registry.activate(owner),
    },
    toast: { error: () => '', warning: () => '', success: () => '', info: () => '' },
    telemetry: { log() {}, warn() {}, error() {} },
    timelineServices: PUBLIC_TIMELINE_SERVICE_HOOKS,
  }), [owner, registry]);
  return <BrowserVideoEditor dataProvider={provider} timelineId={timelineId} effectCatalog={createVideoEditorEffectCatalog({ effects: [] })} hostServices={services}>
    {children}
  </BrowserVideoEditor>;
}

createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <MemoryRouter>
      <AgentChatProvider>
        <HostServices><FixtureControls /></HostServices>
      </AgentChatProvider>
    </MemoryRouter>
  </QueryClientProvider>,
);
