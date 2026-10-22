import { useRef, useState } from 'react';
import { Check, ChevronDown, Paperclip, Pencil, Star } from 'lucide-react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/shared/components/ui/command.tsx';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import { cn } from '@/shared/components/ui/contracts/cn';
import type { LocalAgentId } from '@/integrations/astrid/localAgents.ts';
import { AgentIcon, agentNames } from './agentIdentity.tsx';
import { RenameChatDialog } from './RenameChatDialog.tsx';

export const ROW_BUTTON = 'inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-sm text-muted-foreground hover:bg-foreground/5 hover:text-foreground [@media(pointer:coarse)]:h-8 [@media(pointer:coarse)]:w-8';

export const matches = (query: string, text: string) => query.toLowerCase().split(/\s+/).filter(Boolean).every(token => text.toLowerCase().includes(token));
const chatLabel = (session: AgentChatMenuSession, index: number) => session.title?.trim() || `Chat ${session.chatNumber ?? index + 1}`;

export interface AgentChatMenuSession { id: string; title?: string; chatNumber?: number }

interface AgentChatMenuProps {
  sessions: AgentChatMenuSession[];
  activeSessionId: string | null;
  mainSessionId?: string | null;
  settingMainSessionId?: string | null;
  /** Each chat's agent and the model it last used, shown under its title. */
  describeSession?: (sessionId: string) => { agent: LocalAgentId; model?: string | null };
  onSelectSession: (sessionId: string) => void;
  onSetMainSession?: (sessionId: string) => void;
  onRenameSession?: (sessionId: string, title: string) => Promise<unknown>;
  /** A new chat is starting; the trigger names it until it opens. */
  starting?: boolean;
  disabled?: boolean;
  /** Bring a chat started elsewhere into this project. */
  attachExisting?: { open: boolean; toggle: () => void };
  onOpenChange?: (open: boolean) => void;
}

