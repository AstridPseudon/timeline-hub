import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, renderHook, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { RUNTIME_CONNECTION_COPY } from '@/shared/components/RuntimeConnection/copy.ts';
import { setRuntimeAppUrl } from '@/integrations/runtime/runtimeAppUrl.ts';

let origin = '';
vi.mock('@/integrations/runtime/connection.ts', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/integrations/runtime/connection.ts')>()),
  runtimeOrigin: () => origin,
}));

vi.mock('@/shared/contexts/AgentChatContext', () => ({
  useAgentChatBridge: () => ({ timelineId: 'timeline-1', editorContext: { projectId: 'project-1' } }),
  useAgentChatActionsRegistry: () => null,
}));

import { AgentChatPanel } from './AgentChat.tsx';
import { isTimelineAgentSessionsAvailable, useProjectAgentTaskLinks } from '@/tools/video-editor/hooks/useAgentSession.ts';

const GATEWAY = 'http://127.0.0.1:17340';

function withQueryClient({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return React.createElement(QueryClientProvider, { client }, children);
}

describe('agent chat on the hosted build', () => {
  let fetchSpy: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchSpy = vi.fn(async () => new Response('{}', { status: 404 }));
    vi.stubGlobal('fetch', fetchSpy);
  });

  afterEach(() => {
    origin = '';
    setRuntimeAppUrl(null);
    vi.unstubAllGlobals();
  });

  it('says agent chat is not on this page yet, with an "Open the full editor" link only when the app address is known', () => {
    origin = GATEWAY;
    setRuntimeAppUrl('http://127.0.0.1:2222');
    const view = render(<AgentChatPanel />, { wrapper: withQueryClient });

    expect(screen.getByText("Agent chat isn't on this page yet.")).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open the full editor' })).toHaveAttribute('href', 'http://127.0.0.1:2222');
    expect(document.body.textContent).not.toContain('127.0.0.1');
    view.unmount();

    setRuntimeAppUrl(null);
    render(<AgentChatPanel />, { wrapper: withQueryClient });
    expect(screen.getByText("Agent chat isn't on this page yet.")).toBeInTheDocument();
    expect(screen.queryByRole('link')).toBeNull();
  });

  it('with a gateway origin, shows one quiet line, no alert, and requests nothing from the gateway', async () => {
    origin = GATEWAY;
    expect(isTimelineAgentSessionsAvailable()).toBe(false);

    render(<AgentChatPanel />, { wrapper: withQueryClient });
    // The project-chat poll runs on an interval; let the first query settle before asserting nothing was sent.
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(screen.getByText(RUNTIME_CONNECTION_COPY.agentChatDisabled)).toBeInTheDocument();
    expect(screen.queryByRole('alert')).toBeNull();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('with a gateway origin, the task-links poll does not request the project chat route', async () => {
    origin = GATEWAY;
    const { result } = renderHook(() => useProjectAgentTaskLinks('project-1'), { wrapper: withQueryClient });
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(result.current.fetchStatus).toBe('idle');
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('same-origin is unchanged: chat is available and no hosted line shows', () => {
    origin = '';
    expect(isTimelineAgentSessionsAvailable()).toBe(true);

    const { result } = renderHook(() => useProjectAgentTaskLinks('project-1'), { wrapper: withQueryClient });
    expect(result.current.fetchStatus).not.toBe('idle');
  });
});
