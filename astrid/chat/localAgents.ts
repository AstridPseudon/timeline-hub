import { z } from 'zod';
import { dirname, isAbsolute, join, win32 } from 'node:path';

export const localAgentIdSchema = z.enum(['astrid', 'claude-code', 'codex']);
export type LocalAgentId = z.infer<typeof localAgentIdSchema>;

function astridSignInLine(): string {
  const configuredRoot = process.env.ASTRID_INSTALL_PROGRAM_ROOT;
  const servicePython = process.env.ASTRID_SERVICE_PYTHON;
  const fromService = servicePython && isAbsolute(servicePython)
    ? [1, 2, 3, 4, 5].reduce(path => dirname(path), servicePython)
    : undefined;
  const home = process.env.USERPROFILE || process.env.HOME || '.';
  const defaultRoot = process.platform === 'win32'
    ? join(process.env.LOCALAPPDATA || join(home, 'AppData', 'Local'), 'Astrid')
    : join(process.env.XDG_DATA_HOME || join(home, '.local', 'share'), 'astrid');
  const root = configuredRoot && isAbsolute(configuredRoot) ? configuredRoot
    : fromService || defaultRoot;
  if (process.platform === 'win32') {
    const launcher = win32.join(root, 'run-astrid.cmd').replaceAll("'", "''");
    return `Run \`& '${launcher}'\`, then enter \`/login\` in Astrid.`;
  }
  const launcher = join(root, 'run-astrid').replaceAll("'", "'\"'\"'");
  return `Run \`'${launcher}'\`, then enter \`/login\` in Astrid.`;
}

/** One shared table for the service's agent names and the exact recovery lines shown in the menu. */
export const LOCAL_AGENT_TABLE: Record<LocalAgentId, {
  name: string;
  signInLine: string;
  notInstalledLine?: string;
  windowsNotInstalledLine?: string;
}> = {
  astrid: { name: 'Astrid', signInLine: astridSignInLine() },
  'claude-code': {
    name: 'Claude Code',
    signInLine: 'Run `claude auth login`, then come back.',
    notInstalledLine: 'Install with `curl -fsSL https://claude.ai/install.sh | bash`',
    windowsNotInstalledLine: 'Install with `npm install -g @anthropic-ai/claude-code`',
  },
  codex: {
    name: 'Codex',
    signInLine: 'Run `codex login`, then come back.',
    notInstalledLine: 'Install with `npm install -g @openai/codex`',
  },
};

const agentModelSchema = z.object({
  modelId: z.string().min(1),
  name: z.string().min(1),
  description: z.string().nullable().optional(),
});

export const localAgentCatalogSchema = z.object({
  defaultAgent: localAgentIdSchema,
  agents: z.array(z.strictObject({
    id: localAgentIdSchema,
    name: z.string(),
    state: z.enum(['ready', 'sign-in', 'not-installed']),
    line: z.string().nullable(),
    signInLine: z.string().optional(),
    models: z.array(agentModelSchema),
    defaultModel: z.string().nullable(),
  })),
});
export type LocalAgentChoice = Pick<z.infer<typeof localAgentCatalogSchema>['agents'][number], 'id' | 'name' | 'state' | 'line'>;

export const localAgentModelsSchema = z.object({
  availableModels: z.array(agentModelSchema),
  currentModelId: z.string(),
});
export type LocalAgentModels = z.infer<typeof localAgentModelsSchema>;

/** Astrid's existing opaque IDs remain unchanged; other agents have distinct stores. */
export function sessionAgentId(sessionId: string): LocalAgentId {
  if (sessionId.startsWith('claude-code:')) return 'claude-code';
  if (sessionId.startsWith('codex:')) return 'codex';
  return 'astrid';
}

