import { z } from 'zod';

/** Names for local agents; install and sign-in instructions come from the service. */
export const LOCAL_AGENT_TABLE = {
  astrid: { name: 'Astrid' },
  'claude-code': { name: 'Claude Code' },
  codex: { name: 'Codex' },
  hermes: { name: 'Hermes' },
} as const;

export type LocalAgentId = keyof typeof LOCAL_AGENT_TABLE;
export const LOCAL_AGENT_IDS = Object.keys(LOCAL_AGENT_TABLE) as [LocalAgentId, ...LocalAgentId[]];
export const EXTERNAL_AGENT_IDS = LOCAL_AGENT_IDS.filter((id): id is Exclude<LocalAgentId, 'astrid'> => id !== 'astrid');
export const localAgentIdSchema = z.enum(LOCAL_AGENT_IDS);

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

const localAgentModelSchema = z.object({
  modelId: z.string().min(1),
  name: z.string().min(1),
  description: z.string().nullable().optional(),
  thoughtLevel: thoughtLevelSchema.optional(),
});

export const localAgentCatalogSchema = z.object({
  agents: z.array(z.strictObject({
    id: localAgentIdSchema,
    name: z.string(),
    state: z.enum(['ready', 'sign-in', 'not-installed']),
    line: z.string().nullable(),
    signInLine: z.string().optional(),
    models: z.array(localAgentModelSchema),
    defaultModel: z.string().nullable(),
  })),
  defaultAgent: localAgentIdSchema,
});
export type LocalAgentChoice = z.infer<typeof localAgentCatalogSchema>['agents'][number];

export const localAgentModelsSchema = z.object({
  availableModels: z.array(localAgentModelSchema),
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
