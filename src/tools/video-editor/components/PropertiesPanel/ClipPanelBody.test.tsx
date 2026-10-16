// @vitest-environment jsdom

import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ClipPanelBody, type ClipPanelBodyProps } from './ClipPanelBody.tsx';

vi.mock('./ClipEffectsTab.tsx', () => ({
  ClipEffectsTab: ({ hasActiveAstridElementParams }: { hasActiveAstridElementParams?: boolean }) => (
    <div data-testid="effects-astrid-form-state">{String(Boolean(hasActiveAstridElementParams))}</div>
  ),
}));

function bodyProps(hasActiveAstridElementParams?: boolean): ClipPanelBodyProps {
  return {
    readOnly: false,
    clip: { id: 'clip-1', clipType: 'media', at: 0, track: 'V1' },
    track: { id: 'V1', kind: 'visual', label: 'Video 1' },
    deviceClass: 'desktop',
    interactionMode: 'move',
    precisionEnabled: false,
    hasPredecessor: false,
    onChange: () => undefined,
    onResetPosition: () => undefined,
    onClose: () => undefined,
    onToggleMute: () => undefined,
    onSplitAtPlayhead: () => undefined,
    onMoveTrackUp: () => undefined,
    onMoveTrackDown: () => undefined,
    onSetInteractionMode: () => undefined,
    onSetPrecisionEnabled: () => undefined,
    compositionWidth: 1920,
    compositionHeight: 1080,
    registry: {},
    activeTab: 'effects',
    setActiveTab: () => undefined,
    effectResources: { canCreateEffect: false, canUpdateEffect: false, effects: [] },
    hasActiveAstridElementParams,
  } as unknown as ClipPanelBodyProps;
}

describe('ClipPanelBody Astrid form ownership', () => {
  it('forwards active form ownership to the effects tab', () => {
    render(<ClipPanelBody {...bodyProps(true)} />);
    expect(screen.getByTestId('effects-astrid-form-state').textContent).toBe('true');
  });

  it('keeps the legacy effects state when no active form owns it', () => {
    render(<ClipPanelBody {...bodyProps()} />);
    expect(screen.getByTestId('effects-astrid-form-state').textContent).toBe('false');
  });
});

describe('ClipPanelBody timing value commits', () => {
  it.each([
    ['Speed', 2, { speed: 2 }],
    ['Source In', 1, { from: 1 }],
  ] as const)('reapplies %s if the controlled clip value resets before blur', (label, value, expectedPatch) => {
    const onChange = vi.fn();
    const initialClip = { id: 'clip-1', clipType: 'media', at: 0, track: 'V1', from: 0, to: 5, speed: 1 };
    const props = {
      ...bodyProps(),
      clip: initialClip,
      activeTab: 'timing' as const,
      onChange,
    };
    const { rerender } = render(<ClipPanelBody {...props} />);
    const input = screen.getByText(label).parentElement?.querySelector('input');
    expect(input).not.toBeNull();

    input!.focus();
    expect(document.activeElement).toBe(input);
    fireEvent.change(input!, { target: { value: String(value) } });
    expect(onChange).toHaveBeenLastCalledWith(expectedPatch);

    // The timeline first adopts the edit, then an external refresh restores the
    // old controlled clip while Base UI still preserves the typed text.
    rerender(<ClipPanelBody {...props} clip={{ ...initialClip, ...expectedPatch }} />);
    expect(document.activeElement).toBe(input);
    rerender(<ClipPanelBody {...props} />);
    expect(document.activeElement).toBe(input);
    fireEvent.blur(input!);

    expect(onChange).toHaveBeenLastCalledWith(expectedPatch);
    expect(onChange).toHaveBeenCalledTimes(2);
  });
});
