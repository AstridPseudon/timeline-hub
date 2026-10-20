import { useMemo, useState } from 'react';
import { Search, Sparkles } from 'lucide-react';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { useQueryClient } from '@tanstack/react-query';
import { Button } from '@/shared/components/ui/button.tsx';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog.tsx';
import { Input } from '@/shared/components/ui/input.tsx';
import { Badge } from '@/shared/components/ui/badge.tsx';
import { useAgentChatBridge } from '@/shared/contexts/AgentChatContext.tsx';
import { timelineQueryKey } from '@/tools/video-editor/hooks/useTimeline.ts';
import {
  useTimelineChromeContextSafe,
  useTimelineEditorData,
  useTimelineEditorOpsSafe,
  useTimelineEditorDataSafe,
} from '@/tools/video-editor/hooks/timelineStore.ts';
import { captureClipScalarEdit, submitClipScalarEdit } from '@/tools/video-editor/commands/clipScalarGesture.ts';
import { buildElementOverlayRow } from '@/tools/video-editor/runtime/element-adapter.ts';
import type { AstridElementCatalogEntry } from '@/tools/video-editor/runtime/element-contract.ts';

type ElementFilter = 'all' | 'effect' | 'animation' | 'transition';

function publicationLabel(element: AstridElementCatalogEntry): string {
  return element.publication === 'draft' ? 'Draft / Preview only' : element.publication;
}

function parentClipSelect(clip: { id: string; app?: unknown }): string | null {
  const canonical = clip.app && typeof clip.app === 'object' && !Array.isArray(clip.app)
    ? (clip.app as { canonical?: unknown }).canonical : undefined;
  if (canonical !== undefined) {
    if (!canonical || typeof canonical !== 'object' || Array.isArray(canonical)) return null;
    const clipRef = (canonical as { clipRef?: unknown }).clipRef;
    if (typeof clipRef !== 'string') return null;
    return /^parent\/clip:[^/]+$/.test(clipRef) && !clipRef.includes('::') ? clipRef : null;
  }
  return typeof clip.id === 'string' && !clip.id.includes('/') && !clip.id.includes('::')
    ? `parent/clip:${clip.id}` : null;
}

function retainedFps(value: unknown): number {
  if (typeof value === 'number' && Number.isFinite(value) && value > 0) return value;
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    const rate = value as { numerator?: unknown; denominator?: unknown };
    if (typeof rate.numerator === 'number' && typeof rate.denominator === 'number'
      && Number.isFinite(rate.numerator) && Number.isFinite(rate.denominator) && rate.numerator > 0 && rate.denominator > 0) {
      return rate.numerator / rate.denominator;
    }
  }
  return 30;
}

