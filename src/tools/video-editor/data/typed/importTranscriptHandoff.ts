import type { CommitDataOptions } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { buildDataFromCurrentRegistry } from '@/tools/video-editor/lib/timeline-save-utils.ts';
import { getPlayableAssetKind } from '@/tools/video-editor/lib/timeline-asset-plans.ts';
import type { SourceFrozenDataItem } from './envelope.ts';
import { reconcileTranscriptReferences } from './reconcileTranscriptReferences.ts';
import {
  normalizeTranscriptSource,
  TRANSCRIPT_SCHEMA_REF,
  type TranscriptSourceSegment,
} from './adaptTranscript.ts';

/** Stable error codes for the transcript panel's actionable import messages. */
export type TranscriptImportErrorCode =
  | 'invalid_json'
  | 'invalid_document'
  | 'invalid_content'
  | 'empty_transcript'
  | 'missing_asset_association'
  | 'invalid_asset_association'
  | 'asset_mismatch'
  | 'asset_not_found'
  | 'asset_not_media'
  | 'timeline_not_loaded';

export class TranscriptImportError extends Error {
  constructor(
    readonly code: TranscriptImportErrorCode,
    message: string,
  ) {
    super(message);
    this.name = 'TranscriptImportError';
  }
}

export interface TranscriptImportInput {
  /** JSON text from Astrid's transcript export, or an already parsed value. */
  document: string | unknown;
  /** Explicit association for legacy `{segments}` files without `assetId`. */
  associationAssetId?: string;
}

export interface TranscriptImportReceipt {
  assetId: string;
  sourceId: string;
  importedSegments: number;
  replacedSegments: number;
  replacedExistingSource: boolean;
}

export type TranscriptImportCallback = (input: TranscriptImportInput) => TranscriptImportReceipt;

export interface TranscriptImportHost {
  /** Read at invocation time so import always uses the latest canonical data. */
  dataRef: { current: TimelineData | null };
  /** The editor's existing history, dirty-state, and persistence entry point. */
  commitData: (nextData: TimelineData, options?: CommitDataOptions) => void;
}

interface ParsedTranscriptDocument {
  assetId?: string;
  sourceId?: string;
  segments: readonly TranscriptSourceSegment[];
}

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value);

const readOptionalId = (
  value: unknown,
  label: string,
): string | undefined => {
  if (value === undefined) return undefined;
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new TranscriptImportError('invalid_document', `${label} must be a non-empty string when provided.`);
  }
  return value.trim();
};

const readTime = (value: unknown, label: string): number => {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
    throw new TranscriptImportError('invalid_content', `${label} must be a finite, non-negative number of seconds.`);
  }
  return value;
};

const readTranscriptSegment = (value: unknown, index: number): TranscriptSourceSegment => {
  const label = `Segment ${index + 1}`;
  if (!isRecord(value)) {
    throw new TranscriptImportError('invalid_content', `${label} must be an object with start, end, and text fields.`);
  }
  const id = readOptionalId(value.id, `${label} id`);
  const start = readTime(value.start, `${label} start`);
  const end = readTime(value.end, `${label} end`);
  if (end < start) {
    throw new TranscriptImportError('invalid_content', `${label} end must be at or after its start.`);
  }
  if (typeof value.text !== 'string') {
    throw new TranscriptImportError('invalid_content', `${label} text must be a string.`);
  }
  if (value.speaker !== undefined && value.speaker !== null && typeof value.speaker !== 'string') {
    throw new TranscriptImportError('invalid_content', `${label} speaker must be a string or null.`);
  }

  let words: TranscriptSourceSegment['words'];
  if (value.words !== undefined) {
    if (!Array.isArray(value.words)) {
      throw new TranscriptImportError('invalid_content', `${label} words must be an array when provided.`);
    }
    words = value.words.map((wordValue: unknown, wordIndex) => {
      const wordLabel = `${label}, word ${wordIndex + 1}`;
      if (!isRecord(wordValue)) {
        throw new TranscriptImportError('invalid_content', `${wordLabel} must be an object with timing and text fields.`);
      }
      const wordId = readOptionalId(wordValue.id, `${wordLabel} id`);
      const wordStart = readTime(wordValue.start, `${wordLabel} start`);
      const wordEnd = readTime(wordValue.end, `${wordLabel} end`);
      if (wordEnd < wordStart) {
        throw new TranscriptImportError('invalid_content', `${wordLabel} end must be at or after its start.`);
      }
      if (wordValue.text !== undefined && typeof wordValue.text !== 'string') {
        throw new TranscriptImportError('invalid_content', `${wordLabel} text must be a string.`);
      }
      if (wordValue.word !== undefined && typeof wordValue.word !== 'string') {
        throw new TranscriptImportError('invalid_content', `${wordLabel} legacy word field must be a string.`);
      }
      if (wordValue.text === undefined && wordValue.word === undefined) {
        throw new TranscriptImportError('invalid_content', `${wordLabel} needs a text field.`);
      }
      if (wordValue.text !== undefined && wordValue.word !== undefined && wordValue.text !== wordValue.word) {
        throw new TranscriptImportError('invalid_content', `${wordLabel} has conflicting text and word fields.`);
      }
      return {
        ...(wordId !== undefined ? { id: wordId } : {}),
        start: wordStart,
        end: wordEnd,
        ...(wordValue.text !== undefined ? { text: wordValue.text } : {}),
        ...(wordValue.word !== undefined ? { word: wordValue.word } : {}),
      };
    });
  }

  return {
    ...(id !== undefined ? { id } : {}),
    start,
    end,
    text: value.text,
    ...(value.speaker !== undefined ? { speaker: value.speaker as string | null } : {}),
    ...(words !== undefined ? { words } : {}),
  };
};

