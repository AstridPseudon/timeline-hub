import { useEffect, useState } from 'react';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/shared/components/ui/popover.tsx';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/shared/components/ui/command.tsx';
import { Check, ChevronsUpDown, Pencil, Plus, Star } from 'lucide-react';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import type { UseAstridBridgeDiscoveryResult } from '@/tools/video-editor/hooks/useAstridBridgeDiscovery.ts';
import { Button } from '@/shared/components/ui/button.tsx';
import { Input } from '@/shared/components/ui/input.tsx';
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/shared/components/ui/dialog.tsx';
import { toast } from '@/shared/components/ui/toast.tsx';

interface ProjectTimelineSelectorsProps {
  localProjectSlug: string | null;
  localProjectName?: string | null;
  localTimelineId: string | null;
  localTimelineName: string | null;
  /** Result of `useAstridBridgeDiscovery` (owned by the page). */
  discovery: UseAstridBridgeDiscoveryResult;
  /** Called with the selected Astrid project slug. */
  onSelectProject: (projectSlug: string) => void;
  onSelectTimeline: (timelineId: string) => void;
  /** Persists the project-level primary timeline selection. */
  onSetPrimaryTimeline?: (timelineId: string) => void;
  /** Creates a new canonical timeline in the selected local project. */
  onCreateTimeline?: () => void;
  creatingTimeline?: boolean;
  /** Canonical timeline id currently being promoted, if any. */
  settingPrimaryTimelineId?: string | null;
  /** Disables the triggers while a save is in flight. */
  disabled?: boolean;
  /** The app-wide header already owns the project selector in the live shell. */
  showProjectSelector?: boolean;
  /** Keeps the selector accessible while omitting a redundant visible label. */
  showProjectLabel?: boolean;
  /** The shared app header omits the editor timeline picker outside the editor. */
  showTimelineSelector?: boolean;
  /** Reports whether any dropdown is open (drives discovery refetch/polling). */
  onOpenChange?: (open: boolean) => void;
}

const triggerClass = cn(
  'flex h-7 min-w-0 items-center gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs',
  'text-muted-foreground transition-colors hover:bg-accent hover:text-foreground',
  'focus:outline-none focus-visible:ring-2 focus-visible:ring-ring',
  'disabled:pointer-events-none disabled:opacity-50',
);

/**
 * Picker rows follow the shared Select: a fixed leading check slot (pl-8) and a
 * soft neutral tint for the current choice, distinct from the accent used for
 * the keyboard/hover highlight (which still wins on the current row).
 */
const rowClass = cn(
  'group gap-2 py-1.5 pl-8 pr-1.5',
  'data-[current=true]:bg-muted data-[current=true]:font-medium',
  'data-[current=true]:data-[selected=true]:bg-accent',
);

/** Row actions stay hidden until the row is hovered/highlighted or the action is focused. */
const rowActionClass = cn(
  'h-6 w-6 shrink-0 rounded-sm text-muted-foreground [&_svg]:size-3.5',
  'hover:bg-foreground/5 hover:text-foreground focus-visible:ring-offset-0',
  'opacity-0 transition-opacity focus-visible:opacity-100',
  'group-hover:opacity-100 group-data-[selected=true]:opacity-100',
  '[@media(hover:none)]:opacity-100',
);

/**
 * The rename field edits the name exactly as stored, so undo the user-text
 * lowercase display rule from index.css here (same selector, more specific).
 */
const renameInputClass =
  '[:root:not(.preserve-user-text)_&.preserve-case]:!normal-case';

const timelineRecency = (timeline: {
  created_at?: string;
  updated_at?: string;
}): number | null => {
  const value = timeline.updated_at ?? timeline.created_at;
  if (!value) return null;
  const timestamp = Date.parse(value);
  return Number.isFinite(timestamp) ? timestamp : null;
};

