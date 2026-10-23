import { afterEach, describe, expect, it, vi } from 'vitest';
import { agentInstructions, installCommand } from './copy.ts';

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

describe('update handoff', () => {
  it('offers the installer and the source-checkout route, and tells the agent to check first', () => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Macintosh');
    const text = agentInstructions('update', 'https://astrid.haus');
    expect(text).toContain('If you installed Astrid with the installer');
    expect(text).toContain("If you run Astrid from source checkouts: update those checkouts to their main branches and restart Astrid. Don't run the installer over them.");
    expect(text).toContain('running runtime_protocol from a git checkout');
    expect(agentInstructions('install', 'https://astrid.haus')).not.toContain('source checkouts');
  });
});
