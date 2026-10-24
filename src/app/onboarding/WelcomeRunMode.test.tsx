import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const install = vi.hoisted(() => ({
  prompt: null as unknown,
  standalone: false,
  outcome: 'accepted' as 'accepted' | 'dismissed',
  calledWithPhase: '' as string,
  consume: vi.fn(),
}));
vi.mock('@/shared/hooks/platformInstall/signals.ts', () => ({
  useInstallPromptSignals: () => ({ deferredPrompt: install.prompt, consumeDeferredPrompt: install.consume }),
  useStandaloneStatus: () => install.standalone,
  runInstallPrompt: async (event: { prompt: () => Promise<void>; userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }> }) => {
    install.calledWithPhase = localStorage.getItem('astrid:welcome-v1') ?? '';
    await event.prompt();
    return event.userChoice;
  },
}));

import { WelcomeRunMode, type RunMode } from './WelcomeRunMode.tsx';

function mount(onContinue: (phase: 'connection' | 'local') => void = phase => { localStorage.setItem('astrid:welcome-v1', phase); }, runMode: RunMode = 'hosted') {
  return render(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={onContinue} runMode={runMode} setRunMode={vi.fn()} />);
}

beforeEach(() => {
  cleanup();
  localStorage.clear();
  install.prompt = null;
  install.standalone = false;
  install.outcome = 'accepted';
  install.calledWithPhase = '';
  install.consume.mockReset().mockReturnValue(true);
  vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Chrome/131.0.0.0 Safari/537.36');
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); delete (navigator as Navigator & { clipboard?: Clipboard }).clipboard; });

describe('run-mode choice', () => {
  it('selects the hosted tile by default and shows App window by default in Chrome', () => {
    install.prompt = { prompt: vi.fn(), userChoice: Promise.resolve({ outcome: 'accepted' }) };
    mount();
    expect(screen.getByRole('radio', { name: 'Use it at astrid.haus' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'App window' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Browser tab' })).toBeInTheDocument();
  });

  it('Safari explains the browser requirement and copies the page link for Chrome or Edge', async () => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Version/17.0 Safari/605.1.15');
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    mount();
    expect(screen.getByText('Needs Chrome or Edge to reach your computer.')).toBeInTheDocument();
    expect(screen.queryByRole('radiogroup', { name: 'Open in' })).not.toBeInTheDocument();
    expect(screen.queryByText(/Add to Dock/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Copy link for Chrome or Edge' }));
    await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Copied. Open it in Chrome or Edge.' })).toBeInTheDocument());
    expect(writeText).toHaveBeenCalledWith(window.location.href);
    expect(localStorage.getItem('astrid:welcome-v1')).toBeNull();
  });

  it('Firefox offers the browser tab only', () => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 Firefox/132.0');
    mount();
    expect(screen.queryByRole('radio', { name: 'App window' })).not.toBeInTheDocument();
    expect(screen.queryByRole('radiogroup', { name: 'Open in' })).not.toBeInTheDocument();
    expect(screen.getByText('Needs Chrome or Edge to reach your computer.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Copy link for Chrome or Edge' })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: 'Run everything on your computer' })).toBeInTheDocument();
  });

  it('an installed standalone app has no window choice', () => {
    install.standalone = true;
    mount();
    expect(screen.queryByRole('radiogroup', { name: 'Open in' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
  });

  it('writes connection before prompting and shows the accepted path', async () => {
    const prompt = vi.fn(async () => undefined);
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'accepted' }) };
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'Install app and continue' }));
    expect(install.calledWithPhase).toBe('connection');
    expect(prompt).toHaveBeenCalledOnce();
    expect(await screen.findByText('Astrid opened in its own window')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Continue here instead' })).toBeInTheDocument();
    expect(install.consume).toHaveBeenCalledOnce();
  });

  it('continues in this tab when the install prompt is dismissed', async () => {
    const onContinue = vi.fn();
    const prompt = vi.fn(async () => undefined);
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'dismissed' }) };
    install.outcome = 'dismissed';
    mount(onContinue);
    fireEvent.click(screen.getByRole('button', { name: 'Install app and continue' }));
    await vi.waitFor(() => expect(prompt).toHaveBeenCalledOnce());
    await vi.waitFor(() => expect(onContinue).toHaveBeenCalledWith('connection'));
    expect(localStorage.getItem('astrid:welcome-v1')).toBe('connection');
    expect(screen.queryByText('Astrid opened in its own window')).not.toBeInTheDocument();
  });

  it('shows Open in only while hosted is selected and continues to local setup', () => {
    install.prompt = { prompt: vi.fn(), userChoice: Promise.resolve({ outcome: 'accepted' }) };
    const onContinue = vi.fn();
    const setRunMode = vi.fn();
    const { rerender } = render(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={onContinue} runMode="hosted" setRunMode={setRunMode} />);
    fireEvent.click(screen.getByRole('radio', { name: 'Run everything on your computer' }));
    expect(setRunMode).toHaveBeenCalledWith('local');
    rerender(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={onContinue} runMode="local" setRunMode={setRunMode} />);
    expect(screen.queryByRole('radiogroup', { name: 'Open in' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Set up with your agent' }));
    expect(onContinue).toHaveBeenCalledWith('local');
  });
});
