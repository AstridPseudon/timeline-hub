import { createElement } from 'react';
import { render } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

// The Runtime origin is module state set once per page, so each case loads fresh modules.
type Connection = typeof import('@/integrations/runtime/connection');
type MediaCrossOrigin = typeof import('./mediaCrossOrigin');
let connection: Connection;
let mediaCrossOrigin: MediaCrossOrigin['mediaCrossOrigin'];

const GATEWAY = 'http://127.0.0.1:17340';

beforeEach(async () => {
  vi.resetModules();
  connection = await import('@/integrations/runtime/connection');
  ({ mediaCrossOrigin } = await import('./mediaCrossOrigin'));
});

describe('mediaCrossOrigin', () => {
  describe('with a gateway origin configured', () => {
    beforeEach(() => {
      connection.setRuntimeOrigin({ VITE_RUNTIME_ORIGIN: GATEWAY });
    });

    it("returns 'anonymous' for a gateway URL", () => {
      expect(mediaCrossOrigin(`${GATEWAY}/api/runtime/v1/objects/a/content`)).toBe('anonymous');
    });

    it.each([
      ['same-origin path', '/api/runtime/v1/objects/a/content'],
      ['Supabase storage', 'https://abc.supabase.co/storage/v1/object/public/image_uploads/a.png'],
      ['CDN', 'https://cdn.example.com/a.png'],
      ['another loopback port', 'http://127.0.0.1:17341/a.png'],
      ['data URL', 'data:image/png;base64,AAAA'],
      ['blob URL', 'blob:https://astrid.haus/0b1c'],
      ['empty string', ''],
      ['null', null],
      ['undefined', undefined],
    ])('returns undefined for %s', (_label, url) => {
      expect(mediaCrossOrigin(url)).toBeUndefined();
    });

    it('renders crossorigin on a gateway <img> and omits it elsewhere', () => {
      const gatewaySrc = `${GATEWAY}/api/runtime/v1/objects/a/content`;
      const otherSrc = 'https://cdn.example.com/a.png';
      const { container } = render(
        createElement('div', null,
          createElement('img', { 'data-testid': 'gateway', alt: '', src: gatewaySrc, crossOrigin: mediaCrossOrigin(gatewaySrc) }),
          createElement('img', { 'data-testid': 'other', alt: '', src: otherSrc, crossOrigin: mediaCrossOrigin(otherSrc) }),
        ),
      );
      expect(container.querySelector('[data-testid="gateway"]')?.getAttribute('crossorigin')).toBe('anonymous');
      expect(container.querySelector('[data-testid="other"]')?.hasAttribute('crossorigin')).toBe(false);
    });
  });

  describe('same-origin build (no gateway origin)', () => {
    beforeEach(() => {
      connection.setRuntimeOrigin({});
    });

    it('returns undefined for every URL, including a loopback gateway-shaped one', () => {
      expect(mediaCrossOrigin(`${GATEWAY}/api/runtime/v1/objects/a/content`)).toBeUndefined();
      expect(mediaCrossOrigin('/api/runtime/v1/objects/a/content')).toBeUndefined();
    });

    it('renders a non-gateway <img> without the attribute', () => {
      const src = '/api/runtime/v1/objects/a/content';
      const { container } = render(createElement('img', { alt: '', src, crossOrigin: mediaCrossOrigin(src) }));
      expect(container.querySelector('img')?.hasAttribute('crossorigin')).toBe(false);
    });
  });
});
