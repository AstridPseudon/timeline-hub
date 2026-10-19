import { useState } from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/components/ui/popover.tsx';
import type { AcpModelCatalog } from '@/integrations/astrid/acpRoutes.ts';

interface AgentChatModelSelectorProps {
  catalog: AcpModelCatalog;
  onSelectModel: (model: string) => void | Promise<void>;
  selectionError?: string | null;
  busy?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  loading?: boolean;
  catalogError?: string | null;
}

export function AgentChatModelSelector({ catalog, onSelectModel, selectionError = null, busy = false, open: controlledOpen, onOpenChange, loading = false, catalogError = null }: AgentChatModelSelectorProps) {
  const [localOpen, setLocalOpen] = useState(false);
  const open = controlledOpen ?? localOpen;
  const changeOpen = (next: boolean) => { setLocalOpen(next); onOpenChange?.(next); };
  const current = catalog.providers.flatMap(provider => provider.models.map(model => ({ provider, model })))
    .find(item => `${item.provider.id}/${item.model.id}` === catalog.currentModel);
  const openList = () => changeOpen(true);

  return (
    <div className="flex min-w-0 flex-col items-end">
      <Popover open={open} onOpenChange={changeOpen}>
        <PopoverTrigger asChild>
          <button type="button" role="combobox" aria-label="Agent model" aria-expanded={open}
            className="flex h-7 max-w-36 min-w-0 items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground hover:bg-accent hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring">
            <span className="truncate">{current?.model.name ?? catalog.currentModel ?? 'Choose model'}</span>
            <ChevronsUpDown className="h-3.5 w-3.5 shrink-0 opacity-50" aria-hidden="true" />
          </button>
        </PopoverTrigger>
        <PopoverContent align="end" className="w-72 max-w-[calc(100vw-2rem)] p-2">
          <div className="max-h-80 space-y-3 overflow-y-auto">
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
          </div>
        </PopoverContent>
      </Popover>
      {selectionError && <p role="alert" className="mt-1 max-w-64 text-right text-[10px] text-destructive">{selectionError} <button type="button" className="underline" onClick={openList}>Switch model</button></p>}
    </div>
  );
}
