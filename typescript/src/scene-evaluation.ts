/** Pure requested-frame scene answers. Undeclared component pixels remain unknown. */
import {prepareTrack, queryTrackFrame, type PreparedTrack, type TransitionSpec, type IncomingTransitionSpec} from './evaluation';
import {getClipDurationInFrames} from './lib/duration';
import {animationElapsed, clipOpacity, fadeMultiplier, normalizeAnimationRefs, remappedFrame,
  type AnimationReferenceItem} from './lib/clip-look';
import {builtinClipLookStyle} from './lib/clip-look-animation';
import {admitModifiers} from './lib/modifier-admission';
import {mediaModifierBounds} from './lib/modifier-bounds';
import type {AssetRegistry, TimelineClip, TrackDefinition} from './types';
import {provenOpaqueMedia, type SceneCapabilities, type ComponentDiagnostics} from './scene-capabilities';
import type {ModifierRegistry, ModifierBounds} from './modifier-types';
import {computeRenderBounds, getVisibleBoundsFromCrop, type RenderBounds} from './lib/render-bounds';

export type SceneFinding = {code: string; clipId: string; reason: string; instanceId?: string; element?: string};
export type SceneTrackInput = {track: TrackDefinition; clips: readonly TimelineClip[];
  transitions: readonly (TransitionSpec | null)[];
  incomingTransitions?: readonly (IncomingTransitionSpec | null)[]};
export type PreparedScene = {tracks: (SceneTrackInput & {prepared: PreparedTrack})[];
  assets: AssetRegistry; fps: number; width: number; height: number;
  capabilities: SceneCapabilities; elements: ReadonlySet<string>; modifiers: ModifierRegistry; roles: Readonly<Record<string, string>>};
export type SceneLayer = {clipId: string; track: string; clipIndex: number; z: number;
  drawLocalFrame: number; ownFrame: number; contentFrame: number; transitionOpacity: number; opacity: number | null;
  visible: boolean | 'unknown';
  /** Evaluated target geometry, independent of uncertain modified output bounds. */
  targetBounds: ModifierBounds; bounds: ModifierBounds; role: string; fullFrame: boolean;
  opaqueSupport: 'rect' | 'none' | 'unknown';
  diagnostics?: ComponentDiagnostics;
  coverage: 'covered' | 'partial' | 'unknown'; findings: SceneFinding[]; dip: boolean};
export type SceneFrame = {frame: number; width: number; height: number; layers: SceneLayer[]; coverage: 'COVERED' | 'DIP' | 'GAP' | 'UNKNOWN';
  content: 'CONTENT' | 'EMPTY' | 'UNKNOWN' | null; findings: SceneFinding[]};
export type SceneOcclusion = {status: 'known'; occluderId: string | null; fraction: number}
  | {status: 'unknown'; reason: string};

// Consume already-admitted projection timing only when the caller explicitly opts in.
const occurrenceEndFrame = (clip: TimelineClip, fps: number): number | undefined => {
  const timing = (clip as TimelineClip & {app?: {canonicalTiming?: {occurrenceStartMs?: unknown;
    occurrenceDurationMs?: unknown}}}).app?.canonicalTiming;
  if (timing === undefined) return undefined;
  if (!timing || typeof timing !== 'object' || Array.isArray(timing)) {
    throw new Error('transition/invalid-span: Malformed canonical occurrence cap');
  }
  const {occurrenceStartMs: start, occurrenceDurationMs: duration} = timing;
  if (start === undefined && duration === undefined) return undefined;
  if (typeof start !== 'number' || !Number.isFinite(start) || start < 0
      || typeof duration !== 'number' || !Number.isFinite(duration) || duration < 0) {
    throw new Error('transition/invalid-span: Malformed canonical occurrence cap');
  }
  return Math.ceil(((start + duration) / 1000) * fps);
};

