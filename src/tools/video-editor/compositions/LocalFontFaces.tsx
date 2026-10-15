import { continueRender, delayRender } from 'remotion';
import { createElement, useEffect, useState, type ReactElement } from 'react';
import {
  LOCAL_FONT_FACES,
  LOCAL_FONT_GLYPH_PROBE,
  type LocalFontFace,
} from '../../../../vendor/astrid-browser/remotion/src/fonts.ts';

// The same binaries Astrid's renderer registers (remotion/src/fonts.ts), vendored
// with their sha256 record in vendor/astrid-browser/provenance.json. Vite emits
// each one as a hashed asset URL.
const FONT_URLS = import.meta.glob<string>('../../../../vendor/astrid-browser/remotion/public/fonts/*.woff2', {
  eager: true,
  query: '?url',
  import: 'default',
});

const fontUrl = (file: string): string => {
  const name = file.split('/').pop() ?? file;
  const url = Object.entries(FONT_URLS).find(([path]) => path.endsWith(`/${name}`))?.[1];
  if (!url) throw new Error(`Vendored Astrid font is missing from the bundle: ${file}`);
  return url;
};

export const localFontFaceCss = (faces: readonly LocalFontFace[] = LOCAL_FONT_FACES): string =>
  faces
    .map(
      ({ family, file, weight, style = 'normal' }) =>
        `@font-face { font-family: '${family}'; src: url('${fontUrl(file)}') format('woff2'); font-weight: ${weight}; font-style: ${style}; font-display: block; }`,
    )
    .join('\n');

export const localFontSpec = ({ family, weight, style }: LocalFontFace): string =>
  `${style === 'italic' ? 'italic ' : ''}${weight} 16px "${family}"`;

/**
 * Registers Astrid's shipped local faces for the editor preview and holds the
 * composition until each face has loaded, so text is never measured against a
 * system fallback. A failed load is logged and released: the preview should
 * degrade to a fallback rather than hang.
 */
export function LocalFontFaces(): ReactElement {
  const [renderHandle] = useState(() => delayRender('Loading Astrid local fonts'));

  useEffect(() => {
    let cancelled = false;
    const release = () => {
      if (!cancelled) continueRender(renderHandle);
    };
    const loadFonts = async (): Promise<void> => {
      if (typeof document === 'undefined' || !document.fonts) {
        console.warn('Astrid local fonts need the FontFaceSet API; using system fallbacks.');
        return;
      }
      const results = await Promise.allSettled(
        LOCAL_FONT_FACES.map((face) => document.fonts.load(localFontSpec(face), LOCAL_FONT_GLYPH_PROBE)),
      );
      const failed = results.flatMap((result, index) => (result.status === 'rejected' ? [LOCAL_FONT_FACES[index]] : []));
      if (failed.length > 0) {
        console.warn(`Astrid local font load failed: ${failed.map((face) => localFontSpec(face)).join(', ')}`);
      }
    };
    loadFonts().catch((error) => console.warn('Astrid local font load failed', error)).finally(release);
    return () => {
      cancelled = true;
    };
  }, [renderHandle]);

  return createElement('style', { 'data-astrid-local-fonts': true }, localFontFaceCss());
}
