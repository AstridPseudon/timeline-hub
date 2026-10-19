import { z } from 'zod';

export const localAgentIdSchema = z.enum(['astrid', 'claude-code', 'codex']);
export type LocalAgentId = z.infer<typeof localAgentIdSchema>;
export const localAgentCatalogSchema = z.object({
  agents: z.array(z.strictObject({
    id: localAgentIdSchema,
    name: z.string(),
    installed: z.boolean(),
    authStatus: z.enum(['signed-in', 'signed-out', 'unknown']),
    adapterInstalled: z.boolean(),
    installCommand: z.string().nullable(),
    loginCommand: z.string().nullable(),
  })),
});
export type LocalAgentChoice = z.infer<typeof localAgentCatalogSchema>['agents'][number];

/** Astrid's existing opaque IDs remain unchanged; other agents have distinct stores. */
export function sessionAgentId(sessionId: string): LocalAgentId {
  if (sessionId.startsWith('claude-code:')) return 'claude-code';
  if (sessionId.startsWith('codex:')) return 'codex';
  return 'astrid';
}

export const LOCAL_AGENT_SETTING_KEY = 'astrid.app.defaultAgent';

export function savedLocalAgent(): LocalAgentId {
  try {
    const value = localAgentIdSchema.safeParse(globalThis.localStorage?.getItem(LOCAL_AGENT_SETTING_KEY));
    return value.success ? value.data : 'astrid';
  } catch {
    return 'astrid';
  }
}
