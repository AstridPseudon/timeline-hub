import { afterEach, describe, expect, it, vi } from 'vitest';
import { agentInstructions, installCommand, localSetupInstructions, LOCAL_SETUP } from './copy.ts';

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

describe('onboarding instructions', () => {
  it('ends web instructions with the chosen window mode', () => {
    expect(agentInstructions('install', 'https://astrid.haus', 'app-window')).toMatch(/When Astrid is running, open it in the installed Astrid app if it exists, otherwise https:\/\/astrid\.haus in my browser\.$/);
    expect(agentInstructions('install', 'https://astrid.haus', 'browser-tab')).toMatch(/When Astrid is running, open it at https:\/\/astrid\.haus in my browser\.$/);
  });

  it('returns the fully local instructions', () => {
    const text = localSetupInstructions();
    expect(text).toContain('Please set up Astrid to run fully on this computer, including the editor, so I can change Astrid itself.');
    expect(text).toContain('https://github.com/banodoco/astrid-app');
    expect(text).toContain('npm run dev:local');
    expect(text.match(/npx -y npm@11 ci/g)).toHaveLength(2);
    expect(text).not.toContain('npm ci');
    expect(text).toContain('http://127.0.0.1:5180/tools/video-editor?connect=1');
    expect(text).toContain(LOCAL_SETUP.startCommand);
  });

  it('uses the set-up title that matches the permission screen', async () => {
    const { RUNTIME_CONNECTION_COPY } = await import('./copy.ts');
    expect(RUNTIME_CONNECTION_COPY.setUp.title).toBe('Set up Astrid on this computer');
    expect(RUNTIME_CONNECTION_COPY.permission.title).toBe('Connect to Astrid on this computer');
  });

  it('local setup start command is defined', () => {
    expect(LOCAL_SETUP.startCommand).not.toMatch(/job X2/i);
    expect(LOCAL_SETUP.startCommand.trim()).not.toBe('');
  });
});
