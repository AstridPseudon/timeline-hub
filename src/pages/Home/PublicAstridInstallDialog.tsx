import { useCallback, useEffect, useLayoutEffect, useMemo, useRef } from 'react';
import { ArrowRight, Check, Link2, Monitor, Share, X } from 'lucide-react';
import {
  APP_ENTRY_PATH,
  rememberAppEntryPreference,
} from '@/app/entryClassification.ts';
import { requestAutoConnect } from '@/integrations/runtime/autoConnectRequest.ts';
import { runInstallPrompt, useInstallPromptSignals } from '@/shared/hooks/platformInstall/signals';
import { detectInstallScenario, type InstallScenario } from './installScenario.ts';
import { ToolbarPointer } from '@/shared/components/ToolbarPointer/ToolbarPointer.tsx';
import { useSendLinkToComputer } from './useSendLinkToComputer.ts';
import { CopyInstallCommand } from '@/shared/components/RuntimeConnection/CopyInstallCommand.tsx';
import { withCommandShell } from '@/shared/components/RuntimeConnection/copy.ts';
import './PublicAstridInstallDialog.css';

const AVATAR_SRC = '/astrid-app-icon-192.png';
const HOME_PATH = '/home';

/** Landing page wording is kept together here for the product copy pass. */
export const SET_UP_ASTRID_COPY = {
  title: 'Set up Astrid',
  subtitle: 'Run one line in a terminal to set up Astrid on your computer.',
  copyCommand: 'Copy',
  browserShortcut: 'Add a browser shortcut',
  installNow: 'Add the shortcut',
  useHere: 'Already set up? Open Astrid',
  useHereInstalled: 'Open Astrid in this tab',
};

function useInstallScenario(): InstallScenario {
  return useMemo(detectInstallScenario, []);
}

function useBrowserInstall(active: boolean) {
  const { deferredPrompt, isAppInstalled, consumeDeferredPrompt } = useInstallPromptSignals();
  const activeRef = useRef(active);
  const requestRef = useRef(0);

  useEffect(() => {
    activeRef.current = active;
    if (!active) requestRef.current += 1;
  }, [active]);

  useEffect(() => () => {
    activeRef.current = false;
    requestRef.current += 1;
  }, []);

  // Installing from anywhere (the address bar included, not just this dialog) sends later visits
  // straight into the app.
  useEffect(() => {
    if (isAppInstalled) rememberAppEntryPreference();
  }, [isAppInstalled]);

  const promptInstall = useCallback(async () => {
    if (!activeRef.current || !deferredPrompt) return;
    const promptEvent = deferredPrompt;
    const request = ++requestRef.current;
    try {
      const { outcome } = await runInstallPrompt(promptEvent);
      if (!activeRef.current || request !== requestRef.current || !consumeDeferredPrompt(promptEvent)) return;
      if (outcome === 'accepted') rememberAppEntryPreference();
    } catch {
      if (activeRef.current && request === requestRef.current) consumeDeferredPrompt(promptEvent);
    }
  }, [consumeDeferredPrompt, deferredPrompt]);

  return { canPrompt: Boolean(deferredPrompt), installed: isAppInstalled, promptInstall };
}

function openInBrowser() {
  rememberAppEntryPreference();
  // Choosing the browser already says "take me in": the app goes straight to Chrome's prompt instead of explaining it first.
  requestAutoConnect();
  window.location.assign(APP_ENTRY_PATH);
}

/** A little window mock: the address bar's install icon pulses, is clicked, and offers Install. */
function ChromiumVisual() {
  return (
    <div className="astrid-install-visual" data-scenario="chromium" aria-hidden="true">
      <div className="astrid-install-window">
        <div className="astrid-install-toolbar">
          <span className="astrid-install-lights"><i /><i /><i /></span>
          <span className="astrid-install-omnibox">
            <span className="astrid-install-url">astrid</span>
            <span className="astrid-install-target astrid-install-target-chromium">
              <Monitor size={11} strokeWidth={2.2} />
              <ArrowRight className="astrid-install-target-arrow" size={7} strokeWidth={3} />
            </span>
          </span>
          <span className="astrid-install-menu"><i /><i /><i /></span>
        </div>
        <div className="astrid-install-page"><i /><i /><i /></div>
        <div className="astrid-install-popover">
          <span className="astrid-install-popover-title">Install app?</span>
          <span className="astrid-install-popover-app">
            <img src={AVATAR_SRC} alt="" />
            <span>Astrid</span>
          </span>
          <span className="astrid-install-popover-actions">
            <span>Cancel</span>
            <span className="astrid-install-popover-confirm">Install</span>
          </span>
        </div>
        <span className="astrid-install-cursor" />
      </div>
    </div>
  );
}

