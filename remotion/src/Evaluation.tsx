// Host query adapter over the public pure planner. Inputs are already compiled
// track spans/transitions in frames, not a second timeline compiler. Mounted
// layers/transition opacity do not establish component visibility or coverage.
import {prepareTrack, queryTrackFrame} from '@banodoco/timeline-composition/evaluation';
import type {ClipSpan, TransitionSpec} from '@banodoco/timeline-composition/evaluation';

export type EvaluationProps = {
  spans: ClipSpan[];
  transitions: (TransitionSpec | null)[];
  frames: number[];
  evaluation?: ReturnType<typeof queryTrackFrame>[];
};

export const TrackEvaluation = (_props: EvaluationProps): null => null;

export const evaluationMetadata = ({props}: {props: EvaluationProps}) => {
  if (!Array.isArray(props.spans) || props.spans.length > 1024
      || !Array.isArray(props.transitions) || props.transitions.length > props.spans.length
      || !Array.isArray(props.frames) || props.frames.length < 1 || props.frames.length > 120
      || props.frames.some(frame => !Number.isSafeInteger(frame) || frame < 0)
      || props.spans.some(span => !Number.isSafeInteger(span.start) || span.start < 0
        || !Number.isSafeInteger(span.duration) || span.duration < 1)
      || props.transitions.some(value => value !== null && (
        !Number.isSafeInteger(value.T) || value.T < 0
        || !['dissolve', 'dip'].includes(value.kind)
        || !['start', 'center', 'end'].includes(value.align)))) {
    throw new Error('evaluation_inputs_invalid');
  }
  const prepared = prepareTrack(props.spans, props.transitions);
  return {props: {...props, evaluation: props.frames.map(frame => queryTrackFrame(prepared, frame))}};
};
