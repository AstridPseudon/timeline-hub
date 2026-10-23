export type ReadonlyOutboxRead<T> =
  | { status: 'verified'; value: T }
  | { status: 'unknown'; reason: 'unavailable' | 'read-rejected' };

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
