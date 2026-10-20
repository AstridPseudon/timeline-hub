import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  from: vi.fn(),
  toastError: vi.fn(),
  normalizeAndPresentError: vi.fn(),
  uploadImageToStorage: vi.fn(),
  generateClientThumbnail: vi.fn(),
  uploadImageWithThumbnail: vi.fn(),
  createGenerationForLocalFile: vi.fn(),
  cropImageToProjectAspectRatio: vi.fn(),
}));

vi.mock('@/integrations/supabase/client', () => ({
  getSupabaseClient: () => ({
    from: mocks.from,
  }),
}));

vi.mock('@/shared/components/ui/runtime/sonner', () => ({
  toast: {
    error: mocks.toastError,
  },
}));

vi.mock('@/shared/lib/errorHandling/runtimeError', () => ({
  normalizeAndPresentError: mocks.normalizeAndPresentError,
}));

vi.mock('@/shared/lib/media/imageUploader', () => ({
  uploadImageToStorage: mocks.uploadImageToStorage,
}));

vi.mock('@/shared/media/clientThumbnailGenerator', () => ({
  generateClientThumbnail: mocks.generateClientThumbnail,
  uploadImageWithThumbnail: mocks.uploadImageWithThumbnail,
}));

vi.mock('@/shared/lib/media/createGenerationFromFile', async () => {
  const actual = await vi.importActual<typeof import('@/shared/lib/media/createGenerationFromFile')>(
    '@/shared/lib/media/createGenerationFromFile',
  );
  return {
    ...actual,
    createGenerationForLocalFile: mocks.createGenerationForLocalFile,
  };
});

vi.mock('@/shared/lib/media/imageCropper', () => ({
  cropImageToProjectAspectRatio: mocks.cropImageToProjectAspectRatio,
}));

import { processDroppedImages } from './externalImageDrop';

function makeLargeFile(name = 'large.png'): File {
  const file = new File(['large'], name, { type: 'image/png' });
  Object.defineProperty(file, 'size', { value: 26 * 1024 * 1024 });
  return file;
}

function makeStubHandle(file: File): FileSystemFileHandle {
  return {
    kind: 'file',
    name: file.name,
    getFile: async () => file,
    isSameEntry: async () => false,
    // Persisted local handles must expose the permission methods; a bare
    // FileSystemFileHandle is intentionally not trusted for the local path.
    queryPermission: async () => 'granted',
    requestPermission: async () => 'granted',
  } as unknown as FileSystemFileHandle;
}

function createQueryResult(data: unknown) {
  return {
    select: vi.fn().mockReturnThis(),
    eq: vi.fn().mockReturnThis(),
    single: vi.fn().mockResolvedValue({ data }),
    insert: vi.fn().mockReturnThis(),
  };
}

function createInsertResult(data: unknown) {
  return {
    insert: vi.fn().mockReturnThis(),
    select: vi.fn().mockReturnThis(),
    single: vi.fn().mockResolvedValue({ data, error: null }),
  };
}

function createInsertOnlyResult() {
  return {
    insert: vi.fn().mockResolvedValue({ error: null }),
  };
}

describe('processDroppedImages', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.generateClientThumbnail.mockResolvedValue({
      thumbnailBlob: new Blob(['thumb'], { type: 'image/jpeg' }),
    });
    mocks.uploadImageWithThumbnail.mockResolvedValue({
      imageUrl: 'https://example.com/image.png',
      thumbnailUrl: 'https://example.com/thumb.png',
    });
    mocks.uploadImageToStorage.mockResolvedValue('https://example.com/image.png');
    mocks.from.mockImplementation((table: string) => {
      if (table === 'projects') {
        return createQueryResult({ aspect_ratio: null, settings: null });
      }
      if (table === 'shots') {
        return createQueryResult({ aspect_ratio: null });
      }
      if (table === 'generations') {
        return createInsertResult({
          id: 'gen-1',
          location: 'https://example.com/image.png',
          thumbnail_url: 'https://example.com/thumb.png',
          type: 'image',
          created_at: '2026-04-06T00:00:00.000Z',
          params: {
            source: 'upload',
            original_filename: 'frame.png',
            file_type: 'image/png',
            file_size: 3,
          },
          primary_variant_id: null,
        });
      }
      if (table === 'generation_variants') {
        return createInsertOnlyResult();
      }
      return createQueryResult(null);
    });
  });

  it('rejects in Astrid before the internal crop/read wrapper touches Supabase', async () => {
    const createShot = vi.fn();

    await expect(processDroppedImages({
      variables: {
        imageFiles: [new File(['img'], 'one.png', { type: 'image/png' })],
        targetShotId: 'shot-1',
        currentProjectQueryKey: 'project-1',
        currentShotCount: 1,
      },
      projectId: 'project-1',
      createShot,
      addImageToShot: vi.fn(),
      addImageToShotWithoutPosition: vi.fn(),
    })).rejects.toMatchObject({ code: 'capability_unavailable' });

    expect(mocks.from).not.toHaveBeenCalled();
    expect(createShot).not.toHaveBeenCalled();
    expect(mocks.uploadImageToStorage).not.toHaveBeenCalled();
  });
});
