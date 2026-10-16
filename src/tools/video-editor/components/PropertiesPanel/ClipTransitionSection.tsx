import { useMemo } from 'react';
import { AlertTriangle, Globe, Monitor, RefreshCw, Server, Trash2 } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { NumberInput } from '@/shared/components/ui/number-input.tsx';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select.tsx';
import { ParameterControls } from '@/tools/video-editor/components/ParameterControls.tsx';
import { BlockerActionCard } from '@/tools/video-editor/components/BlockerActionCard.tsx';
import type { ClipEditorPatch } from '@/tools/video-editor/lib/timeline-data.ts';
import type { ResolvedTimelineClip } from '@/tools/video-editor/types/index.ts';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import type { AstridElementDescriptor, AstridElementHost } from '@/tools/video-editor/runtime/astrid-element-host.ts';
import {
  useOptionalTransitionRegistryContext,
  type TransitionRegistryRecord,
} from '@/tools/video-editor/transitions/registry/index.ts';
import {
  listTransitions,
  resolveTransition,
  createTransitionSnapshot,
  materializeTransitionDefaults,
} from '@/tools/video-editor/transitions/catalog.ts';
import { FieldLabel, NO_TRANSITION } from './clip-panel-primitives.tsx';

// ---------------------------------------------------------------------------
// Transition helpers (T11: single-clip transition controls)
// ---------------------------------------------------------------------------

/** Returns a short provenance label for display in transition selectors. */
function getTransitionProvenanceLabel(record: TransitionRegistryRecord): string | null {
  switch (record.provenance) {
    case 'built-in':
      return 'Built-in';
    case 'bundled-extension':
      return 'Extension';
    case 'external-catalog':
      return 'Catalog';
    case 'db-resource':
      return 'DB';
    case 'ai-generated':
      return 'AI';
    case 'local-storage-draft':
      return 'Draft';
    case 'trusted-loader':
      return 'Trusted';
    default:
      return null;
  }
}

/** Returns rendered export routes that are blocked for a transition record. */
function getTransitionBlockedRoutes(record: TransitionRegistryRecord): string[] {
  if (!record.renderability?.capabilities) return [];
  return record.renderability.capabilities
    .filter((cap) => cap.route !== 'preview' && cap.status === 'blocked')
    .map((cap) => cap.route);
}

/** Check if a transition is preview-only (browser-export and worker-export both blocked). */
function isTransitionPreviewOnly(record: TransitionRegistryRecord): boolean {
  if (!record.renderability?.capabilities) return false;
  const hasBrowserExport = record.renderability.capabilities.some(
    (cap) => cap.route === 'browser-export' && cap.status === 'supported',
  );
  const hasWorkerExport = record.renderability.capabilities.some(
    (cap) => cap.route === 'worker-export' && cap.status === 'supported',
  );
  const hasPreview = record.renderability.capabilities.some(
    (cap) => cap.route === 'preview' && cap.status === 'supported',
  );
  return hasPreview && !hasBrowserExport && !hasWorkerExport;
}

/** Check if stored transition params differ from schema defaults. */
function hasCustomTransitionParams(
  record: TransitionRegistryRecord | undefined,
  storedParams: Record<string, unknown> | null | undefined,
): boolean {
  if (!record?.schema?.length) return false;
  const defaults = materializeTransitionDefaults(record.schema);
  const params = storedParams ?? {};
  const allKeys = new Set([...Object.keys(defaults), ...Object.keys(params)]);
  for (const key of allKeys) {
    if (JSON.stringify(params[key]) !== JSON.stringify(defaults[key])) {
      return true;
    }
  }
  return false;
}

/** Merge stored transition params with schema defaults. */
function getMergedTransitionParams(
  record: TransitionRegistryRecord | undefined,
  storedParams: Record<string, unknown> | null | undefined,
): Record<string, unknown> {
  return {
    ...materializeTransitionDefaults(record?.schema),
    ...(storedParams ?? {}),
  };
}

function resolveDeclaredTransition(
  record: TransitionRegistryRecord | undefined,
  snapshot: ReturnType<typeof createTransitionSnapshot>,
  host: AstridElementHost | undefined,
): AstridElementDescriptor | undefined {
  if (!record || record.status !== 'active' || !host) return undefined;
  const matches = host.descriptors.filter((descriptor) => descriptor.kind === 'transition'
    && descriptor.revision.length > 0
    && descriptor.componentPath.length > 0
    && resolveTransition(descriptor.id, snapshot) === record
    && Boolean(host.resolveComponent(descriptor.id, 'transition', descriptor.packId)));
  return matches.length === 1 ? matches[0] : undefined;
}

