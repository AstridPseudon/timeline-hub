import { describe, expect, it } from 'vitest';
import { ASTRID_ACP_CONTEXT_SYSTEM_PROMPT } from './astridAcpLauncher.ts';

/**
 * Timeline verbs that exist in the current Astrid CLI.
 * Source: `astrid-tools timelines --help` / `astrid timelines <verb> --help` run from
 * labs/main-custody/Astrid (branch claude/main-reliability-20261015). `retime-clip` was
 * removed in Astrid commit 0bd37792 ("retire legacy timeline document routes").
 * Only the verbs this prompt uses are listed here.
 */
const ASTRID_TIMELINE_VERBS_IN_PROMPT = ['show', 'checkout', 'edit', 'publish'] as const;

/** Flags that only existed on the removed `retime-clip` / `save` routes. */
const REMOVED_RETIME_FLAGS = ['--preserve-duration', '--hold', '--expected-version'] as const;

describe('ASTRID_ACP_CONTEXT_SYSTEM_PROMPT runtime commands', () => {
  it('does not reference the removed retime-clip command', () => {
    expect(ASTRID_ACP_CONTEXT_SYSTEM_PROMPT).not.toContain('retime-clip');
  });

  it('only uses timeline verbs that the current Astrid CLI provides', () => {
    const verbs = [...ASTRID_ACP_CONTEXT_SYSTEM_PROMPT.matchAll(/astrid-tools timelines ([a-z-]+)/g)].map(
      (match) => match[1],
    );
    expect(verbs.length).toBeGreaterThan(0);
    for (const verb of verbs) {
      expect(ASTRID_TIMELINE_VERBS_IN_PROMPT).toContain(verb);
    }
  });

  it('does not mention flags that only the removed retime-clip route accepted', () => {
    for (const flag of REMOVED_RETIME_FLAGS) {
      expect(ASTRID_ACP_CONTEXT_SYSTEM_PROMPT).not.toContain(flag);
    }
  });
});
