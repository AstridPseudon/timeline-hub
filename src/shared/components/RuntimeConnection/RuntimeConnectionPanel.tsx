import type { ReactNode } from 'react';
import { LoaderCircle, Plug, ShieldAlert, TriangleAlert, WifiOff } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import type { RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { CopyAgentInstructions } from './CopyAgentInstructions.tsx';
import { RUNTIME_CONNECTION_COPY as COPY, type Segment } from './copy.ts';

export interface RuntimeConnectionPanelProps {
  /** The gate's value; the panel is only rendered while it is not connected. */
  readonly connection: RuntimeConnectionValue;
}

interface PanelFrameProps {
  /** The `data-state` the journey and the Layout test read: `connecting`, `permission`, `cant_reach`, `blocked`, `not_ready`. */
  readonly dataState: string;
  readonly icon: ReactNode;
  readonly title: string;
  readonly pageOrigin: string;
  readonly showCopy?: boolean;
  readonly children?: ReactNode;
}

/** The one layout every not-connected state shares: an icon, a heading, its body and the agent instructions. */
function PanelFrame({ dataState, icon, title, pageOrigin, showCopy = true, children }: PanelFrameProps) {
  return (
    <section
      aria-label={COPY.panelLabel}
      data-testid="runtime-not-connected"
      data-state={dataState}
      className="flex min-h-screen items-center justify-center bg-background p-4 text-foreground"
    >
      <div className="w-full max-w-xl space-y-5 rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted text-muted-foreground">
          {icon}
        </div>
        <div className="space-y-3">
          <h1 className="text-xl font-semibold leading-tight">{title}</h1>
          {children}
        </div>
        {showCopy && (
          <div className="border-t border-border/70 pt-4">
            <CopyAgentInstructions pageOrigin={pageOrigin} />
          </div>
        )}
      </div>
    </section>
  );
}

const Body = ({ children }: { children: ReactNode }) => <p className="text-sm leading-6 text-muted-foreground">{children}</p>;

/** Inline code: a command to type, or an address to select. Wraps anywhere, so a long one never overflows a phone. */
const Code = ({ children, select = false }: { children: ReactNode; select?: boolean }) => (
  <code className={`break-all rounded bg-muted px-1 py-0.5 font-mono text-xs text-foreground${select ? ' select-all' : ''}`}>{children}</code>
);

/** A sentence of text and commands, with each command in `<code>`. */
const Sentence = ({ segments }: { segments: readonly Segment[] }) => (
  <Body>
    {segments.map((segment, index) => (typeof segment === 'string'
      ? <span key={index}>{segment}</span>
      : <Code key={index}>{segment.code}</Code>))}
  </Body>
);

/** How to install, with readable link text to the guide's full address. */
const InstallLine = () => (
  <Body>
    {COPY.install.before}
    <a href={COPY.commands.installUrl} target="_blank" rel="noreferrer" className="text-foreground underline underline-offset-2">
      {COPY.install.linkText}
    </a>
    {COPY.install.after}
  </Body>
);

/** Chrome's local-network prompt has not been asked: nothing was sent, and Connect is what asks. */
function PermissionPanel({ connection, pageOrigin }: { connection: RuntimeConnectionValue; pageOrigin: string }) {
  const { permission } = COPY;
  return (
    <PanelFrame dataState="permission" icon={<Plug aria-hidden="true" className="h-5 w-5" />} title={permission.title} pageOrigin={pageOrigin}>
      <Body>{permission.explainer[0]}</Body>
      <Body>{permission.explainer[1]}</Body>
      <div>
        <Button type="button" onClick={() => connection.connect()} disabled={connection.isChecking}>
          {connection.isChecking ? permission.connectPending : permission.connect}
        </Button>
      </div>
      <InstallLine />
    </PanelFrame>
  );
}

/** Nothing answers: first time on this origin, or a returning visit where Reigh has stopped. */
function CantReachPanel({ firstTime, pageOrigin }: { firstTime: boolean; pageOrigin: string }) {
  if (!firstTime) {
    const returning = COPY.cantReach.returning;
    return (
      <PanelFrame dataState="cant_reach" icon={<WifiOff aria-hidden="true" className="h-5 w-5" />} title={returning.title} pageOrigin={pageOrigin}>
        <Body>{returning.sentence}</Body>
      </PanelFrame>
    );
  }
  const first = COPY.cantReach.firstTime;
  return (
    <PanelFrame dataState="cant_reach" icon={<WifiOff aria-hidden="true" className="h-5 w-5" />} title={first.title} pageOrigin={pageOrigin}>
      <Body>{first.sentence}</Body>
      <Body>{first.alreadyInstalled}</Body>
      <InstallLine />
    </PanelFrame>
  );
}

/** Permission `denied`: the browser stopped the request, so the fix is in Chrome's site settings. */
function BlockedPanel({ pageOrigin }: { pageOrigin: string }) {
  const blocked = COPY.blocked;
  return (
    // No agent instructions: the fix is a Chrome site setting, which an agent cannot change.
    <PanelFrame dataState="blocked" icon={<ShieldAlert aria-hidden="true" className="h-5 w-5" />} title={blocked.title} pageOrigin={pageOrigin} showCopy={false}>
      <Body>{blocked.sentence}</Body>
      <div className="space-y-2">
        <h3 className="text-base font-medium text-foreground [font-family:inherit]">{blocked.fixTitle}</h3>
        <ol className="list-decimal space-y-2 pl-5 text-sm leading-6 text-muted-foreground">
          {blocked.fixSteps.map((step) => <li key={step}>{step}</li>)}
        </ol>
        <p className="text-xs leading-5 text-muted-foreground">
          {blocked.settingsHint}{' '}
          <Code select>{blocked.settingsAddress(pageOrigin)}</Code>
        </p>
      </div>
    </PanelFrame>
  );
}

/** The gateway answered 503: it is up, and the Runtime behind it is not ready. */
function NotReadyPanel({ reason, pageOrigin }: { reason: keyof typeof COPY.notReady.reasons; pageOrigin: string }) {
  const { title, sentence } = COPY.notReady.reasons[reason];
  return (
    // 'starting' only waits, so there is nothing to copy for an agent.
    <PanelFrame dataState="not_ready" icon={<TriangleAlert aria-hidden="true" className="h-5 w-5" />} title={title} pageOrigin={pageOrigin} showCopy={reason !== 'starting'}>
      <Sentence segments={sentence} />
    </PanelFrame>
  );
}

/**
 * The connection panel for the hosted build, one per state (Plan A, D3). Renders nothing once connected: the gate
 * then shows the app, and the pill takes over. Every heading and sentence comes from `copy.ts`.
 */
export function RuntimeConnectionPanel({ connection }: RuntimeConnectionPanelProps) {
  const pageOrigin = window.location.origin;
  const { state } = connection;
  if (state.status === 'connected') return null;
  if (connection.awaitingConnect) return <PermissionPanel connection={connection} pageOrigin={pageOrigin} />;
  switch (state.status) {
    case 'connecting':
      return (
        <PanelFrame
          dataState="connecting"
          icon={<LoaderCircle aria-hidden="true" className="h-5 w-5 animate-spin" />}
          title={COPY.connecting.title}
          pageOrigin={pageOrigin}
          showCopy={false}
        >
          <Body>{COPY.connecting.sentence}</Body>
        </PanelFrame>
      );
    case 'cant_reach':
      return <CantReachPanel firstTime={state.firstTime} pageOrigin={pageOrigin} />;
    case 'blocked':
      return <BlockedPanel pageOrigin={pageOrigin} />;
    case 'not_ready':
      return <NotReadyPanel reason={state.reason} pageOrigin={pageOrigin} />;
  }
}
