// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest';
import { EXTERNAL_AGENT_IDS, LOCAL_AGENT_IDS, LOCAL_AGENT_SETTING_KEY, LOCAL_AGENT_TABLE, isExternalAgentSession, localAgentInstallLine, saveLocalAgent, savedLocalAgent, sessionAgentId } from './localAgents.ts';

afterEach(() => localStorage.clear());

describe('local agent registry', () => {
  it('keeps external IDs and session routing in sync', () => {
    expect(LOCAL_AGENT_IDS).toEqual(['astrid', 'claude-code', 'codex', 'hermes']);
    for (const agent of EXTERNAL_AGENT_IDS) {
      expect(isExternalAgentSession(`${agent}:chat-1`)).toBe(true);
      expect(sessionAgentId(`${agent}:chat-1`)).toBe(agent);
    }
    expect(sessionAgentId('opaque-astrid-chat')).toBe('astrid');
  });

  it('persists Hermes in the existing default-agent setting', () => {
    saveLocalAgent('hermes');
    expect(localStorage.getItem(LOCAL_AGENT_SETTING_KEY)).toBe('hermes');
    expect(savedLocalAgent()).toBe('hermes');
  });

  it('offers one platform-specific Hermes installer command', () => {
    expect(localAgentInstallLine('hermes', 'posix')).toBe('Install with `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`');
    expect(localAgentInstallLine('hermes', 'windows')).toBe('Install with `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`');
    expect(localAgentInstallLine('hermes', 'windows')).not.toContain('curl');
  });

  it('shows Hermes sign-in recovery instructions', () => {
    expect(LOCAL_AGENT_TABLE.hermes.signInLine).toBe('Run `hermes setup`, then come back.');
  });
});
