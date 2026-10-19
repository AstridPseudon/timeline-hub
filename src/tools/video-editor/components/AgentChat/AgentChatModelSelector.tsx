import { Fragment, useState } from 'react';
import { Check, ChevronRight, ChevronsUpDown, Loader2, X } from 'lucide-react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/shared/components/ui/command.tsx';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import { cn } from '@/shared/components/ui/contracts/cn';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';
import type { LocalAgentChoice, LocalAgentId } from '@/integrations/astrid/localAgents.ts';

type Provider = AcpModelCatalog['providers'][number];
type UsageLimit = NonNullable<Provider['usage']>['limits'][number];

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
const AGENT_IDS = ['astrid', 'claude-code', 'codex'] as const;

type AgentState = { disabled: boolean; status: string; installCommand?: string; loginCommand?: string; authLabel?: string };

const KEYCAP = 'verbatim-case rounded border border-border px-1 font-mono text-[10px]';
/** Past this many keyless models, each keyless provider folds into one row. */
const FOLD_OVER = 40;
/** An unfolded provider lists this many models; search reaches the rest. */
const UNFOLD_LIMIT = 100;
/** Search shows this many matches; typing more narrows them. */
const SEARCH_LIMIT = 50;

function matches(tokens: string[], text: string): boolean {
  const haystack = text.toLowerCase();
  return tokens.every((token) => haystack.includes(token));
}

function usedFraction(limit: UsageLimit): number | null {
  if (limit.usedFraction !== undefined) return limit.usedFraction;
  if (limit.remainingFraction !== undefined) return 1 - limit.remainingFraction;
  if (limit.used !== undefined && limit.limit) return limit.used / limit.limit;
  return null;
}

function windowLabel(durationMs: number | undefined): string {
  if (!durationMs) return '';
  const hours = durationMs / 3_600_000;
  if (hours >= 24 * 6.5 && hours <= 24 * 7.5) return 'weekly ';
  if (hours >= 23 && hours <= 25) return 'daily ';
  return hours >= 1 ? `${Math.round(hours)}-hour ` : `${Math.round(durationMs / 60_000)}-minute `;
}

function resetLabel(resetsAt: number | undefined): string {
  if (!resetsAt) return '';
  const date = new Date(resetsAt < 1e12 ? resetsAt * 1000 : resetsAt);
  if (Number.isNaN(date.getTime())) return '';
  const sameDay = date.toDateString() === new Date().toDateString();
  return `, resets ${sameDay ? date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : date.toLocaleDateString([], { month: 'short', day: 'numeric' })}`;
}

/** The tightest limit as one short figure; every limit in the tooltip. */
export function summarizeUsage(usage: Provider['usage']) {
  const limits = (usage?.limits ?? []).map((limit) => ({ limit, fraction: usedFraction(limit) }))
    .filter((entry) => entry.fraction !== null || entry.limit.status === 'exhausted');
  if (limits.length === 0) return null;
  const tightest = limits.reduce((worst, entry) => {
    const rank = (item: typeof entry) => item.limit.status === 'exhausted' ? 2 : item.fraction ?? 0;
    return rank(entry) > rank(worst) ? entry : worst;
  });
  const fraction = Math.min(1, Math.max(0, tightest.fraction ?? 1));
  const exhausted = tightest.limit.status === 'exhausted' || fraction >= 1;
  const warning = !exhausted && (tightest.limit.status === 'warning' || fraction >= 0.8);
  return {
    fraction,
    text: exhausted ? 'Limit reached' : `${Math.round(fraction * 100)}% used`,
    tone: exhausted ? 'exhausted' as const : warning ? 'warning' as const : 'ok' as const,
    detail: limits.map(({ limit, fraction: used }) => `${used === null ? 'Limit reached' : `${Math.round(Math.min(1, used) * 100)}% of ${windowLabel(limit.durationMs)}limit used`}${resetLabel(limit.resetsAt)}`).join('\n'),
  };
}

