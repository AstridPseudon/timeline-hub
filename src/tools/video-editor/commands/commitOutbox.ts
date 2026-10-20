// Local persistence only. The Runtime adapter owns wire DTOs and response decoding.
export type OutboxJson = null | boolean | number | string | OutboxJson[] | { [key: string]: OutboxJson };

export interface OutboxScope {
  realmId: string;
  actorId: string;
  projectId: string;
  timelineId: string;
}

export interface OutboxHead {
  revisionId: string;
  publicationId: string;
}

export type OutboxBasis = { head: OutboxHead } | { after: string };

export interface OutboxIntent {
  id: string;
  basis: OutboxBasis;
  // Complete original commands, guards, bindings and allocated IDs, never rebased here.
  payload: OutboxJson;
  readyBase?: OutboxHead;
  conflict?: OutboxJson;
}

export interface OutboxRequest {
  method: string;
  path: string;
  body: string;
  key: string;
}

export type OutboxOutcome =
  | { kind: 'accepted'; head: OutboxHead; value: OutboxJson }
  | { kind: 'rejected'; error: OutboxJson }
  | { kind: 'retry'; error: OutboxJson };

export interface OutboxRecord {
  scope: OutboxScope;
  ownerId: string;
  generation: number;
  intents: OutboxIntent[];
  pending?: { intentId: string; request: OutboxRequest; outcome?: OutboxOutcome };
  // Only the last acknowledged prefix, also usable by a late dependent append.
  accepted?: { intentId: string; head: OutboxHead; value: OutboxJson };
}

export type OutboxExclusiveLock = <T>(name: string, work: () => Promise<T>) => Promise<T>;
// Wrap original payload in the generated request at base; never refresh its guards.
export type OutboxRequestBuilder = (
  intent: OutboxIntent,
  base: OutboxHead,
) => { method: string; path: string; body: OutboxJson };

export interface ClaimedOutbox {
  read(): Promise<OutboxRecord>;
  append(payload: OutboxJson, basis: OutboxBasis): Promise<string>;
  cancel(intentId: string): Promise<void>;
  resolveRejected(intentIds: string[], replacement?: { payload: OutboxJson; head: OutboxHead }, isCurrent?: () => boolean): Promise<OutboxRecord>;
  dispatch(
    build: OutboxRequestBuilder,
    transmit: (request: OutboxRequest) => Promise<OutboxOutcome>,
  ): Promise<OutboxRecord>;
}

const DATABASE = 'astrid.command-outbox';
const STORE = 'owners';

const browserLock: OutboxExclusiveLock = async (name, work) => {
  if (!globalThis.navigator?.locks) throw new Error('Exclusive browser locks are unavailable');
  return await navigator.locks.request(name, { mode: 'exclusive', ifAvailable: true }, (lock) => {
    if (!lock) throw new Error('Outbox is already claimed');
    return work();
  });
};

function detached<T>(value: T): T {
  const check = (item: unknown): void => {
    if (item === null || typeof item === 'string' || typeof item === 'boolean') return;
    if (typeof item === 'number' && Number.isFinite(item)) return;
    if (Array.isArray(item)) { for (const value of item) check(value); return; }
    if (typeof item === 'object' && (Object.getPrototypeOf(item) === Object.prototype || Object.getPrototypeOf(item) === null)) {
      Object.values(item).forEach(check);
      return;
    }
    throw new Error('Outbox values must be finite JSON');
  };
  check(value);
  const clone = (item: unknown): unknown => {
    if (item === null || typeof item !== 'object') return item;
    if (Array.isArray(item)) return item.map(clone);
    const output = Object.create(null) as Record<string, unknown>;
    for (const key of Object.keys(item)) Object.defineProperty(output, key, {
      value: clone((item as Record<string, unknown>)[key]), enumerable: true, configurable: true, writable: true,
    });
    return output;
  };
  return clone(value) as T;
}

function newIntent(payload: OutboxJson, basis: OutboxBasis): OutboxIntent {
  return detached({ id: crypto.randomUUID(), payload, basis,
    ...('head' in basis ? { readyBase: basis.head } : {}) });
}

function scopeKey(scope: OutboxScope, ownerId: string): string {
  const parts = [scope.realmId, scope.actorId, scope.projectId, scope.timelineId, ownerId];
  if (parts.some((part) => typeof part !== 'string' || !part)) throw new Error('Incomplete outbox scope');
  return JSON.stringify(parts);
}

