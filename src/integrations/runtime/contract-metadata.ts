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

export const ASTRID_C1_CANONICAL_DIGEST = 'sha256:bce45d851aa4c92fe3abcf53379e5401d8180f8be10209acb69a5f4484c92e66' as const;
export const ASTRID_C2_CANONICAL_DIGEST = 'sha256:6f64835b5c351d7a5ee658f0aefcee598e1e3a0fafdae5a59deeaa6e968cbc24' as const;
