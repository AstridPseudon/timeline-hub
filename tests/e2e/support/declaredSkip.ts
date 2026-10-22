import { test } from '@playwright/test';
import { declaredTag, laneIsRequired } from '../../../config/testing/skipRegistry.mjs';

/**
 * The only way a Playwright test skips. Call it inside a test or hook:
 *   skipWhen('direct-journey-ffmpeg', !video.decodable, 'ffmpeg is not installed');
 * `name` must be declared in config/testing/skipRegistry.mjs. In a CI job that provides the lane
 * (ASTRID_REQUIRE_LANES contains the registry entry's requireInLane) the unmet condition FAILS the test instead
 * of skipping it. config/testing/playwrightSkipGuard.ts reports every skip by name and fails the run on any
 * skip that is not declared.
 */
export function skipWhen(name: string, condition: boolean | string | null, detail?: string): void {
  if (!condition) return;
  const why = [detail, typeof condition === 'string' ? condition : undefined].filter(Boolean).join(': ');
  const message = why ? `${declaredTag(name)} (${why})` : declaredTag(name);
  if (laneIsRequired(name)) throw new Error(`required in this lane but unavailable: ${message}`);
  test.skip(true, message);
}
