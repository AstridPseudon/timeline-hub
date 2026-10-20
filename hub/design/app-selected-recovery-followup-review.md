# Selected PARAM recovery follow-up independent re-review

## Verdict

**APPROVE** `5541998086415c7b1794d83cc579f06f89712c66` (`tl/app-m2-selected-server-recovery-followup`) against exact parent `1c7345b702ee84cc627ed0bc03c82ae77364a50b`.

The bounded two-path recovery correction fixes both prior stale ordinary-ACK repros and preserves the settled server-authority contract. This is source/test approval only; it is not V1 Runtime/native/browser qualification.

## Line evidence

- `src/tools/video-editor/commands/commitSession.ts:50-64` compares literal `params` states for parent and occurrence-owned selected clips, including absent/present state, without schema evaluation or local provider validation.
- `:578-590` uses the accepted closure only when the retained first intent explicitly follows that accepted intent (`basis.after`); it then detects selected/inverse effects either from the accepted command or from a selected-state difference and replays only the existing original ordinary previews through `workingBundle()`.
- `:206-208` keeps selected work unsent when its original basis is not accepted; `:471-498` retains `after: null`, the captured basis/pin/inputs, and the exact `JSON.stringify(command)` lookup/key path. No basis flag refresh, guard refresh, new DTO, catch fallback, native policy, or writer was added.
- `src/tools/video-editor/commands/commitSession.selectedParams.test.ts:378-426` preserves the two prior ordinary-ACK/refusal repros for selected and inverse recovery; `:428-458` covers a newer original display base after an older selected/inverse acceptance. The pre-existing test body is an unchanged prefix; the diff adds only four tests and deletes none.

The diff from the parent changes only `commitSession.ts` and its existing selected-params test. The unchanged external `counterexamples.test.ts` (four prior controls) and `probes.test.ts` (two repros plus cancellation/new-capture control) were byte-identical to the prior independent review.

## Evidence

Successful focused rerun from a private Git extraction of the reviewed SHA, using private cache/output paths, `--configLoader=runner`, `--no-cache`, `--maxWorkers=1`, and `--no-file-parallelism`:

```text
Test Files  8 passed (8)
Tests       241 passed (241)
```

Successful unchanged external controls from the same private extraction:

```text
Test Files  2 passed (2)
Tests       7 passed (7)
```

The first two overlay attempts failed before test collection because the temporary review config lacked the Composition subpath/Astrid aliases; after correcting only that private harness configuration, the exact source suites passed. No shared dependency, shared cache, product file, or other worktree was modified.

Read-only checks:

```text
git diff --check 1c7345b702ee84cc627ed0bc03c82ae77364a50b 5541998086415c7b1794d83cc579f06f89712c66  # PASS
git diff --name-status 1c7345b702ee84cc627ed0bc03c82ae77364a50b 5541998086415c7b1794d83cc579f06f89712c66  # two intended files only
git status --short --branch  # clean review worktree
```

## Not qualified / next step

No full suite, build, browser, localhost/live socket, project `tsc`, install, or native Runtime process-restart/custody flow was run. D01 remains open: actual V1 Runtime flow, durable lost-ACK exact retry, retained V1 validation after V2/removal, native inverse/reload, matching-pair/property ingress, and zero-legacy browser journey require the orchestrator's separate qualification.
