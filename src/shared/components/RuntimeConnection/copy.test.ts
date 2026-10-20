import { afterEach, describe, expect, it, vi } from 'vitest';
import { installCommand, terminalOpeningHint } from './copy.ts';

afterEach(() => vi.restoreAllMocks());

describe('install commands', () => {
  it.each([
    ['MacIntel', 'Macintosh', 'install', 'curl -fsSL https://astrid.haus/install | sh'],
    ['Linux x86_64', 'Linux', 'install', 'curl -fsSL https://astrid.haus/install | sh'],
    ['Win32', 'Windows', 'install', 'irm https://astrid.haus/install.ps1 | iex'],
    ['MacIntel', 'Macintosh', 'update', 'curl -fsSL https://astrid.haus/install | sh -s -- --update'],
    ['Linux x86_64', 'Linux', 'update', 'curl -fsSL https://astrid.haus/install | sh -s -- --update'],
    ['Win32', 'Windows', 'update', '& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update'],
  ] as const)('%s %s %s command', (platform, os, mode, expected) => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue(platform);
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue(os);
    expect(installCommand(mode)).toBe(expected);
  });
});

describe('terminal opening hints', () => {
  it.each([
    ['MacIntel', 'Macintosh', 'Open Terminal from Applications → Utilities.'],
    ['Win32', 'Windows', 'Open Start and type PowerShell.'],
    ['Linux x86_64', 'Linux', 'Open Terminal from your applications menu.'],
    ['Other', 'Other', 'Open a terminal on your computer.'],
  ] as const)('%s %s hint', (platform, os, expected) => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue(platform);
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue(os);
    expect(terminalOpeningHint()).toBe(expected);
  });
});
