// @vitest-environment jsdom
import React from 'react';
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { setRecoveryCardShowing } from '@/integrations/runtime/recoveryCard.ts';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { TimelineEditorShellToolbar } from './TimelineEditorShellToolbar.tsx';
import { createTimelineStore, TimelineStoreProvider } from '@/tools/video-editor/hooks/timelineStore.ts';

// '' is same-origin; a gateway origin is the hosted build.
let hostedOrigin = '';
vi.mock('@/integrations/runtime/connection.ts', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/integrations/runtime/connection.ts')>()),
  runtimeOrigin: () => hostedOrigin,
}));

describe('TimelineEditorShellToolbar', () => {
  it('refreshes canonical history whenever its dropdown opens', async () => {
    const refreshCanonicalHistory = vi.fn(async () => {});
    const store = createTimelineStore();
    store.setState((state) => ({
      chrome: {
        ...state.chrome,
        canonicalHistorySupported: true,
        refreshCanonicalHistory,
      },
    }));

    render(
      <TimelineStoreProvider store={store}>
        <TimelineEditorShellToolbar
          touchChrome={false}
          condensed={false}
          toolbarModeSwitcher={null}
          onDividerPointerDown={() => {}}
          onDividerPointerMove={() => {}}
          onDividerPointerUp={() => {}}
          onDividerPointerCancel={() => {}}
          onDividerLostPointerCapture={() => {}}
          isTimelineMaximized={false}
          setIsTimelineMaximized={() => {}}
          onOpenElements={() => {}}
        />
      </TimelineStoreProvider>,
    );

    fireEvent.click(screen.getByTitle('History'));
    await waitFor(() => expect(refreshCanonicalHistory).toHaveBeenCalledTimes(1));
  });

  const renderHistory = () => {
    const restoreCanonicalRevision = vi.fn(async () => {});
    const current = {
      revisionId: 'parent-repeated', publicationId: 'publication-restored',
      projectId: 'project-1', parentDocumentId: 'timeline-1',
      createdAt: '2026-10-19T12:00:00Z', isCurrentHead: true,
    };
    const older = { ...current, publicationId: 'publication-original', createdAt: '2026-10-18T12:00:00Z', isCurrentHead: false };
    const store = createTimelineStore();
    store.setState((state) => ({ chrome: {
      ...state.chrome,
      canonicalHistorySupported: true,
      canonicalHistory: [current, older],
      refreshCanonicalHistory: vi.fn(async () => {}),
      restoreCanonicalRevision,
    } }));
    render(
      <TimelineStoreProvider store={store}>
        <TimelineEditorShellToolbar
          touchChrome={false}
          condensed={false}
          toolbarModeSwitcher={null}
          onDividerPointerDown={() => {}}
          onDividerPointerMove={() => {}}
          onDividerPointerUp={() => {}}
          onDividerPointerCancel={() => {}}
          onDividerLostPointerCapture={() => {}}
          isTimelineMaximized={false}
          setIsTimelineMaximized={() => {}}
          onOpenElements={() => {}}
        />
      </TimelineStoreProvider>,
    );
    fireEvent.click(screen.getByTitle('History'));
    return { store, current, older, restoreCanonicalRevision };
  };

  it('keeps repeated-revision publications visible with distinct keys and one current entry', async () => {
    const { store, current, older, restoreCanonicalRevision } = renderHistory();
    const entries = await screen.findAllByRole('menuitem');
    expect(entries).toHaveLength(2);
    expect(within(entries[0]).getByText('Current')).toBeTruthy();
    expect(entries[0]).toHaveAttribute('aria-disabled', 'true');
    expect(entries[1]).not.toHaveAttribute('aria-disabled', 'true');
    expect(within(entries[0]).getByText('parent-repeated')).toBeTruthy();
    expect(within(entries[1]).getByText('parent-repeated')).toBeTruthy();
    expect(screen.getAllByText('Current')).toHaveLength(1);

    act(() => store.setState((state) => ({ chrome: { ...state.chrome, canonicalHistory: [older, current] } })));
    const reordered = screen.getAllByRole('menuitem');
    expect(reordered[0]).toBe(entries[1]);
    expect(reordered[1]).toBe(entries[0]);
    fireEvent.click(reordered[0]);
    expect(restoreCanonicalRevision).toHaveBeenCalledWith('parent-repeated');
  });

  it('keeps the restore progress and disables history actions while restoring', async () => {
    const { store, older, restoreCanonicalRevision } = renderHistory();
    act(() => store.setState((state) => ({ chrome: {
      ...state.chrome, restoringCanonicalRevisionId: older.revisionId,
    } })));
    const entries = await screen.findAllByRole('menuitem');
    expect(screen.getByText('Restoring')).toBeTruthy();
    for (const entry of entries) {
      expect(entry).toHaveAttribute('aria-disabled', 'true');
      fireEvent.click(entry);
    }
    expect(restoreCanonicalRevision).not.toHaveBeenCalled();
  });

  it('shows unavailable history errors without presenting stale entries or checkpoints as accepted history', async () => {
    const { store } = renderHistory();
    act(() => store.setState((state) => ({ chrome: {
      ...state.chrome, canonicalHistoryError: 'Accepted history is unavailable',
    } })));
    expect(await screen.findByRole('alert')).toHaveTextContent('Accepted history is unavailable');
    expect(screen.queryAllByRole('menuitem')).toHaveLength(0);
    expect(screen.queryByText('No published revisions yet.')).toBeNull();
    expect(screen.queryByText('parent-repeated')).toBeNull();
  });

  describe('the save badge', () => {
    const renderToolbar = (saveStatus: 'saved' | 'saving' | 'dirty' | 'retrying' | 'error', isConflictExhausted = false) => {
      const store = createTimelineStore();
      store.setState((state) => ({ chrome: { ...state.chrome, saveStatus, isConflictExhausted } }));
      return render(
        <TimelineStoreProvider store={store}>
          <TimelineEditorShellToolbar
            touchChrome={false}
            condensed={false}
            toolbarModeSwitcher={null}
            onDividerPointerDown={() => {}}
            onDividerPointerMove={() => {}}
            onDividerPointerUp={() => {}}
            onDividerPointerCancel={() => {}}
            onDividerLostPointerCapture={() => {}}
            isTimelineMaximized={false}
            setIsTimelineMaximized={() => {}}
            onOpenElements={() => {}}
          />
        </TimelineStoreProvider>,
      );
    };

    it('reads Error in red when a save fails with no recovery card up', () => {
      renderToolbar('error');
      const badge = screen.getByText('error');
      expect(badge.className).toContain('bg-destructive');
    });

    it('reads Not saved, neutral and muted, while the Astrid stopped / restarted card is showing', () => {
      act(() => setRecoveryCardShowing(true));
      try {
        renderToolbar('error');
        expect(screen.queryByText('error')).toBeNull();
        const badge = screen.getByText('Not saved');
        expect(badge.className).not.toContain('bg-destructive');
        expect(badge.className).toContain('text-muted-foreground');
      } finally {
        act(() => setRecoveryCardShowing(false));
      }
    });

    it('reads Not saved, neutral and muted, while a save conflict is open: a choice, not an error', () => {
      renderToolbar('error', true);
      expect(screen.queryByText('error')).toBeNull();
      const badge = screen.getByText('Not saved');
      expect(badge.className).not.toContain('bg-destructive');
      expect(badge.className).toContain('text-muted-foreground');
    });

    describe('on the hosted build', () => {
      afterEach(() => { hostedOrigin = ''; });

      it('never reads a red Error for a save that failed during a stop, even once the card has cleared', () => {
        hostedOrigin = 'http://127.0.0.1:17340';
        renderToolbar('error');
        expect(screen.queryByText('error')).toBeNull();
        const badge = screen.getByText('Not saved');
        expect(badge.className).not.toContain('bg-destructive');
        expect(badge.className).toContain('text-muted-foreground');
      });

      it('keeps the other statuses as they are', () => {
        hostedOrigin = 'http://127.0.0.1:17340';
        for (const status of ['saving', 'dirty', 'retrying'] as const) {
          const view = renderToolbar(status);
          expect(screen.getByText(status)).toBeTruthy();
          expect(screen.queryByText('Not saved')).toBeNull();
          view.unmount();
        }
      });
    });

    it('still says saved when nothing is wrong, card or not', () => {
      act(() => setRecoveryCardShowing(true));
      try {
        renderToolbar('saved');
        expect(screen.getByText('saved')).toBeTruthy();
        expect(screen.queryByText('Not saved')).toBeNull();
      } finally {
        act(() => setRecoveryCardShowing(false));
      }
    });
  });
});
