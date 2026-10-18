// @vitest-environment jsdom

import { fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ClipPanelBody, type ClipPanelBodyProps } from './ClipPanelBody.tsx';

const durationPort = vi.hoisted(() => ({ enabled: false, updateClip: vi.fn() }));
vi.mock('@/tools/video-editor/hooks/useTimelineCommandsService.ts', () => ({
  useTimelineCommandsServiceSafe: () => ({ updateClip: durationPort.updateClip }),
}));
vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useOptionalVideoEditorRuntime: () => ({ provider: { semanticCommandSaving: durationPort.enabled } }),
}));
afterEach(() => { durationPort.enabled = false; durationPort.updateClip.mockReset(); });

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


describe('visible HOLD duration callback', () => {
  const durationProps = () => ({ ...bodyProps(), activeTab: 'timing' as const,
    clip: { id: 'clip-0', clipType: 'hold', track: 'V1', at: 0, hold: 5 }, onChange: vi.fn() } as ClipPanelBodyProps);
  it('keeps the flag-off callback compatible', () => {
    const props = durationProps(); render(<ClipPanelBody {...props} />);
    fireEvent.change(screen.getAllByRole('textbox')[1], { target: { value: '6' } });
    expect(props.onChange).toHaveBeenCalledWith({ hold: 6 }); expect(durationPort.updateClip).not.toHaveBeenCalled();
  });
  it('captures the displayed HOLD expectation for the mounted semantic facade', () => {
    durationPort.enabled = true; durationPort.updateClip.mockReturnValue({ ok: true });
    const props = durationProps(); render(<ClipPanelBody {...props} />);
    fireEvent.change(screen.getAllByRole('textbox')[1], { target: { value: '6' } });
    expect(durationPort.updateClip).toHaveBeenCalledWith({ clipId: 'clip-0', patch: { hold: 6 }, expectedHold: 5 });
    expect(props.onChange).not.toHaveBeenCalled();
  });
  it('surfaces the real refusal without calling the legacy callback', () => {
    durationPort.enabled = true; durationPort.updateClip.mockReturnValue({ ok: false, error: { message: 'Captured base changed' } });
    const props = durationProps(); render(<ClipPanelBody {...props} />);
    fireEvent.change(screen.getAllByRole('textbox')[1], { target: { value: '6' } });
    expect(screen.getByRole('alert').textContent).toBe('Captured base changed'); expect(props.onChange).not.toHaveBeenCalled();
  });
});
