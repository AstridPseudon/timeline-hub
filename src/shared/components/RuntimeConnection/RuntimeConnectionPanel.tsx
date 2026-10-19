import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { Check, Link2 } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { MinkRunner } from '@/shared/components/MinkRunner/MinkRunner.tsx';
import { ToolbarPointer } from '@/shared/components/ToolbarPointer/ToolbarPointer.tsx';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { isMobileDevice } from '@/pages/Home/installScenario.ts';
import { useSendLinkToComputer } from '@/pages/Home/useSendLinkToComputer.ts';
import { CopyInstallCommand } from './CopyInstallCommand.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, withBrowser } from './copy.ts';

export interface RuntimeConnectionPanelProps {
  /** The gate's value; the panel is only rendered while it is not connected. */
  readonly connection: RuntimeConnectionValue;
}

/** How long the mark is alone on the screen before the line under it fades in. */
const CONNECTING_LINE_DELAY_MS = 1000;

/** The same face the landing page, the install dialog and the header show: the pixel mink's app icon. */
const AVATAR_SRC = '/astrid-app-icon-192.png';

interface PanelFrameProps {
  /** The screen name, read by the journey and Layout tests. */
  readonly dataState: string;
  readonly title: string;
  readonly sentence: string;
  /** A second line under the sentence, in the same voice (set up's "Already installed?"). */
  readonly detail?: string;
  /** The state's one primary action. */
  readonly action?: ReactNode;
  /** The one quiet line under the action. */
  readonly footer?: ReactNode;
  /** Content between the sentence and the action (the blocked state's steps). */
  readonly children?: ReactNode;
  /** The word on a hand-drawn arrow, outside the card, aimed at the top left of the window: the browser's prompt is there. */
  readonly pointer?: string;
}

/**
 * The one layout every not-connected card shares, in the install dialog's style: the avatar, a serif heading, one
 * sentence (two only on set up), at most one primary button and at most one quiet line. Everything is centred, and
 * balanced so no line ends on a lone word at phone width.
 */
function PanelFrame({ dataState, title, sentence, detail, action, footer, children, pointer }: PanelFrameProps) {
  return (
    <section
      aria-label={COPY.panelLabel}
      data-testid="runtime-not-connected"
      data-state={dataState}
      className="flex min-h-screen items-center justify-center bg-background p-4 text-foreground"
    >
      <div className="w-full max-w-md space-y-5 rounded-2xl border border-border bg-card p-6 text-center sm:p-8">
        {/* The icon file carries its own rounded tile and shadow, as the install dialog shows it at this size. */}
        <img src={AVATAR_SRC} alt="" className="mx-auto h-[76px] w-[76px]" />
        <div className="space-y-3">
          <h1 className="text-balance font-serif font-theme-heading text-2xl leading-tight text-foreground">{title}</h1>
          <p className="text-balance text-base leading-7 text-muted-foreground">{sentence}</p>
          {detail && <p className="text-balance text-base leading-7 text-muted-foreground">{detail}</p>}
        </div>
        {children}
        {action && <div className="flex flex-col items-center">{action}</div>}
        {footer && <p className="text-balance text-sm text-muted-foreground">{footer}</p>}
        {pointer && <ToolbarPointer label={pointer} corner="top-left" tone="page" />}
      </div>
    </section>
  );
}

