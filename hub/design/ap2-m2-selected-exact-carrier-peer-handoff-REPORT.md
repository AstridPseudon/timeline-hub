# Selected PARAM exact-carrier handoff

## Outcome

The exact native carrier exists in the current published 0.2.13 line. The
App branch already contains the bounded adapter, so this worker made no source
changes and did not draft a missing-carrier peer request. The earlier CLI
setter refusal is a guarded convenience/checkout path; it is not evidence that
the native `clip.set-params` carrier is absent.

## Current published / pinned source

- App branch: `ff6a55c30` (the selected PARAM route is already present).
- Current Agent integration: `6f0cdc7d`; current Runtime integration:
  `7e160c5d`.
- Current generated metadata in Agent, Runtime, and App is contract `0.2.13`
  with schema digest
  `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
  and component digest
  `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.
- Frozen public references inspected read-only: Agent `8130a401` and Runtime
  `2c4ac18`. Agent’s registry has the existing
  `clip.set-params -> clip_set_params` operation. Runtime’s
  `ClipSetParamsArgs` is the same `{values, clear, schema_source?}` shape.

The existing carrier is sufficient for the accepted selected scope:

1. App emits the existing `clip.set-params` operation with `values`, `clear`,
   and the exact `DocumentPin`; it adds no DTO or EditCommand variant.
2. Agent’s native selected-pack path admits the exact source pin and records
   `params.schema`, `params.snapshot`, and fixed `params.element` dependencies,
   then applies only literal top-level PARAM values/clears while preserving
   unmentioned opaque fields.
3. Runtime accepts the same command/schema. App’s `paramReadClient` only wraps
   the existing verified-document and verified-object reads.

Relevant current App source is `src/tools/video-editor/commands/clipParamsCapture.ts:6-25`,
`src/tools/video-editor/commands/commitSession.ts:440-508`, and
`src/integrations/runtime/dataProvider.ts:332-341`. The selected authority
resolver requires the accepted history direct triple and exact original P1;
it does not infer authority from a manifest winner or current catalog.
Literal PARAM handling and the old safe catalog fallback remain available where
the selected-native prerequisite is not met; refusal remains visible.

## Private ordinary 0.2.14 hold

Agent `3c4f6de4` and Runtime `2020741` are separately available by `git show`.
Both carry contract `0.2.14`, schema digest
`sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`,
and the same existing PARAM carrier shape. They remain private hold sources;
there was no activation, public-pin change, or native-contract edit here. The
current public P1 is the 0.2.13 source above.

## Evidence

- App targeted Vitest:
  `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx`
  -> **4 files, 24 tests passed**.
- Agent targeted native/schema/authority/checkout tests:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider /home/user/work/agent/tests/sdk/test_timeline_selected_schema.py /home/user/work/agent/tests/sdk/test_timeline_selected_param_authority.py /home/user/work/agent/tests/sdk/test_timeline_selected_schema_runtime.py /home/user/work/agent/tests/sdk/test_timeline_native_checkout.py`
  -> **79 passed, 32 skipped**.
- Runtime focused contracts:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider /home/user/work/runtime/tests/test_timeline_bundle2_contract.py /home/user/work/runtime/tests/test_schema_validation.py /home/user/work/runtime/tests/test_command_schema_compatibility.py /home/user/work/runtime/tests/test_timeline_current_union_contract.py -k 'not test_typescript_package_exports_native_args_and_open_rows'`
  -> **252 passed, 1 deselected**. The unfiltered run had one environment-only
  `tsc` failure (`TS5112`: the fixture invokes `tsc` with an explicit file while
  a repo `tsconfig.json` is present); its other **252 tests passed**.
- Current App `selectedParamsCommand` was executed directly with `node
  --import tsx`; its JSON command core exactly matched the existing accepted
  native PARAM command (`parent/clip:effect`, values `{seed:9}`, clear `[]`,
  public P1 pin).
- The retained portable original-P1 replay was attempted against current Agent
  with:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-app2-native/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/selected-param-original-pin-probe.py`
  -> **blocked by `CommitRejected: submitted reads does not match authoritative
  capture`**. The existing probe itself fails the same way on current Agent,
  so this is a stale captured-record/read-envelope mismatch, not an App command
  mismatch. The current Agent targeted suite independently proves native full
  record, bundle, inverse, rebase, and replay behavior, but a fresh current
  TS-to-Agent full-record replay is not claimed here.

## Blocked / next step

No App or contract change is authorized by this handoff. Before merging the
selected producer 130 PASS, Agent/Runtime owners should refresh or reconcile
the portable original-P1 transcript’s captured `reads` against the current
Agent read recorder, then rerun the exact TS-command-to-Agent full-record,
bundle, inverse, and replay check. Do not broaden the wire or replace the
existing carrier. No full suite, browser, localhost, or socket run was made.
