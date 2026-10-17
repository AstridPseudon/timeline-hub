/** Pure requested-frame scene answers. Undeclared component pixels remain unknown. */
import {prepareTrack, queryTrackFrame, type PreparedTrack, type TransitionSpec} from './evaluation';
import {getClipDurationInFrames} from './lib/duration';
import {clipOpacity, fadeMultiplier, remappedFrame} from './lib/clip-look';
import {admitModifiers} from './lib/modifier-admission';
import {mediaModifierBounds} from './lib/modifier-bounds';
import type {AssetRegistry, TimelineClip, TrackDefinition} from './types';
import {provenOpaqueMedia, type SceneCapabilities} from './scene-capabilities';
import type {ModifierRegistry, ModifierBounds} from './modifier-types';

export type SceneFinding = {code: string; clipId: string; reason: string; instanceId?: string; element?: string};
export type SceneTrackInput = {track: TrackDefinition; clips: readonly TimelineClip[];
  transitions: readonly (TransitionSpec | null)[]};
export type PreparedScene = {tracks: (SceneTrackInput & {prepared: PreparedTrack})[];
  assets: AssetRegistry; fps: number; width: number; height: number;
  capabilities: SceneCapabilities; elements: ReadonlySet<string>; modifiers: ModifierRegistry; roles: Readonly<Record<string, string>>};
export type SceneLayer = {clipId: string; track: string; clipIndex: number; z: number;
  drawLocalFrame: number; ownFrame: number; transitionOpacity: number; opacity: number | null;
  visible: boolean | 'unknown';
  /** Evaluated target geometry, independent of uncertain modified output bounds. */
  targetBounds: ModifierBounds; bounds: ModifierBounds; role: string; fullFrame: boolean;
  opaqueSupport: 'rect' | 'none' | 'unknown';
  coverage: 'covered' | 'partial' | 'unknown'; findings: SceneFinding[]; dip: boolean};
export type SceneFrame = {frame: number; layers: SceneLayer[]; coverage: 'COVERED' | 'DIP' | 'GAP' | 'UNKNOWN';
  content: 'CONTENT' | 'EMPTY' | 'UNKNOWN' | null; findings: SceneFinding[]};

// Track input order is bottom to top, exactly Composition's painter order.
export const prepareScene = (tracks: readonly SceneTrackInput[], assets: AssetRegistry,
  fps: number, width: number, height: number, options: {elements?: ReadonlySet<string>;
    capabilities?: SceneCapabilities; modifiers?: ModifierRegistry; roles?: Readonly<Record<string, string>>} = {}): PreparedScene => {
  if (![fps, width, height].every(value => Number.isFinite(value) && value > 0)) throw new Error('evaluation_inputs_invalid');
  return {tracks: tracks.map(input => ({...input, prepared: prepareTrack(input.clips.map(clip => ({
    start: Math.round(clip.at * fps), duration: getClipDurationInFrames(clip, fps)})), input.transitions)})),
    assets, fps, width, height, capabilities: options.capabilities ?? {}, elements: options.elements ?? new Set(), modifiers: options.modifiers ?? {}, roles: options.roles ?? {}};
};

const rectContains = (a: ModifierBounds, b: ModifierBounds): boolean => a.status === 'known' && b.status === 'known'
  && a.rect.x <= b.rect.x && a.rect.y <= b.rect.y
  && a.rect.x + a.rect.width >= b.rect.x + b.rect.width && a.rect.y + a.rect.height >= b.rect.y + b.rect.height;

