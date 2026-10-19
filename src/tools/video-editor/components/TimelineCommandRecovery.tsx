import { useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import type { TimelineCommandSessionSurface } from '@/tools/video-editor/hooks/useTimelineCommandSession.ts';

export interface TimelineCommandRecoveryProps {
  commandSession?: TimelineCommandSessionSurface;
}

function actionErrorMessage(error: unknown): string {
  if (error instanceof Error && error.message) return error.message;
  if (typeof error === 'string' && error) return error;
  return 'The recovery action could not finish.';
}

export function TimelineCommandRecovery({ commandSession }: TimelineCommandRecoveryProps) {
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  if (!commandSession) return null;

  const { state } = commandSession;
  const recoverableOwners = state.recoverableOwners;
  const hasRecoveryChoices = recoverableOwners.length > 0;
  if (state.status === 'saved' || (state.status === 'loading' && !hasRecoveryChoices)) return null;

  const isConflict = state.status === 'conflict';
  const isRetry = state.status === 'retry';
  const canRetry = state.status === 'retry' || state.status === 'error';
  const isBusy = busyAction !== null;
  const message = hasRecoveryChoices
    ? 'Saved edits from another editor session are available. Choose which session to recover.'
    : isConflict
      ? 'Your saved edits conflict with another change and are retained for resolution.'
      : state.status === 'retry'
        ? 'The save result is uncertain. Retry save to check it without applying edits again.'
        : state.status === 'error'
          ? state.ownerId
            ? 'Your saved edits could not be completed.'
            : 'Editing is unavailable right now.'
          : state.status === 'saving'
            ? 'Your timeline changes are being saved.'
            : state.status === 'dirty'
              ? 'Your timeline changes are still unsaved.'
              : 'Your timeline editing session is starting.';
  const stateError = state.error && !hasRecoveryChoices ? state.error : null;

  const runAction = async (actionId: string, action: () => Promise<void>) => {
    setBusyAction(actionId);
    setActionError(null);
    try {
      await action();
    } catch (error) {
      setActionError(actionErrorMessage(error));
    } finally {
      setBusyAction(null);
    }
  };

  const urgent = hasRecoveryChoices || isRetry || isConflict || state.status === 'error';
  return (
    <div
      role={urgent ? 'alert' : 'status'}
      aria-live={urgent ? 'assertive' : 'polite'}
      aria-atomic="true"
      aria-busy={isBusy}
      className={cn(
        'flex flex-wrap items-center justify-between gap-3 border-b px-3 py-2 text-sm',
        isConflict ? 'border-amber-500/40 bg-amber-500/10' : 'border-border bg-muted/40',
      )}
      data-testid="timeline-command-recovery"
    >
      <div className="min-w-0">
        <p>{message}</p>
        {stateError && <p className="mt-1 text-xs text-muted-foreground">Details: {stateError}</p>}
        {actionError && <p className="mt-1 text-xs text-destructive">Details: {actionError}</p>}
      </div>
      {hasRecoveryChoices ? (
        <div className="flex flex-wrap items-center gap-2" aria-label="Saved edit sessions">
          {recoverableOwners.map((ownerId, index) => {
            const actionId = `recover-${index}`;
            return (
              <Button
                key={`${ownerId}-${index}`}
                type="button"
                size="sm"
                variant="outline"
                data-owner-id={ownerId}
                disabled={isBusy}
                aria-busy={busyAction === actionId}
                onClick={() => void runAction(actionId, () => commandSession.recover(ownerId))}
              >
                {busyAction === actionId ? 'Recovering saved edits…' : `Recover saved edits${recoverableOwners.length > 1 ? ` (session ${index + 1})` : ''}`}
              </Button>
            );
          })}
        </div>
      ) : canRetry ? (
        <Button
          type="button"
          size="sm"
          variant="outline"
          data-testid="timeline-command-retry"
          disabled={isBusy}
          aria-busy={busyAction === 'retry'}
          onClick={() => void runAction('retry', commandSession.retry)}
        >
          {busyAction === 'retry' ? 'Retrying save…' : 'Retry save'}
        </Button>
      ) : null}
    </div>
  );
}
