import { test } from 'node:test';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { declareAppTransition, admitTransitionContribution, transitionContributionIdentity, queryTrackFrame, prepareDeclaredTrack, prepareTrack, TransitionAdmissionError, } from '../src/evaluation.js';
const host = 'timeline-composition';
const clips = [{ id: 'a', start: 0, duration: 30 }, { id: 'b', start: 30, duration: 30 }];
const declare = () => declareAppTransition('v1', 'a', { type: 'crossfade', duration: 0.3 }, 30, host);
const refused = (fn, code) => {
    assert.throws(fn, (error) => {
        assert.ok(error instanceof TransitionAdmissionError);
        assert.equal(error.code, code);
        assert.ok(error.nextStep.length > 0);
        assert.ok(error.message.includes(error.nextStep));
        return true;
    });
};
test('App seconds, alias, params and one outgoing owner convert explicitly', () => {
    const input = { type: 'crossfade', duration: 0.35, params: { easing: 'linear', custom: 7 } };
    const before = JSON.stringify(input);
    const d = declareAppTransition('v1', 'a', input, 30, host);
    assert.deepEqual(d, {
        owner: { trackId: 'v1', clipId: 'a' },
        implementation: { host, id: 'cross-fade' },
        spec: { T: 11, kind: 'dissolve', align: 'end' }, params: input.params,
    });
    assert.notEqual(d.params, input.params);
    assert.equal(JSON.stringify(input), before);
});
test('fade declares dip; canonical cross-fade declares dissolve', () => {
    assert.equal(declareAppTransition('v1', 'a', { type: 'fade', duration: 0.3 }, 30, host).spec.kind, 'dip');
    assert.equal(declareAppTransition('v1', 'a', { type: 'cross-fade', duration: 0.3 }, 30, host).spec.kind, 'dissolve');
});
test('admitted declarations use the existing planner exactly', () => {
    const d = declare();
    assert.deepEqual(prepareDeclaredTrack('v1', clips, [d], host), prepareTrack(clips, [d.spec, null]));
});
test('gaps remain valid, are not closed, and retain the planner cut', () => {
    const gap = [clips[0], { ...clips[1], start: 40 }];
    const before = JSON.stringify(gap);
    assert.deepEqual(prepareDeclaredTrack('v1', gap, [declare()], host), prepareTrack(gap, [null, null]));
    assert.equal(JSON.stringify(gap), before);
});
for (const start of [29, 20, 0, -5]) {
    test(`same-track overlap at frame ${start} is refused with a next step, never repaired`, () => {
        const input = [clips[0], { ...clips[1], start }];
        const before = JSON.stringify(input);
        refused(() => prepareDeclaredTrack('v1', input, [declare()], host), 'transition/same-track-overlap');
        assert.equal(JSON.stringify(input), before);
    });
}
test('overlaps are refused even without a transition declaration', () => {
    refused(() => prepareDeclaredTrack('v1', [clips[0], { ...clips[1], start: 20 }], [], host), 'transition/same-track-overlap');
});
test('separate tracks may occupy the same time', () => {
    assert.doesNotThrow(() => prepareDeclaredTrack('v1', [clips[0]], [], host));
    assert.doesNotThrow(() => prepareDeclaredTrack('v2', [{ ...clips[0], id: 'overlay' }], [], host));
});
test('duplicate declarations cannot acquire the same owner', () => {
    refused(() => prepareDeclaredTrack('v1', clips, [declare(), declare()], host), 'transition/duplicate-owner');
});
for (const owner of [{ trackId: 'v2', clipId: 'a' }, { trackId: 'v1', clipId: 'missing' }, { trackId: 'v1', clipId: 'b' }]) {
    test(`foreign/missing/final owner ${owner.trackId}/${owner.clipId} is refused`, () => {
        refused(() => prepareDeclaredTrack('v1', clips, [{ ...declare(), owner }], host), 'transition/invalid-owner');
    });
}
test('unsupported host is explicit at conversion and admission, even on an empty track', () => {
    refused(() => declareAppTransition('v1', 'a', { type: 'crossfade', duration: 1 }, 30, 'browser-export'), 'transition/unsupported-host');
    refused(() => prepareDeclaredTrack('v1', [], [], 'browser-export'), 'transition/unsupported-host');
});
test('a declaration cannot carry an unsupported host past admission', () => {
    const d = declare();
    const forged = { ...d, implementation: { ...d.implementation, host: 'other' } };
    refused(() => prepareDeclaredTrack('v1', clips, [forged], host), 'transition/unsupported-host');
});
test('unknown implementations are refused, never approximated by dissolve', () => {
    refused(() => declareAppTransition('v1', 'a', { type: 'wipe', duration: 1 }, 30, host), 'transition/unsupported-implementation');
    const d = declare();
    refused(() => prepareDeclaredTrack('v1', clips, [{ ...d, spec: { ...d.spec, kind: 'dip' } }], host), 'transition/invalid-declaration');
});
for (const duration of [0, -1, NaN, Infinity, 0.001]) {
    test(`invalid duration ${duration} is refused`, () => {
        refused(() => declareAppTransition('v1', 'a', { type: 'crossfade', duration }, 30, host), 'transition/invalid-duration');
    });
}
test('invalid fps, owner and duplicate clip IDs are refused', () => {
    refused(() => declareAppTransition('v1', 'a', { type: 'crossfade', duration: 1 }, 0, host), 'transition/invalid-duration');
    refused(() => declareAppTransition('', 'a', { type: 'crossfade', duration: 1 }, 30, host), 'transition/invalid-owner');
    refused(() => prepareDeclaredTrack('v1', [clips[0], { ...clips[1], id: 'a' }], [], host), 'transition/invalid-span');
});
test('legacy one-frame overlap and last-clip behavior remains unchanged', () => {
    const legacy = prepareTrack([clips[0], { ...clips[1], start: 29 }], [declare().spec, declare().spec]);
    assert.equal(legacy.plans[1].drawStart, 21);
    assert.equal(legacy.plans[1].ownOffset, 8);
    assert.equal(legacy.plans[1].fadeOut, null);
});
const resource = () => ({
    owner: 'pack:example', id: 'example.transition.soft', kind: 'transition',
    transitionId: 'example:soft', implementation: { host, id: 'cross-fade' },
    supportedParams: ['easing'], defaults: { easing: 'linear' },
});
const reference = (r) => ({
    owner: r.owner, id: r.id, transitionId: r.transitionId,
    revision: 'sha256:' + createHash('sha256').update(transitionContributionIdentity(r)).digest('hex'),
});
const admitted = async (r = resource()) => admitTransitionContribution(r, reference(r), true);
const contributed = (binding, params) => declareAppTransition('v1', 'a', { type: binding.resource.transitionId, revision: binding.revision,
    duration: 0.3, params }, 30, host, binding);
