import { ORIGINAL_640, type ParityCanvas } from './canvas';

export type RgbFrame = {
  readonly width: number;
  readonly height: number;
  readonly bytes: Buffer;
};

export type FrameComparison = {
  readonly frame: number;
  readonly pixels: number;
  readonly pixelsOutsideBound: number;
  readonly outsideBoundFraction: number;
  readonly maxChannelError: number;
  readonly meanChannelError: number;
};

export function compareRgbFrames(expected: RgbFrame, actual: RgbFrame, frame: number, canvas: ParityCanvas = ORIGINAL_640): FrameComparison {
  for (const [host, image] of [['Player', expected], ['export', actual]] as const) {
    if (image.width !== canvas.width || image.height !== canvas.height
      || image.bytes.length !== canvas.width * canvas.height * 3) {
      throw new Error(`frame ${frame}: invalid ${host} RGB frame dimensions/bytes: ${image.width}x${image.height}, ${image.bytes.length} bytes`);
    }
  }
  let pixelsOutsideBound = 0;
  let totalError = 0;
  let maxChannelError = 0;
  for (let offset = 0; offset < expected.bytes.length; offset += 3) {
    let pixelOutsideBound = false;
    for (let channel = 0; channel < 3; channel += 1) {
      const error = Math.abs(expected.bytes[offset + channel] - actual.bytes[offset + channel]);
      maxChannelError = Math.max(maxChannelError, error);
      totalError += error;
      if (error > 2) pixelOutsideBound = true;
    }
    if (pixelOutsideBound) pixelsOutsideBound += 1;
  }
  const pixels = expected.width * expected.height;
  return {
    frame,
    pixels,
    pixelsOutsideBound,
    outsideBoundFraction: pixelsOutsideBound / pixels,
    maxChannelError,
    meanChannelError: totalError / expected.bytes.length,
  };
}

export function assertFrameWithinBound(comparison: FrameComparison, canvas: ParityCanvas = ORIGINAL_640): void {
  if (!Number.isFinite(comparison.outsideBoundFraction) || comparison.pixels !== canvas.width * canvas.height) {
    throw new Error(`frame ${comparison.frame}: invalid comparison`);
  }
  if (comparison.outsideBoundFraction > 0.001) {
    throw new Error(`frame ${comparison.frame}: ${comparison.pixelsOutsideBound}/${comparison.pixels} pixels exceed 2/255; max channel error=${comparison.maxChannelError}/255, mean=${comparison.meanChannelError.toFixed(3)}/255`);
  }
}
