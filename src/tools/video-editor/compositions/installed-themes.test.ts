import { describe, expect, it } from 'vitest';
import { DEFAULT_THEME, type Theme } from '@banodoco/timeline-composition/theme-api';
import { INSTALLED_TIMELINE_THEMES, resolveTimelineRenderTheme } from './installed-themes';

describe('resolveTimelineRenderTheme', () => {
  // Owner policy: implicit preview adopts the public navy/Arial/cyan export default.
  it.each([undefined, 'banodoco-default', 'uninstalled-theme'])(
    'resolves %s to the complete public DEFAULT_THEME',
    (theme) => {
      expect(resolveTimelineRenderTheme({ theme })).toEqual(DEFAULT_THEME);
    },
  );

  it('preserves explicit 2rp fields when merging a nested background override', () => {
    const installed = structuredClone(INSTALLED_TIMELINE_THEMES['2rp']);
    const theme_overrides = { visual: { color: { bg: '#192837' } } };
    const originalOverrides = structuredClone(theme_overrides);

    expect(resolveTimelineRenderTheme({ theme: '2rp', theme_overrides })).toEqual({
      ...installed,
      visual: {
        ...installed.visual,
        color: { ...installed.visual.color, bg: theme_overrides.visual.color.bg },
      },
    });
    expect(INSTALLED_TIMELINE_THEMES['2rp']).toEqual(installed);
    expect(theme_overrides).toEqual(originalOverrides);
    expect(resolveTimelineRenderTheme({ theme: '2rp' })).toEqual(installed);
  });

  it('preserves a complete authored visual theme without default leakage', () => {
    const visual: Theme['visual'] = {
      color: { fg: '#abcdef', bg: '#123456', accent: '#fedcba' },
      type: {
        families: { heading: 'Authored Heading', body: 'Authored Body', mono: 'Authored Mono' },
        size: { base: 41, small: 19, large: 97 },
        weight: { normal: 350, bold: 750 },
        lineHeight: 1.4,
      },
      motion: { fadeMs: 725 },
      canvas: { width: 1280, height: 720, fps: 24 },
    };
    const before = structuredClone(visual);

    expect(resolveTimelineRenderTheme({
      theme: 'authored-film',
      theme_overrides: { visual },
    }).visual).toEqual(before);
    expect(visual).toEqual(before);
    expect(resolveTimelineRenderTheme({})).toEqual(DEFAULT_THEME);
  });

  it('merges a partial accent without mutating the public default or later resolutions', () => {
    const before = structuredClone(DEFAULT_THEME);
    const theme_overrides = { visual: { color: { accent: '#a123ef' } } };
    const originalOverrides = structuredClone(theme_overrides);
    const resolved = resolveTimelineRenderTheme({ theme_overrides });

    expect(resolved).toEqual({
      ...before,
      visual: {
        ...before.visual,
        color: { ...before.visual.color, accent: theme_overrides.visual.color.accent },
      },
    });
    resolved.visual.type.families.heading = 'Only this resolution';
    resolved.visual.color.bg = '#342156';
    expect(theme_overrides).toEqual(originalOverrides);
    expect(DEFAULT_THEME).toEqual(before);
    expect(INSTALLED_TIMELINE_THEMES['banodoco-default']).toEqual(before);
    expect(resolveTimelineRenderTheme({})).toEqual(before);
  });
});
