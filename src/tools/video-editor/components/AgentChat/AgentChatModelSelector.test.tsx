// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { AgentChatModelSelector, summarizeUsage } from './AgentChatModelSelector.tsx';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';
import type { LocalAgentChoice } from '@/integrations/astrid/localAgents.ts';

beforeAll(() => {
  // cmdk keeps the highlighted option in view while arrowing; jsdom has no layout.
  Element.prototype.scrollIntoView ??= vi.fn();
});
afterEach(cleanup);

const catalog: AcpModelCatalog = {
  currentModel: 'openai/gpt-5',
  providers: [
    { id: 'anthropic', name: 'Anthropic', signedIn: false, models: [] },
    { id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-5', name: 'GPT 5' }, { id: 'gpt-5-mini', name: 'GPT 5 Mini' }],
      usage: { limits: [{ unit: 'requests', used: 12, limit: 100, usedFraction: 0.12, durationMs: 3_600_000, status: 'ok' }] } },
  ],
};

const agents: LocalAgentChoice[] = [
  { id: 'claude-code', name: 'Claude Code', installed: true, authStatus: 'signed-in', adapterInstalled: false, installCommand: 'astrid adapters install claude-code', loginCommand: 'claude auth login' },
  { id: 'codex', name: 'Codex', installed: true, authStatus: 'signed-in', adapterInstalled: true, installCommand: null, loginCommand: null },
];

function openList(onSelectModel = vi.fn(), onOpenChange = vi.fn()) {
  render(<AgentChatModelSelector catalog={catalog} onSelectModel={onSelectModel} onOpenChange={onOpenChange} />);
  fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
  return { onSelectModel, onOpenChange };
}

