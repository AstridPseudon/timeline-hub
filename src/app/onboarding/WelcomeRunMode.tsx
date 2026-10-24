import { useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { RadioGroup, RadioGroupItem } from '@/shared/components/ui/radio-group.tsx';
import { SegmentedControl, SegmentedControlItem } from '@/shared/components/ui/segmented-control.tsx';
import { runInstallPrompt, useInstallPromptSignals, useStandaloneStatus } from '@/shared/hooks/platformInstall/signals.ts';
import { detectInstallScenario } from '@/pages/Home/installScenario.ts';
import type { WindowMode } from '@/shared/components/RuntimeConnection/copy.ts';
import { EditorCard } from '@/shared/components/RuntimeConnection/EditorCard.tsx';
import { EditorCardLayer } from '@/shared/components/RuntimeConnection/EditorCardLayer.tsx';
import { writeWelcomePhase } from './welcomeProgress.ts';

export type { WindowMode };
export type RunMode = 'hosted' | 'local';

interface Props {
  readonly onContinue: (phase: 'connection' | 'local') => void;
  readonly windowMode: WindowMode;
  readonly setWindowMode: (mode: WindowMode) => void;
  readonly runMode: RunMode;
  readonly setRunMode: (mode: RunMode) => void;
}

const ASTRID_REPO = 'https://github.com/banodoco/astrid-app';

export function WelcomeRunMode({ onContinue, windowMode, setWindowMode, runMode, setRunMode }: Props) {
  const { deferredPrompt, consumeDeferredPrompt } = useInstallPromptSignals();
  const standalone = useStandaloneStatus();
  const scenario = detectInstallScenario();
  const canInstall = !standalone && scenario === 'chromium' && deferredPrompt !== null;
  const [opened, setOpened] = useState(false);
  const [copied, setCopied] = useState(false);

  const continueHere = () => onContinue('connection');
  const copyForChromium = async () => {
    await navigator.clipboard.writeText(window.location.href);
    setCopied(true);
  };
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

  if (opened) return <main aria-label="Astrid opened in its own window">
    <EditorCardLayer cardKey="opened">
      <EditorCard title="Astrid opened in its own window" sentence="Carry on there. You can close this tab.">
        <a href="#continue" className="text-[13px] text-muted-foreground underline underline-offset-4 hover:text-foreground" onClick={event => { event.preventDefault(); continueHere(); }}>Continue here instead</a>
      </EditorCard>
    </EditorCardLayer>
  </main>;

  const buttonLabel = runMode === 'local'
    ? 'Set up with your agent'
    : canInstall && windowMode === 'app-window'
      ? 'Install app and continue'
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
              {runMode === 'hosted' && canInstall && <div className="flex items-center gap-2.5 px-3.5 pb-3.5 pl-[43px]">
                <span className="text-[13px] text-muted-foreground">Open in</span>
                <SegmentedControl value={windowMode} onValueChange={value => setWindowMode(value as WindowMode)} size="sm" aria-label="Open in">
                  <SegmentedControlItem value="app-window">App window</SegmentedControlItem>
                  <SegmentedControlItem value="browser-tab">Browser tab</SegmentedControlItem>
                </SegmentedControl>
              </div>}
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
                  <span className="mt-1 block text-[13px] leading-5 text-muted-foreground">The editor runs on your machine too: no browser permission, works offline, and you can change Astrid itself. Your agent sets it up from <a className="underline underline-offset-4 hover:text-foreground" href={ASTRID_REPO} target="_blank" rel="noreferrer">github.com/banodoco/astrid-app</a>.</span>
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
