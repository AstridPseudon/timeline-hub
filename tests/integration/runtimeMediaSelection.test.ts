import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { expect, it } from 'vitest';
import { RuntimeDataProvider } from '../../src/integrations/runtime/dataProvider.ts';
import type { ManagedOutput, MediaImportOperation, MediaSelection, MediaSelectionQuery, Transport } from '../../src/integrations/runtime/generated.ts';
import type { VerifiedMedia } from '../../src/integrations/runtime/timeline-commit-types.ts';
import { ASTRID_PYTHON, revisionSet } from '../e2e/local/support/astrid.ts';
import { DirectHarness, makePng, runtimePython, sha256Hex } from '../e2e/local/support/harness.ts';

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
    const database = path.join(harness.realmDir, 'realm.sqlite3');
    const sqlSnapshot = (timelineOnly = false) => execFileSync(runtimePython()!, ['-c', `
import json, sqlite3, sys
from pathlib import Path
with sqlite3.connect(Path(sys.argv[1]).as_uri() + '?mode=ro', uri=True) as conn:
    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    if sys.argv[2] == 'timeline':
        tables = [name for name in tables if any(part in name for part in ('timeline', 'composition', 'revision', 'publication'))]
    print(json.dumps({name: conn.execute('SELECT * FROM "' + name.replace('"', '""') + '"').fetchall()
                      for name in tables}, sort_keys=True, default=repr))
`, database, timelineOnly ? 'timeline' : 'all'], { encoding: 'utf8' });
    const beforeTimelineSql = sqlSnapshot(true);
    const unchangedRead = async <T>(read: () => Promise<T>): Promise<T> => {
      const beforeSql = sqlSnapshot();
      try {
        return await read();
      } finally {
        expect(sqlSnapshot()).toEqual(beforeSql);
      }
    };
    const refuseVerified = async (consumer: RuntimeDataProvider, pin: MediaSelection, status: number, code: string) => {
      const captured = structuredClone(pin);
      const start = wire.length;
      await unchangedRead(async () => {
        await expect(consumer.getProjectVerifiedMedia(pin)).rejects.toMatchObject({ status, code });
      });
      expect(pin).toEqual(captured);
      expect(wire.slice(start).filter(({ path }) => path.includes('/media-selection/verified?'))).toHaveLength(1);
      expect(wire.at(-1)).toMatchObject({ method: 'GET', status, response: { code } });
      expect(wire.slice(start).every(({ path }) => path.includes('/media-selection/verified?')
        || ['/v1/health', '/v1/handshake', '/v1/realm'].includes(path))).toBe(true);
    };
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
      const verifiedImage = await unchangedRead(() => provider.getProjectVerifiedMedia(captured));
      expect(verifiedImage).toEqual({ selection: captured, media_type: 'image/png', size: png.length, width: 64, height: 48 });
      expect(wire.at(-1)).toMatchObject({ method: 'GET', status: 200, response: verifiedImage });
      expect(wire.at(-1)!.path).toBe(`${projectPath}/media-selection/verified?${Object.entries(captured)
        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`).join('&')}`);
      const alias = await provider.getProjectMediaSelection({ ...explicit, asset: 'popup/image 音 + original' });
      await expect(unchangedRead(() => provider.getProjectVerifiedMedia(alias))).resolves.toEqual({ ...verifiedImage, selection: alias });
      expect(alias.asset).toBe('popup/image 音 + original');

      // Positive inputs use ordinary public media imports, including actual decodable old/new video bytes.
      const videoInputs: Array<{ pin: MediaSelection; media: VerifiedMedia; associationQuery: MediaSelectionQuery; output: ManagedOutput }> = [];
      for (const [name, color] of [['old', 'blue'], ['new', 'red']]) {
        const filename = path.join(harness.tmp, `${name}.mp4`);
        execFileSync('ffmpeg', ['-v', 'error', '-f', 'lavfi', '-i', `color=c=${color}:s=16x16:r=10`,
          '-t', '2', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-y', filename], { timeout: 60_000 });
        const bytes = readFileSync(filename);
        const duration = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
          '-of', 'default=noprint_wrappers=1:nokey=1', filename], { encoding: 'utf8', timeout: 10_000 }).trim());
        expect(duration).toBe(2);
        const importedVideo = await provider.prepareMediaImport(new File([new Uint8Array(bytes)], `${name}.mp4`, { type: 'video/mp4' }), {
          width: 16, height: 16, durationSeconds: duration, expectedDigest: sha256Hex(bytes),
        });
        const operation = await harness.runtimeJson<MediaImportOperation>('GET', `${projectPath}/media-imports/${importedVideo.importOperationId}`);
        expect(operation.status).toBe(200);
        expect(operation.body).toMatchObject({ status: 'completed', generation_id: importedVideo.generationId, variant_id: importedVideo.variantId });
        const settled = await harness.runtimeJson<{ items: ManagedOutput[] }>('GET', `/v1/tasks/${operation.body.task_id}/managed-outputs`);
        expect(settled.status).toBe(200);
        expect(settled.body.items).toHaveLength(1);
        const output = settled.body.items[0];
        expect(output).toMatchObject({ project_id: projectId, object_id: sha256Hex(bytes), durability: 'durable', state: 'available' });
        const associationQuery: MediaSelectionQuery = { association_id: output.association_id, object_id: output.object_id, version: output.version };
        const associationPin = await provider.getProjectMediaSelection(associationQuery);
        await expect(unchangedRead(() => provider.getProjectVerifiedMedia(associationPin))).resolves.toMatchObject({ selection: associationPin, duration_seconds: duration });
        const query: MediaSelectionQuery = { asset: `popup/${name} 音 + original`, generation_id: importedVideo.generationId, variant_id: importedVideo.variantId };
        const pin = await provider.getProjectMediaSelection(query);
        const media = await unchangedRead(() => provider.getProjectVerifiedMedia(pin));
        expect(media).toEqual({ selection: pin, media_type: 'video/mp4', size: bytes.length, duration_seconds: duration, width: 16, height: 16 });
        expect(pin.asset).toBe(query.asset);
        videoInputs.push({ pin, media, associationQuery, output });
      }
      const [oldVideo, newVideo] = videoInputs;
      expect(oldVideo.pin.object_id).not.toBe(newVideo.pin.object_id);
      const swap = { old_media: oldVideo.pin, media: newVideo.pin, row: { from: 0.5, to: 1.5, hold: 1 } };
      const originalSwap = structuredClone(swap);
      const detached = await Promise.all([swap.old_media, swap.media].map((pin) => unchangedRead(() => provider.getProjectVerifiedMedia(pin))));
      expect(detached).toEqual([oldVideo.media, newVideo.media]);
      expect(detached.every((media) => media.duration_seconds! >= swap.row.to)).toBe(true);
      expect(swap).toEqual(originalSwap);

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
      await expect(unchangedRead(() => provider.getProjectVerifiedMedia(captured))).resolves.toEqual(verifiedImage);

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
      await refuseVerified(foreignProvider, oldVideo.pin, 404, 'not_found');
      await refuseVerified(provider, { ...oldVideo.pin, object_id: newVideo.pin.object_id }, 404, 'not_found');
      await refuseVerified(provider, { ...oldVideo.pin, catalog_digest: `sha256:${'0'.repeat(64)}` }, 409, 'conflict');

      // Negative catalog race after successful settlement: changed intrinsic metadata must refuse the captured pin.
      execFileSync(runtimePython()!, ['-c', `
