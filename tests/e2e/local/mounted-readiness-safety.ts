export type ReadonlyOutboxRead<T> =
  | { status: 'verified'; value: T }
  | { status: 'unknown'; reason: 'unavailable' | 'read-rejected' };

export type MountedBootstrapStage = 'context' | 'navigation' | 'connection' | 'selection' | 'outbox-read';

export type MountedBootstrapFailure = {
  stage: MountedBootstrapStage;
  code: 'mounted-bootstrap';
  class: 'mounted-bootstrap';
};

export class MountedBootstrapError extends Error {
  readonly failure: MountedBootstrapFailure;

  constructor(failure: MountedBootstrapFailure, cause: unknown) {
    super(`mounted baseline ${failure.stage} failed`, { cause });
    this.name = 'MountedBootstrapError';
    this.failure = failure;
  }
}

let lastMountedBootstrapFailure: MountedBootstrapFailure | undefined;

export function clearMountedBootstrapFailure(): void {
  lastMountedBootstrapFailure = undefined;
}

export function recordMountedBootstrapFailure(error: unknown): void {
  lastMountedBootstrapFailure = error instanceof MountedBootstrapError ? error.failure : undefined;
}

export function readMountedBootstrapFailure(): MountedBootstrapFailure | undefined {
  return lastMountedBootstrapFailure;
}

export async function readExistingReadonly<T>(
  databaseExists: () => Promise<boolean>,
  readExisting: () => Promise<T>,
): Promise<ReadonlyOutboxRead<T>> {
  try {
    if (!(await databaseExists())) return { status: 'unknown', reason: 'unavailable' };
  } catch {
    return { status: 'unknown', reason: 'unavailable' };
  }
  try {
    return { status: 'verified', value: await readExisting() };
  } catch {
    return { status: 'unknown', reason: 'read-rejected' };
  }
}

export type SettledOwner = { ownerId: string; pending?: unknown; intents: readonly unknown[] };

export function hasFreshSettledOwner(owners: readonly SettledOwner[], previousOwnerIds: ReadonlySet<string>): boolean {
  return owners.some((owner) => !previousOwnerIds.has(owner.ownerId) && !owner.pending && owner.intents.length === 0);
}

export function isFreshlyConnected(summary: { attached: boolean | 'UNKNOWN'; state: string }): boolean {
  return summary.attached === true && summary.state === 'connected';
}
