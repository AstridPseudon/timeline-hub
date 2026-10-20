import { z } from 'zod';

/** One shared table for the service's agent names and the exact recovery lines shown in the menu. */
export const LOCAL_AGENT_TABLE = {
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
  hermes: {
    name: 'Hermes',
    signInLine: 'Run `hermes setup`, then come back.',
    notInstalledLine: 'Install with `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`',
    notInstalledLineWindows: 'Install with `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`',
  },
} as const;

export type LocalAgentId = keyof typeof LOCAL_AGENT_TABLE;
export const LOCAL_AGENT_IDS = Object.keys(LOCAL_AGENT_TABLE) as [LocalAgentId, ...LocalAgentId[]];
export const EXTERNAL_AGENT_IDS = LOCAL_AGENT_IDS.filter((id): id is Exclude<LocalAgentId, 'astrid'> => id !== 'astrid');
export const localAgentIdSchema = z.enum(LOCAL_AGENT_IDS);

export const localAgentCatalogSchema = z.object({
  agents: z.array(z.strictObject({
    id: localAgentIdSchema,
    name: z.string(),
    state: z.enum(['ready', 'sign-in', 'not-installed']),
    line: z.string().nullable(),
  })),
});
export type LocalAgentChoice = z.infer<typeof localAgentCatalogSchema>['agents'][number];

export const thoughtLevelSchema = z.object({
  configId: z.string().min(1),
  name: z.string(),
  currentValue: z.string(),
  options: z.array(z.object({ value: z.string().min(1), name: z.string(), description: z.string().nullable().optional() })),
  recommendedValue: z.string().optional(),
});
export type AgentThoughtLevel = z.infer<typeof thoughtLevelSchema>;

export function defaultThoughtLevel(level: AgentThoughtLevel): string {
  return level.recommendedValue ?? level.options.find(option => option.value === 'default')?.value ?? level.currentValue;
}

export const localAgentModelsSchema = z.object({
  availableModels: z.array(z.object({
    modelId: z.string().min(1),
    name: z.string().min(1),
    description: z.string().nullable().optional(),
  })),
  currentModelId: z.string(),
  modelConfigId: z.string().optional(),
  /** Only the current model's advertised levels; never infer another model's support. */
  thoughtLevel: thoughtLevelSchema.optional(),
});
export type LocalAgentModels = z.infer<typeof localAgentModelsSchema>;

/** Astrid's existing opaque IDs remain unchanged; other agents have distinct stores. */
export function sessionAgentId(sessionId: string): LocalAgentId {
  for (const id of EXTERNAL_AGENT_IDS) if (isExternalAgentSession(sessionId, id)) return id;
  return 'astrid';
}

export function isExternalAgentSession(sessionId: string, agent?: typeof EXTERNAL_AGENT_IDS[number]): boolean {
  return agent ? sessionId.startsWith(`${agent}:`) : EXTERNAL_AGENT_IDS.some(id => sessionId.startsWith(`${id}:`));
}

export function localAgentInstallLine(agent: LocalAgentId, platform?: 'windows' | 'posix'): string | null {
  const install: { name: string; notInstalledLine?: string; notInstalledLineWindows?: string } = LOCAL_AGENT_TABLE[agent];
  const targetPlatform = platform ?? (typeof navigator !== 'undefined' && /Win/i.test(navigator.userAgent) ? 'windows' : 'posix');
  return targetPlatform === 'windows' ? install.notInstalledLineWindows ?? install.notInstalledLine ?? null : install.notInstalledLine ?? null;
}

export const LOCAL_AGENT_SETTING_KEY = 'astrid.app.defaultAgent';
export const LOCAL_AGENT_CHANGED_EVENT = 'astrid:local-agent-changed';
export const localAgentModelSettingKey = (agent: LocalAgentId) => `astrid.app.defaultModel.${agent}`;

export function savedLocalAgentModel(agent: LocalAgentId): string | undefined {
  try {
    return globalThis.localStorage?.getItem(localAgentModelSettingKey(agent)) || undefined;
  } catch {
    return undefined;
  }
}

export function savedLocalAgent(): LocalAgentId {
  try {
    const value = localAgentIdSchema.safeParse(globalThis.localStorage?.getItem(LOCAL_AGENT_SETTING_KEY));
    return value.success ? value.data : 'astrid';
  } catch {
    return 'astrid';
  }
}

export function saveLocalAgent(agent: LocalAgentId): void {
  try { globalThis.localStorage?.setItem(LOCAL_AGENT_SETTING_KEY, agent); } catch { /* Storage can be blocked. */ }
  if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(LOCAL_AGENT_CHANGED_EVENT, { detail: agent }));
}