// Exact rectangular support partition, using the renderer's evaluated bounds and alpha.
// This handles tiled pictures and overlapping translucent plates without inventing geometry.
const canvasCovered = (layers: SceneLayer[], width: number, height: number): boolean => {
  const known = layers.filter(layer => layer.opaqueSupport === 'rect' && layer.coverage !== 'unknown' && layer.bounds.status === 'known'
    && layer.opacity !== null && layer.opacity > 0);
  const rects = known.map(layer => ({rect: (layer.bounds as {status: 'known'; rect: {x: number; y: number; width: number; height: number}}).rect,
    opacity: layer.opacity as number}));
  const xs = [...new Set([0, width, ...rects.flatMap(({rect}) => [Math.max(0, Math.min(width, rect.x)), Math.max(0, Math.min(width, rect.x + rect.width))])])].sort((a, b) => a - b);
  for (let i = 0; i < xs.length - 1; i++) {
    const x = (xs[i] + xs[i + 1]) / 2;
    const active = rects.filter(({rect}) => rect.x <= x && rect.x + rect.width >= x);
    const ys = [...new Set([0, height, ...active.flatMap(({rect}) => [Math.max(0, Math.min(height, rect.y)), Math.max(0, Math.min(height, rect.y + rect.height))])])].sort((a, b) => a - b);
    for (let j = 0; j < ys.length - 1; j++) {
      const y = (ys[j] + ys[j + 1]) / 2;
      const alpha = 1 - active.filter(({rect}) => rect.y <= y && rect.y + rect.height >= y)
        .reduce((remaining, layer) => remaining * (1 - layer.opacity), 1);
      if (alpha < .999) return false;
    }
  }
  return true;
};

