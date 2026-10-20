# AP2-M2 ordinary visual-fixture membership recipe

## Result

Prepared the smallest source/test correction for the real SceneMarkers ordinary
journey. The existing `seedThreeProducts(..., 'ordinary')` fixture is retained
unchanged: its displayed snapshot contains five visual members — the two
authored parent clips and the three projected clips in `f2-occurrence`.

The production action calls `visualClips(snapshot)` and aligns every returned
visual clip. Therefore the journey's previous four-command expectation was a
membership mismatch. The patch now expects the truthful five-member native
batch, ordered as ten commands: `clip.move` + `clip.set` for each member.

Occurrence selectors are asserted explicitly:

```text
occurrence:f2-occurrence/clip:f2-plate
occurrence:f2-occurrence/clip:f2-agent-clip
occurrence:f2-occurrence/clip:f2-agent-clear-clip
```

All three occurrence members are expected at `on: 6` with `hold: 3`; the two
parent members remain `appClipId` at `1`/`5` and `transitionClipId` at
`6`/`3`. Existing move/hold, Agent intervention, newer local edit, lost ACK,
reload, restart, retry, undo, opaque-data, and zero-legacy assertions remain
unchanged.

## Changed files

- `tests/e2e/local/three-products.spec.ts`: replace the incorrect four-command
  expectation with an explicit ten-command/five-member expectation.
- `src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts`:
  add a focused regression proving occurrence-projected visual clips remain in
  the action membership.

No producer filtering, supported-subset selection, fixture child removal,
shared-seed mutation, UI/API/schema change, or native failure workaround was
added.

## Validation

```text
npm exec vitest run --no-cache --configLoader=runner \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts
PASS — 1 file, 45 tests

npm exec eslint -- --max-warnings 0 \
  tests/e2e/local/three-products.spec.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts
PASS — exit 0

git diff --check
PASS
```

No full suite, browser, localhost, live socket, Runtime-door, dependency,
schema, pin, or central run was performed. The central ordinary run remains
blocked by the already-diagnosed App stale TimelineOps adapter and must wait
for that shared-core fix. Whether the five occurrence members are accepted by
the current Agent/Runtime pair is intentionally unverified here; any native
boundary failure is a prediction until an actual post-adapter trace proves
it.

## Recommended next step

After the stale adapter owner lands the exact peer fix, run one central ordinary
integration gate against this source. If the gate reaches a native occurrence
refusal, report the actual trace and stop there; do not revert to a filtered
subset or change the producer based on prediction.