/** The chat header's chats menu: its trigger names the open chat, and it switches chats, renames, makes a chat Main and attaches existing chats. Starting chats is the new-chat button's job. */
export function AgentChatMenu({
  sessions, activeSessionId, mainSessionId = null, settingMainSessionId = null, describeSession, onSelectSession, onSetMainSession, onRenameSession,
  starting = false, disabled = false, attachExisting, onOpenChange,
}: AgentChatMenuProps) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [highlighted, setHighlighted] = useState('');
  const [renaming, setRenaming] = useState<{ id: string; label: string } | null>(null);
  const root = useRef<HTMLDivElement>(null);
  const search = useRef<HTMLInputElement>(null);

  const activeIndex = sessions.findIndex(session => session.id === activeSessionId);
  const activeSession = activeIndex >= 0 ? sessions[activeIndex] : null;
  // While the chat list reloads, the open chat keeps the name it was last shown with.
  const shownChat = useRef<{ id: string; label: string; titled: boolean } | null>(null);
  if (activeSession) shownChat.current = { id: activeSession.id, label: chatLabel(activeSession, activeIndex), titled: Boolean(activeSession.title?.trim()) };
  const openChat = activeSessionId && shownChat.current?.id === activeSessionId ? shownChat.current : null;
  const triggerLabel = !starting && openChat ? openChat.label : 'New chat';

  const changeOpen = (next: boolean) => {
    setOpen(next);
    if (next) { setHighlighted(activeSession ? `session:${activeSession.id}` : ''); setQuery(''); }
    onOpenChange?.(next);
  };

  const chatRows = sessions.map((session, index) => {
    const label = chatLabel(session, index);
    const fallbackLabel = `Chat ${session.chatNumber ?? index + 1}`;
    const selected = session.id === activeSessionId;
    const isMain = session.id === mainSessionId;
    const meta = describeSession?.(session.id);
    const metaLabel = meta ? `${agentNames[meta.agent]}${meta.model ? ` · ${meta.model}` : ''}` : null;
    return (
      <CommandItem key={session.id} value={`session:${session.id}`} keywords={[label, fallbackLabel, ...(isMain ? ['Main'] : []), ...(metaLabel ? [metaLabel] : [])]}
        aria-current={selected ? 'true' : undefined} className="group gap-2 [@media(pointer:coarse)]:min-h-[44px]"
        onSelect={() => { onSelectSession(session.id); changeOpen(false); }}>
        <Check className={cn('h-3.5 w-3.5 shrink-0', selected ? 'opacity-100' : 'opacity-0')} aria-hidden="true" />
        <span className="flex min-w-0 flex-1 flex-col">
          <span title={label} className={'min-w-0 truncate'}>{label}</span>
          {meta && (
            <span className="flex min-w-0 items-center gap-1 text-[11px] leading-4 text-muted-foreground" title={metaLabel ?? undefined}>
              <AgentIcon agent={meta.agent} className="h-3 w-3 shrink-0" />
              <span className="truncate">{metaLabel}</span>
            </span>
          )}
        </span>
        {(isMain || onSetMainSession || (onRenameSession && selected)) && (
          <span className="ml-auto flex shrink-0 items-center gap-0.5">
            {isMain ? (
              <span title="Main chat" className="inline-flex h-6 w-6 items-center justify-center text-muted-foreground">
                <Star className="h-3 w-3 fill-current" aria-hidden="true" />
                <span className="sr-only">Main</span>
              </span>
            ) : onSetMainSession && (
              <button type="button" aria-label={`Make ${label} main`} title={`Make ${label} main`} disabled={settingMainSessionId !== null}
                className={cn(ROW_BUTTON, settingMainSessionId !== null ? 'opacity-100' : 'opacity-0 focus-visible:opacity-100 group-hover:opacity-100 [@media(hover:none)]:opacity-100')}
                onClick={(event) => { event.preventDefault(); event.stopPropagation(); onSetMainSession(session.id); }}>
                <Star className={cn('h-3.5 w-3.5', session.id === settingMainSessionId && 'animate-pulse fill-current')} aria-hidden="true" />
              </button>
            )}
            {onRenameSession && selected && (
              <button type="button" aria-label={`Rename ${label}`} title={`Rename ${label}`}
                className={cn(ROW_BUTTON, 'opacity-0 transition-opacity focus-visible:opacity-100 group-hover:opacity-100 group-data-[selected=true]:opacity-100 [@media(hover:none)]:opacity-100')}
                onClick={(event) => {
                  event.preventDefault();
                  event.stopPropagation();
                  changeOpen(false);
                  setRenaming({ id: session.id, label });
                }}>
                <Pencil className="h-3.5 w-3.5" aria-hidden="true" />
              </button>
            )}
          </span>
        )}
      </CommandItem>
    );
  });

  return (
    <>
      <Popover open={open} onOpenChange={changeOpen}>
        <PopoverTrigger asChild>
          <button type="button" disabled={disabled} aria-label={`Chat: ${triggerLabel}`} title="Switch chats"
            className="flex h-6 min-w-0 max-w-full items-center gap-1 rounded-md px-1.5 text-sm font-medium text-foreground transition-colors hover:bg-accent focus:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-60 aria-expanded:bg-accent [@media(pointer:coarse)]:h-7">
            <span className={'min-w-0 truncate'}>{triggerLabel}</span>
            <ChevronDown className="h-3.5 w-3.5 shrink-0 text-muted-foreground" aria-hidden="true" />
          </button>
        </PopoverTrigger>
        <PopoverContent align="start" aria-label="Chats" className="w-72 max-w-[calc(100vw-2rem)] p-0"
          initialFocus={(type) => (type === 'touch' ? null : search.current) ?? root.current}>
          <Command ref={root} loop value={highlighted} onValueChange={setHighlighted} className="outline-none"
            filter={(_value, text, keywords) => matches(text, (keywords ?? []).join(' ')) ? 1 : 0}>
            {sessions.length > 0 && <CommandInput ref={search} placeholder="Search chats…" className="h-8" value={query} onValueChange={setQuery} />}
            <CommandList className="max-h-96">
              {sessions.length > 0
                ? <CommandGroup heading="Chats">{chatRows}</CommandGroup>
                : <p className="px-3 py-3 text-xs text-muted-foreground">No chats yet. Use + to start one.</p>}
              {attachExisting && (
                <>
                  {sessions.length > 0 && <CommandSeparator />}
                  <CommandGroup>
                    <CommandItem value="attach-existing" keywords={['Attach an existing chat']} className="gap-2 text-xs text-muted-foreground"
                      onSelect={() => { changeOpen(false); attachExisting.toggle(); }}>
                      <Paperclip className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
                      <span>{attachExisting.open ? 'Hide existing chats' : 'Attach an existing chat…'}</span>
                    </CommandItem>
                  </CommandGroup>
                </>
              )}
              {sessions.length > 0 && <CommandEmpty className="py-4 text-center text-xs text-muted-foreground">No chats found.</CommandEmpty>}
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
      {onRenameSession && <RenameChatDialog chat={renaming} onClose={() => setRenaming(null)} onRename={onRenameSession} />}
    </>
  );
}
