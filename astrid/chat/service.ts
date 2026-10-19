import { randomBytes } from 'node:crypto';
import { isAbsolute } from 'node:path';
import { createAstridAcpHttpServer, resolveAstridAcpBridgeConfig } from './astrid-acp-bridge.ts';
import { chatRegistration, chatRegistrationPath, removeChatRegistration, writeChatRegistration } from './chat-registration.ts';

export async function runChatService(env = process.env, createServer = createAstridAcpHttpServer): Promise<void> {
  const discovery = env.ASTRID_WORKSPACE_DISCOVERY?.trim();
  if (!discovery || !isAbsolute(discovery)) throw new Error('ASTRID_WORKSPACE_DISCOVERY must be an explicit absolute path');
  const config = resolveAstridAcpBridgeConfig({
    ...env,
    ASTRID_ACP_BRIDGE_TOKEN: env.ASTRID_ACP_BRIDGE_TOKEN?.trim() || randomBytes(32).toString('base64url'),
    ASTRID_ACP_LOCAL_MEDIA_ONLY: '1',
  });
  const { server, bridge } = createServer({ config });
  const path = chatRegistrationPath(discovery);
  const registration = chatRegistration(config.port, config.token);
  const release = () => removeChatRegistration(path, value => value?.endpoint === registration.endpoint && value?.token === registration.token);
  let stopping: Promise<void> | undefined;
  const stop = () => stopping ??= (async () => {
    release();
    server.close();
    server.closeAllConnections();
    await bridge.close();
  })();
  try {
    await new Promise<void>((resolve, reject) => {
      server.once('error', reject);
      server.listen(config.port, '127.0.0.1', resolve);
    });
    // Publish only after our own listener bound successfully.
    writeChatRegistration(path, registration);
    process.once('exit', release);
    process.once('SIGINT', stop);
    process.once('SIGTERM', stop);
    console.log(`Astrid chat listening on 127.0.0.1:${config.port}`);
    await new Promise<void>((resolve, reject) => {
      server.once('close', resolve);
      server.once('error', reject);
    });
  } finally {
    await stop();
    process.removeListener('exit', release);
    process.removeListener('SIGINT', stop);
    process.removeListener('SIGTERM', stop);
  }
}

if (import.meta.main) await runChatService();
