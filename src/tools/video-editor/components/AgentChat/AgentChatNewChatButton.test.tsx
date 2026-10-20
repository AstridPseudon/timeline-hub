// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { LOCAL_AGENT_IDS, LOCAL_AGENT_TABLE, type LocalAgentChoice } from '@/integrations/astrid/localAgents.ts';
import { AgentChatNewChatButton, type NewChatAgentModels } from './AgentChatNewChatButton.tsx';

beforeAll(() => {
  Element.prototype.scrollIntoView ??= vi.fn();
});
afterEach(cleanup);
const plainLine = (line: string) => line.replaceAll('`', '');

const ready: LocalAgentChoice[] = LOCAL_AGENT_IDS
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

  it.each(['sign-in', 'not-installed'] as const)('shows Hermes and opens the menu when the default agent is %s', (state) => {
    const onNewChat = vi.fn();
    render(<AgentChatNewChatButton defaultAgent="hermes" agents={[{ id: 'hermes', name: 'Hermes', state, line: state === 'sign-in' ? LOCAL_AGENT_TABLE.hermes.signInLine : LOCAL_AGENT_TABLE.hermes.notInstalledLine }]} onNewChat={onNewChat} />);
    expect(screen.getByRole('button', { name: 'New chat' })).toHaveAttribute('title', 'New chat with Hermes');
    fireEvent.click(screen.getByRole('button', { name: 'New chat' }));
    expect(onNewChat).not.toHaveBeenCalled();
    expect(screen.getByRole('option', { name: /Hermes/ })).toHaveTextContent(state === 'sign-in' ? 'Sign in' : 'Not installed');
  });

  it('does not copy or start a chat when a non-ready row is clicked', () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    const { onNewChat } = openMenu({ agents: [
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
    expect(writeText).not.toHaveBeenCalled();
    expect(onNewChat).not.toHaveBeenCalled();
    expect(claude).toHaveTextContent('Sign in');
  });

  it('copies only the command from its Copy button', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    const command = 'curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash';
    const { onNewChat } = openMenu({ agents: [
      { id: 'hermes', name: LOCAL_AGENT_TABLE.hermes.name, state: 'not-installed', line: LOCAL_AGENT_TABLE.hermes.notInstalledLine! },
    ] });
    const hermes = screen.getByRole('option', { name: /Hermes/ });
    const copyButton = within(hermes).getByRole('button', { name: 'Copy command' });
    expect(copyButton).toHaveAttribute('title', 'Copy command');
    expect(copyButton).toHaveAttribute('tabindex', '0');

    fireEvent.click(copyButton);

    await waitFor(() => expect(writeText).toHaveBeenCalledWith(command));
    expect(writeText).not.toHaveBeenCalledWith(expect.stringContaining('Install with'));
    expect(onNewChat).not.toHaveBeenCalled();
    expect(hermes).toHaveTextContent('Not installed');
  });

  it('gives each command in a line its own copy button', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    openMenu({ agents: [
      { id: 'astrid', name: LOCAL_AGENT_TABLE.astrid.name, state: 'sign-in', line: LOCAL_AGENT_TABLE.astrid.signInLine },
    ] });
    const astrid = screen.getByRole('option', { name: /Astrid/ });
    const buttons = within(astrid).getAllByRole('button', { name: 'Copy command' });
    expect(buttons).toHaveLength(2);

    fireEvent.click(buttons[0]);
    fireEvent.click(buttons[1]);

    await waitFor(() => expect(writeText).toHaveBeenNthCalledWith(2, '/login'));
    expect(writeText).toHaveBeenNthCalledWith(1, 'omp');
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

  it('starts Hermes directly and omits model drill-in until a model list is reported', () => {
    const { onNewChat } = openMenu({ defaultAgent: 'hermes', agentCanBrowse: { hermes: false } });
    expect(screen.getByRole('option', { name: /Hermes/ })).toHaveTextContent('Ready');
    expect(screen.queryByRole('button', { name: 'Choose a Hermes model' })).toBeNull();
    fireEvent.click(screen.getByRole('option', { name: /Hermes/ }));
    expect(onNewChat).toHaveBeenCalledWith('hermes', undefined);
  });

  it('does not enter Hermes model browsing with ArrowRight until models are reported', () => {
    const { onBrowseAgent } = openMenu({ defaultAgent: 'hermes', agentCanBrowse: { hermes: false } });
    fireEvent.keyDown(document.querySelector('[cmdk-root]') as HTMLElement, { key: 'ArrowRight' });
    expect(onBrowseAgent).not.toHaveBeenCalledWith('hermes');
    expect(screen.queryByPlaceholderText('Search Hermes models...')).toBeNull();
  });

  it('closes the Hermes model picker when a session reports an empty list', async () => {
    const { onNewChat, onBrowseAgent, view } = openMenu({ defaultAgent: 'hermes', agentCanBrowse: { hermes: true } });
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Hermes model' }));
    view.rerender(<AgentChatNewChatButton defaultAgent="hermes" agents={ready} onNewChat={onNewChat} onBrowseAgent={onBrowseAgent} agentCanBrowse={{ hermes: true }} agentModels={{ agent: 'hermes', models: [], loading: false }} />);
    await waitFor(() => expect(screen.queryByPlaceholderText('Search Hermes models...')).toBeNull());
    expect(onBrowseAgent).toHaveBeenLastCalledWith(null);
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

  const effortModels = {
    agent: 'claude-code' as const, defaultModel: 'opus', loading: false,
    models: [{ id: 'opus', name: 'Opus', thoughtLevel: { configId: 'effort', name: 'Effort', currentValue: 'low', recommendedValue: 'high',
      options: [{ value: 'low', name: 'Low' }, { value: 'high', name: 'High' }] } }],
  };

  it('starts immediately from a model with the recommended effort', async () => {
    const { onNewChat } = openMenu({ agentModels: effortModels });
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Claude Code model' }));
    await waitFor(() => expect(screen.getByRole('option', { name: /Opus/ })).toHaveAttribute('aria-selected', 'true'));
    fireEvent.keyDown(document.querySelector('[cmdk-root]')!, { key: 'Enter' });
    expect(onNewChat).toHaveBeenCalledWith('claude-code', 'opus', 'high');
  });

  it('opens levels with →, lands on the recommendation, returns with ← and picks another level', async () => {
    const { onNewChat } = openMenu({ agentModels: effortModels });
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Claude Code model' }));
    await waitFor(() => expect(screen.getByRole('option', { name: /Opus/ })).toHaveAttribute('aria-selected', 'true'));
    fireEvent.keyDown(document.querySelector('[cmdk-root]')!, { key: 'ArrowRight' });
    const high = screen.getByRole('option', { name: /High/ });
    expect(high).toHaveAttribute('aria-current', 'true');
    await waitFor(() => expect(high).toHaveAttribute('aria-selected', 'true'));
    expect(screen.queryByRole('combobox')).toBeNull();
    fireEvent.keyDown(document.activeElement!, { key: 'ArrowLeft' });
    await waitFor(() => expect(screen.getByRole('option', { name: /Opus/ })).toHaveAttribute('aria-selected', 'true'));
    fireEvent.click(screen.getByRole('button', { name: 'Choose a thinking level for Opus' }));
    fireEvent.click(screen.getByRole('option', { name: 'Low' }));
    expect(onNewChat).toHaveBeenCalledWith('claude-code', 'opus', 'low');
  });

  it('defaults to the reported Default row without a recommendation', () => {
    const { onNewChat } = openMenu({ agentModels: { ...effortModels, models: [{ id: 'opus', name: 'Opus', thoughtLevel: {
      configId: 'effort', name: 'Effort', currentValue: 'high', options: [{ value: 'default', name: 'Default' }, { value: 'high', name: 'High' }],
    } }] } });
    fireEvent.click(screen.getByRole('button', { name: 'Choose a Claude Code model' }));
    fireEvent.click(screen.getByRole('option', { name: /Opus/ }));
    expect(onNewChat).toHaveBeenCalledWith('claude-code', 'opus', 'default');
  });

  it.each(['hermes', 'astrid'] as const)('shows no level step for %s models without levels', agent => {
    const { onNewChat } = openMenu({ agentModels: { agent, loading: false, models: [{ id: 'a', name: 'Model A' }] } });
    fireEvent.click(screen.getByRole('button', { name: `Choose a ${LOCAL_AGENT_TABLE[agent].name} model` }));
    expect(screen.queryByRole('button', { name: /Choose a thinking level/ })).toBeNull();
    fireEvent.click(screen.getByRole('option', { name: 'Model A' }));
    expect(onNewChat).toHaveBeenCalledWith(agent, 'a');
  });
});
