import { useState } from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';
import type { LocalAgentChoice, LocalAgentId } from '@/integrations/astrid/localAgents.ts';

interface AgentChatModelSelectorProps {
  catalog: AcpModelCatalog;
  onSelectModel: (model: string) => void | Promise<void>;
  selectionError?: string | null;
  busy?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  loading?: boolean;
  catalogError?: string | null;
  agents?: LocalAgentChoice[];
  selectedAgent?: LocalAgentId;
  onSelectAgent?: (agent: LocalAgentId) => void | Promise<void>;
  agentsLoading?: boolean;
  agentsError?: string | null;
}

const agentNames: Record<LocalAgentId, string> = {
  astrid: 'Astrid',
  'claude-code': 'Claude Code',
  codex: 'Codex',
};

export function AgentChatModelSelector({ catalog, onSelectModel, selectionError = null, busy = false, open: controlledOpen, onOpenChange, loading = false, catalogError = null, agents, selectedAgent = 'astrid', onSelectAgent, agentsLoading = false, agentsError = null }: AgentChatModelSelectorProps) {
  const [localOpen, setLocalOpen] = useState(false);
  const open = controlledOpen ?? localOpen;
  const changeOpen = (next: boolean) => { setLocalOpen(next); onOpenChange?.(next); };
  const current = catalog.providers.flatMap(provider => provider.models.map(model => ({ provider, model })))
    .find(item => `${item.provider.id}/${item.model.id}` === catalog.currentModel);
  const openList = () => changeOpen(true);
  const agentChoices = agents ?? [];
  const selectedAgentName = agentNames[selectedAgent];

  const agentState = (id: LocalAgentId): { disabled: boolean; status: string; installCommand?: string; loginCommand?: string; authLabel?: string } => {
    if (id === 'astrid') {
      const signedIn = catalog.providers.some(provider => provider.signedIn);
      return { disabled: busy, status: signedIn ? 'Signed in' : 'Choose a model or sign in to an OMP provider' };
    }
    const agent = agentChoices.find(choice => choice.id === id);
    if (!agent) return { disabled: true, status: agentsLoading ? 'Checking availability…' : 'Status unavailable' };
    if (!agent.installed) return { disabled: true, status: 'CLI not installed' };
    const authLabel = agent.authStatus === 'signed-in' ? 'Signed in' : agent.authStatus === 'signed-out' ? 'Signed out' : 'Sign-in status unknown';
    if (!agent.adapterInstalled) return { disabled: true, status: 'Available to install', installCommand: agent.installCommand ?? undefined, loginCommand: agent.authStatus === 'signed-out' ? agent.loginCommand ?? undefined : undefined, authLabel };
    if (agent.authStatus === 'signed-out') return { disabled: true, status: 'Signed out', loginCommand: agent.loginCommand ?? undefined, authLabel };
    if (agent.authStatus === 'unknown') return { disabled: true, status: 'Sign-in status unknown', authLabel };
    return { disabled: busy, status: 'Signed in', authLabel };
  };

  const selectAgent = (id: LocalAgentId) => {
    const state = agentState(id);
    if (state.disabled || !onSelectAgent) return;
    void Promise.resolve(onSelectAgent(id)).catch(() => undefined);
    changeOpen(false);
  };

  return (
    <div className="flex min-w-0 flex-col items-end">
      <Popover open={open} onOpenChange={changeOpen}>
        <PopoverTrigger asChild>
          <button type="button" role="combobox" aria-label="Agent model" aria-expanded={open}
            className="flex h-7 max-w-36 min-w-0 items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring">
            <span className="truncate">{selectedAgent === 'astrid' ? current?.model.name ?? catalog.currentModel ?? 'Choose model' : selectedAgentName}</span>
            <ChevronsUpDown className="h-3.5 w-3.5 shrink-0 opacity-50" aria-hidden="true" />
          </button>
        </PopoverTrigger>
        <PopoverContent align="end" className="w-72 max-w-[calc(100vw-2rem)] p-2">
          <div className="max-h-80 space-y-3 overflow-y-auto">
            {(agents !== undefined || agentsLoading || agentsError) && <>
              <section aria-label="Local agents">
                <h3 className="px-2 pb-1 text-[11px] font-semibold text-muted-foreground">Agent</h3>
                {agentsLoading && <p className="px-2 py-1 text-[11px] text-muted-foreground">Checking agent availability…</p>}
                {agentsError && <p role="alert" className="px-2 py-1 text-[11px] text-destructive">Could not load agents: {agentsError}</p>}
                {(['astrid', 'claude-code', 'codex'] as const).map(id => {
                  const state = agentState(id);
                  const selected = selectedAgent === id;
                  return <div key={id} className="px-2 py-1">
                    <button type="button" disabled={state.disabled || !onSelectAgent} aria-current={selected ? 'true' : undefined}
                      className="flex w-full items-center gap-2 rounded text-left text-xs disabled:opacity-50"
                      onClick={() => selectAgent(id)}>
                      <Check className={`h-3.5 w-3.5 shrink-0 ${selected ? 'opacity-100' : 'opacity-0'}`} aria-hidden="true" />
                      <span className="font-medium">{agentNames[id]}</span>
                      <span className="ml-auto text-[11px] text-muted-foreground">{state.status}</span>
                    </button>
                    {state.installCommand && <p className="pl-5 text-[11px] text-muted-foreground"><span>Install adapter: </span><code>{state.installCommand}</code></p>}
                    {state.loginCommand && <p className="pl-5 text-[11px] text-muted-foreground"><span>Sign in: run </span><code>{state.loginCommand}</code></p>}
                    {id === 'astrid' && <p className="pl-5 text-[11px] text-muted-foreground">OMP models</p>}
                    {id === 'claude-code' && <p className="pl-5 text-[11px] text-muted-foreground">Your Claude login{state.authLabel && <> · {state.authLabel}</>}</p>}
                    {id === 'codex' && <p className="pl-5 text-[11px] text-muted-foreground">Your ChatGPT login{state.authLabel && <> · {state.authLabel}</>}</p>}
                  </div>;
                })}
                <p className="px-2 pt-1 text-[11px] text-muted-foreground">Agent selection affects new chats only. Saved chats keep their original agent.</p>
              </section>
              {selectedAgent !== 'astrid' && <p className="px-2 py-1 text-xs text-muted-foreground">Uses your {selectedAgentName} default model. New chats use this agent; saved chats keep their original agent.</p>}
            </>}
            {selectedAgent === 'astrid' && <>
            {loading && <p className="px-2 py-1 text-xs text-muted-foreground">Loading models…</p>}
            {catalogError && <p role="alert" className="px-2 py-1 text-xs text-destructive">Could not load models: {catalogError}</p>}
            {!loading && !catalogError && catalog.providers.length === 0 && <p className="px-2 py-1 text-xs text-muted-foreground">No models available.</p>}
            {catalog.providers.map(provider => (
              <section key={provider.id} aria-label={provider.name}>
                <h3 className="px-2 pb-1 text-[11px] font-semibold text-muted-foreground">{provider.name}</h3>
                {provider.signedIn && provider.models.length === 0 && <p className="px-2 py-1 text-[11px] text-muted-foreground">Signed in. No enabled models; check <code>omp models ls</code>.</p>}
                {provider.signedIn || provider.models.length > 0 ? provider.models.map(model => {
                  const id = `${provider.id}/${model.id}`;
                  const selected = catalog.currentModel === id;
                  return <button key={id} type="button" disabled={busy} aria-current={selected ? 'true' : undefined}
                    className="flex w-full items-center gap-2 rounded px-2 py-1.5 text-left text-xs hover:bg-accent disabled:opacity-50"
                    onClick={() => { void Promise.resolve(onSelectModel(id)).catch(() => undefined); changeOpen(false); }}>
                    <Check className={`h-3.5 w-3.5 shrink-0 ${selected ? 'opacity-100' : 'opacity-0'}`} aria-hidden="true" />
                    <span className="truncate">{model.name}</span>
                  </button>;
                }) : <p className="px-2 py-1 text-[11px] text-muted-foreground">Sign in: run <code>omp</code>, then <code>/login</code></p>}
              </section>
            ))}
            </>}
          </div>
        </PopoverContent>
      </Popover>
      {selectionError && <p role="alert" className="mt-1 max-w-64 text-right text-[10px] text-destructive">{selectionError} <button type="button" className="underline" onClick={openList}>Switch model</button></p>}
    </div>
  );
}