import json, sqlite3, sys
with sqlite3.connect(sys.argv[1]) as conn:
    metadata = json.loads(conn.execute('SELECT metadata_json FROM generations WHERE id=?', (sys.argv[2],)).fetchone()[0])
    metadata['params']['duration_seconds'] = 3
    conn.execute('UPDATE generations SET metadata_json=? WHERE id=?', (json.dumps(metadata), sys.argv[2]))
`, database, oldVideo.pin.generation_id]);
      await refuseVerified(provider, oldVideo.pin, 409, 'conflict');
      expect(swap).toEqual(originalSwap);

      const videoPinned = await harness.runtimeJson('POST', `/v1/managed-outputs/${newVideo.output.association_id}/lifecycle`, {
        operation: 'pin', expected_version: newVideo.output.version,
      });
      expect(videoPinned.status).toBe(200);
      await refuse(provider, newVideo.associationQuery, 409, 'conflict');
      await refuseVerified(provider, newVideo.pin, 409, 'conflict');
      expect(swap).toEqual(originalSwap);

      // Capture, then change lifecycle through its normal API: a deterministic stale-read race.
      const pinned = await harness.runtimeJson('POST', `/v1/managed-outputs/${association.association_id}/lifecycle`, {
        operation: 'pin', expected_version: association.version,
      });
      expect(pinned.status).toBe(200);
      expect(pinned.body.data.version).toBe(association.version + 1);
      await refuse(provider, managed, 409, 'conflict');
      await refuseVerified(provider, captured, 409, 'conflict');
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
      expect(sqlSnapshot(true)).toEqual(beforeTimelineSql);
      expect(wire.filter(({ method, path }) => method !== 'GET' && path !== '/v1/handshake'
        && path !== `${projectPath}/media-imports`)).toEqual([]);
      expect(harness.audit().filter(({ method, path }) => method !== 'GET' && /\/timelines\//.test(path))).toEqual([]);
    }
  } finally {
    await harness.stop();
  }
});
