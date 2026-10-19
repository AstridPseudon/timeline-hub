import { test, expect } from 'bun:test';
import { EventEmitter } from 'node:events';
import { mkdtempSync, readFileSync, rmSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { runChatService } from './service.ts';
import type { createAstridAcpHttpServer } from './astrid-acp-bridge.ts';
import { executableNames } from './astrid-local-agents.ts';

test('Windows executable discovery keeps native exe names', () => {
  expect(executableNames('bun', 'win32')).toEqual(['bun.exe', 'bun']);
  expect(executableNames('claude', 'win32')).toEqual(['claude.exe', 'claude']);
  expect(executableNames('codex', 'linux')).toEqual(['codex']);
});

for (const bindFails of [false, true]) {
  test(`chat publishes only after binding, cleans up its registration, and preserves another owner (bindFails=${bindFails})`, async () => {
    const directory = mkdtempSync(join(tmpdir(), 'astrid-chat-service-'));
    const path = join(directory, 'chat.json');
    const previous = { endpoint: 'http://127.0.0.1:17335', token: 'other-owner' };
    writeFileSync(path, JSON.stringify(previous));
    const server = new EventEmitter() as EventEmitter & Record<string, unknown>;
    let closed = false;
    server.listen = (_port: number, host: string, ready: () => void) => {
      expect(host).toBe('127.0.0.1');
      expect(JSON.parse(readFileSync(path, 'utf8'))).toEqual(previous);
      queueMicrotask(() => bindFails ? server.emit('error', new Error('EADDRINUSE')) : ready());
    };
    server.close = () => { queueMicrotask(() => server.emit('close')); };
    server.closeAllConnections = () => {};
    const factory = (({ config }) => {
      expect(config.localMediaOnly).toBe(true);
      return { server, bridge: { close: async () => { closed = true; } } };
    }) as typeof createAstridAcpHttpServer;
    try {
      const running = runChatService({ ASTRID_WORKSPACE_DISCOVERY: join(directory, 'discovery.json'), ASTRID_ACP_CWD: directory, ASTRID_ACP_BRIDGE_TOKEN: 'ours' }, factory);
      if (bindFails) {
        await expect(running).rejects.toThrow('EADDRINUSE');
        expect(JSON.parse(readFileSync(path, 'utf8'))).toEqual(previous);
      } else {
        await new Promise(resolve => setTimeout(resolve, 0));
        expect(JSON.parse(readFileSync(path, 'utf8'))).toEqual({ ...previous, token: 'ours' });
        server.emit('close');
        await running;
        expect(existsSync(path)).toBe(false);
      }
      expect(closed).toBe(true);
    } finally { rmSync(directory, { recursive: true, force: true }); }
  });
}
