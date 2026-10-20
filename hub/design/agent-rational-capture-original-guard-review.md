# Agent rational capture/original-guard review

Date: 2026-10-20 UTC  
Scope: Agent commit `b96ab3a48f393fefc57e34e022d9970ff0a517de`

## Disposition

**SOURCE-ONLY APPROVE** for the Agent `clip.move` rate fix.

The patch reads the current main spelling in `astrid/sdk/timeline/capture.py`:

```json
{"config": {"output": {"numerator": 30000, "denominator": 1001}}}
```

It first probes `config.output.fps` for the existing spelling, then reads the
whole `config.output` and accepts the direct rational only when its keys are
exactly `numerator` and `denominator`. `rate()` remains the sole parser: it
requires positive integer rational components, or a finite positive numeric
FPS. The patch does not infer a compiled/rendered rate or add a timing policy.

The fixed move keeps the existing quantization policy and half-open geometry:
`clip_start_frame` selects the start frame, and `Fraction(frame, 1) / fps`
converts that frame back to authored seconds. The existing actual-front-end
proof asserts the rational move is `[30, 60)`, contains frames `30..59`, and
excludes frame `60`; it also covers closure persistence, reload, inverse, and
redo.

## Original sealed capture guard

The compatibility concern is safe in the current recorder contract. A fresh
direct-rational capture seals both observations:

```text
parent.config.output.fps  -> absent
parent.config.output      -> {numerator: 30000, denominator: 1001}
```

The smallest executable regression is one direct-rational base, one simulated
pre-b96 command with only the first (absent) read, and one changed direct output.
Run `execute` with the simulated old command both against the unchanged base
and against the changed head. Current behavior visibly refuses both with
`CommandError.kind == "capture_mismatch"`; it never recomputes the move from
the changed direct rational. A current capture against the changed head instead
fails its complete original output guard with `dependency_changed`.

The probe used an immutable `document_fixture()` source, changed only the
direct `config.output` object in detached copies, and produced:

```text
unchanged old sealed capture: capture_mismatch submitted reads does not match authoritative capture
stale old direct-rational capture: capture_mismatch submitted reads does not match authoritative capture
fixed sealed capture after direct-rate change: dependency_changed original authored guard changed
```

Thus an old capture either carries the complete new basis or is visibly refused;
the new fallback cannot silently refresh it. Ledger-first accepted retries and
the existing inverse/rebase checks were not changed.

## Browser contract divergence

There is one concrete adjacent divergence to track, but it is outside this
source-only patch: the Agent browser/render profile contract uses
`fps_rational: [numerator, denominator]`, while the timeline authoring fix
supports the direct `config.output` rational object above. The current App
timeline projection reads numeric `output.fps`, and Runtime visual-seam
normalization also reads numeric `config.output.fps`; neither consumes the
direct object. This is an existing cross-product contract gap, not a reason to
change `capture.py`, add a schema/version, or rewrite a guard here. It must be
resolved before browser capture is claimed to support the direct authoring
spelling.

## Evidence

- `git show b96ab3a48^:astrid/sdk/timeline/capture.py` confirms the old code read
  only `config.output.fps` and defaulted a direct rational to 30.
- `tests/editing_conformance/test_native_sheet_current_runtime.py` is the
  actual Python/CLI/NativeSheet direct-rational proof and asserts the exact
  `[30,60)` boundary.
- Targeted local test:

  ```text
  /home/user/work/venv-agent/bin/pytest -q tests/editing_conformance/test_recipe_m1_commands.py::test_quantization_once_with_rational_fps_and_ms_codec tests/editing_conformance/test_recipe_m1_commands.py::test_exact_authored_move_inverse_redo
  ......                                                                   [100%]
  6 passed in 1.06s
  ```

No full or central browser/live suite was requested, per task instructions.
