import { act, render, waitFor, screen, within } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, afterEach, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { webcrypto } from 'node:crypto';
import { TooltipProvider } from '@/shared/components/ui/tooltip';
import { setEditorTourBeat } from '@/shared/state/editorTourStore';
import { useTimelineEditorData, useTimelineOpsFromStoreSafe } from '@/tools/video-editor/hooks/timelineStore';
import { useVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext';
import { useClipTypeRegistryContext } from '@/tools/video-editor/clip-types/ClipTypeRegistryContext';
import type { ClipRendererProps } from '@/tools/video-editor/clip-types/ClipTypeRegistry';
import type { ComponentType } from 'react';
import { TOUR_CLIP_IDS } from '@/tools/video-editor/tour/timeline/tourStages';

let captured: ReturnType<typeof useTimelineEditorData>;
let operations: ReturnType<typeof useTimelineOpsFromStoreSafe>;
let runtime: ReturnType<typeof useVideoEditorRuntime>;
// Keep the actual provider, extension activation and driver operations. Browser media and layout
// are outside jsdom: the preview boundary records the real resolved composition instead.
vi.mock('@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx', () => ({ RemotionPreview: () => {
  captured = useTimelineEditorData(); operations = useTimelineOpsFromStoreSafe(); runtime = useVideoEditorRuntime();
  const { registry } = useClipTypeRegistryContext();
  const scene = captured.resolvedConfig?.clips.find(clip => clip.clipType === 'haus.astrid.liveScene');
  const record = registry.resolve('haus.astrid.liveScene');
  if (!scene || record?.status !== 'active' || typeof record.renderer !== 'function') return <div data-testid="captured-preview" />;
  const Renderer = record.renderer as ComponentType<ClipRendererProps>;
  return <div data-testid="captured-preview"><Renderer clipId={scene.id} clipTypeId={scene.clipType!}
    time={0} sourceTime={2.5} source={scene.app as Record<string, unknown>} params={{}}
    width={1280} height={720} live={{bindings: [], diagnostics: [], getSource: () => undefined,
      getChannelMetadata: () => undefined, readLatestSample: () => undefined, readSampleAt: () => undefined,
      readSamples: () => [], getSampleCount: () => 0, resolveChannelId: () => undefined}} /></div>;
} }));
vi.mock('@/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx', () => ({ TimelineEditorCoreBody: () => null }));
vi.mock('@/tools/video-editor/tour/runner/EditorTourRunner.tsx', () => ({ EditorTourRunner: () => null }));
// A real iframe/Three.js frame cannot be driven in jsdom. Keep the shipped
// extension and its registered renderer real; stub only the iframe boundary.
vi.mock('@astrid/packs/rendering/ui/threejs-live-editor/SceneSurface', async () => {
  const React = await import('react');
  return { SceneSurface: ({ source, sourceTime, onReady }: { source?: unknown; sourceTime: number; onReady?: (reported?: unknown) => void }) => {
    React.useEffect(() => onReady?.({ events: [], shots: [], explore: null }), []);
    return <div data-testid="scene-renderer-ready" data-phase="ready" data-source-time={sourceTime}
      data-has-source={String(!!source)} />;
  } };
});
import { BrowserTourEditor } from './BrowserTourEditor';
import { EDITOR_TOUR_MEDIA } from '@/tools/video-editor/tour/tourMedia';
const requests: string[] = [];
beforeEach(() => {
  requests.length = 0;
  vi.stubGlobal('crypto', webcrypto);
  vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input); requests.push(url);
    if (!url.startsWith('/astrid/onboarding/lantern-valley-14s-v1/')) throw new Error(`Unexpected workspace request: ${url}`);
    const bytes = readFileSync(`public${url}`);
    return new Response(bytes);
  }));
});
afterEach(() => vi.unstubAllGlobals());
it('admits the bundled world and applies all three stages with only shipped asset fetches', async () => {
  render(<QueryClientProvider client={new QueryClient({defaultOptions:{queries:{retry:false}}})}><TooltipProvider><MemoryRouter>
    <BrowserTourEditor onFinish={() => undefined} />
  </MemoryRouter></TooltipProvider></QueryClientProvider>);
  const pane = screen.getByRole('complementary', { name: 'Task and chat pane' });
  expect(pane).toHaveAttribute('data-tasks-pane', 'true');
  expect(pane).toHaveAttribute('data-pane-side', 'right');
  const main = screen.getByRole('main', { name: 'Lantern Valley guided demo' });
  // The same right-pane width used by the connected editor reserves the second desktop column.
  expect(main).toHaveStyle({ '--tasks-pane-width': '300px' });
  expect(main.lastElementChild).toBe(pane);
  expect(main).toHaveClass('md:grid-cols-[minmax(0,1fr)_var(--tasks-pane-width)]');
  const extensionsDock = screen.getByTestId('video-editor-right-panel-dock');
  expect(extensionsDock).toHaveAttribute('data-open', 'true');
  expect(within(extensionsDock).getByRole('tab', { name: 'Extensions' })).toHaveAttribute('aria-selected', 'true');
  expect(await within(extensionsDock).findByRole('region', { name: 'World Explorer' })).toBeInTheDocument();
  const chat = pane.querySelector('[data-tasks-pane-chat]')!;
  expect(within(pane).getByRole('textbox')).toHaveAttribute('readonly');
  expect(chat.querySelector('[data-editor-tour="chat-composer"]')).not.toBeNull();
  expect(chat.querySelector('[data-editor-tour="chat-transcript"]')).not.toBeNull();
  expect(chat.querySelector('[data-editor-tour="chat-send"]')).not.toBeNull();
  expect(document.querySelectorAll('[data-editor-tour="chat-composer"]')).toHaveLength(1);
  await waitFor(() => expect(operations).toBeTruthy());
  act(() => setEditorTourBeat(1, 'land', true));
  await waitFor(() => expect(captured.resolvedConfig?.clips.some(clip => clip.clipType === 'haus.astrid.liveScene')).toBe(true));
  await waitFor(() => expect(document.querySelector('[data-testid="scene-renderer-ready"][data-phase="ready"]')).not.toBeNull());
  expect(document.querySelector('[data-testid="scene-renderer-ready"]')).toHaveAttribute('data-has-source', 'true');
  expect(document.querySelector('[data-testid="scene-renderer-ready"]')).toHaveAttribute('data-source-time', '2.5');
  expect(runtime.provider.persistenceEnabled).toBe(false);
  expect(runtime.livePermissionService).toBeUndefined();
  act(() => setEditorTourBeat(2, 'land', true));
  await waitFor(() => expect(captured.resolvedConfig?.clips.filter(clip => (
    TOUR_CLIP_IDS.stills.includes(clip.id as typeof TOUR_CLIP_IDS.stills[number]) && clip.clipType === 'hold'
  ))).toHaveLength(4));
  act(() => setEditorTourBeat(3, 'land', true));
  await waitFor(() => expect(captured.resolvedConfig?.clips.some(clip => clip.id === TOUR_CLIP_IDS.video && clip.clipType === 'media')).toBe(true));
  expect(requests.length).toBeGreaterThan(0);
  expect(requests.every(url => url.startsWith('/astrid/onboarding/'))).toBe(true);
  expect(EDITOR_TOUR_MEDIA.video).toBeTruthy();
});
