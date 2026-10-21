# Agent -> Runtime/App2: bounded effects source packet

Date: 2026-10-21 04:40 UTC

Status: ACK requested for the narrow raw-leaf source contract below. HOLD on
claiming parity with Main's complete `timeline.set_clip_fade` producer: Main
couples `entrance`, `effects`, and `exit`, while this unpublished Agent unit is
deliberately only `effects.fade_in`/`effects.fade_out` through `clip.set`.

## Exact source and floors

- Candidate source: Agent commit
  `097c68a9fe3641183372657b5f71cbdcb0a5b326`, tree
  `55da544815c3ef9cc33942b549e097d77294d3a0`.
- Candidate `edit-command.schema.json` raw SHA-256:
  `9e14ef571b3b2b8b0e4bfb165f8f4ce4deda9c031fe3ff30c686349ece30f0f7`.
  It is a 62-definition/36-clause schema and changes only `ClipSetArgs` for
  this feature.
- Exact pre-effects source: parent commit
  `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`, tree
  `6dd13b552c4f07fff5586b1fa772bdbdf64accba`.
- Pre-effects `edit-command.schema.json` raw SHA-256 (`daec`):
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
  The canonical re-serialization used by the floor test is
  `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`.
- Stripping only this effects slice reconstructs `daec`; the existing source
  floor checks then still reconstruct exact `84fc0863`, `65bb68ac`, `27f2e3ed`,
  `39211e63`, `613123b2`, and ordinary `6ba7b51e` schema hashes. No frozen
  artifact is rewritten.

## Main source trace and the HOLD boundary

The inspected Main App source is `origin/main` commit
`860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
`ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.

- `src/tools/video-editor/runtime/element-adapter.ts:334-344` implements
  `timeline.set_clip_fade`. It preserves an existing non-array `clip.effects`
  object, writes the requested numeric `fade_in`/`fade_out`, and also writes
  `entrance={type:"fade",duration:fade_in}` and
  `exit={type:"fade-out",duration:fade_out}`. Arrays fall back to an empty
  effects object for this legacy operation.
- The current semantic producer was introduced at App commit
  `f6e3fa14c4e95090f10735b2163aced88e77bb2d`, tree
  `58113372d9e028aa71731fb0fd645ce6b241b554`. Its
  `commands/semanticGestures.ts:191-205` emits `clip.set-fade`, rejects an
  ordered effects array, and captures original `entrance`, `effects`, and
  `exit` states together. The adapter saves the already-applied coupled
  config and that command (`element-adapter.ts:558-563`).
- `hooks/useTimelineCommandsService.ts:604` is the generic shallow `updateClip`
  facade; `ClipEffectsTab.tsx` delegates to the separate Entrance, Exit, and
  Continuous fields. No live Main/App caller was changed by this packet.

Therefore this source packet must not say that `clip.set` effects leaves
reproduce Main's coupled `clip.set-fade` behavior. Runtime/App2 may ACK the
bounded leaf carrier only. Full coupled parity is a concrete HOLD until the
three-property command shape and its guards are explicitly reviewed.

## Bounded Agent contract

The only new set shape is:

```json
{"values":{"effects":{"fade_in":0.4,"fade_out":0.8}},"clear":[]}
```

The only new clear names are `effects.fade_in` and `effects.fade_out`. The
effects object is a non-empty closed map with numeric leaves only; unknown
leaves, empty patches, non-numbers, booleans, NaN/infinity, duplicate set/clear
intent, and ordered effects arrays are refused atomically. No `clip.set-params`,
new endpoint, DTO, manifest, client, generated contract, or generic effects
writer is introduced.

The implementation in `astrid/sdk/timeline/_clip_scalar_commands.py:89-119`
has these state rules:

- Set reads the original `effects` property. An absent or null parent is
  materialized as an object; an existing object is patched in place. Existing
  opaque siblings are untouched and the new leaf is appended in object order.
- Clear records the exact leaf before/after. An absent or null parent remains
  absent/null; an absent leaf is a no-op; a present null leaf is removed; an
  existing numeric leaf is removed; an empty object remains an object. Other
  leaves and their order survive.
- A present non-object, including an ordered effects array, refuses for both
  set and clear. There is no silent array-to-map conversion.
- `values` and `clear` remain disjoint. `entrance`, `exit`, `transition`, and
  other original properties are not read or rewritten by this effects-only
  path. In particular, an effects fade is not converted into an entrance or
  exit duration.

The schema describes both fade leaves as raw Main duration numbers in seconds,
with no frame conversion or clamping. This is distinct from the prior audio
`source_offset` evidence: Main's canonical occurrence/source offset is `350`
milliseconds, not `.35`; that metadata is unrelated to an effects fade and
must not be rescaled or reused. Clip `hold` is also a separate source-seconds
extent operation with timing guards; fade leaves do not alter hold, source
windows, or occurrence duration.

## Original reads, inverse, and rebase

The effect handler reads the original parent `effects` state before creating or
patching the container, then records leaf writes with exact `before` and
`after` states. The normal recorder retains the original property read and
opaque values; no snapshot or inferred default is used.

Inverse applies the recorded leaf writes and refuses when the guarded leaf,
original container/read, selection, or dependent history changed. In particular
an A->B->A write on the same fade leaf is still an intervening-write conflict.
An independent write to the other fade leaf can rebase and inverse back to the
prior head. These are the existing `inverse.py`/`rebase.py` guards, not a new
effects-specific guard or Runtime behavior claim.

## Evidence and scope

- Predecessor evidence retained: targeted Agent run **214 passed** and focused
  effects run **20 passed**; `git diff --check` passed.
- This worker's narrow rerun, with the required Runtime source on
  `PYTHONPATH`, was:
  `PYTHONPATH=/home/user/work/wt/agt-m2-effects-source-peer-packet:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_materialization_schema_union.py`
  Result: **159 passed in 9.50s**.
- The same command without `PYTHONPATH=/home/user/work/runtime` stopped at
  collection with `ModuleNotFoundError: runtime_protocol`; this was an
  environment import-path issue, not a test assertion. The corrected run is
  the evidence above.
- No full, browser, socket, renderer, Runtime acceptance, App activation,
  client pin, schema generation/freeze, native qualification, or writer
  retirement was run or claimed. Live callers changed: **NONE**.

## Requested peer response

Runtime: ACK or identify a concrete mismatch for accepting this existing
`clip.set` carrier and its exact absence/null/opaque/order/read/guard rules.
Do not widen it to `clip.set-fade` or infer coupled entrance/exit writes.

App2: ACK or identify a concrete mismatch for preserving the current App
coupled writer/draft while treating this as a future bounded leaf carrier.
Do not claim the App inspector is retired or that a native caller is active.

This is a source-contract handoff only. It authorizes no implementation,
schema mutation, generation, freeze, pin, activation, native proof, or public
release.
