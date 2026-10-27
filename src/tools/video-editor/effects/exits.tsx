import type { FC } from 'react';
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import type { EffectComponentProps } from '@/tools/video-editor/effects/entrances.tsx';

const getExitProgress = (frame: number, durationInFrames: number, effectFrames: number, easing?: string): number => {
  const easingFunction = easing === undefined || easing === 'linear' ? Easing.linear
    : easing === 'in' || easing === 'ease-in' ? Easing.in(Easing.quad)
      : easing === 'out' || easing === 'ease-out' ? Easing.out(Easing.quad)
        : easing === 'in-out' || easing === 'inout' || easing === 'in_out' || easing === 'ease-in-out'
          ? Easing.inOut(Easing.quad)
          : easing === 'step' ? (progress: number) => progress < 1 ? 0 : 1
            : (() => { throw new Error(`unknown motion easing ${easing}`); })();
  return interpolate(
    frame,
    [Math.max(0, durationInFrames - effectFrames), durationInFrames],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: easingFunction,
    },
  );
};

export const SlideDownExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? 18);
  const translateY = interpolate(progress, [0, 1], [0, 120]);
  const opacity = interpolate(progress, [0, 1], [1, 0]);
  return <AbsoluteFill style={{ width: '100%', height: '100%', transform: `translateY(${translateY}px)`, opacity }}>{children}</AbsoluteFill>;
};

export const SlideUpExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames, easing, params }) => {
  const frame = useCurrentFrame();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? 12, easing ?? params?.easing as string | undefined);
  const translateY = interpolate(progress, [0, 1], [0, -30]);
  return <AbsoluteFill style={{ width: '100%', height: '100%', transform: `translateY(${translateY}px)`, opacity: 1 - progress }}>{children}</AbsoluteFill>;
};

export const ZoomOutExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? 14);
  const scale = interpolate(progress, [0, 1], [1, 0.6]);
  const opacity = interpolate(progress, [0, 1], [1, 0]);
  return <AbsoluteFill style={{ width: '100%', height: '100%', transform: `scale(${scale})`, opacity }}>{children}</AbsoluteFill>;
};

export const FlipExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? 18);
  const rotateX = interpolate(progress, [0, 1], [0, 90]);
  const opacity = interpolate(progress, [0, 0.85, 1], [1, 1, 0]);
  return (
    <AbsoluteFill style={{ perspective: 1000 }}>
      <AbsoluteFill style={{ width: '100%', height: '100%', transform: `rotateX(${rotateX}deg)`, opacity }}>
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const FadeOutExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames, easing, params }) => {
  const frame = useCurrentFrame();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? 12, easing ?? params?.easing as string | undefined);
  const opacity = interpolate(progress, [0, 1], [1, 0]);
  return <AbsoluteFill style={{ width: '100%', height: '100%', opacity }}>{children}</AbsoluteFill>;
};

export const ShrinkExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? 14);
  const scale = interpolate(progress, [0, 1], [1, 0.2]);
  const opacity = interpolate(progress, [0, 1], [1, 0]);
  return <AbsoluteFill style={{ width: '100%', height: '100%', transform: `scale(${scale})`, opacity }}>{children}</AbsoluteFill>;
};

export const DissolveExit: FC<EffectComponentProps> = ({ children, durationInFrames, effectFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = getExitProgress(frame, durationInFrames, effectFrames ?? Math.max(6, Math.round(fps * 0.3)));
  const blur = interpolate(progress, [0, 1], [0, 16]);
  const opacity = interpolate(progress, [0, 1], [1, 0]);
  return <AbsoluteFill style={{ width: '100%', height: '100%', filter: `blur(${blur}px)`, opacity }}>{children}</AbsoluteFill>;
};
