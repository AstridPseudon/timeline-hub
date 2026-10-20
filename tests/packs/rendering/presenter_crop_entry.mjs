// Bind the existing TimelineComposition renderer to ordinary host discovery.
import {createElement as h} from 'react';
import {Composition, registerRoot} from 'remotion';
import {TimelineComposition, toRuntimeTheme} from '@banodoco/timeline-composition';
import {resolveHostRegistries} from './src/host-registries';

const HostTimeline = props => h(TimelineComposition, {...props,
  registries: resolveHostRegistries(toRuntimeTheme(props.theme))});
registerRoot(() => h(Composition, {id: 'presenter-crop', component: HostTimeline,
  width: 1920, height: 1080, fps: 30, durationInFrames: 60}));
