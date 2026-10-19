import { z } from 'zod';

export const localAgentIdSchema = z.enum(['astrid', 'claude-code', 'codex']);
export type LocalAgentId = z.infer<typeof localAgentIdSchema>;

/** One shared table for the service's agent names and the exact recovery lines shown in the menu. */
export const LOCAL_AGENT_TABLE: Record<LocalAgentId, {
  name: string;
  signInLine: string;
  notInstalledLine?: string;
}> = {
  astrid: { name: 'Astrid', signInLine: 'Run `omp`, then `/login`.' },
  'claude-code': {
    name: 'Claude Code',
    signInLine: 'Run `claude auth login`, then come back.',
    notInstalledLine: 'Install with `curl -fsSL https://claude.ai/install.sh | bash`',
  },
  codex: {
    name: 'Codex',
    signInLine: 'Run `codex login`, then come back.',
    notInstalledLine: 'Install with `npm install -g @openai/codex`',
  },
};

export const localAgentCatalogSchema = z.object({
  agents: z.array(z.strictObject({
    id: localAgentIdSchema,
    name: z.string(),
    state: z.enum(['ready', 'sign-in', 'not-installed']),
    line: z.string().nullable(),
  })),
});
export type LocalAgentChoice = z.infer<typeof localAgentCatalogSchema>['agents'][number];

export const localAgentModelsSchema = z.object({
  availableModels: z.array(z.object({
    modelId: z.string().min(1),
    name: z.string().min(1),
    description: z.string().nullable().optional(),
  })),
  currentModelId: z.string(),
});
export type LocalAgentModels = z.infer<typeof localAgentModelsSchema>;

/** Astrid's existing opaque IDs remain unchanged; other agents have distinct stores. */
export function sessionAgentId(sessionId: string): LocalAgentId {
  if (sessionId.startsWith('claude-code:')) return 'claude-code';
  if (sessionId.startsWith('codex:')) return 'codex';
  return 'astrid';
}

