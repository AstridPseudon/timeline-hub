// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { LOCAL_AGENT_TABLE, type LocalAgentChoice } from '@/integrations/astrid/localAgents.ts';
import { AgentChatNewChatButton, type NewChatAgentModels } from './AgentChatNewChatButton.tsx';

beforeAll(() => {
  Element.prototype.scrollIntoView ??= vi.fn();
});
afterEach(cleanup);
const plainLine = (line: string) => line.replaceAll('`', '');

const ready: LocalAgentChoice[] = (['astrid', 'claude-code', 'codex'] as const)
  .map(id => ({ id, name: LOCAL_AGENT_TABLE[id].name, state: 'ready', line: null }));
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
  const view = render(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} onNewChat={onNewChat} onBrowseAgent={onBrowseAgent} {...props} />);
  fireEvent.click(screen.getByRole('button', { name: 'New chat with…' }));
  return { onNewChat, onBrowseAgent, view };
}

describe('AgentChatNewChatButton', () => {
  it('starts a chat with the last-used agent from the main click', () => {
    const onNewChat = vi.fn();
    render(<AgentChatNewChatButton defaultAgent="codex" agents={ready} onNewChat={onNewChat} />);
    const main = screen.getByRole('button', { name: 'New chat' });
    expect(main).toHaveAttribute('title', 'New chat with Codex');
    fireEvent.click(main);
    expect(onNewChat).toHaveBeenCalledWith();
  });

  it('copies the service line for every non-ready row without disabling it', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    openMenu({ agents: [
      { id: 'astrid', name: LOCAL_AGENT_TABLE.astrid.name, state: 'sign-in', line: LOCAL_AGENT_TABLE.astrid.signInLine },
      { id: 'claude-code', name: LOCAL_AGENT_TABLE['claude-code'].name, state: 'sign-in', line: LOCAL_AGENT_TABLE['claude-code'].signInLine },
      { id: 'codex', name: LOCAL_AGENT_TABLE.codex.name, state: 'not-installed', line: LOCAL_AGENT_TABLE.codex.notInstalledLine! },
    ] });
    const astrid = screen.getByRole('option', { name: /Astrid/ });
    const claude = screen.getByRole('option', { name: /Claude Code/ });
    const codex = screen.getByRole('option', { name: /Codex/ });
    expect(astrid).toHaveTextContent('Sign in');
    expect(astrid).toHaveTextContent(plainLine(LOCAL_AGENT_TABLE.astrid.signInLine));
    expect(claude).toHaveTextContent(plainLine(LOCAL_AGENT_TABLE['claude-code'].signInLine));
    expect(codex).toHaveTextContent('Not installed');
    expect(codex).toHaveTextContent(plainLine(LOCAL_AGENT_TABLE.codex.notInstalledLine!));
    for (const row of [astrid, claude, codex]) expect(row).not.toHaveAttribute('aria-disabled', 'true');
    fireEvent.click(claude);
    await waitFor(() => expect(writeText).toHaveBeenCalledWith(plainLine(LOCAL_AGENT_TABLE['claude-code'].signInLine)));
    expect(await screen.findByText('Copied')).toBeTruthy();
  });

  it('starts ready agents and treats unknown sign-in as ready', async () => {
    const { onNewChat } = openMenu({ agents: [
      { id: 'claude-code', name: LOCAL_AGENT_TABLE['claude-code'].name, state: 'not-installed', line: LOCAL_AGENT_TABLE['claude-code'].notInstalledLine! },
      { id: 'codex', name: LOCAL_AGENT_TABLE.codex.name, state: 'ready', line: null },
    ] });
    expect(screen.getByRole('option', { name: /Claude Code/ })).not.toHaveAttribute('aria-disabled', 'true');
    expect(screen.getByRole('option', { name: /Codex/ })).toHaveTextContent('Ready');
    fireEvent.click(screen.getByRole('option', { name: /Codex/ }));
    await waitFor(() => expect(onNewChat).toHaveBeenCalledWith('codex', undefined));
    expect(screen.queryByRole('option', { name: /Codex/ })).toBeNull();
  });

  it('shows a known current model on the ready row', () => {
    openMenu({ agentModelNames: { 'claude-code': 'Sonnet 4.5' } });
    expect(screen.getByLabelText('Ready, using Sonnet 4.5')).toHaveTextContent('Sonnet 4.5');
  });

  it('disables both halves while a chat cannot start', () => {
    render(<AgentChatNewChatButton defaultAgent="astrid" agents={ready} onNewChat={vi.fn()} disabled />);
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
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} onNewChat={onNewChat} onBrowseAgent={onBrowseAgent} agentModels={claudeModels} />);
    expect(screen.getByRole('option', { name: /Sonnet/ })).toHaveAttribute('aria-current', 'true');
    await waitFor(() => expect(screen.getByRole('option', { name: /Sonnet/ })).toHaveAttribute('aria-selected', 'true'));
    fireEvent.click(screen.getByRole('option', { name: /Opus/ }));
    expect(onNewChat).toHaveBeenCalledWith('claude-code', 'opus');
  });

  it('opens a submenu from the row arrow, searches it, and goes back with ←', () => {
    const { onBrowseAgent, view } = openMenu();
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Claude Code model' }));
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} onNewChat={vi.fn()} onBrowseAgent={onBrowseAgent} agentModels={claudeModels} />);
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
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} onNewChat={vi.fn()} agentModels={{ agent: 'claude-code', models: [], loading: false, note: 'Start one first.' }} />);
    expect(screen.getByText('Start one first.')).toBeTruthy();
  });

  it('shows the Astrid sign-in command at the foot of its model list', () => {
    const { onBrowseAgent, view } = openMenu();
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Astrid model' }));
    view.rerender(<AgentChatNewChatButton defaultAgent="claude-code" agents={ready} onNewChat={vi.fn()} onBrowseAgent={onBrowseAgent} agentModels={{ agent: 'astrid', models: [], loading: false, note: 'No models available.' }} />);
    const [omp, login] = Array.from(LOCAL_AGENT_TABLE.astrid.signInLine.matchAll(/`([^`]+)`/g), match => match[1]);
    expect(screen.getByText((_text, element) => element?.textContent === `More models: run ${omp}, then ${login}.`)).toBeTruthy();
  });

  it('keeps attaching an existing chat in the same menu', () => {
    const toggle = vi.fn();
    openMenu({ attachExisting: { open: false, toggle } });
    fireEvent.click(screen.getByRole('option', { name: /Attach an existing chat/ }));
    expect(toggle).toHaveBeenCalledOnce();
  });
});
