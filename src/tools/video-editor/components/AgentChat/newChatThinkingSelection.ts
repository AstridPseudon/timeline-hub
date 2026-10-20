import type { LocalAgentId } from '@/integrations/astrid/localAgents.ts';

const MAX_SELECTIONS = 200;
const thoughtSelectionsKey = (agent: LocalAgentId) => `astrid.app.modelThoughtSelections.${agent}`;

/** Explicit New-menu choices only; offered levels and model defaults come from the service. */
export function readModelThoughtSelections(agent: LocalAgentId): Record<string, string> {
  try {
    const value: unknown = JSON.parse(globalThis.localStorage?.getItem(thoughtSelectionsKey(agent)) ?? '{}');
    if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
    return Object.fromEntries(Object.entries(value).filter((entry): entry is [string, string] => typeof entry[1] === 'string'));
  } catch { return {}; }
}

export function rememberModelThoughtSelection(agent: LocalAgentId, model: string, value: string): Record<string, string> {
  const previous = readModelThoughtSelections(agent);
  delete previous[model];
  const next = Object.fromEntries([...Object.entries(previous), [model, value]].slice(-MAX_SELECTIONS));
  try { globalThis.localStorage?.setItem(thoughtSelectionsKey(agent), JSON.stringify(next)); } catch { /* The menu retains its in-memory choice. */ }
  return next;
}
