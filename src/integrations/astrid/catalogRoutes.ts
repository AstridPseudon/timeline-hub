import {
  runtimeCapabilitySchema,
  runtimeCapabilityV2Schema,
  type RuntimeCapabilityV2,
  runtimePageSchema,
  type RuntimeCapability,
} from '@/tools/video-editor/data/bridgeContract.ts';
import { z } from 'zod';
import type { AstridBridgeTransport } from './transport.ts';

const capabilityPageSchema = runtimePageSchema(runtimeCapabilitySchema);

export class AstridCapabilityBindingError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AstridCapabilityBindingError';
  }
}

export class AstridLocalCatalogRoutes {
  constructor(private readonly transport: AstridBridgeTransport) {}

  async list(options: { cursor?: string; limit?: number } = {}): Promise<{
    items: RuntimeCapability[];
    next_cursor: string | null;
  }> {
    const query = new URLSearchParams();
    query.set('limit', String(options.limit ?? 50));
    if (options.cursor !== undefined) query.set('cursor', options.cursor);
    return await this.transport.requestJson(
      `/v1/capabilities?${query.toString()}`,
      {},
      capabilityPageSchema,
      'capability catalog',
    );
  }

  /** Explicit version selection: never retry dynamic actions against v1 placeholders. */
  async getV2(capabilityId: string): Promise<RuntimeCapabilityV2> {
    if (!capabilityId) throw new AstridCapabilityBindingError('capability ID is required');
    const schema = z.strictObject({
      catalog_version: z.literal(2), items: z.array(runtimeCapabilityV2Schema),
      next_cursor: z.string().min(1).nullable(),
    });
    const ids = new Set<string>();
    const cursors = new Set<string>();
    let cursor: string | null = null;
    let match: RuntimeCapabilityV2 | undefined;
    do {
      const query = new URLSearchParams({ catalog_version: '2', limit: '50' });
      if (cursor !== null) {
        if (cursors.has(cursor)) throw new AstridCapabilityBindingError('capability catalog cursor cycle detected');
        cursors.add(cursor);
        query.set('cursor', cursor);
      }
      const page = await this.transport.requestJson(`/v1/capabilities?${query}`, {}, schema, 'capability catalog v2');
      for (const row of page.items) {
        if (ids.has(row.capability_id)) throw new AstridCapabilityBindingError(`capability catalog contains duplicate ID: ${row.capability_id}`);
        ids.add(row.capability_id);
        if (row.capability_id === capabilityId) match = row;
      }
      cursor = page.next_cursor;
    } while (cursor !== null);
    if (!match) throw new AstridCapabilityBindingError(`capability is not registered: ${capabilityId}`);
    return match;
  }

  async bindV2(capabilityId: string, expectedDigest: string): Promise<string> {
    const match = await this.getV2(capabilityId);
    if (match.status !== 'ready' || match.storage_estimate.mode === 'unavailable') {
      throw new AstridCapabilityBindingError(`capability is not ready: ${capabilityId}`);
    }
    if (match.definition_digest !== expectedDigest) {
      throw new AstridCapabilityBindingError(`capability digest mismatch: ${capabilityId}`);
    }
    return match.definition_digest;
  }

  async bind(capabilityId: string, expectedDigest?: string): Promise<string> {
    const match = await this.get(capabilityId);
    if (expectedDigest !== undefined && expectedDigest !== match.definition_digest) {
      throw new AstridCapabilityBindingError(`capability digest mismatch: ${capabilityId}`);
    }
    return match.definition_digest;
  }

  /** Resolve one ready catalog record without inventing a local digest. */
  async get(capabilityId: string): Promise<RuntimeCapability> {
    if (capabilityId.length === 0) {
      throw new AstridCapabilityBindingError('capability ID is required');
    }
    let cursor: string | undefined;
    const seenCursors = new Set<string>();
    const seenCapabilityIds = new Set<string>();
    let match: RuntimeCapability | undefined;

    while (true) {
      if (cursor !== undefined) {
        if (seenCursors.has(cursor)) {
          throw new AstridCapabilityBindingError('capability catalog cursor cycle detected');
        }
        seenCursors.add(cursor);
      }
      const page = await this.list({ cursor });
      for (const capability of page.items) {
        if (seenCapabilityIds.has(capability.capability_id)) {
          throw new AstridCapabilityBindingError(
            `capability catalog contains duplicate ID: ${capability.capability_id}`,
          );
        }
        seenCapabilityIds.add(capability.capability_id);
        if (capability.capability_id === capabilityId) {
          if (match !== undefined) {
            throw new AstridCapabilityBindingError(`capability catalog contains duplicate ID: ${capabilityId}`);
          }
          match = capability;
        }
      }
      if (page.next_cursor === null) break;
      cursor = page.next_cursor;
    }

    if (match === undefined) {
      throw new AstridCapabilityBindingError(`capability is not registered: ${capabilityId}`);
    }
    if (match.status !== 'ready') {
      throw new AstridCapabilityBindingError(
        `capability is not ready: ${capabilityId} (${match.status})`,
      );
    }
    return match;
  }
}
