import type { EditCommand, JSON, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { buildDataFromCurrentRegistry } from '../lib/timeline-save-utils.ts';
import { createShotCompositionAdapter, type ShotCompositionPort } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import type { AuthoringBundle } from './authoringBundle.ts';
import { copy, equal, freezeJson, object } from './clipMovePrimitives.ts';
import type { JsonObject } from './types.ts';

export type OccurrenceMediaRequest = {
  ownerRef: `occurrence:${string}`;
  trackRef: `occurrence:${string}/track:${string}`;
  media: MediaSelection;
} & ({ kind: 'add'; row: Record<string, JSON> } | {
  kind: 'swap'; clipRef: `occurrence:${string}/clip:${string}`; oldMedia: MediaSelection;
});

export interface OccurrenceMediaCapturePort {
  capture(input: { request: OccurrenceMediaRequest; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): Promise<{ command: EditCommand; preview: TimelinePatch }>;
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}

type PopupPostSelectionDiagnosticDetails = {
  occurrenceId?: string;
  ownerRef?: string;
  trackRef?: string;
  commandOp?: string;
  hasPort?: boolean;
  hasSelection?: boolean;
  hasTarget?: boolean;
  hasSession?: boolean;
};

function diagnosticError(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message
    .replace(/https?:\/\/\S+/gi, '[url]')
    .replace(/(?:authorization|cookie|password|secret|token|body)\s*[:=]\s*\S+/gi, '[redacted]')
    .slice(0, 180);
}

export function logPopupPostSelectionDiagnostic(
  boundary: string,
  outcome: 'enter' | 'return' | 'refused' | 'throw',
  details: PopupPostSelectionDiagnosticDetails = {},
  error?: unknown,
): void {
  console.log('[popup-post-selection-diagnostic]', {
    boundary,
    outcome,
    ...details,
    ...(error === undefined ? {} : { error: diagnosticError(error) }),
  });
}
/** Bind a shot-local display to its explicit owner in the mounted parent session. */
export function bindPopupOccurrenceMediaPort(
  port: OccurrenceMediaCapturePort,
  occurrenceId: string,
  getParent: () => TimelineData | null,
): OccurrenceMediaCapturePort {
  return {
    capture({ request, current }) {
      logPopupPostSelectionDiagnostic('popup-port.capture', 'enter', {
        occurrenceId,
        ownerRef: request.ownerRef,
        trackRef: request.trackRef,
        hasPort: true,
      });
      try {
        const parent = getParent();
        const projection = current.config.app?.canonicalComposition;
        if (!parent?.head || !object(projection)
          || projection.projectId !== parent.head.projectId
          || projection.parentDocumentId !== parent.head.timelineId
          || projection.headRevisionId !== parent.head.headRevisionId
          || !equal(projection.occurrenceIds, [occurrenceId])
          || request.ownerRef !== `occurrence:${occurrenceId}`) {
          logPopupPostSelectionDiagnostic('popup-port.capture.target', 'refused', {
            occurrenceId,
            ownerRef: request.ownerRef,
            trackRef: request.trackRef,
            hasTarget: Boolean(parent?.head && projection),
          });
          throw new Error('The popup media owner or displayed head changed; keep the imported media');
        }
        const basis = port.capture({ request, current: parent });
        logPopupPostSelectionDiagnostic('popup-port.capture', 'return', {
          occurrenceId,
          ownerRef: request.ownerRef,
          trackRef: request.trackRef,
          hasTarget: true,
        });
        return basis;
      } catch (error) {
        logPopupPostSelectionDiagnostic('popup-port.capture', 'throw', {
          occurrenceId,
          ownerRef: request.ownerRef,
          trackRef: request.trackRef,
        }, error);
        throw error;
      }
    },
    async finish(basis) {
      logPopupPostSelectionDiagnostic('popup-port.finish', 'enter', { occurrenceId, hasPort: true });
      try {
        if (!getParent()) throw new Error('The popup media session is closed; keep the imported media');
        const result = await port.finish(basis);
        if (!getParent()) throw new Error('The popup media session is closed; keep the imported media');
        logPopupPostSelectionDiagnostic('popup-port.finish', 'return', {
          occurrenceId,
          commandOp: result.command.op,
        });
        return result;
      } catch (error) {
        logPopupPostSelectionDiagnostic('popup-port.finish', 'throw', { occurrenceId }, error);
        throw error;
      }
    },
    submit(input) {
      logPopupPostSelectionDiagnostic('popup-port.submit', 'enter', {
        occurrenceId,
        commandOp: input.command.op,
        hasPort: true,
      });
      try {
        if (!getParent()) throw new Error('The popup media session is closed; keep the imported media');
        port.submit(input);
        logPopupPostSelectionDiagnostic('popup-port.submit', 'return', {
          occurrenceId,
          commandOp: input.command.op,
        });
      } catch (error) {
        logPopupPostSelectionDiagnostic('popup-port.submit', 'throw', {
          occurrenceId,
          commandOp: input.command.op,
        }, error);
        throw error;
      }
    },
  };
}

export type VerifiedMediaRead = (selection: MediaSelection) => Promise<VerifiedMedia>;

export function captureOccurrenceMediaEdit(port: OccurrenceMediaCapturePort | undefined, current: TimelineData, request: OccurrenceMediaRequest) {
  logPopupPostSelectionDiagnostic('capture', 'enter', {
    occurrenceId: request.ownerRef.slice('occurrence:'.length),
    ownerRef: request.ownerRef,
    trackRef: request.trackRef,
    hasPort: Boolean(port),
  });
  try {
    if (!port) throw new Error('Occurrence media capture is unavailable');
    const captured = Object.freeze({ port, basis: freezeJson(port.capture({ request, current })) });
    logPopupPostSelectionDiagnostic('capture', 'return', {
      occurrenceId: request.ownerRef.slice('occurrence:'.length),
      ownerRef: request.ownerRef,
      trackRef: request.trackRef,
    });
    return captured;
  } catch (error) {
    logPopupPostSelectionDiagnostic('capture', 'throw', {
      occurrenceId: request.ownerRef.slice('occurrence:'.length),
      ownerRef: request.ownerRef,
      trackRef: request.trackRef,
    }, error);
    throw error;
  }
}

export async function submitOccurrenceMediaEdit(captured: ReturnType<typeof captureOccurrenceMediaEdit>): Promise<void> {
  logPopupPostSelectionDiagnostic('submit', 'enter');
  let request: OccurrenceMediaRequest | undefined;
  try {
    const result = await captured.port.finish(captured.basis);
    request = captured.basis.request as unknown as OccurrenceMediaRequest;
    logPopupPostSelectionDiagnostic('submit.finish', 'return', {
      occurrenceId: request.ownerRef.slice('occurrence:'.length),
      ownerRef: request.ownerRef,
      commandOp: result.command.op,
    });
    const args = request.kind === 'add' ? { row: request.row, media: request.media } : { old_media: request.oldMedia, media: request.media };
    if (result.command.schema_version !== 1 || result.command.version !== '1'
      || result.command.op !== `occurrence.${request.kind}-media`
      || result.command.select !== (request.kind === 'add' ? request.ownerRef : request.clipRef)
      || !equal(result.command.intent, { ownership: 'occurrence' }) || !equal(result.command.args, args)) {
      logPopupPostSelectionDiagnostic('submit.command', 'refused', {
        occurrenceId: request.ownerRef.slice('occurrence:'.length),
        ownerRef: request.ownerRef,
        commandOp: result.command.op,
      });
      throw new Error('Unsupported occurrence media capture result');
    }
    logPopupPostSelectionDiagnostic('submit.port', 'enter', {
      occurrenceId: request.ownerRef.slice('occurrence:'.length),
      ownerRef: request.ownerRef,
      commandOp: result.command.op,
    });
    captured.port.submit(freezeJson(result));
    logPopupPostSelectionDiagnostic('submit.port', 'return', {
      occurrenceId: request.ownerRef.slice('occurrence:'.length),
      ownerRef: request.ownerRef,
      commandOp: result.command.op,
    });
  } catch (error) {
    logPopupPostSelectionDiagnostic('submit', 'throw', {
      ...(request === undefined ? {} : {
        occurrenceId: request.ownerRef.slice('occurrence:'.length),
        ownerRef: request.ownerRef,
        trackRef: request.trackRef,
      }),
    }, error);
    throw error;
  }
}

export function occurrenceMediaPreview(bundle: AuthoringBundle, graph: Record<string, unknown> | undefined): TimelinePatch {
  if (!graph) throw new Error('Occurrence media preview requires the original canonical graph');
  return freezeJson({ version: 1, source: 'occurrence.media', operations: [], meta: { occurrenceMediaBundle: copy(bundle), occurrenceMediaGraph: copy(graph) } });
}

export function projectOccurrenceMediaPreview(patch: TimelinePatch, current: TimelineData, port?: ShotCompositionPort): TimelineData | undefined {
  if (patch.source !== 'occurrence.media') return;
  const bundle = patch.meta?.occurrenceMediaBundle as AuthoringBundle | undefined;
  if (patch.version !== 1 || patch.operations.length || !bundle || !current.head || !port
    || bundle.project_id !== current.head.projectId || bundle.timeline_id !== current.head.timelineId) {
    throw new Error('Occurrence media preview requires its complete original scoped closure');
  }
  const prepared = createShotCompositionAdapter(port).prepare(patch.meta?.occurrenceMediaGraph);
  if (prepared.projectId !== bundle.project_id || prepared.parentDocumentId !== bundle.timeline_id
    || prepared.headRevisionId !== bundle.base_parent.revision_id || prepared.occurrences.length !== bundle.placements.length) {
    throw new Error('Occurrence media graph differs from its original scope');
  }
  const occurrences = prepared.occurrences.map((occurrence) => {
    const placement = bundle.placements.find((row) => row.occurrence_id === occurrence.occurrenceId);
    const shot = placement && bundle.shots[String(placement.shot_id)];
    const source = placement && bundle.source_mapping.shots[String(placement.shot_id)];
    if (!shot || !source || !equal(placement, bundle.base_placements[occurrence.occurrenceId])
      || source.shot_id !== occurrence.shotId || source.revision_id !== occurrence.revisionId) throw new Error('Occurrence media preview is missing an exact source binding');
    const internal = occurrence.revision.internal_timeline_revision;
    if (!object(internal) || internal.revision_id !== source.internal_timeline_revision_id) throw new Error('Occurrence media preview is missing its original internal revision');
    if (equal(shot.internal_timeline, shot.base_internal_timeline)) return occurrence;
    const playback = occurrence.revision.runtime_playback_assets ?? occurrence.revision.assets;
    const assets = Array.isArray(playback) ? copy(playback) : [];
    const registry = shot.internal_timeline.registry, baseRegistry = shot.base_internal_timeline.registry;
    if (!equal(registry, baseRegistry) && (!object(registry) || !object(registry.assets) || !object(baseRegistry) || !object(baseRegistry.assets))) throw new Error('Occurrence media preview cannot represent registry container changes');
    const bindings = object(registry) && object(registry.assets) ? registry.assets : {}, baseBindings = object(baseRegistry) && object(baseRegistry.assets) ? baseRegistry.assets : {};
    for (const [assetId, entry] of Object.entries(bindings)) {
      if (equal(entry, baseBindings[assetId])) continue;
      if (!object(entry) || typeof entry.media_id !== 'string' || !['image', 'video'].includes(String(entry.type))) throw new Error('Occurrence media preview cannot represent this registry binding');
      assets.push({ ...copy(entry), asset_id: assetId, object_id: entry.media_id });
    }
    return { ...occurrence, revision: { ...copy(occurrence.revision), runtime_playback_assets: assets, internal_timeline_revision: { ...copy(internal), timeline: copy(shot.internal_timeline) } } };
  });
  const { config } = projectCanonicalComposition({ ...prepared, occurrences, contract: { ...prepared.contract, parent_composition: copy(bundle.parent) } }, undefined, { clampToOccurrenceDuration: false });
  return buildDataFromCurrentRegistry(config, current, { registry: { assets: config.registry }, resolvedRegistry: config.registry });
}

