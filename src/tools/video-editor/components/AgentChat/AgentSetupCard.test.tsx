// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { LOCAL_AGENT_IDS, LOCAL_AGENT_TABLE, type LocalAgentChoice } from '@/integrations/astrid/localAgents.ts';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';
import { BridgeRouteError } from '@/integrations/astrid/transport.ts';
import { AgentSetupCard } from './AgentSetupCard';

const mocks = vi.hoisted(() => ({ models: vi.fn(), saveKey: vi.fn(), readChoice: vi.fn(), remember: vi.fn() }));
vi.mock('@/integrations/astrid/client.ts', () => ({ AstridLocalClient: class { acp = { models: mocks.models, saveAstridApiKey: mocks.saveKey }; } }));
vi.mock('./newChatThinkingSelection', () => ({ readNewChatChoice: mocks.readChoice, rememberNewChatChoice: mocks.remember }));
const clients: QueryClient[] = [];
const ready = (): LocalAgentChoice[] => LOCAL_AGENT_IDS.map(id => ({ id, name: LOCAL_AGENT_TABLE[id].name, state: 'ready', signIn: 'signed-in', line: null, models: [], defaultModel: null }));
const catalog = (): AcpModelCatalog => ({ providers: [
  { id: 'other', name: 'Other account', signedIn: false, models: [{ id: 'model', name: 'Unavailable model' }] },
  { id: 'openrouter', name: 'OpenRouter', signedIn: true, models: [{ id: 'first', name: 'First model' }, { id: 'default', name: 'Default model' }] },
  { id: 'claude', name: 'Claude', signedIn: true, models: [{ id: 'sonnet', name: 'Sonnet' }] },
], currentModel: 'openrouter/default' });
function mount(props: Partial<React.ComponentProps<typeof AgentSetupCard>> = {}) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: 0 } } });
  clients.push(client);
  const base = { agents: ready(), defaultAgent: 'astrid' as const, refetchAgents: vi.fn().mockResolvedValue(undefined), startChatWith: vi.fn().mockResolvedValue(undefined), onComplete: vi.fn(), ...props };
  const view = render(<QueryClientProvider client={client}><AgentSetupCard {...base} /></QueryClientProvider>);
  return { ...base, ...view, rerenderCard: (next: Partial<typeof base>) => view.rerender(<QueryClientProvider client={client}><AgentSetupCard {...base} {...next} /></QueryClientProvider>) };
}
const choose = (name: string) => fireEvent.click(screen.getByRole('option', { name: new RegExp(name) }));
beforeEach(() => { vi.clearAllMocks(); mocks.readChoice.mockReturnValue(null); mocks.models.mockResolvedValue({ providers: [], currentModel: null }); });
afterEach(() => { cleanup(); clients.splice(0).forEach(client => client.clear()); vi.useRealTimers(); });

