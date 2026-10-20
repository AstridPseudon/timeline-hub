import { describe, expect, it, vi } from 'vitest';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { environment, scope } from './__tests__/commitSessionEnvironment.ts';

describe('generic patch command session', () => {
  it('persists one command list and retries the exact request after restart', async () => {
    const env = await environment();
    const patch: TimelinePatch = {
      version: 1,
      operations: [{ op: 'track.update', target: 'V1', payload: { label: 'Native label' } }],
    };
    env.setFault('lost');

    const first = await env.mount();
    const captured = first.genericPatchPort.capture({ patch, current: env.current() });
    const prepared = first.genericPatchPort.finish(captured);
    first.genericPatchPort.submit(prepared);
    await new Promise<void>((resolve) => {
      const check = () => env.commits().length ? resolve() : setTimeout(check, 0);
      check();
    });
    await first.dispose();

    const owners = await env.outboxes.list(scope);
    expect(owners).toHaveLength(1);
    const second = await env.mount();
    await second.recover(owners[0].ownerId);
    await second.flush();

    expect(env.commits()).toHaveLength(2);
    expect(env.commits()[0].body?.commands).toHaveLength(1);
    expect(env.commits()[1].body?.commands).toEqual(env.commits()[0].body?.commands);
    expect(env.commits()[1].bodyText).toBe(env.commits()[0].bodyText);
    expect(env.commits()[1].key).toBe(env.commits()[0].key);
    await second.dispose();
  });

  it('proves the private392 consumer through the generic port/session/client seam', async () => {
    const env = await environment();
    const first = await env.mount();
    const patch: TimelinePatch = { version: 1, operations: [
      { op: 'project-data.write', target: 'com.example.private392', payload: {
        key: 'settings', value: { keep: true, opaque: { nullish: null, disabled: false } }, mode: 'merge',
      }, order: 1 },
      { op: 'project-data.write', target: 'com.example.private392', payload: {
        key: 'settings', value: { nested: { first: true } }, mode: 'merge',
      }, order: 2 },
      { op: 'project-data.write', target: 'com.example.private392', payload: {
        key: 'replacement', value: { fresh: true }, mode: 'replace',
      }, order: 3 },
    ] };

    env.setFault('lost');
    const captured = first.genericPatchPort.capture({ patch, current: env.current() });
    const prepared = first.genericPatchPort.finish(captured);
    first.genericPatchPort.submit(prepared);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    const original = structuredClone(env.commits()[0]);
    await first.dispose();

    const [owner] = await env.outboxes.list(scope);
    const second = await env.mount();
    await second.recover(owner.ownerId);
    await second.flush();
    expect(env.commits()[1]).toEqual(original);
    expect(env.commits()[1].body?.commands.map((command) => command.op)).toEqual([
      'project-data.write', 'project-data.write', 'project-data.write',
    ]);
    expect(env.commits()[1].body?.commands[0].expect).toMatchObject({
      'parent::config.app': { state: 'absent' },
      'parent::config.app["com.example.private392"]': { state: 'absent' },
    });
    expect(env.commits()[1].body?.commands[1].expect).toMatchObject({
      'parent::config.app["com.example.private392"].settings': {
        state: 'present',
        value: { keep: true, opaque: { nullish: null, disabled: false } },
      },
    });
    expect(env.commits()[1].body?.commands[0].args).toMatchObject({
      target: 'com.example.private392', key: 'settings', mode: 'replace',
    });
    expect(env.commits()[1].body?.commands[0].args.value).toEqual({
      keep: true, opaque: { nullish: null, disabled: false },
    });
    expect(env.commits()[1].body?.commands[1].args.value).toEqual({
      keep: true, opaque: { nullish: null, disabled: false }, nested: { first: true },
    });
    expect(env.commits()[1].body?.commands[2].args.value).toEqual({ fresh: true });

    const disjoint = second.genericPatchPort.capture({ patch: {
      version: 1,
      operations: [{ op: 'project-data.write', target: 'com.example.private392', payload: {
        key: 'settings', value: { nested: { second: true } }, mode: 'merge',
      } }],
    }, current: env.current() });
    const disjointPrepared = second.genericPatchPort.finish(disjoint);
    const remote = await env.external((document) => {
      const app = document.parent_revision.payload.config.app ??= {};
      const namespace = app['com.example.private392'] as Record<string, unknown>;
      namespace.remote = { preserved: [null, false, 'opaque'] };
    });
    expect(remote.head.revisionId).toMatch(/^external-/);
    second.genericPatchPort.submit(disjointPrepared);
    await second.flush();
    expect(env.commits()[2].body?.base_revision_id).toBe('r1');
    expect(env.acceptedCommits()).toBe(2);
    expect(env.current().config.app?.['com.example.private392']).toMatchObject({
      remote: { preserved: [null, false, 'opaque'] },
      settings: { nested: { second: true } },
    });

    const stale = second.genericPatchPort.capture({ patch: {
      version: 1,
      operations: [{ op: 'project-data.write', target: 'com.example.private392', payload: {
        key: 'settings', value: { stale: true }, mode: 'replace',
      } }],
    }, current: env.current() });
    const stalePrepared = second.genericPatchPort.finish(stale);
    await env.external((document) => {
      const namespace = document.parent_revision.payload.config.app!['com.example.private392'] as Record<string, unknown>;
      namespace.settings = { changed: 'elsewhere' };
    });
    const acceptedBeforeStale = env.acceptedCommits();
    second.genericPatchPort.submit(stalePrepared);
    await vi.waitFor(() => expect(second.getState().status).toBe('conflict'));
    expect(env.acceptedCommits()).toBe(acceptedBeforeStale);
    await second.useLatest();

    await second.undo();
    expect(env.current().config.app?.['com.example.private392']).toEqual({
      settings: {
        keep: true, opaque: { nullish: null, disabled: false }, nested: { first: true },
      },
      replacement: { fresh: true },
      remote: { preserved: [null, false, 'opaque'] },
    });
    expect(env.calls.filter((call) => call.method === 'POST' && call.path !== '/v1/handshake'
      && !call.path.endsWith('/commit'))).toEqual([]);
    await second.dispose();
  });
});
