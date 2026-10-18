import type { AssetRegistryEntry } from '@/tools/video-editor/types/index.ts';
import type { GenerationRow } from '@/domains/generation/types/index.ts';
import { fetchGenerationById } from '@/integrations/supabase/repositories/generationRepository.ts';
import type { DataProvider } from '@/tools/video-editor/data/DataProvider.ts';
import type { SelectedProjectMediaIdentity } from '@/shared/contracts/selectedProjectMedia.ts';
import type { MutationReceipt } from '@/integrations/runtime/generated.ts';
import { readSelectedProjectMediaIdentity } from '@/tools/video-editor/commands/selectedProjectMedia.ts';
import { canonicalJsonStringify } from '@/tools/video-editor/data/typed/timelineBundle.ts';

export interface DuplicatedGenerationAsset {
  generationId: string;
  variantId: string;
  variantType: 'image' | 'video';
  imageUrl: string;
  thumbUrl: string;
  /** Required before timeline placement. Selection APIs do not acquire this.
   * The current unavailable adapter never returns a registered acquisition. */
  registeredAsset?: { projectId: string; assetId: string; entry: AssetRegistryEntry };
  selectedMedia: SelectedProjectMediaIdentity;
  acquisitionReceipt: MutationReceipt;
}

/** Metadata acquisition through the selected authenticated Runtime provider. */
export async function duplicateGenerationAsset(params: {
  projectId: string;
  source: SelectedProjectMediaIdentity;
  idempotencyKey: string;
  provider: DataProvider;
}): Promise<DuplicatedGenerationAsset> {
  if (!params.provider.duplicateProjectGeneration) throw new Error('Selected provider does not support generation duplication.');
  const result = await params.provider.duplicateProjectGeneration({ projectId: params.projectId,
    source: params.source, idempotencyKey: params.idempotencyKey });
  const selection = readSelectedProjectMediaIdentity(result.selection);
  const kind = result.entry.media_type.split('/')[0];
  if (!selection || !['image', 'video'].includes(kind)
    || result.generation.project_id !== params.projectId || result.generation.status !== 'completed'
    || selection.generation_id !== result.generation.generation_id || selection.variant_id !== result.variant.variant_id
    || result.variant.generation_id !== selection.generation_id || selection.object_id !== result.variant.object_id
    || selection.object_id !== result.entry.object_id || selection.object_id !== params.source.object_id
    || selection.generation_id === params.source.generation_id || selection.variant_id === params.source.variant_id
    || result.receipt?.command_kind !== 'generation.duplicate' || result.receipt.project_id !== params.projectId
    || result.receipt.idempotency_key !== params.idempotencyKey
    || canonicalJsonStringify((result.generation.metadata.runtime_metadata_copy as { source?: unknown })?.source)
      !== canonicalJsonStringify(params.source)) throw new Error('Runtime returned an inconsistent generation acquisition.');
  return { generationId: selection.generation_id, variantId: selection.variant_id, variantType: kind as 'image' | 'video',
    imageUrl: '', thumbUrl: '', selectedMedia: result.selection, acquisitionReceipt: result.receipt,
    registeredAsset: { projectId: params.projectId, assetId: selection.asset, entry: {
      media_id: selection.object_id, content_sha256: selection.object_id.slice(7), type: result.entry.media_type,
      generationId: selection.generation_id, variantId: selection.variant_id,
      duration: result.entry.duration_seconds, format: result.entry,
    } } };
}

/** Gallery detail is part of the frozen bridge route set. */
export async function loadGenerationForLightbox(generationId: string): Promise<GenerationRow | null> {
  return await fetchGenerationById(generationId);
}
