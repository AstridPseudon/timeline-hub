import { declaredTag } from '../../config/testing/skipRegistry.mjs';

/**
 * The only way a vitest test skips. Call it first in the test body with the test context:
 *   it('...', (ctx) => { skipWhen('posix-owner-only-modes', process.platform === 'win32', ctx); ... })
 * `name` must be declared in config/testing/skipRegistry.mjs; the run reports the skip by test name and
 * config/testing/skipGuardReporter.ts fails the run on any skip that is not declared.
 */
export function skipWhen(name: string, condition: boolean, ctx: { skip: (note?: string) => never }): void {
  const note = declaredTag(name);
  if (condition) ctx.skip(note);
}
