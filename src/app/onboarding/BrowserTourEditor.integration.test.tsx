import { render, waitFor, screen, within } from '@testing-library/react';
import { onlineManager, QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, afterEach, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { webcrypto } from 'node:crypto';
import { TooltipProvider } from '@/shared/components/ui/tooltip';
import { useVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext';

let runtime: ReturnType<typeof useVideoEditorRuntime>;
// Keep the actual provider and extension activation. Browser media and layout are outside jsdom.
vi.mock('@/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx', () => ({ RemotionPreview: () => {
  runtime = useVideoEditorRuntime();
  return <div data-testid="captured-preview" />;
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
const requests: string[] = [];
beforeEach(() => {
  onlineManager.setOnline(true);
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
it('shows the bundled tour with no Runtime requests', async () => {
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
  const chat = pane.querySelector('[data-tasks-pane-chat]')!;
  expect(within(pane).getByRole('textbox')).toHaveAttribute('readonly');
  expect(chat.querySelector('[data-editor-tour="chat-composer"]')).not.toBeNull();
  expect(chat.querySelector('[data-editor-tour="chat-transcript"]')).not.toBeNull();
  expect(chat.querySelector('[data-editor-tour="chat-send"]')).not.toBeNull();
  expect(document.querySelectorAll('[data-editor-tour="chat-composer"]')).toHaveLength(1);
  await waitFor(() => expect(runtime).toBeTruthy());
  expect(runtime.extensionRuntime.extensions.map(extension => extension.manifest.id)).toContain('haus.astrid.threejs-live-editor');
  expect(runtime.provider.persistenceEnabled).toBe(false);
  expect(runtime.livePermissionService).toBeUndefined();
  expect(requests.length).toBeGreaterThan(0);
  expect(requests.every(url => url.startsWith('/astrid/onboarding/'))).toBe(true);
});
