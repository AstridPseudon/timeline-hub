import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { WorkspaceClient, type Task, type ManagedOutput, type Transport } from '@/integrations/runtime/generated.ts';
import { createCommitOutbox, type ClaimedOutbox, type OutboxExclusiveLock, type OutboxOutcome,
  type OutboxPlacementCapture, type OutboxRequest, type OutboxIntent, type OutboxHead, type OutboxScope } from './commitOutbox.ts';
import { createPlacementRequester, preparePlacementTask, type PlacementRequest } from './placementRequester.ts';

const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project', timelineId: 'original-timeline' };
const head = { revisionId: 'R0', publicationId: 'P0' };
const selected = { group_key: 'pictures', variant_key: 'approved', output_port: 'image', ordinal: 1 };
const objectId = `sha256:${'a'.repeat(64)}`;
const pin = { asset: 'variant', generation_id: 'generation', variant_id: 'variant', object_id: objectId,
  catalog_digest: `sha256:${'b'.repeat(64)}` };
const prepared = preparePlacementTask({
  capability_id: 'image.generate', capability_digest: `sha256:${'c'.repeat(64)}`, project: scope.projectId,
  input_object_ids: [], spec: { prompt: 'original prompt' },
  settlement_effect: { effect_type: 'generation.publish_v1', target_id: scope.projectId, payload: {
    version: 1, modality: 'image', generation_type: 'image', metadata: {}, partial_success_policy: 'reject',
    groups: [{ group_key: selected.group_key, selectors: [{ variant_key: selected.variant_key, output_port: selected.output_port,
      ordinal: selected.ordinal, selector: 'requested' }] }],
  } },
}, 'original-task-key');
const input: PlacementRequest = { request: prepared, head, readClosure: { immutable: ['original-read-pin'] },
  ownerRef: 'parent', anchor: { ref: 'parent/clip:anchor' }, lane: { ref: 'parent/track:lane' }, fallback: null,
  policy: { placement: 'anchor-after', fallback: 'append', image: 'completion-five-second' },
  output: selected, autoApprove: true, createdIds: ['allocated-birth'] };
const completed: Task = {
  task_id: 'task', run_id: 'run', project_id: scope.projectId, state: 'succeeded', version: 9,
  capability_id: 'image.generate', capability_digest: `sha256:${'c'.repeat(64)}`, idempotency_key: prepared.key,
  created_at: '', updated_at: '', attempt_id: 'settled-attempt', runtime_epoch: 1, input_object_ids: [], spec: {},
  result: { generation_publish_v1: { publications: [{ group_key: selected.group_key, generation_id: 'generation',
    variants: [{ ...selected, variant_id: 'variant', generation_id: 'generation', object_id: objectId }] }] } },
};
const managed: ManagedOutput = { ...selected, association_id: 'association', project_id: scope.projectId,
  task_id: 'task', run_id: 'run', attempt_id: 'settled-attempt', selector: { group_key: selected.group_key, variant_key: selected.variant_key }, object_id: objectId,
  digest: objectId, manifest_ref: null, size: 4, filename: 'image.png', media_type: 'image/png', role: 'output',
  producer: {}, provenance: {}, durability: 'durable', state: 'available', version: 99,
  lifecycle: { version: 3, state: 'available' } };
