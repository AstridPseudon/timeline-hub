# AP2 M2 ordinary admitted-fixture real gate

## Result

The one requested central gate was submitted against the exact target and
failed before build or test collection. No source change or rerun was made.

- Target: `ap2-m2-ordinary-current-scene-fixture-join`
- Suite: `e2e-m2-ordinary-integration`
- Request: `ap2-m2-ordinary-current-scene-fixture-join-e2e-m2-ordinary-integration-1020213403-2249`
- App tree: `95fc6a28b736c70f29b9387f7f11e759d7719d65`
- Result: exit 2 in 1s; no test counts
- First causal error: the clean central snapshot did not contain
  `scripts/testing/run-central-m2-ordinary.sh`.

The retained central trace is outside the disposable snapshot:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-current-scene-fixture-join-e2e-m2-ordinary-integration-1020213403-2249/`

Its command was:

```text
sh "$PWD/scripts/testing/run-central-m2-ordinary.sh" "$PWD"
```

and its log contains only:

```text
sh: 0: cannot open /home/user/work/wt/.test-ap2-m2-ordinary-current-scene-fixture-join-e2e-m2-ordinary-integration-1020213403-2249/scripts/testing/run-central-m2-ordinary.sh: No such file
```

Therefore the real action emitted none of the ten commands and provides no
evidence for Agent/local/lost-ACK/restart/retry/undo/opaque/transition/
zeroLegacy behavior. No browser, localhost, socket, build, or local script
invocation was performed.

## Pre-request verification

- Worktree was clean at committed `264b1cbb0fbfb5d767d4c27c6abac8104c03b14c`;
  tree `95fc6a28b736c70f29b9387f7f11e759d7719d65`.
- `7d42fcd3a` (owner source) and `8c0e1f799` (ordinary row packet) were both
  ancestors of the target.
- The committed source contains the existing
  `scenePhaseMarkersExtension` admission and calls
  `harness.enableTimelineAuthoring(ASTRID_PYTHON)` before standalone
  `openApp` navigation, including the focused ordering/refusal coverage.
- The prior candidate report records 59 focused tests, lint, and diff-check
  passing; those checks were not rerun here per the no-rerun instruction.
- The requested suite is the reviewed narrowed effective13 runner path, whose
  intended guards are Agent `8130a401bf44a518d5a40ae274d398b8c560be55`,
  Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and Composition
  `0.0.13`. Those guards were not reached.

## Blocker and next step

The target branch needs the reviewed effective13 runner restored as a committed
input before this gate can reach build or collection. After that source-level
repair is integrated, submit one new central request against the resulting
clean target; do not classify this pre-run failure as an ordinary behavior
failure.
