# AP2 M2 parent durable result: diagnosis

## Outcome

The one authorized central rerun was submitted exactly once with `--no-cache` and failed before the driver reached a browser case. The service result is `fail`, exit `1`, in `2s`; the service `log.txt` and `runner.log` are empty. Therefore real App coverage is zero: no ADD body, recovery, raw/opaque, undo, or `zeroLegacy` assertion executed. This is not evidence for or against the parent ADD product behavior.

Central command:

```text
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-reviewed-driver-durable-stage-0303/run-parent-manual-drop-evidence.sh run "$PWD"
```

Result packet:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-exact-negative-source-finish-0230-ap2-m2-parent-reviewed-driver-durable-stage-0303-e2e-integration-1021030553-14429
```

No browser, socket, full suite, local replay, alternate suite, second request, assertion removal, or product edit was made.

Service commands and results: `request-test ap2-m2-parent-exact-negative-source-finish-0230 ap2-m2-parent-reviewed-driver-durable-stage-0303-e2e-integration --no-cache` was submitted once; `wait-test` for result `...1021030553-14429` completed with exit `1`. No local App test suite was run because this task required consuming the central result only.

## First failure and classification

This is a staging-driver fixture defect. The durable driver exits at its first App-tree preflight, line 157 of `run-parent-manual-drop-evidence.sh`:

```text
test "$observed_app_tree" = "$expected_app_tree"
```

The preserved `recorded-evidence/source-identity.txt` reports:

```text
tree=6809757f93ca5e166b24b8bc0160ca09005e984a
expected_tree=78f3784287d78fc92677ebe5eb710d162b0f50ae
```

The frozen parent source and the service snapshot both identify App tree `6809757f93ca5e166b24b8bc0160ca09005e984a` (`da6d910f7ab3dfc71142ece7f632d43341238882`). The shared `normal014-source-common.sh` final95 parent guard also expects `6809757f...`. The durable driver’s hard-coded `expected_app_tree=78f37842...` is stale. The failure happens before its source runner, Playwright, Runtime, HTTP, or any test assertion.

The staged driver is otherwise the approved byte-identical 9,218-byte object with SHA-256 `9c3bd0c88df9290d78a3ba5838bb177f90d31494f5a235b9f7ea4682f05b877`; that identity does not make the stale tree constant compatible with the frozen parent source.

## Minimal correction request

App2’s durable-driver/staging owner should regenerate or minimally correct the driver fixture so its parent App-tree expectation is `6809757f93ca5e166b24b8bc0160ca09005e984a`, then repeat the source/custody review against the corrected bytes. No product, timing, `afterClipId`, persistence, or partial-save change is indicated. A new central run requires explicit authorization; this worker did not retry.

The central packet also records external integration refs `agent=04fdd64205b4a2365e50455bd3ac81b027c617f3`, `runtime=be8d254aef249cd421946cbf06ed86d58bc4b307`, and `composition=7bb54bbd64107e5090643ecca1e4d33164173e85`. Because the driver failed before source preparation, these refs are not a behavioral result and are not classified as the first defect.

## Live parent ADD callers

The current mounted path remains:

`TimelineEditorCore.tsx:941` (`onDrop`) → `useExternalDrop.ts:612-630` (`onTimelineDrop` / `dispatchTimelineDrop`) → `useExternalDrop.ts:115` → `external-drop-utils.ts:275` (`handleFileDrop`) → `external-drop-utils.ts:375` / prepared-asset branches → `useAssetManagement.ts:274-309` (`placePreparedAsset`) → `useTimelineCommandsService.ts:458-500` (`commands.addClip`) → `useTimelineCommandSession.ts:271-284` (durable parent-media session/outbox guards).

The driver’s registered callers are `suites.conf:34`, `:42`, `:105`, and `:106`; only `:106` uses the durable driver. The durable stage’s ACTUAL selector collected exactly one intended parent case. The existing legacy ADD path therefore remains live and unqualified.

## Cut decision and boundaries

No legacy ADD leaf was deleted. The required full mounted ADD body and every recovery/raw/opaque/undo/`zeroLegacy` assertion did not pass, or even execute. Duplicate-generation, shared-persistence, serializer, and pin-adoption boundaries remain untouched and unqualified as instructed.

