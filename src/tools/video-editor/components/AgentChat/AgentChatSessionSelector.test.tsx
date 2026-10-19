// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { AgentChatSessionSelector } from './AgentChatSessionSelector.tsx';

beforeAll(() => {
  Element.prototype.scrollIntoView ??= vi.fn();
});
afterEach(cleanup);

describe('AgentChatSessionSelector', () => {
  it('shows each chat\'s agent and last model under its title, and the agent alone when the model is unknown', async () => {
    const describeSession = (id: string) => id === 'codex:one'
      ? { agent: 'codex' as const, model: '6 Sol' }
      : { agent: 'claude-code' as const, model: null };
    render(<AgentChatSessionSelector sessions={[{ id: 'codex:one' }, { id: 'claude-code:two' }]} activeSessionId="codex:one" onSelectSession={vi.fn()} describeSession={describeSession} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Project chat session' }));
    expect(await screen.findByText('Codex · 6 Sol')).toBeTruthy();
    expect(screen.getByText('Claude Code')).toBeTruthy();
    fireEvent.change(screen.getByPlaceholderText('Search chats...'), { target: { value: 'codex' } });
    expect(screen.getByRole('option', { name: /^Chat 1/ })).toBeTruthy();
    expect(screen.queryByRole('option', { name: /^Chat 2/ })).toBeNull();
  });
});
