import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useSendMessage } from './useAgentSession.ts';

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('cut timeline-agent proposal vertical', () => {
  it('does not prompt or apply an edge proposal when ACP is unavailable', async () => {
    const queryClient = new QueryClient();
    const proposalApply = vi.fn();
    const request = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/acp/projects/project-1/chat')) {
        return new Response(JSON.stringify({ error: 'acp_unavailable', detail: 'No ACP service is available.' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' },
        });
      }
      throw new Error(`Unexpected bridge request while ACP is unavailable: ${url}`);
    });
    vi.stubGlobal('fetch', request);
    const context = {
      tool: 'video-editor' as const,
      projectId: 'project-1',
      projectSlug: 'project-one',
      timelineId: 'tl-1',
      timelineName: 'Timeline',
      elementOperationAdapter: { execute: proposalApply },
    };
    const { result, unmount } = renderHook(() => useSendMessage('session-1', context, 'project-1'), {
      wrapper: ({ children }: { children: React.ReactNode }) => React.createElement(
        QueryClientProvider,
        { client: queryClient },
        children,
      ),
    });

    let mutationError: unknown;
    try {
      await act(async () => {
        try {
          await result.current.mutateAsync({ input: { message: 'apply proposal' }, projectId: 'project-1', sessionId: 'session-1', context });
        } catch (error) { mutationError = error; }
      });
      expect(mutationError).toMatchObject({ code: 'acp_unavailable', status: 503 });
      expect(request).toHaveBeenCalledTimes(1);
      expect(String(request.mock.calls[0]?.[0])).toMatch(/\/acp\/projects\/project-1\/chat$/);
    } finally {
      unmount();
    }
    expect(request.mock.calls.some(([input]) => String(input).endsWith('/acp/projects/project-1/chat/prompt'))).toBe(false);
    expect(proposalApply).not.toHaveBeenCalled();
  });
});
