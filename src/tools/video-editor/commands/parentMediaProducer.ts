import type {
  MediaSelection,
  MediaSelectionQuery,
  VerifiedMedia,
} from '@/integrations/runtime/timeline-commit-types.ts';
import {
  ClipMoveError,
  copy,
  equal,
  freezeJson,
  object,
} from './clipMovePrimitives.ts';
import {
  captureParentClipAddMedia,
  finishParentClipAddMedia,
  type ParentClipAddMediaBasis,
} from './parentClipAddCapture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';

type Row = Record<string, JSON>;

/** The two existing immutable Runtime reads needed by parent media capture. */
export interface ParentMediaReadCapability {
  getProjectMediaSelection(projectId: string, query: MediaSelectionQuery): Promise<MediaSelection>;
  getProjectVerifiedMedia(projectId: string, selection: MediaSelection): Promise<VerifiedMedia>;
}

export type ParentMediaProducerInput = {
  readonly projectId: string;
  readonly bundle: AuthoredBundle;
  readonly row: Row;
  readonly selectionQuery: MediaSelectionQuery;
};

export type ParentMediaProducerBasis = ParentClipAddMediaBasis & {
  readonly selectionQuery: MediaSelectionQuery;
};

function requireCapability(capability: ParentMediaReadCapability | undefined): ParentMediaReadCapability {
  if (!capability || typeof capability.getProjectMediaSelection !== 'function' ||
    typeof capability.getProjectVerifiedMedia !== 'function') {
    throw new ClipMoveError('parent media producer requires immutable Runtime selection and verification reads', 'unsupported_media');
  }
  return capability;
}

/** Capture the immutable selection and detached verification exactly once. */
export async function captureParentClipAddMediaFromRuntime(
  capability: ParentMediaReadCapability | undefined,
  input: ParentMediaProducerInput,
): Promise<ParentMediaProducerBasis> {
  const reads = requireCapability(capability);
  const selectionQuery = copy(input.selectionQuery);
  const media = await reads.getProjectMediaSelection(input.projectId, selectionQuery);
  const verifiedMedia = await reads.getProjectVerifiedMedia(input.projectId, media);
  if (!object(verifiedMedia) || !equal(verifiedMedia.selection, media)) {
    throw new ClipMoveError('parent media verification does not match the captured selection', 'dependency_changed');
  }
  const basis = captureParentClipAddMedia(input.bundle, input.row, media, [verifiedMedia]);
  return freezeJson({ ...basis, selectionQuery });
}

/** Retry from the frozen original bundle, command, selection, and verification. */
export function finishParentClipAddMediaFromBasis(basis: ParentMediaProducerBasis): {
  command: EditCommand;
  bundle: AuthoredBundle;
} {
  const result = finishParentClipAddMedia(basis);
  return { command: result.command, bundle: result.bundle };
}
