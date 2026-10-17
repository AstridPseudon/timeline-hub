import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {test} from 'node:test';
import {pathToFileURL} from 'node:url';
import {createElement, isValidElement} from 'react';

// Explicit source-selected integration fixture. No substitute product definition.
const config = JSON.parse(readFileSync(process.env.I_MODIFIER_TEST_CONFIG, 'utf8'));
const descriptor = JSON.parse(readFileSync(config.descriptor, 'utf8'));
const actual = await import(pathToFileURL(config.pack + '/extensions/timeline.component/vignette.tsx').href);
const {bindComponentRegistry} = await import(pathToFileURL(config.sdk + '/remotion/src/components.ts').href);
const {configureComponentHost} = await import(pathToFileURL(config.app + '/src/tools/video-editor/runtime/astrid-components.ts').href);
const {composeAppClipModifiers} = await import(pathToFileURL(config.app + '/src/tools/video-editor/runtime/clip-modifiers.ts').href);
const {composeModifiers, modifierParameterAddress, parseModifierParameterAddress} = await import('../src/modifiers.ts');
const {composeClipLook} = await import('../src/ClipLook.tsx');
const {DEFAULT_THEME} = await import('../src/ThemeContext.tsx');
const identity = 'timeline.component/fresh_vignette_029.vignette';
const digest = '1ac864cc8cf36842bc9fecddc80761f601eb88b7447eab8df6daf72a9ab98d0b';
const binding = {identity, implementation_digest: digest, key: identity + '@' + digest, descriptor, module: actual};
const nativeRegistry = bindComponentRegistry([binding]);
const appRegistry = configureComponentHost({modifierRegistry: {}}, [binding]).modifierRegistry;
const content = createElement('div', {style: {overflow: 'hidden', clipPath: 'inset(0 0 0 25%)'}}, 'same cropped alpha source');
const bounds = {status: 'known', rect: {x: 10, y: 20, width: 80, height: 40}};
const clip = {id: 'target', track: 'visual', at: 2, hold: 2, from: 7, speed: 2, keyframeOrigin: .25,
  modifiers: [{id: 'shade', element: identity, params: {strength: .2}}, {id: 'other', element: identity, params: {strength: .7}}]};
const path = modifierParameterAddress('shade', 'strength');
const pair = (interpolation = 'linear', easing) => [
  {time: 0, value: 0, interpolation, ...(easing === undefined ? {} : {easing}), opaque: {retain: [null, false, 1.125]}},
  {time: 1, value: 1, interpolation: 'linear'},
];
const animated = (keys = pair()) => ({...clip, keyframes: {[path]: keys, 'literal.key[0]': [{legacy: 'opaque'}]}});
const node = value => {assert.ok(isValidElement(value)); return value;};
function run(host, target = animated(), frame = 10, globalFrame = 50) {
  if (host === 'app') return node(composeAppClipModifiers({clip: target, content, frame, fps: 20, bounds,
    host: {registry: appRegistry, theme: {}, globalFrame}}));
  return node(composeModifiers({instances: target.modifiers, registry: nativeRegistry, content, host: 'composition',
    context: {clip: target, frame, fps: 20, keyframeFrame: frame - target.keyframeOrigin * 20,
      keyframeTime: (target.at + frame / 20) - (target.at + target.keyframeOrigin), globalFrame, bounds, theme: {}}}));
}
const shade = output => output.key === 'shade' ? output : node(output.props.children);

test('actual native ClipLook supplies the evaluated origin clock through cropped faded transition-handle content', () => {
  const theme = {...DEFAULT_THEME, color: DEFAULT_THEME.visual.color,
    type: DEFAULT_THEME.visual.type, motion: DEFAULT_THEME.visual.motion};
  const target = {...animated(), clipType: 'media', opacity: .4, effects: {fade_in: 1}, volume: .7};
  const before = structuredClone(target);
  for (const [frame, expected] of [[0, 0], [10, .25], [39, 1]]) {
    const tree = node(composeClipLook({clip: target, fps: 20, kind: 'media', children: content,
      modifierRegistry: nativeRegistry, modifierBounds: bounds, globalFrame: 50}, frame, theme));
    const modifier = shade(node(tree.props.children));
    assert.equal(modifier.props.params.strength, expected);
    assert.equal(modifier.props.context.globalFrame, 50);
    assert.strictEqual(modifier.props.children, content);
    if (frame === 10) assert.equal(tree.props.style.opacity, .2);
  }
  assert.deepEqual(target, before);
  assert.throws(() => composeClipLook({clip: {...target, modifiers: []}, fps: 20, kind: 'media', children: content,
    modifierRegistry: nativeRegistry, modifierBounds: bounds, globalFrame: 50}, 10, theme), /Unknown modifier instance/);
});

test('both actual descriptor hosts sample real J at endpoints and intermediate target time exactly once', () => {
  for (const host of ['app', 'composition']) {
    for (const [frame, expected] of [[0, 0], [5, 0], [10, .25], [15, .5], [25, 1], [39, 1]]) {
      const output = shade(run(host, undefined, frame));
      assert.ok(Math.abs(output.props.params.strength - expected) < 1e-12);
      assert.equal(output.props.context.globalFrame, 50);
      assert.ok(Math.abs(output.props.context.keyframeTime - (frame / 20 - .25)) < 1e-12);
      assert.strictEqual(output.props.children, content);
    }
    assert.equal(shade(run(host, undefined, 10, 500)).props.params.strength, .25);
    assert.equal(shade(run(host, {...animated(), from: 100, speed: .5})).props.params.strength, .25);
  }
});

