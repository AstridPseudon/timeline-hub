export type PeekSide = 'top' | 'right' | 'bottom' | 'left';

export interface PeekAnchor {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

export interface PeekViewport {
  width: number;
  height: number;
}

export interface PeekPlacementOptions {
  margin?: number;
  gap?: number;
}

export interface PeekPlacement {
  side: PeekSide;
  left: number;
  top: number;
  width: number;
  height: number;
}

export interface PeekConnector {
  orientation: 'horizontal' | 'vertical';
  /** Centre of the 1 px line, relative to the bridge's cross-axis start. */
  crossOffset: number;
  length: number;
  transformOrigin: 'center top' | 'center bottom' | 'left center' | 'right center';
}

const DEFAULT_ASPECT_RATIO = 16 / 9;
const SIDES: PeekSide[] = ['top', 'right', 'bottom', 'left'];

function finiteNonNegative(value: number): number {
  return Number.isFinite(value) ? Math.max(0, value) : 0;
}

function finiteCoordinate(value: number): number {
  return Number.isFinite(value) ? value : 0;
}

function fitRegion(regionWidth: number, regionHeight: number, aspectRatio: number) {
  const widthLimit = finiteNonNegative(regionWidth);
  const heightLimit = finiteNonNegative(regionHeight);
  const width = Math.min(widthLimit, heightLimit * aspectRatio);
  const height = Math.min(heightLimit, width / aspectRatio);
  return { width: finiteNonNegative(width), height: finiteNonNegative(height) };
}

/** Places an aspect-ratio-preserving peek beside its anchor in the roomiest viewport region. */
export function placePeek(
  anchor: PeekAnchor,
  viewport: PeekViewport,
  aspectRatio: number,
  opts: PeekPlacementOptions = {},
): PeekPlacement {
  const width = finiteNonNegative(viewport.width);
  const height = finiteNonNegative(viewport.height);
  const margin = Math.min(finiteNonNegative(opts.margin ?? 12), width / 2, height / 2);
  const gap = finiteNonNegative(opts.gap ?? 14);
  const ar = Number.isFinite(aspectRatio) && aspectRatio > 0 ? aspectRatio : DEFAULT_ASPECT_RATIO;
  const a = {
    left: finiteCoordinate(anchor.left),
    top: finiteCoordinate(anchor.top),
    right: finiteCoordinate(anchor.right),
    bottom: finiteCoordinate(anchor.bottom),
  };

  const availableWidth = Math.max(0, width - margin * 2);
  const availableHeight = Math.max(0, height - margin * 2);
  const regions = {
    top: { width: availableWidth, height: Math.max(0, a.top - gap - margin) },
    right: { width: Math.max(0, width - margin - a.right - gap), height: availableHeight },
    bottom: { width: availableWidth, height: Math.max(0, height - margin - a.bottom - gap) },
    left: { width: Math.max(0, a.left - gap - margin), height: availableHeight },
  } satisfies Record<PeekSide, { width: number; height: number }>;

  const candidates = SIDES.map((side) => {
    const size = fitRegion(regions[side].width, regions[side].height, ar);
    return { side, ...size, area: size.width * size.height };
  });
  const maxArea = Math.max(...candidates.map((candidate) => candidate.area));
  const winner = candidates.find((candidate) => candidate.area >= maxArea * 0.99) ?? candidates[0];
  const { side, width: peekWidth, height: peekHeight } = winner;
  const clamp = (value: number, min: number, max: number) => Math.min(Math.max(value, min), Math.max(min, max));

  const left = side === 'right'
    ? a.right + gap
    : side === 'left'
      ? a.left - gap - peekWidth
      : clamp((a.left + a.right - peekWidth) / 2, margin, width - margin - peekWidth);
  const top = side === 'bottom'
    ? a.bottom + gap
    : side === 'top'
      ? a.top - gap - peekHeight
      : clamp((a.top + a.bottom - peekHeight) / 2, margin, height - margin - peekHeight);
  const boundedLeft = clamp(left, margin, width - margin - peekWidth);
  const boundedTop = clamp(top, margin, height - margin - peekHeight);

  return {
    side,
    left: finiteCoordinate(boundedLeft),
    top: finiteCoordinate(boundedTop),
    width: peekWidth,
    height: peekHeight,
  };
}

/** Returns the visible connector geometry relative to the bridge, or null when the eye and
 * the peek's straight edge do not overlap on the cross-axis. */
export function connectorFor(
  anchor: PeekAnchor,
  placement: PeekPlacement,
  radius: number,
): PeekConnector | null {
  const isVertical = placement.side === 'top' || placement.side === 'bottom';
  const anchorStart = finiteCoordinate(isVertical ? anchor.left : anchor.top);
  const anchorEnd = finiteCoordinate(isVertical ? anchor.right : anchor.bottom);
  const anchorCenter = (anchorStart + anchorEnd) / 2;
  const edgeStart = finiteCoordinate(isVertical ? placement.left : placement.top);
  const edgeSize = finiteNonNegative(isVertical ? placement.width : placement.height);
  const inset = Math.min(finiteNonNegative(radius), edgeSize / 2);
  const straightStart = edgeStart + inset;
  const straightEnd = edgeStart + edgeSize - inset;
  const crossPosition = Math.min(Math.max(anchorCenter, straightStart), straightEnd);

  if (crossPosition < anchorStart || crossPosition > anchorEnd) return null;

  const gap = placement.side === 'top'
    ? finiteCoordinate(anchor.top) - (finiteCoordinate(placement.top) + finiteNonNegative(placement.height))
    : placement.side === 'bottom'
      ? finiteCoordinate(placement.top) - finiteCoordinate(anchor.bottom)
      : placement.side === 'left'
        ? finiteCoordinate(anchor.left) - (finiteCoordinate(placement.left) + finiteNonNegative(placement.width))
        : finiteCoordinate(placement.left) - finiteCoordinate(anchor.right);
  if (gap <= 0) return null;

  const transformOrigin = placement.side === 'top'
    ? 'center bottom'
    : placement.side === 'bottom'
      ? 'center top'
      : placement.side === 'left'
        ? 'right center'
        : 'left center';

  return {
    orientation: isVertical ? 'vertical' : 'horizontal',
    crossOffset: crossPosition - anchorStart,
    length: gap,
    transformOrigin,
  };
}
