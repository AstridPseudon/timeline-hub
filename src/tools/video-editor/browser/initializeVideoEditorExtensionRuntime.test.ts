import { beforeEach, describe, expect, it, vi } from 'vitest';

const runtimeMocks = vi.hoisted(() => ({
  installOperationalAnalytics: vi.fn(),
}));

vi.mock('../runtime/extensionOperationalAnalytics.ts', () => ({
  installExtensionOperationalAnalyticsSink: runtimeMocks.installOperationalAnalytics,
}));

import { initializeVideoEditorExtensionRuntime } from '@/tools/video-editor/browser';

describe('initializeVideoEditorExtensionRuntime', () => {
  beforeEach(() => {
    runtimeMocks.installOperationalAnalytics.mockReset();
  });

  it('installs the best-effort analytics sink synchronously, with no release config to wait for', () => {
    initializeVideoEditorExtensionRuntime();
    expect(runtimeMocks.installOperationalAnalytics).toHaveBeenCalledOnce();
  });
});
