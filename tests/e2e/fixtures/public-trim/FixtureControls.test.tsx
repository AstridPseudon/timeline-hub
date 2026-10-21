import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { FixtureControls } from './FixtureControls';

const useTimelineEditorData = vi.hoisted(() => vi.fn());
const useTimelineChromeContext = vi.hoisted(() => vi.fn());
const useTimelineCommandsService = vi.hoisted(() => vi.fn());

vi.mock('@/tools/video-editor/hooks/timelineStore', () => ({
  useTimelineEditorData,
  useTimelineChromeContext,
}));
vi.mock('@/tools/video-editor/hooks/useTimelineCommandsService', () => ({ useTimelineCommandsService }));

afterEach(() => vi.clearAllMocks());

describe('public trim fixture controls', () => {
  it('keeps the real trim port disabled until resolved config becomes ready', () => {
    useTimelineChromeContext.mockReturnValue({ canUndo: false, undo: vi.fn(), saveStatus: 'idle', commandSession: null });
    const trimClip = vi.fn().mockReturnValue({ ok: true });
    useTimelineCommandsService.mockReturnValue({ trimClip });
    useTimelineEditorData.mockReturnValue({ resolvedConfig: null });

    const view = render(<FixtureControls />);
    expect(screen.getByTestId('public-trim-trigger')).toBeDisabled();

    useTimelineEditorData.mockReturnValue({
      resolvedConfig: { clips: [{ id: 'f2-transition-clip', at: 0, from: 0, to: 3, track: 'V1' }] },
    });
    view.rerender(<FixtureControls />);

    const trigger = screen.getByTestId('public-trim-trigger');
    expect(trigger).toBeEnabled();
    trigger.click();
    expect(trimClip).toHaveBeenCalledWith({ clipId: 'f2-transition-clip', endTime: 2.5 });
  });
});
