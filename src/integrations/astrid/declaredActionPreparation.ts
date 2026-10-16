import { z } from 'zod';
import {
  bridgeTaskAdmissionRequestSchema,
  bridgeTaskAdmissionSpecSchema,
  bridgeTaskStorageEstimateSchema,
  runtimeEstimatorIdentitySchema,
  runtimeSha256IdSchema,
} from '@/tools/video-editor/data/bridgeContract.ts';

/** Shared flat J038 preparation reply, not a new HTTP route.
 * The authenticated host integration must supply the canonical digest implementation.
 * Its execution-side source-fenced recomputation remains authoritative.
 */
export const declaredActionPreparationRequestSchema = bridgeTaskAdmissionRequestSchema.omit({
  storage_estimate: true,
});
export const preparedDeclaredActionSchema = z.strictObject({
  capability_id: z.string().min(1),
  capability_digest: runtimeSha256IdSchema,
  schema_version: z.literal(1),
  spec: bridgeTaskAdmissionSpecSchema,
  // The admitted no-input declared-action path has no immutable input facts.
  input_facts: z.tuple([]),
  storage_estimate: bridgeTaskStorageEstimateSchema,
  estimator: runtimeEstimatorIdentitySchema,
  spec_digest: runtimeSha256IdSchema,
  source_digest: runtimeSha256IdSchema,
  preparation_digest: runtimeSha256IdSchema,
});
export type DeclaredActionPreparationRequest = z.infer<typeof declaredActionPreparationRequestSchema>;
export type PreparedDeclaredAction = z.infer<typeof preparedDeclaredActionSchema>;
export interface DeclaredActionPreparationAdapter {
  /** At the host boundary only: map schema '1' to 1 and empty IDs to input_facts: []. */
  prepare(request: DeclaredActionPreparationRequest): Promise<unknown>;
  /** Exact host canonical encoding, including numeric and Unicode representation. */
  digest(value: unknown): Promise<string>;
}
