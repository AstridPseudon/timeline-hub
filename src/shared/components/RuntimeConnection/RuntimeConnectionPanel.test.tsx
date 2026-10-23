// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { CONNECTED_MIN_MS, LEAVE_MS, RuntimeConnectionPanel, SETTLED_QUIET_MS } from './RuntimeConnectionPanel.tsx';
import { installCommand, RUNTIME_CONNECTION_COPY as COPY } from './copy.ts';
import { CONNECTED_REALM, connectionFor } from './connectionFixture.ts';

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.restoreAllMocks();
});

const CHROME = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
const EDGE = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0';
const IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

// jsdom's own user agent names the host OS ("(darwin)" on a Mac), which reads as a phone: every case starts on desktop Chrome.
beforeEach(() => {
  vi.spyOn(window.navigator, 'userAgent', 'get').mockReturnValue(CHROME);
});

function panel(connection: RuntimeConnectionValue) {
  return render(<RuntimeConnectionPanel connection={connection} />);
}

function inEdge() {
  vi.spyOn(window.navigator, 'userAgent', 'get').mockReturnValue(EDGE);
}

function onAPhone() {
  vi.spyOn(window.navigator, 'userAgent', 'get').mockReturnValue(IPHONE);
}

function stubClipboard(writeText: (text: string) => Promise<void>) {
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
}

/** Every visible word: the panel's text content, with no hidden helper text. */
const shownText = () => document.body.textContent ?? '';

/** The card every not-connected screen shares. */
const CARD = '.rounded-\\[18px\\]';

/** What a person must never read on these screens (the agent block is the only place for these words). */
const ENGINEER_WORDS = /Runtime|workspace|realm|gateway|loopback|127\.0\.0\.1|ACP|identity|discovery|profile|process|npm run|banodoco/;

const ALL_SCREENS: ReadonlyArray<[string, () => RuntimeConnectionValue]> = [
  ['permission', () => connectionFor({ status: 'connecting' }, { awaitingConnect: true })],
  ['permission pending', () => connectionFor({ status: 'connecting' }, { awaitingConnect: true, isChecking: true })],
  ['blocked', () => connectionFor({ status: 'blocked' })],
  ['set up', () => connectionFor({ status: 'set_up' })],
  ['not running', () => connectionFor({ status: 'not_running' })],
];

