import type { DirectHarness } from '../../local/support/harness';

export interface PackHostSession {
  stop(): Promise<void>;
}

/**
 * Agent-owned seam: attach the production launcher to this exact realm and
 * support root, then ensure_pack_host with its issued source/boot handoff.
 * Return only after rendering.render is ready; stop must reap the host group.
 * Discovery or AstridCli.host() alone cannot supply this authority.
 */
export async function startRealPackHost(harness: DirectHarness): Promise<PackHostSession> {
  throw new Error(
    `Agent launcher bootstrap helper required for realm ${harness.realmDir} and support root ${harness.supportDir}. `
    + 'It must own the astrid-pack-host credential, source inventory and boot manifest, call ensure_pack_host, '
    + 'use the parent-selected installed Remotion browser, and return a cleanup handle. '
    + 'See escalation viewing-20261019T2248Z; no marker-host or fabricated handoff fallback.',
  );
}
