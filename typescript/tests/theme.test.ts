import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createElement, type ReactElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {DEFAULT_THEME, ThemeProvider, useTheme, toRuntimeTheme, TimelineComposition,
  prepareCompositionScene, querySceneFrame, resolveElementRegistries, type Theme, type RuntimeTheme,
  type EffectProps, type TrackDefinition, type CompositionRegistries} from '../src/index';
import {DEFAULT_THEME as apiDefault} from '../src/theme-api';

const track: TrackDefinition = {id: 'visual', kind: 'visual', label: 'Visual'};
const clip = {id: 'title', track: track.id, at: 0, hold: 2, clipType: 'text-card',
  params: {content: 'Title', typewriter: false, entrance: 'none', exit: 'none'}};
const assets = {assets: {}};

const render = (content: ReactElement) => {
  const video = {id: 'test', width: 1920, height: 1080, fps: 30, durationInFrames: 60,
    defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
    nonce: [], schema: null, calculateMetadata: null, stack: null};
  return renderToStaticMarkup(createElement(Internals.CompositionManager.Provider, {
    value: {compositions: [video], currentCompositionMetadata: null, folders: [],
      canvasContent: {type: 'composition', compositionId: 'test'}},
  }, createElement(Internals.TimelineContext.Provider, {
    value: {frame: {test: 24}, playing: false, imperativePlaying: {current: false}, audioAndVideoTags: {current: []}},
  }, createElement(Internals.CanUseRemotionHooksProvider, null, content))));
};

