import { Fragment, useEffect, useRef, useState, type KeyboardEvent } from 'react';
import { Check, ChevronDown, ChevronLeft, ChevronRight, Copy, Loader2, Paperclip } from 'lucide-react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/shared/components/ui/command.tsx';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import { cn } from '@/shared/components/ui/contracts/cn';
import { defaultThoughtLevel, type AgentThoughtLevel, type LocalAgentChoice, type LocalAgentId } from '@/integrations/astrid/localAgents.ts';
import { AGENT_IDS, AgentIcon, agentAvailability, agentNames } from './agentIdentity.tsx';

const KEYCAP = 'verbatim-case select-all rounded border border-border px-1 font-mono text-[10px]';
const SEGMENT = 'flex h-7 items-center text-xs text-muted-foreground transition-colors hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50';
/** A submenu lists this many models; its search reaches the rest. */
const SUBMENU_LIMIT = 50;

export interface NewChatModelChoice { id: string; name: string; detail?: string | null; thoughtLevel?: AgentThoughtLevel | null }

/** One agent's models for the submenu, supplied by the host as it fetches them. */
export interface NewChatAgentModels {
  agent: LocalAgentId;
  models: NewChatModelChoice[];
  /** The model a plain click on the agent starts with. */
  defaultModel?: string | null;
  loading: boolean;
  /** Shown when there is no list to offer, such as before the agent's first chat. */
  note?: string | null;
}

interface AgentChatNewChatButtonProps {
  /** The agent the last chat started with; the main click reuses it. */
  defaultAgent: LocalAgentId;
  agents?: LocalAgentChoice[];
  /** Current model names when existing model-list plumbing has reported them. */
  agentModelNames?: Partial<Record<LocalAgentId, string | null>>;
  /** Hide model drill-in for agents that have no reported or queryable model list. */
  agentCanBrowse?: Partial<Record<LocalAgentId, boolean>>;
  agentsLoading?: boolean;
  agentsError?: string | null;
  disabled?: boolean;
  /** Start a chat: no agent reuses the last one; no model uses that agent's default. */
  onNewChat: (agent?: LocalAgentId, model?: string, thoughtLevel?: string) => void;
  onMenuOpenChange?: (open: boolean) => void;
  /** Tells the host which agent's models to fetch (null when the submenu closes). */
  onBrowseAgent?: (agent: LocalAgentId | null) => void;
  agentModels?: NewChatAgentModels | null;
  /** Bring a chat started elsewhere into this project. */
  attachExisting?: { open: boolean; toggle: () => void };
}

const matches = (query: string, text: string) => query.toLowerCase().split(/\s+/).filter(Boolean).every(token => text.toLowerCase().includes(token));

