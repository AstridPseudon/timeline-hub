import { useEffect, useRef, useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';
import { RUNTIME_CONNECTION_COPY, type AgentInstructionsVariant } from './copy.ts';

export interface CopyAgentInstructionsProps {
  /** The origin the gateway must accept; the instructions name it. */
  readonly pageOrigin: string;
  /** The state's button label: `agent.copySetup` for set up, `agent.copy` for the rest. */
  readonly label: string;
  /** `setup` finds an install first; `start` is for an existing install. */
  readonly variant?: AgentInstructionsVariant;
}

type CopyStatus = 'idle' | 'copied' | 'failed';

/** How long the button reads "Copied" before it goes back to its label. */
const COPIED_MS = 2000;

/**
 * The state's one primary action: copy the steps for the person's agent. A person never needs to read them, so the
 * text is shown only when the clipboard write fails (in a box, already selected). It does not use `useCopyToClipboard`:
 * that hook never learns whether the write worked, and a failed copy must show the text to select by hand, not a false
 * "Copied".
 */
export function CopyAgentInstructions({ pageOrigin, label, variant = 'start' }: CopyAgentInstructionsProps) {
  const copy = RUNTIME_CONNECTION_COPY.agent;
  const instructions = copy.instructions(pageOrigin, variant);
  const [status, setStatus] = useState<CopyStatus>('idle');
  const [showPasteNext, setShowPasteNext] = useState(false);
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
    if (copied) setShowPasteNext(true);
    resetRef.current = copied
      ? window.setTimeout(() => {
        resetRef.current = null;
        setStatus('idle');
      }, COPIED_MS)
      : null;
  };

  return (
    <div className="w-full space-y-3">
      <Button type="button" className="w-full sm:w-auto" onClick={() => void handleCopy()}>
        {status === 'copied'
          ? <Check aria-hidden="true" className="mr-2 h-4 w-4" />
          : <Copy aria-hidden="true" className="mr-2 h-4 w-4" />}
        {status === 'copied' ? copy.copied : label}
      </Button>
      {showPasteNext && <p role="status" className="text-sm text-muted-foreground">{copy.pasteNext}</p>}
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
