import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  astridEditorOnlyRedirectTarget,
  isAstridEditorOnlyShellPath,
  isAstridEditorOnlyWorkspace,
} from './localWorkspaceShell';

describe('local Astrid editor-only workspace shell', () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it('is controlled by the local workspace client flag', () => {
    vi.stubEnv('VITE_ASTRID_EDITOR_ONLY', '1');
    expect(isAstridEditorOnlyWorkspace()).toBe(true);
    expect(isAstridEditorOnlyShellPath('/tools/video-editor')).toBe(true);
    expect(isAstridEditorOnlyShellPath('/tools/video-editor/harness')).toBe(false);
  });

  it('redirects other local app routes to the editor and preserves its selection', () => {
    vi.stubEnv('VITE_ASTRID_EDITOR_ONLY', '1');
    expect(astridEditorOnlyRedirectTarget(
      '/tools/image-generation',
      '?project=project-1&timeline=timeline-1&mode=discard',
    )).toBe('/tools/video-editor?project=project-1&timeline=timeline-1');
    expect(astridEditorOnlyRedirectTarget('/tools/video-editor', '?project=project-1')).toBeNull();
    expect(astridEditorOnlyRedirectTarget('/tools/video-editor/harness', '')).toBe('/tools/video-editor');
  });

  it('leaves cloud route handling untouched', () => {
    expect(isAstridEditorOnlyWorkspace()).toBe(false);
    expect(isAstridEditorOnlyShellPath('/tools/video-editor')).toBe(false);
    expect(astridEditorOnlyRedirectTarget('/tools/image-generation', '')).toBeNull();
  });
});