// Track input order is bottom to top, exactly Composition's painter order.
export const prepareScene = (tracks: readonly SceneTrackInput[], assets: AssetRegistry,
  fps: number, width: number, height: number, options: {elements?: ReadonlySet<string>;
    capabilities?: SceneCapabilities; modifiers?: ModifierRegistry; roles?: Readonly<Record<string, string>>} = {}): PreparedScene => {
  if (![fps, width, height].every(value => Number.isFinite(value) && value > 0)) throw new Error('evaluation_inputs_invalid');
  return {tracks: tracks.map(input => ({...input, prepared: prepareTrack(input.clips.map(clip => ({
    start: Math.round(clip.at * fps), duration: getClipDurationInFrames(clip, fps),
    ...(input.incomingTransitions === undefined ? {} : {endCap: occurrenceEndFrame(clip, fps)})})), input.transitions, input.incomingTransitions)})),
    assets, fps, width, height, capabilities: options.capabilities ?? {}, elements: options.elements ?? new Set(), modifiers: options.modifiers ?? {}, roles: options.roles ?? {}};
};

const validRect = (rect: RenderBounds): boolean => [rect.x, rect.y, rect.width, rect.height,
  rect.x + rect.width, rect.y + rect.height].every(Number.isFinite) && rect.width >= 0 && rect.height >= 0;
const clippedRect = (bounds: ModifierBounds, width: number, height: number): RenderBounds | null => {
  if (bounds.status !== 'known' || !validRect(bounds.rect)) return null;
  const rect = bounds.rect;
  const x = Math.max(0, Math.min(width, rect.x));
  const y = Math.max(0, Math.min(height, rect.y));
  return {x, y, width: Math.max(0, Math.min(width, rect.x + rect.width) - x),
    height: Math.max(0, Math.min(height, rect.y + rect.height) - y)};
};

type ClipLookEntrance = {status: 'inactive'} | {status: 'active'; opacity: number;
  translateY?: number; scale?: number} | {status: 'unknown'; reason: string};

const clipLookEntrance = (clip: TimelineClip, frame: number, fps: number): ClipLookEntrance => {
  if (clip.entrance === undefined) return {status: 'inactive'};
  try {
    const normalized = normalizeAnimationRefs(clip.entrance, fps);
    const refs = normalized === undefined ? [] : Array.isArray(normalized) ? normalized : [normalized];
    if (refs.length !== 1) return {status: 'unknown', reason: 'Entrance animation composition is undeclared'};
    const ref = refs[0] as AnimationReferenceItem;
    const id = typeof ref === 'string' ? ref : ref.id;
    if (id !== 'fade-up' && id !== 'scale-in') {
      return {status: 'unknown', reason: `Entrance animation '${id}' is undeclared`};
    }
    const configured = typeof ref === 'string' ? undefined : ref.durationFrames;
    // Both admitted built-in clip-look animations use the same generated
    // default duration; keep this pure path independent of component registries.
    const duration = configured ?? 18;
    if (typeof duration !== 'number' || !Number.isFinite(duration) || duration < 0) {
      return {status: 'unknown', reason: `Entrance animation '${id}' has no valid duration`};
    }
    const elapsed = animationElapsed('entrance', frame, getClipDurationInFrames(clip, fps), duration);
    if (elapsed === null) return {status: 'inactive'};
    const easing = typeof ref === 'string' ? undefined : ref.easing ?? ref.params?.easing;
    return {status: 'active', ...builtinClipLookStyle(id, elapsed, duration, fps, easing)};
  } catch (error) {
    return {status: 'unknown', reason: error instanceof Error ? error.message : String(error)};
  }
};

const transformBounds = (bounds: ModifierBounds, style: Extract<ClipLookEntrance, {status: 'active'}>,
  width: number, height: number): ModifierBounds => {
  if (bounds.status !== 'known') return bounds;
  const rect = style.scale === undefined ? {...bounds.rect, y: bounds.rect.y + (style.translateY ?? 0)} : {
    x: width / 2 + (bounds.rect.x - width / 2) * style.scale,
    y: height / 2 + (bounds.rect.y - height / 2) * style.scale,
    width: bounds.rect.width * style.scale,
    height: bounds.rect.height * style.scale,
  };
  return {status: 'known', rect: computeRenderBounds(rect, width, height)};
};

// ClipLook applies element crop to its full-canvas outer AbsoluteFill. The
// entrance wrapper is inside that crop, so transform first and intersect with
// the canvas crop region afterwards.
const applyElementCrop = (bounds: ModifierBounds, clip: TimelineClip,
  width: number, height: number): ModifierBounds => {
  if (bounds.status !== 'known') return bounds;
  const crop = getVisibleBoundsFromCrop({x: 0, y: 0, width, height}, clip);
  const rect = bounds.rect;
  return {status: 'known', rect: computeRenderBounds({
    x: Math.max(rect.x, crop.x),
    y: Math.max(rect.y, crop.y),
    width: Math.max(0, Math.min(rect.x + rect.width, crop.x + crop.width) - Math.max(rect.x, crop.x)),
    height: Math.max(0, Math.min(rect.y + rect.height, crop.y + crop.height) - Math.max(rect.y, crop.y)),
  }, width, height)};
};