describe('AgentChatModelSelector', () => {
  it('offers usable keyless models without requiring a provider sign-in', async () => {
    const onSelectModel = vi.fn();
    render(<AgentChatModelSelector catalog={{ currentModel: null, providers: [
      { id: 'local', name: 'Local models', signedIn: false, models: [{ id: 'llama', name: 'Llama' }] },
    ] }} onSelectModel={onSelectModel} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
    expect(screen.queryByText('Not signed in')).toBeNull();
    fireEvent.click(await screen.findByRole('option', { name: /Llama$/ }));
    expect(onSelectModel).toHaveBeenCalledWith('local/llama');
  });

  it('lists signed-in providers first, marks the active model, and selects exact provider/model ids', async () => {
    const { onSelectModel, onOpenChange } = openList();
    expect(onOpenChange).toHaveBeenCalledWith(true);
    const current = await screen.findByRole('option', { name: /GPT 5$/ });
    expect(current.getAttribute('aria-current')).toBe('true');
    expect(screen.getByText('12% used')).toBeTruthy();
    fireEvent.click(screen.getByRole('option', { name: /GPT 5 Mini$/ }));
    await waitFor(() => expect(onSelectModel).toHaveBeenCalledWith('openai/gpt-5-mini'));
  });

  it('keeps signed-out providers secondary behind one sign-in hint', async () => {
    openList();
    expect(await screen.findByText('Not signed in')).toBeTruthy();
    expect(screen.getByText((_, element) => element?.tagName === 'P' && element.textContent === 'To sign in, run omp then /login.')).toBeTruthy();
    expect(screen.queryByRole('option', { name: 'Anthropic' })).toBeNull();
    fireEvent.click(screen.getByRole('option', { name: /Show all/ }));
    expect(screen.getByRole('option', { name: 'Anthropic' }).getAttribute('aria-disabled')).toBe('true');
  });

  it('finds signed-out providers by search', async () => {
    openList();
    fireEvent.change(await screen.findByPlaceholderText('Search models...'), { target: { value: 'anthro' } });
    expect(await screen.findByRole('option', { name: 'Anthropic' })).toBeTruthy();
    expect(screen.queryByRole('option', { name: /GPT 5$/ })).toBeNull();
  });

  it('starts on the current model and moves with the arrow keys', async () => {
    const { onSelectModel } = openList();
    const input = await screen.findByPlaceholderText('Search models...');
    expect(screen.getByRole('option', { name: /GPT 5$/ }).getAttribute('aria-selected')).toBe('true');
    fireEvent.keyDown(input, { key: 'ArrowDown' });
    expect(screen.getByRole('option', { name: /GPT 5 Mini$/ }).getAttribute('aria-selected')).toBe('true');
    fireEvent.keyDown(input, { key: 'Enter' });
    await waitFor(() => expect(onSelectModel).toHaveBeenCalledWith('openai/gpt-5-mini'));
  });

  it('folds a large keyless catalog into one row per provider, with search across every model', async () => {
    const many = (prefix: string, count: number) => Array.from({ length: count }, (_, index) => ({ id: `${prefix}-${index}`, name: `${prefix} ${index}` }));
    render(<AgentChatModelSelector onSelectModel={vi.fn()} catalog={{ currentModel: 'gateway/gateway-7', providers: [
      ...catalog.providers,
      { id: 'gateway', name: 'Gateway', signedIn: false, models: many('gateway', 30) },
      { id: 'router', name: 'Router', signedIn: false, models: many('router', 30) },
    ] }} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
    expect(await screen.findByText('Other providers')).toBeTruthy();
    // The current model's provider opens on its own; the others stay one row.
    expect(screen.getByRole('option', { name: /gateway 7$/ }).getAttribute('aria-current')).toBe('true');
    expect(screen.queryByRole('option', { name: /router 3$/ })).toBeNull();
    fireEvent.click(screen.getByRole('option', { name: /Router/ }));
    expect(screen.getByRole('option', { name: /router 3$/ })).toBeTruthy();
    fireEvent.change(screen.getByPlaceholderText('Search models...'), { target: { value: 'router 2' } });
    expect(screen.getByRole('option', { name: /router 29$/ })).toBeTruthy();
    expect(screen.queryByRole('option', { name: /gateway/ })).toBeNull();
    fireEvent.change(screen.getByPlaceholderText('Search models...'), { target: { value: 't' } });
    expect(screen.getByText('Showing 50 of 62 matches. Keep typing to narrow.')).toBeTruthy();
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
    expect(screen.getByRole('option', { name: /Claude Code/ })).toHaveAttribute('aria-disabled', 'true');
    expect(screen.getByText('Your ChatGPT login · Signed out')).toBeTruthy();
    expect(screen.getByText('astrid adapter install codex --exact')).toBeTruthy();
    expect(screen.getByText('codex login --browser')).toBeTruthy();
    expect(screen.getByRole('option', { name: /Codex/ })).toHaveAttribute('aria-disabled', 'true');
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
    expect(screen.getByRole('option', { name: /Claude Code/ })).toHaveAttribute('aria-disabled', 'true');
    expect(screen.getByRole('option', { name: /Codex/ })).toHaveAttribute('aria-disabled', 'true');
    rerender(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={agents} onSelectAgent={vi.fn()} busy />);
    expect(screen.getByRole('option', { name: /Codex/ })).toHaveAttribute('aria-disabled', 'true');
  });

  it('selects a ready external agent, closes the picker, and hides OMP models', async () => {
    const onSelectAgent = vi.fn();
    const { rerender } = render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={agents} onSelectAgent={onSelectAgent} />);
    const trigger = screen.getByRole('combobox', { name: 'Agent model' });
    fireEvent.click(trigger);
    expect(await screen.findByText('OpenAI')).toBeTruthy();
    expect(screen.getByText('OMP models')).toBeTruthy();
    fireEvent.click(screen.getByRole('option', { name: /Codex/ }));
    await waitFor(() => expect(onSelectAgent).toHaveBeenCalledWith('codex'));
    rerender(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} agents={agents} onSelectAgent={onSelectAgent} selectedAgent="codex" />);
    expect(trigger.textContent).toContain('Codex');
    expect(trigger.getAttribute('aria-expanded')).toBe('false');
    fireEvent.click(trigger);
    expect(await screen.findByText('Uses your Codex default model. New chats use this agent; saved chats keep their original agent.')).toBeTruthy();
    expect(screen.queryByText('OpenAI')).toBeNull();
    expect(screen.queryByRole('option', { name: /GPT 5/ })).toBeNull();
  });

  it('lets a selection failure be dismissed', () => {
    render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} selectionError="Provider quota exceeded" />);
    fireEvent.click(screen.getByRole('button', { name: 'Dismiss' }));
    expect(screen.queryByRole('alert')).toBeNull();
  });
});

describe('summarizeUsage', () => {
  it('reports the tightest limit and its tone', () => {
    expect(summarizeUsage(undefined)).toBeNull();
    expect(summarizeUsage({ limits: [{ unit: 'tokens' }] })).toBeNull();
    expect(summarizeUsage({ limits: [{ usedFraction: 0.2 }, { remainingFraction: 0.1, status: 'warning' }] })).toMatchObject({ text: '90% used', tone: 'warning' });
    expect(summarizeUsage({ limits: [{ used: 5, limit: 50 }, { status: 'exhausted' }] })).toMatchObject({ text: 'Limit reached', tone: 'exhausted' });
    expect(summarizeUsage({ limits: [{ usedFraction: 0.42, durationMs: 18_000_000 }] })).toMatchObject({ text: '42% used', tone: 'ok', detail: '42% of 5-hour limit used' });
  });
});
