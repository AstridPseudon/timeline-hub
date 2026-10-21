// @vitest-environment jsdom

import { act, render } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { exitEditorTour, getEditorTourState, markEditorTourReady } from '@/shared/state/editorTourStore';
import { EditorTourSlot } from '../timeline/editorTourSlot';
import { useEditorTourHost } from './useEditorTourHost';

vi.mock('@/shared/hooks/mobile', () => ({
  useIsMobile: () => false,
  useIsTablet: () => false,
  useViewportWidth: () => 1440,
  isTabletHardware: () => false,
}));

function Page({ hasSelection }: { hasSelection: boolean }) {
  useEditorTourHost(hasSelection);
  return <EditorTourSlot />;
}

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
});

afterEach(() => {
  exitEditorTour();
  localStorage.clear();
});

describe('useEditorTourHost', () => {
  it('starts on the first mount with a selection and shows the runner only while the tour runs', () => {
    const { unmount } = render(<Page hasSelection />);

    expect(getEditorTourState().status).toBe('running');
    expect(document.querySelector('[data-editor-tour-shield]')).not.toBeNull();

    act(() => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    });
    expect(getEditorTourState().status).toBe('idle');
    expect(document.querySelector('[data-editor-tour-shield]')).toBeNull();
    unmount();
  });

  it('does not start without a selection, and Enter swallows the keystroke while running', () => {
    const idle = render(<Page hasSelection={false} />);
    expect(getEditorTourState().status).toBe('idle');
    idle.unmount();

    const { unmount } = render(<Page hasSelection />);
    // Replay path: the flag is set, so only an explicit start runs it again.
    // The welcome card has played its entrance, so Enter is its OK.
    act(() => markEditorTourReady('card'));
    const enter = new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true });
    act(() => {
      window.dispatchEvent(enter);
    });
    expect(enter.defaultPrevented).toBe(true);
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'compose' });
    unmount();
  });
});
