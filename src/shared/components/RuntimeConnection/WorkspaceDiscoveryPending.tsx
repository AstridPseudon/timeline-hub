import { useState } from 'react';
import { useRuntimeRequestWait } from '@/integrations/runtime/useRuntimeRequestWait.ts';
import { Button } from '@/shared/components/ui/button.tsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card.tsx';

/** Release the boot layer when discovery needs the person's attention, even if no request settles. */
export function WorkspaceDiscoveryPending({ onRetry, onOpenEditor, waitedAlready = false }: {
  /** The caller already held its own loading screen for the deadline. */
  waitedAlready?: boolean;
  onRetry: () => void;
  onOpenEditor?: () => void;
}) {
  const [attempt, setAttempt] = useState(0);
  const stillWaiting = useRuntimeRequestWait(true, attempt) || (waitedAlready && attempt === 0);
  return <div className="flex flex-1 items-center justify-center px-6">
    {!stillWaiting && <span data-boot-hold="" hidden />}
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>{stillWaiting ? 'Still waiting for your workspace' : 'Opening your workspace…'}</CardTitle>
        <CardDescription role="status">{stillWaiting
          ? 'Astrid is taking longer than usual to answer. You can keep waiting or retry.'
          : 'Astrid is looking for your projects on this computer.'}</CardDescription>
      </CardHeader>
      {stillWaiting && <CardContent className="flex flex-wrap gap-3">
        <Button onClick={() => { setAttempt(value => value + 1); onRetry(); }}>Retry workspace discovery</Button>
        {onOpenEditor && <Button variant="outline" onClick={onOpenEditor}>Open editor</Button>}
      </CardContent>}
    </Card>
  </div>;
}
