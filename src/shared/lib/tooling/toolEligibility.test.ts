import { describe, expect, it } from 'vitest';

import { AppEnv } from '@/types/env';

import { isToolEligible } from './toolEligibility';
import { TOOL_IDS } from './toolIds';
import { toolsUIManifest } from './toolManifest';

describe('isToolEligible', () => {
  it('rejects a missing tool', () => {
    expect(isToolEligible(null, { currentEnv: AppEnv.WEB })).toBe(false);
    expect(isToolEligible(undefined, { currentEnv: AppEnv.DEV })).toBe(false);
  });

  it('admits a tool only in the environments it lists, except in dev', () => {
    const localOnly = { id: 'local-only', environments: [AppEnv.LOCAL] };
    expect(isToolEligible(localOnly, { currentEnv: AppEnv.LOCAL })).toBe(true);
    expect(isToolEligible(localOnly, { currentEnv: AppEnv.WEB })).toBe(false);
    expect(isToolEligible(localOnly, { currentEnv: AppEnv.DEV })).toBe(true);
  });

  it('shows the character animate tool like every other registered tool', () => {
    const characterAnimate = toolsUIManifest.find((tool) => tool.id === TOOL_IDS.CHARACTER_ANIMATE);
    expect(characterAnimate).toBeDefined();
    for (const currentEnv of [AppEnv.LOCAL, AppEnv.WEB, AppEnv.DEV]) {
      expect(isToolEligible(characterAnimate, { currentEnv })).toBe(true);
    }
  });
});
