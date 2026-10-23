import { forwardRef, Fragment, useCallback, useEffect, useImperativeHandle, useRef, useState, type KeyboardEvent } from 'react';
import { Check, ChevronDown, ChevronRight, Copy, Plus } from 'lucide-react';
import { Command, CommandGroup, CommandItem, CommandList } from '@/shared/components/ui/command.tsx';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import { cn } from '@/shared/components/ui/contracts/cn';
import type { LocalAgentChoice, LocalAgentId } from '@/integrations/astrid/localAgents.ts';
import { PICKER_GROUP, PICKER_PANEL, PickerSearch, ROW_BUTTON, matches } from '@/shared/components/ui/picker-menu.tsx';
import { ChatUpdateNeeded, isChatUpdateError } from './ChatUpdateNeeded.tsx';
import { AGENT_IDS, AgentIcon, agentAvailability, agentNames } from './agentIdentity.tsx';
import { readModelThoughtSelections, readNewChatChoice, rememberModelThoughtSelection, rememberNewChatChoice, type NewChatChoice } from './newChatThinkingSelection.ts';
import { NewChatModels, type NewChatAgentModels } from './NewChatModels.tsx';

export type { NewChatAgentModels, NewChatModelChoice } from './NewChatModels.tsx';

const KEYCAP = 'select-all rounded border border-border px-1 font-mono text-[10px]';
const SPLIT_BUTTON = 'inline-flex h-6 items-center justify-center text-muted-foreground transition-colors hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-60 [@media(pointer:coarse)]:h-8';

export interface NewChatMenuHandle {
  /** Opens the chooser on one agent's models: a chat keeps its model, so a different model is chosen for the next chat. */
  openModels: (agent: LocalAgentId) => void;
}

/** What the + button starts: the open chat's agent, model and thinking level. */
export interface NewChatLike { agent: LocalAgentId; model?: string; modelName?: string | null; thoughtLevel?: string }

interface NewChatMenuProps {
  /** The open chat, which + repeats unless a choice was made in the menu; without one, + starts the default agent with its default model. */
  current?: NewChatLike | null;
  defaultAgent: LocalAgentId;
  agents?: LocalAgentChoice[];
  /** Each agent's default model, which a choice of its row uses. */
  agentModelNames?: Partial<Record<LocalAgentId, string | null>>;
  /** Hide model drill-in for agents that have no reported or queryable model list. */
  agentCanBrowse?: Partial<Record<LocalAgentId, boolean>>;
  agentsLoading?: boolean;
  agentsError?: Error | null;
  /** No new chat can start, such as before a project opens or while one starts. */
  disabled?: boolean;
  /** A new chat is being created; the buttons wait for it. */
  newChatDisabled?: boolean;
  /** Start a chat: no model uses that agent's default. */
  onNewChat: (agent?: LocalAgentId, model?: string, thoughtLevel?: string) => void;
  /** Tells the host which agent's service catalog to show (null when the model list closes). */
  onBrowseAgent?: (agent: LocalAgentId | null) => void;
  agentModels?: NewChatAgentModels | null;
  onOpenChange?: (open: boolean) => void;
}

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

/**
 * The chat header's new-chat split button, like a split Merge button: + starts a chat, and ▾ opens a chooser for what + starts
 * (an agent, → drills into that agent's models and thinking levels). The chooser never starts a chat itself.
 */
