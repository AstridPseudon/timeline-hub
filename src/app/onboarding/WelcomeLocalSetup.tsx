import { ChevronLeft, Check, Copy } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { CardDisclosure, EditorCard, EditorCardFoot } from '@/shared/components/RuntimeConnection/EditorCard.tsx';
import { EditorCardLayer } from '@/shared/components/RuntimeConnection/EditorCardLayer.tsx';
import { LOCAL_SETUP, RUNTIME_CONNECTION_COPY, localSetupInstructions, localSetupSteps } from '@/shared/components/RuntimeConnection/copy.ts';
import { CopyCommandRow, CopyFallback, useCopyAction } from '@/shared/components/RuntimeConnection/CopyInstallCommand.tsx';

export function WelcomeLocalSetup({ onBack }: { readonly onBack: () => void }) {
  const instructions = localSetupInstructions();
  const steps = localSetupSteps();
  const copy = useCopyAction(instructions);
  const copied = copy.status === 'copied';

  return <main aria-label="Set up Astrid with your agent">
    <EditorCardLayer cardKey="local">
      <EditorCard
        scrollContent
        title="Have your agent set it up"
        sentence={<>Paste these instructions into Claude Code, Codex or another agent. It installs Astrid, gets the editor from <a className="underline underline-offset-4 hover:text-foreground" href={LOCAL_SETUP.repoUrl} target="_blank" rel="noreferrer">github.com/banodoco/astrid-app</a> and starts both on your computer.</>}
        topLeft={<Button type="button" variant="ghost" className="inline-flex h-auto items-center gap-0.5 rounded-md py-1 pl-1 pr-2 text-[13px] text-muted-foreground hover:bg-muted/60 hover:text-foreground" onClick={onBack}><ChevronLeft aria-hidden="true" className="h-4 w-4" />Back</Button>}
        foot={<EditorCardFoot>When it&apos;s done, Astrid opens from your own computer.</EditorCardFoot>}
      >
        <div className="space-y-2">
          <Button type="button" className="h-11 w-full justify-between rounded-xl px-4 text-sm" onClick={() => void copy.copy()}>
            <span aria-live="polite">{copied ? RUNTIME_CONNECTION_COPY.agent.copied : RUNTIME_CONNECTION_COPY.agent.copy}</span>
            {copied ? <Check aria-hidden="true" className="h-4 w-4" /> : <Copy aria-hidden="true" className="h-4 w-4" />}
          </Button>
          {copy.status === 'failed' && <CopyFallback text={instructions} label={RUNTIME_CONNECTION_COPY.agent.copy} />}
        </div>
        <CardDisclosure label="Show the instructions" openLabel="Hide the instructions">
          <pre className="max-h-[220px] overflow-y-auto whitespace-pre-wrap font-mono text-xs leading-5 text-foreground">{instructions}</pre>
        </CardDisclosure>
        <section className="min-w-0 space-y-1.5 text-left">
          <p className="text-[13px] font-medium text-muted-foreground">Or do it yourself</p>
          <ol className="min-w-0 list-decimal space-y-1.5 pl-5 text-[13px] leading-5 text-muted-foreground marker:text-muted-foreground">
            {steps.map((step, stepIndex) => <li key={stepIndex} className="min-w-0">
              <div className="min-w-0 break-words">
                {step.line}
              </div>
              {step.command && <div className="mt-1 space-y-1">
                <CopyCommandRow
                  command={step.command}
                  label={step.commandLabel ?? 'Copy command'}
                />
                {step.hint && <p className="text-xs leading-4 text-muted-foreground">{step.hint}</p>}
              </div>}
            </li>)}
          </ol>
          <p className="text-[13px] leading-5 text-muted-foreground">Ctrl+C stops it. To start again, run npm run dev:local in the astrid-app folder.</p>
        </section>
      </EditorCard>
    </EditorCardLayer>
  </main>;
}
