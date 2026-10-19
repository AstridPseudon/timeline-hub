import { afterEach, describe, expect, it, vi } from 'vitest';
import { ASTRID_COMMANDS, installCommand } from './copy.ts';

afterEach(() => vi.restoreAllMocks());

describe('install commands', () => {
  it.each([
    ['MacIntel', 'Macintosh', 'install', ASTRID_COMMANDS.macLinux],
    ['Linux x86_64', 'Linux', 'install', ASTRID_COMMANDS.macLinux],
    ['Win32', 'Windows', 'install', ASTRID_COMMANDS.windows],
    ['MacIntel', 'Macintosh', 'update', ASTRID_COMMANDS.macLinuxUpdate],
    ['Linux x86_64', 'Linux', 'update', ASTRID_COMMANDS.macLinuxUpdate],
    ['Win32', 'Windows', 'update', ASTRID_COMMANDS.windowsUpdate],
  ] as const)('%s %s %s command', (platform, os, mode, expected) => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue(platform);
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue(os);
    expect(installCommand(mode)).toBe(expected);
  });
});
