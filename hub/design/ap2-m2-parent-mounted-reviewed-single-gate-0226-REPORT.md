# AP2-M2 mounted parent manual ADD single gate

## Result

**BLOCKED. No central case was requested or run.** The existing mounted-drop
runner in the assigned base does not fit the frozen reviewed source cohort, and
the independent negative-conversion review had not produced its required final
approval artifact at the task cutoff.

I did not change the helper, add a wrapper, run a local browser, request a full
suite, install dependencies, or repeat the HTTP SWAP13087 case.

## Approval and source checks

- Author0223 report: APPROVED the valid five-field media-selection mismatch
  correction. Its correction commit is `7e85d89120227f336a2e8dbf8e0ea44d98311da0`.
  The approved cohort recorded there is App `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`
  / tree `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`, Agent
  `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, Runtime/producer
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, and public13 archive
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Independent negative-conversion review0226: no final report, approval, or
  DONE marker was available when this task stopped; its worker was still
  running. Therefore the required two-review approval gate was not satisfied.
- Assigned worktree: HEAD `ce7152ee4bd5c2dc07454d18200d3be8225ca391`, tree
  `b3a8ba54b0af213a7d6be075645e6718446f8fd5`, clean.
- Checked-in `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`
  still guards App tree `78f3784287d78fc92677ebe5eb710d162b0f50ae`, Agent
  `3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
  `202074110717146fc7f08af2306a8dd7f695b0b1`, and producer
  `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`. Its preflight compares the
  current App tree to that stale `78f...` value and would reject before the
  central service starts the selected case.
- The separate existing `normal014-source-common.sh` does contain the final95
  Agent/Runtime/producer and public13 values, but that does not repair the
  stale checked-in mounted helper. The author correction's parent tree is
  `972d...`; the correction commit itself has a different tree, so no exact
  runnable source/helper pair is present in this base.

## Required case preservation

The existing selector is present at
`tests/e2e/local/three-products.spec.ts:1440`:
`M2 real mounted manual video drop: Runtime selection refusal is closed, native
ADD recovers exactly, and undo preserves opaque data`.

The source retains the intended refusal plus valid ADD journey, including raw
media/file selection, the first request/response failure, lost acknowledgement,
restart and exact retry key/body, reload, undo, opaque data, duplicate/add-row
identity, and zero legacy-save assertions. No live caller was changed in this
worktree. The author report lists the existing live callers as
`useAssetManagement.ts`, `external-drop-utils.ts`, `useExternalDrop.ts`,
`useTimelineState.ts`, `useTimelineCommandsService.ts`, and the existing
commit-session/outbox path.

## Verification

Read-only checks performed:

```text
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git show 7e85d8912 -- tests/e2e/local/support/run-parent-manual-drop-evidence.sh
read-only helper/source identity inspection
read-only preflight comparison: expected 78f378... != actual b3a8ba...
```

No central test command was run. In particular, there is no named test ID,
request result, browser result, or actual case failure to report. No local
browser, full suite, install, second run, or source/product test was run.

## Next step

After the reviewed helper/source pair is integrated into the exact final95
cohort, obtain the independent negative-conversion approval artifact, then
request exactly one named central source-bound case with `--no-cache` through
the existing `run-parent-manual-drop-evidence.sh` and selector. Do not broaden
the selector, alter assertions, or use the HTTP SWAP13087 result as App
evidence.
