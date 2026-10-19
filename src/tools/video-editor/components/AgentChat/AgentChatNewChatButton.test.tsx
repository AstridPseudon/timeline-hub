// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import type { LocalAgentChoice } from '@/integrations/astrid/localAgents.ts';
import { AgentChatNewChatButton, type NewChatAgentModels } from './AgentChatNewChatButton.tsx';

beforeAll(() => {
  Element.prototype.scrollIntoView ??= vi.fn();
});
afterEach(cleanup);

const ready: LocalAgentChoice[] = [
  { id: 'claude-code', name: 'Claude Code', installed: true, authStatus: 'signed-in', adapterInstalled: true, installCommand: null, loginCommand: null },
  { id: 'codex', name: 'Codex', installed: true, authStatus: 'signed-in', adapterInstalled: true, installCommand: null, loginCommand: null },
];
const claudeModels: NewChatAgentModels = {
  agent: 'claude-code',
  defaultModel: 'sonnet',
  loading: false,
  models: [
    { id: 'opus', name: 'Opus', detail: 'For complex work' },
    { id: 'sonnet', name: 'Sonnet', detail: 'Most efficient' },
  ],
};

function openMenu(props: Partial<Parameters<typeof AgentChatNewChatButton>[0]> = {}) {
  const onNewChat = vi.fn();
  const onBrowseAgent = vi.fn();
  const view = render(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} astridSignedIn onNewChat={onNewChat} onBrowseAgent={onBrowseAgent} {...props} />);
  fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
  return { onNewChat, onBrowseAgent, view };
}

describe('AgentChatNewChatButton', () => {
  it('starts a chat with the last-used agent from the main click', () => {
    const onNewChat = vi.fn();
    render(<AgentChatNewChatButton defaultAgent="codex" agents={ready} astridSignedIn onNewChat={onNewChat} />);
    const main = screen.getByRole('button', { name: 'New chat' });
    expect(main).toHaveAttribute('title', 'New chat with Codex');
    fireEvent.click(main);
    expect(onNewChat).toHaveBeenCalledWith();
  });

  it('shows unavailable agent states and the exact adapter install and login commands', () => {
    openMenu({ agents: [
      { id: 'claude-code', name: 'Claude Code', installed: true, authStatus: 'signed-in', adapterInstalled: false, installCommand: 'astrid adapter install claude-code --exact', loginCommand: 'claude auth login' },
      { id: 'codex', name: 'Codex', installed: true, authStatus: 'signed-out', adapterInstalled: false, installCommand: 'astrid adapter install codex --exact', loginCommand: 'codex login --browser' },
    ] });
    expect(screen.getAllByText('Available to install')).toHaveLength(2);
    expect(screen.getByText('astrid adapter install claude-code --exact')).toBeTruthy();
    expect(screen.getByText('Your Claude login · Signed in')).toBeTruthy();
    expect(screen.queryByText('claude auth login')).toBeNull();
    expect(screen.getByRole('option', { name: /Claude Code/ })).toHaveAttribute('aria-disabled', 'true');
    expect(screen.getByText('Your ChatGPT login · Signed out')).toBeTruthy();
    expect(screen.getByText('astrid adapter install codex --exact')).toBeTruthy();
    expect(screen.getByText('codex login --browser')).toBeTruthy();
    expect(screen.getByRole('option', { name: /Codex/ })).toHaveAttribute('aria-disabled', 'true');
  });

  it('allows installed agents with unknown sign-in, keeps missing CLIs disabled, and starts the chosen agent', async () => {
    const { onNewChat } = openMenu({ agents: [
      { id: 'claude-code', name: 'Claude Code', installed: false, authStatus: 'unknown', adapterInstalled: false, installCommand: null, loginCommand: null },
      { id: 'codex', name: 'Codex', installed: true, authStatus: 'unknown', adapterInstalled: true, installCommand: null, loginCommand: null },
    ] });
    expect(screen.getByText('CLI not installed')).toBeTruthy();
    expect(screen.getByText('Sign-in status unknown')).toBeTruthy();
    expect(screen.getByRole('option', { name: /Claude Code/ })).toHaveAttribute('aria-disabled', 'true');
    fireEvent.click(screen.getByRole('option', { name: /Codex/ }));
    await waitFor(() => expect(onNewChat).toHaveBeenCalledWith('codex', undefined));
    expect(screen.queryByRole('option', { name: /Codex/ })).toBeNull();
  });

  it('disables both halves while a chat cannot start', () => {
    render(<AgentChatNewChatButton defaultAgent="astrid" agents={ready} astridSignedIn onNewChat={vi.fn()} disabled />);
    expect(screen.getByRole('button', { name: 'New chat' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'New chat with…' })).toBeDisabled();
  });

  it('opens an agent\'s models with → and starts the chat with the picked model', async () => {
    const { onNewChat, onBrowseAgent, view } = openMenu();
    const list = document.querySelector('[cmdk-root]') as HTMLElement;
    expect(screen.getByRole('option', { name: /Claude Code/ })).toHaveAttribute('aria-selected', 'true');
    fireEvent.keyDown(list, { key: 'ArrowRight' });
    expect(onBrowseAgent).toHaveBeenLastCalledWith('claude-code');
    expect(screen.getByText('Loading models...')).toBeTruthy();
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} astridSignedIn onNewChat={onNewChat} onBrowseAgent={onBrowseAgent} agentModels={claudeModels} />);
    expect(screen.getByRole('option', { name: /Sonnet/ })).toHaveAttribute('aria-current', 'true');
    await waitFor(() => expect(screen.getByRole('option', { name: /Sonnet/ })).toHaveAttribute('aria-selected', 'true'));
    fireEvent.click(screen.getByRole('option', { name: /Opus/ }));
    expect(onNewChat).toHaveBeenCalledWith('claude-code', 'opus');
  });

  it('opens a submenu from the row arrow, searches it, and goes back with ←', () => {
    const { onBrowseAgent, view } = openMenu();
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Claude Code model' }));
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} astridSignedIn onNewChat={vi.fn()} onBrowseAgent={onBrowseAgent} agentModels={claudeModels} />);
    const search = screen.getByPlaceholderText('Search Claude Code models...');
    fireEvent.change(search, { target: { value: 'complex' } });
    expect(screen.getByRole('option', { name: /Opus/ })).toBeTruthy();
    expect(screen.queryByRole('option', { name: /Sonnet/ })).toBeNull();
    fireEvent.change(search, { target: { value: '' } });
    fireEvent.keyDown(search, { key: 'ArrowLeft' });
    expect(onBrowseAgent).toHaveBeenLastCalledWith(null);
    expect(screen.getByRole('option', { name: /Codex/ })).toBeTruthy();
  });

  it('explains when an agent has not reported its models yet', () => {
    const { view } = openMenu();
    fireEvent.keyDown(document.querySelector('[cmdk-root]') as HTMLElement, { key: 'ArrowRight' });
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} astridSignedIn onNewChat={vi.fn()} agentModels={{ agent: 'claude-code', models: [], loading: false, note: 'Start one first.' }} />);
    expect(screen.getByText('Start one first.')).toBeTruthy();
  });

  it('keeps attaching an existing chat in the same menu', () => {
    const toggle = vi.fn();
    openMenu({ attachExisting: { open: false, toggle } });
    fireEvent.click(screen.getByRole('option', { name: /Attach an existing chat/ }));
    expect(toggle).toHaveBeenCalledOnce();
  });
});