/** No cached/sessionStorage owner: every new editor starts a fresh durable owner. */
export function createCommitOutbox(options: {
  indexedDB?: IDBFactory;
  exclusiveLock?: OutboxExclusiveLock;
} = {}) {
  const factory = options.indexedDB ?? globalThis.indexedDB;
  const lock = options.exclusiveLock ?? browserLock;

  function open(): Promise<IDBDatabase> {
    if (!factory) return Promise.reject(new Error('Durable outbox storage is unavailable'));
    return new Promise((resolve, reject) => {
      const request = factory.open(DATABASE, 1);
      request.addEventListener('upgradeneeded', () => request.result.createObjectStore(STORE));
      request.addEventListener('error', () => reject(request.error));
      request.addEventListener('blocked', () => reject(new Error('Outbox database is blocked')));
      request.addEventListener('success', () => resolve(request.result));
    });
  }

  async function transaction<T>(
    mode: IDBTransactionMode,
    run: (store: IDBObjectStore, finish: (value: T) => void) => void,
  ): Promise<T> {
    const db = await open();
    try {
      return await new Promise<T>((resolve, reject) => {
        const tx = db.transaction(STORE, mode, { durability: 'strict' });
        let result: T;
        tx.addEventListener('complete', () => resolve(result));
        tx.addEventListener('abort', () => reject(tx.error ?? new Error('Outbox transaction aborted')));
        tx.addEventListener('error', () => reject(tx.error));
        try {
          run(tx.objectStore(STORE), (value) => { result = value; });
        } catch (error) {
          tx.abort();
          reject(error);
        }
      });
    } finally {
      db.close();
    }
  }

  async function list(scope: OutboxScope): Promise<OutboxRecord[]> {
    const prefix = scopeKey(scope, '_');
    return transaction('readonly', (store, finish) => {
      const request = store.getAll();
      request.addEventListener('success', () => finish((request.result as OutboxRecord[])
        .filter((record) => scopeKey(record.scope, '_') === prefix).map(detached)));
    });
  }

  async function own<T>(
    scopeInput: OutboxScope,
    ownerId: string,
    create: boolean,
    work: (outbox: ClaimedOutbox, ownerId: string) => Promise<T>,
  ): Promise<T> {
    const { realmId, actorId, projectId, timelineId } = scopeInput;
    const scope = detached({ realmId, actorId, projectId, timelineId });
    const key = scopeKey(scope, ownerId);
    return lock(`${DATABASE}:${key}`, async () => {
      const generation = await transaction<number>('readwrite', (store, finish) => {
        const request = store.get(key);
        request.addEventListener('success', () => {
          const current = request.result as OutboxRecord | undefined;
          if (create ? !!current : !current) {
            finish(0);
            return;
          }
          const record = detached(current ?? { scope, ownerId, generation: 0, intents: [] });
          record.generation += 1;
          store.put(record, key);
          finish(record.generation);
        });
      });
      if (!generation) throw new Error('Outbox owner does not match explicit claim');
      let active = true;
      let dispatching = false;

      function access<T>(mode: IDBTransactionMode, change: (record: OutboxRecord) => T): Promise<T> {
        let failure: unknown;
        return transaction<T>(mode, (store, finish) => {
          const request = store.get(key);
          request.addEventListener('success', () => {
            try {
              const current = request.result as OutboxRecord | undefined;
              if (!active || current?.generation !== generation) throw new Error('Stale outbox claim');
              const record = detached(current);
              const result = change(record);
              if (mode === 'readwrite') store.put(record, key);
              finish(result);
            } catch (error) {
              // Throwing from an IDB event handler alone does not reject the caller's promise.
              failure = error;
              store.transaction.abort();
            }
          });
        }).catch((error) => { throw failure ?? error; });
      }

      const outbox: ClaimedOutbox = {
        read: () => access('readonly', detached),
        async append(payload, basis) {
          const intent = newIntent(payload, basis);
          return access('readwrite', (record) => {
            const predecessor = record.intents[record.intents.length - 1];
            let readyBase = 'head' in intent.basis ? intent.basis.head : undefined;
            if ('after' in intent.basis && predecessor?.id !== intent.basis.after) {
              if (predecessor || record.accepted?.intentId !== intent.basis.after) {
                throw new Error('Dependent intent must follow its queued or last accepted predecessor');
              }
              readyBase = record.accepted.head;
            }
            record.intents.push({
              ...intent,
              ...(readyBase ? { readyBase } : {}),
              ...('after' in intent.basis && predecessor?.conflict !== undefined ? { conflict: predecessor.conflict } : {}),
            });
            return intent.id;
          });
        },
        cancel(intentId) {
          return access('readwrite', (record) => {
            if (record.pending?.intentId === intentId) throw new Error('Cannot cancel an uncertain request');
            if (record.intents.some((intent) => 'after' in intent.basis && intent.basis.after === intentId)) {
              throw new Error('Cannot cancel a predecessor of retained work');
            }
            record.intents = record.intents.filter((intent) => intent.id !== intentId);
          });
        },
        resolveRejected(intentIds, replacement, isCurrent = () => true) {
          const ids = detached(intentIds);
          const intent = replacement ? newIntent(replacement.payload, { head: replacement.head }) : undefined;
          return access('readwrite', (record) => {
            if (!isCurrent()) throw new Error('Timeline command session is closed');
            if (dispatching || record.pending?.outcome?.kind !== 'rejected'
              || record.pending.intentId !== record.intents[0]?.id) {
              throw new Error('Only a definitively rejected prefix can be resolved');
            }
            if (!ids.length || JSON.stringify(ids) !== JSON.stringify(record.intents.map((item) => item.id))) {
              throw new Error('Retained work changed before explicit resolution');
            }
            if (intent && ids.length !== 1) throw new Error('Cannot replace a predecessor of retained work');
            record.intents = intent ? [intent] : [];
            delete record.pending;
            return detached(record);
          });
        },
        async dispatch(build, transmit) {
          if (dispatching) throw new Error('Outbox request is already being transmitted');
          dispatching = true;
          try {
            const pending = await access('readwrite', (record) => {
              if (record.pending) {
                if (record.pending.outcome?.kind === 'rejected') throw new Error('Outbox has a rejected prefix');
                return detached(record.pending);
              }
              const intent = record.intents[0];
              if (!intent) throw new Error('Outbox is empty');
              if (intent.conflict !== undefined || !intent.readyBase) throw new Error('Outbox intent is blocked');
              const built = detached(build(detached(intent), detached(intent.readyBase)));
              const expectedPath = `/v1/projects/${encodeURIComponent(scope.projectId)}/timelines/${encodeURIComponent(scope.timelineId)}/commit`;
              if (built.method !== 'POST' || built.path !== expectedPath) throw new Error('Noncanonical commit route');
              record.pending = {
                intentId: intent.id,
                request: { method: built.method, path: built.path, body: JSON.stringify(built.body), key: crypto.randomUUID() },
              };
              return detached(record.pending);
            });
            // The reservation's transaction has completed before any network callback.
            if (!active) throw new Error('Stale outbox claim');
            let outcome: OutboxOutcome;
            try {
              outcome = detached(await transmit(detached(pending.request)));
            } catch {
              outcome = { kind: 'retry', error: { reason: 'transport_error' } };
            }
            return await access('readwrite', (record) => {
              if (record.pending?.request.key !== pending.request.key
                || record.intents[0]?.id !== pending.intentId) throw new Error('Stale outbox completion');
              if (outcome.kind === 'accepted') {
                record.accepted = { intentId: pending.intentId, head: outcome.head, value: outcome.value };
                record.intents.shift();
                delete record.pending;
                const next = record.intents[0];
                if (next && 'after' in next.basis && next.basis.after === pending.intentId) {
                  next.readyBase = outcome.head;
                }
              } else {
                record.pending.outcome = outcome;
                if (outcome.kind === 'rejected') {
                  const rejected = new Set([pending.intentId]);
                  for (const intent of record.intents) {
                    if (rejected.has(intent.id) || ('after' in intent.basis && rejected.has(intent.basis.after))) {
                      intent.conflict = outcome.error;
                      rejected.add(intent.id);
                    }
                  }
                }
              }
              return detached(record);
            });
          } finally {
            dispatching = false;
          }
        },
      };
      try {
        return await work(outbox, ownerId);
      } finally {
        active = false;
      }
    });
  }

  return {
    list,
    create: <T>(scope: OutboxScope, work: (outbox: ClaimedOutbox, ownerId: string) => Promise<T>) =>
      own(scope, crypto.randomUUID(), true, work),
    recover: <T>(scope: OutboxScope, ownerId: string, work: (outbox: ClaimedOutbox) => Promise<T>) =>
      own(scope, ownerId, false, work),
  };
}
