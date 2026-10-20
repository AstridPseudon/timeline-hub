// @vitest-environment jsdom
import React from 'react';
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
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

  it('shows publication metadata and restores a legacy revision even when another publication reuses it', async () => {
    const restoreCanonicalRevision = vi.fn(async () => {});
    const store = createTimelineStore();
    const legacy = {
      revisionId: 'shared-revision', publicationId: 'legacy-publication',
      projectId: 'project-1', parentDocumentId: 'timeline-1', contentDigest: `sha256:${'a'.repeat(64)}`,
      createdAt: '2026-10-19T00:00:00Z', isCurrentHead: false,
      intent: 'legacy_unknown' as const, publisher: null,
    };
    store.setState((state) => ({ chrome: {
      ...state.chrome,
      canonicalHistorySupported: true,
      canonicalHistory: [legacy, {
        ...legacy, publicationId: 'recorded-publication', intent: 'recorded', isCurrentHead: true,
        publisher: 'actor-1', label: 'Restore opening', rationale: 'Keep the original framing',
      }],
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
    const recorded = await screen.findByRole('menuitem', { name: /Restore opening/ });
    expect(recorded.getAttribute('aria-disabled')).toBe('true');
    expect(screen.getByText('actor-1')).toBeTruthy();
    expect(screen.getByText('Keep the original framing')).toBeTruthy();
    expect(screen.getAllByText('Current')).toHaveLength(1);
    const historical = screen.getByRole('menuitem', { name: /Legacy history · command intent unknown/ });
    expect(historical.getAttribute('aria-disabled')).not.toBe('true');
    fireEvent.click(historical);
    await waitFor(() => expect(restoreCanonicalRevision).toHaveBeenCalledWith('shared-revision'));
  });

  it('shows canonical history failures as an alert without offering stale entries', async () => {
    const store = createTimelineStore();
    store.setState((state) => ({ chrome: {
      ...state.chrome,
      canonicalHistorySupported: true,
      canonicalHistoryError: 'Workspace Runtime returned a repeated history cursor',
      canonicalHistory: [{
        revisionId: 'stale-revision', projectId: 'project-1', parentDocumentId: 'timeline-1',
        contentDigest: `sha256:${'a'.repeat(64)}`, createdAt: '2026-10-19T00:00:00Z', isCurrentHead: false,
      }],
      refreshCanonicalHistory: vi.fn(async () => {}),
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
    expect(await screen.findByRole('alert')).toHaveTextContent('repeated history cursor');
    expect(screen.queryByText('stale-revision')).toBeNull();
    expect(screen.queryByText('No published revisions yet.')).toBeNull();
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
