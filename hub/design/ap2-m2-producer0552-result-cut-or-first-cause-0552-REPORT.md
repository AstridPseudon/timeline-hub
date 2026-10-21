# App2 M2 producer 0552 result/cut report

## Result: BLOCKED — no producer actual was authorized or submitted

Executor 0552 stopped on the concrete custody HOLD returned by worker 0551. No
same-result producer run exists to inspect, and no retry or unchanged audit was
submitted. The exact prerequisite is a fresh, centrally registered successor
source-preflight plus startup-only smoke for the candidate below, with literal
hash binding for the startup gate, owned startup probe, and exact `tsx`
executable/module bytes. The smoke must prove real Runtime daemon startup,
health, teardown, and zero producer-body execution. Only then can the separate
single original producer actual be authorized.

The 0551 review also requires the successor command to bind or rerun the
complete inherited preflight guards. Its three defects were: absent central
startup-only result, absent literal probe/tsx custody binding, and no named
central suite entry. This is an environment/custody prerequisite, not evidence
of an App product defect.

## Frozen source and original body

- Candidate source worker: `/home/user/work/wt/ap2-m2-producer-realm-physical-path-diagnosis-0538`
- Candidate HEAD/tree: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` /
  `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Candidate wrapper SHA-256:
  `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`
- Original spec/helper/config SHA-256:
  `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`,
  `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`,
  `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`
- Original body: `tests/e2e/local/producer-ownership-current-pin.spec.ts`,
  exactly one test collected:
  `removes only stale owned transcript output and moves only owned scene output`.

The body retains all required assertions: owned stale transcript deletion;
foreign/user row identity, raw fields, and order; owned scene `clip.move` plus
`clip.set` hold update; lost acknowledgement and exact idempotent retry after
reload; guarded Runtime inverse/undo; reload state; and zero legacy save
traffic. No body, helper, config, selector, timeout, option, pin, or assertion
was changed.

## Prior result and current result accounting

The latest completed original actual remains central test ID
`ap2-m2-producer-final-reviewed-run-one-case-0532-ap2-m2-producer-run-mode-closed-repair-0524-actual-1021053231-23729`:
one test collected, zero passed, one failed, exit 1. Its first retained
failure was Runtime startup refusal before the producer action or request body:
`startup_error: realm root must not traverse a symlink`; body count was zero.

0552 produced no test ID, no request directory, and no test count because the
0551 HOLD stopped dependent execution. Therefore ownership/raw/order/reload/
retry/undo/zero-legacy behavior remains unverified by a real producer actual.

## Original body and bounded-cut inspection

The candidate body was read from the frozen source worker. It exercises the
mounted transcript and scene producer controls through the existing direct
Runtime-door harness. The source diagnosis identified the earlier failure as a
symlinked App alias in the temporary realm path; the candidate wrapper changes
only the ephemeral `TMPDIR` carrier to a physical short path. Runtime's
symlink guard remains intact.

No bounded App2 deletion is safe on this evidence. The ordinary snapshot route
is still live at `src/tools/video-editor/hooks/useTimelineOps.ts:316-321`, where
unmigrated operations call `commitData(compiled.nextData, { save: true,
semantic: true })`. `useTimelineOps` is HOME-owned, so no edit or patch artifact
was sent. Its native `genericPatchPort` branch remains live at lines 267-275.
The active head-based provider path remains
`src/integrations/runtime/dataProvider.ts:1014-1030`, and recovery can call it
again at lines 1275-1278. The whole ordinary row therefore stays OPEN until
all producer families migrate and a real PASS proves the zero-legacy assertion.

Changed live callers: none. The inspected callers remain unchanged, including
`src/tools/video-editor/hooks/useTimelineState.ts:830-841` constructing
`useTimelineOps`, the native command consumers wired through
`save.commands.genericPatchPort`, and the existing Runtime provider head-save
path. No App source file was modified.

## Commands and results

Read-only inspection commands:

```text
git -C /home/user/work/wt/ap2-m2-producer-realm-physical-path-diagnosis-0538 status --short --branch
# PASS; clean candidate source, branch tl/ap2-m2-producer-realm-physical-path-diagnosis-0538

git -C ... rev-parse HEAD && git -C ... rev-parse HEAD^{tree}
# PASS; b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 / fd16d32fd3487e56c9fe1ff16582dba240f63b77

sha256sum producer-ownership-current-pin.spec.ts producer-ownership-current-pin.ts playwright.producer-ownership-current-pin.config.ts run-producer-public13-list.sh
# PASS; hashes recorded above

rg -n '^  test\(' tests/e2e/local/producer-ownership-current-pin.spec.ts
# PASS; exactly one test

rg -n -C 3 'Unmigrated operations|commitData\(compiled.nextData|genericPatchPort|saveTimelineInOrder|saveTimelineAtHead' ...
# PASS; live fallback/native/provider paths recorded above
```

No local App tests, browser, build, install, daemon/socket run, full suite, or
central producer actual was run by this worker. The prior 0532 central command
and result are recorded in
`ap2-m2-producer-final-reviewed-run-one-case-0532-REPORT.md`; it must not be
replayed unchanged.

## Recommended next step

The orchestrator should first land or register the exact 0551-required
startup-only custody repair, run that source-preflight/startup smoke once, and
obtain a PASS with real health/teardown and zero body count. Then perform at
most one separately reviewed original producer actual. If that actual passes
every original assertion, prepare a minimal App2-owned dead-writer/helper
deletion with direct-neighbor tests and send a tiny exact patch artifact for
`useTimelineOps`; if it fails, diagnose only its first retained body/request/
launch failure.