const parseTranscriptDocument = (input: string | unknown): ParsedTranscriptDocument => {
  let value = input;
  if (typeof input === 'string') {
    try {
      value = JSON.parse(input) as unknown;
    } catch (error) {
      const detail = error instanceof Error ? error.message : 'Unknown JSON parse error';
      throw new TranscriptImportError(
        'invalid_json',
        `Transcript file is not valid JSON (${detail}). Choose an Astrid transcript.json export.`,
      );
    }
  }
  if (!isRecord(value)) {
    throw new TranscriptImportError('invalid_document', 'Transcript JSON must be an object containing a segments array.');
  }
  const assetId = readOptionalId(value.assetId, 'Transcript assetId');
  const sourceId = readOptionalId(value.sourceId, 'Transcript sourceId');
  if (!Array.isArray(value.segments)) {
    throw new TranscriptImportError('invalid_document', 'Transcript JSON must contain a segments array.');
  }
  if (value.segments.length === 0) {
    throw new TranscriptImportError(
      'empty_transcript',
      'This transcript contains no segments, so nothing was imported. Check the source export before replacing a transcript.',
    );
  }
  return {
    ...(assetId !== undefined ? { assetId } : {}),
    ...(sourceId !== undefined ? { sourceId } : {}),
    segments: value.segments.map(readTranscriptSegment),
  };
};

const resolveAssociatedAssetId = (
  documentAssetId: string | undefined,
  associationAssetId: string | undefined,
): string => {
  let association: string | undefined;
  if (associationAssetId !== undefined) {
    if (typeof associationAssetId !== 'string' || associationAssetId.trim().length === 0) {
      throw new TranscriptImportError(
        'invalid_asset_association',
        'The selected media association is empty. Choose a source audio or video asset in the editor and try again.',
      );
    }
    association = associationAssetId.trim();
  }
  if (documentAssetId && association && documentAssetId !== association) {
    throw new TranscriptImportError(
      'asset_mismatch',
      `This transcript names media asset “${documentAssetId}”, but the selected editor asset is “${association}”. Select the matching media or import a transcript for the selected asset.`,
    );
  }
  const assetId = documentAssetId ?? association;
  if (!assetId) {
    throw new TranscriptImportError(
      'missing_asset_association',
      'This transcript has no assetId. Select the source media in the editor and associate the transcript with that asset before importing.',
    );
  }
  return assetId;
};

const assertRegisteredTranscriptMedia = (data: TimelineData, assetId: string): void => {
  const entry = data.registry.assets?.[assetId];
  if (!entry) {
    throw new TranscriptImportError(
      'asset_not_found',
      `Media asset “${assetId}” is not registered in this timeline. Select an asset from this editor or add it before importing.`,
    );
  }
  const kind = getPlayableAssetKind(entry);
  const declaredKind = entry.type?.toLowerCase();
  if (kind !== 'audio' && kind !== 'video' && declaredKind !== 'audio' && declaredKind !== 'video') {
    throw new TranscriptImportError(
      'asset_not_media',
      `Asset “${assetId}” is not registered as audio or video media. Choose the source audio or video asset for this transcript.`,
    );
  }
};

const sourceIdFromItem = (item: SourceFrozenDataItem): unknown => {
  if (!isRecord(item.payload)) return undefined;
  return item.payload.sourceId;
};

/**
 * Build an editor-owned callback for importing Astrid transcript handoffs.
 * The callback re-reads current timeline data, replaces only the matching
 * `(assetId, sourceId)` transcript source, and commits through the existing
 * history and TimelineBundle persistence path.
 */
export function createTranscriptImportCallback({ dataRef, commitData }: TranscriptImportHost): TranscriptImportCallback {
  return ({ document, associationAssetId }) => {
    const current = dataRef.current;
    if (!current) {
      throw new TranscriptImportError('timeline_not_loaded', 'Timeline data is still loading. Try importing again after the editor is ready.');
    }

    const parsed = parseTranscriptDocument(document);
    const assetId = resolveAssociatedAssetId(parsed.assetId, associationAssetId);
    assertRegisteredTranscriptMedia(current, assetId);

    let normalized: readonly SourceFrozenDataItem[];
    try {
      normalized = normalizeTranscriptSource({
        assetId,
        ...(parsed.sourceId !== undefined ? { sourceId: parsed.sourceId } : {}),
        segments: parsed.segments,
      });
    } catch (error) {
      const detail = error instanceof Error ? error.message : 'Transcript segment validation failed';
      throw new TranscriptImportError('invalid_content', `Transcript content is invalid: ${detail}`);
    }

    const sourceId = parsed.sourceId ?? `transcript:${assetId}`;
    const existingForSchema = current.sourceItemsBySchemaRef?.[TRANSCRIPT_SCHEMA_REF] ?? [];
    const keptItems = existingForSchema.filter((item) => !(
      item.schemaRef === TRANSCRIPT_SCHEMA_REF
      && item.sourceArtifactRef.assetId === assetId
      && sourceIdFromItem(item) === sourceId
    ));
    const replacedSegments = existingForSchema.length - keptItems.length;
    const sourceItemsBySchemaRef = {
      ...(current.sourceItemsBySchemaRef ?? {}),
      [TRANSCRIPT_SCHEMA_REF]: [...keptItems, ...normalized],
    };

    const config = reconcileTranscriptReferences(current.config, existingForSchema, normalized, assetId, sourceId);
    const nextData = buildDataFromCurrentRegistry(config, current, { sourceItemsBySchemaRef });
    commitData(nextData, { save: true, semantic: true });

    return {
      assetId,
      sourceId,
      importedSegments: normalized.length,
      replacedSegments,
      replacedExistingSource: replacedSegments > 0,
    };
  };
}
