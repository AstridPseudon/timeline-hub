# App project-data merge lowering guard review

Date: 2026-10-20 UTC  
Decision: **APPROVE** the exact two-file delta from
`tl/ap2-m2-project-data-native-subprocess-repair` to
`tl/ap2-m2-project-data-main-merge-lowering`, for the inert PLAN2/3/6
ordinary-batch row only.

## Scope and findings

Reviewed only:

- `src/tools/video-editor/commands/projectDataMember.ts`
- `src/tools/video-editor/commands/projectDataMember.test.ts`

The lowering matches Main's compiler semantics: omitted mode is `replace`,
`merge` recursively combines only two non-null plain-object cells, and arrays,
null, absent leaves, and scalar cells replace. Operations use Main's declared
order rule (ordered ascending, stable source-index ties, unordered last).
Each lowered command reads the raw leaf from the current pre-command recording
state, derives the value from that guarded raw cell plus the declared input,
then emits one closed native `replace` write. It does not fresh-capture or
filter writes.

The existing setup-object recording preserves absent/null/empty distinctions;
the leaf `expect` remains the exact original value/presence guard. Existing
sibling namespace keys and insertion order are retained. Incoming values still
require finite JSON, canonical non-reserved keys, recursively non-reserved
object keys, and the existing entry/count/total limits. A malformed namespace
or any unsupported/mixed operation refuses before returning a capture; the
working clone is not exposed, so no partial batch is committed.

The new assertions cover Main-vs-native recursive merge/default/order output,
sibling order, same-leaf stale refusal, disjoint-key replay preservation,
opaque/null/absence handling, unsafe input refusal, and mixed-batch atomic
refusal. The only changed prior expectation is the now-intended former
`merge` refusal, replaced by the required Main-compatible merge coverage; the
other safety assertions remain intact.

## Cross-repo evidence

The immutable Agent `0a774e4...` and `e010e6a...` refs contain the same
project-data handler/operation contract; their relevant diff is limited to
recording/command/inverse/rebase machinery, not project-data semantics. Source
inspection confirms the setup-container exception is narrow, while exact leaf
guards remain authoritative. The frozen e010 conformance lane was rerun from
one private extraction and passed all 17 tests, including:

- ordered source/source-map batch and atomic refusal;
- absent, null, empty namespace, opaque values, exact inverse and redo;
- disjoint-key replay, same-key ABA refusal, and dependent inverse refusal;
- canonical/reserved/finite/size/count/total validation.

The prior source-freeze parity report's TS-to-Agent 0a/e010 bundle, record,
inverse, redo, and replay matcher is consistent with this source and remains
the claimed evidence; this review did not rerun that separate matcher.

## Tests run

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 2 files passed; 17 tests passed

./node_modules/.bin/eslint src/tools/video-editor/commands/projectDataMember.ts src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
=> passed

git diff --check
=> passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Agent e010 extraction> /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py
=> 17 passed, 2 warnings
```

No full suite, browser, localhost, live socket, Runtime HTTP, activation,
pinning, dependency change, or current integration change was run or made.
Runtime392/provider-door pairing remains required before native activation,
public qualification, or legacy-writer retirement.

## Recommended next step

Qualify this exact lowered batch through the paired Runtime392/Agent provider
and door, retaining accepted-record identity, retry/restart, mixed refusal,
same-leaf stale refusal, disjoint rebase, and exact inverse controls.