export const querySceneFrame = (scene: PreparedScene, frame: number): SceneFrame => {
  if (!Number.isSafeInteger(frame) || frame < 0) throw new Error('evaluation_inputs_invalid');
  const layers: SceneLayer[] = [];
  for (const {track, clips, prepared} of scene.tracks) {
    for (const draw of queryTrackFrame(prepared, frame).layers) {
      const clip = clips[draw.clipIndex];
      const findings: SceneFinding[] = [];
      const unknown = (code: string, reason: string) => {findings.push({code, clipId: clip.id, reason});};
      const element = scene.elements.has(clip.clipType ?? '')
        || (!!clip.clipType && !['media', 'image', 'video', 'hold', 'effect-layer'].includes(clip.clipType));
      const asset = clip.asset ? scene.assets.assets[clip.asset] : undefined;
      const capability = element ? scene.capabilities.components?.[clip.id] : undefined;
      const support = capability?.frame(remappedFrame(draw.ownFrame, clip.speed));
      const targetBounds: ModifierBounds = element && support ? support.bounds : element ? {status: 'unknown', reason: 'Component has no declared evaluated bounds'}
        : mediaModifierBounds(clip, track, asset, scene.width, scene.height);
      let bounds = targetBounds;
      let opacity: number | null = Math.min(1, Math.max(0, track.opacity ?? 1))
        * clipOpacity(clip, draw.ownFrame, scene.fps) * draw.opacity;
      // An assetless native layer draws nothing; an unresolved referenced asset
      // is still unknown and cannot acquire valid absence from missing media.
      const absent = support?.presence === 'absent' || clip.clipType === 'effect-layer' || (!element && !clip.asset);
      if (element && !absent && (!support || support.presence === 'unknown' || support.opaqueSupport === 'unknown')) unknown('unknown-component-internals', 'Final component alpha and support are undeclared');
      if (clip.entrance !== undefined || clip.exit !== undefined
          || (element && [clip.cropTop, clip.cropBottom, clip.cropLeft, clip.cropRight].some(value => value !== undefined && value !== 0))) {
        unknown('unknown-animation-geometry', 'Animation does not declare evaluated support and alpha');
        bounds = {status: 'unknown', reason: 'Animation geometry is undeclared'};
      }
      const instances = clip.modifiers ?? [];
      if (targetBounds.status === 'unknown' && !absent) {
        unknown(instances.length ? 'unknown-target-bounds' : 'unknown-component-bounds', targetBounds.reason);
      }
      try {
        const declarations = admitModifiers(instances, scene.modifiers);
        declarations.forEach((declaration, index) => {
          if (declaration.bounds === 'unknown') {
            const reason = 'Modifier declares unknown output bounds';
            findings.push({code: 'unknown-modifier-bounds', clipId: clip.id,
              instanceId: instances[index].id, element: declaration.element, reason});
            bounds = {status: 'unknown', reason};
          }
        });
      } catch (error) {
        unknown('modifier-admission-refused', error instanceof Error ? error.message : String(error));
        bounds = {status: 'unknown', reason: 'Modifier admission refused'};
      }
      // Unresolved intrinsic alpha (e.g. PNG/video alpha) cannot establish opaque coverage.
      const opaqueMedia = provenOpaqueMedia(asset,
        clip.asset ? scene.capabilities.media?.[clip.asset] : undefined);
      let opaqueSupport: SceneLayer['opaqueSupport'] = element ? support?.opaqueSupport ?? 'unknown'
        : opaqueMedia ? 'rect' : 'unknown';
      if (track.blendMode && track.blendMode !== 'normal') {
        unknown('unknown-blend-support', 'Blend mode does not prove opaque support');
        opaqueSupport = 'unknown';
      }
      if (!absent && !element && !opaqueMedia) unknown('unknown-media-alpha', 'Media does not declare opaque alpha');
      const uncertain = findings.some(item => item.code !== 'unknown-component-bounds');
      let visible: boolean | 'unknown' = absent || opacity === 0 ? false : uncertain ? 'unknown' : true;
      // Known support outside the canvas draws no visible content. Keep its real
      // geometry (including negative/partial bounds) for downstream inspection.
      if (bounds.status === 'known' && (bounds.rect.width === 0 || bounds.rect.height === 0
          || (!uncertain && (bounds.rect.x >= scene.width || bounds.rect.y >= scene.height
            || bounds.rect.x + bounds.rect.width <= 0 || bounds.rect.y + bounds.rect.height <= 0)))) visible = false;
      if (visible !== false && uncertain) opacity = null;
      if (absent) {
        opacity = 0;
        const admissionFailures = findings.filter(item => item.code === 'modifier-admission-refused');
        findings.splice(0, findings.length, ...admissionFailures);
        opaqueSupport = 'none';
      }
      const fullFrame = bounds.status === 'known' && bounds.rect.x <= 0 && bounds.rect.y <= 0
        && bounds.rect.x + bounds.rect.width >= scene.width && bounds.rect.y + bounds.rect.height >= scene.height;
      const plan = prepared.plans[draw.clipIndex];
      const dip = !absent && (((plan.fadeIn?.kind === 'dip' || plan.fadeOut?.kind === 'dip') && draw.opacity < 1)
        || fadeMultiplier(clip, draw.ownFrame, scene.fps) < 1);
      layers.push({clipId: clip.id, track: track.id, clipIndex: draw.clipIndex, z: 0,
        drawLocalFrame: draw.drawLocalFrame, ownFrame: draw.ownFrame, transitionOpacity: draw.opacity,
        opacity, visible, opaqueSupport, targetBounds, bounds, fullFrame, role: scene.roles[clip.id] ?? (track.id === 'plate' ? 'picture' : 'content'),
        coverage: bounds.status === 'unknown' || uncertain ? 'unknown' : opaqueSupport === 'rect' && fullFrame && opacity! >= .999 ? 'covered' : 'partial', findings, dip});
    }
  }
  // Occlusion only from proven opaque support. Unknown/translucent layers never erase content.
  const front: SceneLayer[] = [];
  for (const layer of [...layers].reverse()) {
    layer.z = front.length;
    if (front.some(top => top.visible === true && top.opaqueSupport === 'rect' && top.opacity === 1 && top.coverage !== 'unknown'
      && rectContains(top.bounds, layer.bounds))) layer.visible = false;
    front.push(layer);
  }
  const visible = front.filter(layer => layer.visible !== false);
  const picture = visible.filter(layer => ['picture', 'background'].includes(layer.role));
  const covered = canvasCovered(picture, scene.width, scene.height);
  const unknownCoverage = visible.some(layer => layer.coverage === 'unknown');
  const coverage = covered ? 'COVERED' : unknownCoverage ? 'UNKNOWN' : layers.some(layer => ['picture', 'background'].includes(layer.role) && layer.dip) ? 'DIP' : 'GAP';
  const content = coverage !== 'COVERED' ? null : visible.some(layer => layer.role !== 'background'
    && layer.visible === true && (layer.opacity ?? 0) >= .05) ? 'CONTENT'
      : visible.some(layer => layer.role !== 'background' && layer.visible === 'unknown') ? 'UNKNOWN' : 'EMPTY';
  return {frame, layers, coverage, content, findings: layers.flatMap(layer => layer.visible !== false ? layer.findings
    : layer.findings.filter(item => item.code === 'modifier-admission-refused'))};
};
