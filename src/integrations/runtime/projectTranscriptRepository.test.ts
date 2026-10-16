import { afterEach, describe, expect, it, vi } from 'vitest';
import { ReighRuntimeClient } from './client.ts';
import { RuntimeDataProvider } from './dataProvider.ts';
import {
  transcriptDocumentId,
  type ProjectTranscriptContent,
  type ProjectTranscriptDocument,
} from '@/tools/video-editor/data/typed/projectTranscript.ts';
const media = 'sha256:' + 'a'.repeat(64);
const content: ProjectTranscriptContent = {
  schema: 'media.transcript/v1',
  media_id: media,
  source_id: 'default',
  segments: [{ id: 'segment', start: 0, end: 1, text: 'text' }],
};
async function document(
  source = 'default',
): Promise<ProjectTranscriptDocument> {
  return {
    document_id: await transcriptDocumentId('p', media, source),
    project_id: 'p',
    kind: 'media.transcript',
    content: { ...content, source_id: source },
    version: 1,
    created_at: 'now',
    updated_at: 'now',
  };
}
afterEach(() => vi.restoreAllMocks());
describe('Runtime project transcript repository', () => {
  it('uses kind-filtered pagination and validates every returned canonical document', async () => {
    const a = await document(),
      b = await document('other');
    const list = vi
      .spyOn(ReighRuntimeClient.prototype, 'listDocuments')
      .mockResolvedValueOnce({ items: [a], next_cursor: 'page-2' })
      .mockResolvedValueOnce({ items: [b], next_cursor: null });
    const port = new RuntimeDataProvider({ projectId: 'p' }).projectTranscripts;
    expect(port.projectId).toBe('p');
    expect(await port.listForMedia(media)).toEqual([a, b]);
    expect(list.mock.calls).toEqual([
      ['p', undefined, 100, 'media.transcript'],
      ['p', 'page-2', 100, 'media.transcript'],
    ]);
  });
  it('passes expected document version and a stable attempt key using ordinary document transport', async () => {
    const d = await document();
    const create = vi
      .spyOn(ReighRuntimeClient.prototype, 'createDocument')
      .mockResolvedValue({ ...d, receipt: {} as any });
    const update = vi
      .spyOn(ReighRuntimeClient.prototype, 'updateDocument')
      .mockResolvedValue({ ...d, version: 2, receipt: {} as any });
    const port = new RuntimeDataProvider({ projectId: 'p' }).projectTranscripts;
    await port.create(content, 'create-key');
    await port.update(d.document_id, content, 1, 'update-key');
    expect(create).toHaveBeenCalledWith(
      'p',
      d.document_id,
      'media.transcript',
      content,
      'create-key',
    );
    expect(update).toHaveBeenCalledWith(
      'p',
      d.document_id,
      1,
      content,
      'update-key',
    );
  });
  it('fails closed on wrong project, identity, malformed rich content and repeated pagination', async () => {
    const d = await document();
    const get = vi.spyOn(ReighRuntimeClient.prototype, 'getDocument');
    const port = new RuntimeDataProvider({ projectId: 'p' }).projectTranscripts;
    get.mockResolvedValueOnce({ ...d, project_id: 'other' });
    await expect(port.get(d.document_id)).rejects.toThrow('authority');
    get.mockResolvedValueOnce({ ...d, document_id: 'transcript:wrong' });
    await expect(port.get(d.document_id)).rejects.toThrow('identity');
    get.mockResolvedValueOnce({
      ...d,
      content: {
        ...content,
        segments: [{ id: 's', start: 2, end: 1, text: 'bad' }],
      },
    });
    await expect(port.get(d.document_id)).rejects.toThrow();
    vi.spyOn(ReighRuntimeClient.prototype, 'listDocuments').mockResolvedValue({
      items: [d],
      next_cursor: 'same',
    });
    await expect(port.listForMedia(media)).rejects.toThrow('repeated');
  });
});
