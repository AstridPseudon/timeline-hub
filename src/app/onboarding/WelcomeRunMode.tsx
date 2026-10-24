import { useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { detectBrowser } from '@/shared/hooks/platformInstall/platformDetection.ts';
import { runInstallPrompt, useInstallPromptSignals, useStandaloneStatus } from '@/shared/hooks/platformInstall/signals.ts';
import { detectInstallScenario } from '@/pages/Home/installScenario.ts';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';
import { localSetupInstructions, type WindowMode } from '@/shared/components/RuntimeConnection/copy.ts';
import { writeWelcomePhase } from './welcomeProgress.ts';

export type { WindowMode };

interface Props {
  readonly local?: boolean;
  readonly onContinue?: (phase: 'connection' | 'local') => void;
  readonly onBack?: () => void;
  readonly windowMode: WindowMode;
  readonly setWindowMode: (mode: WindowMode) => void;
}

export function WelcomeRunMode({ local = false, onContinue, onBack, windowMode, setWindowMode }: Props) {
  const { deferredPrompt, consumeDeferredPrompt } = useInstallPromptSignals();
  const standalone = useStandaloneStatus();
  const browser = detectBrowser();
  const scenario = detectInstallScenario();
  const canInstall = !standalone && scenario === 'chromium' && deferredPrompt !== null;
  const [opened, setOpened] = useState(false);
  const [copied, setCopied] = useState(false);
  const [copyFailed, setCopyFailed] = useState(false);

  if (local) {
    const instructions = localSetupInstructions();
    return <main className="mx-auto grid min-h-screen w-full max-w-2xl content-center gap-6 px-6 py-10 text-foreground">
      <header className="space-y-3"><h1 className="text-balance font-serif text-3xl">Have your agent set it up</h1>
        <p className="text-pretty leading-7 text-muted-foreground">Paste these instructions into Claude Code, Codex or another agent. It installs Astrid, downloads the editor from <a className="underline underline-offset-4" href="https://github.com/banodoco/astrid-app">github.com/banodoco/astrid-app</a>, and starts both on your computer. When it&apos;s done, Astrid opens in your browser from your own machine.</p>
      </header>
      <div className="rounded-xl border border-border bg-card p-4"><pre className="whitespace-pre-wrap text-sm leading-6">{instructions}</pre></div>
      <div className="flex flex-wrap gap-3"><Button onClick={() => { void writeClipboardTextSafe(instructions).then(ok => { setCopied(ok); setCopyFailed(!ok); }); }}>{copied ? 'Copied' : 'Copy instructions'}</Button><Button variant="outline" onClick={onBack}>Back</Button></div>
      {copyFailed && <p role="status" className="text-sm text-muted-foreground">Copying didn&apos;t work. Select the instructions above and copy them.</p>}
    </main>;
  }

  const continueHere = () => onContinue?.('connection');
  const installApp = async () => {
    if (!deferredPrompt) return continueHere();
    writeWelcomePhase('connection');
    try {
      const { outcome } = await runInstallPrompt(deferredPrompt);
      consumeDeferredPrompt(deferredPrompt);
      if (outcome === 'accepted') setOpened(true);
      else continueHere();
    } catch { continueHere(); }
  };

  if (opened) return <main className="mx-auto grid min-h-screen w-full max-w-xl content-center gap-6 px-6 py-10 text-center text-foreground">
    <h1 className="text-balance font-serif text-3xl">Astrid opened in its own window</h1>
    <a href="#continue" className="underline underline-offset-4" onClick={event => { event.preventDefault(); continueHere(); }}>Continue here instead</a>
  </main>;

  return <main className="mx-auto grid min-h-screen w-full max-w-2xl content-center gap-6 px-6 py-10 text-foreground">
    <header className="space-y-2"><h1 className="text-balance font-serif text-3xl">How do you want to run Astrid?</h1></header>
    <section className="space-y-4 rounded-xl border border-border bg-card p-5">
      <div className="space-y-1"><h2 className="font-semibold">Use it at astrid.haus.</h2><p className="text-sm text-muted-foreground">Most convenient. The editor stays up to date and connects to Astrid on your computer, where your files, models and agent run.</p></div>
      {canInstall && <div className="flex items-center gap-2"><span className="text-sm text-muted-foreground">Open in:</span><div role="radiogroup" aria-label="Open in" className="flex gap-2">
        {(['app-window', 'browser-tab'] as const).map(value => <button key={value} type="button" role="radio" aria-checked={windowMode === value} className="rounded-md border border-border px-3 py-2 text-sm hover:bg-muted" onClick={() => setWindowMode(value)}>{value === 'app-window' ? 'App window' : 'Browser tab'}</button>)}
      </div></div>}
      {browser === 'safari' && !standalone && <p className="text-sm text-muted-foreground">File → Add to Dock</p>}
      <Button className="w-full" onClick={canInstall && windowMode === 'app-window' ? installApp : continueHere}>{canInstall && windowMode === 'app-window' ? 'App window' : 'Continue in browser tab'}</Button>
    </section>
    <section className="space-y-4 rounded-xl border border-border bg-card p-5">
      <div className="space-y-1"><h2 className="font-semibold">Run everything on your computer.</h2><p className="text-sm text-muted-foreground">Most control. The editor runs on your machine too: no browser permission, works offline, and you can change Astrid itself. Your agent sets it up from <a className="underline underline-offset-4" href="https://github.com/banodoco/astrid-app">github.com/banodoco/astrid-app</a>.</p></div>
      <Button variant="outline" className="w-full" onClick={() => onContinue?.('local')}>Run everything on your computer</Button>
    </section>
  </main>;
}