test('public default preserves the complete existing export style', () => {
  // FINAL PLAN / INBOX 2026-10-20 06:18Z: implicit preview changes; exports stay unchanged.
  assert.strictEqual(DEFAULT_THEME, apiDefault);
  assert.deepEqual(DEFAULT_THEME, {
    id: 'banodoco-default',
    visual: {
      color: {fg: '#FAFAFA', bg: '#050814', accent: '#67E8F9'},
      type: {
        families: {heading: 'Arial', body: 'Arial', mono: 'monospace'},
        size: {base: 32, small: 22, large: 84},
        weight: {normal: 400, bold: 600},
        lineHeight: 1.2,
      },
      motion: {fadeMs: 450},
      canvas: {width: 1920, height: 1080, fps: 30},
    },
  });
  let observed: RuntimeTheme | undefined;
  const Probe = () => {observed = useTheme(); return null;};
  renderToStaticMarkup(createElement(Probe));
  assert.deepEqual(observed, toRuntimeTheme(DEFAULT_THEME));
  renderToStaticMarkup(createElement(ThemeProvider, {children: createElement(Probe)}));
  assert.deepEqual(observed, toRuntimeTheme(DEFAULT_THEME));
  const markup = render(createElement(TimelineComposition, {
    timeline: {theme: 'default', tracks: [track], clips: [clip]}, assets,
  }));
  assert.match(markup, /^<div style="[^"]*background-color:#050814(?:;|")/);
  assert.match(markup, /color:#FAFAFA/);
  assert.match(markup, /font-family:Arial/);
  assert.match(markup, /font-size:32px/);
  assert.match(markup, /font-weight:400/);
  assert.match(markup, /line-height:1.2/);
  assert.match(markup, /<span>Title<\/span>/);
});

const explicit: Theme = {
  id: 'film-pinned',
  visual: {
    color: {fg: '#123456', bg: '#234567', accent: '#345678'},
    type: {
      families: {heading: 'Film Heading', body: 'Film Body', mono: 'Film Mono'},
      size: {base: 51, small: 27, large: 109},
      weight: {normal: 300, bold: 800}, lineHeight: 1.7,
    },
    motion: {fadeMs: 730}, canvas: {width: 1280, height: 720, fps: 24},
  },
};

// Composition accepts resolved themes; a partial nested override is resolved by the caller.
const partialOverride: Theme = {...explicit, visual: {...explicit.visual,
  color: {...explicit.visual.color, accent: '#abcdef'},
  type: {...explicit.visual.type, families: {heading: 'Film Heading', body: 'Film Body'}},
}};

for (const [name, selected] of [['full', explicit], ['partial nested override without optional mono', partialOverride]] as const) {
  test(`explicit ${name} stays intact through provider, evaluator and SSR`, () => {
    const before = structuredClone(selected);
    const observed: RuntimeTheme[] = [];
    const Probe = () => {observed.push(useTheme()); return null;};
    renderToStaticMarkup(createElement(ThemeProvider, {value: selected, children: createElement(Probe)}));
    assert.deepEqual(observed.pop(), toRuntimeTheme(before));
    const evaluated: RuntimeTheme[] = [];
    const rendered: RuntimeTheme[] = [];
    const Plate = Object.assign(({theme}: EffectProps) => {rendered.push(theme); return createElement(Probe);}, {
      prepareSceneCapability: () => {
        return {identity: 'theme-probe@1', frame: () => ({presence: 'present' as const,
          opaqueSupport: 'rect' as const, bounds: {status: 'known' as const,
            rect: {x: 0, y: 0, width: 1920, height: 1080}}})};
      },
    });
    const registries: CompositionRegistries = {
      effects: {...resolveElementRegistries(toRuntimeTheme(selected)).effects, plate: Plate},
      transitions: {observe: ({theme}) => {
        evaluated.push(theme);
        return {presentation: null, timing: null};
      }},
    };
    const clips = [{...clip, transition: 'observe'}, {...clip, id: 'probe', clipType: 'plate', at: 2}];
    const scene = prepareCompositionScene([{track, clips}], assets, 30, toRuntimeTheme(selected),
      1920, 1080, undefined, undefined, {}, '', {}, registries);
    assert.equal(querySceneFrame(scene, 60).layers[0].visible, true);
    assert.deepEqual(evaluated, [toRuntimeTheme(before)]);
    const markup = render(createElement(TimelineComposition, {
      timeline: {theme: 'default', tracks: [track], clips: [clip, {...clips[1], at: 0}]},
      assets, theme: selected, registries,
    }));
    assert.deepEqual(rendered, [toRuntimeTheme(before)]);
    assert.deepEqual(observed, [toRuntimeTheme(before)]);
    assert.match(markup, /^<div style="[^"]*background-color:#234567(?:;|")/);
    assert.match(markup, /color:#123456/);
    assert.match(markup, /font-family:Film Heading/);
    assert.match(markup, /font-size:51px/);
    assert.match(markup, /font-weight:300/);
    assert.match(markup, /line-height:1.7/);
    assert.deepEqual(selected, before);
  });
}

test('public Composition consumes a custom Runtime-pinned theme carrier', () => {
  const selected = structuredClone(explicit);
  const markup = render(createElement(TimelineComposition, {
    timeline: {theme: 'film-pinned', tracks: [track], clips: [clip]}, assets, theme: selected,
  }));

  assert.match(markup, /^<div style="[^"]*background-color:#234567(?:;|")/);
  assert.match(markup, /color:#123456/);
  assert.match(markup, /font-family:Film Heading/);
  assert.match(markup, /font-size:51px/);
  assert.match(markup, /font-weight:300/);
  assert.match(markup, /line-height:1.7/);
  assert.deepEqual(selected, explicit);
});

test('public Composition consumes nested-merged theme fields without default fallback', () => {
  const selected = structuredClone(partialOverride);
  const markup = render(createElement(TimelineComposition, {
    timeline: {theme: 'film-pinned', tracks: [track], clips: [clip]}, assets, theme: selected,
  }));

  assert.match(markup, /^<div style="[^"]*background-color:#234567(?:;|")/);
  assert.match(markup, /color:#123456/);
  assert.match(markup, /font-family:Film Heading/);
  assert.match(markup, /font-size:51px/);
  assert.match(markup, /font-weight:300/);
  assert.match(markup, /line-height:1.7/);
  assert.deepEqual(selected, partialOverride);
});
