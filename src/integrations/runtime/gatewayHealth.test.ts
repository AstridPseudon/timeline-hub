import { describe, expect, it } from 'vitest';
import { appUrlFromHealth, withAppUrl } from './gatewayHealth.ts';

describe('gatewayHealth', () => {
  it('reads the local app address from a health answer', () => {
    expect(appUrlFromHealth({ status: 'ok', app_url: 'http://127.0.0.1:2222' })).toBe('http://127.0.0.1:2222');
  });

  it('gives null when the address is absent, malformed or not on the loopback', () => {
    expect(appUrlFromHealth({ status: 'ok' })).toBeNull();
    expect(appUrlFromHealth(undefined)).toBeNull();
    expect(appUrlFromHealth('ok')).toBeNull();
    for (const app_url of ['https://evil.test', 'http://127.0.0.1', 'http://127.0.0.1:2222/path', 'javascript:alert(1)', 7]) {
      expect(appUrlFromHealth({ app_url })).toBeNull();
    }
  });

  it('adds the address to an object body and leaves any other body alone', () => {
    expect(withAppUrl({ status: 'ok' }, 'http://127.0.0.1:2222')).toEqual({ status: 'ok', app_url: 'http://127.0.0.1:2222' });
    expect(withAppUrl('text', 'http://127.0.0.1:2222')).toBe('text');
    expect(withAppUrl([1], 'http://127.0.0.1:2222')).toEqual([1]);
    expect(() => withAppUrl({}, 'https://evil.test')).toThrow();
  });
});
