import { Asterisk, Hexagon, Sparkles, type LucideProps } from 'lucide-react';
import type { LocalAgentChoice, LocalAgentId } from '@/integrations/astrid/localAgents.ts';

export const AGENT_IDS = ['astrid', 'claude-code', 'codex'] as const satisfies readonly LocalAgentId[];

export const agentNames: Record<LocalAgentId, string> = {
  astrid: 'Astrid',
  'claude-code': 'Claude Code',
  codex: 'Codex',
};

const agentIcons = { astrid: Sparkles, 'claude-code': Asterisk, codex: Hexagon } as const;

/** A quiet mark that tells chats apart at a glance; the name always travels with it. */
export function AgentIcon({ agent, ...props }: { agent: LocalAgentId } & LucideProps) {
  const Icon = agentIcons[agent];
  return <Icon aria-hidden="true" {...props} />;
}

export interface AgentAvailability {
  usable: boolean;
  status: string;
  detail: string;
  installCommand?: string;
  loginCommand?: string;
}

/** Whether a new chat can start with this agent, from its CLI, sign-in and adapter state. */
export function agentAvailability(id: LocalAgentId, choice: LocalAgentChoice | undefined, { astridSignedIn, loading }: { astridSignedIn: boolean; loading: boolean }): AgentAvailability {
  if (id === 'astrid') return { usable: true, status: astridSignedIn ? 'Signed in' : 'Not signed in', detail: 'OMP models' };
  const login = id === 'claude-code' ? 'Your Claude login' : 'Your ChatGPT login';
  if (!choice) return { usable: false, status: loading ? 'Checking availability…' : 'Status unavailable', detail: login };
  if (!choice.installed) return { usable: false, status: 'CLI not installed', detail: login };
  const auth = choice.authStatus === 'signed-in' ? 'Signed in' : choice.authStatus === 'signed-out' ? 'Signed out' : 'Sign-in status unknown';
  const detail = `${login} · ${auth}`;
  if (!choice.adapterInstalled) {
    return { usable: false, status: 'Available to install', detail, installCommand: choice.installCommand ?? undefined, loginCommand: choice.authStatus === 'signed-out' ? choice.loginCommand ?? undefined : undefined };
  }
  if (choice.authStatus === 'signed-out') return { usable: false, status: 'Signed out', detail, loginCommand: choice.loginCommand ?? undefined };
  // Some CLIs cannot report sign-in; let the chat start and the agent say if it needs a login.
  if (choice.authStatus === 'unknown') return { usable: true, status: 'Sign-in status unknown', detail };
  return { usable: true, status: 'Signed in', detail };
}