// Shared by visibility and the public threshold query. Upper layers are front first.
const occlusionForLayer = (target: SceneLayer | undefined, upper: readonly SceneLayer[],
  width: number, height: number, minimumFraction: number): SceneOcclusion => {
  const none: SceneOcclusion = {status: 'known', occluderId: null, fraction: 0};
  if (!target || target.opacity === 0) return none;
  const rect = clippedRect(target.bounds, width, height);
  if (!rect) return {status: 'unknown', reason: 'Target output bounds are unknown'};
  if (rect.width === 0 || rect.height === 0) return none;
  let uncertain = false;
  for (const top of upper) {
    if (top.visible === false || (top.opacity !== null && top.opacity < 1)) continue;
    const covering = clippedRect(top.bounds, width, height);
    if (!covering) {uncertain = true; continue;}
    const overlapWidth = Math.max(0, Math.min(rect.x + rect.width, covering.x + covering.width) - Math.max(rect.x, covering.x));
    const overlapHeight = Math.max(0, Math.min(rect.y + rect.height, covering.y + covering.height) - Math.max(rect.y, covering.y));
    const fraction = (overlapWidth / rect.width) * (overlapHeight / rect.height);
    if (fraction < minimumFraction) continue;
    if (top.visible === true && top.opaqueSupport === 'rect' && top.opacity === 1 && top.coverage !== 'unknown') {
      return {status: 'known', occluderId: top.clipId, fraction};
    }
    uncertain = true;
  }
  return uncertain ? {status: 'unknown', reason: 'Upper layer support or alpha is undeclared'} : none;
};

/** Single opaque rectangle covering a fraction of the canvas-clipped target bounds,
 * never pixel/glyph alpha coverage. Reads an existing answer without evaluating callbacks. */
export const querySceneOcclusion = (answer: SceneFrame, clipId: string, minimumFraction: number): SceneOcclusion => {
  if (![answer.width, answer.height].every(value => Number.isFinite(value) && value > 0)
      || !Number.isFinite(minimumFraction) || minimumFraction <= 0 || minimumFraction > 1) {
    throw new Error('evaluation_inputs_invalid');
  }
  const index = answer.layers.findIndex(layer => layer.clipId === clipId);
  return occlusionForLayer(answer.layers[index], index < 0 ? [] : answer.layers.slice(index + 1).reverse(),
    answer.width, answer.height, minimumFraction);
};

