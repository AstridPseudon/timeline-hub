import { PARITY_WIDTH as SOURCE_WIDTH, PARITY_HEIGHT as SOURCE_HEIGHT } from './media';

export const PARITY_WIDTH = 1920;
export const PARITY_HEIGHT = 1080;

/** Read readiness cells in the native screenshot; never resize compared RGB. */
export function readNativeFrameMarker(bytes: Uint8Array): number | null {
  if (bytes.length !== PARITY_WIDTH * PARITY_HEIGHT * 3) return null;
  const sample = (x: number, y: number) => {
    const offset = ((y * PARITY_HEIGHT / SOURCE_HEIGHT) * PARITY_WIDTH + x * PARITY_WIDTH / SOURCE_WIDTH) * 3;
    return Array.from(bytes.slice(offset, offset + 3));
  };
  if (!sample(250, 24).every(value => value > 220)) return null;
  let frame = 0;
  for (let bit = 0; bit < 6; bit++) {
    const rgb = sample(24 + bit * 40, 24);
    if (rgb.every(value => value > 220)) frame |= 1 << bit;
    else if (!rgb.every(value => value < 35)) return null;
  }
  return frame;
}
