import assert from 'node:assert/strict';
import type { Page, Response } from '@playwright/test';
import type { ManagedOutput, ObjectLocation } from '../../../../src/integrations/runtime/generated';
import { mediaHash } from './media';

interface FetchRead {
  url: string;
  method: string;
  resourceType: string;
  status: number;
  range?: string;
  origin?: string;
  redirected: boolean;
}

export interface DownloadTransfer {
  runtimeBase: string;
  pageOrigin: string;
  location: FetchRead & { objectId: string; digest: string; size: number };
  object: FetchRead & { bytes: Uint8Array };
}

export function assertDownloadTransfer(
  transfer: DownloadTransfer,
  runtimeBase: string,
  projectId: string,
  video: ManagedOutput,
  savedBytes: Uint8Array,
  downloadUrl: string,
  pageOrigin: string,
): void {
  assert.equal(transfer.runtimeBase, runtimeBase);
  assert.equal(transfer.pageOrigin, pageOrigin);
  const base = runtimeBase.replace(/\/$/, '');
  const objectId = encodeURIComponent(video.object_id);
  assert.equal(transfer.location.url,
    `${base}/v1/projects/${encodeURIComponent(projectId)}/objects/${objectId}/location`);
  assert.equal(transfer.object.url, `${base}/v1/objects/${objectId}`);
  for (const read of [transfer.location, transfer.object]) {
    assert.equal(read.method, 'GET');
    assert.equal(read.resourceType, 'fetch');
    assert.equal(read.status, 200);
    assert.equal(read.range, undefined);
    assert.equal(read.origin, pageOrigin);
    assert.equal(read.redirected, false);
  }
  assert.equal(transfer.location.objectId, video.object_id);
  assert.equal(transfer.location.digest, video.digest);
  assert.equal(transfer.location.size, video.size);
  assert.equal(transfer.object.bytes.length, video.size);
  assert.equal(mediaHash(transfer.object.bytes), video.digest);
  assert.deepEqual(Buffer.from(savedBytes), Buffer.from(transfer.object.bytes));
  assert.ok(downloadUrl.startsWith(`blob:${pageOrigin}/`), 'native download must use a same-page blob');
  const blob = new URL(downloadUrl.slice(5));
  assert.equal(blob.origin, pageOrigin);
  assert.ok(blob.pathname.length > 1);
  assert.equal(blob.search, '');
  assert.equal(blob.hash, '');
}

/** Observe the click's generated-client reads without intercepting App bytes. */
export function observeDownloadTransfer(page: Page, runtimeBase: string, projectId: string, video: ManagedOutput) {
  const pageOrigin = new URL(page.url()).origin;
  const base = runtimeBase.replace(/\/$/, '');
  const objectUrl = `${base}/v1/objects/${encodeURIComponent(video.object_id)}`;
  const locationUrl = `${base}/v1/projects/${encodeURIComponent(projectId)}/objects/${encodeURIComponent(video.object_id)}/location`;
  const reads: Array<Promise<{ read: FetchRead; bytes: Buffer }>> = [];
  const onResponse = (response: Response) => {
    if (![objectUrl, locationUrl].includes(response.url())) return;
    const request = response.request();
    if (request.resourceType() === 'media') return;
    const headers = request.headers();
    const read: FetchRead = {
      url: response.url(), method: request.method(), resourceType: request.resourceType(),
      status: response.status(), range: headers.range, origin: headers.origin,
      redirected: request.redirectedFrom() !== null,
    };
    const reading = response.body().then(bytes => ({ read, bytes }));
    void reading.catch(() => {});
    reads.push(reading);
  };
  page.on('response', onResponse);
  return {
    async finish(): Promise<DownloadTransfer> {
      const results = await Promise.all(reads);
      const locations = results.filter(item => item.read.url === locationUrl);
      const objects = results.filter(item => item.read.url === objectUrl && item.read.resourceType !== 'media');
      assert.equal(locations.length, 1, 'click must read exactly one same-project object location');
      assert.equal(objects.length, 1, 'click must fetch exactly one full generated-client object');
      assert.ok(results.indexOf(locations[0]) < results.indexOf(objects[0]), 'location must precede object fetch');
      const location = JSON.parse(locations[0].bytes.toString('utf8')) as Pick<ObjectLocation, 'object_id' | 'digest' | 'size'>;
      return {
        runtimeBase,
        pageOrigin,
        location: { ...locations[0].read, objectId: location.object_id, digest: location.digest, size: location.size },
        object: { ...objects[0].read, bytes: objects[0].bytes },
      };
    },
    stop() { page.off('response', onResponse); },
  };
}