export const NewChatMenu = forwardRef<NewChatMenuHandle, NewChatMenuProps>(function NewChatMenu({
  current = null, defaultAgent, agents, agentModelNames, agentCanBrowse, agentsLoading = false, agentsError = null,
  disabled = false, newChatDisabled = false, onNewChat, onBrowseAgent, agentModels = null, onOpenChange,
}, ref) {
  const [open, setOpen] = useState(false);
  const [browsing, setBrowsing] = useState<LocalAgentId | null>(null);
  const [openLevelSelector, setOpenLevelSelector] = useState<string | null>(null);
  const [levelSelections, setLevelSelections] = useState(() => Object.fromEntries(
    AGENT_IDS.map(agent => [agent, readModelThoughtSelections(agent)]),
  ) as Record<LocalAgentId, Record<string, string>>);
  const [highlighted, setHighlighted] = useState('');
  const [query, setQuery] = useState('');
  const [copiedCommands, setCopiedCommands] = useState<Set<string>>(() => new Set());
  const copyTimeouts = useRef(new Map<string, number>());
  const root = useRef<HTMLDivElement>(null);
  const search = useRef<HTMLInputElement>(null);
  const landOnModel = useRef(false);
  const landOnAgent = useRef<string | null>(null);
  const wasBrowsing = useRef(false);
  // The agent row itself opened the model list, so an empty catalog falls back to choosing that agent.
  const startedFromRow = useRef(false);

  const [stored, setStored] = useState<NewChatChoice | null>(readNewChatChoice);
  // A stored choice whose agent is no longer usable falls back to the open chat, or the default agent.
  const choice = stored && (!agents || agentAvailability(agents.find(item => item.id === stored.agent)).usable) ? stored : null;
  const effective: NewChatLike = choice ?? current ?? { agent: defaultAgent };
  const homeValue = `agent:${effective.agent}`;
  const availability = (id: LocalAgentId) => agentAvailability(agents?.find(choice => choice.id === id));
  const canBrowse = (id: LocalAgentId) => Boolean(agents?.some(choice => choice.id === id)) && availability(id).usable && agentCanBrowse?.[id] !== false;
  const astridSignInLine = agents?.find(choice => choice.id === 'astrid')?.signInLine;
  const updateNeeded = agentsError && isChatUpdateError(agentsError) ? agentsError : null;
  const quickAgent = effective.agent;
  const quickModel = choice ? choice.modelName ?? agentModelNames?.[choice.agent] : current ? current.modelName : agentModelNames?.[defaultAgent];
  const quickLabel = `New chat · ${[agentNames[quickAgent], quickModel].filter(Boolean).join(' · ')}`;

  const browse = (agent: LocalAgentId | null) => {
    landOnModel.current = agent !== null;
    if (agent === null) startedFromRow.current = false;
    // Coming back lands on the agent that was open, so ← then → returns to the same place.
    landOnAgent.current = agent ? null : `agent:${browsing ?? defaultAgent}`;
    setHighlighted(agent ? '' : `agent:${browsing ?? defaultAgent}`);
    setBrowsing(agent);
    setOpenLevelSelector(null);
    setQuery('');
    onBrowseAgent?.(agent);
  };
  const changeOpen = (next: boolean) => {
    setOpen(next);
    if (next) { setHighlighted(homeValue); setQuery(''); }
    else if (browsing) browse(null);
    onOpenChange?.(next);
  };
  useImperativeHandle(ref, () => ({
    openModels: (agent: LocalAgentId) => {
      if (!open) { setOpen(true); onOpenChange?.(true); }
      browse(agent);
    },
  }));
  const choose = (agent: LocalAgentId, model?: string, level?: string, modelName?: string | null) => {
    const next: NewChatChoice = { agent, ...(model ? { model } : {}), ...(modelName ? { modelName } : {}), ...(level !== undefined ? { thoughtLevel: level } : {}) };
    setStored(next);
    rememberNewChatChoice(next);
    changeOpen(false);
  };
  const startQuick = () => {
    const source = choice ?? current;
    if (source?.thoughtLevel === undefined) onNewChat(source?.agent, source?.model);
    else onNewChat(source.agent, source.model, source.thoughtLevel);
  };
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
    setCopiedCommands(currentCopied => new Set(currentCopied).add(key));
    copyTimeouts.current.set(key, window.setTimeout(() => {
      setCopiedCommands(currentCopied => {
        const next = new Set(currentCopied);
        next.delete(key);
        return next;
      });
      copyTimeouts.current.delete(key);
    }, 1_500));
  };

  // Back from a model list: keep focus in the menu, and land on the agent once cmdk has re-filtered and picked its first row.
  useEffect(() => {
    if (open && !browsing && wasBrowsing.current && root.current && !root.current.contains(document.activeElement)) root.current.focus();
    wasBrowsing.current = browsing !== null;
    const target = landOnAgent.current;
    if (browsing || !target) return;
    const frame = requestAnimationFrame(() => { landOnAgent.current = null; setHighlighted(target); });
    return () => cancelAnimationFrame(frame);
  }, [open, browsing]);

  const onKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (!browsing && event.key === 'ArrowRight') {
      const agent = AGENT_IDS.find(id => `agent:${id}` === highlighted);
      if (agent && canBrowse(agent)) { event.preventDefault(); browse(agent); }
    } else if (browsing && (event.key === 'ArrowRight' || (event.key === ' ' && (event.target === root.current || query === '')))) {
      const model = agentModels?.models.find(model => `model:${model.id}` === highlighted);
      if (model?.thoughtLevel?.options.length) { event.preventDefault(); setOpenLevelSelector(model.id); }
    } else if (browsing && event.key === 'ArrowLeft' && query === '') {
      event.preventDefault();
      browse(null);
    }
  };

  const submenu = browsing && agentModels?.agent === browsing ? agentModels : null;
  useEffect(() => {
    if (browsing !== 'hermes' || !submenu || submenu.loading || submenu.models.length > 0) return;
    // Hermes may not publish a model catalog. Return to the agent list once an
    // empty result is known, so the menu never leaves an empty model picker open.
    if (startedFromRow.current) { startedFromRow.current = false; choose('hermes'); return; }
    setBrowsing(null);
    setQuery('');
    setHighlighted('agent:hermes');
    onBrowseAgent?.(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [browsing, onBrowseAgent, submenu]);
  // Highlights a model and brings it into view: cmdk scrolls only for its own key moves, not for a value set here.
  const revealHighlight = useRef(false);
  const highlightModel = useCallback((id: string) => { revealHighlight.current = true; setHighlighted(`model:${id}`); }, []);
  useEffect(() => {
    if (!revealHighlight.current) return;
    // A frame on, once cmdk has marked the row.
    const frame = requestAnimationFrame(() => {
      revealHighlight.current = false;
      root.current?.querySelector('[cmdk-item][data-selected="true"]')?.scrollIntoView({ block: 'nearest' });
    });
    return () => cancelAnimationFrame(frame);
  }, [highlighted]);
  // A model list opens on the agent's default model (or its first), not on the back row.
  useEffect(() => {
    if (!landOnModel.current || !submenu || submenu.models.length === 0) return;
    const target = submenu.models.find(model => model.id === submenu.defaultModel) ?? submenu.models[0];
    // After cmdk settles its own first-item pick for the freshly mounted list.
    const frame = requestAnimationFrame(() => { landOnModel.current = false; highlightModel(target.id); });
    return () => cancelAnimationFrame(frame);
  }, [submenu, highlightModel]);
  const shownModels = (submenu?.models ?? []).filter(model => !query || matches(query, `${model.name} ${model.detail ?? ''} ${model.id}`));
  // A search lands on its first match, so Enter picks it rather than going back (cmdk picks the back row, the first item).
  const firstMatch = query ? shownModels[0]?.id : undefined;
  useEffect(() => {
    if (!firstMatch) return;
    const frame = requestAnimationFrame(() => highlightModel(firstMatch));
    return () => cancelAnimationFrame(frame);
  }, [query, firstMatch, highlightModel]);

  const agentRows = agents?.map(choice => {
    const id = choice.id;
    const state = availability(id);
    const model = state.usable ? agentModelNames?.[id] : null;
    return (
      <CommandItem key={id} value={`agent:${id}`} disabled={newChatDisabled}
        className="items-start gap-2 pr-1 [@media(pointer:coarse)]:min-h-[44px]" onSelect={() => { if (canBrowse(id)) { startedFromRow.current = true; browse(id); } else if (state.usable) choose(id); }}>
        <Check className={cn('mt-[3px] h-3.5 w-3.5 shrink-0', effective.agent === id ? 'opacity-100' : 'opacity-0')} aria-hidden="true" />
        <AgentIcon agent={id} className={cn('mt-[3px] h-3.5 w-3.5 shrink-0', state.usable ? 'text-foreground/80' : 'text-muted-foreground/60')} />
        <span className="flex min-w-0 flex-1 flex-col">
          <span className="flex items-baseline gap-2">
            <span>{agentNames[id]}</span>
            <span aria-label={model ? `Ready, using ${model}` : undefined} className="ml-auto shrink-0 text-[10px] text-muted-foreground">
              {state.usable ? model ?? 'Ready' : state.state === 'sign-in' ? 'Sign in' : 'Not installed'}
            </span>
          </span>
          {state.line && <span className="text-[11px] text-muted-foreground"><AgentLine agent={id} line={state.line} copiedCommands={copiedCommands} onCopy={(command, index) => void copyLine(id, command, index)} /></span>}
        </span>
        {canBrowse(id) && (
          <button type="button" tabIndex={-1} aria-label={`Choose a ${agentNames[id]} model`} title="Choose a model (→)"
            className={cn(ROW_BUTTON, '-my-0.5 self-center')}
            onPointerDown={(event) => event.preventDefault()}
            onClick={(event) => { event.preventDefault(); event.stopPropagation(); browse(id); }}>
            <ChevronRight className="h-3.5 w-3.5" aria-hidden="true" />
          </button>
        )}
      </CommandItem>
    );
  });

  return (
    <Popover open={open} onOpenChange={changeOpen}>
      <div role="group" aria-label="New chat" className="flex shrink-0 items-center rounded-md transition-colors hover:has-[:enabled]:bg-accent/50 has-[[aria-expanded=true]]:bg-accent/50">
        <button type="button" disabled={disabled || newChatDisabled} aria-label={quickLabel} title={quickLabel}
          className={cn(SPLIT_BUTTON, 'w-6 rounded-l-md [@media(pointer:coarse)]:w-8')}
          onClick={startQuick}>
          <Plus className="h-3.5 w-3.5" aria-hidden="true" />
        </button>
        <PopoverTrigger asChild>
          <button type="button" disabled={disabled} aria-label="Choose the agent and model for new chats" title="Choose the agent and model for new chats"
            className={cn(SPLIT_BUTTON, 'gap-0.5 rounded-r-md px-1 aria-expanded:bg-accent aria-expanded:text-foreground')}>
            <AgentIcon agent={effective.agent} className="h-3 w-3 shrink-0" />
            <ChevronDown className="h-3.5 w-3.5" aria-hidden="true" />
          </button>
        </PopoverTrigger>
      </div>
      <PopoverContent align="end" aria-label="New chat" className={PICKER_PANEL}
        initialFocus={(type) => (type === 'touch' ? null : search.current) ?? root.current}>
        <Command ref={root} loop value={highlighted} onValueChange={setHighlighted} onKeyDown={onKeyDown} className="outline-none" shouldFilter={false}>
          {/* An out-of-date Astrid is the one thing to act on, so its update stays at the top, outside the scrolling list. */}
          {!browsing && updateNeeded && (
            <div role="alert" className="border-b border-border px-3 py-2 text-xs"><ChatUpdateNeeded detail={updateNeeded.message} /></div>
          )}
          {browsing && <PickerSearch ref={search} autoFocus placeholder={`Search ${agentNames[browsing]} models…`} value={query} onValueChange={setQuery} />}
          <CommandList className={updateNeeded && !browsing ? 'max-h-48' : 'max-h-96'}>
            {browsing ? (
              <NewChatModels agent={browsing} submenu={submenu} models={shownModels} levelSelections={levelSelections[browsing]} openLevelSelector={openLevelSelector}
                returnFocus={search} onBack={() => browse(null)} selectedModel={effective.agent === browsing ? effective.model : undefined}
                onStartNow={(model, level, name) => { choose(browsing, model, level, name); if (level === undefined) onNewChat(browsing, model); else onNewChat(browsing, model, level); }}
                onPick={(model, level) => choose(browsing, model, level, submenu?.models.find(item => item.id === model)?.name)}
                onLevelSelectorOpenChange={(modelId, next) => {
                  setOpenLevelSelector(next ? modelId : null);
                  setHighlighted(`model:${modelId}`);
                }}
                onRememberLevel={(modelId, value) => {
                  rememberModelThoughtSelection(browsing, modelId, value);
                  setLevelSelections(selections => ({ ...selections, [browsing]: { ...selections[browsing], [modelId]: value } }));
                }}
                footer={browsing === 'astrid' && astridSignInLine && (
                  <p className="px-2 py-1.5 text-[11px] text-muted-foreground">More models: <AgentLine agent="astrid" line={astridSignInLine} copiedCommands={copiedCommands} onCopy={(command, index) => void copyLine('astrid', command, index)} /></p>
                )} />
            ) : (
              <CommandGroup heading="Use for new chats" className={PICKER_GROUP}>
                {agentsLoading && <p className="px-2 pb-1 text-[11px] text-muted-foreground">Checking agent availability…</p>}
                {agentsError && !updateNeeded && <p role="alert" className="px-2 pb-1 text-[11px] text-destructive">Could not load agents: {agentsError.message}</p>}
                {agentRows}
              </CommandGroup>
            )}
          </CommandList>
          <p className="border-t border-border px-3 py-2 text-[10px] text-muted-foreground/80">
            {browsing ? 'A chat keeps its model. + starts the chat.' : 'A chat keeps its agent. Press → to pick its model. + starts the chat.'}
          </p>
        </Command>
      </PopoverContent>
    </Popover>
  );
});
