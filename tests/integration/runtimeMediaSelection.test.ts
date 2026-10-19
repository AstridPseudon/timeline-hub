import { expect, it } from 'vitest';
import { RuntimeDataProvider } from '../../src/integrations/runtime/dataProvider.ts';
import type { ManagedOutput, MediaImportOperation, MediaSelection, MediaSelectionQuery, Transport } from '../../src/integrations/runtime/generated.ts';
import { ASTRID_PYTHON, revisionSet } from '../e2e/local/support/astrid.ts';
import { DirectHarness, makePng, sha256Hex } from '../e2e/local/support/harness.ts';

it('M2 App media selection reads exact settled imports through the real Runtime door without timeline writes', async () => {
  const harness = new DirectHarness();
  try {
    await harness.start();
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);
    const health = await harness.runtimeJson('GET', '/v1/health');
    console.info('Media selection integration source tuple:', {
      ...revisionSet(), runtimeSchemaDigest: health.body.schema_digest,
    });
    const { projectId, timelineId, headRevisionId } = harness.seed;
    const projectPath = `/v1/projects/${projectId}`;
    const timelinePath = `${projectPath}/timelines/${timelineId}`;
    const wire: Array<{ method: string; path: string; status: number; response: unknown }> = [];
    const transport: Transport = async (method, path, headers, body) => {
      const bytes = body instanceof Blob ? Buffer.from(await body.arrayBuffer()) : body ? Buffer.from(body) : undefined;
      const response = await harness.doorRequest(path, { method, headers, body: bytes });
      wire.push({ method, path, status: response.status, response: response.json() });
      return { status: response.status, headers: {}, body: new Uint8Array(response.body) };
    };
    const providerFor = (projectId: string) => new RuntimeDataProvider({ projectId, baseUrl: harness.doorBase, transport });
    const provider = providerFor(projectId);
    const before = await provider.loadTimelineCommandBasis(timelineId);
    const timelineBytes = async () => {
      const responses = await Promise.all([
        timelinePath,
        `${timelinePath}/composition-revisions/${headRevisionId}`,
        `${timelinePath}/commits?limit=50`,
      ].map((path) => harness.doorRequest(path)));
      for (const response of responses) expect(response.status, response.text).toBe(200);
      return responses.map((response) => response.body);
    };
    const beforeBytes = await timelineBytes();
    try {
      const png = makePng();
      const imported = await provider.prepareMediaImport(new File([new Uint8Array(png)], 'selection.png', { type: 'image/png' }), {
        width: 64, height: 48, expectedDigest: sha256Hex(png),
      });
      expect(imported.assetId).toBe(sha256Hex(png));
      expect(imported.entry).toMatchObject({
        media_id: imported.assetId, content_sha256: imported.assetId,
        generationId: imported.generationId, variantId: imported.variantId,
      });
      const descriptor = await harness.runtimeJson<MediaImportOperation>('GET', `${projectPath}/media-imports/${imported.importOperationId}`);
      expect(descriptor.status).toBe(200);
      expect(descriptor.body).toMatchObject({ status: 'completed', generation_id: imported.generationId, variant_id: imported.variantId });
      const outputs = await harness.runtimeJson<{ items: ManagedOutput[] }>('GET', `/v1/tasks/${descriptor.body.task_id}/managed-outputs`);
      expect(outputs.status).toBe(200);
      expect(outputs.body.items).toHaveLength(1);
      const association = outputs.body.items[0];
      expect(association).toMatchObject({ project_id: projectId, object_id: imported.assetId, durability: 'durable', state: 'available' });
      const explicit: MediaSelectionQuery = {
        asset: imported.variantId, generation_id: imported.generationId, variant_id: imported.variantId,
      };
      const managed: MediaSelectionQuery = {
        association_id: association.association_id, object_id: imported.assetId, version: association.version,
      };

      const selected = await provider.getProjectMediaSelection(explicit);
      const nativeMediaSelection = wire.at(-1)!;
      expect(nativeMediaSelection).toMatchObject({ method: 'GET', status: 200 });
      expect(nativeMediaSelection.path).toBe(`${projectPath}/media-selection?asset=${encodeURIComponent(imported.variantId)}&generation_id=${encodeURIComponent(imported.generationId)}&variant_id=${encodeURIComponent(imported.variantId)}`);
      expect(selected).toEqual(nativeMediaSelection.response);
      expect(selected).toEqual({
        ...explicit, object_id: imported.assetId, catalog_digest: expect.stringMatching(/^sha256:[0-9a-f]{64}$/),
      });
      await expect(provider.getProjectMediaSelection(managed)).resolves.toEqual(selected);
      const captured: MediaSelection = { ...selected };

      // A new catalog item has its own primary; it must never replace the exact older selection.
      const newer = await provider.prepareMediaImport(new File([new Uint8Array(makePng(32, 24))], 'newer.png', { type: 'image/png' }), {
        width: 32, height: 24,
      });
      expect(newer.generationId).not.toBe(imported.generationId);
      expect(newer.variantId).not.toBe(imported.variantId);
      expect(newer.assetId).not.toBe(imported.assetId);
      const primary = await harness.runtimeJson('GET', `/v1/variants/${newer.variantId}`);
      expect(primary.status).toBe(200);
      expect(primary.body.metadata.is_primary).toBe(true);
      const viewed = await harness.runtimeJson('POST', `/v1/variants/${imported.variantId}/viewed`, {});
      expect(viewed.status).toBe(200);
      await expect(provider.getProjectMediaSelection(explicit)).resolves.toEqual(captured);
      await expect(provider.getProjectMediaSelection(managed)).resolves.toEqual(captured);

      const refuse = async (consumer: RuntimeDataProvider, query: MediaSelectionQuery, status: number, code: string) => {
        const start = wire.length;
        await expect(consumer.getProjectMediaSelection(query)).rejects.toMatchObject({ status, code });
        // Refusals must reach the real door once, without a catalog/latest fallback.
        expect(wire.slice(start).filter(({ path }) => path.includes('/media-selection?'))).toHaveLength(1);
        expect(wire.at(-1)).toMatchObject({ method: 'GET', status, response: { code } });
        expect(wire.slice(start).every(({ path }) => path.includes('/media-selection?')
          || ['/v1/health', '/v1/handshake', '/v1/realm'].includes(path))).toBe(true);
      };
      await refuse(provider, { ...explicit, variant_id: 'missing-variant' }, 404, 'not_found');
      await refuse(provider, { ...explicit, generation_id: newer.generationId }, 404, 'not_found');
      await refuse(provider, { ...managed, association_id: 'missing-association' }, 404, 'not_found');
      await refuse(provider, { ...managed, object_id: newer.assetId }, 409, 'conflict');
      const foreign = await harness.runtimeJson('POST', '/v1/projects', { name: 'Foreign selection' });
      expect(foreign.status).toBe(201);
      const foreignProvider = providerFor(foreign.body.data.project_id);
      await refuse(foreignProvider, explicit, 404, 'not_found');
      await refuse(foreignProvider, managed, 404, 'not_found');

      // Capture, then change lifecycle through its normal API: a deterministic stale-read race.
      const pinned = await harness.runtimeJson('POST', `/v1/managed-outputs/${association.association_id}/lifecycle`, {
        operation: 'pin', expected_version: association.version,
      });
      expect(pinned.status).toBe(200);
      expect(pinned.body.data.version).toBe(association.version + 1);
      await refuse(provider, managed, 409, 'conflict');
      const refreshed = await provider.getProjectMediaSelection({ ...managed, version: pinned.body.data.version });
      expect(refreshed).toMatchObject(explicit);
      expect(refreshed.object_id).toBe(captured.object_id);
      // Lifecycle is part of Runtime's catalog basis; its change must change this pin.
      expect(refreshed.catalog_digest).not.toBe(captured.catalog_digest);
      await expect(provider.getProjectMediaSelection(explicit)).resolves.toEqual(refreshed);
      expect(selected).toEqual(captured);
      console.info('nativeMediaSelection passed:', { explicit, managed, captured, refreshed });
    } finally {
      expect(await provider.loadTimelineCommandBasis(timelineId)).toEqual(before);
      expect(await timelineBytes()).toEqual(beforeBytes);
      expect(wire.filter(({ method, path }) => method !== 'GET' && path !== '/v1/handshake'
        && path !== `${projectPath}/media-imports`)).toEqual([]);
      expect(harness.audit().filter(({ method, path }) => method !== 'GET' && /\/timelines\//.test(path))).toEqual([]);
    }
  } finally {
    await harness.stop();
  }
});
