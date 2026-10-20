import { describe, expect, it, vi } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { environment, scope, trimDocument } from './__tests__/commitSessionEnvironment.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from './trackLabelGesture.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from './clipParamsGesture.ts';
import { captureClipTrimEdit, submitClipTrimEdit } from './clipTrimGesture.ts';

// This fake unit transport proves App queue/recovery behavior, not Runtime acceptance.
describe('mixed edits in the shared durable command session', () => {
  it('recovers label → params → trim with the original guards and exact lost-ACK request', async () => {
    const env = await environment(trimDocument());
    const session = await env.mount();
    const labelFinish = vi.spyOn(session.trackLabelPort, 'finish');
    const paramsFinish = vi.spyOn(session.clipParamsPort, 'finish');
    const trimFinish = vi.spyOn(session.clipTrimPort, 'finish');
    env.setFault('lost');

    const label = captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1');
    submitTrackLabelEdit(label, { values: { label: 'Picture — α' }, clear: [] });
    const params = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
    submitClipParamsEdit(params, { values: { choice: null }, clear: ['missing'] });
    const trim = captureClipTrimEdit(session.clipTrimPort, env.current(), 'x');
    const originalTrimBasis = structuredClone(trim.basis);
    submitClipTrimEdit(trim, { in_s: 1.123456, out_s: 5.987654 });
    const commands: EditCommand[] = structuredClone([labelFinish.mock.results[0].value.command,
      paramsFinish.mock.results[0].value.command, trimFinish.mock.results[0].value.command]);

    expect(commands.map((command) => command.op)).toEqual(['track.set', 'clip.set-params', 'clip.trim']);
    expect(commands[0].expect!['parent/track:V1::label']).toEqual({ state: 'absent' });
    expect(commands[1].expect!['parent/clip:x::params.choice']).toEqual({ state: 'absent' });
    expect(commands[2]).toMatchObject({ args: { in_s: 1.123456, out_s: 5.987654 },
      expect: { 'parent/clip:x::from': { state: 'present', value: 2 } },
      reads: expect.arrayContaining([{ ref: 'parent/clip:x', path: ['speed'], state: { state: 'present', value: 2 } }]) });
    expect(trim.basis).toEqual(originalTrimBasis);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    await session.dispose();

    const originalRequest = structuredClone(env.commits()[0]);
    expect(env.commits()).toHaveLength(1);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(3);
    expect(stored.intents.map((intent) => (intent.payload as unknown as { commands: EditCommand[] }).commands))
      .toEqual(commands.map((command) => [command]));
    expect(stored.intents[0].basis).toEqual({ head: env.initial.head });
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    expect(stored.intents[2].basis).toEqual({ after: stored.intents[1].id });
    expect(stored.pending!.request.key).toBe(originalRequest.key);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(originalRequest.body);
    expect(env.previews).toHaveBeenCalledTimes(3);

    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    expect(reopened.getState().status).toBe('recovery');
    expect(env.commits()).toHaveLength(1);
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.commits()).toHaveLength(4);
    expect(env.commits()[1]).toEqual(originalRequest);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [commands[1]] });
    expect(env.commits()[3].body).toMatchObject({ base_revision_id: 'r2', base_publication_id: 'p2', commands: [commands[2]] });
    expect(new Set(env.commits().map((call) => call.key)).size).toBe(3);
    expect(env.current().config.tracks![0].label).toBe('Picture — α');
    expect(env.current().config.clips[0]).toMatchObject({ params: { choice: null },
      from: 1.123456, to: 5.987654, hold: 4.864198, speed: 2,
      app: { astrid: { opaque: [null, false] }, 'org.example': { literal: 'x', clear: null } },
      unknown: { keep: [null, false, 0] } });
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(0);
    expect(saved.pending).toBeUndefined();
    expect(reopened.getState().status).toBe('saved');
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')).toEqual(env.commits());
    await reopened.dispose();
  });
});