const componentDiagnostics = (source: ComponentDiagnostics, geometryReason: string | undefined,
  invalid: (reason: string) => void): ComponentDiagnostics => {
  const region = (bounds: ModifierBounds): ModifierBounds => {
    if (geometryReason) return {status: 'unknown', reason: geometryReason};
    if (bounds.status === 'known' && !validRect(bounds.rect)) {
      invalid('Diagnostic region must have finite coordinates and nonnegative dimensions');
      return {status: 'unknown', reason: 'Invalid diagnostic region'};
    }
    return bounds;
  };
  const result: ComponentDiagnostics = {};
  if (source.motion !== undefined) {
    const motion = source.motion;
    const prototype = motion !== null && typeof motion === 'object' ? Object.getPrototypeOf(motion) : undefined;
    if (prototype !== Object.prototype && prototype !== null) invalid('Intrinsic motion must be a plain numeric record');
    else if (Object.values(motion).every(value => typeof value === 'number' && Number.isFinite(value))) result.motion = {...motion};
    else invalid('Intrinsic motion scalars must be finite numbers');
  }
  if (source.face !== undefined) result.face = region(source.face);
  if (source.mouth !== undefined) result.mouth = region(source.mouth);
  if (source.text !== undefined) {
    result.text = {bounds: region(source.text.bounds)};
    if (source.text.minPx !== undefined) {
      if (!Number.isFinite(source.text.minPx) || source.text.minPx <= 0) invalid('Minimum text size must be positive and finite');
      else if (!geometryReason) result.text.minPx = source.text.minPx;
    }
  }
  return result;
};

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
      const support = capability?.frame(remappedFrame(draw.contentFrame, clip.speed));
      const targetBounds: ModifierBounds = element && support ? support.bounds : element ? {status: 'unknown', reason: 'Component has no declared evaluated bounds'}
        : mediaModifierBounds(clip, track, asset, scene.width, scene.height);
      let bounds = targetBounds;
      let opacity: number | null = Math.min(1, Math.max(0, track.opacity ?? 1))
        * clipOpacity(clip, draw.contentFrame, scene.fps) * draw.opacity;
      let clipLookChanged = false;
      const instances = clip.modifiers ?? [];
      // An assetless native layer draws nothing; an unresolved referenced asset
      // is still unknown and cannot acquire valid absence from missing media.
      const absent = support?.presence === 'absent' || clip.clipType === 'effect-layer' || (!element && !clip.asset);
      if (element && !absent && (!support || support.presence === 'unknown' || support.opaqueSupport === 'unknown')) unknown('unknown-component-internals', 'Final component alpha and support are undeclared');
      const hasCrop = [clip.cropTop, clip.cropBottom, clip.cropLeft, clip.cropRight]
        .some(value => value !== undefined && value !== 0);
      if (element && hasCrop && instances.length) {
        unknown('unknown-animation-geometry', 'Element crop inside a custom modifier is undeclared');
        bounds = {status: 'unknown', reason: 'Element crop inside a custom modifier is undeclared'};
      }
      const entrance = clipLookEntrance(clip, draw.contentFrame, scene.fps);
      if (entrance.status === 'unknown') {
        unknown('unknown-animation-geometry', entrance.reason);
        bounds = {status: 'unknown', reason: entrance.reason};
      } else if (entrance.status === 'active') {
        opacity = opacity === null ? null : Math.min(1, Math.max(0, opacity * entrance.opacity));
        bounds = transformBounds(bounds, entrance, scene.width, scene.height);
        clipLookChanged = true;
      }
      if (element && hasCrop && !instances.length) {
        bounds = applyElementCrop(bounds, clip, scene.width, scene.height);
        clipLookChanged = true;
      }
      if (clip.exit !== undefined) {
        unknown('unknown-animation-geometry', 'Exit animation does not declare evaluated support and alpha');
        bounds = {status: 'unknown', reason: 'Exit animation geometry is undeclared'};
      }
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
        || fadeMultiplier(clip, draw.contentFrame, scene.fps) < 1);
      const geometryReason = bounds.status === 'unknown' ? bounds.reason
        : instances.length ? 'Modifiers do not declare internal region positions or text size'
        : clipLookChanged ? 'Clip look changes outer geometry or alpha' : undefined;
      const diagnostics = support?.diagnostics === undefined ? undefined : componentDiagnostics(support.diagnostics,
        geometryReason, reason => unknown('invalid-component-diagnostics', reason));
      layers.push({clipId: clip.id, track: track.id, clipIndex: draw.clipIndex, z: 0,
        drawLocalFrame: draw.drawLocalFrame, ownFrame: draw.ownFrame, contentFrame: draw.contentFrame, transitionOpacity: draw.opacity,
        opacity, visible, opaqueSupport, targetBounds, bounds, fullFrame,
        role: (Object.prototype.hasOwnProperty.call(scene.roles, clip.id) ? scene.roles[clip.id] : undefined)
          ?? (track.id === 'plate' ? 'picture' : 'content'),
        ...(diagnostics === undefined ? {} : {diagnostics}),
        coverage: bounds.status === 'unknown' || uncertain ? 'unknown' : opaqueSupport === 'rect' && fullFrame && opacity! >= .999 ? 'covered' : 'partial', findings, dip});
    }
  }
  // Occlusion only from proven opaque support. Unknown/translucent layers never erase content.
  const front: SceneLayer[] = [];
  for (const layer of [...layers].reverse()) {
    layer.z = front.length;
    const occlusion = occlusionForLayer(layer, front, scene.width, scene.height, 1);
    if (occlusion.status === 'known' && occlusion.occluderId !== null) layer.visible = false;
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
  return {frame, width: scene.width, height: scene.height, layers, coverage, content, findings: layers.flatMap(layer => layer.visible !== false ? layer.findings
    : layer.findings.filter(item => item.code === 'modifier-admission-refused'))};
};
