import type { Json } from '@/shared/types/json';

/** The `generations` row an upload returns: the columns the drop and gallery flows read. */
export interface UploadedGenerationRow {
  id: string;
  location: string | null;
  thumbnail_url: string | null;
  type: string | null;
  created_at: string;
  params: Json | null;
  primary_variant_id: string | null;
}
