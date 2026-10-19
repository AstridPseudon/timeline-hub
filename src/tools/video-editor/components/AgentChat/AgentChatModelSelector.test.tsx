// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AgentChatModelSelector } from './AgentChatModelSelector.tsx';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';
import type { LocalAgentChoice } from '@/integrations/astrid/localAgents.ts';

afterEach(cleanup);

const catalog: AcpModelCatalog = {
  currentModel: 'openai/gpt-5',
  providers: [
    { id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-5', name: 'GPT 5' }, { id: 'gpt-5-mini', name: 'GPT 5 Mini' }] },
    { id: 'anthropic', name: 'Anthropic', signedIn: false, models: [] },
  ],
};

const agents: LocalAgentChoice[] = [
  { id: 'claude-code', name: 'Claude Code', installed: true, authStatus: 'signed-in', adapterInstalled: false, installCommand: 'astrid adapters install claude-code', loginCommand: 'claude auth login' },
  { id: 'codex', name: 'Codex', installed: true, authStatus: 'signed-in', adapterInstalled: true, installCommand: null, loginCommand: null },
];

describe('AgentChatModelSelector', () => {
  it('offers usable keyless models without requiring a provider sign-in', () => {
    const onSelectModel = vi.fn();
    render(<AgentChatModelSelector catalog={{ currentModel: null, providers: [
      { id: 'local', name: 'Local models', signedIn: false, models: [{ id: 'llama', name: 'Llama' }] },
    ] }} onSelectModel={onSelectModel} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
    fireEvent.click(screen.getByRole('button', { name: 'Llama' }));
    expect(onSelectModel).toHaveBeenCalledWith('local/llama');
  });

  it('opens provider groups, marks the active model, and selects exact provider/model ids', async () => {
    const onSelectModel = vi.fn();
    const onOpenChange = vi.fn();
    render(<AgentChatModelSelector catalog={catalog} onSelectModel={onSelectModel} onOpenChange={onOpenChange} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
    expect(onOpenChange).toHaveBeenCalledWith(true);
    expect(await screen.findByText((_, element) => element?.tagName === 'P' && element.textContent?.includes('Sign in: run') === true)).toBeTruthy();
    expect(screen.getByRole('button', { name: /GPT 5$/ }).getAttribute('aria-current')).toBe('true');
    fireEvent.click(screen.getByRole('button', { name: /GPT 5 Mini$/ }));
    await waitFor(() => expect(onSelectModel).toHaveBeenCalledWith('openai/gpt-5-mini'));
  });

  it('shows a selection failure inline with a Switch model action that opens the list', async () => {
    render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} selectionError="Provider quota exceeded" />);
    expect(screen.getByRole('alert').textContent).toContain('Provider quota exceeded');
    fireEvent.click(screen.getByRole('button', { name: 'Switch model' }));
    expect(await screen.findByText('OpenAI')).toBeTruthy();
  });

  it('shows unavailable agent states and the exact adapter install and login commands', () => {
    const unavailable: LocalAgentChoice[] = [
      { id: 'claude-code', name: 'Claude Code', installed: true, authStatus: 'signed-in', adapterInstalled: false, installCommand: 'astrid adapter install claude-code --exact', loginCommand: 'claude auth login' },
      { id: 'codex', name: 'Codex', installed: true, authStatus: 'signed-out', adapterInstalled: false, installCommand: 'astrid adapter install codex --exact', loginCommand: 'codex login --browser' },
    ];
    render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={unavailable} onSelectAgent={vi.fn()} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
    expect(screen.getAllByText('Available to install')).toHaveLength(2);
    expect(screen.getByText('astrid adapter install claude-code --exact')).toBeTruthy();
    expect(screen.getByText('Your Claude login · Signed in')).toBeTruthy();
    expect(screen.queryByText('claude auth login')).toBeNull();
    expect(screen.getByRole('button', { name: /Claude Code/ })).toBeDisabled();
    expect(screen.getByText('Your ChatGPT login · Signed out')).toBeTruthy();
    expect(screen.getByText('astrid adapter install codex --exact')).toBeTruthy();
    expect(screen.getByText('codex login --browser')).toBeTruthy();
    expect(screen.getByRole('button', { name: /Codex/ })).toBeDisabled();
  });

  it('keeps missing, unknown-auth, and busy agents disabled', () => {
    const unknown: LocalAgentChoice[] = [
      { id: 'claude-code', name: 'Claude Code', installed: false, authStatus: 'unknown', adapterInstalled: false, installCommand: null, loginCommand: null },
      { id: 'codex', name: 'Codex', installed: true, authStatus: 'unknown', adapterInstalled: true, installCommand: null, loginCommand: null },
    ];
    const { rerender } = render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={unknown} onSelectAgent={vi.fn()} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
    expect(screen.getByText('CLI not installed')).toBeTruthy();
    expect(screen.getByText('Sign-in status unknown')).toBeTruthy();
    expect(screen.getByRole('button', { name: /Claude Code/ })).toBeDisabled();
    expect(screen.getByRole('button', { name: /Codex/ })).toBeDisabled();
    rerender(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={agents} onSelectAgent={vi.fn()} busy />);
    expect(screen.getByRole('button', { name: /Codex/ })).toBeDisabled();
  });

  it('selects a ready external agent, closes the picker, and hides OMP models', async () => {
    const onSelectAgent = vi.fn();
    const { rerender } = render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={agents} onSelectAgent={onSelectAgent} />);
    const trigger = screen.getByRole('combobox', { name: 'Agent model' });
    fireEvent.click(trigger);
    expect(await screen.findByText('OpenAI')).toBeTruthy();
    expect(screen.getByText('OMP models')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /Codex/ }));
    await waitFor(() => expect(onSelectAgent).toHaveBeenCalledWith('codex'));
    rerender(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={agents} onSelectAgent={onSelectAgent} selectedAgent="codex" />);
    expect(trigger.textContent).toContain('Codex');
    expect(trigger.getAttribute('aria-expanded')).toBe('false');
    fireEvent.click(trigger);
    expect(await screen.findByText('Uses your Codex default model. New chats use this agent; saved chats keep their original agent.')).toBeTruthy();
    expect(screen.queryByText('OpenAI')).toBeNull();
    expect(screen.queryByRole('button', { name: /GPT 5/ })).toBeNull();
  });
});
