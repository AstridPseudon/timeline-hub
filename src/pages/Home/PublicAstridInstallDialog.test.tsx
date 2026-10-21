// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useState } from 'react';
import {
  __resetInstallPromptSignalsForTests,
  useInstallPromptSignals,
} from '@/shared/hooks/platformInstall/signals';
import { PublicAstridInstallDialog } from './PublicAstridInstallDialog';

const originalUserAgent = Object.getOwnPropertyDescriptor(navigator, 'userAgent');
const originalPlatform = Object.getOwnPropertyDescriptor(navigator, 'platform');
const originalClipboard = Object.getOwnPropertyDescriptor(navigator, 'clipboard');
const originalShare = Object.getOwnPropertyDescriptor(navigator, 'share');

function setNavigator(userAgent: string, platform: string) {
  Object.defineProperty(navigator, 'userAgent', { value: userAgent, configurable: true });
  Object.defineProperty(navigator, 'platform', { value: platform, configurable: true });
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((res) => { resolve = res; });
  return { promise, resolve };
}

function promptEvent(userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>) {
  return Object.assign(new Event('beforeinstallprompt', { cancelable: true }), {
    prompt: vi.fn().mockResolvedValue(undefined),
    userChoice,
  });
}

const BROWSER = { name: 'Use it in the browser' };

function openDialog() {
  fireEvent.click(screen.getByRole('button', { name: 'Open install' }));
}

function openComputerStep() {
  openDialog();
  fireEvent.click(screen.getByRole('button', BROWSER));
}

function Harness() {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)}>Open install</button>
      <PublicAstridInstallDialog open={open} onClose={() => setOpen(false)} />
    </>
  );
}

