import { useState } from 'react';
import { Check, ChevronsUpDown, Star } from 'lucide-react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/shared/components/ui/command.tsx';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';

interface AgentChatSessionSelectorProps {
  sessions: Array<{ id: string }>;
  activeSessionId: string | null;
  mainSessionId?: string | null;
  onSelectSession: (sessionId: string) => void;
}

export function AgentChatSessionSelector({ sessions, activeSessionId, mainSessionId = null, onSelectSession }: AgentChatSessionSelectorProps) {
  const [open, setOpen] = useState(false);
  const activeIndex = sessions.findIndex((session) => session.id === activeSessionId);
  const activeLabel = activeIndex >= 0 ? `Chat ${activeIndex + 1}` : 'Choose chat';

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <button
          type="button"
          role="combobox"
          aria-label="Project chat session"
          aria-expanded={open}
          title={`Choose chat session: ${activeLabel}`}
          className="flex h-7 w-[5.5rem] min-w-0 max-w-32 shrink items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground transition-colors hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <span className="min-w-0 truncate">{activeLabel}</span>
          <ChevronsUpDown className="ml-auto h-3.5 w-3.5 shrink-0 opacity-50" aria-hidden="true" />
        </button>
      </PopoverTrigger>
      <PopoverContent className="w-48 max-w-[calc(100vw-2rem)] p-0" align="end">
        <Command>
          <CommandInput placeholder="Search chats..." className="h-8" />
          <CommandList>
            <CommandEmpty>No chats found.</CommandEmpty>
            <CommandGroup heading="Agent chats">
              {sessions.map((session, index) => {
                const label = `Chat ${index + 1}`;
                const selected = session.id === activeSessionId;
                return (
                  <CommandItem
                    key={session.id}
                    value={label}
                    keywords={[label]}
                    onSelect={() => {
                      onSelectSession(session.id);
                      setOpen(false);
                    }}
                  >
                    <Check className={`mr-2 h-3.5 w-3.5 shrink-0 ${selected ? 'opacity-100' : 'opacity-0'}`} aria-hidden="true" />
                    <span>{label}</span>
                    {session.id === mainSessionId && <span className="ml-auto flex items-center gap-1 text-[10px] text-muted-foreground"><Star className="h-3 w-3 fill-current" aria-hidden="true" />Main</span>}
                  </CommandItem>
                );
              })}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
