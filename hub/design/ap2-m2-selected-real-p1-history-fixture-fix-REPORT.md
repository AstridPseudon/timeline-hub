# AP2 M2 selected real P1 history fixture fix

## Result

Repaired only `tests/e2e/local/support/harness.ts`.

- The initial selected PARAM hold-effect clip now keeps the existing same-id,
  same-kind, no-media/hold shape but uses an unowned `revision: 'draft-1'`
  ref with no `packId`.
- The normal Agent `timelines update-element` call therefore owns P1 through
  the admitted project pack. The harness reads accepted Runtime history and
  fails unless the real accepted receipt contains exactly:
  `clip.set-element`, then `clip.set-params`.
- No product/shared consumer, schema, API, dependency, synthetic history,
  selected-authority bypass, browser hash, or alias was changed.

## Checks run

- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts` — passed.
- `npx tsc --noEmit --pretty false` — passed.
- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts` — passed, 2 files / 16 tests.
- `git diff --check` — passed.

An initial requested pure-test invocation with `--configLoader=runner` was
not usable because this repository config references CommonJS `__dirname`;
it failed during config loading before tests ran. The normal bundled config
above passed. No browser, socket, DEV, runner, request-test, or full suite was
run, as required.

## Later authority review and central command

After this candidate is reviewed, the orchestrator should inspect the final
diff/report and then run the explicitly authorized central suite command from
outside this worker. The exact deferred command is:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-real-p1-history-fixture-fix full) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The real DEV P1/P2/removal/refusal/retry/reload/undo/zero-legacy journey and
later authority review remain unverified in this code-only worker run.