const rejects = async (fn, code) => {
    await assert.rejects(fn, (error) => {
        assert.ok(error instanceof TransitionAdmissionError);
        assert.equal(error.code, code);
        assert.ok(error.nextStep.length > 0);
        return true;
    });
};
test('unique contributed identity survives JSON save/load, admission, declaration and shared frame queries', async () => {
    const binding = await admitted();
    const persisted = { type: binding.resource.transitionId, revision: binding.revision, duration: 0.3, params: { easing: 'linear' } };
    const before = JSON.stringify(persisted);
    const d = declareAppTransition('v1', 'a', JSON.parse(before), 30, host, binding);
    assert.equal(d.contribution, binding);
    assert.equal(d.implementation, binding.resource.implementation);
    assert.equal(d.contribution.resource.id, 'example.transition.soft');
    assert.equal(d.contribution.resource.owner, 'pack:example');
    assert.equal(d.contribution.resource.transitionId, persisted.type);
    assert.equal(d.contribution.revision, persisted.revision);
    assert.equal(JSON.stringify(persisted), before);
    assert.deepEqual(d.params, persisted.params);
    const planned = prepareDeclaredTrack('v1', clips, [d], host);
    const existing = prepareTrack(clips, [d.spec, null]);
    assert.deepEqual(planned, existing);
    for (const frame of [0, 21, 25, 29, 30, 59, 60]) {
        assert.deepEqual(queryTrackFrame(planned, frame), queryTrackFrame(existing, frame));
    }
});
test('contributed fade reaches the existing dip planner and exact implementation binding', async () => {
    const binding = await admitted({ ...resource(), implementation: { host, id: 'fade' } });
    const d = contributed(binding);
    assert.equal(d.implementation, binding.resource.implementation);
    assert.equal(d.spec.kind, 'dip');
    assert.deepEqual(prepareDeclaredTrack('v1', clips, [d], host), prepareTrack(clips, [d.spec, null]));
});
test('admission snapshots and freezes all resource identity before awaiting the digest', async () => {
    const r = resource();
    const pending = admitTransitionContribution(r, reference(r), true);
    r.implementation.id = 'fade';
    r.defaults.easing = 'ignored';
    const binding = await pending;
    assert.equal(binding.resource.implementation.id, 'cross-fade');
    assert.equal(binding.resource.defaults.easing, 'linear');
    for (const value of [binding, binding.resource, binding.resource.implementation,
        binding.resource.supportedParams, binding.resource.defaults])
        assert.ok(Object.isFrozen(value));
});
for (const type of ['crossfade', 'cross-fade', 'fade']) {
    test(`builtin ${type} has priority over an unrelated contributed binding`, async () => {
        const binding = await admitted();
        const input = { type, duration: 0.3, params: { custom: 7 } };
        assert.deepEqual(declareAppTransition('v1', 'a', input, 30, host, binding), declareAppTransition('v1', 'a', input, 30, host));
    });
}
for (const patch of [
    { owner: 'pack:other' }, { id: 'other.contribution' }, { transitionId: 'other:soft' },
    { implementation: { host, id: 'fade' } }, { supportedParams: [], defaults: {} }, { defaults: {} },
]) {
    test(`changed resource ${JSON.stringify(patch)} requires an explicit repin`, async () => {
        const r = resource();
        await rejects(() => admitTransitionContribution({ ...r, ...patch }, reference(r), true), ['owner', 'id', 'transitionId'].some(key => Object.hasOwn(patch, key))
            ? 'transition/reference-mismatch' : 'transition/revision-mismatch');
    });
}
test('inactive resource and missing/mismatched expected identity refuse explicitly', async () => {
    const r = resource(), ref = reference(r);
    await rejects(() => admitTransitionContribution(r, ref, false), 'transition/inactive-contribution');
    for (const patch of [{ owner: '' }, { id: '' }, { transitionId: '' }, { revision: '' }, { revision: undefined }]) {
        await rejects(() => admitTransitionContribution(r, { ...ref, ...patch }, true), 'transition/reference-mismatch');
    }
});
test('unknown IDs, missing admission, forged binding and stale clip revisions never alias or fall back', async () => {
    const binding = await admitted();
    refused(() => declareAppTransition('v1', 'a', { type: 'unknown:soft', duration: 0.3 }, 30, host), 'transition/unsupported-implementation');
    const input = { type: binding.resource.transitionId, duration: 0.3 };
    for (const revision of [undefined, '', 'sha256:' + '0'.repeat(64)]) {
        refused(() => declareAppTransition('v1', 'a', { ...input, revision }, 30, host, binding), 'transition/reference-mismatch');
    }
    refused(() => declareAppTransition('v1', 'a', { ...input, type: 'unknown:soft', revision: binding.revision }, 30, host, binding), 'transition/reference-mismatch');
    refused(() => contributed(JSON.parse(JSON.stringify(binding))), 'transition/invalid-binding');
});
for (const patch of [
    { owner: '' }, { id: '' }, { transitionId: '' }, { transitionId: 'crossfade' },
    { transitionId: 'cross-fade' }, { transitionId: 'fade' },
]) {
    test(`invalid or protected resource identity ${JSON.stringify(patch)} refuses`, async () => {
        await rejects(() => admitTransitionContribution({ ...resource(), ...patch }, reference(resource()), true), 'transition/invalid-resource');
    });
}
test('unsupported resource host/implementation and missing implementation refuse', async () => {
    const ref = reference(resource());
    for (const [implementation, code] of [
        [{ host: 'browser-export', id: 'cross-fade' }, 'transition/unsupported-host'],
        [{ host, id: 'wipe' }, 'transition/unsupported-implementation'],
        [undefined, 'transition/invalid-binding'],
    ]) {
        await rejects(() => admitTransitionContribution({ ...resource(), implementation }, ref, true), code);
    }
});
for (const params of [null, [], 'linear', { custom: 7 }, { easing: 'ease-in' }, { easing: undefined }]) {
    test(`malformed or unsupported contributed params ${JSON.stringify(params)} refuse`, async () => {
        const binding = await admitted();
        refused(() => contributed(binding, params), 'transition/invalid-params');
    });
}
test('defaults are applied only from the pinned resource; undeclared easing refuses', async () => {
    const binding = await admitted();
    assert.deepEqual(contributed(binding).params, { easing: 'linear' });
    const empty = await admitted({ ...resource(), supportedParams: [], defaults: {} });
    assert.deepEqual(contributed(empty).params, {});
    refused(() => contributed(empty, { easing: 'linear' }), 'transition/invalid-params');
    for (const patch of [{ supportedParams: ['custom'] }, { defaults: { easing: 'ease-in' } },
        { supportedParams: [], defaults: { easing: 'linear' } }, { supportedParams: ['easing', 'easing'] }]) {
        await rejects(() => admitTransitionContribution({ ...resource(), ...patch }, reference(resource()), true), 'transition/invalid-params');
    }
});
test('contributed declarations preserve all owner/host/binding/params refusal guards at planner admission', async () => {
    const d = contributed(await admitted());
    for (const owner of [{ trackId: 'v2', clipId: 'a' }, { trackId: 'v1', clipId: 'missing' }, { trackId: 'v1', clipId: 'b' }]) {
        refused(() => prepareDeclaredTrack('v1', clips, [{ ...d, owner }], host), 'transition/invalid-owner');
    }
    refused(() => declareAppTransition(' ', 'a', { type: 'example:soft', revision: d.contribution.revision, duration: 0.3 }, 30, host, d.contribution), 'transition/invalid-owner');
    refused(() => prepareDeclaredTrack('v1', clips, [d], 'worker-export'), 'transition/unsupported-host');
    refused(() => prepareDeclaredTrack('v1', clips, [{ ...d, implementation: { ...d.implementation } }], host), 'transition/invalid-binding');
    refused(() => prepareDeclaredTrack('v1', clips, [{ ...d, params: { easing: 'ignored' } }], host), 'transition/invalid-params');
    refused(() => prepareDeclaredTrack('v1', clips, [{ ...d, contribution: { ...d.contribution } }], host), 'transition/invalid-binding');
});
