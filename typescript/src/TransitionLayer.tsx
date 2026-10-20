import type {ReactElement, ReactNode} from 'react';
import {AbsoluteFill, Freeze, useCurrentFrame} from 'remotion';
import {queryDrawFrame, type DrawPlan} from './evaluation';

// Wraps one clip's content inside its draw Sequence. Frames here are draw-local.
// Default extensions freeze at the own-span boundary. Opted-in incoming content
// keeps this draw-local clock, including preroll; opacity is purely visual.
export const composeTransitionLayer = ({
  plan,
  children,
}: {
  plan: DrawPlan;
  children: ReactNode;
}, frame: number): ReactElement => {
  const evaluated = queryDrawFrame(plan, frame);
  const extended = plan.drawDuration > plan.ownDuration;
  const body = extended && plan.incomingPolicy !== 'preroll-crossfade'
    ? <Freeze frame={evaluated.contentFrame}>{children}</Freeze>
    : children;

  // Decided per plan, not per frame, so the wrapper does not mount and unmount
  // (and remount media) when a ramp reaches 1.
  if (!plan.fadeIn && !plan.fadeOut) {
    return <>{body}</>;
  }
  return (
    <AbsoluteFill style={{opacity: evaluated.opacity}}>
      {body}
    </AbsoluteFill>
  );
};

export const TransitionLayer = (props: {plan: DrawPlan; children: ReactNode}): ReactElement =>
  composeTransitionLayer(props, useCurrentFrame());
