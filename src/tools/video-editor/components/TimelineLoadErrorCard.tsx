import { RefreshCw } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card.tsx';
import { runtimeOrigin } from '@/integrations/runtime/connection.ts';
import { RUNTIME_CONNECTION_COPY as COPY } from '@/shared/components/RuntimeConnection/copy.ts';

/**
 * Takes the timeline region's place when the timeline failed to load. A load
 * failure happens before the first render, so no error boundary can catch it —
 * this is the only thing standing between a malformed backend payload and a
 * blank editor whose badge claims `saved`.
 *
 * On the hosted build (a gateway origin is configured) the failure is almost
 * always "Astrid is not answering", and the raw message names the Runtime, the
 * workspace and the loopback address. A person gets one friendly line instead,
 * and never the message.
 */
export function TimelineLoadErrorCard({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  const hosted = runtimeOrigin() !== '';
  return (
    <div className="flex h-full min-h-0 items-center justify-center overflow-auto p-4">
      <Card className="w-full max-w-md" role="alert">
        <CardHeader>
          <CardTitle className="text-base">{hosted ? COPY.loadFailed.title : 'Unable to load this timeline'}</CardTitle>
          <CardDescription>{hosted ? COPY.loadFailed.sentence : message}</CardDescription>
        </CardHeader>
        <CardContent>
          {hosted ? null : (
            <p className="text-sm text-muted-foreground">
              The editor kept its toolbar so you can switch timelines, but there is
              nothing to edit until the timeline loads.
            </p>
          )}
          <Button
            type="button"
            size="sm"
            variant="outline"
            className="mt-3 gap-1.5"
            onClick={onRetry}
          >
            <RefreshCw className="h-3.5 w-3.5" />
            {hosted ? COPY.loadFailed.button : 'Retry'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
