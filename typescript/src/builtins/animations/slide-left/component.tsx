import type {ReactElement} from 'react';
import {interpolate, spring} from 'remotion';
import type {WrapperAnimationProps} from '../../../effects-types';

export const SlideLeft = ({
  children,
  fps,
  durationFrames,
  elapsedFrames,
  progress: explicitProgress,
}: WrapperAnimationProps): ReactElement => {
  const progress = explicitProgress ?? spring({
    frame: elapsedFrames,
    fps,
    from: 0,
    to: 1,
    durationInFrames: durationFrames,
    config: {damping: 14, stiffness: 110},
  });
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: progress,
        transform: `translateX(${explicitProgress === undefined ? interpolate(progress, [0, 1], [80, 0]) : 80 * (1 - progress)}px)`,
      }}
    >
      {children}
    </div>
  );
};

export default SlideLeft;
