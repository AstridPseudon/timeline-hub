import { useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import type { TimelineCommandSessionSurface } from '../hooks/useTimelineCommandSession.ts';

type TimelineConflictLocation = {
  ref: string;
  path: readonly string[];
};

type TimelineCommandRecoveryState = TimelineCommandSessionSurface['state'] & {
  canDiscardRejected?: boolean;
  canReapplyLabel?: boolean;
  conflicts?: readonly TimelineConflictLocation[];
};

/** The command core adds these capabilities when a rejection is definitively resolvable. */
export type TimelineCommandRecoverySession = Omit<TimelineCommandSessionSurface, 'state'> & {
  state: TimelineCommandRecoveryState;
  useLatest?: () => Promise<void>;
  keepLabelChanges?: () => Promise<void>;
};

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

function readableRef(value: string): string | null {
  const ref = value.trim();
  if (ref.length === 0 || ref.length > 120 || !/^[A-Za-z0-9][A-Za-z0-9_./:-]*$/.test(ref)) return null;
  const parts = ref.split(/[/:.]/);
  return parts.every((part) => part.length > 0 && !part.startsWith('__')) ? ref : null;
}

function readablePath(path: readonly string[]): string | null {
  const fields = path.map((field) => field.trim());
  if (fields.length === 0 || fields.length > 12 || fields.some((field) => (
    field.length === 0 || field.length > 64 || !/^[A-Za-z][A-Za-z0-9_-]*$/.test(field) || field.startsWith('__')
  ))) return null;
  return fields.join('.');
}

function readableConflictLocation(conflict: TimelineConflictLocation): string | null {
  const ref = readableRef(conflict.ref);
  if (!ref) return null;
  const path = readablePath(conflict.path);
  return `Changed target: ${ref}${path ? ` · Property: ${path}` : ' · Target itself changed'}`;
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
  const canKeepLabelChanges = isConflict && state.canReapplyLabel === true && !!commandSession.keepLabelChanges;
  const canUseLatest = isConflict && state.canDiscardRejected === true && !!commandSession.useLatest;
  const conflictLocations = isConflict && !hasRecoveryChoices
    ? (state.conflicts ?? []).map(readableConflictLocation).filter((location): location is string => location !== null)
    : [];
  const unavailableResolution = isConflict && !hasRecoveryChoices
    ? !canKeepLabelChanges && !canUseLatest
      ? 'No automatic resolution is available for this conflict yet. Your changes remain here.'
      : !canKeepLabelChanges
        ? 'Keeping these changes is not available for this conflict. Your changes remain here.'
        : !canUseLatest
          ? 'Using the latest version is not available for this conflict. Your changes remain here.'
          : null
    : null;
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
        {conflictLocations.length > 0 && (
          <ul className="mt-1 text-xs text-muted-foreground" aria-label="Changed timeline properties">
            {conflictLocations.map((location) => <li key={location}>{location}</li>)}
          </ul>
        )}
        {unavailableResolution && <p className="mt-1 text-xs text-muted-foreground">{unavailableResolution}</p>}
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
      ) : isConflict && (canKeepLabelChanges || canUseLatest) ? (
        <div className="flex flex-wrap items-center gap-2" aria-label="Conflict resolution actions">
          {canKeepLabelChanges && (
            <Button
              type="button"
              size="sm"
              variant="default"
              data-testid="timeline-command-keep"
              disabled={isBusy}
              aria-busy={busyAction === 'keep'}
              onClick={() => void runAction('keep', commandSession.keepLabelChanges!)}
            >
              {busyAction === 'keep' ? 'Keeping my changes…' : 'Keep my changes'}
            </Button>
          )}
          {canUseLatest && (
            <Button
              type="button"
              size="sm"
              variant="outline"
              data-testid="timeline-command-use-latest"
              disabled={isBusy}
              aria-busy={busyAction === 'use-latest'}
              onClick={() => void runAction('use-latest', commandSession.useLatest!)}
            >
              {busyAction === 'use-latest' ? 'Using latest version…' : 'Use latest version'}
            </Button>
          )}
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
