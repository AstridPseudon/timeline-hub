import { RefreshCw } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card.tsx';
import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { RUNTIME_CONNECTION_COPY as COPY } from '@/shared/components/RuntimeConnection/copy.ts';
import { useOnAstridAnswers } from '@/shared/components/RuntimeConnection/useRuntimeRestartWatch.ts';

/**
 * Takes the timeline region's place when the timeline failed to load. A load
 * failure happens before the first render, so no error boundary can catch it —
 * this is the only thing standing between a malformed backend payload and a
 * blank editor whose badge claims `saved`.
 *
 * On the hosted build (a gateway origin is configured) the failure is almost
 * always "Astrid is not answering", and the raw message names the Runtime, the
 * workspace and the loopback address. A person gets the connection cards' frame
 * and one friendly line instead, never the message, and the load is tried again
 * by itself as soon as Astrid answers.
 */
export function TimelineLoadErrorCard({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  return runtimeOrigin() !== '' ? <HostedLoadErrorCard onRetry={onRetry} /> : <LoadErrorCard message={message} onRetry={onRetry} />;
}

/** The connection panel's frame (RuntimeConnectionPanel's PanelFrame): centred, a serif heading, one filled primary button. */
function HostedLoadErrorCard({ onRetry }: { onRetry: () => void }) {
  useOnAstridAnswers(onRetry);
  return (
    <div className="flex h-full min-h-0 items-center justify-center overflow-auto p-4">
      <section role="alert" className="w-full max-w-md space-y-5 rounded-2xl border border-border bg-card p-6 text-center text-card-foreground sm:p-8">
        <div className="space-y-3">
          <h2 className="text-balance font-serif font-theme-heading text-2xl leading-tight text-foreground">{COPY.loadFailed.title}</h2>
          <p className="text-balance text-base leading-7 text-muted-foreground">{COPY.loadFailed.sentence}</p>
        </div>
        <div className="flex flex-col items-center">
          <Button type="button" className="w-full sm:w-auto" onClick={onRetry}>{COPY.loadFailed.button}</Button>
        </div>
      </section>
    </div>
  );
}

function LoadErrorCard({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="flex h-full min-h-0 items-center justify-center overflow-auto p-4">
      <Card className="w-full max-w-md" role="alert">
        <CardHeader>
          <CardTitle className="text-base">Unable to load this timeline</CardTitle>
          <CardDescription>{message}</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            The editor kept its toolbar so you can switch timelines, but there is
            nothing to edit until the timeline loads.
          </p>
          <Button
            type="button"
            size="sm"
            variant="outline"
            className="mt-3 gap-1.5"
            onClick={onRetry}
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Retry
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
