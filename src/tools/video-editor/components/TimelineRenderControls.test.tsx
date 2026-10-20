import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
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
    downloadRenderResult: vi.fn(async () => undefined),
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
    // The explicit link retains the admitted object identity; no automatic download.
    const link = screen.getByRole('link', { name: /Download/ });
    expect(link.getAttribute('href')).toBe('/api/astrid/v1/objects/render.mp4');
    expect(link.getAttribute('download')).toBe('render.mp4');
    expect(anchorClick).not.toHaveBeenCalled();

    act(() => { fireEvent.keyDown(document.activeElement ?? document.body, { key: 'Escape' }); });
    fireEvent.click(screen.getByRole('button', { name: /Play last render/ }));
    expect(screen.getByTestId('timeline-render-player')).toBeTruthy();
    anchorClick.mockRestore();
  });

  it('uses the bound download callback, prevents navigation, and keeps playback/retry after a refusal', async () => {
    const downloadRenderResult = vi.fn()
      .mockRejectedValueOnce(new Error('Could not download render: HTTP 403'))
      .mockResolvedValueOnce(undefined);
    mocks.useTimelineChromeContext.mockReturnValue(chrome({ downloadRenderResult }));
    render(<TimelineRenderControls previewActionButtonClass="" />);
    fireEvent.click(screen.getByRole('button', { name: /Play last render/ }));
    const link = screen.getByRole('link', { name: 'Download' });

    expect(fireEvent.click(link)).toBe(false);
    expect(downloadRenderResult).toHaveBeenCalledOnce();
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('HTTP 403'));
    expect(screen.getByTestId('timeline-render-player')).toHaveAttribute('src', '/api/astrid/v1/objects/render.mp4');
    expect(link).toHaveAttribute('href', '/api/astrid/v1/objects/render.mp4');
    expect(link).toHaveAttribute('download', 'render.mp4');

    expect(fireEvent.click(link)).toBe(false);
    await waitFor(() => expect(screen.queryByRole('alert')).toBeNull());
    expect(downloadRenderResult).toHaveBeenCalledTimes(2);
  });

  it('does not issue a second download while its binary read is pending', async () => {
    let complete!: () => void;
    const downloadRenderResult = vi.fn(() => new Promise<void>((resolve) => { complete = resolve; }));
    mocks.useTimelineChromeContext.mockReturnValue(chrome({ downloadRenderResult }));
    render(<TimelineRenderControls previewActionButtonClass="" />);
    fireEvent.click(screen.getByRole('button', { name: /Play last render/ }));
    fireEvent.click(screen.getByRole('link', { name: 'Download' }));
    const pending = screen.getByRole('link', { name: 'Downloading…' });
    expect(pending).toHaveAttribute('aria-disabled', 'true');
    fireEvent.click(pending);
    expect(downloadRenderResult).toHaveBeenCalledOnce();
    await act(async () => { complete(); });
    expect(screen.getByRole('link', { name: 'Download' })).toBeTruthy();
  });

  it('keeps the new result download available and ignores an older download failure', async () => {
    let rejectOld!: (error: Error) => void;
    let completeNew!: () => void;
    const downloadRenderResult = vi.fn(() => new Promise<void>((_resolve, reject) => { rejectOld = reject; }));
    const nextDownload = vi.fn(() => new Promise<void>((resolve) => { completeNew = resolve; }));
    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      downloadRenderResult, renderResultInfo: { revision: 7, completedAt: 1000 },
    }));
    const { rerender } = render(<TimelineRenderControls previewActionButtonClass="" />);
    fireEvent.click(screen.getByRole('button', { name: /Play last render/ }));
    fireEvent.click(screen.getByRole('link', { name: 'Download' }));
    expect(downloadRenderResult).toHaveBeenCalledOnce();

    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      downloadRenderResult: nextDownload,
      renderResultUrl: '/api/astrid/v1/objects/next.mp4',
      renderResultInfo: { revision: 8, completedAt: 2000 },
    }));
    rerender(<TimelineRenderControls previewActionButtonClass="" />);
    fireEvent.click(screen.getByRole('link', { name: 'Download' }));
    expect(nextDownload).toHaveBeenCalledOnce();

    await act(async () => { rejectOld(new Error('The old render result changed.')); });
    expect(screen.queryByRole('alert')).toBeNull();
    expect(screen.getByRole('link', { name: 'Downloading…' })).toHaveAttribute('aria-disabled', 'true');
    await act(async () => { completeNew(); });
    expect(screen.getByRole('link', { name: 'Download' })).toHaveAttribute('aria-disabled', 'false');
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

  it('shows a structured seam report and separate eligible declaration actions', () => {
    const declareHardCuts = vi.fn();
    const acknowledgeCues = vi.fn();
    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      renderStatus: 'error',
      renderLog: 'Visual seam admission blocked: boundary at frame 30 has undeclared visual cues',
      visualSeamReport: {
        version: 1,
        fps: 30,
        guardFrames: 2,
        boundaries: [{
          frame: 30,
          timeSeconds: 1,
          intent: undefined,
          participants: [{
            ownerId: 'clip-b', clipId: 'clip-b', path: ['clip', 'clip-b'], behavior: 'motion-start',
            cue: {frame: 30, kind: 'motion-start', id: 'motion', path: ['clip', 'clip-b']},
          }],
          structuralIssues: [],
          unacknowledgedRisk: true,
          requiresIntent: true,
        }],
        opaqueElements: [],
        structuralIssues: [],
        cues: [],
        warningCount: 1,
        blocked: true,
      },
      canDeclareSeamsAsHardCuts: false,
      declareSeamsAsHardCuts: declareHardCuts,
      canAcknowledgeVisualCues: true,
      acknowledgeVisualCuesAsSynchronized: acknowledgeCues,
    }));

    render(<TimelineRenderControls previewActionButtonClass="" />);

    expect(screen.getByRole('region', {name: 'Visual seam admission report'})).toBeTruthy();
    expect(screen.getByText('Frame 30 · 1.00s')).toBeTruthy();
    expect(screen.getByText('motion-start')).toBeTruthy();
    expect(screen.queryByRole('button', {name: 'Declare flagged boundaries as hard cuts'})).toBeNull();
    fireEvent.click(screen.getByRole('button', {name: 'Acknowledge listed cues as synchronized'}));
    expect(acknowledgeCues).toHaveBeenCalledOnce();
    expect(declareHardCuts).not.toHaveBeenCalled();
  });

  it('offers the hard-cut declaration only when the hook marks all flagged boundaries eligible', () => {
    const declareHardCuts = vi.fn();
    mocks.useTimelineChromeContext.mockReturnValue(chrome({
      renderStatus: 'error',
      renderLog: 'Visual seam admission blocked',
      visualSeamReport: {
        version: 1, fps: 30, guardFrames: 2,
        boundaries: [{
          frame: 30, timeSeconds: 1,
          participants: [{ownerId: 'b', clipId: 'b', path: ['clip', 'b'], behavior: 'source-change'}],
          structuralIssues: [], unacknowledgedRisk: true, requiresIntent: true,
        }],
        opaqueElements: [], structuralIssues: [], cues: [], warningCount: 1, blocked: true,
      },
      canDeclareSeamsAsHardCuts: true,
      declareSeamsAsHardCuts: declareHardCuts,
      canAcknowledgeVisualCues: false,
      acknowledgeVisualCuesAsSynchronized: vi.fn(),
    }));

    render(<TimelineRenderControls previewActionButtonClass="" />);

    fireEvent.click(screen.getByRole('button', {name: 'Declare flagged boundaries as hard cuts'}));
    expect(declareHardCuts).toHaveBeenCalledOnce();
    expect(screen.queryByRole('button', {name: 'Acknowledge listed cues as synchronized'})).toBeNull();
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
