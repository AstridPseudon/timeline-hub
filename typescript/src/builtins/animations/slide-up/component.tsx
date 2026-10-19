import type {ReactElement} from 'react';
import {interpolate} from 'remotion';
import type {WrapperAnimationProps} from '../../../effects-types';

export const SlideUp = ({
  children,
  durationFrames,
  elapsedFrames,
  progress: explicitProgress,
}: WrapperAnimationProps): ReactElement => {
  const progress = explicitProgress ?? interpolate(elapsedFrames, [0, durationFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: 1 - progress,
        transform: `translateY(${explicitProgress === undefined ? interpolate(progress, [0, 1], [0, -30]) : -30 * progress}px)`,
      }}
    >
      {children}
    </div>
  );
};

export default SlideUp;