export function ElementsLibraryPanel({
  open,
  onOpenChange,
  onOpenCreationPrompt,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onOpenCreationPrompt: () => void;
}) {
  const { editorContext } = useAgentChatBridge();
  const { selectedClipIds } = useTimelineEditorData();
  const current = useTimelineEditorDataSafe()?.data;
  const clipScalar = useTimelineEditorOpsSafe()?.clipScalar;
  const elementOverlay = useTimelineChromeContextSafe()?.commandSession?.elementOverlay;
  const queryClient = useQueryClient();
  const [filter, setFilter] = useState<ElementFilter>('all');
  const [query, setQuery] = useState('');
  const [busyId, setBusyId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const selectedIds = useMemo(() => [...selectedClipIds], [selectedClipIds]);

  const filteredElements = useMemo(() => {
    const elements = editorContext?.elementContext?.catalog ?? [];
    const normalized = query.trim().toLowerCase();
    return elements.filter((element) => (
      (filter === 'all' || element.kind === filter)
      && (!normalized || `${element.id} ${element.label} ${element.description ?? ''}`.toLowerCase().includes(normalized))
    ));
  }, [editorContext?.elementContext?.catalog, filter, query]);

  const applyElement = async (element: AstridElementCatalogEntry) => {
    const adapter = editorContext?.elementOperationAdapter;
    const project = editorContext?.projectSlug;
    const timeline = editorContext?.timelineId;
    const expectedVersion = editorContext?.timelineSummary?.configVersion;
    if (element.publication !== 'published') {
      setMessage(`${element.label} is still a draft. Validate it before applying it to the timeline.`);
      return;
    }
    if (element.kind === 'transition' && selectedIds.length < 2) {
      setMessage('Select two adjacent clips to apply a transition.');
      return;
    }
    if (element.kind !== 'transition' && selectedIds.length < 1) {
      setMessage('Select a clip to apply this element.');
      return;
    }
    if (element.kind === 'transition') {
      if (element.packId && element.packId !== 'rendering') {
        setMessage('Hosted transition binding is unavailable for this project pack; the draft was not changed.');
        return;
      }
      if (!current || !clipScalar) {
        setMessage('Native transition editing is unavailable until the current timeline session is ready.');
        return;
      }
      const target = current.resolvedConfig.clips.find((clip) => clip.id === selectedIds[1]);
      if (!target) {
        setMessage('The selected transition target is no longer present in the current timeline.');
        return;
      }
      const fps = retainedFps(current.resolvedConfig.output?.fps);
      const defaults = element.defaults as Record<string, unknown> | undefined;
      const durationFrames = defaults?.durationFrames;
      const frames = Number.isInteger(durationFrames) && Number(durationFrames) > 0 ? Number(durationFrames) : 8;
      setBusyId(element.id);
      setMessage(null);
      try {
        const captured = captureClipScalarEdit(clipScalar, current, target.id);
        submitClipScalarEdit(captured, {
          values: {
            transition: { type: element.id, duration: frames / fps, revision: element.revision },
            elementRef: {
              id: element.id,
              kind: 'transition',
              revision: element.revision,
              ...(element.packId ? { packId: element.packId } : {}),
            },
          },
          clear: [],
        });
        setMessage(`${element.label} queued through the native timeline session.`);
      } catch (error) {
        setMessage(error instanceof Error ? error.message : String(error));
      } finally {
        setBusyId(null);
      }
      return;
    }
    if (element.kind === 'effect' && !element.packId) {
      if (!current || !elementOverlay) {
        setMessage('Literal overlay editing is unavailable until the native timeline session is ready.');
        return;
      }
      const selectedClip = current.resolvedConfig.clips.find((clip) => clip.id === selectedIds[0]);
      const exactEntries = editorContext?.elementContext?.catalog.filter((candidate) =>
        candidate.id === element.id && candidate.kind === 'effect' && candidate.revision === element.revision
        && candidate.packId === undefined);
      if (!selectedClip || exactEntries?.length !== 1 || exactEntries[0].publication !== 'published'
        || exactEntries[0].admitted !== true || exactEntries[0].legacy) {
        setMessage('This literal element is not admitted for the current timeline.');
        return;
      }
      const selectedScope = parentClipSelect(selectedClip);
      if (!selectedScope || selectedScope !== `parent/clip:${selectedClip.id}`) {
        setMessage('Literal overlays are unavailable for occurrence-owned clips.');
        return;
      }
      setBusyId(element.id);
      setMessage(null);
      try {
        const row = buildElementOverlayRow(current.resolvedConfig,
          { id: element.id, kind: 'effect', revision: element.revision }, selectedClip.id);
        const captured = elementOverlay.capture({ current, operation: {
          kind: 'create', row: row as unknown as Record<string, JSON>,
        } });
        const prepared = elementOverlay.finish(captured);
        elementOverlay.submit(prepared);
        setMessage(`${element.label} queued through the native timeline session.`);
      } catch (error) {
        setMessage(error instanceof Error ? error.message : String(error));
      } finally {
        setBusyId(null);
      }
      return;
    }
    if (!adapter || !project || !timeline || !expectedVersion) {
      setMessage('Elements are unavailable until the current timeline is loaded.');
      return;
    }
    setBusyId(element.id);
    setMessage(null);
    try {
      const result = element.kind === 'transition'
        ? await adapter.execute({
            name: 'timeline.apply_transition',
            project,
            timeline,
            expected_version: expectedVersion,
            from_clip: selectedIds[0],
            to_clip: selectedIds[1],
            transition: {
              id: element.id,
              kind: element.kind,
              revision: element.revision,
              ...(element.packId ? { packId: element.packId } : {}),
            },
          })
        : await adapter.execute({
            name: 'timeline.apply_element',
            project,
            timeline,
            expected_version: expectedVersion,
            clip_id: selectedIds[0],
            placement: element.kind === 'animation' ? 'clip' : 'overlay',
            element: {
              id: element.id,
              kind: element.kind,
              revision: element.revision,
              ...(element.packId ? { packId: element.packId } : {}),
            },
          });
      await queryClient.invalidateQueries({ queryKey: timelineQueryKey(timeline) });
      setMessage(`${element.label} applied${result.config_version ? ` · timeline v${result.config_version}` : ''}.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error));
    } finally {
      setBusyId(null);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2"><Sparkles className="h-4 w-4" /> Elements</DialogTitle>
          <DialogDescription>
            One library for effects, animations, and transitions. Ask Astrid to create a new element when you need something new.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <div className="relative min-w-0 flex-1">
              <Search className="pointer-events-none absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search elements" className="pl-8" />
            </div>
            <div className="flex shrink-0 gap-1" role="tablist" aria-label="Element type">
              {(['all', 'effect', 'animation', 'transition'] as const).map((value) => (
                <Button key={value} type="button" size="sm" variant={filter === value ? 'secondary' : 'ghost'} onClick={() => setFilter(value)}>
                  {value === 'all' ? 'All' : `${value[0].toUpperCase()}${value.slice(1)}s`}
                </Button>
              ))}
            </div>
          </div>
          <div className="max-h-[50vh] space-y-2 overflow-y-auto pr-1">
            {filteredElements.length === 0 ? (
              <div className="rounded-lg border border-dashed p-6 text-center text-sm text-muted-foreground">
                No registered elements are available in this editor session.
              </div>
            ) : filteredElements.map((element) => (
              <div key={`${element.kind}:${element.id}`} className="flex items-center justify-between gap-3 rounded-lg border border-border/70 p-3">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="font-medium">{element.label}</span>
                    <Badge variant="outline" className="text-[10px]">{element.kind}</Badge>
                    <Badge variant={element.publication === 'published' ? 'secondary' : 'outline'} className="text-[10px]">{publicationLabel(element)}</Badge>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">{element.description ?? element.id}</p>
                  <p className="mt-1 text-[10px] text-muted-foreground">{element.id} · {element.revision}</p>
                </div>
                <Button type="button" size="sm" variant="outline" disabled={busyId !== null || element.publication !== 'published'} onClick={() => void applyElement(element)}>
                  {busyId === element.id ? 'Applying…' : 'Apply'}
                </Button>
              </div>
            ))}
          </div>
          {message && <div role="status" className="rounded-md border border-border bg-muted/30 px-3 py-2 text-xs">{message}</div>}
          <div className="flex justify-end border-t border-border pt-3">
            <Button type="button" variant="secondary" onClick={() => { onOpenChange(false); onOpenCreationPrompt(); }}>
              Ask Astrid to create an element
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
