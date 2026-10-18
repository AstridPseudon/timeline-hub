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

export const ASTRID_C1_CANONICAL_DIGEST = 'sha256:74ff6d5b7582391d6ae5335162bc25faf9bec9745d4d90b4c7646fc20ee76772' as const;
export const ASTRID_C2_CANONICAL_DIGEST = 'sha256:1a3eef2ed3bd8977334a482ef8882b38bb28fbc0a9e3151cfb1c028637247a14' as const;
