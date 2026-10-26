import type {TransitionComponentResult, TransitionProps} from '../../../effects-types';

type CrossFadeParams = {
  easing?: string;
};

export const CrossFade = ({
  durationFrames,
  params,
}: TransitionProps<Record<string, unknown>>): TransitionComponentResult => {
  const typedParams = params as CrossFadeParams;
  return {
    presentation: {type: 'cross-fade', easing: typedParams.easing ?? 'linear'},
    timing: {type: 'linear', durationFrames},
  };
};

export default CrossFade;
