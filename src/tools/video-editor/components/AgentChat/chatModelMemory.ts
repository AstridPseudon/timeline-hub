import { EXTERNAL_AGENT_IDS, thoughtLevelSchema, type AgentThoughtLevel, type LocalAgentId } from '@/integrations/astrid/localAgents.ts';

/**
 * The model each chat last used, by session ID, so the chat list can say
 * "Codex · gpt-6.1-sol" without loading every session. Browser-local display
 * memory only: the agent's own session stays the source of truth.
 */
const CHAT_MODELS_KEY = 'astrid.app.chatModels';
const MAX_CHATS = 200;

export function readChatModels(): Record<string, string> {
  try {
    const value: unknown = JSON.parse(globalThis.localStorage?.getItem(CHAT_MODELS_KEY) ?? '{}');
    if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
    return Object.fromEntries(Object.entries(value).filter((entry): entry is [string, string] => typeof entry[1] === 'string'));
  } catch {
    return {};
  }
}

export function rememberChatModel(sessionId: string, model: string): Record<string, string> {
  const others = readChatModels();
  delete others[sessionId];
  // Newest last; the oldest chats fall out first.
  const next = Object.fromEntries([...Object.entries(others), [sessionId, model]].slice(-MAX_CHATS));
  try {
    globalThis.localStorage?.setItem(CHAT_MODELS_KEY, JSON.stringify(next));
  } catch {
    // Storage can be full or blocked; the list then shows the agent alone.
  }
  return next;
}

export interface RememberedAgentModel { id: string; name: string; description?: string | null }

const agentModelsKey = (agent: typeof EXTERNAL_AGENT_IDS[number]) => `astrid.app.agentModels.${agent}`;

/** An agent's model list from its last session, so New chat can offer it before a session starts. */
export function readAgentModels(agent: typeof EXTERNAL_AGENT_IDS[number]): RememberedAgentModel[] {
  try {
    const value: unknown = JSON.parse(globalThis.localStorage?.getItem(agentModelsKey(agent)) ?? '[]');
    return Array.isArray(value)
      ? value.filter((model): model is RememberedAgentModel => Boolean(model) && typeof model.id === 'string' && typeof model.name === 'string')
      : [];
  } catch {
    return [];
  }
}

export function rememberAgentModels(agent: typeof EXTERNAL_AGENT_IDS[number], models: RememberedAgentModel[]): void {
  try {
    globalThis.localStorage?.setItem(agentModelsKey(agent), JSON.stringify(models.map(({ id, name, description }) => ({ id, name, description: description ?? null }))));
  } catch {
    // Without storage the submenu fetches the list each time.
  }
}

const thoughtLevelsKey = (agent: LocalAgentId) => `astrid.app.modelThoughtLevels.${agent}`;
export type ModelThoughtLevels = Record<string, AgentThoughtLevel | null>;

/** Each response describes just its current model. Unseen models get no level submenu. */
export function readModelThoughtLevels(agent: LocalAgentId): ModelThoughtLevels {
  try {
    const value: unknown = JSON.parse(globalThis.localStorage?.getItem(thoughtLevelsKey(agent)) ?? '{}');
    if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
    return Object.fromEntries(Object.entries(value).flatMap<[string, AgentThoughtLevel | null]>(([id, candidate]) => {
      if (candidate === null) return [[id, null]];
      const parsed = thoughtLevelSchema.safeParse(candidate);
      return parsed.success ? [[id, parsed.data]] : [];
    }));
  } catch { return {}; }
}

export function rememberModelThoughtLevel(agent: LocalAgentId, model: string, level?: AgentThoughtLevel): ModelThoughtLevels {
  const previous = readModelThoughtLevels(agent);
  delete previous[model];
  const next = Object.fromEntries([...Object.entries(previous), [model, level ?? null]].slice(-MAX_CHATS));
  try { globalThis.localStorage?.setItem(thoughtLevelsKey(agent), JSON.stringify(next)); } catch { /* Display cache only. */ }
  return next;
}
