import { afterEach, describe, expect, it, vi } from 'vitest';
import { agentInstructions, installCommand, localSetupInstructions, localSetupSteps, LOCAL_SETUP } from './copy.ts';

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
  it.each(['install', 'update'] as const)('ends %s instructions with the same browser handoff', mode => {
    const text = agentInstructions(mode, 'https://astrid.haus');
    expect(text).toContain('If the installer couldn\'t open a browser, open https://astrid.haus/?connect=1.');
    expect(text).toContain('My astrid.haus tab connects by itself once Astrid answers; if it shows a Connect button, click it.');
    expect(text).toContain('Tell me to choose Allow if Chrome or Edge asks');
    expect(agentInstructions(mode, 'https://preview.example')).toContain('the page at https://preview.example can connect');
    expect(agentInstructions(mode, 'https://preview.example')).toContain('If the installer couldn\'t open a browser, open https://astrid.haus/?connect=1.');
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

  it('local setup step five gives one browser address to open', () => {
    const step = localSetupSteps()[4];
    expect(step.line).toBe('Open this address in your browser. The editor opens with your project.');
    expect(step.command).toBe(LOCAL_SETUP.openUrl);
    expect(step.commandLabel).toBe('Copy the address');
  });

  it('local setup start command is defined', () => {
    expect(LOCAL_SETUP.startCommand).not.toMatch(/job X2/i);
    expect(LOCAL_SETUP.startCommand.trim()).not.toBe('');
  });
});
