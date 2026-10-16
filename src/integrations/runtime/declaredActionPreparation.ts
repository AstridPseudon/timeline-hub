import type { DeclaredActionPreparationAdapter } from '@/integrations/astrid/declaredActionPreparation.ts';
import { declaredActionPreparationRequestSchema } from '@/integrations/astrid/declaredActionPreparation.ts';
import { canonicalJsonStringify, sha256Hex } from '@/tools/video-editor/data/typed/timelineBundle.ts';
import { ReighRuntimeClient } from './client.ts';

type CapabilityStoragePreparer = Pick<ReighRuntimeClient, 'prepareCapabilityStorage'>;

/** Connect the generic Generator form to Runtime's authenticated preparation route. */
export function createRuntimeDeclaredActionPreparationAdapter(
  runtime: CapabilityStoragePreparer = new ReighRuntimeClient(),
): DeclaredActionPreparationAdapter {
  return {
    async prepare(request) {
      const parsed = declaredActionPreparationRequestSchema.parse(request);
      if (parsed.input_object_ids.length !== 0) {
        throw new Error('Typed action preparation currently requires an empty immutable-input list.');
      }
      return await runtime.prepareCapabilityStorage(parsed.project, parsed.capability_id, {
        capability_digest: parsed.capability_digest,
        schema_version: 1,
        spec: parsed.spec,
        input_object_ids: [],
      });
    },
    async digest(value) {
      return `sha256:${await sha256Hex(canonicalJsonStringify(value))}`;
    },
  };
}
