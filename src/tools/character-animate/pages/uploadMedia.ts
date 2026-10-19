import { requireCloudBackend } from '@/shared/lib/cloudBackend';

export async function uploadVideoWithPoster(_file: File): Promise<{ videoUrl: string; posterUrl: string }> {
  return requireCloudBackend('character-animate upload');
}
