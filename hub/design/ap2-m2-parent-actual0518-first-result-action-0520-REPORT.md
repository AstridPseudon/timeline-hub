# App2 M2 parent actual 0518 first-result action

## Result

HOLD: the one authorized parent actual failed before browser/request capture.
This is an execution/setup failure, not a product failure. No legacy writer or
helper cut and no regression fix is justified.

The exact consumed outcome report was:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-finalhash-approved-one-actual-0518-REPORT.md`

Central actual test ID:

`ap2-m2-parent-complete-current-proof-source-0455-ap2-m2-parent-finalhash-actual-0517-1021052152-26621`

Central result: `fail`, exit `1`, elapsed `2s`. The custody gate passed:
service tree, protected keeper, helper hash, and driver hash all matched. The
existing durable driver then returned exit 1 before retaining its disposable
runner log. Its retained evidence has `runner_status=1`, empty
`requests`, `responses`, and `console`, and no trace/error/request summary.
Therefore zero browser tests, HTTP requests, ADD bodies, or product
assertions are evidenced. The first failing boundary is the unchanged durable
driver/environment before runner evidence retention.

The actual preserved every original assertion: exact 404, ADD/raw/opaque,
order, reload, lost acknowledgement, restart, exact body/key retry, undo, and
`zeroLegacy`. The broad parent row remains open. No new actual or retry was
run.

## Exact source and live path

- Actual source worker: `ap2-m2-parent-complete-current-proof-source-0455`.
- Source HEAD/tree: `a304dce02a185a4774ff514d5aa451c9702aa46f` /
  `a3c82aa91f1336b86491191acf857d88c56179b2`, clean.
- Exact test: `tests/e2e/local/three-products.spec.ts:1440-1635`,
  `M2 real mounted manual video drop: Runtime selection refusal is closed,
  native ADD recovers exactly, and undo preserves opaque data`.
- Source-only preflight:
  `ap2-m2-parent-literal-digest-delta-review-0517-ap2-m2-parent-finalhash-preflight-0517-1021051812-12544`, pass exit 0; 76 artifacts verified and exactly one test collected at `three-products.spec.ts:1440`.
- Actual submission command was:

  ```sh
  R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
    ap2-m2-parent-complete-current-proof-source-0455 \
    ap2-m2-parent-finalhash-actual-0517)
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
    ap2-m2-parent-complete-current-proof-source-0455-ap2-m2-parent-finalhash-actual-0517-1021052152-26621
  ```

  The registered command was:

  ```sh
  test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh' | cut -d' ' -f1)" = '2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1' && '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh' run
  ```

- Unchanged live chain: `TimelineEditorCore.tsx:onDrop` →
  `useExternalDrop.ts` → `external-drop-utils.ts:handleFileDrop` →
  `useAssetManagement.ts:placePreparedAsset` →
  `useTimelineCommandsService.ts:commands.addClip` →
  `useTimelineCommandSession.ts` parent-media session/outbox.
- Changed live callers: none. Changed product files: none. Candidate cut:
  none, because no product behavior was observed and zero live/public callers
  were not newly proven.

## Verification

Read-only checks in this worker:

```text
git status --short --branch
→ clean: tl/ap2-m2-parent-actual0518-first-result-action-0520...hub/tl/integration
git rev-parse HEAD
→ bc6f9dd39c7e5154ddf075cb87b7202cf5702e65
git rev-parse HEAD^{tree}
→ 4cd13d09b7cffd60612d8521f1a2921ca4e762d2
git diff --check
→ pass
```

No targeted product test was run because this worker changed no files. No
browser/full/install/local socket/source-copy/shared-dependency mutation was
performed.

## Required prerequisite / next step

Before any future actual authorization, diagnose and repair or explain the
unchanged durable driver's pre-browser exit and missing runner-log retention
in the central execution environment. A future run must use a newly granted
single-actual authorization; do not infer a product result or perform a
writer cut from this execution failure.
