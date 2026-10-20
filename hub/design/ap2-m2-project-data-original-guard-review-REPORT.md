# App project-data original-guard review

Date: 2026-10-20 UTC  
Decision: **APPROVE the inert helper merge; HOLD native activation pending the paired Runtime gate.**

## Scope and exact diff

Reviewed App commit `ebd7d955e071d398290086d0c034d7ea13a66d06`, parent
`092ee4ab102e89c2e2c9360413e845312f48b8c1`:

- `src/tools/video-editor/commands/projectDataMember.ts`: removed the
  optional `ctx.command.reads` path-hint population; retained the three
  `ctx.object(...)` setup operations and leaf `ctx.write(...)`; deleted the
  generated command's optional `reads` property after claim validation.
- `src/tools/video-editor/commands/projectDataMember.test.ts`: moved the
  setup-read assertion from `commands[0].reads` to `records[0].reads` and
  added the assertion that the submitted command has no `reads` property.

No public pin, wire contract, API, dependency, schema, Runtime, or Agent
source was changed. The worktree is clean and `git diff --check` passes.

## Guard proof

The removed field is only the optional submitted read hint. In the App source:

- `projectDataMember.ts:193-196` still calls `ctx.object` for `config`,
  `config.app`, and the target namespace, then writes the requested leaf.
- `clipMovePrimitives.ts:311-316` (`MoveRecording.object`) records a read and
  a write for absent/null setup containers; `assign` records every write's
  `before` state in `record.writes` (`:295-301`).
- `projectDataMember.ts:134-144` (`replaceGeneratedClaims`) copies each
  recorded write's original `before` state into `command.expect`, including
  the exact leaf value/absence/null and the container states.
- `MoveRecording` initializes `record.reads` as the original reads-array
  reference (`clipMovePrimitives.ts:225-230`). Deleting `ctx.command.reads` at
  `projectDataMember.ts:208` removes
  only the optional command property; `record.reads` remains available to the
  accepted local record.

The positive App test now demonstrates both sides: `records[0].reads` retains
the original absent container observations (`projectDataMember.test.ts:55-58`),
while `commands[0]` omits `reads` (`:59`). The same test asserts original
absent container and leaf guards in `commands[0].expect` (`:48-53`), and the
null-leaf test asserts the exact `{state: "present", value: null}` guard
(`:85-87`).

The matched Agent source floor is commit
`0a774e4968f5a9728c4ee6b5bbbfe286e26f29a3`, schema
`89ed90ce0a4a95559a6d086d57f851fbcc6d224c9e7658f41467dfa9280eb0c3`:

- `_project_data_commands.py:89-96` uses the same container setup and exact
  leaf write.
- `_recording.py:121-147` records original write states and setup reads.
- `commands.py:159-185` explicitly relaxes only missing/null/dictionary
  container setup claims; `commands.py:195-207` still verifies every supplied
  `expect` leaf guard. The container exception cannot bypass a present,
  non-null leaf guard.
- `commands.py:272-329` accepts omitted optional `reads` when the submitted
  command did not claim them, while retaining generated accepted records.
- `rebase.py:9-16` checks intervening history before executing the captured
  command; `inverse.py:178-228` and `:384-415` use accepted record writes/reads
  and exact after-state guards for stale inverse refusal.

This is source-level proof of where the original guard lives; it does not infer
guard safety from TypeScript output parity.

## Focused behavioral evidence

Using one private extracted copy of Agent `0a774...`, cleaned on exit:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PRIVATE_DIR" \
  /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  "$PRIVATE_DIR/tests/editing_conformance/test_recipe_m2_project_data.py" \
  -k 'disjoint_key_rebase_and_same_key_aba_refuses or disjoint_key_rebase_merges_through_a_null_namespace or replace_preserves_namespace_and_restores_absent_null_and_opaque_values'
3 passed, 14 deselected, 3 warnings
```

The direct dependent-B probe then passed all three controls:

1. A changes `source` to `A` and is acknowledged at `HA`.
2. B is authored over `HA` and its `expect` retains `source=A`.
3. An intervening same-leaf `source=C` causes stale B replay to refuse.
4. A disjoint `source-map=B` replay preserves both `source=C` and
   `source-map=B`.
5. Native inverse of A restores the original absent namespace exactly.

App targeted lane:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts -t 'project-data'
2 files passed; 76 tests passed, 233 skipped
```

No full, browser, localhost, socket, Runtime HTTP, or whole-matrix suite was
run.

## Activation hold / unsafe envelope gap

The frozen Runtime candidate
`origin/codex/handover-timeline-r4-20261019-candidate-runtime` and current
Runtime `tl/integration` contain no `project-data.write` schema/registry or
matching provider. Therefore this review cannot prove the actual Runtime-door
stale-head rebase, dependent-B-at-HA submission, accepted-record persistence,
or Runtime inverse behavior. The concrete unsafe envelope is: a future
Runtime consumer must consume the Agent `0a774...` operation and preserve
`command.expect` leaf guards while treating only setup-container claims as
mergeable. Until that paired provider/registry/accepted-history proof exists,
the App native activation and legacy-writer retirement remain held.

Recommended next step: qualify the exact Agent schema/registry through the
existing Runtime `/v1` provider with one stale same-leaf refusal and one
disjoint-preservation/native-inverse control, then review the App consumer
join. Do not weaken Agent validation or copy new capture guards into App.
