import { act, fireEvent, render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { TimelineRenderControls } from './TimelineRenderControls';

const mocks = vi.hoisted(() => ({
  useTimelineChromeContext: vi.fn(),
}));

vi.mock('@/tools/video-editor/hooks/timelineStore.ts', () => ({
  useTimelineChromeContext: mocks.useTimelineChromeContext,
}));

function chrome(overrides: Record<string, unknown> = {}) {
  return {
    renderDestination: 'download',
    renderStatus: 'done',
    renderDirty: false,
    renderResultUrl: '/api/astrid/v1/objects/render.mp4',
    renderResultFilename: 'render.mp4',
    renderProgress: null,
    activeRenderTaskId: null,
    startRender: vi.fn(),
    cancelRender: vi.fn(),
    setRenderDestination: vi.fn(),
    ...overrides,
  };
}

describe('TimelineRenderControls', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('does not auto-open the player or download for a result that already existed', () => {
    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      renderResultInfo: { revision: 4, completedAt: 1000 },
    }));

    render(<TimelineRenderControls previewActionButtonClass="" />);

    expect(screen.queryByRole('combobox', { name: 'Render destination' })).toBeNull();
    expect(screen.queryByTestId('timeline-render-player')).toBeNull();
    expect(screen.queryByRole('link', { name: /Download/ })).toBeNull();
    expect(screen.getByRole('button', { name: /Play last render/ })).toBeTruthy();
  });

  it('opens a streaming player when a render completes and reopens it from Play last render', () => {
    const anchorClick = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => undefined);
    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      renderStatus: 'rendering', renderResultUrl: null, renderResultFilename: null, renderResultInfo: null,
    }));
    const { rerender } = render(<TimelineRenderControls previewActionButtonClass="" />);
    expect(screen.queryByTestId('timeline-render-player')).toBeNull();

    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      renderResultInfo: { revision: 7, completedAt: 2000 },
    }));
    rerender(<TimelineRenderControls previewActionButtonClass="" />);

    const video = screen.getByTestId('timeline-render-player') as HTMLVideoElement;
    expect(video.getAttribute('src')).toBe('/api/astrid/v1/objects/render.mp4');
    expect(video.hasAttribute('controls')).toBe(true);
    expect(video.getAttribute('preload')).toBe('metadata');
    expect(screen.getByText(/Timeline version 7/)).toBeTruthy();
    // Download is an explicit link; nothing was clicked automatically.
    const link = screen.getByRole('link', { name: /Download/ });
    expect(link.getAttribute('href')).toBe('/api/astrid/v1/objects/render.mp4');
    expect(link.getAttribute('download')).toBe('render.mp4');
    expect(anchorClick).not.toHaveBeenCalled();

    act(() => { fireEvent.keyDown(document.activeElement ?? document.body, { key: 'Escape' }); });
    fireEvent.click(screen.getByRole('button', { name: /Play last render/ }));
    expect(screen.getByTestId('timeline-render-player')).toBeTruthy();
    anchorClick.mockRestore();
  });

  it('keeps cancellation visible for an active render', () => {
    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      renderStatus: 'rendering',
      activeRenderTaskId: 'task-1',
      renderProgress: { current: 4, total: 10, percent: 40, phase: 'render' },
    }));

    render(<TimelineRenderControls previewActionButtonClass="" />);

    expect(screen.getByRole('button', { name: 'Cancel render' })).toBeTruthy();
  });
});


it('places a supplied pane control immediately after Render and before cancellation', () => {
  mocks.useTimelineChromeContext.mockReturnValue(chrome({ renderStatus: 'rendering', activeRenderTaskId: 'task-1' }));
  render(<TimelineRenderControls previewActionButtonClass="" afterRenderControl={<button aria-label="Panel display">Panel</button>} />);
  const renderButton = screen.getByRole('button', { name: 'Render' });
  const panelButton = screen.getByRole('button', { name: 'Panel display' });
  expect(renderButton).toBeDisabled();
  expect(panelButton).not.toBeDisabled();
  expect(renderButton.nextElementSibling).toBe(panelButton);
  expect(panelButton.nextElementSibling).toBe(screen.getByRole('button', { name: 'Cancel render' }));
});
