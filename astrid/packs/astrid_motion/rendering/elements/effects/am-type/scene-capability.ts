/** Preparation uses the selected browser's existing layout-utils route.
 * Requested-frame evaluation consumes only the resulting immutable measurements. */
import {measureText} from '@remotion/layout-utils';
import type {ComponentCapabilityContext, PreparedComponentCapability, ComponentFrameSupport} from '@banodoco/timeline-composition/evaluation';
import {amTypeLayout, amTypeReveal} from './layout';

const unknown = (reason: string): ComponentFrameSupport => ({presence: 'unknown',
  bounds: {status: 'unknown', reason}, opaqueSupport: 'unknown'});
const absent: ComponentFrameSupport = {presence: 'absent',
  bounds: {status: 'known', rect: {x: 0, y: 0, width: 0, height: 0}}, opaqueSupport: 'none'};
export const prepareAmTypeCapability = ({clip, width, height, rendererIdentity, fontDigests}: ComponentCapabilityContext): PreparedComponentCapability => {
  const params = {...clip.params};
  const text = typeof params.text === 'string' ? params.text : '';
  const layout = amTypeLayout(params, 0);
  const identity = JSON.stringify(['am-type/layout-v1', rendererIdentity, fontDigests, params, width, height]);
  const unsupported = (reason: string): PreparedComponentCapability => ({identity, frame: () => unknown(reason)});
  if (!text.trim()) return {identity, frame: () => absent};
  // Inline typography has unbounded CSS shadow/overflow. Styled runs, multiline,
  // arbitrary CSS colors/fonts and fallback glyphs need additional actual support.
  const allowed = new Set(['text', 'font', 'size', 'color', 'align', 'x', 'y', 'width', 'reveal', 'tracking', 'lineHeight',
    'italicWord', 'underlineWord', 'underlineAt', 'italicColor']);
  if (Object.keys(params).some(key => !allowed.has(key)) || params.italicWord || params.underlineWord
      || !/^[ -~]+$/.test(text)
      || (params.font !== undefined && !['display', 'label'].includes(String(params.font)))
      || (params.reveal !== undefined && !['slideUp', 'type', 'none'].includes(String(params.reveal)))
      || (params.align !== undefined && !['left', 'center', 'right'].includes(String(params.align)))
      || ['size', 'x', 'y', 'width', 'tracking', 'lineHeight'].some(key =>
        params[key] !== undefined && (typeof params[key] !== 'number' || !Number.isFinite(params[key])))
      || (params.color !== undefined && !/^#[a-f0-9]{6}$/i.test(String(params.color)))) {
    return unsupported('Unsupported am-type typography, shadow, glyphs or parameters');
  }
  const qualifiedFonts: Readonly<Record<string, string>> = {"Gelasio-Regular.woff2": "698c2aa61ec1960371b6ed32e6120f028fa614613256f4b9e3f5d10ceb013eb5", "DepartureMono-Regular.woff2": "5b4fed1daa90708aa9c6ee1190abca9dc22164a1c1def0020386e46b61038cfb"};
  const fontFile = layout.isLabel ? 'DepartureMono-Regular.woff2' : 'Gelasio-Regular.woff2';
  if (!rendererIdentity || fontDigests?.[fontFile] !== qualifiedFonts[fontFile] || typeof document === 'undefined' || !document.fonts
      || !document.fonts.check(`400 ${layout.size}px "${layout.family}"`, text)) {
    return unsupported('Selected font/material identity or resolved browser font is unavailable');
  }
  let rect: {x: number; y: number; width: number; height: number};
  try {
    const dimensions = measureText({text, fontFamily: layout.family, fontSize: layout.size,
      fontWeight: 400, letterSpacing: String(layout.line.letterSpacing),
      textTransform: layout.isLabel ? 'uppercase' : 'none', validateFontIsLoaded: true,
      additionalStyles: {lineHeight: String(layout.lineHeight),
        // Inert custom property also keys layout-utils by the actual font closure.
        ['--astrid-scene-font-identity' as 'fontFeatureSettings']: rendererIdentity}});
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (!context) return unsupported('Resolved font ink metrics are unavailable');
    context.font = `400 ${layout.size}px "${layout.family}"`;
    const metrics = context.measureText(layout.isLabel ? text.toUpperCase() : text);
    const ink = [metrics.actualBoundingBoxAscent, metrics.actualBoundingBoxDescent,
      metrics.actualBoundingBoxLeft, metrics.actualBoundingBoxRight];
    if (![dimensions.width, dimensions.height, ...ink].every(Number.isFinite)
        || dimensions.width <= 0 || dimensions.height <= 0 || dimensions.width > layout.width) {
      return unsupported('Wrapping or unresolved ink geometry');
    }
    // Conservative support, not an opaque glyph mask or an exact painted box.
    // DOM measurement owns the real advance/line box. Actual selected-font ink
    // metrics bound overflow in every direction, including negative leading.
    const padX = Math.max(0, metrics.actualBoundingBoxLeft,
      metrics.actualBoundingBoxRight - metrics.width);
    const padY = Math.max(metrics.actualBoundingBoxAscent, metrics.actualBoundingBoxDescent, 0);
    const alignOffset = layout.align === 'left' ? 0 : (layout.width - dimensions.width) / (layout.align === 'center' ? 2 : 1);
    rect = {x: layout.x + alignOffset - padX, y: layout.y - padY,
      width: dimensions.width + padX * 2, height: dimensions.height + padY * 2};
    if (![rect.x, rect.y, rect.width, rect.height].every(Number.isFinite)
        || rect.x < 0 || rect.y < 0 || rect.x + rect.width > width || rect.y + rect.height > height) {
      return unsupported('Partial/off-canvas text ink support is not resolved');
    }
  } catch {
    return unsupported('Selected browser font measurement unavailable');
  }
  const frozenBounds = {status: 'known' as const, rect: {...rect}};
  return {identity: JSON.stringify([identity, frozenBounds]), frame: frame => {
    // Drawing uses the exact same reveal model. During masked slide motion,
    // line boxes alone cannot prove whether actual glyph pixels cross the mask.
    if (layout.reveal === 'type' && amTypeReveal(frame).visibleChars <= 0) return absent;
    if (layout.reveal === 'slideUp' && frame < 8) return unknown('Masked slide glyph support is unresolved');
    return {presence: 'present', bounds: frozenBounds, opaqueSupport: 'none'};
  }};
};
