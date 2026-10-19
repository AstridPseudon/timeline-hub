import { describe, expect, it } from 'vitest';
import {
  devSessionStorageKey,
} from './devSession.ts';

const URL = 'http://127.0.0.1:54321';

describe('devSession', () => {
  it('derives the storage key from the Supabase URL hostname', () => {
    expect(devSessionStorageKey(URL)).toBe('sb-127-auth-token');
    expect(devSessionStorageKey('https://abcdef.supabase.co')).toBe('sb-abcdef-auth-token');
  });

});
