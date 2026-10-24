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

import { WelcomeRunMode } from './WelcomeRunMode.tsx';

function mount(onContinue: (phase: 'connection' | 'local') => void = phase => { localStorage.setItem('astrid:welcome-v1', phase); }) {
  return render(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={onContinue} />);
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
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('run-mode choice', () => {
  it('Chrome with beforeinstallprompt defaults to App window', () => {
    install.prompt = { prompt: vi.fn(), userChoice: Promise.resolve({ outcome: 'accepted' }) };
    mount();
    expect(screen.getByRole('radio', { name: 'App window' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Browser tab' })).toBeInTheDocument();
  });

  it('Safari shows the Add to Dock hint and continues in the browser tab', () => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Version/17.0 Safari/605.1.15');
    mount();
    expect(screen.getByText('File → Add to Dock')).toBeInTheDocument();
    expect(screen.queryByRole('radio', { name: 'App window' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue in browser tab' }));
    expect(localStorage.getItem('astrid:welcome-v1')).toBe('connection');
  });

  it('Firefox offers the browser tab only', () => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 Firefox/132.0');
    mount();
    expect(screen.queryByRole('radio', { name: 'App window' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue in browser tab' })).toBeInTheDocument();
  });

  it('an installed standalone app has no window choice', () => {
    install.standalone = true;
    mount();
    expect(screen.queryByRole('radio', { name: 'App window' })).not.toBeInTheDocument();
    expect(screen.queryByRole('radio', { name: 'Browser tab' })).not.toBeInTheDocument();
  });

  it('writes connection before prompting and shows the accepted path', async () => {
    const prompt = vi.fn(async () => undefined);
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'accepted' }) };
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'App window' }));
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
    fireEvent.click(screen.getByRole('button', { name: 'App window' }));
    await vi.waitFor(() => expect(prompt).toHaveBeenCalledOnce());
    await vi.waitFor(() => expect(onContinue).toHaveBeenCalledWith('connection'));
    expect(localStorage.getItem('astrid:welcome-v1')).toBe('connection');
    expect(screen.queryByText('Astrid opened in its own window')).not.toBeInTheDocument();
  });
});
