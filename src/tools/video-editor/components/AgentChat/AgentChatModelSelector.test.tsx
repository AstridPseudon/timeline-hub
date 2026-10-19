// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AgentChatModelSelector } from './AgentChatModelSelector.tsx';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';

afterEach(cleanup);

const catalog: AcpModelCatalog = {
  currentModel: 'openai/gpt-5',
  providers: [
    { id: 'openai', name: 'OpenAI', signedIn: true, models: [{ id: 'gpt-5', name: 'GPT 5' }, { id: 'gpt-5-mini', name: 'GPT 5 Mini' }] },
    { id: 'anthropic', name: 'Anthropic', signedIn: false, models: [] },
  ],
};

describe('AgentChatModelSelector', () => {
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
});