describe('PublicAstridInstallDialog', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    __resetInstallPromptSignalsForTests();
    setNavigator(
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
      'MacIntel',
    );
    Object.defineProperty(navigator, 'clipboard', {
      value: { writeText: vi.fn().mockResolvedValue(undefined) }, configurable: true,
    });
    Object.defineProperty(navigator, 'share', { value: undefined, configurable: true });
    window.matchMedia = vi.fn().mockImplementation((media: string) => ({
      media,
      matches: false,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
    }));
    Object.defineProperty(HTMLDialogElement.prototype, 'showModal', {
      configurable: true,
      value: vi.fn(function (this: HTMLDialogElement) { this.open = true; }),
    });
    Object.defineProperty(HTMLDialogElement.prototype, 'close', {
      configurable: true,
      value: vi.fn(function (this: HTMLDialogElement) { this.open = false; }),
    });
  });

  afterEach(() => {
    cleanup();
    __resetInstallPromptSignalsForTests();
    vi.restoreAllMocks();
    if (originalUserAgent) Object.defineProperty(navigator, 'userAgent', originalUserAgent);
    if (originalPlatform) Object.defineProperty(navigator, 'platform', originalPlatform);
    if (originalClipboard) Object.defineProperty(navigator, 'clipboard', originalClipboard);
    else delete (navigator as Navigator & { clipboard?: Clipboard }).clipboard;
    if (originalShare) Object.defineProperty(navigator, 'share', originalShare);
    else delete (navigator as Navigator & { share?: Navigator['share'] }).share;
    vi.useRealTimers();
  });

  it('returns focus to the Home CTA and closes safely', () => {
    render(<Harness />);
    const trigger = screen.getByRole('button', { name: 'Open install' });
    trigger.focus();
    fireEvent.click(trigger);
    expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal', 'true');
    expect(screen.getByRole('button', { name: 'Close' })).toHaveFocus();
    fireEvent.click(screen.getByRole('button', { name: 'Close' }));
    expect(document.querySelector('dialog')).not.toHaveAttribute('open');
    expect(trigger).toHaveFocus();
  });

  it('names how to open the matching shell on Windows', () => {
    setNavigator(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36',
      'Win32',
    );
    render(<Harness />);
    openComputerStep();

    expect(screen.getByText('Or run this command yourself in PowerShell:')).toBeInTheDocument();
  });

  it.each([
    ['chromium', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36', 'MacIntel', 'Astrid installs straight from your browser'],
    ['safari', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15', 'MacIntel', 'Astrid installs straight from Safari'],
    ['mobile', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1', 'iPhone', 'Open this page there to copy the line'],
  ] as const)('renders the %s install variant', (scenario, userAgent, platform, copy) => {
    setNavigator(userAgent, platform);
    render(<Harness />);
    screen.getByRole('button', { name: 'Open install' }).focus();
    fireEvent.click(screen.getByRole('button', { name: 'Open install' }));
    expect(screen.getByRole('dialog')).toHaveAttribute('data-scenario', scenario);
    // Step 1 first: the app, with the platform's install instructions (no prompt in jsdom).
    expect(screen.getByRole('heading', { name: 'Get the Astrid app' })).toBeInTheDocument();
    if (scenario === 'mobile') expect(screen.getByText('Choose Add to Home Screen.')).toBeInTheDocument();
    else expect(screen.getByText(new RegExp(copy))).toBeInTheDocument();
    if (scenario === 'safari') expect(screen.getByText('Choose Add to Dock.')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', BROWSER));
    expect(screen.getByRole('heading', { name: 'Connect your computer' })).toBeInTheDocument();
    if (scenario === 'mobile') expect(screen.getByText(/Open this page there to copy the line/)).toBeInTheDocument();
    else {
      expect(screen.getByText('Give these instructions to your coding agent to set up Astrid on your computer.')).toBeInTheDocument();
      expect(screen.getByText(/https:\/\/astrid\.haus\/install/)).toBeInTheDocument();
    }
  });

  it('shows the browser arrow on the app step only, and not once a prompt can be used', () => {
    render(<Harness />);
    openDialog();
    expect(document.querySelector('svg.astrid-toolbar-pointer')).not.toBeNull();
    fireEvent.click(screen.getByRole('button', BROWSER));
    expect(document.querySelector('svg.astrid-toolbar-pointer')).toBeNull();
  });

  it('shows the app step first, with the browser choice beside it and no old shortcut details', () => {
    render(<Harness />);
    openDialog();
    expect(screen.getByRole('heading', { name: 'Get the Astrid app' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Done — continue' })).toBeInTheDocument();
    expect(screen.getByRole('button', BROWSER)).toBeInTheDocument();
    expect(screen.queryByText('Add a browser shortcut')).not.toBeInTheDocument();
    expect(document.querySelector('details')).toBeNull();
    expect(screen.queryByText(/curl -fsSL/)).not.toBeInTheDocument();
  });

  it('offers Install when the browser can prompt, and an accepted prompt moves to the computer step', async () => {
    vi.useRealTimers();
    const event = promptEvent(Promise.resolve({ outcome: 'accepted' }));
    act(() => window.dispatchEvent(event));
    render(<Harness />);
    openDialog();
    expect(screen.queryByRole('button', { name: 'Done — continue' })).not.toBeInTheDocument();
    window.localStorage.clear();
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: /Install Astrid/ })); });
    await act(async () => { await Promise.resolve(); await Promise.resolve(); });
    expect(event.prompt).toHaveBeenCalledTimes(1);
    expect(screen.getByRole('heading', { name: 'Connect your computer' })).toBeInTheDocument();
    expect(window.localStorage.getItem('astrid:prefers-app')).toBe('1');
  });

  it('stays on the app step when the prompt is dismissed', async () => {
    vi.useRealTimers();
    const event = promptEvent(Promise.resolve({ outcome: 'dismissed' }));
    act(() => window.dispatchEvent(event));
    render(<Harness />);
    openDialog();
    await act(async () => { fireEvent.click(screen.getByRole('button', { name: /Install Astrid/ })); });
    await act(async () => { await Promise.resolve(); await Promise.resolve(); });
    expect(screen.getByRole('heading', { name: 'Get the Astrid app' })).toBeInTheDocument();
  });

  it('"Use it in the browser" records the choice, moves to step 2 and does not navigate; Back returns', () => {
    window.localStorage.clear();
    const assign = vi.fn();
    vi.spyOn(window, 'location', 'get').mockReturnValue({ ...window.location, assign } as unknown as Location);
    render(<Harness />);
    openDialog();
    expect(window.localStorage.getItem('astrid:prefers-app')).toBeNull();
    fireEvent.click(screen.getByRole('button', BROWSER));
    expect(window.localStorage.getItem('astrid:prefers-app')).toBe('1');
    expect(assign).not.toHaveBeenCalled();
    expect(screen.getByRole('heading', { name: 'Connect your computer' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: '← Back' }));
    expect(screen.getByRole('heading', { name: 'Get the Astrid app' })).toBeInTheDocument();
  });

  it('skips the app step when running as a standalone app', () => {
    window.matchMedia = vi.fn().mockImplementation((media: string) => ({
      media, matches: media.includes('standalone'), addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn(),
    }));
    render(<Harness />);
    openDialog();
    expect(screen.getByRole('heading', { name: 'Connect your computer' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '← Back' })).not.toBeInTheDocument();
  });

  it('renders the installed variant without an install prompt action', () => {
    act(() => window.dispatchEvent(new Event('appinstalled')));
    render(<Harness />);
    screen.getByRole('button', { name: 'Open install' }).focus();
    openDialog();
    // Installed already: straight to the computer step.
    expect(screen.getByRole('heading', { name: 'Connect your computer' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Install Astrid/ })).not.toBeInTheDocument();
  });

  it.each([
    ['not installed', 'Already set up? Open Astrid', false],
    ['installed', 'Open Astrid in this tab', true],
  ] as const)('%s: choosing the browser already says "take me in", so the app is told to go straight to Chrome\'s prompt', (_name, label, installed) => {
    window.sessionStorage.clear();
    if (installed) act(() => window.dispatchEvent(new Event('appinstalled')));
    // jsdom cannot navigate; the click only needs to leave the one-shot flag behind.
    vi.spyOn(console, 'error').mockImplementation(() => {});
    render(<Harness />);
    screen.getByRole('button', { name: 'Open install' }).focus();
    openDialog();
    if (!installed) fireEvent.click(screen.getByRole('button', BROWSER));
    expect(window.sessionStorage.getItem('astrid.runtime.autoConnect')).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: label }));
    expect(window.sessionStorage.getItem('astrid.runtime.autoConnect')).toBe('1');
  });

  it('still goes in when session storage refuses the flag', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('blocked'); });
    render(<Harness />);
    screen.getByRole('button', { name: 'Open install' }).focus();
    openComputerStep();
    expect(() => fireEvent.click(screen.getByRole('button', { name: 'Already set up? Open Astrid' }))).not.toThrow();
  });

  it('does not consume a prompt whose result arrives after modal departure', async () => {
    const choice = deferred<{ outcome: 'accepted' | 'dismissed' }>();
    const event = promptEvent(choice.promise);
    act(() => window.dispatchEvent(event));
    render(<Harness />);
    openDialog();
    fireEvent.click(screen.getByRole('button', { name: /Install Astrid/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Close' }));
    choice.resolve({ outcome: 'accepted' });
    await act(async () => { await Promise.resolve(); await Promise.resolve(); });

    const observer = render(<PromptObserver />);
    expect(observer.container).toHaveTextContent('present');
  });

  it('ignores a late clipboard result after mobile modal close and bounds feedback', async () => {
    setNavigator(
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
      'iPhone',
    );
    const write = deferred<void>();
    Object.defineProperty(navigator, 'clipboard', { value: { writeText: vi.fn(() => write.promise) }, configurable: true });
    render(<Harness />);
    screen.getByRole('button', { name: 'Open install' }).focus();
    openComputerStep();
    fireEvent.click(screen.getByRole('button', { name: 'Send the link to your computer' }));
    fireEvent.click(screen.getByRole('button', { name: 'Not now' }));
    write.resolve();
    await act(async () => { await Promise.resolve(); });
    expect(screen.queryByText('Link copied')).not.toBeInTheDocument();
    await act(async () => { await vi.advanceTimersByTimeAsync(2_000); });
    expect(screen.getByRole('button', { name: 'Open install' })).toHaveFocus();
  });

  it('does not apply a late share result after close', async () => {
    setNavigator(
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
      'iPhone',
    );
    const sharing = deferred<void>();
    const share = vi.fn(() => sharing.promise);
    Object.defineProperty(navigator, 'share', { value: share, configurable: true });
    render(<Harness />);
    openComputerStep();
    fireEvent.click(screen.getByRole('button', { name: 'Send the link to your computer' }));
    fireEvent.click(screen.getByRole('button', { name: 'Not now' }));
    sharing.resolve();
    await act(async () => { await Promise.resolve(); });
    expect(share).toHaveBeenCalledTimes(1);
    expect(screen.queryByText('Link copied')).not.toBeInTheDocument();
  });
});

function PromptObserver() {
  const { deferredPrompt } = useInstallPromptSignals();
  return <span>{deferredPrompt ? 'present' : 'consumed'}</span>;
}
