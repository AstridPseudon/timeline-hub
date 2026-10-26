/**
 * Compatibility metadata for the one generated Runtime client.
 * Runtime remains the wire/schema authority.
 */

import { CONTRACT_VERSION, PROTOCOL, SCHEMA_DIGEST, COMPONENT_MANIFEST_SHA256, OPERATIONS } from './generated-contract-metadata.ts';

/** Full C0 v2 schemas, including D62's additive authenticated history ABI. */
export function supportsFullV2Commit(): boolean {
  return PROTOCOL === 'workspace.v1' && CONTRACT_VERSION === '0.2.14'
    && COMPONENT_MANIFEST_SHA256 === 'sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5'
    && [
      'sha256:fce459b4b6639e6cdf310c663b400967a30436eeda2d0382546b79eec73afe81',
      'sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c',
      'sha256:4118b1e26d30be43cb1a01649df0065fed6e55a528b8956364df8f4eedb413d2',
      'sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b',
    ].includes(SCHEMA_DIGEST)
    && Array.isArray(OPERATIONS) && OPERATIONS.includes('commitTimeline') && OPERATIONS.includes('listTimelineCommits');
}

export const RUNTIME_PROTOCOL = PROTOCOL;
/** The current generated Runtime contract; compatible older contracts are listed below. */
export const RUNTIME_SCHEMA_DIGEST = SCHEMA_DIGEST;
export const RUNTIME_ACCEPTED_SCHEMA_DIGESTS = [
  RUNTIME_SCHEMA_DIGEST,
  // Runtime e6e5273d predates unresolved-effect warning support and remains compatible.
  'sha256:9081570c9d68212906426cfb0290c319849ea3dacaea1a0375d9e7e96d8c5ae9',
  // Runtime fa9cd546 is still pinned by the installer and predates this generated client refresh.
  'sha256:3605a9c517d92031d7702307e256223905784e0800bcd09c87005ce21ee53a47',
  // Before app-state: the Runtime without /v1/app-state stays compatible (the editor tour falls back to its local flag).
  'sha256:53bc985a9ab3dba290c3d2a99c7837460f43c9bb0f0ef486d273eec3e2e44ed0',
  // Before the additive starting state: existing service health remains compatible.
  'sha256:d4b3e46ab6481694810561c7aac99e45356a24a04b08545e53a7257663f007c4',
  // Before service health was added: existing Runtime responses remain compatible.
  'sha256:ec06fbc6567fe28065d22626b040cad81bb2e5318623586ae9187c713794f6b9',
] as const;
export const RUNTIME_COMPONENT_MANIFEST_SHA256 = COMPONENT_MANIFEST_SHA256;
export const RUNTIME_TARGETED_EXECUTION_CAPABILITY = 'execution_binding.targeted.v1' as const;
