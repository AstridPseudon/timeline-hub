import { access, mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { describe, expect, it } from 'vitest';
import { document } from '../__tests__/commitSessionEnvironment.ts';
import { producePreparedImageRequestFromPaths, type PreparedImageRequestInput } from './preparedImageRequestProducer.ts';

const SYNTHETIC_SELECTION = {
  asset: 'synthetic-image',
  generation_id: 'synthetic-generation',
  variant_id: 'synthetic-variant',
  object_id: `sha256:${'1'.repeat(64)}`,
  catalog_digest: `sha256:${'2'.repeat(64)}`,
} as const;

function input(selection: typeof SYNTHETIC_SELECTION | undefined = SYNTHETIC_SELECTION): PreparedImageRequestInput {
  return {
    projectId: 'project-commit',
    timelineId: 'timeline-commit',
    head: { revisionId: 'r0', publicationId: 'p0' },
    canonicalDocument: document(),
    preparedAsset: {
      assetKey: 'synthetic-image', mediaType: 'image', durationSeconds: null, source: 'registered',
      entry: { file: 'synthetic-image.png', type: 'image/png' }, mediaSelection: selection as typeof SYNTHETIC_SELECTION,
    },
    placement: { trackId: 'V1', at: 2 },
  };
}

describe('prepared image request producer fixture', () => {
  it('exports the real App semantic request before authority acceptance and refuses missing or malformed selections', async () => {
    const directory = await mkdtemp(join(process.env.TMPDIR ?? tmpdir(), 'app-prepared-image-'));
    const inputPath = join(directory, 'input.json');
    const outputPath = join(directory, 'output.json');
    const source = input();
    await writeFile(inputPath, JSON.stringify(source), 'utf8');

    await producePreparedImageRequestFromPaths(inputPath, outputPath);
    const exported = JSON.parse(await readFile(outputPath, 'utf8')) as {
      request: Record<string, unknown>; idempotency_key: string; request_body_sha256: string;
    };
    expect(exported.request).toMatchObject({
      api_version: 1, project_id: source.projectId, timeline_id: source.timelineId,
      base_revision_id: source.head.revisionId, base_publication_id: source.head.publicationId,
      label: 'Add media', steps: [{ label: 'Add media', intent: 'Add media', tags: [], command_ordinals: [0], patch: [] }],
      merge: 'fields', dry_run: false, source: { via: 'app' },
    });
    const command = (exported.request.commands as Array<Record<string, unknown>>)[0]!;
    expect(command).toMatchObject({ op: 'clip.add-media', select: 'parent', args: { media: SYNTHETIC_SELECTION } });
    expect((command.args as Record<string, unknown>).row).toMatchObject({
      id: 'clip-0', track: 'V1', at: 2, clipType: 'hold', hold: 5, asset: 'synthetic-image',
    });
    expect(exported.idempotency_key).toMatch(/^[0-9a-f-]{36}$/);
    expect(exported.request_body_sha256).toMatch(/^sha256:[0-9a-f]{64}$/);

    const missing = input(undefined);
    delete (missing.preparedAsset as { mediaSelection?: unknown }).mediaSelection;
    const missingPath = join(directory, 'missing.json');
    const missingOutput = join(directory, 'missing-output.json');
    await writeFile(missingPath, JSON.stringify(missing), 'utf8');
    await expect(producePreparedImageRequestFromPaths(missingPath, missingOutput)).rejects.toThrow('mediaSelection');
    await expect(access(missingOutput)).rejects.toThrow();

    const malformed = input({ ...SYNTHETIC_SELECTION, object_id: 'not-a-digest' } as typeof SYNTHETIC_SELECTION);
    const malformedPath = join(directory, 'malformed.json');
    const malformedOutput = join(directory, 'malformed-output.json');
    await writeFile(malformedPath, JSON.stringify(malformed), 'utf8');
    await expect(producePreparedImageRequestFromPaths(malformedPath, malformedOutput)).rejects.toThrow('malformed');
    await expect(access(malformedOutput)).rejects.toThrow();
  });
});
