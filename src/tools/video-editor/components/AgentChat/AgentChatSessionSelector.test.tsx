// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { toast } from '@/shared/components/ui/toast.tsx';
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

  it('uses titles in the trigger and rows, while retaining creation-order fallback names and searching both', async () => {
    render(<AgentChatSessionSelector sessions={[{ id: 'one', title: 'Planning' }, { id: 'two' }]} activeSessionId="one" onSelectSession={vi.fn()} onRenameSession={vi.fn()} />);
    expect(screen.getByRole('combobox', { name: 'Project chat session' })).toHaveTextContent('Planning');
    fireEvent.click(screen.getByRole('combobox', { name: 'Project chat session' }));
    const activeOption = await screen.findByRole('option', { name: /^Planning/ });
    expect(activeOption).toHaveAttribute('data-selected', 'true');
    expect(screen.getByRole('option', { name: /^Chat 2/ })).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Rename Planning' })).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Rename Chat 2' })).toBeNull();
    fireEvent.change(screen.getByPlaceholderText('Search chats...'), { target: { value: 'Chat 1' } });
    expect(screen.getByRole('option', { name: /^Planning/ })).toBeTruthy();
    fireEvent.change(screen.getByPlaceholderText('Search chats...'), { target: { value: 'Planning' } });
    expect(screen.getByRole('option', { name: /^Planning/ })).toBeTruthy();
    expect(screen.queryByRole('option', { name: /^Chat 2/ })).toBeNull();
  });

  it('keeps fallback chat numbers stable when missing sessions are omitted or new chats are appended', async () => {
    const { rerender } = render(<AgentChatSessionSelector sessions={[{ id: 'one', title: 'Planning', chatNumber: 1 }, { id: 'three', chatNumber: 3 }]} activeSessionId="three" onSelectSession={vi.fn()} />);
    expect(screen.getByRole('combobox', { name: 'Project chat session' })).toHaveTextContent('Chat 3');
    fireEvent.click(screen.getByRole('combobox', { name: 'Project chat session' }));
    const firstOption = await screen.findByRole('option', { name: /^Planning/ });
    const activeOption = screen.getByRole('option', { name: /^Chat 3/ });
    expect(firstOption).toHaveAttribute('data-selected', 'false');
    expect(activeOption).toHaveAttribute('data-selected', 'true');
    rerender(<AgentChatSessionSelector sessions={[{ id: 'one', title: 'Planning', chatNumber: 1 }, { id: 'three', chatNumber: 3 }, { id: 'four', chatNumber: 4 }]} activeSessionId="three" onSelectSession={vi.fn()} />);
    expect(screen.getByRole('option', { name: /^Chat 3/ })).toBeTruthy();
    expect(screen.getByRole('option', { name: /^Chat 4/ })).toBeTruthy();
  });

  it('trims and saves a nonempty title', async () => {
    const onRenameSession = vi.fn().mockResolvedValue(undefined);
    const onOpenChange = vi.fn();
    render(<AgentChatSessionSelector sessions={[{ id: 'one' }]} activeSessionId="one" onOpenChange={onOpenChange} onSelectSession={vi.fn()} onRenameSession={onRenameSession} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Project chat session' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Rename Chat 1' }));
    expect(onOpenChange).toHaveBeenLastCalledWith(false);
    const nameInput = screen.getByRole('textbox', { name: 'Chat name' }) as HTMLInputElement;
    expect(nameInput.selectionStart).toBe(0);
    expect(nameInput.selectionEnd).toBe('Chat 1'.length);
    fireEvent.change(nameInput, { target: { value: '  Launch plan  ' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    await waitFor(() => expect(onRenameSession).toHaveBeenCalledWith('one', 'Launch plan'));
  });

  it('validates nonempty and 120 character titles', async () => {
    const onRenameSession = vi.fn().mockResolvedValue(undefined);
    render(<AgentChatSessionSelector sessions={[{ id: 'one' }]} activeSessionId="one" onSelectSession={vi.fn()} onRenameSession={onRenameSession} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Project chat session' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Rename Chat 1' }));
    const input = screen.getByRole('textbox', { name: 'Chat name' });
    fireEvent.change(input, { target: { value: '   ' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(await screen.findByText('Enter a chat name.')).toBeTruthy();
    fireEvent.change(input, { target: { value: 'x'.repeat(121) } });
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(await screen.findByText('Chat names must be 120 characters or fewer.')).toBeTruthy();
    expect(onRenameSession).not.toHaveBeenCalled();
  });

  it('shows a toast when renaming fails', async () => {
    const toastError = vi.spyOn(toast, 'error').mockImplementation(() => 'toast-id');
    const onRenameSession = vi.fn().mockRejectedValue(new Error('Rename failed'));
    render(<AgentChatSessionSelector sessions={[{ id: 'one' }]} activeSessionId="one" onSelectSession={vi.fn()} onRenameSession={onRenameSession} />);
    fireEvent.click(screen.getByRole('combobox', { name: 'Project chat session' }));
    fireEvent.click(await screen.findByRole('button', { name: 'Rename Chat 1' }));
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    await waitFor(() => expect(toastError).toHaveBeenCalledWith('Rename failed'));
    toastError.mockRestore();
  });
});