const acceptance = (name: string): OutboxOutcome => ({ kind: 'accepted', head: { revisionId: `R${name}`, publicationId: `P${name}` }, value: { accepted: name } });
function deferred() {
  let resolve!: () => void;
  const promise = new Promise<void>((done) => { resolve = done; });
  return { promise, resolve };
}
function environment() {
  const factory = createFakeIndexedDB();
  const fault = { abortNextWrite: false };
  const open = factory.open.bind(factory);
  // Match the rollback fixture in commitOutbox.test.ts; this fake needs explicit rollback.
  factory.open = (...args: unknown[]) => {
    const request = open(...args);
    request.addEventListener('success', () => {
      const db = request.result;
      const transaction = db.transaction.bind(db);
      db.transaction = (store: string, mode: string) => {
        const tx = transaction(store, mode);
        const records = db.recordsByStore.get(store);
        const before = new Map(records);
        const dispatch = tx.dispatch.bind(tx);
        let aborted = false;
        tx.dispatch = (type: string, event: unknown) => {
          if (type === 'complete' && !aborted && mode === 'readwrite' && fault.abortNextWrite) {
            fault.abortNextWrite = false;
            tx.abort();
            return;
          }
          if (type === 'abort') {
            aborted = true;
            records.clear();
            for (const [key, value] of before) records.set(key, value);
          }
          if (type === 'complete' && aborted) return;
          dispatch(type, event);
        };
        return tx;
      };
    });
    return request;
  };
  const held = new Set<string>();
  const exclusiveLock: OutboxExclusiveLock = async (name, work) => {
    if (held.has(name)) throw new Error('Outbox is already claimed');
    held.add(name);
    try { return await work(); } finally { held.delete(name); }
  };
  const storage = () => createCommitOutbox({ indexedDB: factory, exclusiveLock });
  const state = { task: structuredClone(completed), pages: [[structuredClone(managed)]], pin: { ...pin },
    identity: { realmId: scope.realmId, actorId: scope.actorId }, admissionFailure: 0, readFailure: 0, lostAdmission: false };
  const calls: { method: string; path: string; body?: string; key?: string }[] = [];
  const transport: Transport = vi.fn(async (method, path, headers, bytes) => {
    calls.push({ method, path, body: bytes ? new TextDecoder().decode(bytes as Uint8Array) : undefined, key: headers['Idempotency-Key'] });
    let body: unknown;
    let status = 200;
    if (method === 'POST') {
      if (state.lostAdmission) { state.lostAdmission = false; throw new Error('Lost task ACK'); }
      status = state.admissionFailure || 201;
      body = status === 201 ? { data: state.task, receipt: { receipt_id: 'task-receipt' } }
        : { code: 'admission_refused', message: 'original admission rejected' };
    } else if (path.includes('managed-outputs')) {
      const pageIndex = Number(new URL(path, 'http://fixture').searchParams.get('cursor') ?? '0');
      body = { items: state.pages[pageIndex], next_cursor: pageIndex + 1 < state.pages.length ? String(pageIndex + 1) : null };
    } else if (path.includes('media-selection')) body = state.pin;
    else {
      status = state.readFailure || 200;
      body = status === 200 ? state.task : { code: 'task_read_failed', message: 'task read failed' };
    }
    return { status, headers: {}, body: new TextEncoder().encode(JSON.stringify(body)) };
  });
  const client = new WorkspaceClient('', undefined, transport);
  // Opaque semantic fixture only: these tests do not implement or qualify automatic placement commands.
  const capture = vi.fn<OutboxPlacementCapture>(async (original) => ({ fixture: 'Agent-owned guarded payload', media: original.mediaPin!, ids: original.input.createdIds }));
  const build = vi.fn((intent: OutboxIntent, base: OutboxHead, originalScope: OutboxScope = scope) => ({ method: 'POST',
    path: `/v1/projects/${originalScope.projectId}/timelines/${originalScope.timelineId}/commit`,
    body: { fixture: intent.payload, base: { revisionId: base.revisionId, publicationId: base.publicationId } } }));
  const transmit = vi.fn<(request: OutboxRequest) => Promise<OutboxOutcome>>(async () => acceptance('A'));
  const requester = (withCapture = true) => createPlacementRequester({ client, outboxes: storage(),
    getRecoverableIdentity: async () => state.identity, ...(withCapture ? { capture } : {}), build, transmit });
  async function reserve(box: ClaimedOutbox) { await box.reservePlacementAdmission('request', input); }
  return { factory, fault, storage, state, client, calls, capture, build, transmit, requester, reserve };
}