export function ProjectTimelineSelectors(props: ProjectTimelineSelectorsProps) {
  const {
    discovery,
    localProjectSlug,
    localTimelineId,
    localProjectName,
    localTimelineName,
  } = props;
  const projects = discovery.projectsQuery.data?.projects ?? [];
  const timelines = (discovery.timelinesQuery.data?.timelines ?? [])
    .filter(
      (t) =>
        !t.is_shot ||
        t.timeline_id === localTimelineId ||
        t.timeline_ulid === localTimelineId,
    )
    .map((t, index) => ({ t, index }))
    .sort(
      (a, b) =>
        (timelineRecency(b.t) ?? b.index) - (timelineRecency(a.t) ?? a.index),
    )
    .map(({ t }) => t);
  const [lastName, setLastName] = useState<{ id: string; name: string } | null>(
    null,
  );
  const projectName =
    localProjectName?.trim() ||
    projects.find((p) => p.slug === localProjectSlug)?.name?.trim();
  useEffect(() => {
    if (localProjectSlug && projectName)
      setLastName({ id: localProjectSlug, name: projectName });
  }, [localProjectSlug, projectName]);
  const pending =
    !discovery.bridgeDown &&
    !discovery.projectsQuery.error &&
    (discovery.healthQuery.isLoading ||
      discovery.projectsQuery.isLoading ||
      discovery.projectsQuery.isFetching ||
      !discovery.projectsQuery.data);
  const fallback =
    lastName?.id === localProjectSlug &&
    (!discovery.projectsQuery.data || discovery.projectsQuery.isFetching)
      ? lastName.name
      : undefined;
  return (
    <ProjectTimelinePicker
      projects={projects.map((p) => ({
        id: p.slug,
        name: p.name,
        detail: p.slug,
      }))}
      timelines={timelines.map((t) => ({
        id: t.timeline_ulid ?? t.timeline_id,
        name: t.name,
        canonicalId: t.timeline_id,
        isPrimary: t.is_default,
      }))}
      projectId={localProjectSlug}
      timelineId={localTimelineId}
      projectName={
        projectName ||
        fallback ||
        (localProjectSlug
          ? pending
            ? 'Loading project…'
            : discovery.projectsQuery.error
              ? localProjectSlug
              : 'Project not found'
          : pending
            ? 'Loading projects…'
            : 'Select project')
      }
      timelineName={
        localTimelineName ||
        timelines.find(
          (t) =>
            t.timeline_id === localTimelineId ||
            t.timeline_ulid === localTimelineId,
        )?.name ||
        localTimelineId
      }
      projectsLoading={
        discovery.healthQuery.isLoading || discovery.projectsQuery.isLoading
      }
      timelinesLoading={discovery.timelinesQuery.isLoading}
      projectsError={
        discovery.projectsQuery.error?.message ||
        (discovery.bridgeDown
          ? 'Unable to connect to the local workspace. Start the installed Runtime and reopen the editor.'
          : undefined)
      }
      timelinesError={discovery.timelinesQuery.error?.message}
      onSelectProject={props.onSelectProject}
      onSelectTimeline={props.onSelectTimeline}
      onSetPrimaryTimeline={props.onSetPrimaryTimeline}
      settingPrimaryTimelineId={props.settingPrimaryTimelineId}
      onCreateTimeline={props.onCreateTimeline}
      creatingTimeline={props.creatingTimeline}
      disabled={props.disabled}
      showProjectSelector={props.showProjectSelector}
      showTimelineSelector={props.showTimelineSelector}
      showProjectLabel={props.showProjectLabel}
      onOpenChange={props.onOpenChange}
    />
  );
}

