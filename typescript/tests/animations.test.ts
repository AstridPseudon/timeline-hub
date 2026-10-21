import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createElement, type CSSProperties, type ReactElement, type ReactNode} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {ANIMATION_DEFAULTS, ANIMATION_META, ANIMATION_REGISTRY} from '../src/animations.generated';
import {ANIMATION_DEFAULTS as PURE_ANIMATION_DEFAULTS, ANIMATION_META as PURE_ANIMATION_META} from '../src/animation-metadata.generated';
import {DEFAULT_THEME, toRuntimeTheme} from '../src/ThemeContext';
import {ElementRegistryProvider, useElementRegistries} from '../src/RegistryContext';
import type {AnimationRegistries} from '../src/registries';
import type {BaseAnimationProps, HookAnimationProps, WrapperAnimationProps} from '../src/effects-types';
import {composeAnimations, resolveAnimationReferences} from '../src/lib/animations';
import {animationProgress, normalizeAnimationEasing} from '../src/lib/animation-easing';
import type {TimelineClip} from '../src/types';

const clip: TimelineClip = {id: 'title', track: 'v', at: 0, hold: 4, clipType: 'text-card'};
const input = {clip, phase: 'entrance' as const, content: 'abcdefgh', text: 'abcdefgh',
  theme: toRuntimeTheme(DEFAULT_THEME), fps: 30, elapsedFrames: 25};
const markup = (content: ReactNode) => renderToStaticMarkup(createElement('section', null, content));

test('pure animation metadata is the normal generated registry metadata', () => {
  assert.strictEqual(PURE_ANIMATION_DEFAULTS, ANIMATION_DEFAULTS);
  assert.strictEqual(PURE_ANIMATION_META, ANIMATION_META);
});

test('registration declares easing for new and overridden IDs, for hooks and wrappers', () => {
  const seen: BaseAnimationProps[] = [];
  const Wrapper = (props: WrapperAnimationProps) => {
    seen.push(props);
    return createElement('b', {'data-progress': props.progress}, props.children);
  };
  const Hook = (props: HookAnimationProps) => {
    seen.push(props);
    return {content: createElement('b', {'data-progress': props.progress}, props.content)};
  };
  for (const id of ['project-sweep', 'fade-up', 'type-on']) {
    for (const kind of ['hook', 'wrapper'] as const) {
      const registries: AnimationRegistries = {
        animations: {[id]: kind === 'hook' ? Hook : Wrapper},
        animationMeta: {[id]: {kind, phase: 'entrance', supportsEasing: true}},
        // These params belong to the host, even when it reuses the type-on ID.
        animationDefaults: {[id]: {durationFrames: 100, startFrame: 'host-owned', durationFraction: null}},
      };
      const before = structuredClone({meta: registries.animationMeta, defaults: registries.animationDefaults});
      const output = composeAnimations({...input, refs: {id, easing: 'in'}, registries});
      if (kind === 'wrapper') assert.strictEqual((output as ReactElement).type, Wrapper);
      assert.equal(markup(output), '<section><b data-progress="0.0625">abcdefgh</b></section>');
      const props = seen.at(-1)!;
      assert.equal(props.easing, 'in');
      assert.equal(props.progress, 0.0625);
      assert.equal(props.elapsedFrames, 25);
      assert.equal(props.durationFrames, 100);
      assert.equal(props.params.startFrame, 'host-owned');
      assert.deepEqual({meta: registries.animationMeta, defaults: registries.animationDefaults}, before);
    }
  }
});

test('replacing only a built-in component keeps the generic progress clock', () => {
  let observed: HookAnimationProps | undefined;
  const Custom = (props: HookAnimationProps) => {observed = props; return {content: 'host'};};
  assert.equal(composeAnimations({...input, refs: {id: 'type-on', durationFrames: 100, easing: 'linear'},
    registries: {animations: {'type-on': Custom}}}), 'host');
  assert.equal(observed?.progress, 0.25);
  assert.equal(observed?.elapsedFrames, 25);
  assert.equal(observed?.params.startFrame, 18);
});

test('explicit easing requires declared support, and defaults do not author a curve', () => {
  const Custom = ({progress, easing}: WrapperAnimationProps) => {
    assert.equal(progress, undefined);
    assert.equal(easing, undefined);
    return null;
  };
  for (const id of ['project-sweep', 'fade-up', 'type-on']) {
    for (const supportsEasing of [undefined, false]) {
      const registries: AnimationRegistries = {animations: {[id]: Custom},
        animationMeta: {[id]: {kind: 'wrapper', supportsEasing}},
        animationDefaults: {[id]: {durationFrames: 100, easing: 'ease-out'}}};
      assert.equal(markup(composeAnimations({...input, refs: id, registries})), '<section></section>');
      for (const ref of [{id, easing: 'linear'}, {id, params: {easing: 'linear'}}]) {
        assert.throws(() => resolveAnimationReferences(ref, 'entrance', registries), /cannot consume explicit easing/);
      }
    }
  }
});

test('two mounted registry scopes keep custom support, params and progress isolated', () => {
  const Custom = ({progress, params}: WrapperAnimationProps) =>
    createElement('b', {'data-progress': progress}, String(params.label));
  const scope = (label: string, durationFrames: number): AnimationRegistries => ({
    animations: {'project-sweep': Custom},
    animationMeta: {'project-sweep': {kind: 'wrapper', supportsEasing: true}},
    animationDefaults: {'project-sweep': {label, durationFrames}},
  });
  const first = scope('first', 100), second = scope('second', 50);
  const Animated = () => composeAnimations({...input, refs: {id: 'project-sweep', easing: 'linear'},
    registries: useElementRegistries()});
  const pair = () => markup([first, second].map((value, key) =>
    createElement(ElementRegistryProvider, {key, value, children: createElement(Animated)})));
  const expected = '<section><b data-progress="0.25">first</b><b data-progress="0.5">second</b></section>';
  assert.equal(pair(), expected);
  assert.throws(() => resolveAnimationReferences('project-sweep', 'entrance'), /Unknown animation/);
  assert.equal(pair(), expected);
});

