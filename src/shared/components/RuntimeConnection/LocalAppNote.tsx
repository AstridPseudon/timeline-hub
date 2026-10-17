import { runtimeAppUrl } from '@/integrations/runtime/runtimeAppUrl.ts';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { RUNTIME_CONNECTION_COPY as COPY } from './copy.ts';

/**
 * The line next to a control the hosted build disables (making images, agent chat): what works only in the local Astrid
 * app, then "Open it" linking there. The link is the address the gateway reported (`gatewayHealth.ts`); when it reported
 * none, there is no link. The text never shows the address.
 */
export function LocalAppNote({ message, className }: { message: string; className?: string }) {
  const appUrl = runtimeAppUrl();
  return (
    <p role="note" className={cn('text-muted-foreground', className)}>
      {message}
      {appUrl && (
        <>
          {' '}
          <a href={appUrl} target="_blank" rel="noreferrer" className="text-foreground underline underline-offset-2">{COPY.openApp}</a>
        </>
      )}
    </p>
  );
}
