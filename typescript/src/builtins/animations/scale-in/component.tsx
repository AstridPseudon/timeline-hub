import type {ReactElement} from 'react';
import type {WrapperAnimationProps} from '../../../effects-types';
import {builtinClipLookStyle} from '../../../lib/clip-look-animation';

export const ScaleIn = ({
  children,
  fps,
  durationFrames,
  elapsedFrames,
  progress: suppliedProgress,
  easing,
}: WrapperAnimationProps): ReactElement => {
  const style = builtinClipLookStyle('scale-in', elapsedFrames, durationFrames, fps, easing, suppliedProgress);
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: style.opacity,
        transform: style.transform,
        transformOrigin: 'center center',
      }}
    >
      {children}
    </div>
  );
};

export default ScaleIn;