test('bundled wrappers preserve normal motion and consume explicit progress themselves', () => {
  const style = (id: string, elapsedFrames: number, easing?: string): CSSProperties => {
    const phase = id === 'slide-up' || id === 'fade' ? 'exit' : 'entrance';
    const node = composeAnimations({...input, phase, elapsedFrames, refs: {id, durationFrames: 12, easing}}) as ReactElement;
    assert.strictEqual(node.type, ANIMATION_REGISTRY[id]);
    return ((node.type as (props: unknown) => ReactElement)(node.props).props as {style: CSSProperties}).style;
  };
  for (const id of ['fade', 'fade-up', 'scale-in', 'slide-left', 'slide-up']) {
    const exit = id === 'fade' || id === 'slide-up';
    assert.equal(style(id, 0).opacity, exit ? 1 : 0);
    assert.equal(style(id, 12).opacity, exit ? 0 : 1.002956228407837);
    assert.equal(style(id, 6, 'linear').opacity, 0.5);
    assert.equal(style(id, 6, 'ease-in').opacity, exit ? 0.75 : 0.25);
  }
  assert.equal(style('fade', 6).opacity, 0.5);
  assert.equal(style('slide-up', 6).transform, 'translateY(-15px)');
  assert.equal(style('fade-up', 6, 'linear').transform, 'translateY(20px)');
  assert.equal(style('slide-left', 6, 'linear').transform, 'translateX(40px)');
  assert.equal(style('scale-in', 6, 'linear').transform, 'scale(0.9249999999999999)');
  // Omitted easing still selects the spring, rather than implicit linear.
  assert.notEqual(style('fade-up', 6).opacity, 0.5);
});

test('type-on owns its reveal window under every ID and retains caret and hidden tail', () => {
  const id = 'project-reveal';
  const registries: AnimationRegistries = {animations: {[id]: ANIMATION_REGISTRY['type-on']},
    animationDefaults: {[id]: ANIMATION_DEFAULTS['type-on']}, animationMeta: {[id]: ANIMATION_META['type-on']}};
  for (const easing of [undefined, 'linear', 'ease-in', 'ease-out']) {
    for (const elapsedFrames of [0, 18, 42, 66, 120]) {
      assert.equal(markup(composeAnimations({...input, refs: {id, easing}, elapsedFrames, registries})),
        markup(composeAnimations({...input, refs: {id: 'type-on', easing}, elapsedFrames})));
    }
  }
  const reveal = (elapsedFrames: number, easing?: string, durationFrames = 20) =>
    markup(composeAnimations({...input, elapsedFrames, refs: {id, easing, durationFrames,
      params: {startFrame: 4, durationFraction: 0.6}}, registries}));
  assert.match(reveal(4, 'linear'), /^<section><span><span><\/span>/);
  assert.match(reveal(8, 'linear'), /^<section><span><span>abcd<\/span>/);
  assert.match(reveal(8, 'ease-in'), /^<section><span><span>ab<\/span>/);
  assert.match(reveal(8), /^<section><span><span>abcd<\/span>/);
  assert.match(reveal(12, 'linear'), /^<section><span><span>abcdefgh<\/span>/);
  assert.match(reveal(0, 'linear', 0), /^<section><span><span>abcdefgh<\/span>/);
  assert.match(reveal(8, 'linear'), /aria-hidden="true".*opacity:1/);
  assert.match(reveal(8, 'linear'), /<span style="opacity:0">efgh<\/span>/);
  assert.throws(() => composeAnimations({...input, refs: {id, easing: 'linear', params: {startFrame: 'invalid'}},
    registries}), /finite startFrame/);
});

test('generic curves retain aliases, clamping, zero duration and explicit spelling validation', () => {
  assert.equal(normalizeAnimationEasing('ease-in'), 'in');
  assert.equal(animationProgress(1, 4, 'in'), 0.0625);
  assert.equal(animationProgress(1, 4, 'out'), 0.4375);
  assert.equal(animationProgress(1, 4, 'inOut'), 0.125);
  assert.equal(animationProgress(1, 4, 'linear'), 0.25);
  assert.equal(animationProgress(3, 4, 'step'), 0);
  assert.equal(animationProgress(4, 4, 'step'), 1);
  assert.equal(animationProgress(-1, 4, 'linear'), 0);
  assert.equal(animationProgress(5, 4, 'linear'), 1);
  assert.equal(animationProgress(-1, 0, 'linear'), 0);
  assert.equal(animationProgress(0, 0, 'linear'), 1);
  assert.equal(animationProgress(1, 4, undefined), undefined);
  assert.throws(() => animationProgress(NaN, 4, 'linear'), /finite/);
  assert.throws(() => animationProgress(1, -1, 'linear'), /finite/);
  assert.throws(() => animationProgress(1, 4, 'bogus'), /unknown motion easing/);
  assert.doesNotThrow(() => resolveAnimationReferences({id: 'fade', easing: 'in', params: {easing: 'ease-in'}}, 'exit'));
  assert.throws(() => resolveAnimationReferences({id: 'fade', easing: 'in', params: {easing: 'out'}}, 'exit'), /Conflicting/);
});
