import { useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import type { TimelineCommandSessionSurface } from '../hooks/useTimelineCommandSession.ts';

export type TimelineCommandRecoverySession = TimelineCommandSessionSurface;

export interface TimelineCommandRecoveryProps {
  commandSession?: TimelineCommandRecoverySession;
}

function readableError(error: string | null): string | null {
  if (!error) return null;
  const normalized = error.toLowerCase();

  if (/head_busy|\b503\b|transport|network|timed out|timeout|unknown/.test(normalized)) {
    return 'The save result is uncertain. Your changes are still here.';
  }
  if (/lock|claim|outbox|storage|indexeddb|database|persist/.test(normalized)) {
    return 'Your unsaved changes are still here, but this browser could not safely hold the recovery session.';
  }
  if (/credential|authori[sz]|forbidden/.test(normalized)) {
    return 'Your unsaved changes are still here, but this editor is not authorized to save them yet.';
  }

  return null;
}

function actionErrorMessage(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return readableError(message) ?? 'The recovery action could not finish. Your unsaved changes are still here.';
}

function conflictLocation(ref: string, path: string[]): string {
  const scoped = /^(parent|occurrence:([^/]+))\/(clip|track):([^/]+)$/.exec(ref);
  const target = scoped
    ? `${scoped[3] === 'clip' ? 'Clip' : 'Track'} ${scoped[4]} (${scoped[1] === 'parent' ? 'timeline' : `occurrence ${scoped[2]}`})`
    : `Target ${ref}`;
  const labels = new Map([['at', 'Start time'], ['track', 'Track'], ['label', 'Name'], ['name', 'Name']]);
  const property = path.length === 0
    ? 'Target itself changed'
    : (path.length === 1 ? labels.get(path[0]) : undefined) ?? `Field ${path.join(' → ')}`;
  return `${target} · ${property}`;
}

export function TimelineCommandRecovery({ commandSession }: TimelineCommandRecoveryProps) {
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  if (!commandSession) return null;

  const { state } = commandSession;
  const recoverableOwners = state.recoverableOwners;
  const hasRecoveryChoices = recoverableOwners.length > 0;
  if (state.status === 'saved' || state.status === 'loading' && !hasRecoveryChoices) return null;

  const isConflict = state.status === 'conflict';
  const isRetry = state.status === 'retry';
  const hasRetainedWork = Boolean(state.ownerId || state.canUndo || hasRecoveryChoices);
  const isBusy = busyAction !== null;
  const stateError = readableError(state.error);
  const message = hasRecoveryChoices
    ? 'Saved edits from another editor session are available. Choose which session to recover.'
    : isConflict
      ? 'Your changes are retained and need resolution before they can be saved.'
      : isRetry
        ? 'The save result is uncertain. Retry save to check it without creating another edit.'
        : state.status === 'error' && !hasRetainedWork
          ? 'Saving is unavailable. Retry to try again.'
        : state.status === 'saving'
          ? 'Your timeline changes are being saved.'
          : state.status === 'dirty'
            ? 'Your timeline changes are still unsaved.'
            : stateError ?? 'Your unsaved changes are still here.';

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
        {isConflict && !hasRecoveryChoices && !!state.conflicts?.length && (
          <ul className="mt-1 text-xs text-muted-foreground" aria-label="Changed timeline properties">
            {state.conflicts.map((conflict, index) => (
              <li key={index}>
                {conflictLocation(conflict.ref, conflict.path)}
              </li>
            ))}
          </ul>
        )}
        {stateError && stateError !== message && hasRetainedWork && !hasRecoveryChoices && !isConflict && (
          <p className="mt-1 text-xs text-muted-foreground">{stateError}</p>
        )}
        {actionError && <p className="mt-1 text-xs text-destructive">{actionError}</p>}
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
      ) : isRetry || state.status === 'error' ? (
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
