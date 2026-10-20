import { describe, expect, it } from 'vitest';
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
});
