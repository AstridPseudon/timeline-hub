import {prepareCompositionScene, toRuntimeTheme} from '@banodoco/timeline-composition';
import type {TimelineCompositionProps} from '@banodoco/timeline-composition';
import * as timelineComposition from '@banodoco/timeline-composition';
import {resolveHostRegistries} from './host-registries';

// Root's props and the selected composition's frame basis, without a second
// transition, capability or geometry implementation.
export const prepareHostScene = (props: TimelineCompositionProps,
  basis: {fps: number; width: number; height: number}, roles: Record<string, string>) => {
  if (!props.theme || !props.assets?.assets || !Array.isArray(props.timeline?.clips)
    || !Array.isArray(props.timeline.tracks)
    || ![basis.fps, basis.width, basis.height].every(n => Number.isFinite(n) && n > 0)) {
    throw new Error('scene requires exact Root props, explicit tracks and render frame basis');
  }
  const app = (props.timeline as typeof props.timeline & {app?: Record<string, unknown>}).app;
  if (app?.astrid_render_clock) {
    throw new Error('scene preparation does not evaluate Root RenderClockTail');
  }
  if (props.compiledTransitions !== undefined
    && typeof timelineComposition.compileCanonicalTransitions !== 'function') {
    throw new Error('scene compiled transition carrier unavailable in installed Composition API');
  }
  // TimelineComposition paints visual tracks in reverse authored order. Clip
  // sorting and all transition/default resolution belong to the public prepare.
  const tracks = [...props.timeline.tracks].reverse().filter(track => track.kind === 'visual')
    .map(track => ({track, clips: props.timeline.clips.filter(clip => clip.track === track.id)}));
  const theme = toRuntimeTheme(props.theme);
  return prepareCompositionScene(tracks, props.assets, basis.fps, theme,
    basis.width, basis.height, undefined, roles, {}, '', {}, resolveHostRegistries(theme),
    props.compiledTransitions);
};
