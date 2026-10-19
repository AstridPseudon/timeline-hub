import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, renderHook, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { TooltipProvider } from '@/shared/components/ui/tooltip.tsx';

let origin = '';
vi.mock('@/integrations/runtime/connection.ts', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/integrations/runtime/connection.ts')>()),
  runtimeOrigin: () => origin,
  astridBase: () => `${origin}/api/astrid`,
}));

vi.mock('@/shared/contexts/AgentChatContext', () => ({
  useAgentChatBridge: () => ({ timelineId: null, editorContext: { projectId: 'project-1' } }),
  useAgentChatActionsRegistry: () => ({ registerHandlers: () => {}, publishState: () => {}, unregister: () => {} }),
}));
vi.mock('@/tools/video-editor/hooks/useAgentVoice', () => ({
  useAgentVoice: () => ({ isRecording: false, isProcessing: false, cancelRecording: () => {} }),
}));

import { AgentChatPanel } from './AgentChat.tsx';
import { isTimelineAgentSessionsAvailable, useProjectAgentTaskLinks } from '@/tools/video-editor/hooks/useAgentSession.ts';

const GATEWAY = 'http://127.0.0.1:17340';
const chat = {
  project_id: 'project-1', scope_key: 'realm:project-1', revision: 0,
  selected_session_id: null, sessions: [], draft: { text: '', revision: 0 },
};
const models = {
  currentModel: 'openai-codex/gpt-5.6-sol',
  providers: [{ id: 'openai-codex', name: 'OpenAI Codex', signedIn: true, models: [{ id: 'gpt-5.6-sol', name: 'GPT 5.6 Sol' }] }],
};

function withQueryClient({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0 } } });
  return <QueryClientProvider client={client}><TooltipProvider>{children}</TooltipProvider></QueryClientProvider>;
}

describe('agent chat on the hosted build', () => {
  let fetchSpy: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchSpy = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      const body = url.endsWith('/acp/models') ? models : url.endsWith('/chat') ? chat
        : url.endsWith('/agents') ? { agents: [] }
        : url.endsWith('/connect') ? { connection_id: 'connection-1', initialize: {} }
        : url.endsWith('/events') ? { notifications: [], disconnected: false } : null;
      return new Response(JSON.stringify(body), { status: body ? 200 : 404 });
    });
    vi.stubGlobal('fetch', fetchSpy);
  });

  afterEach(() => {
    origin = '';
    vi.unstubAllGlobals();
  });

  it('mounts the composer and reads project chat and signed-in models through the local gateway', async () => {
    origin = GATEWAY;
    expect(isTimelineAgentSessionsAvailable()).toBe(true);
    render(<AgentChatPanel />, { wrapper: withQueryClient });

    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.queryByText("Agent chat isn't on this page yet.")).toBeNull();
    expect(screen.queryByRole('link', { name: 'Open the full editor' })).toBeNull();
    await waitFor(() => expect(screen.getByText('GPT 5.6 Sol')).toBeInTheDocument());
    const urls = fetchSpy.mock.calls.map(([url]) => String(url));
    expect(urls).toContain(`${GATEWAY}/api/astrid/acp/models`);
    expect(urls).toContain(`${GATEWAY}/api/astrid/acp/agents`);
    expect(urls).toContain(`${GATEWAY}/api/astrid/acp/projects/project-1/chat`);
    expect(urls.every(url => url.startsWith(`${GATEWAY}/api/astrid/acp/`))).toBe(true);
    for (const [, request] of fetchSpy.mock.calls) expect(request?.headers).not.toHaveProperty('Authorization');
  });

  it('rehydrates project task links through the gateway', async () => {
    origin = GATEWAY;
    const { result } = renderHook(() => useProjectAgentTaskLinks('project-1'), { wrapper: withQueryClient });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual([]);
    expect(fetchSpy).toHaveBeenCalledWith(`${GATEWAY}/api/astrid/acp/projects/project-1/chat`, expect.anything());
    expect(fetchSpy.mock.calls.every(([url]) => String(url).startsWith(`${GATEWAY}/api/astrid/acp/`))).toBe(true);
  });

  it('keeps same-origin chat available', async () => {
    expect(isTimelineAgentSessionsAvailable()).toBe(true);
    const { result } = renderHook(() => useProjectAgentTaskLinks('project-1'), { wrapper: withQueryClient });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(fetchSpy).toHaveBeenCalledWith('/api/astrid/acp/projects/project-1/chat', expect.anything());
  });
});
