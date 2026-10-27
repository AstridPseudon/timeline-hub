import { cloneElement, isValidElement, type FC, type ReactNode } from 'react';
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export type EffectComponentProps = {
  children: ReactNode;
  durationInFrames: number;
  effectFrames?: number;
  intensity?: number;
  params?: Record<string, unknown>;
  easing?: string;
  text?: string;
};

const getEasing = (value?: string) => {
  if (value === undefined || value === 'linear') return Easing.linear;
  if (value === 'in' || value === 'ease-in') return Easing.in(Easing.quad);
  if (value === 'out' || value === 'ease-out') return Easing.out(Easing.quad);
  if (value === 'in-out' || value === 'inout' || value === 'in_out' || value === 'ease-in-out') return Easing.inOut(Easing.quad);
  if (value === 'step') return (progress: number) => progress < 1 ? 0 : 1;
  throw new Error(`unknown motion easing ${value}`);
};

const getNormalizedProgress = (frame: number, durationInFrames: number, easing?: string): number => {
  return interpolate(frame, [0, Math.max(1, durationInFrames)], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: getEasing(easing),
  });
};

const getLookProgress = (frame: number, durationInFrames: number, fps: number, easing?: string): number => {
  return easing === undefined
    ? spring({ frame, fps, from: 0, to: 1, durationInFrames, config: { damping: 14, stiffness: 110 } })
    : getNormalizedProgress(frame, durationInFrames, easing);
};

const withTransform = (transform: string, opacity = 1): React.CSSProperties => ({
  width: '100%',
  height: '100%',
  transform,
  opacity,
});

export const SlideUpEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({ frame, fps, durationInFrames: effectFrames, config: { damping: 14, stiffness: 120 } });
  const translateY = interpolate(progress, [0, 1], [80, 0]);
  return <AbsoluteFill style={withTransform(`translateY(${translateY}px)`, progress)}>{children}</AbsoluteFill>;
};

export const SlideDownEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 18);
  const translateY = interpolate(progress, [0, 1], [-80, 0]);
  return <AbsoluteFill style={withTransform(`translateY(${translateY}px)`, progress)}>{children}</AbsoluteFill>;
};

export const SlideLeftEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 18);
  const translateX = interpolate(progress, [0, 1], [180, 0]);
  return <AbsoluteFill style={withTransform(`translateX(${translateX}px)`, progress)}>{children}</AbsoluteFill>;
};

export const SlideRightEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 18);
  const translateX = interpolate(progress, [0, 1], [-180, 0]);
  return <AbsoluteFill style={withTransform(`translateX(${translateX}px)`, progress)}>{children}</AbsoluteFill>;
};

export const ZoomInEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 16);
  const scale = interpolate(progress, [0, 1], [0.75, 1]);
  return <AbsoluteFill style={withTransform(`scale(${scale})`, progress)}>{children}</AbsoluteFill>;
};

export const ZoomSpinEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 20);
  const scale = interpolate(progress, [0, 1], [0.35, 1]);
  const rotate = interpolate(progress, [0, 1], [-10, 0]);
  return <AbsoluteFill style={withTransform(`scale(${scale}) rotate(${rotate}deg)`, progress)}>{children}</AbsoluteFill>;
};

export const PulseEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 14);
  const scale = interpolate(progress, [0, 0.6, 1], [1.12, 0.95, 1]);
  return <AbsoluteFill style={withTransform(`scale(${scale})`, progress)}>{children}</AbsoluteFill>;
};

export const FadeEntrance: FC<EffectComponentProps> = ({ children, effectFrames, easing, params }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const duration = effectFrames ?? 12;
  const resolvedEasing = easing ?? params?.easing as string | undefined;
  const progress = resolvedEasing === undefined
    ? spring({ frame, fps, from: 0, to: 1, durationInFrames: duration, config: { damping: 14, stiffness: 110 } })
    : getNormalizedProgress(frame, duration, resolvedEasing);
  return <AbsoluteFill style={withTransform('none', progress)}>{children}</AbsoluteFill>;
};

export const FadeUpEntrance: FC<EffectComponentProps> = ({ children, effectFrames, params, easing }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = getLookProgress(frame, effectFrames ?? 18, fps, easing ?? params?.easing as string | undefined);
  const translateY = interpolate(progress, [0, 1], [40, 0]);
  return <AbsoluteFill style={withTransform(`translateY(${translateY}px)`, progress)}>{children}</AbsoluteFill>;
};

export const ScaleInEntrance: FC<EffectComponentProps> = ({ children, effectFrames, params, easing }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = getLookProgress(frame, effectFrames ?? 18, fps, easing ?? params?.easing as string | undefined);
  const scale = interpolate(progress, [0, 1], [0.85, 1]);
  return <AbsoluteFill style={withTransform(`scale(${scale})`, progress)}>{children}</AbsoluteFill>;
};

