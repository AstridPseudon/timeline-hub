Implemented scoped parent moves and single/bulk transition clears through the existing `doc.patch` carrier. Original causal inputs, physical clip paths, guarded reads, steps and complete untouched child closure are preserved. Unsupported child selections and unrelated changes remain refused.

Only five allowed files changed. Inherited provider/preview code, save-hook source, diagnostics, transport, specs, pins and dependencies remain exact.

Validation:

- Original-source parent reproduction: **3 failed, 1 passed**.
- Expanded original-source positive controls: **15 failed, 1 passed**.
- Repaired source: **292 passed across 13 targeted files**, including all 16 positive controls. No expected-failure or skip markers.
- Three flocked TypeScript checks, scoped ESLint, `git diff --check`, allowed-file census and protected-source identity checks: **passed**.

Exact test command, using these path abbreviations:

```bash
H=src/tools/video-editor/hooks
C=src/tools/video-editor/commands
/opt/node20/bin/node --import "$TMPDIR/vitest-preload.mjs" \
  /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mts" --configLoader runner \
  --no-cache --maxWorkers=1 \
  "$H/timelineLocalSaveHandoff.test.ts" \
  "$H/useTimelinePersistence.test.tsx" "$H/useClipEditing.test.ts" \
  "$C/localSaveSession.test.ts" "$C/localSaveSession.v2.test.ts" \
  "$C/localSaveSession.lifecycle.test.ts" \
  "$C/localSaveSession.replayProtocol.test.ts" \
  "$C/localSaveSession.recoveryBasis.test.ts" \
  "$C/localSaveSession.ownerRecovery.test.ts" \
  "$C/localSaveSession.trackLabelRefusal.test.ts" \
  "$H/useTimelineTrackManagement.test.ts" \
  "$H/useClipDrag.test.tsx" "$H/useTimelineCommit.test.tsx"
```

OLDRED used the first three files with `-t 'P2 parent|causal .*transition None|clears only selected parent'` against original HEAD source.

Static checks used:

```bash
flock -w 300 /home/user/work/.app-tsc.lock \
  /opt/node20/bin/node /home/user/work/app/node_modules/typescript/bin/tsc \
  --noEmit --incremental false -p <config>
```

Each of `tsconfig.json`, `tsconfig.app.json`, and `tsconfig.node.json` passed. ESLint ran with `--max-warnings 0` on all five changed files.

Reviewed ancestry:

- `e6059d5669de230a152d203a794f36ea42fac075`
- `6efdb119932b99e25442ec89b56fffb3761c5a0f`
- `f90e708b379145ac456924742cc51c187ed6e0c6`

Control donor: `87e60529d343b24d48422fa89313260ba8867ead`.

The repair admits verified same-track parent timing moves and explicit transition removals. Cross-track and broader edits remain outside this qualified path. Original production failure attribution remains **UNKNOWN**; no live/P2 credit claimed.

No blockers. Commit message and `DONE` written. Next: independent Luna review.