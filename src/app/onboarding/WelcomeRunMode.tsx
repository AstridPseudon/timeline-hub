import { useEffect, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { RadioGroup, RadioGroupItem } from '@/shared/components/ui/radio-group.tsx';
import { SegmentedControl, SegmentedControlItem } from '@/shared/components/ui/segmented-control.tsx';
import { runInstallPrompt, useInstallPromptSignals, useStandaloneStatus } from '@/shared/hooks/platformInstall/signals.ts';
import { detectInstallScenario } from '@/pages/Home/installScenario.ts';
import { LOCAL_SETUP, type WindowMode } from '@/shared/components/RuntimeConnection/copy.ts';
import { EditorCard } from '@/shared/components/RuntimeConnection/EditorCard.tsx';
import { EditorCardLayer } from '@/shared/components/RuntimeConnection/EditorCardLayer.tsx';
import { readWelcomePhase, writeWelcomePhase } from './welcomeProgress.ts';

export type { WindowMode };
export type RunMode = 'hosted' | 'local';

interface Props {
  readonly onContinue: (phase: 'connection' | 'local') => void;
  readonly windowMode: WindowMode;
  readonly setWindowMode: (mode: WindowMode) => void;
  readonly runMode: RunMode;
  readonly setRunMode: (mode: RunMode) => void;
}

export function WelcomeRunMode({ onContinue, windowMode, setWindowMode, runMode, setRunMode }: Props) {
  const { deferredPrompt, consumeDeferredPrompt } = useInstallPromptSignals();
  const standalone = useStandaloneStatus();
  const scenario = detectInstallScenario();
  const [installUnavailable, setInstallUnavailable] = useState(false);
  const canInstall = !standalone && scenario === 'chromium' && deferredPrompt !== null && !installUnavailable;
  const [opened, setOpened] = useState(false);
  const [copied, setCopied] = useState(false);

  const continueHere = () => {
    onContinue('connection');
  };
  const copyForChromium = async () => {
    await navigator.clipboard.writeText(window.location.href);
    setCopied(true);
  };
  const installApp = async () => {
    if (!deferredPrompt) return continueHere();
    const previousPhase = readWelcomePhase();
    writeWelcomePhase('connection');
    try {
      const { outcome } = await runInstallPrompt(deferredPrompt);
      consumeDeferredPrompt(deferredPrompt);
      if (outcome === 'accepted') setOpened(true);
      else {
        writeWelcomePhase(previousPhase);
        setInstallUnavailable(true);
      }
    } catch {
      consumeDeferredPrompt(deferredPrompt);
      writeWelcomePhase(previousPhase);
      setInstallUnavailable(true);
    }
  };

  useEffect(() => {
    if (opened && standalone) onContinue('connection');
  }, [opened, standalone, onContinue]);

  if (opened && !standalone) return <main aria-label="Astrid opened in its own window">
    <EditorCardLayer cardKey="opened">
      <EditorCard title="Astrid opened in its own window" sentence="Carry on there. You can close this tab.">
        <a href="#continue" className="text-[13px] text-muted-foreground underline underline-offset-4 hover:text-foreground" onClick={event => { event.preventDefault(); continueHere(); }}>Continue here instead</a>
      </EditorCard>
    </EditorCardLayer>
  </main>;

  const buttonLabel = runMode === 'local'
    ? 'Set up with your agent'
    : canInstall && windowMode === 'app-window'
      ? 'Install and continue'
      : standalone ? 'Continue' : 'Continue in this tab';

  return <main aria-label="How to run Astrid">
    <EditorCardLayer cardKey="choose">
      <EditorCard title="How do you want to run Astrid?">
        <div className="space-y-4">
          <RadioGroup aria-label="How to run Astrid" value={runMode} onValueChange={value => setRunMode(value as RunMode)} className="space-y-2.5">
            <div className={`rounded-xl border transition-colors ${runMode === 'hosted' ? 'border-primary/70 bg-primary/[0.06]' : 'border-border hover:border-foreground/25 hover:bg-muted/40'}`}>
              <label htmlFor="welcome-run-hosted" onClick={() => setRunMode('hosted')} className="flex cursor-pointer items-start gap-3 p-3.5">
                <RadioGroupItem id="welcome-run-hosted" value="hosted" aria-labelledby="welcome-title-hosted" className="mt-[3px] border-muted-foreground/50 data-[checked]:border-primary" />
                <span className="min-w-0 flex-1 text-left">
                  <span className="flex flex-wrap items-center gap-2">
                    <span id="welcome-title-hosted" className="text-[15px] font-medium text-foreground">Use it at astrid.haus</span>
                    <span className="rounded-full bg-muted px-2 py-px text-[11px] text-muted-foreground">Most convenient</span>
                  </span>
                  <span className="mt-1 block text-[13px] leading-5 text-muted-foreground">The editor stays up to date and connects to Astrid on your computer, where your files, models and agent run.</span>
                </span>
              </label>
              {runMode === 'hosted' && canInstall && <div className="space-y-2 px-3.5 pb-3.5 pl-[43px]">
                <SegmentedControl value={windowMode} onValueChange={value => setWindowMode(value as WindowMode)} size="sm" aria-label="How to open Astrid">
                  <SegmentedControlItem value="app-window">Install as app</SegmentedControlItem>
                  <SegmentedControlItem value="browser-tab">Stay in browser</SegmentedControlItem>
                </SegmentedControl>
                <p className="text-[13px] leading-5 text-muted-foreground">{windowMode === 'app-window' ? "Its own window and a Dock or taskbar icon. Nothing to download; it's still astrid.haus." : 'Keep using it in this tab.'}</p>
              </div>}
              {runMode === 'hosted' && installUnavailable && <p className="px-3.5 pb-3.5 pl-[43px] text-[13px] leading-5 text-muted-foreground">Not installed. You can install it any time from the install icon in the address bar.</p>}
              {runMode === 'hosted' && scenario === 'unsupported' && <p className="px-3.5 pb-3.5 pl-[43px] text-[13px] text-muted-foreground">Needs Chrome or Edge to reach your computer.</p>}
            </div>
            <div className={`rounded-xl border transition-colors ${runMode === 'local' ? 'border-primary/70 bg-primary/[0.06]' : 'border-border hover:border-foreground/25 hover:bg-muted/40'}`}>
              <label htmlFor="welcome-run-local" onClick={() => setRunMode('local')} className="flex cursor-pointer items-start gap-3 p-3.5">
                <RadioGroupItem id="welcome-run-local" value="local" aria-labelledby="welcome-title-local" className="mt-[3px] border-muted-foreground/50 data-[checked]:border-primary" />
                <span className="min-w-0 flex-1 text-left">
                  <span className="flex flex-wrap items-center gap-2">
                    <span id="welcome-title-local" className="text-[15px] font-medium text-foreground">Run everything on your computer</span>
                    <span className="rounded-full bg-muted px-2 py-px text-[11px] text-muted-foreground">Most control</span>
                  </span>
                  <span className="mt-1 block text-[13px] leading-5 text-muted-foreground">The editor runs on your machine too: no browser permission, works offline, and you can change Astrid itself. GitHub <a className="underline underline-offset-4 hover:text-foreground" href={LOCAL_SETUP.repoUrl} target="_blank" rel="noreferrer">here</a>.</span>
                </span>
              </label>
            </div>
          </RadioGroup>
          <Button type="button" className="h-11 w-full rounded-xl" onClick={() => {
            if (runMode === 'local') onContinue('local');
            else if (scenario === 'unsupported') void copyForChromium();
            else if (canInstall && windowMode === 'app-window') void installApp();
            else continueHere();
          }}>{runMode === 'hosted' && scenario === 'unsupported' ? copied ? 'Copied. Open it in Chrome or Edge.' : 'Copy link for Chrome or Edge' : buttonLabel}</Button>
        </div>
      </EditorCard>
    </EditorCardLayer>
  </main>;
}
