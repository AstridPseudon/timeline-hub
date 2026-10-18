import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  EDITOR_EXTENSION_FIXTURE_ENV,
  editorExtensionFixtureAlias,
} from '../../config/vite/editorExtensionFixtureAlias';

describe('browser-only extension fixture catalog alias', () => {
  it('maps the product catalog to the fixed test inventory only on an opted-in dev server', () => {
    const alias = editorExtensionFixtureAlias('serve', {
      [EDITOR_EXTENSION_FIXTURE_ENV]: '1',
    });

    expect(alias).toEqual({
      find: '@/tools/video-editor/dev/localExtensions.ts',
      replacement: path.resolve(__dirname, 'editorExtensionFixtureCatalog.ts'),
    });
  });

  it('keeps ordinary development and every production build on the Astrid catalog', () => {
    expect(editorExtensionFixtureAlias('serve', {})).toBeNull();
    expect(editorExtensionFixtureAlias('serve', {
      [EDITOR_EXTENSION_FIXTURE_ENV]: 'true',
    })).toBeNull();
    expect(editorExtensionFixtureAlias('build', {
      [EDITOR_EXTENSION_FIXTURE_ENV]: '1',
    })).toBeNull();
  });
});
