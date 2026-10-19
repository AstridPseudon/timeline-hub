import { execFile } from 'node:child_process';
import { mkdir } from 'node:fs/promises';
import { promisify } from 'node:util';
import { expect, type Page, type TestInfo } from '@playwright/test';
import {
  PARITY_FPS,
  PARITY_HEIGHT,
  PARITY_WIDTH,
} from './fixture';

const execFileAsync = promisify(execFile);
const PREVIEW_SURFACE = '[data-testid="video-editor-preview-surface"]';
const RULER = '[data-testid="timeline-ruler"]';
const PLAYER_COMPOSITION = `${PREVIEW_SURFACE} .__remotion-player > div > div`;

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

async function ffprobeDimensions(path: string): Promise<{ width: number; height: number }> {
  const { stdout } = await execFileAsync('ffprobe', [
    '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', path,
  ]);
  const stream = (JSON.parse(stdout) as { streams?: Array<{ width?: number; height?: number }> }).streams?.[0];
  if (!stream?.width || !stream.height) throw new Error(`could not read image dimensions for ${path}`);
  return { width: stream.width, height: stream.height };
}

async function decodeRgb(path: string, args: string[]): Promise<RgbFrame> {
  const dimensions = await ffprobeDimensions(path);
  const { stdout } = await execFileAsync('ffmpeg', [
    '-v', 'error', '-i', path, ...args, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: PARITY_WIDTH * PARITY_HEIGHT * 3 + 1024 });
  const bytes = Buffer.isBuffer(stdout) ? stdout : Buffer.from(stdout);
  expect(bytes).toHaveLength(dimensions.width * dimensions.height * 3);
  return { ...dimensions, bytes };
}

export function compareRgbFrames(expected: RgbFrame, actual: RgbFrame, frame: number): FrameComparison {
  if (expected.width !== actual.width || expected.height !== actual.height) {
    throw new Error(`frame ${frame} dimensions differ: Player ${expected.width}x${expected.height}, export ${actual.width}x${actual.height}`);
  }
  let pixelsOutsideBound = 0;
  let totalError = 0;
  let maxChannelError = 0;
  for (let offset = 0; offset < expected.bytes.length; offset += 3) {
    let pixelOutsideBound = false;
    for (let channel = 0; channel < 3; channel += 1) {
      const error = Math.abs((expected.bytes[offset + channel] ?? 0) - (actual.bytes[offset + channel] ?? 0));
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

export function assertFrameWithinBound(comparison: FrameComparison): void {
  expect(
    comparison.outsideBoundFraction,
    `frame ${comparison.frame}: ${comparison.pixelsOutsideBound}/${comparison.pixels} pixels exceed 2/255; max channel error=${comparison.maxChannelError}/255, mean=${comparison.meanChannelError.toFixed(3)}/255`,
  ).toBeLessThanOrEqual(0.001);
}

export async function decodeExportFrame(exportPath: string, frame: number): Promise<RgbFrame> {
  return decodeRgb(exportPath, ['-map', '0:v:0', '-an', '-vf', `select=eq(n\\,${frame})`]);
}

export async function decodePlayerCapture(path: string): Promise<RgbFrame> {
  return decodeRgb(path, []);
}

async function currentPreviewFrame(page: Page): Promise<number> {
  const time = Number(await page.locator(PREVIEW_SURFACE).getAttribute('data-current-time'));
  if (!Number.isFinite(time)) throw new Error(`preview has no finite current time: ${String(time)}`);
  return Math.round(time * PARITY_FPS);
}

async function seekViaRuler(page: Page, frame: number): Promise<void> {
  const ruler = await page.locator(RULER).boundingBox();
  if (!ruler) throw new Error('timeline ruler has no browser box');
  const current = await currentPreviewFrame(page);
  const timelineDuration = 5.5;
  const x = ruler.x + 2 + (ruler.width - 4) * ((frame / PARITY_FPS) / timelineDuration);
  await page.mouse.click(x, ruler.y + ruler.height / 2);
  await expect.poll(() => currentPreviewFrame(page), { timeout: 5_000 }).toBe(frame);
  if (frame === current) await page.waitForTimeout(100);
}

/** Seek through the editor's real ruler, which ultimately calls the Player ref. */
export async function capturePlayerFrame(page: Page, frame: number, testInfo: TestInfo, name: string): Promise<RgbFrame> {
  await seekViaRuler(page, frame);
  const player = page.locator(`${PREVIEW_SURFACE} .__remotion-player`).first();
  const composition = page.locator(PLAYER_COMPOSITION).first();
  await expect(player).toBeVisible();
  await expect(page.locator(PREVIEW_SURFACE)).toHaveAttribute('data-astrid-preview-frame-ready', 'true');

  // The production Player fits itself to the editor panel. Constrain only the
  // test host to the composition's native box so the screenshot has no scale,
  // editor chrome, loading cover, or resampling before comparison.
  await player.evaluate((element) => {
    const host = element as HTMLElement;
    host.style.width = '640px';
    host.style.height = '360px';
    host.style.flex = '0 0 640px';
  });
  await expect.poll(async () => {
    const box = await composition.boundingBox();
    return box ? [Math.round(box.width), Math.round(box.height)] : null;
  }, { timeout: 5_000 }).toEqual([PARITY_WIDTH, PARITY_HEIGHT]);

  const output = testInfo.outputPath(`viewing-parity/player-frame-${String(frame).padStart(3, '0')}-${name}.png`);
  await mkdir(testInfo.outputPath('viewing-parity'), { recursive: true });
  await composition.screenshot({ path: output, animations: 'disabled' });
  const decoded = await decodePlayerCapture(output);
  expect(decoded.width).toBe(PARITY_WIDTH);
  expect(decoded.height).toBe(PARITY_HEIGHT);
  return decoded;
}

export function playerCapturePath(testInfo: TestInfo, frame: number, name: string): string {
  return testInfo.outputPath(`viewing-parity/player-frame-${String(frame).padStart(3, '0')}-${name}.png`);
}
