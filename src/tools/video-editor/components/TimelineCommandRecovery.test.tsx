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

  it('shows the retry action and reports callback failures while preserving the error', async () => {
    const retry = vi.fn(async () => { throw new Error('The save result could not be confirmed'); });
    const commandSession = { ...session({ status: 'retry', recoverableOwners: [], ownerId: 'owner-a' }), retry };
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Retry save to check it');
    const retryButton = screen.getByRole('button', { name: 'Retry save' });
    expect(retryButton).toHaveAttribute('data-testid', 'timeline-command-retry');
    fireEvent.click(retryButton);
    await waitFor(() => expect(screen.getByText('The recovery action could not finish. Your unsaved changes are still here.')).toBeInTheDocument());
    expect(retry).toHaveBeenCalledOnce();
  });

  it('keeps a native lock failure readable while retaining the unsaved-work warning', () => {
    render(<TimelineCommandRecovery commandSession={session({
      status: 'error', recoverableOwners: [], ownerId: 'owner-a', error: 'Exclusive browser locks are unavailable',
    })} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Your unsaved changes are still here');
    expect(screen.getByRole('alert')).toHaveTextContent('could not safely hold the recovery session');
    expect(screen.getByRole('alert')).not.toHaveTextContent(/exclusive|browser locks|outbox/i);
  });

  it('offers retry for an initialization error without claiming work was retained', async () => {
    const retry = vi.fn(async () => {});
    const commandSession = session({
      status: 'error', recoverableOwners: [], ownerId: null, canUndo: false, error: 'IndexedDB is unavailable',
    });
    commandSession.retry = retry;
    render(<TimelineCommandRecovery commandSession={commandSession} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Saving is unavailable. Retry to try again.');
    expect(screen.getByRole('alert')).not.toHaveTextContent('unsaved changes are still here');
    fireEvent.click(screen.getByRole('button', { name: 'Retry save' }));
    await waitFor(() => expect(retry).toHaveBeenCalledOnce());
  });

  it('distinguishes a retained conflict from an uncertain retry and avoids clash wording for retry errors', () => {
    const { rerender } = render(<TimelineCommandRecovery commandSession={session({
      status: 'conflict', recoverableOwners: [], ownerId: 'owner-a', error: 'Changes retained',
    })} />);
    expect(screen.getByRole('alert')).toHaveTextContent('need resolution before they can be saved');
    expect(screen.queryByRole('button', { name: 'Retry save' })).toBeNull();
    expect(screen.getByRole('alert')).not.toHaveTextContent(/clash|another change/i);

    rerender(<TimelineCommandRecovery commandSession={session({
      status: 'retry', recoverableOwners: [], ownerId: 'owner-a', error: 'head_busy',
    })} />);
    expect(screen.getByRole('button', { name: 'Retry save' })).toBeInTheDocument();
    expect(screen.getByRole('alert')).toHaveTextContent('save result is uncertain');
    expect(screen.getByRole('alert')).not.toHaveTextContent(/clash|conflict/i);
  });

  it('stays hidden without the command surface or after the session is saved', () => {
    const { rerender } = render(<TimelineCommandRecovery />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();

    rerender(<TimelineCommandRecovery commandSession={session({ status: 'saved', recoverableOwners: [], ownerId: 'owner-a' })} />);
    expect(screen.queryByTestId('timeline-command-recovery')).toBeNull();
  });

  it('names the supplied scoped targets and property paths without hiding retained work', () => {
    render(<TimelineCommandRecovery commandSession={session({
      status: 'conflict', recoverableOwners: [], ownerId: 'owner-a',
      error: 'internal protocol message and private document',
      conflicts: [
        { kind: 'dependency_changed', ref: 'parent/clip:x', path: ['at'] },
        { kind: 'dependency_changed', ref: 'occurrence:opening/clip:y', path: ['text', 'content'] },
        { kind: 'identity_changed', ref: 'parent/track:V1', path: [] },
      ],
    })} />);

    expect(screen.getByRole('alert')).toHaveTextContent('Your changes are retained and need resolution before they can be saved.');
    const locations = screen.getByRole('list', { name: 'Changed timeline properties' });
    expect(locations).toHaveTextContent('Changed target: parent/clip:x · Property: at');
    expect(locations).toHaveTextContent('Changed target: occurrence:opening/clip:y · Property: text.content');
    expect(locations).toHaveTextContent('Changed target: parent/track:V1 · Target itself changed');
    expect(screen.getAllByRole('listitem')).toHaveLength(3);
    expect(screen.getByRole('alert')).not.toHaveTextContent(/internal protocol|private document|dependency_changed|identity_changed/);
    expect(screen.queryByRole('button', { name: 'Retry save' })).toBeNull();
  });

  it.each([undefined, []])('keeps the generic retained-work message without conflict locations: %j', (conflicts) => {
    render(<TimelineCommandRecovery commandSession={session({
      status: 'conflict', recoverableOwners: [], ownerId: 'owner-a', conflicts,
    })} />);
    expect(screen.getByRole('alert')).toHaveTextContent('Your changes are retained and need resolution before they can be saved.');
    expect(screen.queryByRole('list', { name: 'Changed timeline properties' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Retry save' })).toBeNull();
  });

  it.each(['retry', 'error', 'recovery'] as const)('hides conflict locations in %s state', (status) => {
    render(<TimelineCommandRecovery commandSession={session({
      status, ownerId: 'owner-a', recoverableOwners: status === 'recovery' ? ['owner-b'] : [],
      conflicts: [{ kind: 'dependency_changed', ref: 'parent/clip:x', path: ['at'] }],
    })} />);
    expect(screen.queryByRole('list', { name: 'Changed timeline properties' })).toBeNull();
    expect(screen.getByRole('alert')).not.toHaveTextContent(/parent\/clip:x|property|clash|conflict/i);
    expect(screen.getByRole('button', { name: status === 'recovery' ? 'Recover saved edits' : 'Retry save' })).toBeInTheDocument();
  });
});
