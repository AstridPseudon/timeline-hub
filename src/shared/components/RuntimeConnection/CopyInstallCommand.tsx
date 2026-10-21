import { useEffect, useRef, useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';
import { agentInstructions, installCommand, RUNTIME_CONNECTION_COPY, terminalOpeningHint, withCommandShell, type CommandMode } from './copy.ts';

export interface CopyInstallCommandProps {
  /** `install` for setup/repair and `update` for an incompatible Astrid. */
  readonly mode?: CommandMode;
}

type CopyStatus = 'idle' | 'copied' | 'failed';
const COPIED_MS = 2000;

/** Each action owns its feedback so copying a command cannot claim the agent brief was copied. */
function useCopyAction(text: string) {
  const [status, setStatus] = useState<CopyStatus>('idle');
  const resetRef = useRef<number | null>(null);
  useEffect(() => () => {
    if (resetRef.current !== null) window.clearTimeout(resetRef.current);
  }, []);
  const copy = async () => {
    const copied = await writeClipboardTextSafe(text);
    if (resetRef.current !== null) window.clearTimeout(resetRef.current);
    setStatus(copied ? 'copied' : 'failed');
    resetRef.current = copied ? window.setTimeout(() => {
      resetRef.current = null;
      setStatus('idle');
    }, COPIED_MS) : null;
  };
  return { status, copy };
}

function CopyFallback({ text, label }: { text: string; label: string }) {
  const fieldRef = useRef<HTMLTextAreaElement>(null);
  useEffect(() => { fieldRef.current?.select(); }, [text]);
  return (
    <div className="space-y-2">
      <p role="status" className="text-sm text-muted-foreground">{RUNTIME_CONNECTION_COPY.agent.copyFailed}</p>
      <textarea
        ref={fieldRef}
        readOnly
        rows={6}
        value={text}
        aria-label={label}
        onFocus={(event) => event.currentTarget.select()}
        className="w-full resize-y rounded-md border border-border bg-background p-2 text-left text-xs leading-5 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      />
    </div>
  );
}

/** Agent handoff first; the manual command has a separate copy action beside it. */
export function CopyInstallCommand({ mode = 'install' }: CopyInstallCommandProps) {
  const copy = RUNTIME_CONNECTION_COPY.agent;
  const instructions = agentInstructions(mode, window.location.origin);
  const command = installCommand(mode);
  const agentCopy = useCopyAction(instructions);
  const commandCopy = useCopyAction(command);

  return (
    <div className="w-full space-y-4">
      <div className="space-y-2">
        <Button type="button" className="w-full sm:w-auto" onClick={() => void agentCopy.copy()}>
          {agentCopy.status === 'copied'
            ? <Check aria-hidden="true" className="mr-2 h-4 w-4" />
            : <Copy aria-hidden="true" className="mr-2 h-4 w-4" />}
          {agentCopy.status === 'copied' ? copy.copied : copy.copy}
        </Button>
        <p role={agentCopy.status === 'copied' ? 'status' : undefined} className="text-xs text-muted-foreground">
          {agentCopy.status === 'copied' ? copy.pasteNext : copy.note}
        </p>
        {agentCopy.status === 'failed' && <CopyFallback text={instructions} label={copy.copyFailed} />}
      </div>
      <div className="space-y-2 text-left">
        <p className="text-xs text-muted-foreground">{withCommandShell(copy.terminalAlternative)}</p>
        <div className="flex min-w-0 items-center gap-2 rounded-md border border-border bg-background p-2">
          <pre className="min-w-0 flex-1 whitespace-pre-wrap break-all text-xs leading-5 text-foreground"><code>{command}</code></pre>
          <Button type="button" variant="ghost" size="icon" className="shrink-0" aria-label={commandCopy.status === 'copied' ? copy.commandCopied : copy.commandCopy} title={copy.commandCopy} onClick={() => void commandCopy.copy()}>
            {commandCopy.status === 'copied' ? <Check aria-hidden="true" className="h-4 w-4" /> : <Copy aria-hidden="true" className="h-4 w-4" />}
          </Button>
        </div>
        <p className="text-xs text-muted-foreground">{terminalOpeningHint()}</p>
        {commandCopy.status === 'failed' && <CopyFallback text={command} label={copy.commandCopy} />}
      </div>
    </div>
  );
}
