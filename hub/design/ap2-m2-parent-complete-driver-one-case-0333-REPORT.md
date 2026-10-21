# Parent mounted ADD run report

## Result

The one authorized central run was submitted against the exact source and
failed in the single requested case. I made no product or test edits and did
not retry after the first failure.

- Source worker: `ap2-m2-parent-exact-negative-source-finish-0230`
- Source commit/tree: `da6d910f7ab3dfc71142ece7f632d43341238882` /
  `6809757f93ca5e166b24b8bc0160ca09005e984a`
- Driver: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh`
- Driver SHA-256: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`
- Central result: `ap2-m2-parent-exact-negative-source-finish-0230-ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration-1021033417-13951`
- Result: exit `1`, one failed test, 217 seconds

## Exact command and failure

The exact command submitted was:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-exact-negative-source-finish-0230 ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The registered invocation used the authorized absolute driver, final95
profile, and parent source role. The build and one-test collection passed.
The first behavior packet then failed at:

```text
tests/e2e/local/three-products.spec.ts:1491
page.waitForResponse: Timeout 90000ms exceeded
method=GET path=/media-selection/verified?
```

This occurred in the one case at line 1440:

```text
M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data
```

Retained browser evidence recorded only `POST /media-imports` with status 201
and `GET /media-selection?` with status 200. It recorded no verified-selection
response and no Astrid calls. Therefore the wrong-selection 404 assertion,
native ADD, lost acknowledgement, retry, reload/restart, undo, raw/opaque
preservation, and zero-legacy assertions were not reached or qualified.

Retained evidence is at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/recorded-evidence
```

## Live callers

The parent drop path remains:

`useTimelineState.ts` wiring → `useExternalDrop.ts:dispatchTimelineDrop` →
`external-drop-utils.ts:handleFileDrop` →
`useAssetManagement.ts:placePreparedAsset` →
`useTimelineCommandsService.ts:addClip` →
`commands/commitSession.ts` / `commands/commitOutbox.ts`.

No other parent case was live during the run. No browser process or central
test remained active after the failure. The older parent rows remain registered
but were not invoked.

## Checks and scope

- Verified the source worker was clean and had the exact `da6d910f` /
  `6809757f` identity before submission.
- Verified the durable driver hash above.
- Central test service ran the authorized build and browser case once.
- No local browser, local full suite, dependency install, wrapper creation,
  source edit, retry, or alternate parent case was run.
- The worker worktree remains unchanged; there is no product diff to commit.

## Decision and next step

Following the plan, I retained the exact first timeout packet and stopped
without edits or retry. The run is not a behavior qualification. The next
step is diagnosis of why the mounted drop emitted import and unverified
selection traffic but no `/media-selection/verified` request/response, using
the retained trace and error context; any rerun requires a new manager
authorization after that diagnosis.