export const TypeOnEntrance: FC<EffectComponentProps> = ({ children, effectFrames, params, text, easing }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (typeof text !== 'string' || text.length === 0 || !isValidElement(children)) return <>{children}</>;
  const duration = effectFrames ?? 120;
  const startFrame = typeof params?.startFrame === 'number' ? params.startFrame : 18;
  const fraction = typeof params?.durationFraction === 'number' ? params.durationFraction : 0.55;
  const endFrame = Math.max(startFrame + 1, Math.floor(duration * fraction));
  const progress = getNormalizedProgress(frame - startFrame, endFrame - startFrame, easing ?? params?.easing as string | undefined);
  const revealCount = Math.max(0, Math.min(text.length, Math.ceil(text.length * progress)));
  const visibleText = text.slice(0, revealCount);
  const hiddenTail = text.slice(revealCount);
  const showCaret = params?.showCaret !== false && progress < 1;
  const caretOpacity = showCaret ? (Math.floor(frame / Math.max(1, Math.round(fps / 3))) % 2 === 0 ? 1 : 0) : 0;
  return (
    cloneElement(children as React.ReactElement, {}, (
      <span>
        <span>{visibleText}</span>
        <span aria-hidden="true" style={{
          display: 'inline-block',
          width: '0.05em',
          marginLeft: showCaret ? '0.05em' : 0,
          opacity: caretOpacity,
          backgroundColor: 'currentColor',
          height: '1em',
          verticalAlign: '-0.15em',
        }} />
        <span style={{ opacity: 0 }}>{hiddenTail}</span>
      </span>
    ))
  );
};

export const FlipEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 18);
  const rotateY = interpolate(progress, [0, 1], [-90, 0]);
  return (
    <AbsoluteFill style={{ perspective: 1000 }}>
      <AbsoluteFill style={withTransform(`rotateY(${rotateY}deg)`, progress)}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

export const BounceEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const progress = getNormalizedProgress(frame, effectFrames ?? 20);
  const translateY = interpolate(progress, [0, 0.6, 0.8, 1], [120, -20, 10, 0]);
  return <AbsoluteFill style={withTransform(`translateY(${translateY}px)`, progress)}>{children}</AbsoluteFill>;
};

export const MeteoriteEntrance: FC<EffectComponentProps> = ({ children, effectFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = effectFrames ?? 24;

  const approach = interpolate(frame, [0, dur * 0.35], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const impact = spring({ frame: Math.max(0, frame - dur * 0.35), fps, durationInFrames: dur * 0.65, config: { damping: 8, stiffness: 250, mass: 0.6 } });
  const phase = approach < 1 ? approach : 1;
  const settled = approach >= 1 ? impact : 0;

  const translateX = interpolate(phase, [0, 1], [600, 0]);
  const translateY = interpolate(phase, [0, 1], [-500, 0]);
  const rotate = interpolate(phase, [0, 1], [-35, 0]);
  const preImpactScale = interpolate(phase, [0, 1], [0.15, 1]);

  const bounceScale = settled > 0 ? interpolate(settled, [0, 1], [1.2, 1]) : 1;
  const finalScale = preImpactScale * bounceScale;

  const shakeIntensity = interpolate(settled, [0, 0.15, 0.5, 1], [0, 12, 4, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const shakeX = shakeIntensity * Math.sin(frame * 47);
  const shakeY = shakeIntensity * Math.cos(frame * 31);

  const flashOpacity = interpolate(settled, [0, 0.08, 0.3], [0, 0.9, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const glowSize = interpolate(settled, [0, 0.5], [20, 80], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const glowOpacity = interpolate(settled, [0, 0.1, 0.6], [0, 0.7, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const brightness = interpolate(settled, [0, 0.1, 0.4], [1, 1.8, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const opacity = interpolate(phase, [0, 0.15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ transform: `translate(${shakeX}px, ${shakeY}px)` }}>
      <AbsoluteFill
        style={{
          background: `rgba(255, 240, 200, ${flashOpacity})`,
          pointerEvents: 'none',
          zIndex: 10,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% 50%, rgba(255, 160, 40, ${glowOpacity}) 0%, rgba(255, 100, 20, ${glowOpacity * 0.5}) ${glowSize * 0.5}%, transparent ${glowSize}%)`,
          pointerEvents: 'none',
          zIndex: 5,
        }}
      />
      <AbsoluteFill
        style={{
          transform: `translate(${translateX}px, ${translateY}px) rotate(${rotate}deg) scale(${finalScale})`,
          opacity,
          filter: `brightness(${brightness})`,
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
