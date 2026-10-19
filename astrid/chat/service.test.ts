import { test, expect } from 'bun:test';
import { EventEmitter } from 'node:events';
import { PassThrough } from 'node:stream';
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
      const running = runChatService({ ASTRID_WORKSPACE_DISCOVERY: join(directory, 'discovery.json'), ASTRID_ACP_CWD: directory, ASTRID_ACP_BRIDGE_TOKEN: 'ours' }, factory, new PassThrough());
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

for (const alreadyEnded of [false, true]) {
  test(`Runtime stdin EOF stops chat, removes its registration and waits for ACP cleanup (alreadyEnded=${alreadyEnded})`, async () => {
    const directory = mkdtempSync(join(tmpdir(), 'astrid-chat-eof-'));
    const path = join(directory, 'chat.json');
    const previous = { endpoint: 'http://127.0.0.1:17335', token: 'other-owner' };
    writeFileSync(path, JSON.stringify(previous));
    const stdin = new PassThrough();
    if (alreadyEnded) {
      const ended = new Promise<void>(resolve => stdin.once('end', resolve));
      stdin.resume();
      stdin.end();
      await ended;
    }
    const server = new EventEmitter() as EventEmitter & Record<string, unknown>;
    let stopped = 0;
    let closedConnections = 0;
    let cleanup = 0;
    let finishCleanup!: () => void;
    const cleaning = new Promise<void>(resolve => { finishCleanup = resolve; });
    server.listen = (_port: number, host: string, ready: () => void) => {
      expect(host).toBe('127.0.0.1');
      queueMicrotask(ready);
    };
    server.close = () => { stopped++; queueMicrotask(() => server.emit('close')); };
    server.closeAllConnections = () => { closedConnections++; };
    const factory = (({ config }) => {
      expect(config.modelStateFile?.startsWith(directory)).toBe(true);
      return { server, bridge: { close: async () => { cleanup++; await cleaning; } } };
    }) as typeof createAstridAcpHttpServer;
    let finished = false;
    try {
      const running = runChatService({ ASTRID_WORKSPACE_DISCOVERY: join(directory, 'discovery.json'), ASTRID_ACP_CWD: directory, ASTRID_ACP_BRIDGE_TOKEN: 'ours' }, factory, stdin).then(() => { finished = true; });
      await new Promise(resolve => setTimeout(resolve, 0));
      if (!alreadyEnded) {
        expect(JSON.parse(readFileSync(path, 'utf8')).token).toBe('ours');
        stdin.end();
        await new Promise(resolve => setTimeout(resolve, 0));
      }
      expect(stopped).toBe(1);
      expect(closedConnections).toBe(1);
      expect(cleanup).toBe(1);
      expect(finished).toBe(false);
      if (alreadyEnded) expect(JSON.parse(readFileSync(path, 'utf8'))).toEqual(previous);
      else expect(existsSync(path)).toBe(false);
      finishCleanup();
      await running;
      expect(finished).toBe(true);
      expect(stdin.listenerCount('end')).toBe(0);
    } finally {
      finishCleanup();
      stdin.destroy();
      rmSync(directory, { recursive: true, force: true });
    }
  });
}
