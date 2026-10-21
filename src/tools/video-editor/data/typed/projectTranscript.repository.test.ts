import { describe, expect, it, vi } from 'vitest';
import type { ProjectDocumentSurface } from '@/sdk/context.ts';
import {
  parseProjectTranscriptDocument,
  transcriptDocumentId,
  transcriptDocumentPin,
  transcriptRepositoryFromDocuments,
  type ProjectTranscriptDocument,
} from './projectTranscript.ts';

const digest = `sha256:${'d'.repeat(64)}`;
const makeDocument = async (mediaId: string, sourceId: string, contentDigest?: string): Promise<ProjectTranscriptDocument> => ({
  document_id: await transcriptDocumentId('project', mediaId, sourceId),
  project_id: 'project',
  kind: 'media.transcript',
  content: {
    schema: 'media.transcript/v1', media_id: mediaId, source_id: sourceId,
    segments: [{ id: sourceId, start: 0, end: 1, text: sourceId }],
  },
  version: 1,
  created_at: 'now',
  updated_at: 'now',
  ...(contentDigest === undefined ? {} : { content_digest: contentDigest }),
});

describe('project transcript document listing', () => {
  it('paginates the transcript kind and validates every document before returning it', async () => {
    const a = await makeDocument(`sha256:${'a'.repeat(64)}`, 'narration');
    const b = await makeDocument(`sha256:${'b'.repeat(64)}`, 'voice');
    const list = vi.fn(async (_kind: string, page?: { cursor?: string; limit?: number }) =>
      page?.cursor ? { items: [b], next_cursor: null } : { items: [a], next_cursor: 'next' });
    const documents = { list } as unknown as ProjectDocumentSurface;
    const repo = transcriptRepositoryFromDocuments(documents, 'project');
    expect(await repo.listAll()).toEqual([a, b]);
    expect(list.mock.calls).toEqual([
      ['media.transcript', { cursor: undefined, limit: 100 }],
      ['media.transcript', { cursor: 'next', limit: 100 }],
    ]);
    list.mockImplementationOnce(async () => ({ items: [{ ...a, document_id: 'wrong' }], next_cursor: null }));
    await expect(repo.listAll()).rejects.toThrow(/identity/);
  });

  it('carries the server digest through every ordinary repository result and maps the exact original P1 pin', async () => {
    const p1 = await makeDocument(`sha256:${'a'.repeat(64)}`, 'narration', digest);
    const documents = {
      list: vi.fn(async () => ({ items: [p1], next_cursor: null })),
      get: vi.fn(async () => p1),
      create: vi.fn(async () => p1),
      update: vi.fn(async () => ({ ...p1, version: 2 })),
      onChange: vi.fn(() => () => undefined),
    } as unknown as ProjectDocumentSurface;
    const repo = transcriptRepositoryFromDocuments(documents, 'project');

    await expect(repo.listAll()).resolves.toEqual([p1]);
    await expect(repo.get(p1.document_id)).resolves.toEqual(p1);
    await expect(repo.create(p1.content, 'create')).resolves.toEqual(p1);
    await expect(repo.update(p1.document_id, p1.content, 1, 'update')).resolves.toMatchObject({
      document_id: p1.document_id,
      version: 2,
      content_digest: digest,
    });
    expect(transcriptDocumentPin(p1)).toEqual({
      document_id: p1.document_id,
      version: 1,
      content_digest: digest,
    });
    expect(Object.keys(p1)).toContain('content_digest');
  });

  it('accepts an old replay without a digest but leaves native association without a pin', async () => {
    const old = await makeDocument(`sha256:${'b'.repeat(64)}`, 'legacy');
    const parsed = await parseProjectTranscriptDocument(old, 'project');

    expect(parsed).not.toHaveProperty('content_digest');
    expect(transcriptDocumentPin(parsed)).toBeUndefined();
  });

  it('rejects null or malformed digest fields while preserving valid digest key presence', async () => {
    const old = await makeDocument(`sha256:${'c'.repeat(64)}`, 'narration');
    await expect(parseProjectTranscriptDocument({ ...old, content_digest: null }, 'project')).rejects.toThrow();
    await expect(parseProjectTranscriptDocument({ ...old, content_digest: 'sha256:not-a-digest' }, 'project')).rejects.toThrow();

    const recovered = await parseProjectTranscriptDocument({ ...old, content_digest: digest }, 'project');
    expect(Object.hasOwn(recovered, 'content_digest')).toBe(true);
    expect(transcriptDocumentPin(recovered)).toEqual({
      document_id: recovered.document_id,
      version: recovered.version,
      content_digest: digest,
    });
  });
});
