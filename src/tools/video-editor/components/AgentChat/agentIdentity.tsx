import { Asterisk, Hexagon, Sparkles, type LucideProps } from 'lucide-react';
import { LOCAL_AGENT_TABLE, type LocalAgentChoice, type LocalAgentId } from '@/integrations/astrid/localAgents.ts';

export const AGENT_IDS = ['astrid', 'claude-code', 'codex'] as const satisfies readonly LocalAgentId[];

export const agentNames: Record<LocalAgentId, string> = {
  astrid: LOCAL_AGENT_TABLE.astrid.name,
  'claude-code': LOCAL_AGENT_TABLE['claude-code'].name,
  codex: LOCAL_AGENT_TABLE.codex.name,
};

const agentIcons = { astrid: Sparkles, 'claude-code': Asterisk, codex: Hexagon } as const;

/** A quiet mark that tells chats apart at a glance; the name always travels with it. */
export function AgentIcon({ agent, ...props }: { agent: LocalAgentId } & LucideProps) {
  const Icon = agentIcons[agent];
  return <Icon aria-hidden="true" {...props} />;
}

export interface AgentAvailability {
  usable: boolean;
  state: LocalAgentChoice['state'];
  line: string | null;
}

/** Unknown sign-in is represented by the service as ready so the agent can report its own auth need. */
export function agentAvailability(choice: LocalAgentChoice | undefined): AgentAvailability {
  const state = choice?.state ?? 'ready';
  return { usable: state === 'ready', state, line: choice?.line ?? null };
}
