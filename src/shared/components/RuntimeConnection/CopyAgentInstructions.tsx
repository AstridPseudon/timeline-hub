import { useState } from 'react';
import { Check, ChevronDown, Copy } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/shared/components/ui/collapsible.tsx';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';
import { RUNTIME_CONNECTION_COPY } from './copy.ts';

export interface CopyAgentInstructionsProps {
  /** The origin the gateway must accept; the instructions name it. */
  readonly pageOrigin: string;
}

type CopyStatus = 'idle' | 'copied' | 'failed';

/**
 * The "Copy instructions for your agent" control every not-connected panel shows. It does not use
 * `useCopyToClipboard`: that hook never learns whether the write worked, and a failed copy must show the text to
 * select by hand, not a false "Copied".
 */
export function CopyAgentInstructions({ pageOrigin }: CopyAgentInstructionsProps) {
  const copy = RUNTIME_CONNECTION_COPY.agent;
  const instructions = copy.instructions(pageOrigin);
  const [status, setStatus] = useState<CopyStatus>('idle');
  const [disclosed, setDisclosed] = useState(false);
  // A failed copy shows the text to select by hand, whether or not the person opened it.
  const showField = disclosed || status === 'failed';

  const handleCopy = async () => {
    const copied = await writeClipboardTextSafe(instructions);
    setStatus(copied ? 'copied' : 'failed');
  };

  return (
    <div className="space-y-2">
      <Button type="button" className="w-full sm:w-auto" onClick={() => void handleCopy()}>
        {status === 'copied'
          ? <Check aria-hidden="true" className="mr-2 h-4 w-4" />
          : <Copy aria-hidden="true" className="mr-2 h-4 w-4" />}
        {copy.copy}
      </Button>
      {status === 'copied' && <p role="status" className="text-xs text-muted-foreground">{copy.copied}</p>}
      {status === 'failed' && <p role="status" className="text-xs text-muted-foreground">{copy.copyFailed}</p>}
      <Collapsible open={showField} onOpenChange={setDisclosed}>
        <CollapsibleTrigger className="flex items-center gap-1 rounded text-xs font-medium text-muted-foreground underline-offset-2 hover:text-foreground hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
          <ChevronDown aria-hidden="true" className={`h-3 w-3 transition-transform ${showField ? 'rotate-180' : ''}`} />
          {showField ? copy.hideInstructions : copy.showInstructions}
        </CollapsibleTrigger>
        <CollapsibleContent className="space-y-1 pt-2">
          <label htmlFor="runtime-connection-agent-instructions" className="block text-xs font-medium text-foreground">{copy.fieldLabel}</label>
          <textarea
            id="runtime-connection-agent-instructions"
            readOnly
            rows={8}
            value={instructions}
            onFocus={(event) => event.currentTarget.select()}
            className="w-full resize-y rounded-md border border-border bg-background p-2 text-xs leading-5 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </CollapsibleContent>
      </Collapsible>
    </div>
  );
}
