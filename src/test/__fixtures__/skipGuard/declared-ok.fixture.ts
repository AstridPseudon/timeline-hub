import { it } from 'vitest';
import { skipWhen } from '../../declaredSkip';
it('platform case', (ctx) => {
  skipWhen('posix-owner-only-modes', true, ctx);
});
it('runs', () => {});