/** Backend-neutral presentation shared by the native Runtime and local selectors. */
export interface EditorProjectChoice {
  id: string;
  name: string;
  detail?: string;
}
export interface EditorTimelineChoice {
  id: string;
  name: string;
  /** Secondary metadata under the name, e.g. "edited 5 minutes ago". */
  detail?: string;
  isPrimary?: boolean;
  canonicalId?: string;
}
export function ProjectTimelinePicker({
  projects,
  timelines,
  projectId,
  timelineId,
  projectName,
  timelineName,
  projectsLoading = false,
  timelinesLoading = false,
  projectsError,
  timelinesError,
  onSelectProject,
  onSelectTimeline,
  onRetry,
  onSetPrimaryTimeline,
  settingPrimaryTimelineId,
  onCreateTimeline,
  creatingTimeline,
  disabled = false,
  showProjectSelector = true,
  showTimelineSelector = true,
  showProjectLabel = true,
  onOpenChange,
  onRenameTimeline,
}: {
  projects: readonly EditorProjectChoice[];
  timelines: readonly EditorTimelineChoice[];
  projectId: string | null;
  timelineId: string | null;
  projectName?: string | null;
  timelineName?: string | null;
  projectsLoading?: boolean;
  timelinesLoading?: boolean;
  projectsError?: string;
  timelinesError?: string;
  onSelectProject(id: string): void;
  onSelectTimeline(id: string): void;
  onRetry?(): void;
  onSetPrimaryTimeline?(id: string): void;
  settingPrimaryTimelineId?: string | null;
  onCreateTimeline?(): void;
  creatingTimeline?: boolean;
  disabled?: boolean;
  showProjectLabel?: boolean;
  showProjectSelector?: boolean;
  showTimelineSelector?: boolean;
  onOpenChange?(open: boolean): void;
  onRenameTimeline?: (timelineId: string, name: string) => Promise<void>;
}) {
  const [projectOpen, setProjectOpen] = useState(false),
    [timelineOpen, setTimelineOpen] = useState(false);
  const [renamingTimeline, setRenamingTimeline] = useState<EditorTimelineChoice | null>(null);
  const [renameValue, setRenameValue] = useState('');
  const [renameError, setRenameError] = useState<string | null>(null);
  const [renamePending, setRenamePending] = useState(false);
  useEffect(() => {
    onOpenChange?.(projectOpen || timelineOpen);
  }, [onOpenChange, projectOpen, timelineOpen]);
  const picker = (
    kind: 'project' | 'timeline',
    open: boolean,
    setOpen: (open: boolean) => void,
    rows: readonly (EditorProjectChoice & Partial<EditorTimelineChoice>)[],
    selected: string | null,
    label: string,
    loading: boolean,
    error?: string,
  ) => (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <button
          type="button"
          role="combobox"
          aria-label={`Select ${kind}`}
          aria-expanded={open}
          disabled={disabled}
          className={cn(triggerClass, 'max-w-64 min-h-8')}
        >
          <span className="truncate preserve-case">{label}</span>
          <ChevronsUpDown className="ml-auto h-3.5 w-3.5 shrink-0 opacity-50" />
        </button>
      </PopoverTrigger>
      <PopoverContent
        className="w-72 max-w-[calc(100vw-2rem)] p-0"
        align="start"
      >
        {/* Open with the current row highlighted, like a native select. */}
        <Command defaultValue={selected ?? undefined}>
          <CommandInput placeholder={`Search ${kind}s...`} className="h-8" />
          <CommandList>
            <CommandEmpty>No {kind}s found.</CommandEmpty>
            <CommandGroup
              heading={kind === 'project' ? 'Projects' : 'Timelines'}
              className="[&_[cmdk-group-heading]]:pl-8"
            >
              {loading && (
                <p
                  role="status"
                  className="px-3 py-2 text-xs text-muted-foreground"
                >
                  Loading {kind}s…
                </p>
              )}
              {error && (
                <div role="alert" className="p-3 text-xs">
                  <p>{error}</p>
                  {onRetry && (
                    <button
                      type="button"
                      className={triggerClass}
                      onClick={onRetry}
                    >
                      Retry connection
                    </button>
                  )}
                </div>
              )}
              {!loading && !error && !rows.length && (
                <p className="p-3 text-xs text-muted-foreground">
                  {kind === 'project'
                    ? 'No projects available.'
                    : 'No timelines for this project yet.'}
                </p>
              )}
              {rows.map((row) => {
                const current = selected === row.id;
                const primary = kind === 'timeline' && row.isPrimary;
                const canRename =
                  kind === 'timeline' && current && !!onRenameTimeline;
                const canMakePrimary =
                  kind === 'timeline' && !row.isPrimary && !!onSetPrimaryTimeline;
                return (
                  <CommandItem
                    key={row.id}
                    value={row.id}
                    keywords={[row.name, row.detail ?? '']}
                    aria-selected={current}
                    aria-current={current ? 'true' : undefined}
                    data-current={current || undefined}
                    className={rowClass}
                    onSelect={() => {
                      (kind === 'project' ? onSelectProject : onSelectTimeline)(
                        row.id,
                      );
                      setOpen(false);
                    }}
                  >
                    {current && (
                      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
                        <Check className="h-4 w-4" aria-hidden="true" />
                      </span>
                    )}
                    <span className="flex min-w-0 flex-1 flex-col">
                      <span className="truncate preserve-case" title={row.name}>
                        {row.name}
                      </span>
                      {(primary || row.detail) && (
                        <span className="truncate text-[11px] font-normal leading-4 text-muted-foreground">
                          {primary && <span>Primary</span>}
                          {primary && row.detail && ' · '}
                          {row.detail}
                        </span>
                      )}
                    </span>
                    {(canRename || canMakePrimary) && (
                      <span className="flex shrink-0 items-center gap-0.5">
                        {canMakePrimary && (
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            aria-label={`Make ${row.name} primary`}
                            disabled={!!settingPrimaryTimelineId}
                            className={rowActionClass}
                            onClick={(event) => {
                              event.preventDefault();
                              event.stopPropagation();
                              onSetPrimaryTimeline?.(row.canonicalId ?? row.id);
                            }}
                          >
                            <Star aria-hidden="true" />
                          </Button>
                        )}
                        {canRename && (
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            aria-label="Rename timeline"
                            className={rowActionClass}
                            onClick={(event) => {
                              event.preventDefault();
                              event.stopPropagation();
                              setRenameValue(row.name);
                              setRenameError(null);
                              setRenamingTimeline(row as EditorTimelineChoice);
                              setOpen(false);
                            }}
                          >
                            <Pencil aria-hidden="true" />
                          </Button>
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
    </Popover>
  );
  return (
    <>
    <div
      className="flex min-w-0 items-center gap-2"
      data-testid="editor-project-timeline-selectors"
    >
      {showProjectSelector && (
        <span
          className={cn(
            'text-xs font-medium text-muted-foreground',
            showProjectLabel === false && 'sr-only',
          )}
        >
          Project
        </span>
      )}
      {showProjectSelector &&
        picker(
          'project',
          projectOpen,
          setProjectOpen,
          projects,
          projectId,
          projectName ||
            projects.find((p) => p.id === projectId)?.name ||
            (projectsLoading
              ? 'Connecting to projects…'
              : projectId
                ? 'Project unavailable'
                : 'Select project'),
          projectsLoading,
          projectsError,
        )}
      {showTimelineSelector && (
        <span className="text-xs font-medium text-muted-foreground">
          Timeline
        </span>
      )}
      {showTimelineSelector &&
        picker(
          'timeline',
          timelineOpen,
          setTimelineOpen,
          timelines,
          timelineId,
          timelineName ||
            timelines.find((t) => t.id === timelineId)?.name ||
            (timelinesLoading
              ? 'Loading timelines…'
              : timelineId
                ? 'Timeline unavailable'
                : 'Select timeline'),
          timelinesLoading,
          timelinesError,
        )}
      {showTimelineSelector && onCreateTimeline && (
        <button
          type="button"
          aria-label="New timeline"
          disabled={disabled || creatingTimeline}
          className={triggerClass}
          onClick={onCreateTimeline}
        >
          <Plus className="h-3.5 w-3.5" />
          New timeline
        </button>
      )}
    </div>
    {onRenameTimeline && <Dialog
      open={!!renamingTimeline}
      onOpenChange={(open) => {
        if (!open && !renamePending) setRenamingTimeline(null);
      }}
    >
      <DialogContent className="sm:max-w-sm">
        <form
          onSubmit={async (event) => {
            event.preventDefault();
            const name = renameValue.trim();
            if (!name) {
              setRenameError('Enter a timeline name.');
              return;
            }
            if (name.length > 120) {
              setRenameError('Timeline names must be 120 characters or fewer.');
              return;
            }
            if (!renamingTimeline || !onRenameTimeline) return;
            setRenamePending(true);
            setRenameError(null);
            try {
              await onRenameTimeline(renamingTimeline.id, name);
              setRenamingTimeline(null);
            } catch (error) {
              toast.error(error instanceof Error ? error.message : 'Could not rename timeline.');
            } finally {
              setRenamePending(false);
            }
          }}
          className="space-y-4"
        >
          <DialogHeader>
            <DialogTitle>Rename timeline</DialogTitle>
          </DialogHeader>
          <div className="space-y-2">
            <Input
              autoFocus
              value={renameValue}
              maxLength={121}
              aria-label="Timeline name"
              className={renameInputClass}
              aria-invalid={!!renameError}
              aria-describedby={renameError ? 'rename-timeline-error' : undefined}
              onChange={(event) => {
                setRenameValue(event.target.value);
                setRenameError(null);
              }}
              disabled={renamePending}
            />
            {renameError && (
              <p id="rename-timeline-error" className="text-sm text-destructive" role="alert">
                {renameError}
              </p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" disabled={renamePending} onClick={() => setRenamingTimeline(null)}>
              Cancel
            </Button>
            <Button type="submit" disabled={renamePending}>
              Save
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>}
    </>
  );
}
