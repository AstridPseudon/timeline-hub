import { beforeEach, describe, expect, it, vi } from 'vitest';

beforeEach(() => { localStorage.clear(); vi.resetModules(); });
describe('welcome ownership', () => {
  it('owns a fresh bare editor, never existing project links or other routes', async () => {
    const { shouldShowWelcome } = await import('./welcomeProgress');
    expect(shouldShowWelcome(new URL('https://astrid.haus/tools/video-editor'))).toBe(true);
    for (const path of ['/', '/settings', '/tools/video-editor?project=real', '/tools/video-editor?timeline=real', '/tools/video-editor?localTest=1']) {
      expect(shouldShowWelcome(new URL(`https://astrid.haus${path}`))).toBe(false);
    }
  });
  it('migrates returning browser signals without a Runtime request', async () => {
    const { shouldShowWelcome } = await import('./welcomeProgress');
    for (const [key, value] of [['astrid.runtime.connectedBefore', '1'], ['astrid-setup-complete', 'true'], ['astrid-editor-tour-v1', '1'], ['astrid:lastOpenedLocalProjectSlug', 'real']]) {
      localStorage.clear(); localStorage.setItem(key, value);
      expect(shouldShowWelcome(new URL('https://astrid.haus/tools/video-editor'))).toBe(false);
    }
  });
  it('resumes connection across reload despite connected-before, then exits only to real selection', async () => {
    const progress = await import('./welcomeProgress');
    progress.writeWelcomePhase('connection');
    localStorage.setItem('astrid.runtime.connectedBefore', '1');
    vi.resetModules();
    const resumed = await import('./welcomeProgress');
    const url = new URL('https://astrid.haus/tools/video-editor');
    expect(resumed.shouldShowWelcome(url)).toBe(true);
    expect(resumed.welcomeEntryPhase(url)).toBe('connection');
    expect(resumed.completeWelcome({projectId: 'saved-id', timelineId: 'saved-timeline'})).toBe('/tools/video-editor?project=saved-id&timeline=saved-timeline');
    expect(resumed.shouldShowWelcome(url)).toBe(false);
  });
  it('installer handoff goes directly to connection and skip does not claim completion', async () => {
    const progress = await import('./welcomeProgress');
    progress.writeWelcomePhase('tour');
    expect(progress.welcomeEntryPhase(new URL('https://astrid.haus/tools/video-editor?connect=1'))).toBe('connection');
    progress.writeWelcomePhase('connection');
    expect(localStorage.getItem('astrid-editor-tour-v1')).toBeNull();
  });
});