function elementReference(descriptor: AstridElementDescriptor) {
  return {
    id: descriptor.id,
    revision: descriptor.revision,
    kind: 'transition' as const,
    ...(descriptor.packId ? { packId: descriptor.packId } : {}),
  };
}

/** T11: single-clip transition controls. */
export function ClipTransitionSection({
  clip,
  onChange,
}: {
  clip: ResolvedTimelineClip;
  onChange: (patch: ClipEditorPatch) => void;
}) {
  const elementHost = useOptionalVideoEditorRuntime()?.astridElementHost;
  const transitionRegistryContext = useOptionalTransitionRegistryContext();
  const mergedTransitionSnapshot = useMemo(
    () => createTransitionSnapshot(transitionRegistryContext?.snapshot),
    [transitionRegistryContext?.snapshot],
  );
  const availableTransitions = useMemo(
    () => listTransitions(mergedTransitionSnapshot),
    [mergedTransitionSnapshot],
  );
  const resolvedTransitionRecord = useMemo(() => {
    if (!clip?.transition?.type || clip.transition.type === NO_TRANSITION) return undefined;
    return resolveTransition(clip.transition.type, mergedTransitionSnapshot);
  }, [clip?.transition?.type, mergedTransitionSnapshot]);
  const isTransitionUnresolvable =
    clip?.transition?.type != null &&
    clip.transition.type !== NO_TRANSITION &&
    !resolvedTransitionRecord;
  const isTransitionInError = resolvedTransitionRecord?.status === 'error';
  const isTransitionInactive = resolvedTransitionRecord?.status === 'inactive';

  return (
    <div className="space-y-2 md:col-span-2">
      <FieldLabel>Transition</FieldLabel>
      <Select
        value={clip.transition?.type ?? NO_TRANSITION}
        onValueChange={(value) => {
          if (value === NO_TRANSITION) {
            onChange({ transition: undefined });
            return;
          }
          const record = resolveTransition(value, mergedTransitionSnapshot);
          const descriptor = resolveDeclaredTransition(record, mergedTransitionSnapshot, elementHost);
          const defaults = record?.schema
            ? materializeTransitionDefaults(record.schema)
            : undefined;
          const params = defaults && Object.keys(defaults).length > 0 ? defaults : undefined;
          onChange({
            transition: {
              type: descriptor?.id ?? value,
              duration: clip.transition?.duration ?? 0.5,
              ...(descriptor ? { revision: descriptor.revision } : {}),
              ...(params ? { params } : {}),
            },
            ...(descriptor ? { elementRef: elementReference(descriptor) } : {}),
          });
        }}
      >
        <SelectTrigger>
          <SelectValue placeholder="None">
            {!clip.transition?.type || clip.transition.type === NO_TRANSITION
              ? 'None'
              : isTransitionUnresolvable
                ? `${clip.transition.type} (missing)`
                : resolvedTransitionRecord
                  ? (() => {
                      const label = getTransitionProvenanceLabel(resolvedTransitionRecord);
                      return label
                        ? `${clip.transition.type} · ${label}`
                        : clip.transition.type;
                    })()
                  : clip.transition.type}
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={NO_TRANSITION}>None</SelectItem>
          {availableTransitions.map((record) => {
            const error = record.status === 'error';
            const inactive = record.status === 'inactive';
            const provenanceLabel = getTransitionProvenanceLabel(record);
            const blocked = getTransitionBlockedRoutes(record);
            return (
              <SelectItem
                key={record.transitionId}
                value={record.transitionId}
                disabled={error}
              >
                <span className="flex items-center gap-1.5">
                  {error && <AlertTriangle className="h-3 w-3 shrink-0 text-destructive" />}
                  {record.transitionId}
                  {provenanceLabel && (
                    <span className="ml-0.5 rounded-sm bg-blue-500/15 px-1 text-[9px] font-medium text-blue-300">
                      {provenanceLabel}
                    </span>
                  )}
                  {blocked.length > 0 && (
                    <span className="ml-0.5 rounded-sm bg-amber-500/15 px-1 text-[9px] font-medium text-amber-300">
                      {blocked.map((r) => r === 'browser-export' ? 'No B' : r === 'worker-export' ? 'No W' : r).join(', ')}
                    </span>
                  )}
                  {inactive && <span className="ml-1 text-[10px] text-muted-foreground">(inactive)</span>}
                  {error && <span className="ml-1 text-[10px] text-destructive">(invalid)</span>}
                </span>
              </SelectItem>
            );
          })}
          {/* Show the current transition if it's not in the list (e.g. removed contributed) */}
          {isTransitionUnresolvable && clip.transition?.type && (
            <>
              <div className="my-1 h-px bg-border" />
              <SelectItem value={clip.transition.type} disabled>
                <span className="text-muted-foreground">
                  {clip.transition.type} (missing)
                </span>
              </SelectItem>
            </>
          )}
        </SelectContent>
      </Select>

      {/* Renderability / provenance badges */}
      {resolvedTransitionRecord && (() => {
        const blocked = getTransitionBlockedRoutes(resolvedTransitionRecord);
        const previewOnly = isTransitionPreviewOnly(resolvedTransitionRecord);
        if (blocked.length === 0 && !previewOnly) return null;
        return (
          <div className="flex flex-wrap items-center gap-1.5 rounded-md border border-amber-500/30 bg-amber-500/8 px-2 py-1 text-[11px] text-amber-200">
            {previewOnly && (
              <span className="inline-flex items-center gap-1"><Monitor className="h-3 w-3" />Preview only</span>
            )}
            {blocked.includes('browser-export') && !previewOnly && (
              <span className="inline-flex items-center gap-1"><Globe className="h-3 w-3" />No browser export</span>
            )}
            {blocked.includes('worker-export') && !previewOnly && (
              <span className="inline-flex items-center gap-1"><Server className="h-3 w-3" />No worker export</span>
            )}
          </div>
        );
      })()}

      {/* Unresolvable / missing transition row */}
      {isTransitionUnresolvable && clip.transition && (
        <BlockerActionCard
          severity="error"
          code="composition/transition-missing-ref"
          message={`Transition "${clip.transition.type}" is not available. The extension may have been removed.`}
        />
      )}

      {/* Duration editing */}
      {clip.transition && clip.transition.type !== NO_TRANSITION && (
        <div className="space-y-1">
          <FieldLabel>Duration (seconds)</FieldLabel>
          <NumberInput
            value={clip.transition.duration}
            min={0.05}
            max={10}
            step={0.05}
            onChange={(value) => {
              if (value !== null && clip.transition) {
                onChange({
                  transition: {
                    ...clip.transition,
                    duration: value,
                  },
                });
              }
            }}
          />
        </div>
      )}

      {/* Remove / Reset buttons */}
      {clip.transition && clip.transition.type !== NO_TRANSITION && (
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-6 gap-1 text-xs text-destructive hover:text-destructive"
            onClick={() => onChange({ transition: undefined })}
          >
            <Trash2 className="h-3 w-3" /> Remove
          </Button>
          {resolvedTransitionRecord?.schema?.length &&
            hasCustomTransitionParams(resolvedTransitionRecord, clip.transition?.params) && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="h-6 gap-1 text-xs"
              onClick={() => {
                if (!clip.transition || !resolvedTransitionRecord?.schema) return;
                onChange({
                  transition: {
                    ...clip.transition,
                    params: materializeTransitionDefaults(resolvedTransitionRecord.schema),
                  },
                });
              }}
            >
              <RefreshCw className="h-3 w-3" /> Reset defaults
            </Button>
          )}
        </div>
      )}

      {/* Parameter controls */}
      {resolvedTransitionRecord?.schema?.length && clip.transition && (
        <ParameterControls
          schema={resolvedTransitionRecord.schema}
          values={getMergedTransitionParams(resolvedTransitionRecord, clip.transition?.params)}
          onChange={(paramName, value) => {
            if (!clip.transition) return;
            onChange({
              transition: {
                ...clip.transition,
                params: {
                  ...(clip.transition.params ?? {}),
                  [paramName]: value,
                },
              },
            });
          }}
          disabled={isTransitionInError || isTransitionInactive}
          diagnostics={resolvedTransitionRecord.diagnostics}
        />
      )}
    </div>
  );
}
