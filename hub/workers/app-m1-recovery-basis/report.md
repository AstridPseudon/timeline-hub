Implemented within the three owned files.

- Recovery projects original R0 plus B’s persisted preview, while retaining HA for submission and B’s exact payload/key.
- Incomplete display pins fail closed and retain work.
- Typed conflicts/refusals survive recovery without resending rejected work. Dispose/drain behavior is unchanged.

Validation:

```bash
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
```

**180 passed**, including the existing 25 session/hook cases.

```bash
./node_modules/.bin/eslint src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts --max-warnings 0
git diff --check
```

Both passed. No full/browser suites or installs.

Decision: legacy recovery uses only a stored direct head with a matching raw document; a dependent submission base cannot establish the display pair.

Composition remains unverified: run the producer regression after its field lands. The fixture now returns typed conflicts for actual guard clashes, so its separate producer `retry` assertion needs review. The required r0/p0 assertion is untouched.

[Commit message written](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m1-recovery-basis/commit-msg). No git mutations.