describe('bounded automatic placement requester', () => {
  it('awaits durable reservation before the generated normal task POST and preserves original capture inputs', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      const durable = deferred();
      const started = deferred();
      const reserve = box.reservePlacementAdmission.bind(box);
      vi.spyOn(box, 'reservePlacementAdmission').mockImplementation(async (id, value) => {
        const saved = await reserve(id, value);
        started.resolve();
        await durable.promise;
        return saved;
      });
      const request = env.requester().request(box, 'request', structuredClone(input));
      await started.promise;
      expect(env.calls).toEqual([]);
      durable.resolve();
      expect((await request).status).toBe('accepted');
      expect(env.calls[0]).toEqual({ method: 'POST', path: '/v1/tasks', body: prepared.body, key: prepared.key });
      expect(env.capture).toHaveBeenCalledTimes(1);
      expect(env.capture.mock.calls[0][0]).toMatchObject({ input, mediaPin: pin,
        taskLocator: { projectId: scope.projectId, taskId: 'task', runId: 'run' } });
      const selection = env.calls.find((v) => v.path.includes('media-selection'))!;
      expect(selection.path).toBe('/v1/projects/project/media-selection?association_id=association&object_id=sha256%3A' + 'a'.repeat(64) + '&version=3');
      const saved = (await box.read()).placementContinuations![0];
      expect(saved.placement?.accepted?.head).toEqual({ revisionId: 'RA', publicationId: 'PA' });
      expect(saved.input).toEqual(input);
    });
  });

  it('never POSTs if reservation fails and never calls capture when no task succeeded', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      env.fault.abortNextWrite = true;
      await expect(env.requester().request(box, 'request', input)).rejects.toThrow('aborted');
      expect(env.calls).toEqual([]);
      expect((await box.read()).placementContinuations).toBeUndefined();
    });
  });

  it('retains exact task bytes/key across lost admission ACK and a fresh requester/storage instance', async () => {
    const env = environment();
    env.state.lostAdmission = true;
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('retry');
      expect((await box.read()).placementContinuations![0].taskLocator).toBeUndefined();
    });
    expect((await env.requester().recover())[0].status).toBe('accepted');
    expect(env.calls.filter((v) => v.method === 'POST')).toEqual([
      { method: 'POST', path: '/v1/tasks', body: prepared.body, key: prepared.key },
      { method: 'POST', path: '/v1/tasks', body: prepared.body, key: prepared.key },
    ]);
    expect(env.capture).toHaveBeenCalledTimes(1);
  });

  it('reconnects from saved task IDs with no event cache or editor, preserving a different original timeline', async () => {
    const env = environment();
    env.state.task.state = 'running';
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('waiting');
      expect((await box.read()).intents).toEqual([]);
    });
    env.state.task.state = 'succeeded';
    env.calls.length = 0;
    const [result] = await env.requester().recover();
    expect(result.scope.timelineId).toBe(scope.timelineId);
    expect(result.status).toBe('accepted');
    expect(env.calls[0]).toMatchObject({ method: 'GET', path: '/v1/tasks/task' });
    expect(env.calls.some((v) => v.method === 'POST')).toBe(false);
  });

  it('reads all output pages and matches the explicit output rather than array-first/latest', async () => {
    const env = environment();
    env.state.pages = [[{ ...managed, variant_key: 'unapproved', ordinal: 0 }], [managed]];
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('accepted');
    });
    expect(env.calls.filter((v) => v.path.includes('managed-outputs'))).toHaveLength(2);
    expect(env.capture.mock.calls[0][0].mediaPin).toEqual(pin);
  });

  it('binds recovery capture and commit to each saved timeline scope before any editor is open', async () => {
    const env = environment();
    const otherScope = { ...scope, timelineId: 'another-saved-timeline' };
    for (const originalScope of [scope, otherScope]) {
      await env.storage().create(originalScope, async (box) => {
        await env.reserve(box);
      });
    }
    const results = await env.requester().recover();
    expect(results.map((v) => v.status)).toEqual(['accepted', 'accepted']);
    expect(env.capture).toHaveBeenNthCalledWith(1, expect.objectContaining({ input }), scope);
    expect(env.capture).toHaveBeenNthCalledWith(2, expect.objectContaining({ input }), otherScope);
    expect(env.build.mock.calls.map((args) => args[2])).toEqual([scope, otherScope]);
    expect(env.transmit.mock.calls.map((args) => args[0].path)).toEqual([
      '/v1/projects/project/timelines/original-timeline/commit',
      '/v1/projects/project/timelines/another-saved-timeline/commit',
    ]);
  });

  it.each(['queued', 'ready', 'running', 'retrying'] as const)('task %s persists its locator without enqueuing an edit', async (state) => {
    const env = environment();
    env.state.task.state = state;
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('waiting');
      expect((await box.read()).intents).toEqual([]);
      expect((await box.read()).placementContinuations![0].taskLocator?.taskId).toBe('task');
    });
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.transmit).not.toHaveBeenCalled();
  });

  it.each(['failed', 'cancelled', 'cancel_requested'] as const)('retains task %s as a visible conflict after restart', async (state) => {
    const env = environment();
    env.state.task.state = state;
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
      expect((await box.read()).placementContinuations![0].conflict).toMatchObject({ message: expect.stringContaining(state) });
    });
    const count = env.calls.length;
    expect((await env.requester().recover())[0].status).toBe('conflict');
    expect(env.calls).toHaveLength(count);
    expect(env.capture).not.toHaveBeenCalled();
  });

  it('retains a normal admission rejection and never silently creates a fresh task', async () => {
    const env = environment();
    env.state.admissionFailure = 409;
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
    });
    expect((await env.requester().recover())[0].status).toBe('conflict');
    expect(env.calls).toHaveLength(1);
  });

  it('retains capture refusal, original pin and IDs without enqueue or recapture', async () => {
    const env = environment();
    env.capture.mockRejectedValue(new Error('original anchor selection changed'));
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
      const record = await box.read();
      expect(record.intents).toEqual([]);
      expect(record.placementContinuations![0]).toMatchObject({ mediaPin: pin, input: { createdIds: input.createdIds },
        conflict: { message: 'original anchor selection changed' } });
    });
    expect((await env.requester().recover())[0].status).toBe('conflict');
    expect(env.capture).toHaveBeenCalledTimes(1);
  });

  it.each(['project_id', 'run_id', 'task_id', 'idempotency_key', 'capability_digest'] as const)('refuses a changed saved task %s', async (field) => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      await env.reserve(box);
      await box.recordPlacementTask('request', prepared, { projectId: scope.projectId, taskId: 'task', runId: 'run' });
    });
    env.state.task[field] = 'other';
    expect((await env.requester().recover())[0].status).toBe('conflict');
    expect(env.capture).not.toHaveBeenCalled();
  });

  it.each(['attempt_id', 'object_id', 'project_id', 'task_id', 'run_id'] as const)('retains a changed managed %s binding as a conflict', async (field) => {
    const env = environment();
    env.state.pages[0][0][field] = 'other';
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
      expect((await box.read()).intents).toEqual([]);
    });
    expect(env.capture).not.toHaveBeenCalled();
  });

  it.each(['missing', 'ambiguous', 'wrong-asset', 'wrong-variant', 'wrong-generation', 'wrong-object', 'extra-field'] as const)('refuses %s output selection', async (failure) => {
    const env = environment();
    if (failure === 'missing') env.state.pages = [[]];
    if (failure === 'ambiguous') env.state.pages = [[managed, managed]];
    if (failure === 'wrong-asset') env.state.pin.asset = 'other';
    if (failure === 'wrong-variant') env.state.pin.variant_id = 'other';
    if (failure === 'wrong-generation') env.state.pin.generation_id = 'other';
    if (failure === 'wrong-object') env.state.pin.object_id = 'other';
    if (failure === 'extra-field') Object.assign(env.state.pin, { unexpected_field: 'refused' });
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
    });
    expect(env.capture).not.toHaveBeenCalled();
    expect((await env.requester().recover())[0].status).toBe('conflict');
  });

  it('persists linkage before commit POST and replays exact commit bytes/key after lost ACK', async () => {
    const env = environment();
    let firstRequest: unknown;
    env.transmit.mockImplementationOnce(async (request) => {
      firstRequest = request;
      const [record] = await env.storage().list(scope);
      expect(record.pending?.request).toEqual(request);
      expect(record.placementContinuations![0].placement?.intentId).toBe(record.intents[0].id);
      throw new Error('Lost commit ACK');
    });
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('retry');
    });
    expect((await env.requester().recover())[0].status).toBe('accepted');
    expect(env.transmit.mock.calls[1][0]).toEqual(firstRequest);
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.build).toHaveBeenCalledTimes(1);
  });

  it('never rearms duplicate completion after acceptance, undo and later B/C acceptance', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('accepted');
      const linked = structuredClone((await box.read()).placementContinuations![0]);
      for (const label of ['undo', 'B', 'C']) {
        await box.append({ fixture: label }, { head });
        await box.dispatch(env.build, async () => acceptance(label));
        expect((await env.requester().resume(box))[0].status).toBe('accepted');
        expect((await box.read()).placementContinuations![0]).toEqual(linked);
      }
    });
    for (let duplicate = 0; duplicate < 2; duplicate += 1) expect((await env.requester().recover())[0].status).toBe('accepted');
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.transmit).toHaveBeenCalledTimes(1);
    expect(env.calls.filter((v) => v.method === 'POST')).toHaveLength(1);
  });

  it('keeps commit rejection visible and preserves captured intent instead of recapturing', async () => {
    const env = environment();
    env.transmit.mockResolvedValue({ kind: 'rejected', error: { kind: 'conflict', message: 'anchor changed' } });
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
    });
    expect((await env.requester().recover())[0].status).toBe('conflict');
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.transmit).toHaveBeenCalledTimes(1);
  });

  it('retains a reservation after locator persistence fails and retries the same normal admission', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      vi.spyOn(box, 'recordPlacementTask').mockRejectedValueOnce(new Error('Outbox transaction aborted'));
      expect((await env.requester().request(box, 'request', input)).status).toBe('retry');
      expect((await box.read()).placementContinuations![0].taskLocator).toBeUndefined();
      expect(env.calls).toHaveLength(1);
    });
    expect((await env.requester().recover())[0].status).toBe('accepted');
    expect(env.calls.filter((v) => v.method === 'POST').map((v) => [v.body, v.key])).toEqual([
      [prepared.body, prepared.key], [prepared.body, prepared.key],
    ]);
  });

  it('retains the original pin after interrupted capture and saves a changed selection conflict on reconnect', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      await env.reserve(box);
      await box.recordPlacementTask('request', prepared, { projectId: scope.projectId, taskId: 'task', runId: 'run' });
      await expect(box.capturePlacement('request', pin, async () => {
        env.fault.abortNextWrite = true;
        return { fixture: 'capture completed before interrupted append' };
      })).rejects.toThrow('aborted');
      expect((await box.read()).placementContinuations![0]).toMatchObject({ mediaPin: pin });
      expect((await box.read()).intents).toEqual([]);
    });
    env.state.pin.catalog_digest = `sha256:${'d'.repeat(64)}`;
    const [result] = await env.requester().recover();
    expect(result.status).toBe('conflict');
    expect(result.continuation).toMatchObject({ mediaPin: pin, conflict: { message: 'Saved immutable media selection changed' } });
    expect(env.capture).not.toHaveBeenCalled();
  });

  it('retries an unavailable normal task read without losing the locator or allocating a new admission', async () => {
    const env = environment();
    env.state.readFailure = 503;
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('retry');
      expect((await box.read()).placementContinuations![0]).toMatchObject({ taskLocator: { taskId: 'task' } });
      expect((await box.read()).placementContinuations![0].conflict).toBeUndefined();
    });
    env.state.readFailure = 0;
    expect((await env.requester().recover())[0].status).toBe('accepted');
    expect(env.calls.filter((v) => v.method === 'POST')).toHaveLength(1);
  });

  it('does not rearm a cancelled unsent placement', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      await env.reserve(box);
      await box.recordPlacementTask('request', prepared, { projectId: scope.projectId, taskId: 'task', runId: 'run' });
      const linked = await box.capturePlacement('request', pin, env.capture);
      await box.cancel(linked.placement!.intentId);
    });
    expect((await env.requester().recover())[0].status).toBe('cancelled');
    expect(env.capture).toHaveBeenCalledTimes(1);
    expect(env.calls).toEqual([]);
  });

  it('rechecks identity after durable reservation and refuses task POST when it changes', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      const reserve = box.reservePlacementAdmission.bind(box);
      vi.spyOn(box, 'reservePlacementAdmission').mockImplementation(async (id, value) => {
        const saved = await reserve(id, value);
        env.state.identity.actorId = 'other-actor';
        return saved;
      });
      await expect(env.requester().request(box, 'request', input)).rejects.toThrow('identity changed');
      expect((await box.read()).placementContinuations![0].input).toEqual(input);
    });
    expect(env.calls).toEqual([]);
  });

  it.each(['generation.create_with_variant', 'generation.variant.append'])('reads the ordinary %s result without using primary variants', async (effect_type) => {
    const env = environment();
    const legacyOutput = { ...selected, group_key: 'default', variant_key: '0', ordinal: 0 };
    const request = preparePlacementTask({ ...JSON.parse(prepared.body), settlement_effect: {
      effect_type, target_id: effect_type === 'generation.variant.append' ? 'generation' : scope.projectId,
      ...(effect_type === 'generation.variant.append' ? { expected_version: 1 } : {}),
      payload: { output_name: selected.output_port, output_ordinal: 0, variant_type: 'image', primary_policy: 'preserve',
        ...(effect_type === 'generation.variant.append' ? { source_variant_id: 'source', source_object_id: objectId }
          : { generation_type: 'image', metadata: {} }) },
    } }, prepared.key);
    env.state.pages = [[{ ...managed, ...legacyOutput, selector: { group_key: 'default', variant_key: '0' } }]];
    env.state.task.result = { generation_variant: { generation_id: pin.generation_id, variant_id: pin.variant_id,
      object_id: pin.object_id, metadata: { source_task_id: 'task', output_name: selected.output_port, output_ordinal: 0 } } };
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', { ...input, request, output: legacyOutput })).status).toBe('accepted');
    });
    expect(env.capture.mock.calls[0][0].mediaPin).toEqual(pin);
  });

  it('requires the original identity and browser owner lock', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      await env.reserve(box);
      const [locked] = await env.requester().recover();
      expect(locked).toMatchObject({ status: 'retry', message: 'Outbox is already claimed' });
      env.state.identity.actorId = 'another-actor';
      await expect(env.requester().resume(box)).rejects.toThrow('identity changed');
      expect(await env.requester().recover()).toEqual([]);
      env.state.identity = { realmId: 'other-realm', actorId: scope.actorId };
      expect(await env.requester().recover()).toEqual([]);
    });
    expect(env.calls).toEqual([]);
  });

  it('keeps missing capture and unbound owners visible for manual placement without auto activation', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      expect((await env.requester(false).request(box, 'request', input)).status).toBe('manual');
      expect((await box.read()).intents).toEqual([]);
    });
    await env.storage().create(scope, async () => {});
    const results = await env.requester(false).recover();
    expect(results).toHaveLength(2);
    expect(results.map((v) => v.status)).toEqual(['manual', 'manual']);
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.transmit).not.toHaveBeenCalled();
  });

  it.each(['approval', 'project', 'bytes', 'selector', 'unsaved'] as const)('refuses %s before task submission', async (failure) => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      const changed = structuredClone(input);
      if (failure === 'approval') Object.assign(changed, { autoApprove: false });
      if (failure === 'project') changed.request = preparePlacementTask({ ...JSON.parse(prepared.body), project: 'wrong-project' }, prepared.key);
      if (failure === 'bytes') changed.request.body += '\n';
      if (failure === 'selector') changed.output.variant_key = 'unapproved';
      if (failure === 'unsaved') await box.append({ fixture: 'unsaved' }, { head });
      await expect(env.requester().request(box, 'request', changed)).rejects.toThrow();
      expect(env.calls).toEqual([]);
    });
  });
});