/** Safari (17+): the Share button, then Add to Dock. */
function SafariVisual() {
  return (
    <div className="astrid-install-visual" data-scenario="safari" aria-hidden="true">
      <div className="astrid-install-window">
        <div className="astrid-install-toolbar">
          <span className="astrid-install-lights"><i /><i /><i /></span>
          <span className="astrid-install-omnibox astrid-install-omnibox-centred">
            <span className="astrid-install-url">astrid</span>
          </span>
          <span className="astrid-install-target astrid-install-target-safari"><Share size={11} strokeWidth={2.2} /></span>
        </div>
        <div className="astrid-install-page"><i /><i /><i /></div>
        <div className="astrid-install-popover astrid-install-share-menu">
          <span>Copy</span>
          <span>Add to Reading List</span>
          <span className="astrid-install-popover-confirm">Add to Dock…</span>
        </div>
        <span className="astrid-install-cursor" />
      </div>
    </div>
  );
}

const DESKTOP_COPY: Record<Exclude<InstallScenario, 'mobile'>, { lede: string; steps: string[] }> = {
  chromium: {
    lede: 'Give Astrid its own window, like any other app.',
    steps: ['Click the install icon at the right end of the address bar, up here.', 'Choose Install.'],
  },
  safari: {
    lede: 'Give Astrid its own window in your Dock, like any other app.',
    steps: ['Click the Share button in the top-right of the toolbar.', 'Choose Add to Dock.'],
  },
  unsupported: {
    lede: 'This browser can’t add shortcuts. Chrome, Edge and Safari can.',
    steps: [],
  },
};

function homeLink() {
  return new URL(HOME_PATH, window.location.origin).href;
}

function MobileContent({ onClose, active }: { onClose: () => void; active: boolean }) {
  const { copied, send: sendToComputer } = useSendLinkToComputer(homeLink, active);
  return (
    <>
      <div className="astrid-install-desk" aria-hidden="true">
        <span className="astrid-install-desk-phone" />
        <ArrowRight className="astrid-install-desk-arrow" size={18} strokeWidth={2.2} />
        <span className="astrid-install-desk-laptop"><span /></span>
      </div>
      <p className="astrid-install-lede">
        Astrid runs on a computer. Open this page there to copy the line.
      </p>
      <div className="astrid-install-actions">
        <button type="button" className="astrid-button astrid-button-primary" onClick={sendToComputer}>
          <span>{copied ? 'Link copied' : 'Send the link to your computer'}</span>
          {copied ? <Check size={17} aria-hidden="true" /> : <Link2 size={17} aria-hidden="true" />}
        </button>
        <button type="button" className="astrid-install-quiet" onClick={onClose}>Not now</button>
      </div>
    </>
  );
}

/**
 * The landing page's install flow: a visual explainer for installing Astrid as an app from the
 * browser, anchored in the top-right corner where the browser's install control lives, with the
 * option to use it right here instead. Either choice makes the site open straight into the app on
 * later visits; /home keeps the landing page.
 */