function AgentLine({ agent, line, copiedCommands, onCopy }: { agent: LocalAgentId; line: string; copiedCommands: Set<string>; onCopy: (command: string, index: number) => void }) {
  return <>{line.split(/`([^`]+)`/g).map((part, index) => {
    if (index % 2 === 0) return part;
    const commandIndex = (index - 1) / 2;
    const isCopied = copiedCommands.has(`${agent}:${commandIndex}`);
    const Icon = isCopied ? Check : Copy;
    return (
      <Fragment key={index}>
        <code className={KEYCAP}>{part}</code>
        <button type="button" tabIndex={0} aria-label="Copy command" title="Copy command"
          className="ml-1 inline-flex h-4 w-4 shrink-0 items-center justify-center rounded text-muted-foreground hover:bg-background/40 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          onPointerDown={(event) => { event.preventDefault(); event.stopPropagation(); }}
          onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') event.stopPropagation(); }}
          onClick={(event) => { event.preventDefault(); event.stopPropagation(); onCopy(part, commandIndex); }}>
          <Icon className="h-3.5 w-3.5" aria-hidden="true" />
        </button>
      </Fragment>
    );
  })}</>;
}

/** "New chat" with the last-used agent; its menu starts a chat with any agent, or drills into one to pick the model too. */
export function AgentChatNewChatButton({ defaultAgent, agents, agentModelNames, agentCanBrowse, agentsLoading = false, agentsError = null, disabled = false, onNewChat, onMenuOpenChange, onBrowseAgent, agentModels = null, attachExisting }: AgentChatNewChatButtonProps) {
  const [open, setOpen] = useState(false);
  const [browsing, setBrowsing] = useState<LocalAgentId | null>(null);
  const [levelModel, setLevelModel] = useState<NewChatModelChoice | null>(null);
  const [highlighted, setHighlighted] = useState(`agent:${defaultAgent}`);
  const [query, setQuery] = useState('');
  const [copiedCommands, setCopiedCommands] = useState<Set<string>>(() => new Set());
  const copyTimeouts = useRef(new Map<string, number>());
  const root = useRef<HTMLDivElement>(null);
  const landOnModel = useRef(false);
  const returnModel = useRef<string | null>(null);
  const browse = (agent: LocalAgentId | null) => {
    landOnModel.current = agent !== null;
    // Coming back lands on the agent that was open, so ← then → returns to the same place.
    setHighlighted(agent ? '' : `agent:${browsing ?? defaultAgent}`);
    setBrowsing(agent);
    setLevelModel(null);
    returnModel.current = null;
    setQuery('');
    onBrowseAgent?.(agent);
  };
  const changeOpen = (next: boolean) => {
    setOpen(next);
    if (next) setHighlighted(`agent:${defaultAgent}`);
    else if (browsing) browse(null);
    onMenuOpenChange?.(next);
  };
  const browseLevels = (model: NewChatModelChoice | null) => {
    returnModel.current = levelModel?.id ?? null;
    landOnModel.current = !model;
    setLevelModel(model);
    setQuery('');
  };
  const start = (agent?: LocalAgentId, model?: string, level?: string) => {
    changeOpen(false);
    if (level === undefined) onNewChat(agent, model);
    else onNewChat(agent, model, level);
  };
  const availability = (id: LocalAgentId) => agentAvailability(agents?.find(choice => choice.id === id));
  const copyLine = async (id: LocalAgentId, command: string, index: number) => {
    try {
      await navigator.clipboard.writeText(command);
    } catch {
      const input = document.createElement('textarea');
      input.value = command;
      input.style.position = 'fixed';
      input.style.opacity = '0';
      document.body.append(input);
      input.select();
      const copiedText = document.execCommand?.('copy') ?? false;
      input.remove();
      if (!copiedText) return;
    }
    const key = `${id}:${index}`;
    const existingTimeout = copyTimeouts.current.get(key);
    if (existingTimeout !== undefined) window.clearTimeout(existingTimeout);
    setCopiedCommands(current => new Set(current).add(key));
    copyTimeouts.current.set(key, window.setTimeout(() => {
      setCopiedCommands(current => {
        const next = new Set(current);
        next.delete(key);
        return next;
      });
      copyTimeouts.current.delete(key);
    }, 1_500));
  };

  // The agent and level lists are short and have no search field, so the list holds focus for the arrow
  // keys (the popover focuses it on open); the model list focuses its search.
  useEffect(() => {
    if (open && (!browsing || levelModel) && root.current && !root.current.contains(document.activeElement)) root.current.focus();
  }, [open, browsing, levelModel]);

  const onKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (!browsing && event.key === 'ArrowRight') {
      const agent = AGENT_IDS.find(id => `agent:${id}` === highlighted);
      if (agent && availability(agent).usable && agentCanBrowse?.[agent] !== false) { event.preventDefault(); browse(agent); }
    } else if (browsing && !levelModel && event.key === 'ArrowRight') {
      const model = agentModels?.models.find(model => `model:${model.id}` === highlighted);
      if (model?.thoughtLevel?.options.length) { event.preventDefault(); browseLevels(model); }
    } else if (browsing && event.key === 'ArrowLeft' && query === '') {
      event.preventDefault();
      if (levelModel) browseLevels(null);
      else browse(null);
    }
  };

  const submenu = browsing && agentModels?.agent === browsing ? agentModels : null;
  useEffect(() => {
    if (browsing !== 'hermes' || !submenu || submenu.loading || submenu.models.length > 0) return;
    // Hermes may not publish a model catalog. Return to the agent list once an
    // empty result is known, so the menu never leaves an empty model picker open.
    setBrowsing(null);
    setQuery('');
    setHighlighted('agent:hermes');
    onBrowseAgent?.(null);
  }, [browsing, onBrowseAgent, submenu]);
  // A submenu opens on the agent's default model (or its first), not on the back row.
  useEffect(() => {
    if (levelModel || !landOnModel.current || !submenu || submenu.models.length === 0) return;
    const target = submenu.models.find(model => model.id === (returnModel.current ?? submenu.defaultModel)) ?? submenu.models[0];
    // After cmdk settles its own first-item pick for the freshly mounted list.
    const frame = requestAnimationFrame(() => { landOnModel.current = false; setHighlighted(`model:${target.id}`); });
    return () => cancelAnimationFrame(frame);
  }, [levelModel, submenu]);
  useEffect(() => {
    if (!levelModel?.thoughtLevel) return;
    const value = defaultThoughtLevel(levelModel.thoughtLevel);
    const frame = requestAnimationFrame(() => setHighlighted(`level:${value}`));
    return () => cancelAnimationFrame(frame);
  }, [levelModel]);
  const shownModels = (submenu?.models ?? []).filter(model => !query || matches(query, `${model.name} ${model.detail ?? ''} ${model.id}`));

  return (
    <div className="flex shrink-0 items-center rounded-md">
      <button type="button" disabled={disabled} aria-label="New chat" title={`New chat with ${agentNames[defaultAgent]}`}
        className={cn(SEGMENT, 'gap-1.5 rounded-l-md pl-2 pr-1')} onClick={() => availability(defaultAgent).usable ? onNewChat() : changeOpen(true)}>
        {/* Narrow panels keep the label short and leave the agent to the tooltip. */}
        <AgentIcon agent={defaultAgent} className="hidden h-3.5 w-3.5 shrink-0 @[24rem]/agent-header:block" />
        <span className="normal-case">New<span className="hidden @[24rem]/agent-header:inline"> chat</span></span>
      </button>
      <Popover open={open} onOpenChange={changeOpen}>
        <PopoverTrigger asChild>
          <button type="button" disabled={disabled} aria-label="New chat with…" aria-expanded={open} className={cn(SEGMENT, 'w-5 justify-center rounded-r-md')}>
            <ChevronDown className="h-3.5 w-3.5" aria-hidden="true" />
          </button>
        </PopoverTrigger>
        <PopoverContent align="end" className="w-72 max-w-[calc(100vw-2rem)] p-0" initialFocus={root}>
          <Command ref={root} loop shouldFilter={false} value={highlighted} onValueChange={setHighlighted} onKeyDown={onKeyDown} className="outline-none">
            {browsing && !levelModel && (
              <CommandInput autoFocus placeholder={`Search ${agentNames[browsing]} models...`} className="h-8" value={query} onValueChange={setQuery} />
            )}
            <CommandList className="max-h-96">
              {!browsing ? (
                <CommandGroup heading="New chat with">
                  {agentsLoading && <p className="px-2 pb-1 text-[11px] text-muted-foreground">Checking agent availability…</p>}
                  {agentsError && <p role="alert" className="px-2 pb-1 text-[11px] text-destructive">Could not load agents: {agentsError}</p>}
                  {AGENT_IDS.map(id => {
                    const state = availability(id);
                    const last = id === defaultAgent;
                    return (
                      <Fragment key={id}>
                        <CommandItem value={`agent:${id}`} aria-current={last ? 'true' : undefined}
                          className="items-start gap-2 pr-1" onSelect={() => { if (state.usable) start(id); }}>
                          <AgentIcon agent={id} className={cn('mt-[3px] h-3.5 w-3.5 shrink-0', state.usable ? 'text-foreground/80' : 'text-muted-foreground/60')} />
                          <span className="flex min-w-0 flex-1 flex-col">
                            <span className="flex items-baseline gap-2">
                              <span className="normal-case">{agentNames[id]}</span>
                              {last && <Check className="h-3 w-3 shrink-0 self-center text-muted-foreground" aria-label="Last used" />}
                              <span aria-label={state.usable && agentModelNames?.[id] ? `Ready, using ${agentModelNames[id]}` : undefined} className="ml-auto shrink-0 text-[10px] text-muted-foreground normal-case">
                                {state.usable ? agentModelNames?.[id] ?? 'Ready' : state.state === 'sign-in' ? 'Sign in' : 'Not installed'}
                              </span>
                            </span>
                            {state.line && <span className="text-[11px] text-muted-foreground normal-case"><AgentLine agent={id} line={state.line} copiedCommands={copiedCommands} onCopy={(command, index) => void copyLine(id, command, index)} /></span>}
                          </span>
                          {state.usable && agentCanBrowse?.[id] !== false && (
                            <button type="button" tabIndex={-1} aria-label={`Choose a ${agentNames[id]} model`} title="Choose a model (→)"
                              className="-my-0.5 shrink-0 self-center rounded p-1 text-muted-foreground hover:bg-background/40 hover:text-foreground"
                              onPointerDown={(event) => event.preventDefault()}
                              onClick={(event) => { event.preventDefault(); event.stopPropagation(); browse(id); }}>
                              <ChevronRight className="h-3.5 w-3.5" aria-hidden="true" />
                            </button>
                          )}
                        </CommandItem>
                      </Fragment>
                    );
                  })}
                </CommandGroup>
              ) : levelModel?.thoughtLevel ? (
                <>
                  <CommandGroup>
                    <CommandItem value="back" className="gap-2 text-xs text-muted-foreground" onSelect={() => browseLevels(null)}>
                      <ChevronLeft className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
                      <AgentIcon agent={browsing} className="h-3.5 w-3.5 shrink-0" />
                      <span className="truncate normal-case">{levelModel.name}</span>
                    </CommandItem>
                  </CommandGroup>
                  <CommandSeparator />
                  <CommandGroup heading="Thinking level">
                    {levelModel.thoughtLevel.options.map(level => {
                      const preselected = level.value === defaultThoughtLevel(levelModel.thoughtLevel!);
                      return (
                        <CommandItem key={level.value} value={`level:${level.value}`} aria-current={preselected ? 'true' : undefined} className="items-start gap-2"
                          onSelect={() => start(browsing, levelModel.id, level.value)}>
                          <Check className={cn('mt-[3px] h-3.5 w-3.5 shrink-0', preselected ? 'opacity-100' : 'opacity-0')} aria-hidden="true" />
                          <span className="flex min-w-0 flex-1 flex-col">
                            <span className="flex items-baseline gap-2">
                              <span className="normal-case">{level.name}</span>
                              {level.value === levelModel.thoughtLevel?.recommendedValue && <span className="ml-auto shrink-0 text-[10px] text-muted-foreground normal-case">Recommended</span>}
                            </span>
                            {level.description && <span className="text-[11px] leading-snug text-muted-foreground normal-case">{level.description}</span>}
                          </span>
                        </CommandItem>
                      );
                    })}
                  </CommandGroup>
                </>
              ) : (
                <>
                  <CommandGroup>
                    <CommandItem value="back" className="gap-2 text-xs text-muted-foreground" onSelect={() => browse(null)}>
                      <ChevronLeft className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
                      <AgentIcon agent={browsing} className="h-3.5 w-3.5 shrink-0" />
                      <span className="normal-case">{agentNames[browsing]}</span>
                    </CommandItem>
                  </CommandGroup>
                  <CommandSeparator />
                  <CommandGroup heading="Start the chat with">
                    {(!submenu || submenu.loading) && shownModels.length === 0 && (
                      <div className="flex items-center gap-2 px-2 py-1.5 text-xs text-muted-foreground"><Loader2 className="h-3.5 w-3.5 animate-spin" aria-hidden="true" />Loading models...</div>
                    )}
                    {shownModels.slice(0, SUBMENU_LIMIT).map(model => {
                      const isDefault = model.id === submenu?.defaultModel;
                      const level = model.thoughtLevel ? defaultThoughtLevel(model.thoughtLevel) : undefined;
                      // The level a plain Enter starts with, shown like the agent row's model; a bare "Default" says nothing.
                      const levelName = level === 'default' ? null : model.thoughtLevel?.options.find(option => option.value === level)?.name;
                      return (
                        <CommandItem key={model.id} value={`model:${model.id}`} aria-current={isDefault ? 'true' : undefined} className="items-start gap-2" onSelect={() => start(browsing, model.id, level)}>
                          <Check className={cn('mt-[3px] h-3.5 w-3.5 shrink-0', isDefault ? 'opacity-100' : 'opacity-0')} aria-hidden="true" />
                          <span className="flex min-w-0 flex-1 flex-col">
                            <span className="flex items-baseline gap-2">
                              <span className="truncate normal-case">{model.name}</span>
                              {levelName && <span className="ml-auto shrink-0 text-[10px] text-muted-foreground normal-case">{levelName}</span>}
                            </span>
                            {model.detail && <span className="truncate text-[11px] text-muted-foreground normal-case">{model.detail}</span>}
                          </span>
                          {Boolean(model.thoughtLevel?.options.length) && (
                            <button type="button" tabIndex={-1} aria-label={`Choose a thinking level for ${model.name}`} title="Choose a thinking level (→)"
                              className="-my-0.5 shrink-0 self-center rounded p-1 text-muted-foreground hover:bg-background/40 hover:text-foreground"
                              onPointerDown={event => event.preventDefault()}
                              onClick={event => { event.preventDefault(); event.stopPropagation(); browseLevels(model); }}>
                              <ChevronRight className="h-3.5 w-3.5" aria-hidden="true" />
                            </button>
                          )}
                        </CommandItem>
                      );
                    })}
                    {shownModels.length > SUBMENU_LIMIT && (
                      <p className="px-2 py-1.5 text-[11px] text-muted-foreground">Showing {SUBMENU_LIMIT} of {shownModels.length}. Keep typing to narrow.</p>
                    )}
                    {submenu && !submenu.loading && submenu.models.length === 0 && (
                      <p className="px-2 py-1.5 text-[11px] text-muted-foreground">{submenu.note ?? `${agentNames[browsing]} reports its models once a chat starts.`}</p>
                    )}
                    {browsing === 'astrid' && (
                      <p className="px-2 py-1.5 text-[11px] text-muted-foreground">More models: run <code className={KEYCAP}>omp</code>, then <code className={KEYCAP}>/login</code>.</p>
                    )}
                  </CommandGroup>
                  {submenu && submenu.models.length > 0 && <CommandEmpty className="py-4 text-center text-xs text-muted-foreground">No models match.</CommandEmpty>}
                </>
              )}
              {!browsing && attachExisting && (
                <>
                  <CommandSeparator />
                  <CommandGroup>
                    <CommandItem value="attach-existing" className="gap-2 text-xs text-muted-foreground" onSelect={() => { changeOpen(false); attachExisting.toggle(); }}>
                      <Paperclip className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
                      <span className="normal-case">{attachExisting.open ? 'Hide existing chats' : 'Attach an existing chat…'}</span>
                    </CommandItem>
                  </CommandGroup>
                </>
              )}
            </CommandList>
            <p className="border-t border-border px-3 py-2 text-[10px] text-muted-foreground/80">
              {levelModel ? 'A chat keeps its model and thinking level.'
                : browsing ? `A chat keeps its model.${submenu?.models.some(model => model.thoughtLevel?.options.length) ? ' Press → to pick its thinking level.' : ''}`
                : 'A chat keeps its agent. Press → to pick its model.'}
            </p>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
