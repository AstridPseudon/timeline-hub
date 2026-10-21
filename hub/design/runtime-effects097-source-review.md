# Agent effects097 source review

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK** for the bounded `clip.set` effects leaf carrier only:
`effects.fade_in` and `effects.fade_out`. No concrete mismatch was found in
the reviewed source contract.

This is not an ACK for Main's coupled `timeline.set_clip_fade` / App
`clip.set-fade` behavior. Coupled entrance/effects/exit parity and live writer
retirement remain **HOLD**; live callers changed by this candidate: **NONE**.

## Exact identities and schema floors

- Candidate Agent commit: `097c68a9fe3641183372657b5f71cbdcb0a5b326`.
- Candidate tree: `55da544815c3ef9cc33942b549e097d77294d3a0`.
- Candidate raw `edit-command.schema.json` SHA-256:
  `9e14ef571b3b2b8b0e4bfb165f8f4ce4deda9c031fe3ff30c686349ece30f0f7`.
- Candidate schema shape: 62 definitions and 36 `EditCommand` clauses.
- Exact pre-effects parent: commit `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`,
  tree `6dd13b552c4f07fff5586b1fa772bdbdf64accba`.
- Parent raw schema SHA-256 (`daec`):
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- Removing only the effects slice reconstructs canonical `daec` hash
  `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`.
- Existing floor assertions remain exact for `84fc0863`, `65bb68ac`,
  `27f2e3ed`, `39211e63`, `613123b2`, and ordinary `6ba7b51e`.

## Bounded source findings

- `ClipSetArgs.values.effects` is a non-empty closed object containing only
  numeric `fade_in`/`fade_out` leaves. Clear permits only
  `effects.fade_in`/`effects.fade_out`; duplicate, unknown, empty, or
  set-and-clear overlap is rejected by the schema/command validation.
- `_effect_values` validates leaves through the finite-number helper, so
  booleans, NaN, infinity, and non-numbers refuse atomically. It refuses a
  present non-object effects value, including an ordered array; it does not
  convert arrays to maps.
- Set on an absent or null parent creates an object. Set on an existing object
  writes only the requested leaf/leafs in deterministic order, retaining
  existing opaque members and their order. It does not read or rewrite
  `entrance`, `exit`, `transition`, `hold`, source windows, or occurrence
  duration.
- Clear on an absent or null parent records an exact absent leaf no-op and
  leaves the parent absent/null. Clear on an empty object leaves the empty
  object. A present null/numeric leaf is removed while opaque siblings and
  order survive.
- The normal recorder captures exact leaf `before`/`after` writes; container
  creation is recorded when set must materialize an absent/null parent. The
  inverse/rebase path therefore restores exact presence, rejects same-leaf
  A→B→A intervening history, and permits the tested independent other-fade
  leaf rebase.

## Main/App boundary comparison

At Main `origin/main` commit `860d43b331fb4422b16bc0dbd7b08666a0c766a0`,
tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`,
`element-adapter.ts:334-344` implements `timeline.set_clip_fade` by writing
effects and also coupling supplied fades to `entrance` and `exit`; its legacy
array fallback is not the Agent carrier contract.

At App commit `f6e3fa14c4e95090f10735b2163aced88e77bb2d`, tree
`58113372d9e028aa71731fb0fd645ce6b241b554`,
`semanticGestures.ts:191-205` emits `clip.set-fade`, rejects ordered effects
arrays, and captures entrance/effects/exit together. The adapter save path
retains that coupled command (`element-adapter.ts:558-563`). The generic
`updateClip` facade and `ClipEffectsTab` remain existing App surfaces; this
packet does not retire or activate them.

## Evidence

Import and collection preflight passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -c '...'
import ok astrid.sdk.timeline._clip_scalar_commands 62 36

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest --collect-only -q \
  -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py \
  tests/sdk/test_timeline_materialization_schema_union.py
159 tests collected
```

Required targeted lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_clip_scalar_fields.py \
  tests/sdk/test_timeline_materialization_schema_union.py
159 passed in 8.27s
```

No full, native, HTTP, socket, browser, renderer, Runtime acceptance, App
activation, generated-client, pin, freeze, or writer-retirement test was run
or claimed. No product, schema, client, pin, generation, freeze, activation,
or source repair was made by this review.