test('both actual hosts preserve outgoing hold and named easing including boundary validation', () => {
  for (const host of ['app', 'composition']) {
    assert.equal(shade(run(host, animated(pair('hold')))).props.params.strength, 0);
    assert.equal(shade(run(host, animated(pair('linear', 'in')))).props.params.strength, .0625);
    for (const frame of [0, 10, 39]) assert.throws(() => run(host, animated(pair('linear', 'bogus')), frame), /unknown motion easing/);
  }
});

test('stable-first duplicate times validate every authored endpoint without rewriting opaque channels', () => {
  for (const host of ['app', 'composition']) {
    const keys = [pair()[0], {...pair()[0], value: .9}, pair()[1]];
    const target = animated(keys), before = structuredClone(target);
    assert.equal(shade(run(host, target)).props.params.strength, .25);
    assert.deepEqual(target, before);
    keys[1].value = 2;
    assert.throws(() => run(host, animated(keys)));
  }
});

test('empty channel preserves static params and ID reorder preserves selected instance and other occurrence', () => {
  for (const host of ['app', 'composition']) {
    assert.equal(shade(run(host, animated([]))).props.params.strength, .2);
    const reversed = {...animated(), modifiers: [...clip.modifiers].reverse()};
    const output = run(host, reversed);
    assert.equal(output.key, 'shade'); assert.equal(output.props.params.strength, .25);
    const other = node(output.props.children);
    assert.equal(other.key, 'other'); assert.equal(other.props.params.strength, .7);
    assert.equal(shade(run(host, {...clip, id: 'other-occurrence'})).props.params.strength, .2);
  }
});

test('D quoted ID serializer and reserved path parser reject ambiguity without claiming opaque legacy names', () => {
  for (const id of ['shade', 'quote"slash\\', 'é😀']) {
    const address = modifierParameterAddress(id, 'strength');
    assert.deepEqual(parseModifierParameterAddress(address), {id, leaf: 'strength'});
  }
  assert.equal(parseModifierParameterAddress('literal.key[0]'), undefined);
  assert.equal(parseModifierParameterAddress('modifiersLegacy'), undefined);
  assert.deepEqual(parseModifierParameterAddress(modifierParameterAddress('shade', 'strengthé')), {id: 'shade', leaf: 'strengthé'});
  for (const address of ['modifiers', 'modifiers.strength', 'modifiers[0].params.strength',
    "modifiers['shade'].params.strength", 'modifiers["shade"].params', 'modifiers["shade"].params.nested.x',
    'modifiers["\\u0073hade"].params.strength', 'modifiers[""].params.strength']) {
    assert.throws(() => parseModifierParameterAddress(address), /modifier/);
  }
});

test('both actual hosts refuse malformed channels unknown owners leaves and invalid static or endpoint values', () => {
  const channels = [null, {}, [{time: NaN, value: 0, interpolation: 'linear'}],
    [{time: Infinity, value: 0, interpolation: 'hold'}], [{time: 0, value: Infinity, interpolation: 'linear'}],
    [{time: 0, value: '0', interpolation: 'linear'}], [{time: 0, value: false, interpolation: 'hold'}],
    [{time: 0, value: 2, interpolation: 'linear'}], [{time: 0, value: -.1, interpolation: 'linear'}],
    [{time: 0, value: .5, interpolation: 'frames'}], [{time: 0, value: .5, interpolation: 'linear', easing: 2}]];
  for (const host of ['app', 'composition']) {
    for (const keys of channels) assert.throws(() => run(host, animated(keys)));
    for (const address of ['modifiers["foreign"].params.strength', 'modifiers["shade"].params.radius', 'modifiers[0].params.strength']) {
      assert.throws(() => run(host, {...clip, keyframes: {[address]: pair()}}));
    }
    assert.throws(() => run(host, {...animated(), modifiers: [{...clip.modifiers[0], params: {strength: 2}}]}));
    assert.throws(() => run(host, {...animated(), modifiers: []}));
  }
});

test('cross-field and discrete descriptor constraints refuse animated admission explicitly', () => {
  for (const schema of [{...descriptor.params, allOf: [{type: 'object'}]}, {...descriptor.params,
    properties: {strength: {...descriptor.params.properties.strength, multipleOf: .1}}}]) {
    const modified = {...binding, descriptor: {...descriptor, params: schema}};
    const registry = configureComponentHost({modifierRegistry: {}}, [modified]).modifierRegistry;
    const target = {...animated(), modifiers: clip.modifiers.map(instance => ({...instance, params: {strength: 0}}))};
    assert.throws(() => composeAppClipModifiers({clip: target, content, frame: 10, fps: 20, bounds,
      host: {registry, theme: {}, globalFrame: 50}}), /descriptor|Unsupported animated/);
  }
});

test('schema-backed authored compiled saved fresh readback resolves on both real hosts', () => {
  const readback = JSON.parse(readFileSync(config.readback, 'utf8'));
  const target = readback.target;
  assert.equal(target.modifiers[0].element, identity);
  assert.deepEqual(target.keyframes[path], readback.authoredKeys[path]);
  assert.deepEqual(target.keyframes['literal.key[0]'], readback.authoredKeys['literal.key[0]']);
  for (const host of ['app', 'composition']) {
    const output = shade(run(host, target, 10));
    assert.equal(output.props.params.strength, .25);
    assert.equal(output.props.context.globalFrame, 50);
  }
});
