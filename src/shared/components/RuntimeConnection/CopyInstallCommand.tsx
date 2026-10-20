import { useEffect, useRef, useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';
import { installCommand, RUNTIME_CONNECTION_COPY, terminalOpeningHint, type CommandMode } from './copy.ts';

export interface CopyInstallCommandProps {
  /** `install` for setup/repair and `update` for an incompatible Runtime. */
  readonly mode?: CommandMode;
  readonly label: string;
}

type CopyStatus = 'idle' | 'copied' | 'failed';

/** How long the button reads "Copied" before it goes back to its label. */
const COPIED_MS = 2000;

/**
 * The state's command is visible and can be copied or pasted into a coding agent. On clipboard failure it appears in
 * a selectable box. It does not use `useCopyToClipboard`:
 * that hook never learns whether the write worked, and a failed copy must show the text to select by hand, not a false
 * "Copied".
 */
export function CopyInstallCommand({ mode = 'install', label }: CopyInstallCommandProps) {
  const copy = RUNTIME_CONNECTION_COPY.agent;
  const instructions = installCommand(mode);
  const [status, setStatus] = useState<CopyStatus>('idle');
  const fieldRef = useRef<HTMLTextAreaElement>(null);
  const resetRef = useRef<number | null>(null);

  useEffect(() => () => {
    if (resetRef.current !== null) window.clearTimeout(resetRef.current);
  }, []);

  // A failed copy leaves the text to copy by hand, so it is selected for the person.
  useEffect(() => {
    if (status === 'failed') fieldRef.current?.select();
  }, [status]);

  const handleCopy = async () => {
    const copied = await writeClipboardTextSafe(instructions);
    if (resetRef.current !== null) window.clearTimeout(resetRef.current);
    setStatus(copied ? 'copied' : 'failed');
    resetRef.current = copied
      ? window.setTimeout(() => {
        resetRef.current = null;
        setStatus('idle');
      }, COPIED_MS)
      : null;
  };

  return (
    <div className="w-full space-y-3">
      <pre className="overflow-x-auto rounded-md border border-border bg-background p-3 text-left text-xs leading-5 text-foreground"><code>{instructions}</code></pre>
      <Button type="button" className="w-full sm:w-auto" onClick={() => void handleCopy()}>
        {status === 'copied'
          ? <Check aria-hidden="true" className="mr-2 h-4 w-4" />
          : <Copy aria-hidden="true" className="mr-2 h-4 w-4" />}
        {status === 'copied' ? copy.copied : label}
      </Button>
      <p className="text-xs text-muted-foreground">{terminalOpeningHint()}</p>
      <p className="text-xs text-muted-foreground">{copy.note}</p>
      {status === 'failed' && (
        <div className="space-y-2">
          <p role="status" className="text-sm text-muted-foreground">{copy.copyFailed}</p>
          <textarea
            ref={fieldRef}
            readOnly
            rows={6}
            value={instructions}
            aria-label={copy.copyFailed}
            onFocus={(event) => event.currentTarget.select()}
            className="w-full resize-y rounded-md border border-border bg-background p-2 text-left text-xs leading-5 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
      )}
    </div>
  );
}