function ProviderHeading({ provider }: { provider: Provider }) {
  const usage = summarizeUsage(provider.usage);
  return (
    <span className="flex min-w-0 items-center gap-2">
      <span className="min-w-0 truncate normal-case">{provider.name}</span>
      {usage && (
        <span title={usage.detail} className={cn('ml-auto flex shrink-0 items-center gap-1.5 text-[10px] tabular-nums',
          usage.tone === 'exhausted' ? 'text-destructive' : usage.tone === 'warning' ? 'icon-warning' : 'text-muted-foreground')}>
          <span aria-hidden="true" className="h-1 w-6 overflow-hidden rounded-full bg-border">
            <span className="block h-full rounded-full bg-current" style={{ width: `${Math.max(usage.fraction * 100, 4)}%` }} />
          </span>
          {usage.text}
        </span>
      )}
    </span>
  );
}

export function AgentChatModelSelector({ catalog, onSelectModel, selectionError = null, busy = false, open: controlledOpen, onOpenChange, loading = false, catalogError = null, agents, selectedAgent = 'astrid', onSelectAgent, agentsLoading = false, agentsError = null }: AgentChatModelSelectorProps) {
  const [localOpen, setLocalOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [showSignedOut, setShowSignedOut] = useState(false);
  const [unfolded, setUnfolded] = useState<ReadonlySet<string> | null>(null);
  const [dismissedError, setDismissedError] = useState<string | null>(null);
  const open = controlledOpen ?? localOpen;
  const changeOpen = (next: boolean) => {
    setLocalOpen(next);
    if (!next) { setQuery(''); setShowSignedOut(false); setUnfolded(null); }
    onOpenChange?.(next);
  };
  const current = catalog.providers.flatMap(provider => provider.models.map(model => ({ provider, model })))
    .find(item => `${item.provider.id}/${item.model.id}` === catalog.currentModel);
  const signedIn = catalog.providers.filter(provider => provider.signedIn);
  // Keyless providers (local models, for example) are usable without signing in.
  const keyless = catalog.providers.filter(provider => !provider.signedIn && provider.models.length > 0);
  const signedOut = catalog.providers.filter(provider => !provider.signedIn && provider.models.length === 0);
  const fold = keyless.reduce((count, provider) => count + provider.models.length, 0) > FOLD_OVER;
  const openProviders = unfolded ?? new Set(current ? [current.provider.id] : []);
  const toggleProvider = (id: string) => setUnfolded(() => {
    const next = new Set(openProviders);
    if (!next.delete(id)) next.add(id);
    return next;
  });
  const tokens = query.toLowerCase().split(/\s+/).filter(Boolean);
  const searching = tokens.length > 0;
  const results = searching ? [...signedIn, ...keyless].flatMap(provider => provider.models
    .filter(model => matches(tokens, `${provider.name} ${model.name} ${provider.id}/${model.id}`))
    .map(model => ({ provider, model }))) : [];
  const shownResults = results.slice(0, SEARCH_LIMIT);
  const resultGroups = [...new Set(shownResults.map(result => result.provider))]
    .map(provider => ({ provider, models: shownResults.filter(result => result.provider === provider).map(result => result.model) }));
  const listedSignedOut = searching ? signedOut.filter(provider => matches(tokens, provider.name)) : showSignedOut ? signedOut : [];
  const agentChoices = agents ?? [];
  const showAgents = agents !== undefined || agentsLoading || Boolean(agentsError);
  const astridSelected = selectedAgent === 'astrid';
  const agentState = (id: LocalAgentId): AgentState => {
    if (id === 'astrid') {
      return { disabled: busy, status: catalog.providers.some(provider => provider.signedIn) ? 'Signed in' : 'Not signed in' };
    }
    const agent = agentChoices.find(choice => choice.id === id);
    if (!agent) return { disabled: true, status: agentsLoading ? 'Checking availability…' : 'Status unavailable' };
    if (!agent.installed) return { disabled: true, status: 'CLI not installed' };
    const authLabel = agent.authStatus === 'signed-in' ? 'Signed in' : agent.authStatus === 'signed-out' ? 'Signed out' : 'Sign-in status unknown';
    if (!agent.adapterInstalled) return { disabled: true, status: 'Available to install', installCommand: agent.installCommand ?? undefined, loginCommand: agent.authStatus === 'signed-out' ? agent.loginCommand ?? undefined : undefined, authLabel };
    if (agent.authStatus === 'signed-out') return { disabled: true, status: 'Signed out', loginCommand: agent.loginCommand ?? undefined, authLabel };
    if (agent.authStatus === 'unknown') return { disabled: busy, status: 'Sign-in status unknown', authLabel };
    return { disabled: busy, status: 'Signed in', authLabel };
  };
  const selectAgent = (id: LocalAgentId) => {
    if (agentState(id).disabled || !onSelectAgent) return;
    void Promise.resolve(onSelectAgent(id)).catch(() => undefined);
    changeOpen(false);
  };
  // Models belong to the Astrid agent; with another agent chosen, search narrows the agents instead.
  const listedAgents = AGENT_IDS.filter(id => !searching || (!astridSelected && matches(tokens, agentNames[id])));
  const label = astridSelected ? current?.model.name ?? catalog.currentModel ?? 'Choose model' : agentNames[selectedAgent];
  const showError = selectionError !== null && selectionError !== dismissedError;

  const modelItem = (provider: Provider, model: Provider['models'][number]) => {
    const id = `${provider.id}/${model.id}`;
    const selected = catalog.currentModel === id;
    return (
      <CommandItem key={id} value={id} disabled={busy} aria-current={selected ? 'true' : undefined}
        className="gap-2" onSelect={() => { void Promise.resolve(onSelectModel(id)).catch(() => undefined); changeOpen(false); }}>
        <Check className={cn('h-3.5 w-3.5 shrink-0', selected ? 'opacity-100' : 'opacity-0')} aria-hidden="true" />
        <span className={cn('min-w-0 truncate normal-case', selected && 'text-foreground')}>{model.name}</span>
      </CommandItem>
    );
  };
  const providerGroup = (provider: Provider, models = provider.models) => (
    <CommandGroup key={provider.id} heading={<ProviderHeading provider={provider} />}>
      {provider.models.length === 0 && (
        <p className="px-2 pb-1.5 text-[11px] text-muted-foreground">No enabled models. Check <code className={KEYCAP}>omp models ls</code>.</p>
      )}
      {models.map(model => modelItem(provider, model))}
    </CommandGroup>
  );

  return (
    // In a crowded header the long model name gives way first; the chat chip keeps its label.
    <div className="flex min-w-0 max-w-40 shrink-[8]">
      <Popover open={open} onOpenChange={changeOpen}>
        <PopoverTrigger asChild>
          <button type="button" role="combobox" aria-label="Agent model" aria-expanded={open}
            title={!astridSelected ? `Agent: ${agentNames[selectedAgent]}` : current ? `Agent model: ${current.provider.name} · ${current.model.name}` : 'Choose the agent model'}
            className={cn('flex h-7 w-full min-w-0 items-center gap-1.5 rounded-md border bg-card/80 px-2 text-xs transition-colors hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring',
              showError ? 'border-destructive/50 text-destructive' : 'border-border/70 text-muted-foreground')}>
            <span className="min-w-0 truncate normal-case">{label}</span>
            <ChevronsUpDown className="ml-auto h-3.5 w-3.5 shrink-0 opacity-50" aria-hidden="true" />
          </button>
        </PopoverTrigger>
        <PopoverContent align="end" className="w-72 max-w-[calc(100vw-2rem)] p-0">
          <Command loop shouldFilter={false} defaultValue={astridSelected ? catalog.currentModel ?? undefined : `agent:${selectedAgent}`}>
            <CommandInput placeholder="Search models..." className="h-8" value={query} onValueChange={setQuery} />
            <CommandList className="max-h-80">
              {showAgents && (listedAgents.length > 0 || !searching) && (
                <>
                  <CommandGroup heading="Agent">
                    {agentsLoading && <p className="px-2 pb-1 text-[11px] text-muted-foreground">Checking agent availability…</p>}
                    {agentsError && <p role="alert" className="px-2 pb-1 text-[11px] text-destructive">Could not load agents: {agentsError}</p>}
                    {listedAgents.map(id => {
                      const state = agentState(id);
                      const selected = selectedAgent === id;
                      const unavailable = state.disabled || !onSelectAgent;
                      return (
                        <Fragment key={id}>
                          <CommandItem value={`agent:${id}`} disabled={unavailable} aria-current={selected ? 'true' : undefined}
                            className="items-start gap-2 data-[disabled=true]:opacity-100" onSelect={() => selectAgent(id)}>
                            <Check className={cn('mt-0.5 h-3.5 w-3.5 shrink-0', selected ? 'opacity-100' : 'opacity-0')} aria-hidden="true" />
                            <span className="flex min-w-0 flex-1 flex-col">
                              <span className="flex items-baseline gap-2">
                                <span className={cn('normal-case', unavailable ? 'text-muted-foreground' : selected && 'text-foreground')}>{agentNames[id]}</span>
                                <span className="ml-auto shrink-0 text-[10px] text-muted-foreground">{state.status}</span>
                              </span>
                              {id === 'astrid' && <span className="text-[11px] text-muted-foreground">OMP models</span>}
                              {id === 'claude-code' && <span className="text-[11px] text-muted-foreground">Your Claude login{state.authLabel && <> · {state.authLabel}</>}</span>}
                              {id === 'codex' && <span className="text-[11px] text-muted-foreground">Your ChatGPT login{state.authLabel && <> · {state.authLabel}</>}</span>}
                            </span>
                          </CommandItem>
                          {state.installCommand && (
                            <p className="pb-1 pl-[1.875rem] pr-2 text-[11px] text-muted-foreground">Install adapter <code className={cn(KEYCAP, 'select-all')}>{state.installCommand}</code></p>
                          )}
                          {state.loginCommand && (
                            <p className="pb-1 pl-[1.875rem] pr-2 text-[11px] text-muted-foreground">Sign in: run <code className={cn(KEYCAP, 'select-all')}>{state.loginCommand}</code></p>
                          )}
                        </Fragment>
                      );
                    })}
                    {astridSelected && !searching && <p className="px-2 pb-1 pt-1.5 text-[10px] text-muted-foreground/80">Agent selection affects new chats only. Saved chats keep their original agent.</p>}
                  </CommandGroup>
                  <CommandSeparator />
                </>
              )}
              {!astridSelected && showAgents && !searching && (
                <p className="px-3 py-2.5 text-[11px] text-muted-foreground">Uses your {agentNames[selectedAgent]} default model. New chats use this agent; saved chats keep their original agent.</p>
              )}
              {astridSelected && loading && (
                <div className="flex items-center gap-2 px-3 py-3 text-xs text-muted-foreground">
                  <Loader2 className="h-3.5 w-3.5 animate-spin" aria-hidden="true" />Loading models...
                </div>
              )}
              {astridSelected && catalogError && <p role="alert" className="px-3 py-3 text-xs text-destructive">Could not load models: {catalogError}</p>}
              {astridSelected && !loading && !catalogError && catalog.providers.length === 0 && <p className="px-3 py-3 text-xs text-muted-foreground">No models available.</p>}
              {catalog.providers.length > 0 && <CommandEmpty className="py-6 text-center text-xs text-muted-foreground">No models match.</CommandEmpty>}
              {astridSelected && busy && signedIn.length + keyless.length > 0 && <p className="px-3 pt-2 text-[11px] text-muted-foreground">You can switch once the agent is idle.</p>}
              {!astridSelected ? null : searching ? resultGroups.map(({ provider, models }) => providerGroup(provider, models)) : (
                <>
                  {signedIn.map(provider => providerGroup(provider))}
                  {!fold && keyless.map(provider => providerGroup(provider))}
                  {fold && (
                    <>
                      {signedIn.length > 0 && <CommandSeparator />}
                      <CommandGroup heading={<span className="flex items-center justify-between"><span>Other providers</span><span className="tabular-nums">{keyless.length}</span></span>}>
                        {keyless.map(provider => {
                          const unfoldedHere = openProviders.has(provider.id);
                          return (
                            <Fragment key={provider.id}>
                              <CommandItem value={`provider:${provider.id}`} aria-expanded={unfoldedHere} className="gap-2 text-xs text-muted-foreground" onSelect={() => toggleProvider(provider.id)}>
                                <ChevronRight className={cn('h-3.5 w-3.5 shrink-0 transition-transform duration-100', unfoldedHere && 'rotate-90')} aria-hidden="true" />
                                <span className="min-w-0 truncate normal-case">{provider.name}</span>
                                <span className="ml-auto pl-2 text-[10px] tabular-nums">{provider.models.length}</span>
                              </CommandItem>
                              {unfoldedHere && provider.models.slice(0, UNFOLD_LIMIT).map(model => modelItem(provider, model))}
                              {unfoldedHere && provider.models.length > UNFOLD_LIMIT && (
                                <p className="py-1 pl-[1.875rem] pr-2 text-[11px] text-muted-foreground">{provider.models.length - UNFOLD_LIMIT} more; search to find them.</p>
                              )}
                            </Fragment>
                          );
                        })}
                      </CommandGroup>
                    </>
                  )}
                </>
              )}
              {astridSelected && results.length > SEARCH_LIMIT && (
                <p className="px-3 py-2 text-[11px] text-muted-foreground">Showing {SEARCH_LIMIT} of {results.length} matches. Keep typing to narrow.</p>
              )}
              {astridSelected && signedOut.length > 0 && (!searching || listedSignedOut.length > 0) && (
                <>
                  {(searching ? results.length : signedIn.length + keyless.length) > 0 && <CommandSeparator />}
                  <CommandGroup heading={<span className="flex items-center justify-between"><span>Not signed in</span>{!searching && <span className="tabular-nums">{signedOut.length}</span>}</span>}>
                    {searching || showSignedOut ? listedSignedOut.map(provider => (
                      <CommandItem key={provider.id} value={`signed-out:${provider.id}`} disabled
                        className="pl-[1.875rem] text-xs text-muted-foreground data-[disabled=true]:opacity-100">
                        <span className="min-w-0 truncate normal-case">{provider.name}</span>
                      </CommandItem>
                    )) : (
                      <CommandItem value="signed-out:show" className="gap-2 text-xs text-muted-foreground" onSelect={() => setShowSignedOut(true)}>
                        <ChevronRight className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
                        <span className="normal-case">Show all</span>
                      </CommandItem>
                    )}
                  </CommandGroup>
                </>
              )}
            </CommandList>
            {astridSelected && signedOut.length > 0 && (
              <p className="border-t border-border px-3 py-2 text-[10px] text-muted-foreground/80">
                To sign in, run <code className={KEYCAP}>omp</code> then <code className={KEYCAP}>/login</code>.
              </p>
            )}
          </Command>
        </PopoverContent>
      </Popover>
      {showError && (
        // Hangs under the host header (its positioned ancestor) at full width, so it is never clipped beside the chip.
        <div role="alert" className="absolute inset-x-3 top-full z-20 mt-1.5 flex items-start gap-2 rounded-md border border-destructive/40 bg-popover px-2.5 py-2 text-[11px] leading-snug text-destructive shadow-md">
          <p className="min-w-0 flex-1 break-words">
            {selectionError}{' '}
            <button type="button" className="font-medium text-foreground underline underline-offset-2 hover:text-foreground/80" onClick={() => changeOpen(true)}>Switch model</button>
          </p>
          <button type="button" aria-label="Dismiss" className="-m-0.5 shrink-0 rounded p-0.5 text-muted-foreground hover:bg-accent hover:text-foreground" onClick={() => setDismissedError(selectionError)}>
            <X className="h-3 w-3" aria-hidden="true" />
          </button>
        </div>
      )}
    </div>
  );
}
