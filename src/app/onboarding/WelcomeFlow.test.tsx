import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { finishEditorTour } from '@/tools/video-editor/tour/runner/tourBeats';
import { registerBrowserTourFinish } from '@/tools/video-editor/tour/runner/tourBeats';
import { startEditorTour, setEditorTourBeat, getEditorTourState } from '@/shared/state/editorTourStore';
import { useEffect } from 'react';
const spies = vi.hoisted(() => ({ record: vi.fn(), connected: vi.fn() }));
vi.mock('@/tools/video-editor/tour/runner/tourRecord', () => ({ recordEditorTour: spies.record, buildEditorTourRecord: vi.fn() }));
vi.mock('./BrowserTourEditor', () => ({ BrowserTourEditor: ({onFinish}: {onFinish:()=>void}) => {
  useEffect(() => {
    const off = registerBrowserTourFinish(onFinish);
    const onKey = (event: KeyboardEvent) => { if (event.key === 'Escape') finishEditorTour(); };
    window.addEventListener('keydown', onKey);
    startEditorTour();
    return () => { off(); window.removeEventListener('keydown', onKey); };
  }, [onFinish]);
  return <><h1>Welcome to Astrid</h1><button onClick={finishEditorTour}>Skip</button><button onClick={() => { setEditorTourBeat(3, 'feedback'); finishEditorTour(); }}>Done</button></>;
} }));
vi.mock('./WelcomeConnection', () => ({ default: () => { spies.connected(); return <h1>Connect your machine</h1>; } }));
vi.mock('./WelcomeRunMode', () => ({ WelcomeRunMode: ({ onContinue, runMode, setRunMode }: { onContinue: (phase: 'local' | 'connection') => void; runMode: 'hosted' | 'local'; setRunMode: (mode: 'hosted' | 'local') => void }) => <><h1>How do you want to run Astrid?</h1><button onClick={() => onContinue('connection')}>Connect</button><button onClick={() => { setRunMode('local'); onContinue('local'); }}>Local</button><span>{runMode}</span></> }));
vi.mock('./WelcomeLocalSetup', () => ({ WelcomeLocalSetup: ({ onBack }: { onBack: () => void }) => <><h1>Have your agent set it up</h1><button onClick={onBack}>Back</button></> }));
import { WelcomeFlow } from './WelcomeFlow';
beforeEach(() => {
  localStorage.clear(); spies.record.mockClear(); spies.connected.mockClear();
  vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Chrome/131.0.0.0 Safari/537.36');
  window.history.replaceState({}, '', '/tools/video-editor');
});
for (const action of ['Skip', 'Done']) it(`${action} opens the run-mode choice`, async () => {
  render(<WelcomeFlow entry="tour" />);
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('tour');
  expect(screen.getByText('Welcome to Astrid')).toBeInTheDocument();
  expect(spies.connected).not.toHaveBeenCalled();
  fireEvent.click(screen.getByText(action));
  await waitFor(() => expect(screen.getByText('How do you want to run Astrid?')).toBeInTheDocument());
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('choose');
  expect(getEditorTourState().status).toBe('idle');
  expect(spies.record).not.toHaveBeenCalled();
});

it('Escape opens the run-mode choice', async () => {
  render(<WelcomeFlow entry="tour" />);
  fireEvent.keyDown(window, { key: 'Escape' });
  expect(await screen.findByText('How do you want to run Astrid?')).toBeInTheDocument();
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('choose');
});

it('moves from the choice to local setup or connection and back', async () => {
  render(<WelcomeFlow entry="choose" />);
  fireEvent.click(screen.getByText('Local'));
  expect(await screen.findByText('Have your agent set it up')).toBeInTheDocument();
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('local');
  fireEvent.click(screen.getByText('Back'));
  expect(await screen.findByText('How do you want to run Astrid?')).toBeInTheDocument();
  expect(screen.getByText('local')).toBeInTheDocument();
  fireEvent.click(screen.getByText('Connect'));
  expect(await screen.findByText('Connect your machine')).toBeInTheDocument();
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('connection');
});

it('returns from the local screen with local selected, including after loading that phase directly', async () => {
  render(<WelcomeFlow entry="local" />);
  expect(await screen.findByText('Have your agent set it up')).toBeInTheDocument();
  fireEvent.click(screen.getByText('Back'));
  expect(await screen.findByText('How do you want to run Astrid?')).toBeInTheDocument();
  expect(screen.getByText('local')).toBeInTheDocument();
});

it.each([['local editor', { localBuild: true }], ['phone', { localBuild: false }]])('%s goes from the tour straight to connection', async (_name, props) => {
  if (_name === 'phone') {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue('iPhone');
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X)');
  }
  render(<WelcomeFlow entry="tour" {...props} />);
  fireEvent.click(screen.getByText('Done'));
  expect(await screen.findByText('Connect your machine')).toBeInTheDocument();
  expect(localStorage.getItem('astrid:welcome-v1')).toBe('connection');
  expect(screen.queryByText('How do you want to run Astrid?')).not.toBeInTheDocument();
});
