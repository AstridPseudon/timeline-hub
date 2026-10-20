import { describe, expect, it } from 'vitest';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
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

  it.each([
    ['matching accepted projection', { kind: 'accepted', head: { revisionId: 'r0', publicationId: 'p0' } }, true],
    ['matching local projection base', { kind: 'local', base: { revisionId: 'r0', publicationId: 'p0' }, generation: 1 }, true],
    ['stale accepted projection', { kind: 'accepted', head: { revisionId: 'r0', publicationId: 'stale' } }, false],
    ['no projection fact', undefined, false],
  ] as const)('requires a matching projection fact when publication is null (%s)', async (_name, projection, allowed) => {
    const env = await environment();
    const current = env.current();
    current.head = { ...current.head!, headPublicationId: null };
    current.editProjection = projection as TimelineData['editProjection'];
    const session = await env.mount();
    const patch: TimelinePatch = {
      version: current.configVersion,
      operations: [{ op: 'track.update', target: 'V1', payload: { label: 'Native label' } }],
    };

    if (allowed) {
      expect(() => session.genericPatchPort.capture({ patch, current })).not.toThrow();
    } else {
      expect(() => session.genericPatchPort.capture({ patch, current }))
        .toThrow('Displayed timeline does not match the raw authoring basis');
    }
    await session.dispose();
  });
});
