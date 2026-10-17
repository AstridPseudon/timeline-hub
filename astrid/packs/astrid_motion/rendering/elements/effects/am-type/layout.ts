/** The actual am-type CSS/reveal model, shared by drawing and capability preparation. */
import type {CSSProperties} from 'react';
import {COLOR, FAMILY, easeOutCubic, finiteNumber, oneOf} from '../../_shared/am';
export const amTypeReveal = (frame: number) => ({
  slideFraction: frame < 8 ? 1 - easeOutCubic(frame / 8) : 0,
  slideTransform: frame < 8 ? `translateY(${(1 - easeOutCubic(frame / 8)) * 100}%)` : undefined,
  visibleChars: Math.floor(frame / 2) + 1,
});
export const amTypeLayout = (params: Record<string, unknown>, frame: number) => {
  const isLabel = oneOf(params.font, ['display', 'label'] as const, 'display') === 'label';
  const reveal = oneOf(params.reveal, ['slideUp', 'type', 'none'] as const, 'slideUp');
  const align = oneOf(params.align, ['left', 'center', 'right'] as const, 'left');
  const size = Math.max(1, finiteNumber(params.size, isLabel ? 28 : 96));
  const tracking = finiteNumber(params.tracking, isLabel ? .12 : -.01);
  const lineHeight = Math.max(.5, finiteNumber(params.lineHeight, isLabel ? 1.3 : .95));
  const x = finiteNumber(params.x, 96), y = finiteNumber(params.y, 96);
  const width = Math.max(1, finiteNumber(params.width, 1200));
  const family = isLabel ? FAMILY.label : FAMILY.display;
  const mask: CSSProperties = {position: 'absolute', left: x, top: y, width,
    overflow: reveal === 'slideUp' && frame < 8 ? 'hidden' : 'visible',
    paddingTop: '0.15em', paddingBottom: '0.25em', marginTop: '-0.15em', marginBottom: '-0.25em',
    boxSizing: 'border-box'};
  const line: CSSProperties = {color: typeof params.color === 'string' ? params.color : COLOR.ink,
    fontFamily: family, fontSize: size, fontWeight: 400, lineHeight,
    letterSpacing: `${tracking}em`, textAlign: align, textTransform: isLabel ? 'uppercase' : 'none',
    whiteSpace: 'pre-wrap',
    transform: reveal === 'slideUp' ? amTypeReveal(frame).slideTransform : undefined};
  return {isLabel, reveal, align, size, tracking, lineHeight, x, y, width, family, mask, line};
};
