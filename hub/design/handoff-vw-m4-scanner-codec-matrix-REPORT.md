# Agent scanner 1.0.7 codec matrix diagnosis

Date: 2026-10-20  
Worker: `vw-m4-scanner-codec-matrix`  
Agent source: `/home/user/work/wt/vw-m4-scanner-codec-matrix`, HEAD `86405964e`  
Scope: read-only diagnosis for the private scanner 1.0.8 repair; no Agent product files changed and no owner data used.

## Finding

The rejection is valid. Agent has a strict authoring codec and a permissive/presentational stored decoder, not one single stored-value validator:

- `FieldSpec.to_stored()` (`astrid/core/timeline/clip_fields.py:62-63`) dispatches to strict `_number`, `_animation_value`, `_audio_fade_value`, or `_transition_value`. It rejects the representative bad values in the matrix, but it also accepts human numeric strings, so it cannot alone establish stored JSON shape.
- `FieldSpec.from_stored()` (`:65-66`) calls `_human`; it formats values and deliberately does not enforce stored ranges or animation identity. Strings, lists, booleans, and malformed mappings can be normalized or emitted as human text. `clip_fields.describe()` (`:555-569`) has the same presentation role. Its exceptions are useful decode failures, but its success is not validity.
- `clip_fields.read()` (`:492-498`) only reads a dotted path and performs no value validation.

The current 1.0.7 `_unreadable_look_names()` calls `describe()` only and checks `spec.stored_at` only. That misses `stored_at_audio` and fails open for values that `describe()` formats or omits. The exact audio duration paths are `params.fadeIn` and `params.fadeOut`, declared by `fade_in`/`fade_out` in `clip_fields.yaml`; the curve paths are `params.fadeInCurve` and `params.fadeOutCurve`, but curves are not FieldSpecs. They are hard-coded in `clip_fields.write()` (`:512-518`) and `timeline_cuts.py` (`:192-196`, `:751-759`).

## Declared storage map

Visual declared fields are `opacity`, `entrance`, `exit`, `cropTop`, `cropRight`, `cropBottom`, `cropLeft`, `speed`, `volume`, and `transition`; `fade_in`/`fade_out` are visual aliases for `entrance`/`exit`. The scanner's 1.0.7 `_LOOK_NAMES` includes opacity, entrance, exit, both fade aliases, all crops, and speed; it intentionally does not include volume or transition in that look list.

Audio fade durations use `FieldSpec.stored_at_audio`:

| authored field | stored path | strict seam |
| --- | --- | --- |
| `fade_in` | `params.fadeIn` | `FIELDS["fade_in"].to_stored(raw, audio=True)` |
| `fade_out` | `params.fadeOut` | `FIELDS["fade_out"].to_stored(raw, audio=True)` |
| `fadeInCurve` | `params.fadeInCurve` | `audio_curves.validate(raw)`; no FieldSpec |
| `fadeOutCurve` | `params.fadeOutCurve` | `audio_curves.validate(raw)`; no FieldSpec |

For shared visual storage, use `FIELDS["entrance"]` for `entrance` and `FIELDS["exit"]` for `exit`. Do not use the visual `fade_in`/`fade_out` alias codec to probe all values at those paths: that codec intentionally rejects non-fade animations such as `scale-in`.

## Targeted adversarial outcomes

The complete machine-readable matrix is in [handoff-vw-m4-scanner-codec-matrix-input-matrix.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-codec-matrix-input-matrix.json).

- Visual numbers: `to_stored()` rejects `"BAD"`, lists, booleans, and out-of-range values. `from_stored()`/`describe()` raise for bad strings/lists, but booleans may be treated as defaults (`opacity`/`speed`) or formatted as `1` (`cropLeft`); numeric bounds such as `opacity=1.5` and `cropLeft=-0.1` are formatted without rejection.
- Visual animations: `to_stored()` rejects bad strings, lists, booleans, unknown types, bad duration strings, and zero durations. `from_stored()`/`describe()` accepts scalar/list/bool/unknown-type values as text; malformed duration can raise, while zero duration formats as `0s`.
- Audio fade durations: `to_stored(..., audio=True)` rejects bad strings, lists, booleans, zero, and negative durations. `from_stored()`/`describe()` raises for bad strings/lists but formats booleans and non-positive numbers.
- Audio curves: `audio_curves.validate()` rejects unknown strings and non-hashable/non-registry values; `describe()` does not call it and appends a truthy raw curve to its human text. The shipped 1.0.7 policy explicitly keeps an unknown string curve as `knowledge: unknown`/complete, so retain that existing policy while failing closed for shape-invalid forms unless the orchestrator changes it.
- Explicit `None`: `cf.write(..., None)` deletes the declared path; `describe()` omits it. Missing and null are absent declarations, not malformed values.
- `params` is open authored/extension data. The shared schema accepts additional `params` keys, and validation strips only its temporary validation projection. Do not inspect, strip, or rewrite unknown extension data.
- Transition policy is separate: `cf.coerce()` and `validate_timeline()` reject unknown catalog IDs, but scanner policy intentionally retains free-form string IDs/types/mappings. Do not route the scanner transition inventory through those closed seams.

## Exact reuse recommendation for scanner 1.0.8

1. Enumerate each present declared FieldSpec path, including `stored_at_audio`; deduplicate `entrance`/`exit` aliases.
2. For each visual path, run the matching general FieldSpec's strict `to_stored(raw)` probe. For each audio fade path, run the matching fade FieldSpec with `audio=True`.
3. For the two curve paths, run `audio_curves.validate()` separately. Missing/null/`linear` retain existing absence/default behavior; preserve the existing unknown-string curve finding policy.
4. If stored JSON shape must reject numeric strings, use the existing `FieldSpec.schema` as a per-field Draft-07 shape check before `to_stored`. These are Draft-07 fragments; `jsonschema.validate()` with the environment default draft raises `SchemaError` for their type arrays. Do not invoke whole-document `validate_timeline()` from the scanner.
5. Keep `describe()` only as presentation after probes. On failure, add one bounded authored source-path error, mark the affected finding unknown, and set `status: incomplete`; never emit raw malformed values or exception text.
6. Keep the single `project_runtime_parent_composition()` closure, explicit clears, open extension data, and free-form transition policy unchanged. Do not add a second validator or rewrite the scanner.

This recommendation is a direct seam reuse, not a new Agent policy or product change.

## Evidence

Targeted command results:

```text
/home/user/work/venv-agent/bin/python -I -B - <<'PY' ... direct clip_fields/audio_curves probes ... PY
PASS: emitted the matrix observations; no files or caches written.

/home/user/work/venv-agent/bin/python -I -B - <<'PY' ... Draft7Validator(FieldSpec.schema) probes ... PY
PASS: schema rejects malformed types/ranges and accepts valid numeric/animation/fade values.

/home/user/work/venv-agent/bin/python -I -B - <<'PY' ... FieldSpec.to_stored probes ... PY
PASS: strict codec rejected all targeted bad authoring/stored candidates; numeric strings remain intentionally accepted as human input.
```

No full suite, browser, renderer, network, local listener, install, owner-film run, or shared dependency mutation was performed.

## Notification

The paired notice file is [handoff-vw-m4-scanner-codec-matrix-NOTICE.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-codec-matrix-NOTICE.md). The independent scanner 1.0.8 repair worker can consume the report and JSON directly.
