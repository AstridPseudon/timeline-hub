// @vitest-environment jsdom
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { TimelineCommandRecovery, type TimelineCommandRecoverySession } from './TimelineCommandRecovery.tsx';

function session(overrides: Partial<TimelineCommandRecoverySession['state']> = {}): TimelineCommandRecoverySession {
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

    expect(commandSession.recover).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Recover saved edits (session 1)' })).toHaveAttribute('data-owner-id', 'owner-a');
    expect(screen.getByRole('button', { name: 'Recover saved edits (session 2)' })).toHaveAttribute('data-owner-id', 'owner-b');

    fireEvent.click(screen.getByRole('button', { name: 'Recover saved edits (session 2)' }));
    await waitFor(() => expect(commandSession.recover).toHaveBeenCalledTimes(1));
    expect(commandSession.recover).toHaveBeenCalledWith('owner-b');
  });

  it('uses the singular human label while keeping the owner id only in the data attribute', () => {
    const commandSession = session({ recoverableOwners: ['owner-with-uuid-1234'] });
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    const button = screen.getByRole('button', { name: 'Recover saved edits' });
    expect(button).toHaveAttribute('data-owner-id', 'owner-with-uuid-1234');
    expect(screen.getByRole('alert')).not.toHaveTextContent('owner-with-uuid-1234');
  });

  it('shows busy state and a readable action error without hiding retained work', async () => {
    let finish!: () => void;
    const recover = vi.fn(() => new Promise<void>((resolve) => { finish = resolve; }));
    const commandSession = { ...session({ recoverableOwners: ['owner-a'] }), recover };
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    fireEvent.click(screen.getByRole('button', { name: 'Recover saved edits' }));
    expect(screen.getByRole('alert')).toHaveAttribute('aria-busy', 'true');
    expect(screen.getByRole('button', { name: 'Recovering saved edits…' })).toBeDisabled();

    await act(async () => { finish(); });
    expect(screen.getByText('Saved edits from another editor session are available. Choose which session to recover.')).toBeInTheDocument();
  });

  it('shows the exact retry action and reports callback failures while preserving the error', async () => {
    const retry = vi.fn(async () => { throw new Error('The save result could not be confirmed'); });
    const commandSession = { ...session({ status: 'retry', recoverableOwners: [], ownerId: 'owner-a' }), retry };
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(screen.getByRole('alert')).toHaveTextContent('without creating another edit');
    fireEvent.click(screen.getByRole('button', { name: 'Retry exact request' }));
    await waitFor(() => expect(screen.getByText('The save result could not be confirmed')).toBeInTheDocument());
    expect(retry).toHaveBeenCalledOnce();
  });

  it('keeps a native lock failure readable while retaining the unsaved-work warning', () => {
    render(<TimelineCommandRecovery commandSession={session({
      status: 'error', recoverableOwners: [], ownerId: null, error: 'Exclusive browser locks are unavailable',
    })} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Your unsaved changes are still here');
    expect(screen.getByRole('alert')).toHaveTextContent('could not safely hold the recovery session');
    expect(screen.getByRole('alert')).not.toHaveTextContent(/exclusive|browser locks|outbox/i);
  });

  it('distinguishes a retained conflict from an uncertain retry and avoids clash wording for retry errors', () => {
    const { rerender } = render(<TimelineCommandRecovery commandSession={session({
      status: 'conflict', recoverableOwners: [], ownerId: 'owner-a', error: 'Changes retained',
    })} />);
    expect(screen.getByRole('alert')).toHaveTextContent('need resolution before they can be saved');
    expect(screen.queryByRole('button', { name: 'Retry exact request' })).toBeNull();
    expect(screen.getByRole('alert')).not.toHaveTextContent(/clash|another change/i);

    rerender(<TimelineCommandRecovery commandSession={session({
      status: 'retry', recoverableOwners: [], ownerId: 'owner-a', error: 'head_busy',
    })} />);
    expect(screen.getByRole('button', { name: 'Retry exact request' })).toBeInTheDocument();
    expect(screen.getByRole('alert')).toHaveTextContent('save result is uncertain');
    expect(screen.getByRole('alert')).not.toHaveTextContent(/clash|conflict/i);
  });

  it('stays hidden without the command surface or after the session is saved', () => {
    const { rerender } = render(<TimelineCommandRecovery />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();

    rerender(<TimelineCommandRecovery commandSession={session({ status: 'saved', recoverableOwners: [], ownerId: 'owner-a' })} />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();
  });
});
