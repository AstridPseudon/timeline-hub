// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { AgentChatModelSelector, summarizeUsage } from './AgentChatModelSelector.tsx';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';

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

function openList(onSelectModel = vi.fn(), onOpenChange = vi.fn()) {
  render(<AgentChatModelSelector catalog={catalog} onSelectModel={onSelectModel} onOpenChange={onOpenChange} />);
  fireEvent.click(screen.getByRole('combobox', { name: 'Agent model' }));
  return { onSelectModel, onOpenChange };
}

describe('AgentChatModelSelector', () => {
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

  it('shows a selection failure inline with a Switch model action that opens the list', async () => {
    render(<AgentChatModelSelector catalog={catalog} onSelectModel={vi.fn()} selectionError="Provider quota exceeded" />);
    expect(screen.getByRole('alert').textContent).toContain('Provider quota exceeded');
    fireEvent.click(screen.getByRole('button', { name: 'Switch model' }));
    expect(await screen.findByText('OpenAI')).toBeTruthy();
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
