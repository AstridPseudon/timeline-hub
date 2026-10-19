// @vitest-environment jsdom
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { TimelineCommandRecovery, type TimelineCommandRecoveryProps } from './TimelineCommandRecovery.tsx';
import type { TimelineCommandSessionSurface } from '@/tools/video-editor/hooks/useTimelineCommandSession.ts';

function session(overrides: Partial<TimelineCommandSessionSurface['state']> = {}): TimelineCommandRecoveryProps['commandSession'] {
  return {
    state: {
      status: 'recovery',
      error: null,
      ownerId: null,
      recoverableOwners: ['owner-a', 'owner-b'],
      canUndo: false,
      ...overrides,
    },
    retry: vi.fn(async () => {}),
    recover: vi.fn(async () => {}),
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe('TimelineCommandRecovery', () => {
  it('requires an explicit owner choice and passes the exact selected owner once', async () => {
    const commandSession = session();
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(commandSession?.recover).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Recover saved edits (session 1)' })).toHaveAttribute('data-owner-id', 'owner-a');
    expect(screen.getByRole('button', { name: 'Recover saved edits (session 2)' })).toHaveAttribute('data-owner-id', 'owner-b');

    fireEvent.click(screen.getByRole('button', { name: 'Recover saved edits (session 2)' }));
    await waitFor(() => expect(commandSession?.recover).toHaveBeenCalledTimes(1));
    expect(commandSession?.recover).toHaveBeenCalledWith('owner-b');
  });

  it('uses the singular human label while keeping the owner id only in the data attribute', () => {
    const commandSession = session({ recoverableOwners: ['owner-with-uuid-1234'] });
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    const button = screen.getByRole('button', { name: 'Recover saved edits' });
    expect(button).toHaveAttribute('data-owner-id', 'owner-with-uuid-1234');
    expect(screen.getByRole('alert')).not.toHaveTextContent('owner-with-uuid-1234');
  });

  it('shows busy state and prevents duplicate recovery clicks', async () => {
    let finish!: () => void;
    const recover = vi.fn(() => new Promise<void>((resolve) => { finish = resolve; }));
    const commandSession = { ...session({ recoverableOwners: ['owner-a'] }), recover };
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    const button = screen.getByRole('button', { name: 'Recover saved edits' });
    fireEvent.click(button);
    fireEvent.click(button);
    expect(commandSession.recover).toHaveBeenCalledTimes(1);
    expect(screen.getByRole('alert')).toHaveAttribute('aria-busy', 'true');
    expect(screen.getByRole('button', { name: 'Recovering saved edits…' })).toBeDisabled();

    await act(async () => { finish(); });
  });

  it('offers exact retry for an uncertain save and explains that it does not apply edits again', async () => {
    const retry = vi.fn(async () => {});
    const commandSession = { ...session({ status: 'retry', recoverableOwners: [], ownerId: 'owner-a' }), retry };
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(screen.getByRole('alert')).toHaveTextContent('without applying edits again');
    fireEvent.click(screen.getByTestId('timeline-command-retry'));
    await waitFor(() => expect(retry).toHaveBeenCalledTimes(1));
  });

  it('offers retry for typed errors, keeps the original detail, and preserves action failures', async () => {
    const retry = vi.fn(async () => { throw new Error('The save result could not be confirmed'); });
    const commandSession = { ...session({ status: 'error', recoverableOwners: [], ownerId: 'owner-a', error: 'provider refused the durable append' }), retry };
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Your saved edits could not be completed.');
    expect(screen.getByRole('alert')).toHaveTextContent('provider refused the durable append');
    fireEvent.click(screen.getByTestId('timeline-command-retry'));
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('The save result could not be confirmed'));
    expect(retry).toHaveBeenCalledOnce();
  });

  it('does not claim unsaved changes for an initial error without an owner', () => {
    render(<TimelineCommandRecovery commandSession={session({
      status: 'error', recoverableOwners: [], ownerId: null, error: 'Timeline command session is unavailable',
    })} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Editing is unavailable right now.');
    expect(screen.getByRole('alert')).not.toHaveTextContent(/unsaved|retained/i);
    expect(screen.getByRole('alert')).toHaveTextContent('Timeline command session is unavailable');
  });

  it('distinguishes a retained conflict and does not offer retry for it', () => {
    const commandSession = session({ status: 'conflict', recoverableOwners: [], ownerId: 'owner-a', error: 'read changed' });
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(screen.getByRole('alert')).toHaveTextContent('conflict with another change');
    expect(screen.queryByTestId('timeline-command-retry')).toBeNull();
    expect(screen.getByRole('alert')).toHaveTextContent('read changed');
  });

  it('stays hidden without the command surface, after saving, and for no-work loading', () => {
    const { rerender } = render(<TimelineCommandRecovery />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();

    rerender(<TimelineCommandRecovery commandSession={session({ status: 'saved', recoverableOwners: [], ownerId: 'owner-a' })} />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();

    rerender(<TimelineCommandRecovery commandSession={session({ status: 'loading', recoverableOwners: [], ownerId: null })} />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();
  });
});