describe('AgentSetupCard choices', () => {
  it('shows all statuses, names, subtitles and linked credit', () => {
    const agents = ready();
    agents[0] = { ...agents[0], state: 'sign-in', signIn: 'signed-out', creditLine: 'Built on oh-my-pi', creditUrl: 'https://example.test/omp' };
    agents[1].signIn = 'unknown'; agents[2].signIn = 'signed-out'; agents[3].state = 'not-installed';
    const view = mount({ agents });
    expect(within(screen.getByRole('option', { name: /Astrid's agent/ })).getByText('Set up')).toBeInTheDocument();
    expect(screen.getByText('Check sign-in')).toBeInTheDocument();
    expect(screen.getByText('Sign in', { exact: true })).toBeInTheDocument();
    expect(screen.getByText('Not installed')).toBeInTheDocument();
    expect(screen.getByText('Use your OpenRouter, ChatGPT or Claude account')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Built on oh-my-pi' })).toHaveAttribute('href', 'https://example.test/omp');
    view.rerenderCard({ agents: ready() });
    expect(screen.getAllByText('Ready')).toHaveLength(4);
  });
  it.each(['last', 'external', 'astrid'])('highlights and focuses the %s choice', kind => {
    const agents = ready();
    if (kind === 'last') mocks.readChoice.mockReturnValue({ agent: 'codex' });
    else agents[0].signIn = 'signed-out';
    if (kind === 'astrid') agents.slice(1).forEach(row => { row.signIn = 'signed-out'; });
    mount({ agents });
    const selected = screen.getByRole('option', { name: kind === 'last' ? /Use Codex/ : kind === 'external' ? /Use Claude Code/ : /Astrid's agent/ });
    expect(selected).toHaveAttribute('aria-selected', 'true');
    expect(selected).toHaveFocus();
  });
  it('supports arrows, Home, End and Enter', async () => {
    mount();
    fireEvent.keyDown(screen.getByRole('option', { selected: true }), { key: 'End' });
    expect(screen.getByRole('option', { name: /Hermes/ })).toHaveFocus();
    fireEvent.keyDown(document.activeElement!, { key: 'ArrowUp' });
    expect(screen.getByRole('option', { name: /Use Codex/ })).toHaveFocus();
    fireEvent.keyDown(document.activeElement!, { key: 'Home' });
    expect(screen.getByRole('option', { name: /Astrid's agent/ })).toHaveFocus();
    fireEvent.keyDown(document.activeElement!, { key: 'ArrowDown' });
    fireEvent.keyDown(document.activeElement!, { key: 'Enter' });
    await screen.findByText('Getting Claude Code ready…');
  });
});

describe('external setup and recovery', () => {
  it('renders install steps, polls every 3 seconds and on focus, then advances when ready', async () => {
    vi.useFakeTimers();
    const agents = ready();
    agents[2] = { ...agents[2], state: 'not-installed', steps: [{ kind: 'install', command: 'install-codex', label: 'Copy install' }, { kind: 'sign-in', command: 'codex login', label: 'Copy sign-in' }] };
    const view = mount({ agents }); choose('Use Codex');
    expect(screen.getByText('install-codex')).toBeInTheDocument();
    expect(screen.getByText('codex login')).toBeInTheDocument();
    expect(screen.getByText('Waiting for Codex…')).toHaveAttribute('aria-live', 'polite');
    await act(async () => { await vi.advanceTimersByTimeAsync(3000); });
    expect(view.refetchAgents).toHaveBeenCalledTimes(1);
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    expect(view.refetchAgents).toHaveBeenCalledTimes(2);
    await act(async () => { view.rerenderCard({ agents: ready() }); });
    expect(view.startChatWith).toHaveBeenCalledExactlyOnceWith('codex', undefined);
    expect(view.onComplete).toHaveBeenCalledWith('codex', undefined);
    await act(async () => { await vi.advanceTimersByTimeAsync(6000); });
    expect(view.refetchAgents).toHaveBeenCalledTimes(3);
  });
  it('uses only sign-in steps for signed-out agents', () => {
    const agents = ready(); agents[1] = { ...agents[1], signIn: 'signed-out', steps: [{ kind: 'install', command: 'install-claude', label: 'Install' }, { kind: 'sign-in', command: 'claude login', label: 'Login' }] };
    const view = mount({ agents }); choose('Use Claude Code');
    expect(screen.queryByText('install-claude')).toBeNull();
    expect(screen.getByText('claude login')).toBeInTheDocument();
    expect(screen.getByText('Waiting for you to sign in…')).toBeInTheDocument();
    expect(view.startChatWith).not.toHaveBeenCalled();
  });
  it('falls back to line for old services and treats ready without signIn as usable', async () => {
    const agents = ready().map(({ signIn: _, ...row }) => row);
    agents[3] = { ...agents[3], state: 'not-installed', line: 'Run `install-hermes`.' };
    const view = mount({ agents }); choose('Use Hermes');
    expect(screen.getByText('install-hermes')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Copy command' })).toBeInTheDocument();
    view.rerenderCard({ agents: ready().map(({ signIn: _, ...row }) => row) });
    await waitFor(() => expect(view.onComplete).toHaveBeenCalledWith('hermes', undefined));
  });
  it('returns setup errors to step 2 with nextAction when there are no steps', async () => {
    const error = new BridgeRouteError('Start', 502, { error: 'agent_sign_in_required', detail: 'Sign-in expired', next_action: 'codex login' });
    const view = mount({ startChatWith: vi.fn().mockResolvedValue({ error }) }); choose('Use Codex');
    expect(await screen.findByText('codex login')).toBeInTheDocument();
    expect(screen.getByText('Sign-in expired')).toBeInTheDocument();
    expect(screen.getByText('Waiting for you to sign in…')).toBeInTheDocument();
    expect(view.startChatWith).toHaveBeenCalledOnce();
    expect(view.onComplete).not.toHaveBeenCalled();
  });
  it('opens a new setup error on its agent even when the chooser is already mounted', async () => {
    const view = mount();
    view.rerenderCard({ initialAgent: 'hermes', initialError: new BridgeRouteError('Start', 502, { error: 'agent_not_installed', detail: 'Hermes is missing', next_action: 'install-hermes' }) });
    expect(await screen.findByText('install-hermes')).toBeVisible();
    expect(screen.queryByRole('listbox')).toBeNull();
    expect(view.startChatWith).not.toHaveBeenCalled();
  });
  it('shows the runtime fix over agent sign-in steps and retries immediately', async () => {
    const error = new BridgeRouteError('Start', 502, { error: 'agent_runtime_missing', detail: 'Bun is missing', next_action: 'install-bun' });
    const startChatWith = vi.fn().mockResolvedValueOnce({ error }).mockResolvedValue(undefined);
    const agents = ready();
    agents[2].steps = [{ kind: 'sign-in', command: 'codex login', label: 'Sign in' }];
    const view = mount({ agents, startChatWith }); choose('Use Codex');
    expect(await screen.findByText('install-bun')).toBeVisible();
    expect(screen.queryByText('codex login')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    await waitFor(() => expect(view.onComplete).toHaveBeenCalledOnce());
    expect(startChatWith).toHaveBeenCalledTimes(2);
  });
  it('offers retry for a runtime error supplied by the parent', async () => {
    const error = new BridgeRouteError('Start', 502, { error: 'agent_runtime_missing', detail: 'Bun is missing', next_action: 'install-bun' });
    const view = mount({ initialAgent: 'codex', initialError: error });
    expect(await screen.findByText('install-bun')).toBeVisible();
    expect(view.startChatWith).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    await waitFor(() => expect(view.onComplete).toHaveBeenCalledOnce());
  });
  it('shows generic failures and retries the same start callback', async () => {
    const startChatWith = vi.fn().mockResolvedValueOnce({ error: new Error('Warm-up failed') }).mockResolvedValue(undefined);
    const view = mount({ startChatWith }); choose('Use Codex');
    expect(await screen.findByRole('alert')).toHaveTextContent('Warm-up failed');
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    await waitFor(() => expect(view.onComplete).toHaveBeenCalledOnce());
    expect(startChatWith.mock.calls).toEqual([['codex', undefined], ['codex', undefined]]);
  });
});

describe("Astrid's setup", () => {
  it('keeps the linked credit on the OpenRouter key step', async () => {
    const agents = ready();
    agents[0] = { ...agents[0], state: 'sign-in', signIn: 'signed-out', creditLine: 'Built on oh-my-pi', creditUrl: 'https://github.com/can1357/oh-my-pi' };
    mount({ agents }); choose("Astrid's agent");
    expect(await screen.findByLabelText('OpenRouter key')).toBeVisible();
    expect(screen.getByRole('link', { name: 'Built on oh-my-pi' })).toHaveAttribute('href', 'https://github.com/can1357/oh-my-pi');
  });
  it('groups and searches the full catalog, selects currentModel and starts with the selected model', async () => {
    const data = catalog();
    data.providers[1].models.push(...Array.from({ length: 60 }, (_, i) => ({ id: `model-${i}`, name: `Model ${i}` })));
    mocks.models.mockResolvedValue(data);
    const view = mount(); choose("Astrid's agent");
    expect(await screen.findByRole('radio', { name: 'Default model' })).toBeChecked();
    expect(screen.getByRole('radio', { name: 'Model 59' })).toBeInTheDocument();
    expect(screen.getAllByRole('group').map(group => group.querySelector('legend')?.textContent)).toEqual(['OpenRouter', 'Claude', 'Other account']);
    expect(screen.getByRole('radio', { name: 'Unavailable model' })).toBeDisabled();
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'sonnet' } });
    expect(screen.queryByRole('radio', { name: 'Default model' })).toBeNull();
    fireEvent.click(screen.getByRole('radio', { name: 'Sonnet' }));
    fireEvent.click(screen.getByRole('button', { name: 'Use Sonnet' }));
    await waitFor(() => expect(view.startChatWith).toHaveBeenCalledExactlyOnceWith('astrid', 'claude/sonnet'));
    expect(mocks.remember).toHaveBeenCalledWith({ agent: 'astrid', model: 'claude/sonnet' });
  });
  it('polls the session-free model query every 3 seconds and on window focus', async () => {
    vi.useFakeTimers();
    const view = mount({ initialAgent: 'astrid' });
    await act(async () => { await vi.advanceTimersByTimeAsync(0); });
    expect(mocks.models).toHaveBeenCalledTimes(1);
    await act(async () => { await vi.advanceTimersByTimeAsync(3000); });
    expect(mocks.models).toHaveBeenCalledTimes(2);
    expect(view.refetchAgents).toHaveBeenCalledTimes(1);
    mocks.models.mockResolvedValue(catalog());
    await act(async () => { window.dispatchEvent(new Event('focus')); await vi.advanceTimersByTimeAsync(0); });
    expect(mocks.models).toHaveBeenCalledTimes(3);
    expect(screen.getByRole('radio', { name: 'Default model' })).toBeChecked();
  });
  it('uses an older provider catalog and agent row without optional fields', async () => {
    mocks.models.mockResolvedValue(catalog());
    mount({ agents: ready().map(({ signIn: _, ...row }) => row) });
    choose("Astrid's agent");
    expect(await screen.findByRole('radio', { name: 'Default model' })).toBeChecked();
    expect(screen.queryByLabelText('OpenRouter key')).toBeNull();
  });
  it('clears the key immediately, checks it locally, then selects the catalog default', async () => {
    let resolve!: (value: unknown) => void;
    mocks.saveKey.mockImplementation(() => new Promise(done => { resolve = done; }));
    const view = mount(); choose("Astrid's agent");
    const input = await screen.findByLabelText('OpenRouter key');
    expect(input).toHaveAttribute('type', 'password');
    expect(input).toHaveAttribute('autocomplete', 'off');
    fireEvent.change(input, { target: { value: 'test-key-value' } });
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }));
    expect(mocks.saveKey).toHaveBeenCalledWith('openrouter', 'test-key-value');
    expect(input).toHaveValue('');
    expect(document.body.innerHTML).not.toContain('test-key-value');
    expect(screen.getByText('Checking your key…')).toBeInTheDocument();
    mocks.models.mockResolvedValue(catalog());
    await act(async () => { resolve({ signedIn: true }); });
    expect(await screen.findByRole('radio', { name: 'Default model' })).toBeChecked();
    expect(view.refetchAgents).toHaveBeenCalled();
    expect(screen.queryByLabelText('OpenRouter key')).toBeNull();
  });
  it.each([
    ['invalid_key', "OpenRouter didn't accept that key."],
    ['provider_unreachable', "Couldn't reach OpenRouter. Check your connection and try again."],
    ['other_error', 'Service detail'],
  ])('shows the %s message without retaining the key', async (code, message) => {
    mocks.saveKey.mockRejectedValue({ code, detail: 'Service detail' });
    mount(); choose("Astrid's agent");
    fireEvent.change(await screen.findByLabelText('OpenRouter key'), { target: { value: 'test-rejected-value' } });
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }));
    expect(await screen.findByRole('alert')).toHaveTextContent(message);
    expect(screen.getByLabelText('OpenRouter key')).toHaveValue('');
    expect(document.body.innerHTML).not.toContain('test-rejected-value');
  });
  it('reveals terminal sign-in steps and switches to models after polling', async () => {
    const agents = ready(); agents[0].steps = [{ kind: 'sign-in', command: 'run-astrid', label: 'Start Astrid' }, { kind: 'sign-in', command: '/login', label: 'Sign in' }];
    const view = mount({ agents }); choose("Astrid's agent");
    const disclosure = await screen.findByText('Already have ChatGPT, Claude or Copilot? Use that instead');
    fireEvent.click(disclosure);
    expect(disclosure.closest('details')).toHaveAttribute('open');
    expect(screen.getByText('run-astrid')).toBeVisible();
    expect(screen.getByText('/login')).toBeVisible();
    mocks.models.mockResolvedValue(catalog());
    await act(async () => { await view.refetchAgents(); clients.at(-1)!.invalidateQueries({ queryKey: ['agent-setup-models'] }); });
    expect(await screen.findByRole('radio', { name: 'Default model' })).toBeChecked();
  });
});