/** The mark alone on the page background, as the boot screen shows it; the line fades in only if the wait is not short. */
function ConnectingPanel({ phone }: { phone: boolean }) {
  const [lineShown, setLineShown] = useState(false);
  useEffect(() => {
    const timer = window.setTimeout(() => setLineShown(true), CONNECTING_LINE_DELAY_MS);
    return () => window.clearTimeout(timer);
  }, []);
  // A phone never reaches Astrid, so once the wait is long enough to see, it gets the phone screen instead.
  if (lineShown && phone) return <PhonePanel />;
  return (
    <section
      aria-label={COPY.panelLabel}
      data-testid="runtime-not-connected"
      data-state="connecting"
      className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background p-4 text-foreground"
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
function PhonePanel() {
  const { phone } = COPY;
  const { copied, send } = useSendLinkToComputer(() => window.location.href);
  return (
    <PanelFrame
      dataState="phone"
      title={phone.title}
      sentence={phone.sentence}
      action={(
        <Button type="button" className="w-full sm:w-auto" onClick={() => void send()}>
          {copied ? <Check aria-hidden="true" className="mr-2 h-4 w-4" /> : <Link2 aria-hidden="true" className="mr-2 h-4 w-4" />}
          {copied ? phone.copied : phone.button}
        </Button>
      )}
    />
  );
}

/** The browser's local-network prompt has not been asked: nothing was sent, and Connect is what asks. */
function PermissionPanel({ connection }: { connection: RuntimeConnectionValue }) {
  const { permission } = COPY;
  if (connection.isChecking) {
    // The browser's prompt is open: nothing to press, only where to look.
    return (
      <PanelFrame
        dataState="pending"
        title={withBrowser(permission.pending.title)}
        sentence={withBrowser(permission.pending.sentence)}
        pointer={permission.pending.pointer}
      />
    );
  }
  return (
    <PanelFrame
      dataState="permission"
      title={withBrowser(permission.title)}
      sentence={withBrowser(permission.sentence)}
      action={<Button type="button" className="w-full sm:w-auto" onClick={() => connection.connect()}>{permission.connect}</Button>}
    />
  );
}

/** Permission `denied`: the browser stopped the request, so the fix is in its site settings. */
function BlockedPanel() {
  const blocked = COPY.blocked;
  return (
    // No agent button: the fix is a browser site setting, which an agent cannot change.
    <PanelFrame dataState="blocked" title={withBrowser(blocked.title)} sentence={withBrowser(blocked.sentence)} footer={blocked.footer}>
      <ol className="list-decimal space-y-2 pl-5 text-left text-sm leading-6 text-muted-foreground text-pretty">
        {blocked.steps.map((step) => <li key={step}>{step}</li>)}
      </ol>
    </PanelFrame>
  );
}

/**
 * Nothing answers and this browser has never connected. That is also what a set-up computer looks like from a new
 * browser or a private window, so the screen uses the same idempotent install line.
 */
function SetUpPanel() {
  const { setUp } = COPY;
  return (
    <PanelFrame
      dataState="set_up"
      title={setUp.title}
      sentence={setUp.sentence}
      action={<CopyInstallCommand label={COPY.agent.copy} mode="install" />}
    />
  );
}

/** Nothing answers on a return visit, or the gateway answered but Astrid is not ready: a person does the same for each. */
function NotRunningPanel() {
  const { notRunning } = COPY;
  return (
    <PanelFrame
      dataState="not_running"
      title={notRunning.title}
      sentence={notRunning.sentence}
      action={<CopyInstallCommand label={COPY.agent.copy} mode="install" />}
    />
  );
}

/** Astrid changed while it was running: the same install line repairs and restarts it. */
function RestartNeededPanel() {
  const { restartNeeded } = COPY;
  return (
    <PanelFrame
      dataState="restart_needed"
      title={restartNeeded.title}
      sentence={restartNeeded.sentence}
      action={<CopyInstallCommand label={COPY.agent.copy} mode="install" />}
    />
  );
}

function UpdateNeededPanel() {
  const { updateNeeded } = COPY;
  return (
    <PanelFrame
      dataState="update_needed"
      title={updateNeeded.title}
      sentence={updateNeeded.sentence}
      action={<CopyInstallCommand label={COPY.agent.copy} mode="update" />}
    />
  );
}

/**
 * The connection panel for the hosted build, one screen per thing a person can do (Plan A, D3). Renders nothing once
 * connected: the gate then shows the app. Every word comes from `copy.ts`.
 */
export function RuntimeConnectionPanel({ connection }: RuntimeConnectionPanelProps) {
  // The landing page's install dialog asks the same question, so the two always agree on who is on a phone.
  const phone = useMemo(isMobileDevice, []);
  const { state } = connection;
  if (state.status === 'connected') return null;
  // Keep setup visible before permission unless a prior connection or explicit installer handoff takes precedence.
  if (connection.awaitingConnect && (state.status !== 'set_up' || connection.isChecking)) {
    return phone ? <PhonePanel /> : <PermissionPanel connection={connection} />;
  }
  switch (state.status) {
    case 'connecting':
      return <ConnectingPanel phone={phone} />;
    case 'set_up':
      return phone ? <PhonePanel /> : <SetUpPanel />;
    case 'not_running':
      return phone ? <PhonePanel /> : <NotRunningPanel />;
    case 'blocked':
      return phone ? <PhonePanel /> : <BlockedPanel />;
    case 'restart_needed':
      return phone ? <PhonePanel /> : <RestartNeededPanel />;
    case 'update_needed':
      return phone ? <PhonePanel /> : <UpdateNeededPanel />;
  }
}
