import { writeFileSync } from 'node:fs';
import { ensureProjectHasTimeline } from '/home/user/work/wt/app-m2-opaque-root-writer-closure/src/integrations/runtime/createDefaultTimeline.ts';
import type { AstridRuntimeClient } from '/home/user/work/wt/app-m2-opaque-root-writer-closure/src/integrations/runtime/client.ts';

async function main() {
  const hiddenAuthored = JSON.parse('{"opaque":[null,false,[]],"nullable":null,"ordered":[3,1,2],"__proto__":{"literal":true},"clips":[{"id":"edited","at":0}],"tracks":[]}');
  let submitted: Record<string, unknown> | undefined;
  // The public timeline resource exposes no legacy authored document bytes.
  const client = {
    listTimelines: async () => [{ timeline_id: 'headless-shell', head_revision_id: null }],
    getProject: async () => ({ version: 1, metadata: {} }),
    publishParentComposition: async (_project: string, _timeline: string, body: Record<string, unknown>) => {
      submitted = body;
      throw new Error('STOP diagnostic before persistence: receiver must protect nonempty shell');
    },
  } as unknown as AstridRuntimeClient;
  try { await ensureProjectHasTimeline('project', client); } catch (error) {
    if (!(error instanceof Error) || !error.message.startsWith('STOP diagnostic')) throw error;
  }
  if (!submitted) throw new Error('No publication candidate captured');
  const config = (submitted.parent_composition as Record<string, unknown>).config as Record<string, unknown>;
  writeFileSync('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-opaque-root-writer-closure/notes/bootstrap-candidate.json', JSON.stringify({ hiddenAuthored, submitted }, null, 2));
  const missing = Object.keys(hiddenAuthored).filter(key => !Object.hasOwn(config, key));
  if (!missing.includes('opaque') || (config.clips as unknown[]).length !== 0) throw new Error('Counterexample no longer reproduces');
  console.log(JSON.stringify({ result: 'UNSAFE CANDIDATE REPRODUCED, NO PERSISTENCE', expected_head: submitted.expected_head,
    missingRawKeys: missing, originalClipIds: hiddenAuthored.clips.map((clip: { id: string }) => clip.id), submittedClips: config.clips,
    limitation: 'App preflight only; this fake receiver deliberately stops before persistence. Real Runtime must check hidden authored shell state atomically.' }, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
