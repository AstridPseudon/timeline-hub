import { createContext, useContext, useEffect, useLayoutEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { Check, Link2 } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { MinkRunner } from '@/shared/components/MinkRunner/MinkRunner.tsx';
import { ToolbarPointer } from '@/shared/components/ToolbarPointer/ToolbarPointer.tsx';
import type { RuntimeConnectionPanelExit, RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { ASTRID_HELP_URL } from '@/integrations/astrid/help.ts';
import { isMobileDevice } from '@/pages/Home/installScenario.ts';
import { useSendLinkToComputer } from '@/pages/Home/useSendLinkToComputer.ts';
import { CopyInstallCommand } from './CopyInstallCommand.tsx';
import { EmptyEditorShell } from './EmptyEditorShell.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, withBrowser } from './copy.ts';

export interface RuntimeConnectionPanelProps {
  /** The gate's value: the screen to show (on the way out, the last one shown). */
  readonly connection: RuntimeConnectionValue;
  readonly firstRun?: boolean;
  /** Set once Astrid has connected after this panel asked for something: it shows so, then leaves (see the gate). */
  readonly exit?: RuntimeConnectionPanelExit | null;
}

/** How long the mark is alone on the screen before the line under it fades in. */
const CONNECTING_LINE_DELAY_MS = 1000;
/** The shortest time "Connected to Astrid" is up, so it is read; the panel then waits for the editor to settle. */
export const CONNECTED_MIN_MS = 900;
/**
 * How long nothing may hold the boot before the editor counts as settled: the editor hands its hold from the
 * workspace to the timeline across a render or two, and the panel must not leave in that gap.
 */
export const SETTLED_QUIET_MS = 150;
/** The panel's way out: the card lifts away and the empty editor cross-fades into the real one. */
export const LEAVE_MS = 500;

/** The same face the landing page, the install dialog and the header show: the pixel mink's app icon. */
const AVATAR_SRC = '/astrid-app-icon-192.png';

/** The editor beneath has painted its frame: nothing in the page holds the boot (`bootLayer.ts`'s ready signal). */
function appSettled(): boolean {
  return document.querySelector('[data-boot-hold]') === null;
}

function prefersReducedMotion(): boolean {
  return typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * On the way out: true once `holdMs` has passed (the "Connected" moment, on a screen that asked for something) and the
 * editor beneath has settled, then `exit.left` after the leaving motion.
 */
function useLeaving(exit: RuntimeConnectionPanelExit | null, holdMs: number): boolean {
  const [leaving, setLeaving] = useState(false);
  useEffect(() => {
    if (!exit) {
      setLeaving(false);
      return undefined;
    }
    let observer: MutationObserver | null = null;
    let quietTimer: number | undefined;
    let leftTimer: number | undefined;
    const leave = () => {
      observer?.disconnect();
      setLeaving(true);
      leftTimer = window.setTimeout(exit.left, prefersReducedMotion() ? 0 : LEAVE_MS);
    };
    // Settled once nothing has held the boot for a quiet moment; a hold that comes back starts the wait again.
    const check = () => {
      window.clearTimeout(quietTimer);
      if (appSettled()) quietTimer = window.setTimeout(() => { if (appSettled()) leave(); }, SETTLED_QUIET_MS);
    };
    const holdTimer = window.setTimeout(() => {
      observer = new MutationObserver(check);
      observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['data-boot-hold'] });
      check();
    }, holdMs);
    return () => {
      window.clearTimeout(holdTimer);
      window.clearTimeout(quietTimer);
      window.clearTimeout(leftTimer);
      observer?.disconnect();
    };
  }, [exit, holdMs]);
  return leaving;
}

/** What the card's status line shows: Astrid answered (the panel is on its way out). */
const ConnectedContext = createContext(false);

/**
 * The layer every not-connected card sits on: the empty editor under a light veil, with the card in the middle. It
 * stays mounted while the screen changes (set up, Allow, blocked), so only the card changes. On the way out, the card
 * lifts away and the layer fades, revealing the real editor that has mounted beneath it in the same places.
 */
function GateLayer({ dataState, exit, children }: { dataState: string; exit: RuntimeConnectionPanelExit | null; children: ReactNode }) {
  const leaving = useLeaving(exit, CONNECTED_MIN_MS);
  return (
    <section
      aria-label={COPY.panelLabel}
      data-testid="runtime-not-connected"
      data-state={dataState}
      data-leaving={leaving ? '' : undefined}
      // Over the app's own panes (the chat pane sits at z 100016) while the app mounts beneath it.
      className={cn('fixed inset-0 z-[100100] overflow-y-auto text-foreground', leaving && 'pointer-events-none')}
    >
      {/* Fades in over the boot screen's paper; fades out over the real editor. */}
      <div className={cn('fixed inset-0 transition-opacity duration-500 ease-out animate-in fade-in-0 motion-reduce:animate-none motion-reduce:transition-none', leaving && 'opacity-0')}>
        <EmptyEditorShell />
        <div aria-hidden="true" className="absolute inset-0 bg-foreground/[0.07] backdrop-blur-[2px]" />
      </div>
      <div className="relative flex min-h-full items-center justify-center p-4">
        <div
          key={dataState}
          className={cn(
            // Opacity only on the way in: the "Up here" arrow is fixed to the viewport, so nothing above it may transform.
            'w-full max-w-[576px] transition-[opacity,transform] duration-300 ease-out animate-in fade-in-0 motion-reduce:transition-none motion-reduce:animate-none',
            leaving && '-translate-y-1 opacity-0',
          )}
        >
          <ConnectedContext.Provider value={Boolean(exit)}>{children}</ConnectedContext.Provider>
        </div>
      </div>
    </section>
  );
}

/**
 * The card's quiet last line, along its foot: what the page is waiting for, with a live dot. When Astrid answers it
 * becomes the check and "Connected to Astrid", in the same place, before the card leaves.
 */
function StatusLine({ text, help }: { text: string; help: boolean }) {
  const connected = useContext(ConnectedContext);
  // The words after the mark keep the width they had while waiting, so the mark stays where it was as it turns into
  // the check and only the words change.
  const wordsRef = useRef<HTMLSpanElement>(null);
  const waitingWidth = useRef<number | null>(null);
  useLayoutEffect(() => {
    if (!connected && wordsRef.current) waitingWidth.current = wordsRef.current.getBoundingClientRect().width;
  });
  return (
    <div className="flex min-h-12 items-center justify-center gap-2 border-t border-border/70 bg-muted/40 px-[22px] py-3 text-[13px] text-muted-foreground">
      <span aria-hidden="true" className="relative flex h-4 w-4 shrink-0 items-center justify-center">
        <span className={cn('absolute h-2 w-2 rounded-full bg-primary transition-opacity duration-200', connected ? 'opacity-0' : 'animate-pulse')} />
        <span className={cn('absolute flex h-4 w-4 items-center justify-center rounded-full bg-primary text-primary-foreground transition-[opacity,transform] duration-300 ease-out', connected ? 'scale-100 opacity-100' : 'scale-50 opacity-0')}>
          <Check className="h-2.5 w-2.5" strokeWidth={3.5} />
        </span>
      </span>
      <span ref={wordsRef} className="flex min-w-0 items-center gap-2" style={connected && waitingWidth.current ? { minWidth: waitingWidth.current } : undefined}>
        <p role="status" className={cn('min-w-0 text-pretty', connected && 'text-foreground')}>
          <span key={connected ? 'connected' : 'waiting'} className={connected ? 'animate-in fade-in-0 duration-300' : undefined}>{connected ? COPY.connected.sentence : text}</span>
        </p>
        {help && !connected && (
          <>
            <span aria-hidden="true">·</span>
            <a className="shrink-0 underline underline-offset-4 hover:text-foreground" href={ASTRID_HELP_URL} target="_blank" rel="noreferrer">Get help</a>
          </>
        )}
      </span>
    </div>
  );
}

interface CardProps {
  readonly title: string;
  readonly sentence: string;
  /** The state's one primary action. */
  readonly action?: ReactNode;
  /** Content between the sentence and the action (the blocked state's steps). */
  readonly children?: ReactNode;
  /** The status line along the card's foot: the screen waits for something done elsewhere, then opens by itself. */
  readonly status?: string;
  /** Help in the status line, for a connection that needs attention. */
  readonly showHelp?: boolean;
  /** The word on a hand-drawn arrow, outside the card, aimed at the top left of the window: the browser's prompt is there. */
  readonly pointer?: string;
}

/**
 * The one card every not-connected screen shares, in the install dialog's style (same width, radius, header and
 * button): the app icon, a serif heading, one short sentence, at most one primary action, and the status line.
 */
function Card({ title, sentence, action, children, status, pointer, showHelp = false }: CardProps) {
  const connected = useContext(ConnectedContext);
  return (
    <div className="relative overflow-hidden rounded-[18px] border border-border bg-card text-center shadow-[0_24px_60px_-24px_rgb(37_36_31/0.45),0_2px_8px_rgb(37_36_31/0.08)]">
      <div className="space-y-4 p-[22px] pt-[26px]">
        <header className="grid justify-items-center gap-3">
          {/* The icon file carries its own rounded tile and shadow, as the install dialog shows it at this size. */}
          <img src={AVATAR_SRC} alt="" className="-mb-1.5 h-[76px] w-[76px]" />
          <div className="space-y-1">
            <h1 className="text-balance font-serif font-theme-heading text-[25px] font-normal leading-tight text-foreground">{title}</h1>
            <p className="text-balance text-sm leading-6 text-muted-foreground">{sentence}</p>
          </div>
        </header>
        {children}
        {action}
      </div>
      {(status || connected) && <StatusLine text={status ?? COPY.waiting} help={showHelp} />}
      {pointer && !connected && <ToolbarPointer label={pointer} corner="top-left" tone="page" />}
    </div>
  );
}

/**
 * The mark alone on the page background, as the boot screen shows it; the line fades in only if the wait is not short.
 * When Astrid answers it stays, as the boot screen would, until the editor beneath has settled, then fades into it:
 * nothing was asked of the person, so there is no "Connected" moment.
 */
function ConnectingPanel({ phone, exit }: { phone: boolean; exit: RuntimeConnectionPanelExit | null }) {
  const [lineShown, setLineShown] = useState(false);
  const leaving = useLeaving(exit, 0);
  useEffect(() => {
    const timer = window.setTimeout(() => setLineShown(true), CONNECTING_LINE_DELAY_MS);
    return () => window.clearTimeout(timer);
  }, []);
  // A phone never reaches Astrid, so once the wait is long enough to see, it gets the phone screen instead.
  if (lineShown && phone) return <GateLayer dataState="phone" exit={exit}><PhoneCard /></GateLayer>;
  return (
    <section
      aria-label={COPY.panelLabel}
      data-testid="runtime-not-connected"
      data-state="connecting"
      data-leaving={leaving ? '' : undefined}
      className={cn(
        'fixed inset-0 z-[100100] flex flex-col items-center justify-center gap-4 bg-background p-4 text-foreground transition-opacity duration-500 ease-out motion-reduce:transition-none',
        leaving && 'pointer-events-none opacity-0',
      )}
    >
      {/* As tall as the line below, so the mark sits at the exact centre of the page: where the boot screen drew it. */}
      <div aria-hidden="true" className="min-h-5" />
      {/* The boot screen's mink, same size and place: the boot layer hands its stride over to this one (bootLayer.ts). */}
      <MinkRunner bootSize className="text-foreground" />
      {/* Always occupies its line, so the mark does not move when the words arrive. */}
      <p className="min-h-5 text-center text-sm text-muted-foreground">
        {lineShown && <span className="animate-in fade-in duration-500">{COPY.connecting.sentence}</span>}
      </p>
    </section>
  );
}

/** A phone: Astrid runs on a computer, so the only useful thing is to send this page there. */
function PhoneCard() {
  const { phone } = COPY;
  const { copied, send } = useSendLinkToComputer(() => window.location.href);
  return (
    <Card
      title={phone.title}
      sentence={phone.sentence}
      action={(
        <Button type="button" className="h-11 w-full justify-between rounded-xl px-4" onClick={() => void send()}>
          <span>{copied ? phone.copied : phone.button}</span>
          {copied ? <Check aria-hidden="true" className="h-4 w-4" /> : <Link2 aria-hidden="true" className="h-4 w-4" />}
        </Button>
      )}
    />
  );
}

/** The browser's local-network prompt has not been asked: nothing was sent, and Connect is what asks. */
function PermissionCard({ connection, firstRun = false }: { connection: RuntimeConnectionValue; firstRun?: boolean }) {
  const { permission } = COPY;
  if (connection.isChecking) {
    // The browser's prompt is open: nothing to press, only where to look.
    return (
      <Card
        title={withBrowser(permission.pending.title)}
        sentence={withBrowser(permission.pending.sentence)}
        pointer={permission.pending.pointer}
        status={COPY.waiting}
      />
    );
  }
  return (
    <Card
      title={firstRun ? COPY.firstRun.title : withBrowser(permission.title)}
      sentence={firstRun ? COPY.firstRun.sentence : withBrowser(permission.sentence)}
      action={<Button type="button" className="h-11 w-full rounded-xl" onClick={() => connection.connect()}>{permission.connect}</Button>}
    />
  );
}

/** Permission `denied`: the browser stopped the request, so the fix is in its site settings. */
function BlockedCard() {
  const blocked = COPY.blocked;
  return (
    // No agent button: the fix is a browser site setting, which an agent cannot change.
    <Card title={withBrowser(blocked.title)} sentence={withBrowser(blocked.sentence)} status={blocked.footer}>
      {/* Numbered as the install dialog numbers its steps. */}
      <ol className="space-y-2 text-left text-sm leading-6 text-foreground">
        {blocked.steps.map((step, index) => (
          <li key={step} className="flex gap-2.5">
            <span aria-hidden="true" className="mt-0.5 flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full bg-primary/15 text-xs font-semibold text-primary">{index + 1}</span>
            <span className="text-pretty">{step}</span>
          </li>
        ))}
      </ol>
    </Card>
  );
}

/**
 * Nothing answers and this browser has never connected. That is also what a set-up computer looks like from a new
 * browser or a private window, so the screen uses the same idempotent install line.
 */
function SetUpCard({ firstRun = false }: { firstRun?: boolean }) {
  const { setUp } = COPY;
  return <Card title={firstRun ? COPY.firstRun.title : setUp.title} sentence={firstRun ? COPY.firstRun.sentence : setUp.sentence} action={<CopyInstallCommand mode="install" />} status={COPY.waiting} />;
}

/** Nothing answers on a return visit, or the gateway answered but Astrid is not ready: a person does the same for each. */
function NotRunningCard() {
  const { notRunning } = COPY;
  return <Card title={notRunning.title} sentence={notRunning.sentence} action={<CopyInstallCommand mode="install" />} status={COPY.waiting} showHelp />;
}

function UpdateNeededCard() {
  const { updateNeeded } = COPY;
  return <Card title={updateNeeded.title} sentence={updateNeeded.sentence} action={<CopyInstallCommand mode="update" />} status={COPY.waiting} showHelp />;
}

/** Chrome's prompt is next. Setup stays in front of it unless a prior connection or the installer's handoff asked to go in. */
function awaitingConnect({ awaitingConnect: awaiting, state, isChecking }: RuntimeConnectionValue): boolean {
  return awaiting && (state.status !== 'set_up' || isChecking);
}

/** The screen for a connection: its name (the journey and Layout tests read it) and its card. */
function screenFor(connection: RuntimeConnectionValue, phone: boolean, firstRun: boolean): { name: string; card: ReactNode } | null {
  const { state } = connection;
  if (phone) return { name: 'phone', card: <PhoneCard /> };
  if (awaitingConnect(connection)) {
    return { name: connection.isChecking ? 'pending' : 'permission', card: <PermissionCard connection={connection} firstRun={firstRun} /> };
  }
  switch (state.status) {
    case 'set_up': return { name: 'set_up', card: <SetUpCard firstRun={firstRun} /> };
    case 'not_running': return { name: 'not_running', card: <NotRunningCard /> };
    case 'blocked': return { name: 'blocked', card: <BlockedCard /> };
    case 'update_needed': return { name: 'update_needed', card: <UpdateNeededCard /> };
    default: return null;
  }
}

/**
 * The connection panel for the hosted build, one screen per thing a person can do, over the empty editor.
 * Renders nothing once connected unless it is on its way out (`exit`). Every word comes from `copy.ts`.
 */
export function RuntimeConnectionPanel({ connection, exit = null, firstRun = false }: RuntimeConnectionPanelProps) {
  // The landing page's install dialog asks the same question, so the two always agree on who is on a phone.
  const phone = useMemo(isMobileDevice, []);
  const { state } = connection;
  if (state.status === 'connected') return null;
  if (state.status === 'connecting' && !awaitingConnect(connection)) return <ConnectingPanel phone={phone} exit={exit} />;
  const screen = screenFor(connection, phone, firstRun);
  if (!screen) return null;
  return <GateLayer dataState={screen.name} exit={exit}>{screen.card}</GateLayer>;
}
