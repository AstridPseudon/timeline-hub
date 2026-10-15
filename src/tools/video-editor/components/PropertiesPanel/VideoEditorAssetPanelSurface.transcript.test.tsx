import { createElement } from 'react';
import { cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import type { TimelineStoreApi } from '../../hooks/timelineStore.ts';
import type { TimelineViewStoreApi } from '../../lib/timeline-view-store.ts';
import { setupTranscriptHost } from '../../lib/transcript-panel-binding.fixture.ts';
import { TranscriptPanel } from '@astrid/packs/rendering/ui/transcript/TranscriptPanel';
import type { ExtensionContext, PanelRenderProps } from '@reigh/editor-sdk';
import { VideoEditorAssetPanelSurface } from './VideoEditorAssetPanelSurface';

const state = vi.hoisted(() => ({ store: null as TimelineStoreApi | null, view: null as TimelineViewStoreApi | null }));
vi.mock('./AssetPanel.tsx', () => ({ default: () => null }));
vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({ useOptionalVideoEditorRuntime: () => ({ timelineViewStore: state.view }) }));
vi.mock('@/tools/video-editor/hooks/timelineStore.ts', async (importOriginal) => ({
  ...await importOriginal<object>(),
  useTimelineStoreApiSafe: () => state.store,
  useTimelineEditorData: () => state.store!.getState().data,
  useTimelineEditorOps: () => state.store!.getState().ops,
}));
vi.mock('@/tools/video-editor/runtime/useVideoEditorRenderContext.ts', () => {
  const panel = { id: 'transcript', label: 'Transcript', extensionId: 'astrid', placement: 'asset-panel', render: (props: PanelRenderProps) => createElement(TranscriptPanel, { ...props, context: {} as ExtensionContext }) };
  return { useVideoEditorPanelRegistry: () => ({ panels: [panel] }), useVideoEditorAssetPanels: () => [panel] };
});
afterEach(cleanup);

it('binds the rendering pack panel at the existing app host boundary with live import, correction and public seek', async () => {
  const host = await setupTranscriptHost();
  state.store = host.store; state.view = host.view;
  const seek = vi.fn();
  host.store.getState().syncOpsSlice({ ...host.store.getState().ops, onClickTimeArea: seek });
  const view = render(<VideoEditorAssetPanelSurface includeBuiltIn={false} activePanelKey="astrid:transcript" />);
  expect(view.getByText(/No transcript yet/)).toBeTruthy();
  fireEvent.change(view.getByLabelText('Import transcript JSON'), { target: { files: [{ text: async () => JSON.stringify({ assetId: 'media', segments: [{ start: 0, end: 4, text: 'Hello' }] }) }] } });
  await waitFor(() => expect(view.getByText('Hello')).toBeTruthy());
  expect(host.commitData).toHaveBeenCalledTimes(1);
  fireEvent.click(view.getByRole('button', { name: 'Seek segment' }));
  expect(seek).toHaveBeenCalledWith(0);
  fireEvent.click(view.getByRole('button', { name: 'Edit segment' }));
  fireEvent.change(view.getByRole('textbox'), { target: { value: 'Corrected' } });
  fireEvent.click(view.getByRole('button', { name: 'Save correction' }));
  expect(view.getByText('Corrected')).toBeTruthy();
  expect(host.commitData).toHaveBeenCalledTimes(2);
  view.rerender(<VideoEditorAssetPanelSurface includeBuiltIn={false} activePanelKey={null} />);
  expect(view.getByTestId('astrid-transcript-panel')).not.toBeVisible();
});
