import { z } from 'zod';
import {
  bridgeTaskAdmissionRequestSchema,
  runtimeEstimatorIdentitySchema,
  runtimeSha256IdSchema,
} from '@/tools/video-editor/data/bridgeContract.ts';

/** App adapter boundary, not an HTTP route or the host's Python dataclass wire format.
 * The authenticated host integration must supply the canonical digest implementation.
 * Its execution-side source-fenced recomputation remains authoritative.
 */
export const declaredActionPreparationRequestSchema = bridgeTaskAdmissionRequestSchema.omit({
  storage_estimate: true,
});
export const preparedDeclaredActionSchema = z.strictObject({
  request: bridgeTaskAdmissionRequestSchema,
  estimator: runtimeEstimatorIdentitySchema,
  spec_digest: runtimeSha256IdSchema,
  source_digest: runtimeSha256IdSchema,
  preparation_digest: runtimeSha256IdSchema,
});
export type DeclaredActionPreparationRequest = z.infer<typeof declaredActionPreparationRequestSchema>;
export type PreparedDeclaredAction = z.infer<typeof preparedDeclaredActionSchema>;
export interface DeclaredActionPreparationAdapter {
  prepare(request: DeclaredActionPreparationRequest): Promise<unknown>;
  /** Exact host canonical encoding, including numeric and Unicode representation. */
  digest(value: unknown): Promise<string>;
}
