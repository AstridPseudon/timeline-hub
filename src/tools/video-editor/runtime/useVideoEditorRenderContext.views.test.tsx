import React from 'react';
import { cleanup, fireEvent, render, renderHook, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useVideoEditorRuntime: () => ({
    provider: {}, timelineId: 't', timelineName: 'Fixture', userId: 'fixture',
    extensions: {registry:{panels:[],inspectorSections:[]}},
  }),
}));
vi.mock('@/tools/video-editor/hooks/timelineStore.ts', () => ({
  useTimelineChromeContext: () => ({}), useTimelineEditorData: () => ({}),
  useTimelineEditorOps: () => ({}), useTimelinePlaybackContext: () => ({}),
}));
import { useVideoEditorAssetPanels } from './useVideoEditorRenderContext';

afterEach(cleanup);
it('lists generated read views through the real panel resolver and production hook', async () => {
  const hook = renderHook(() => useVideoEditorAssetPanels());
  const panel = hook.result.current.find(p => p.id === 'astrid.timeline.views');
  expect(panel).toBeDefined();
  render(<>{panel!.render({} as never)}</>);
  expect(screen.getByRole('region', {name:'Timeline views'})).toBeDefined();
  expect(screen.getByRole('option', {name:'Story overview'})).toBeDefined();
  fireEvent.click(screen.getByRole('button',{name:'Read view'}));
  await waitFor(()=>expect(screen.getByRole('alert').getAttribute('data-code')).toBe('unsupported'));
});
