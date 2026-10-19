// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest';
import { readAgentModels, readChatModels, rememberAgentModels, rememberChatModel } from './chatModelMemory.ts';

afterEach(() => localStorage.clear());

describe('chatModelMemory', () => {
  it('remembers the latest model per chat, newest last', () => {
    rememberChatModel('codex:a', '6 Sol');
    rememberChatModel('claude-code:b', 'Opus');
    expect(rememberChatModel('codex:a', '6 Luna')).toEqual({ 'claude-code:b': 'Opus', 'codex:a': '6 Luna' });
    expect(readChatModels()).toEqual({ 'claude-code:b': 'Opus', 'codex:a': '6 Luna' });
  });

  it('ignores damaged storage', () => {
    localStorage.setItem('astrid.app.chatModels', '[1,2]');
    localStorage.setItem('astrid.app.agentModels.codex', '{"id":1}');
    expect(readChatModels()).toEqual({});
    expect(readAgentModels('codex')).toEqual([]);
  });

  it('remembers each agent\'s model list', () => {
    rememberAgentModels('codex', [{ id: 'gpt-6-sol', name: '6 Sol', description: 'Workhorse' }, { id: 'gpt-6-luna', name: '6 Luna' }]);
    expect(readAgentModels('codex')).toEqual([{ id: 'gpt-6-sol', name: '6 Sol', description: 'Workhorse' }, { id: 'gpt-6-luna', name: '6 Luna', description: null }]);
    expect(readAgentModels('claude-code')).toEqual([]);
  });
});