describe('RuntimeConnectionPanel', () => {
  it('explains first-run local work in the existing connection card without duplicate controls', () => {
    const connect = vi.fn();
    render(<RuntimeConnectionPanel firstRun connection={connectionFor({ status: 'connecting' }, { awaitingConnect: true, connect })} />);
    expect(screen.getAllByRole('heading')).toHaveLength(1);
    expect(screen.getByRole('heading', { name: 'Connect your machine' })).toBeInTheDocument();
    expect(screen.getByText(/own GPU or connected providers/)).toBeInTheDocument();
    expect(screen.getAllByRole('button')).toHaveLength(1);
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }));
    expect(connect).toHaveBeenCalledOnce();
  });

  it.each(ALL_SCREENS)('%s: speaks of Astrid and never names a Runtime, workspace, port or command', (_name, connection) => {
    panel(connection());
    expect(shownText()).toContain('Astrid');
    expect(shownText()).not.toMatch(ENGINEER_WORDS);
    expect(shownText()).not.toMatch(/\bport\b|\borigin\b/i);
  });

  it('shows the install dialog\'s mink tile in every state, at its size, and no per-state icon', () => {
    for (const [, connection] of ALL_SCREENS) {
      const view = panel(connection());
      const avatar = view.container.querySelector('img[src="/astrid-app-icon-192.png"]');
      expect(avatar).not.toBeNull();
      expect(avatar).toHaveAttribute('alt', '');
      // 76px like .astrid-install-avatar; the file carries its own rounded tile, so nothing rounds it again.
      expect(avatar).toHaveClass('h-[76px]', 'w-[76px]');
      expect(avatar).not.toHaveClass('rounded-xl');
      // The tile is the only picture a card shows; the still editor drawn behind it is aria-hidden scenery.
      expect([...view.container.querySelectorAll('img')].filter((img) => !img.closest('[aria-hidden="true"]'))).toEqual([avatar]);
      // The only svgs are the button's own icon and (while the browser asks) the pointing arrow; none is a status icon.
      expect(view.container.querySelector('.lucide-plug, .lucide-wifi-off, .lucide-shield-alert, .lucide-triangle-alert')).toBeNull();
      cleanup();
    }
  });

  it('lays every card out like the install dialog, over the empty editor, with the waiting line along its foot', () => {
    panel(connectionFor({ status: 'not_running' }));
    const section = screen.getByTestId('runtime-not-connected');
    expect(section).toHaveClass('fixed', 'inset-0');
    // The empty editor is drawn beneath the card, inert and hidden from assistive tech.
    const frame = section.querySelector('[inert]') as HTMLElement;
    expect(frame).toHaveAttribute('aria-hidden', 'true');
    expect(frame.querySelector('header')).not.toBeNull();
    expect(frame.querySelector('main')).not.toBeNull();
    const card = section.querySelector(CARD) as HTMLElement;
    expect(card).toHaveClass('border-border', 'bg-card', 'text-center');
    expect(card.parentElement).toHaveClass('max-w-[576px]');
    expect(screen.getByRole('heading', { level: 1 })).toHaveClass('font-theme-heading', 'text-[25px]', 'text-foreground');
    expect(screen.getAllByRole('button')).toHaveLength(2);
    expect(screen.getByRole('button', { name: COPY.agent.copy })).toHaveClass('w-full');
    // The waiting line is the card's last line, not a banner above it.
    expect(card.lastElementChild).toContainElement(screen.getByText(COPY.waiting));
    expect(card.lastElementChild).toContainElement(screen.getByRole('link', { name: 'Get help' }));
  });

  describe('connecting', () => {
    it('is only the mink on the page background, with no card, heading or button', () => {
      const view = panel(connectionFor({ status: 'connecting' }, { isBooting: true }));

      expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'connecting');
      expect(screen.getByTestId('runtime-not-connected')).toHaveClass('bg-background');
      expect(view.container.querySelector('.astrid-mink-runner')).not.toBeNull();
      expect(screen.queryByRole('heading')).not.toBeInTheDocument();
      expect(screen.queryByRole('button')).not.toBeInTheDocument();
      expect(view.container.querySelector('img')).toBeNull();
      expect(view.container.querySelector(CARD)).toBeNull();
    });

    it('draws the mark at the boot screen\'s size and marks it for the boot layer to hand its stride to', () => {
      const view = panel(connectionFor({ status: 'connecting' }, { isBooting: true }));

      const mark = view.container.querySelector('.astrid-mink-runner') as HTMLElement;
      expect(mark).toHaveClass('astrid-mink-runner-boot');
      expect(mark).toHaveAttribute('data-boot-mink-continue');
      // Nothing else on the page carries the marker, and no other state does.
      expect(view.container.querySelectorAll('[data-boot-mink-continue]')).toHaveLength(1);
      cleanup();
      const other = panel(connectionFor({ status: 'not_running' }));
      expect(other.container.querySelector('[data-boot-mink-continue]')).toBeNull();
    });

    it('fades in one line under the mark after a second', () => {
      vi.useFakeTimers();
      panel(connectionFor({ status: 'connecting' }, { isBooting: true }));
      expect(screen.queryByText(COPY.connecting.sentence)).not.toBeInTheDocument();

      act(() => { vi.advanceTimersByTime(1000); });
      expect(screen.getByText(COPY.connecting.sentence)).toBeInTheDocument();
      expect(screen.getByText(COPY.connecting.sentence).closest('p')).toHaveClass('text-sm', 'text-muted-foreground');
    });

    it('shows a starting Astrid exactly as connecting', () => {
      vi.useFakeTimers();
      panel(connectionFor({ status: 'connecting' }));
      act(() => { vi.advanceTimersByTime(1000); });

      expect(screen.getByText(COPY.connecting.sentence)).toBeInTheDocument();
      expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'connecting');
      expect(screen.queryByRole('button')).not.toBeInTheDocument();
      expect(screen.queryByRole('heading')).not.toBeInTheDocument();
    });
  });

  it('permission prompt: explains first, sends nothing, and Connect is what asks', () => {
    const connect = vi.fn();
    panel(connectionFor({ status: 'connecting' }, { awaitingConnect: true, connect }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'permission');
    expect(screen.getByRole('heading', { name: 'Connect to Astrid on this computer' })).toBeInTheDocument();
    expect(screen.getByText('Chrome will ask about devices on your network. Choose Allow so this page can reach Astrid.')).toBeInTheDocument();
    // Nothing is waiting yet: Connect is what starts it.
    expect(screen.queryByText(COPY.waiting)).not.toBeInTheDocument();
    // The install path lives on the set-up state, which a first-timer reaches right after Allow.
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
    expect(screen.getAllByRole('button')).toHaveLength(1);
    expect(screen.queryByRole('button', { name: /agent/i })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Connect' }));
    expect(connect).toHaveBeenCalledOnce();
  });

  it('connect pending: tells the person to choose Allow, says where, and draws the install dialog\'s arrow outside the card, aimed top left', () => {
    const view = panel(connectionFor({ status: 'connecting' }, { awaitingConnect: true, isChecking: true }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'pending');
    expect(screen.getByRole('heading', { name: 'Choose Allow in Chrome' })).toBeInTheDocument();
    expect(screen.getByText('Chrome is asking at the top left of this window.')).toBeInTheDocument();
    expect(screen.getByText(COPY.waiting)).toBeInTheDocument();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
    expect(screen.queryByText('Connecting…')).not.toBeInTheDocument();
    expect(view.container.querySelector('svg.lucide-arrow-up')).toBeNull();
    const arrow = view.container.querySelector('svg.astrid-toolbar-pointer') as SVGElement;
    expect(arrow).not.toBeNull();
    expect(arrow).toHaveAttribute('data-corner', 'top-left');
    expect(arrow).toHaveAttribute('data-tone', 'page');
    expect(arrow).toHaveAttribute('aria-hidden', 'true');
    // It hangs off the card (its parent is the card it leaves) and says "Up here" like the dialog's.
    expect(arrow.parentElement).toBe(screen.getByTestId('runtime-not-connected').querySelector(CARD));
    expect(arrow.querySelector('text')?.textContent).toBe('UP HERE');
    expect(arrow.querySelector('path.astrid-toolbar-pointer-line')).not.toBeNull();
    expect(shownText()).not.toContain('just below the address bar');
  });

  it('names the browser the page runs in: Edge for an Edge user, on every card that names one', () => {
    inEdge();
    panel(connectionFor({ status: 'connecting' }, { awaitingConnect: true, isChecking: true }));
    expect(screen.getByRole('heading', { name: 'Choose Allow in Edge' })).toBeInTheDocument();
    expect(screen.getByText('Edge is asking at the top left of this window.')).toBeInTheDocument();
    cleanup();

    panel(connectionFor({ status: 'connecting' }, { awaitingConnect: true }));
    expect(screen.getByText('Edge will ask about devices on your network. Choose Allow so this page can reach Astrid.')).toBeInTheDocument();
    cleanup();

    panel(connectionFor({ status: 'blocked' }));
    expect(screen.getByRole('heading', { name: 'Allow Astrid in Edge' })).toBeInTheDocument();
    expect(screen.getByText('Edge is blocking this page from reaching Astrid.')).toBeInTheDocument();
    expect(shownText()).not.toContain('Chrome');
    expect(shownText()).not.toContain('{browser}');
  });

  it('browser blocked: two numbered steps in the browser, left-aligned, and the page opens by itself', () => {
    const view = panel(connectionFor({ status: 'blocked' }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'blocked');
    expect(screen.getByRole('heading', { name: 'Allow Astrid in Chrome' })).toBeInTheDocument();
    expect(screen.getByText('Chrome is blocking this page from reaching Astrid.')).toBeInTheDocument();
    const steps = screen.getAllByRole('listitem');
    // Numbered in circles as the install dialog numbers its steps.
    expect(steps.map((step) => step.querySelector('[aria-hidden="true"]')?.textContent)).toEqual(['1', '2']);
    expect(steps.map((step) => step.lastElementChild?.textContent)).toEqual([
      'Click the icon at the left of the address bar, then Site settings.',
      'Set Local network access to Allow.',
    ]);
    const list = steps[0].parentElement as HTMLElement;
    expect(list.tagName).toBe('OL');
    expect(list).toHaveClass('text-left', 'text-sm');
    // It waits along the card's foot like every screen that waits.
    const card = screen.getByTestId('runtime-not-connected').querySelector(CARD) as HTMLElement;
    expect(card.lastElementChild).toContainElement(screen.getByText('Come back here and it opens by itself.'));
    // "Local network access" is Chrome's own setting name, the one word of the product's that may appear.
    expect(shownText()).toContain('Local network access');
    expect(shownText()).not.toMatch(/chrome:\/\//);
    expect(view.container.querySelector('code')).toBeNull();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it("first visit with nothing running: shows the install line and doesn't claim Astrid isn't installed", () => {
    panel(connectionFor({ status: 'set_up' }));

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'set_up');
    expect(screen.getByRole('heading', { name: 'Connect Astrid on this computer' })).toBeInTheDocument();
    const sentence = screen.getByText('Your coding agent can set Astrid up, or reconnect the one you have.');
    expect(sentence).toHaveClass('text-sm', 'text-muted-foreground');
    expect(screen.getAllByRole('button')).toHaveLength(2);
    expect(screen.getByRole('button', { name: COPY.agent.commandCopy })).toBeInTheDocument();
    expect(screen.getByRole('code')).toHaveTextContent(installCommand('install'));
    expect(screen.getByText(COPY.waiting)).toBeInTheDocument();
    // The card says what the instructions are for; no line repeats it, and none explains how to open a terminal.
    expect(shownText()).not.toContain('Paste these instructions');
    expect(shownText()).not.toMatch(/Open Terminal|Applications → Utilities/);
    const panelText = screen.getByTestId('runtime-not-connected').textContent ?? '';
    expect(panelText).not.toContain("isn't installed");
    expect(panelText).not.toContain("isn't running");
  });

  it('uses PowerShell for setup, repair, restart and update on Windows', () => {
    inEdge();
    for (const status of ['set_up', 'not_running', 'update_needed'] as const) {
      panel(connectionFor({ status }));
      expect(screen.getByText(status === 'update_needed' ? 'If you installed Astrid with the installer, run this in PowerShell:' : 'Or run this yourself in PowerShell:')).toBeInTheDocument();
      expect(shownText()).not.toContain('Open Start');
      cleanup();
    }
  });

  const NOT_RUNNING: ReadonlyArray<[string, () => RuntimeConnectionValue]> = [
    ['nothing answers on a return visit', () => connectionFor({ status: 'not_running' })],
    ['Astrid answered but its engine stopped', () => connectionFor({ status: 'not_running' })],
  ];

  it.each(NOT_RUNNING)('not running (%s): one screen with the install line', (_name, connection) => {
    panel(connection());

    expect(screen.getByRole('heading', { name: "Astrid isn't running" })).toBeInTheDocument();
    expect(screen.getByText('Give these instructions to your coding agent to start it again. Your work is kept.')).toBeInTheDocument();
    expect(screen.getByText(COPY.waiting)).toBeInTheDocument();
    expect(screen.getAllByRole('button')).toHaveLength(2);
    expect(screen.getByRole('button', { name: COPY.agent.commandCopy })).toBeInTheDocument();
    expect(screen.getByRole('code')).toHaveTextContent(installCommand('install'));
    expect(shownText()).not.toMatch(/reload/i);
    expect(screen.queryByText('Connect Astrid on this computer')).not.toBeInTheDocument();
  });

  describe('on a phone', () => {
    const NOT_CONNECTED: ReadonlyArray<[string, () => RuntimeConnectionValue]> = [
      ...ALL_SCREENS,
    ];

    it.each(NOT_CONNECTED)('%s: the one "open Astrid on your computer" screen', (_name, connection) => {
      onAPhone();
      panel(connection());

      expect(screen.getByRole('heading', { name: 'Open Astrid on your computer' })).toBeInTheDocument();
      expect(screen.getByText('Astrid runs on a computer, so open this page there.')).toBeInTheDocument();
      expect(screen.getAllByRole('button')).toHaveLength(1);
      expect(screen.getByRole('button', { name: 'Send the link to your computer' })).toBeInTheDocument();
      expect(screen.queryByRole('button', { name: /agent/i })).not.toBeInTheDocument();
      expect(screen.queryByRole('link')).not.toBeInTheDocument();
    });

    it('connecting: the mink alone for the first second, then the same screen', () => {
      vi.useFakeTimers();
      onAPhone();
      panel(connectionFor({ status: 'connecting' }, { isBooting: true }));
      expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'connecting');
      expect(screen.queryByRole('heading')).not.toBeInTheDocument();

      act(() => { vi.advanceTimersByTime(1000); });
      expect(screen.getByRole('heading', { name: 'Open Astrid on your computer' })).toBeInTheDocument();
      expect(screen.queryByText(COPY.connecting.sentence)).not.toBeInTheDocument();
    });

    it('copies this page\'s address and then reads "Link copied" with a check', async () => {
      const previousUrl = window.location.href;
      window.history.replaceState({}, '', '/tools/video-editor?timeline=timeline-7#frame-42');
      onAPhone();
      const writeText = vi.fn(async (_text: string) => undefined);
      Object.defineProperty(navigator, 'share', { configurable: true, value: undefined });
      stubClipboard(writeText);
      panel(connectionFor({ status: 'blocked' }));

      fireEvent.click(screen.getByRole('button', { name: 'Send the link to your computer' }));
      await waitFor(() => expect(screen.getByRole('button', { name: 'Link copied' })).toBeInTheDocument());
      expect(writeText).toHaveBeenCalledWith(`${window.location.origin}/tools/video-editor?timeline=timeline-7#frame-42`);
      expect(screen.getByRole('button', { name: 'Link copied' }).querySelector('svg.lucide-check')).not.toBeNull();
      const previous = new URL(previousUrl);
      window.history.replaceState({}, '', `${previous.pathname}${previous.search}${previous.hash}`);
    });
  });

  it('renders nothing once connected: the gate shows the app', () => {
    const { container } = panel(connectionFor({ status: 'connected', realm: CONNECTED_REALM }));
    expect(container).toBeEmptyDOMElement();
  });

  describe('command copying', () => {
    it.each([
      ['set_up', () => connectionFor({ status: 'set_up' }), 'install'],
      ['not_running', () => connectionFor({ status: 'not_running' }), 'install'],
      ['update_needed', () => connectionFor({ status: 'update_needed' }), 'update'],
    ] as const)('%s shows and copies its command', async (_name, connection, mode) => {
      const writeText = vi.fn(async (_text: string) => undefined);
      stubClipboard(writeText);
      panel(connection());
      const command = mode === 'update' ? installCommand('update') : installCommand('install');
      expect(screen.getByRole('code')).toHaveTextContent(command);
      fireEvent.click(screen.getByRole('button', { name: COPY.agent.commandCopy }));
      await waitFor(() => expect(writeText).toHaveBeenCalledWith(command));
    });

    it.each(['set_up', 'not_running', 'update_needed'] as const)('%s prioritizes the complete agent brief and keeps command copying independent', async (status) => {
      const writeText = vi.fn(async (_text: string) => undefined);
      stubClipboard(writeText);
      panel(connectionFor({ status }));
      const primary = screen.getByRole('button', { name: 'Copy agent instructions' });
      const commandCopy = screen.getByRole('button', { name: 'Copy command' });
      expect(screen.getAllByRole('button')[0]).toBe(primary);
      expect(commandCopy.parentElement).toContainElement(screen.getByRole('code'));
      fireEvent.click(primary);
      await waitFor(() => expect(writeText).toHaveBeenCalledOnce());
      const brief = writeText.mock.calls[0][0];
      expect(brief).toContain(window.location.origin);
      expect(brief).toContain('selected workspace and data root');
      expect(brief).toContain('The installer adopts an existing workspace itself');
      expect(brief).toContain('read the log path printed by the installer');
      expect(brief).toContain('Tell me to choose Allow if Chrome or Edge asks');
      expect(brief).toContain('docs/setup/SKILL.md');
      const command = installCommand(status === 'update_needed' ? 'update' : 'install');
      expect(brief).toContain(command);
      expect(brief).not.toBe(command);
      expect(screen.getByRole('button', { name: 'Copy command' })).toBeInTheDocument();
      fireEvent.click(commandCopy);
      await waitFor(() => expect(writeText).toHaveBeenLastCalledWith(command));
      expect(screen.getByRole('button', { name: 'Command copied' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: COPY.agent.copied })).toBeInTheDocument();
    });

    it('keeps the full agent brief selectable when copying it fails', async () => {
      stubClipboard(vi.fn(async () => { throw new Error('Clipboard denied'); }));
      panel(connectionFor({ status: 'not_running' }));
      fireEvent.click(screen.getByRole('button', { name: 'Copy agent instructions' }));
      const field = await screen.findByRole('textbox', { name: COPY.agent.copyFailed }) as HTMLTextAreaElement;
      expect(field.value).toContain('selected workspace and data root');
      expect(field.value).toContain('read the log path printed by the installer');
      expect(field.selectionEnd).toBe(field.value.length);
      expect(screen.getByRole('button', { name: 'Copy command' })).toBeInTheDocument();
    });

    it('shows the command in a selectable box if clipboard writing fails', async () => {
      stubClipboard(vi.fn(async () => { throw new Error('Clipboard denied'); }));
      panel(connectionFor({ status: 'not_running' }));
      fireEvent.click(screen.getByRole('button', { name: COPY.agent.commandCopy }));
      expect(await screen.findByText(COPY.agent.copyFailed)).toHaveAttribute('role', 'status');
      const field = screen.getByRole('textbox') as HTMLTextAreaElement;
      expect(field.value).toBe(installCommand('install'));
      expect(field.selectionEnd).toBe(field.value.length);
    });
  });

  describe('on the way out (Astrid answered after this screen asked)', () => {
    afterEach(() => document.querySelectorAll('[data-boot-hold]').forEach((node) => node.remove()));

    it('turns the waiting line into "Connected to Astrid" in place, keeps the card, and leaves once the editor beneath has settled', async () => {
      vi.useFakeTimers();
      const left = vi.fn();
      // The editor mounting beneath holds the boot while its workspace and timeline answer (bootLayer.ts).
      const hold = document.createElement('span');
      hold.setAttribute('data-boot-hold', '');
      document.body.append(hold);
      render(<RuntimeConnectionPanel connection={connectionFor({ status: 'set_up' })} exit={{ left }} />);
      const section = screen.getByTestId('runtime-not-connected');
      const card = section.querySelector(CARD) as HTMLElement;

      expect(within(card.lastElementChild as HTMLElement).getByRole('status')).toHaveTextContent(COPY.connected.sentence);
      expect(screen.queryByText(COPY.waiting)).not.toBeInTheDocument();
      expect(screen.getByRole('heading', { name: 'Connect Astrid on this computer' })).toBeInTheDocument();

      act(() => { vi.advanceTimersByTime(CONNECTED_MIN_MS + LEAVE_MS); });
      expect(section).not.toHaveAttribute('data-leaving');
      expect(left).not.toHaveBeenCalled();

      await act(async () => { hold.remove(); await Promise.resolve(); });
      // A hold that comes back within the quiet moment (the editor handing over to its timeline) starts the wait again.
      act(() => { vi.advanceTimersByTime(SETTLED_QUIET_MS - 1); });
      await act(async () => { document.body.append(hold); await Promise.resolve(); });
      act(() => { vi.advanceTimersByTime(SETTLED_QUIET_MS); });
      expect(section).not.toHaveAttribute('data-leaving');
      await act(async () => { hold.remove(); await Promise.resolve(); });
      act(() => { vi.advanceTimersByTime(SETTLED_QUIET_MS); });
      expect(section).toHaveAttribute('data-leaving');
      expect(left).not.toHaveBeenCalled();
      act(() => { vi.advanceTimersByTime(LEAVE_MS); });
      expect(left).toHaveBeenCalledOnce();
    });

    it('shows "Connected" for its moment even when the editor is already there', () => {
      vi.useFakeTimers();
      const left = vi.fn();
      render(<RuntimeConnectionPanel connection={connectionFor({ status: 'not_running' })} exit={{ left }} />);
      const section = screen.getByTestId('runtime-not-connected');
      act(() => { vi.advanceTimersByTime(CONNECTED_MIN_MS + SETTLED_QUIET_MS - 1); });
      expect(section).not.toHaveAttribute('data-leaving');
      act(() => { vi.advanceTimersByTime(1); });
      expect(section).toHaveAttribute('data-leaving');
      act(() => { vi.advanceTimersByTime(LEAVE_MS); });
      expect(left).toHaveBeenCalledOnce();
    });

    it('from the connecting screen, which asked nothing: no "Connected" moment, the mark stays until the editor has settled', async () => {
      vi.useFakeTimers();
      const left = vi.fn();
      const hold = document.createElement('span');
      hold.setAttribute('data-boot-hold', '');
      document.body.append(hold);
      render(<RuntimeConnectionPanel connection={connectionFor({ status: 'connecting' }, { isBooting: true })} exit={{ left }} />);
      const section = screen.getByTestId('runtime-not-connected');
      expect(section).toHaveAttribute('data-state', 'connecting');
      expect(screen.queryByText(COPY.connected.sentence)).not.toBeInTheDocument();
      act(() => { vi.advanceTimersByTime(CONNECTED_MIN_MS); });
      expect(section).not.toHaveAttribute('data-leaving');

      await act(async () => { hold.remove(); await Promise.resolve(); });
      act(() => { vi.advanceTimersByTime(SETTLED_QUIET_MS); });
      expect(section).toHaveAttribute('data-leaving');
      act(() => { vi.advanceTimersByTime(LEAVE_MS); });
      expect(left).toHaveBeenCalledOnce();
    });
  });
});
