import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { finishEditorTour } from '@/tools/video-editor/tour/runner/tourBeats';
import { registerBrowserTourFinish } from '@/tools/video-editor/tour/runner/tourBeats';
import { startEditorTour, setEditorTourBeat, getEditorTourState } from '@/shared/state/editorTourStore';
import { useEffect } from 'react';
const spies = vi.hoisted(() => ({ record: vi.fn(), connected: vi.fn() }));
vi.mock('@/tools/video-editor/tour/runner/tourRecord', () => ({ recordEditorTour: spies.record, buildEditorTourRecord: vi.fn() }));
vi.mock('./BrowserTourEditor', () => ({ BrowserTourEditor: ({onFinish}: {onFinish:()=>void}) => {
  useEffect(() => { const off = registerBrowserTourFinish(onFinish); startEditorTour(); return off; }, [onFinish]);
  return <><h1>Welcome to Astrid</h1><button onClick={finishEditorTour}>Skip</button><button onClick={() => { setEditorTourBeat(3, 'feedback'); finishEditorTour(); }}>Done</button></>;
} }));
vi.mock('./WelcomeConnection', () => ({ default: () => { spies.connected(); return <h1>Connect your machine</h1>; } }));
import { WelcomeFlow } from './WelcomeFlow';
beforeEach(() => { localStorage.clear(); spies.record.mockClear(); spies.connected.mockClear(); window.history.replaceState({}, '', '/tools/video-editor'); });
for (const action of ['Skip', 'Done']) it(`${action} uses one local-only handoff before mounting connection`, async () => {
  render(<WelcomeFlow />);
  expect(screen.getByText('Welcome to Astrid')).toBeInTheDocument();
  expect(spies.connected).not.toHaveBeenCalled();
  fireEvent.click(screen.getByText(action));
  await waitFor(() => expect(screen.getByText('Connect your machine')).toBeInTheDocument());
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('connection');
  expect(getEditorTourState().status).toBe('idle');
  expect(spies.record).not.toHaveBeenCalled();
});
