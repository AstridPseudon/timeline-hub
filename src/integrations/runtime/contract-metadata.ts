/**
 * Compatibility metadata for the one generated Runtime client.
 *
 * Runtime remains the wire/schema authority. The C1/C2 values identify the
 * app contract inputs consumed by this seam; they do not create another wire
 * contract or client.
 */

import { PROTOCOL, SCHEMA_DIGEST, COMPONENT_MANIFEST_SHA256 } from './generated-contract-metadata.ts';

export const RUNTIME_PROTOCOL = PROTOCOL;
/** The checked-in generated contract is the only accepted Runtime authority. */
export const RUNTIME_SCHEMA_DIGEST = SCHEMA_DIGEST;
export const RUNTIME_ACCEPTED_SCHEMA_DIGESTS = [RUNTIME_SCHEMA_DIGEST] as const;
export const RUNTIME_COMPONENT_MANIFEST_SHA256 = COMPONENT_MANIFEST_SHA256;
export const RUNTIME_TARGETED_EXECUTION_CAPABILITY = 'execution_binding.targeted.v1' as const;

export const ASTRID_C1_CANONICAL_DIGEST = 'sha256:e74a88b718861d100e64c1212f1caa7f36ded5d280e44f5cb6d9a424412a8559' as const;
export const ASTRID_C2_CANONICAL_DIGEST = 'sha256:396d117206670e7ed9cf44582317a5a9396761793024e74f55823e448e77ffb3' as const;
