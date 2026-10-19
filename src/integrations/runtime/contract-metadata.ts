/**
 * Compatibility metadata for the one generated Runtime client.
 * Runtime remains the wire/schema authority.
 */

import { PROTOCOL, SCHEMA_DIGEST, COMPONENT_MANIFEST_SHA256 } from './generated-contract-metadata.ts';

export const RUNTIME_PROTOCOL = PROTOCOL;
/** The current generated Runtime contract; compatible older contracts are listed below. */
export const RUNTIME_SCHEMA_DIGEST = SCHEMA_DIGEST;
export const RUNTIME_ACCEPTED_SCHEMA_DIGESTS = [
  RUNTIME_SCHEMA_DIGEST,
  // Before service health was added: existing Runtime responses remain compatible.
  'sha256:ec06fbc6567fe28065d22626b040cad81bb2e5318623586ae9187c713794f6b9',
] as const;
export const RUNTIME_COMPONENT_MANIFEST_SHA256 = COMPONENT_MANIFEST_SHA256;
export const RUNTIME_TARGETED_EXECUTION_CAPABILITY = 'execution_binding.targeted.v1' as const;
