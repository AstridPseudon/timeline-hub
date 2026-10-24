Implemented in exactly the three allowed files.

- [localSaveSession.ts](/home/user/work/wt/app-A2-recovery-basis-sol-0224/src/tools/video-editor/commands/localSaveSession.ts:220) validates every retained intent’s original display basis before enabling recovery.
- Migrated all seven faults unchanged: missing basis, missing/empty revision, missing/empty publication, missing document, mismatched revision.
- Removed precisely the original 48-line matrix from `commitSession.test.ts`; verified all other content is unchanged.
- Added valid accepted-prefix replay coverage across a refreshed mount, preserving B’s exact request/key and canonical sibling/opaque data.

Decision: corrected A4’s retention assertion to compare intents with the **corrupted persisted snapshot**. Comparing against pre-corruption bytes would require repairing the invalid metadata.

Validation used actual Node **20.20.0**, private cache/config, runner loading, no cache, and two workers:

```bash
NODE_OPTIONS=--require=/tmp/w-4d44d2a5dd/vitest-preload.cjs /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config /tmp/w-4d44d2a5dd/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/commands/localSaveSession.recoveryBasis.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
```

**100 passed across five files.** The final recovery file against an exact original-source overlay produced **seven failures and one positive pass**; against the fix, all eight passed.

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c '/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json && /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json && /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json'
```

**PASS** for Root/App/Node.

```bash
/opt/node20/bin/node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/localSaveSession.ts src/tools/video-editor/commands/localSaveSession.recoveryBasis.test.ts src/tools/video-editor/commands/commitSession.test.ts --max-warnings 0
git diff --check
```

**PASS**, including exact scope and seven-case mapping checks.

No blockers. No full, browser, backend, or service runs. Commit message and `DONE` written; no commit or merge performed. Ready for independent reviewer `app-A2-recovery-basis-review-0230`.