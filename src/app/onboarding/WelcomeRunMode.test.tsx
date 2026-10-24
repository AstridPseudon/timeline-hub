import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const install = vi.hoisted(() => ({
  prompt: null as unknown,
  standalone: false,
  outcome: 'accepted' as 'accepted' | 'dismissed',
  calledWithPhase: '' as string,
  onContinue: vi.fn(),
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

import { WelcomeRunMode, type RunMode, type WindowMode } from './WelcomeRunMode.tsx';

function mount(onContinue: (phase: 'connection' | 'local') => void = install.onContinue, runMode: RunMode = 'hosted', windowMode: WindowMode = 'app-window', setWindowMode = vi.fn()) {
  return render(<WelcomeRunMode windowMode={windowMode} setWindowMode={setWindowMode} onContinue={onContinue} runMode={runMode} setRunMode={vi.fn()} />);
}

beforeEach(() => {
  cleanup();
  localStorage.clear();
  sessionStorage.clear();
  install.prompt = null;
  install.standalone = false;
  install.outcome = 'accepted';
  install.calledWithPhase = '';
  install.onContinue.mockReset();
  install.consume.mockReset().mockImplementation(() => { install.prompt = null; return true; });
  vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Chrome/131.0.0.0 Safari/537.36');
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); delete (navigator as Navigator & { clipboard?: Clipboard }).clipboard; });

describe('run-mode choice', () => {
  it('selects the hosted tile by default and explains the install-as-app choice in Chrome', () => {
    install.prompt = { prompt: vi.fn(), userChoice: Promise.resolve({ outcome: 'accepted' }) };
    mount();
    expect(screen.getByRole('radio', { name: 'Use it at astrid.haus' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radiogroup', { name: 'How to open Astrid' })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: 'Install as app' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Stay in browser' })).toBeInTheDocument();
    expect(screen.getByText("Its own window and a Dock or taskbar icon. Nothing to download; it's still astrid.haus.")).toBeInTheDocument();
  });

  it('explains that the browser choice keeps using this tab', () => {
    install.prompt = { prompt: vi.fn(), userChoice: Promise.resolve({ outcome: 'accepted' }) };
    const setWindowMode = vi.fn();
    mount(undefined, 'hosted', 'browser-tab', setWindowMode);
    expect(screen.getByRole('radio', { name: 'Stay in browser' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText('Keep using it in this tab.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue in this tab' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue in this tab' }));
    expect(install.onContinue).toHaveBeenCalledWith('connection');
    fireEvent.click(screen.getByRole('radio', { name: 'Install as app' }));
    expect(setWindowMode).toHaveBeenCalledWith('app-window');
  });

  it('keeps the local option description short and links here to the editor repository', () => {
    mount(() => undefined, 'local');

    const localLabel = screen.getByRole('radio', { name: 'Run everything on your computer' }).closest('label');
    expect(localLabel?.textContent).toContain('The editor runs on your machine too: no browser permission, works offline, and you can change Astrid itself. GitHub here.');

    const link = screen.getByRole('link', { name: 'here' });
    expect(link).toHaveAttribute('href', 'https://github.com/banodoco/astrid-app');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noreferrer');
    expect(link).toHaveClass('underline', 'underline-offset-4', 'hover:text-foreground');
  });

  it('Safari explains the browser requirement and copies the page link for Chrome or Edge', async () => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Version/17.0 Safari/605.1.15');
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    mount();
    expect(screen.getByText('Needs Chrome or Edge to reach your computer.')).toBeInTheDocument();
    expect(screen.queryByRole('radiogroup', { name: 'How to open Astrid' })).not.toBeInTheDocument();
    expect(screen.queryByText(/Add to Dock/)).not.toBeInTheDocument();
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: 'Copy link for Chrome or Edge' }));
      await Promise.resolve();
    });
    await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Copied. Open it in Chrome or Edge.' })).toBeInTheDocument());
    expect(writeText).toHaveBeenCalledWith(window.location.href);
    expect(localStorage.getItem('astrid:welcome-v1')).toBeNull();
  });

  it('Firefox offers the browser tab only', () => {
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 Firefox/132.0');
    mount();
    expect(screen.queryByRole('radio', { name: 'Install as app' })).not.toBeInTheDocument();
    expect(screen.queryByRole('radiogroup', { name: 'How to open Astrid' })).not.toBeInTheDocument();
    expect(screen.getByText('Needs Chrome or Edge to reach your computer.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Copy link for Chrome or Edge' })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: 'Run everything on your computer' })).toBeInTheDocument();
  });

  it('mobile Continue enters the connection phase', () => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue('iPhone');
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) Chrome/131.0.0.0 Mobile Safari/537.36');
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'Continue in this tab' }));

    expect(install.onContinue).toHaveBeenCalledWith('connection');
  });

  it('an installed standalone app has no window choice', () => {
    install.standalone = true;
    mount();
    expect(screen.queryByRole('radiogroup', { name: 'How to open Astrid' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(install.onContinue).toHaveBeenCalledWith('connection');
  });

  it('writes connection before prompting and shows the accepted path', async () => {
    const prompt = vi.fn(async () => undefined);
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'accepted' }) };
    mount();
    fireEvent.click(screen.getByRole('button', { name: 'Install and continue' }));
    expect(install.calledWithPhase).toBe('connection');
    expect(prompt).toHaveBeenCalledOnce();
    expect(await screen.findByText('Astrid opened in its own window')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Continue here instead' })).toBeInTheDocument();
    expect(install.onContinue).not.toHaveBeenCalled();
    expect(install.consume).toHaveBeenCalledOnce();
  });

  it('continues automatically when the accepted install reparents this tab as the app window', async () => {
    const prompt = vi.fn(async () => undefined);
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'accepted' }) };
    const view = mount();
    fireEvent.click(screen.getByRole('button', { name: 'Install and continue' }));
    expect(await screen.findByText('Astrid opened in its own window')).toBeInTheDocument();
    install.standalone = true;
    view.rerender(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={install.onContinue} runMode="hosted" setRunMode={vi.fn()} />);
    await vi.waitFor(() => expect(install.onContinue).toHaveBeenCalledWith('connection'));
    expect(screen.queryByText('Astrid opened in its own window')).not.toBeInTheDocument();
  });

  it('stays on this card and restores the phase when the install prompt is dismissed', async () => {
    localStorage.setItem('astrid:welcome-v1', 'choose');
    const onContinue = vi.fn();
    const prompt = vi.fn(async () => undefined);
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'dismissed' }) };
    mount(onContinue);
    fireEvent.click(screen.getByRole('button', { name: 'Install and continue' }));
    await vi.waitFor(() => expect(prompt).toHaveBeenCalledOnce());
    expect(await screen.findByText('Not installed. You can install it any time from the install icon in the address bar.')).toBeInTheDocument();
    expect(onContinue).not.toHaveBeenCalled();
    expect(localStorage.getItem('astrid:welcome-v1')).toBe('choose');
    expect(install.consume).toHaveBeenCalledOnce();
    expect(install.prompt).toBeNull();
    expect(screen.queryByRole('radiogroup', { name: 'How to open Astrid' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue in this tab' })).toBeInTheDocument();
    expect(screen.queryByText('Astrid opened in its own window')).not.toBeInTheDocument();
  });

  it('stays on this card and restores the phase when the install prompt throws', async () => {
    localStorage.setItem('astrid:welcome-v1', 'choose');
    const onContinue = vi.fn();
    const prompt = vi.fn(async () => { throw new Error('prompt failed'); });
    install.prompt = { prompt, userChoice: Promise.resolve({ outcome: 'dismissed' }) };
    mount(onContinue);
    fireEvent.click(screen.getByRole('button', { name: 'Install and continue' }));
    await vi.waitFor(() => expect(prompt).toHaveBeenCalledOnce());
    expect(await screen.findByText('Not installed. You can install it any time from the install icon in the address bar.')).toBeInTheDocument();
    expect(onContinue).not.toHaveBeenCalled();
    expect(localStorage.getItem('astrid:welcome-v1')).toBe('choose');
    expect(install.consume).toHaveBeenCalledOnce();
    expect(install.prompt).toBeNull();
    expect(screen.queryByRole('radiogroup', { name: 'How to open Astrid' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continue in this tab' })).toBeInTheDocument();
    expect(screen.queryByText('Astrid opened in its own window')).not.toBeInTheDocument();
  });

  it('shows the open choice only while hosted is selected and continues to local setup', () => {
    install.prompt = { prompt: vi.fn(), userChoice: Promise.resolve({ outcome: 'accepted' }) };
    const onContinue = vi.fn();
    const setRunMode = vi.fn();
    const { rerender } = render(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={onContinue} runMode="hosted" setRunMode={setRunMode} />);
    fireEvent.click(screen.getByRole('radio', { name: 'Run everything on your computer' }));
    expect(setRunMode).toHaveBeenCalledWith('local');
    rerender(<WelcomeRunMode windowMode="app-window" setWindowMode={vi.fn()} onContinue={onContinue} runMode="local" setRunMode={setRunMode} />);
    expect(screen.queryByRole('radiogroup', { name: 'How to open Astrid' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Set up with your agent' }));
    expect(onContinue).toHaveBeenCalledWith('local');
  });
});
