import { useState } from 'react';
import { Check, ChevronsUpDown, Pencil, Star } from 'lucide-react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/shared/components/ui/command.tsx';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import { Button } from '@/shared/components/ui/button.tsx';
import { Input } from '@/shared/components/ui/input.tsx';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog.tsx';
import { toast } from '@/shared/components/ui/toast.tsx';
import type { LocalAgentId } from '@/integrations/astrid/localAgents.ts';
import { AgentIcon, agentNames } from './agentIdentity.tsx';

interface AgentChatSessionSelectorProps {
  sessions: Array<{ id: string; title?: string; chatNumber?: number }>;
  activeSessionId: string | null;
  mainSessionId?: string | null;
  onOpenChange?: (open: boolean) => void;
  onSelectSession: (sessionId: string) => void;
  onSetMainSession?: (sessionId: string) => void;
  onRenameSession?: (sessionId: string, title: string) => Promise<unknown>;
  settingMainSessionId?: string | null;
  /** Each chat's agent and the model it last used, shown under its title. */
  describeSession?: (sessionId: string) => { agent: LocalAgentId; model?: string | null };
}

export function AgentChatSessionSelector({
  sessions,
  activeSessionId,
  mainSessionId = null,
  onOpenChange,
  onSelectSession,
  onSetMainSession,
  onRenameSession,
  settingMainSessionId = null,
  describeSession,
}: AgentChatSessionSelectorProps) {
  const [open, setOpen] = useState(false);
  const [renaming, setRenaming] = useState<{ id: string } | null>(null);
  const [renameValue, setRenameValue] = useState('');
  const [renameError, setRenameError] = useState<string | null>(null);
  const [renamePending, setRenamePending] = useState(false);
  const activeIndex = sessions.findIndex((session) => session.id === activeSessionId);
  const activeSession = activeIndex >= 0 ? sessions[activeIndex] : null;
  const activeLabel = activeIndex >= 0
    ? activeSession?.title?.trim() || `Chat ${activeSession?.chatNumber ?? activeIndex + 1}`
    : 'Choose chat';
  const activeFallbackLabel = activeSession ? `Chat ${activeSession.chatNumber ?? activeIndex + 1}` : null;
  const activeCommandValue = activeSession ? `${activeLabel} ${activeFallbackLabel}` : undefined;
  const handleOpenChange = (nextOpen: boolean) => {
    setOpen(nextOpen);
    onOpenChange?.(nextOpen);
  };

  return (
    <Popover open={open} onOpenChange={handleOpenChange}>
      <PopoverTrigger asChild>
        <button
          type="button"
          role="combobox"
          aria-label="Project chat session"
          aria-expanded={open}
          title={`Choose chat session: ${activeLabel}`}
          className="flex h-7 min-w-0 max-w-40 shrink items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground transition-colors hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <span className={`min-w-0 truncate ${activeSession?.title?.trim() ? 'preserve-case' : 'normal-case'}`}>{activeLabel}</span>
          <ChevronsUpDown className="ml-auto hidden h-3.5 w-3.5 shrink-0 opacity-50 @[24rem]/agent-header:block" aria-hidden="true" />
        </button>
      </PopoverTrigger>
      <PopoverContent className="w-72 max-w-[calc(100vw-2rem)] p-0" align="end">
        <Command defaultValue={activeCommandValue}>
          <CommandInput placeholder="Search chats..." className="h-8" />
          <CommandList>
            <CommandEmpty>No chats found.</CommandEmpty>
            <CommandGroup heading="Agent chats">
              {sessions.map((session, index) => {
                const fallbackLabel = `Chat ${session.chatNumber ?? index + 1}`;
                const label = session.title?.trim() || fallbackLabel;
                const selected = session.id === activeSessionId;
                const isMain = session.id === mainSessionId;
                const isSettingMain = session.id === settingMainSessionId;
                const meta = describeSession?.(session.id);
                const metaLabel = meta ? `${agentNames[meta.agent]}${meta.model ? ` · ${meta.model}` : ''}` : null;
                return (
                  <CommandItem
                    key={session.id}
                    value={`${label} ${fallbackLabel}`}
                    keywords={[label, fallbackLabel, ...(isMain ? ['Main'] : []), ...(metaLabel ? [metaLabel] : [])]}
                    className="group"
                    onSelect={() => {
                      onSelectSession(session.id);
                      handleOpenChange(false);
                    }}
                  >
                    <Check className={`mr-2 h-3.5 w-3.5 shrink-0 ${selected ? 'opacity-100' : 'opacity-0'}`} aria-hidden="true" />
                    <span className="flex min-w-0 flex-1 flex-col">
                      <span className={`min-w-0 truncate ${session.title?.trim() ? 'preserve-case' : 'normal-case'}`}>{label}</span>
                      {meta && (
                        <span className="flex min-w-0 items-center gap-1 text-[11px] leading-4 text-muted-foreground normal-case" title={metaLabel ?? undefined}>
                          <AgentIcon agent={meta.agent} className="h-3 w-3 shrink-0" />
                          <span className="truncate">{metaLabel}</span>
                        </span>
                      )}
                    </span>
                    {(isMain || onSetMainSession || (onRenameSession && selected)) && (
                      <span className="ml-auto flex shrink-0 items-center gap-0.5">
                        {isMain ? (
                          <span className="flex items-center gap-1 pl-2 text-[10px] uppercase tracking-[0.12em] text-muted-foreground">
                            <Star className="h-3 w-3 fill-current" aria-hidden="true" />Main
                          </span>
                        ) : onSetMainSession && (
                          <button
                            type="button"
                            aria-label={`Make ${label} main`}
                            title={`Make ${label} main`}
                            disabled={settingMainSessionId !== null}
                            className={`inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-sm text-muted-foreground hover:bg-foreground/5 ${settingMainSessionId !== null ? 'opacity-100' : 'opacity-0 group-hover:opacity-100 focus-visible:opacity-100'}`}
                            onClick={(event) => {
                              event.preventDefault();
                              event.stopPropagation();
                              onSetMainSession(session.id);
                            }}
                          >
                            <Star className={`h-3.5 w-3.5 ${isSettingMain ? 'animate-pulse fill-current' : ''}`} aria-hidden="true" />
                          </button>
                        )}
                        {onRenameSession && selected && (
                          <button
                            type="button"
                            aria-label={`Rename ${label}`}
                            title={`Rename ${label}`}
                            className="inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-sm text-muted-foreground opacity-0 transition-opacity hover:bg-foreground/5 hover:text-foreground focus-visible:opacity-100 group-hover:opacity-100 group-data-[selected=true]:opacity-100 [@media(hover:none)]:opacity-100"
                            onClick={(event) => {
                              event.preventDefault();
                              event.stopPropagation();
                              handleOpenChange(false);
                              setRenaming({ id: session.id });
                              setRenameValue(label);
                              setRenameError(null);
                            }}
                          >
                            <Pencil className="h-3.5 w-3.5" aria-hidden="true" />
                          </button>
                        )}
                      </span>
                    )}
                  </CommandItem>
                );
              })}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
      {onRenameSession && <Dialog
        open={!!renaming}
        onOpenChange={(nextOpen) => {
          if (!nextOpen && !renamePending) setRenaming(null);
        }}
      >
        <DialogContent className="sm:max-w-sm">
          <form
            className="space-y-4"
            onSubmit={async (event) => {
              event.preventDefault();
              const title = renameValue.trim();
              if (!title) {
                setRenameError('Enter a chat name.');
                return;
              }
              if (title.length > 120) {
                setRenameError('Chat names must be 120 characters or fewer.');
                return;
              }
              if (!renaming) return;
              setRenamePending(true);
              setRenameError(null);
              try {
                await onRenameSession(renaming.id, title);
                setRenaming(null);
              } catch (error) {
                toast.error(error instanceof Error ? error.message : 'Could not rename chat.');
              } finally {
                setRenamePending(false);
              }
            }}
          >
            <DialogHeader><DialogTitle>Rename chat</DialogTitle></DialogHeader>
            <div className="space-y-2">
              <Input
                autoFocus
                aria-label="Chat name"
                value={renameValue}
                maxLength={121}
                className="[:root:not(.preserve-user-text)_&.preserve-case]:!normal-case"
                onFocus={(event) => event.currentTarget.select()}
                aria-invalid={!!renameError}
                aria-describedby={renameError ? 'rename-chat-error' : undefined}
                onChange={(event) => { setRenameValue(event.target.value); setRenameError(null); }}
                disabled={renamePending}
              />
              {renameError && <p id="rename-chat-error" className="text-sm text-destructive" role="alert">{renameError}</p>}
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" disabled={renamePending} onClick={() => setRenaming(null)}>Cancel</Button>
              <Button type="submit" disabled={renamePending}>Save</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>}
    </Popover>
  );
}
