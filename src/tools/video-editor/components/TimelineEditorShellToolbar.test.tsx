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

  it('stacks the mode switcher above the centred resize divider so taps on its buttons are not swallowed', () => {
    render(
      <TimelineStoreProvider store={createTimelineStore()}>
        <TimelineEditorShellToolbar
          touchChrome
          condensed={false}
          toolbarModeSwitcher={<button type="button">Move</button>}
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

    const slot = screen.getByRole('button', { name: 'Move' }).closest('[data-toolbar-mode-switcher-slot]') as HTMLElement;
    expect(slot.className).toContain('relative');
    expect(slot.className).toContain('z-10');
    // The divider overlay is a later sibling of the slot with no z-index of its own, so the slot's
    // z-10 is what puts the switcher ahead of it.
    const overlay = slot.parentElement!.querySelector('.cursor-row-resize')!.parentElement as HTMLElement;
    expect(overlay.compareDocumentPosition(slot) & Node.DOCUMENT_POSITION_PRECEDING).toBeTruthy();
    expect(overlay.className).not.toMatch(/\bz-\d+/);
  });

  it('centres the resize grip on the first line of the toolbar, not on the whole wrapped row', () => {
    render(
      <TimelineStoreProvider store={createTimelineStore()}>
        <TimelineEditorShellToolbar
          touchChrome
          condensed={false}
          toolbarModeSwitcher={<button type="button">Move</button>}
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

    const overlay = document.querySelector('.cursor-row-resize')!.parentElement as HTMLElement;
    // Pinned to the top at one touch line's height (h-11, the row's min-h-11): inset-0 would follow the
    // wrapped row's full height and put the grip on the switcher pill's top border.
    expect(overlay.className).toContain('top-0');
    expect(overlay.className).toContain('h-11');
    expect(overlay.className).not.toContain('inset-0');
    expect(overlay.className).not.toContain('bottom-0');
  });

  it('holds the switcher and the touch create tools together in one slot, tools after the switcher, and wraps that slot at the widened threshold', () => {
    render(
      <TimelineStoreProvider store={createTimelineStore()}>
        <TimelineEditorShellToolbar
          touchChrome
          condensed={false}
          toolbarModeSwitcher={<button type="button">Move</button>}
          toolbarCreateTools={<button type="button">New text at playhead</button>}
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

    const move = screen.getByRole('button', { name: 'Move' });
    const tools = screen.getByRole('button', { name: 'New text at playhead' });
    const slot = move.closest('[data-toolbar-mode-switcher-slot]') as HTMLElement;
    expect(tools.closest('[data-toolbar-mode-switcher-slot]')).toBe(slot);
    expect(move.compareDocumentPosition(tools) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    // Same z-10 slot, so the tools are ahead of the divider overlay too.
    expect(slot.className).toContain('z-10');
    const overlay = slot.parentElement!.querySelector('.cursor-row-resize')!.parentElement as HTMLElement;
    expect(overlay.compareDocumentPosition(slot) & Node.DOCUMENT_POSITION_PRECEDING).toBeTruthy();
    // Switcher (368) + gap + tools (132) is wider than the old slot: the one-line threshold rose from 800px.
    expect(slot.className).toContain('flex-wrap');
    expect(slot.className).toContain('@[920px]:w-auto');
    expect(slot.className).not.toContain('@[800px]');
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