export function PublicAstridInstallDialog({ open, onClose }: { open: boolean; onClose: () => void }) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const returnFocusRef = useRef<HTMLElement | null>(null);
  const closeNotifiedRef = useRef(true);
  const onCloseRef = useRef(onClose);
  const scenario = useInstallScenario();
  const { canPrompt, installed, promptInstall } = useBrowserInstall(open);

  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);

  const restoreFocus = useCallback(() => {
    const target = returnFocusRef.current;
    returnFocusRef.current = null;
    if (!target || !target.isConnected || target.hasAttribute('disabled') || target.closest('[inert], [aria-hidden="true"]')) return;
    try {
      target.focus({ preventScroll: true });
    } catch {
      target.focus();
    }
  }, []);

  const notifyClosed = useCallback(() => {
    if (closeNotifiedRef.current) return;
    closeNotifiedRef.current = true;
    onCloseRef.current();
    restoreFocus();
  }, [restoreFocus]);

  const requestClose = useCallback(() => {
    const dialog = dialogRef.current;
    if (dialog?.open) dialog.close();
    notifyClosed();
  }, [notifyClosed]);

  useLayoutEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) {
      const activeElement = document.activeElement;
      if (activeElement instanceof HTMLElement && activeElement !== document.body && !dialog.contains(activeElement)) {
        returnFocusRef.current = activeElement;
      }
      closeNotifiedRef.current = false;
      dialog.showModal();
      closeButtonRef.current?.focus({ preventScroll: true });
    } else if (!open) {
      if (dialog.open) dialog.close();
      notifyClosed();
    }
  }, [notifyClosed, open]);

  useEffect(() => {
    const dialog = dialogRef.current;
    return () => {
      if (dialog?.open) dialog.close();
      notifyClosed();
    };
  }, [notifyClosed]);

  const desktop = scenario !== 'mobile';
  const copy = desktop ? DESKTOP_COPY[scenario] : null;
  const pointsUp = scenario === 'chromium' || scenario === 'safari';

  return (
    <dialog
      ref={dialogRef}
      className="astrid-install-dialog"
      data-scenario={scenario}
      data-points-up={pointsUp && !installed ? '' : undefined}
      aria-labelledby="astrid-install-title"
      aria-modal="true"
      onClose={notifyClosed}
      onCancel={(event) => {
        event.preventDefault();
        requestClose();
      }}
      onClick={(event) => {
        // A click on the backdrop (the dialog element itself, outside its card) dismisses it.
        if (event.target === event.currentTarget) requestClose();
      }}
    >
      <div className="astrid-install-card">
        {open && pointsUp && !installed ? (
          <ToolbarPointer label={scenario === 'safari' ? 'Share, up here' : 'Up here'} />
        ) : null}
        <button ref={closeButtonRef} type="button" className="astrid-install-close" onClick={requestClose} aria-label="Close">
          <X size={16} strokeWidth={2} aria-hidden="true" />
        </button>
        <header className="astrid-install-header">
          <img className="astrid-install-avatar" src={AVATAR_SRC} alt="" />
          <div>
            <h2 id="astrid-install-title">{SET_UP_ASTRID_COPY.title}</h2>
            <p>{withCommandShell(SET_UP_ASTRID_COPY.subtitle)}</p>
          </div>
        </header>

        {!desktop ? <MobileContent onClose={requestClose} active={open} /> : null}

        {desktop && copy ? (
          <>
            <CopyInstallCommand label={SET_UP_ASTRID_COPY.copyCommand} />
            <div className="astrid-install-actions">
              <details className="astrid-install-guide">
                <summary>{SET_UP_ASTRID_COPY.browserShortcut}</summary>
                <div className="astrid-install-body">
                  {scenario === 'chromium' ? <ChromiumVisual /> : null}
                  {scenario === 'safari' ? <SafariVisual /> : null}
                  <div>
                    <p className="astrid-install-lede">{copy.lede}</p>
                    {copy.steps.length ? <ol className="astrid-install-steps">{copy.steps.map((step) => <li key={step}>{step}</li>)}</ol> : null}
                    {canPrompt && !installed ? <button type="button" className="astrid-button astrid-button-primary" onClick={promptInstall}>{SET_UP_ASTRID_COPY.installNow} <Monitor size={17} aria-hidden="true" /></button> : null}
                  </div>
                </div>
              </details>
              <button type="button" className="astrid-button astrid-install-here" onClick={openInBrowser}>
                <span>{installed ? SET_UP_ASTRID_COPY.useHereInstalled : SET_UP_ASTRID_COPY.useHere}</span><ArrowRight size={17} aria-hidden="true" />
              </button>
            </div>
          </>
        ) : null}
      </div>
    </dialog>
  );
}
