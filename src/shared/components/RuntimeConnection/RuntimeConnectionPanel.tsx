import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { ArrowUp, Check, Link2 } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { MinkRunner } from '@/shared/components/MinkRunner/MinkRunner.tsx';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import type { RuntimeNotReadyReason } from '@/integrations/runtime/connection.ts';
import { isMobileDevice } from '@/pages/Home/installScenario.ts';
import { useSendLinkToComputer } from '@/pages/Home/useSendLinkToComputer.ts';
import { CopyAgentInstructions } from './CopyAgentInstructions.tsx';
import { RUNTIME_CONNECTION_COPY as COPY } from './copy.ts';

export interface RuntimeConnectionPanelProps {
  /** The gate's value; the panel is only rendered while it is not connected. */
  readonly connection: RuntimeConnectionValue;
}

/** How long the mark is alone on the screen before the line under it fades in. */
const CONNECTING_LINE_DELAY_MS = 1000;

const AVATAR_SRC = '/astrid-avatar.png';

interface PanelFrameProps {
  /** The `data-state` the journey and the Layout test read: `connecting`, `permission`, `cant_reach`, `blocked`, `not_ready`. */
  readonly dataState: string;
  readonly title: string;
  readonly sentence: string;
  /** The state's one primary action. */
  readonly action?: ReactNode;
  /** The one quiet line under the action. */
  readonly footer?: ReactNode;
  /** Content between the sentence and the action (the blocked state's steps). */
  readonly children?: ReactNode;
  /** A small arrow above the avatar: the thing to look at is Chrome's prompt, up by the address bar. */
  readonly pointUp?: boolean;
}

/**
 * The one layout every not-connected card shares, in the install dialog's style: the avatar, a serif heading, one
 * sentence, at most one primary button and at most one quiet line. Everything is centred.
 */
function PanelFrame({ dataState, title, sentence, action, footer, children, pointUp = false }: PanelFrameProps) {
  return (
    <section
      aria-label={COPY.panelLabel}
      data-testid="runtime-not-connected"
      data-state={dataState}
      className="flex min-h-screen items-center justify-center bg-background p-4 text-foreground"
    >
      <div className="w-full max-w-md space-y-5 rounded-2xl border border-border bg-card p-6 text-center sm:p-8">
        <div className="space-y-3">
          {pointUp && <ArrowUp aria-hidden="true" className="mx-auto h-6 w-6 text-primary" />}
          <img src={AVATAR_SRC} alt="" className="mx-auto h-14 w-14 rounded-xl" />
        </div>
        <div className="space-y-3">
          <h1 className="font-serif font-theme-heading text-2xl leading-tight text-foreground">{title}</h1>
          <p className="text-base leading-7 text-muted-foreground">{sentence}</p>
        </div>
        {children}
        {action && <div className="flex flex-col items-center">{action}</div>}
        {footer && <p className="text-sm text-muted-foreground">{footer}</p>}
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
      <MinkRunner className="text-foreground" />
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
  const { copied, send } = useSendLinkToComputer(() => window.location.origin);
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

/** Chrome's local-network prompt has not been asked: nothing was sent, and Connect is what asks. */
function PermissionPanel({ connection }: { connection: RuntimeConnectionValue }) {
  const { permission } = COPY;
  if (connection.isChecking) {
    // Chrome's prompt is open: nothing to press, only where to look.
    return <PanelFrame dataState="permission" title={permission.pending.title} sentence={permission.pending.sentence} pointUp />;
  }
  return (
    <PanelFrame
      dataState="permission"
      title={permission.title}
      sentence={permission.sentence}
      action={<Button type="button" className="w-full sm:w-auto" onClick={() => connection.connect()}>{permission.connect}</Button>}
    />
  );
}

/** Permission `denied`: the browser stopped the request, so the fix is in Chrome's site settings. */
function BlockedPanel() {
  const blocked = COPY.blocked;
  return (
    // No agent button: the fix is a Chrome site setting, which an agent cannot change.
    <PanelFrame dataState="blocked" title={blocked.title} sentence={blocked.sentence} footer={blocked.footer}>
      <ol className="list-decimal space-y-2 pl-5 text-left text-sm leading-6 text-muted-foreground">
        {blocked.steps.map((step) => <li key={step}>{step}</li>)}
      </ol>
    </PanelFrame>
  );
}

/** Nothing answers and this page has never connected: the install path. */
function SetUpPanel({ pageOrigin }: { pageOrigin: string }) {
  const { setUp } = COPY;
  return (
    <PanelFrame
      dataState="cant_reach"
      title={setUp.title}
      sentence={setUp.sentence}
      action={<CopyAgentInstructions pageOrigin={pageOrigin} label={COPY.agent.copySetup} variant="start" />}
      footer={(
        <>
          {setUp.footer.before}
          <a href={COPY.commands.installUrl} target="_blank" rel="noreferrer" className="text-foreground underline underline-offset-2">
            {setUp.footer.linkText}
          </a>
          {setUp.footer.after}
        </>
      )}
    />
  );
}

/** Nothing answers on a return visit, or the gateway answered but Astrid is not ready: a person does the same for each. */
function NotRunningPanel({ dataState, pageOrigin }: { dataState: string; pageOrigin: string }) {
  const { notRunning } = COPY;
  return (
    <PanelFrame
      dataState={dataState}
      title={notRunning.title}
      sentence={notRunning.sentence}
      action={<CopyAgentInstructions pageOrigin={pageOrigin} label={notRunning.button} variant="start" />}
    />
  );
}

/** The Astrid running is not the one this page was set up with: only a restart helps, and the agent block says so. */
function RestartNeededPanel({ pageOrigin }: { pageOrigin: string }) {
  const { restartNeeded } = COPY;
  return (
    <PanelFrame
      dataState="not_ready"
      title={restartNeeded.title}
      sentence={restartNeeded.sentence}
      action={<CopyAgentInstructions pageOrigin={pageOrigin} label={restartNeeded.button} variant="restart" />}
    />
  );
}

/** The screen a not-ready reason shows: five causes, three things a person can do. */
function notReadyScreen(reason: RuntimeNotReadyReason): 'connecting' | 'not_running' | 'restart_needed' {
  switch (reason) {
    case 'starting': return 'connecting';
    case 'runtime_stopped':
    case 'unknown': return 'not_running';
    case 'identity_mismatch':
    case 'realm_changed': return 'restart_needed';
  }
}

/**
 * The connection panel for the hosted build, one screen per thing a person can do (Plan A, D3). Renders nothing once
 * connected: the gate then shows the app. Every word comes from `copy.ts`.
 */
export function RuntimeConnectionPanel({ connection }: RuntimeConnectionPanelProps) {
  const pageOrigin = window.location.origin;
  // The landing page's install dialog asks the same question, so the two always agree on who is on a phone.
  const phone = useMemo(isMobileDevice, []);
  const { state } = connection;
  if (state.status === 'connected') return null;
  if (connection.awaitingConnect) return phone ? <PhonePanel /> : <PermissionPanel connection={connection} />;
  switch (state.status) {
    case 'connecting':
      return <ConnectingPanel phone={phone} />;
    case 'cant_reach':
      if (phone) return <PhonePanel />;
      return state.firstTime ? <SetUpPanel pageOrigin={pageOrigin} /> : <NotRunningPanel dataState="cant_reach" pageOrigin={pageOrigin} />;
    case 'blocked':
      return phone ? <PhonePanel /> : <BlockedPanel />;
    case 'not_ready': {
      const screen = notReadyScreen(state.reason);
      if (screen === 'connecting') return <ConnectingPanel phone={phone} />;
      if (phone) return <PhonePanel />;
      return screen === 'not_running'
        ? <NotRunningPanel dataState="not_ready" pageOrigin={pageOrigin} />
        : <RestartNeededPanel pageOrigin={pageOrigin} />;
    }
  }
}
