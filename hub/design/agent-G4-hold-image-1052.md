# G4 image-hold media recipe compatibility

## Decision

The Agent occurrence media recipe accepts `clipType: "hold"` only when the
authenticated media selection is an image. The authored `clipType` and
literal `hold` value are retained exactly. Video rows still require the
existing `media`/`video` forms and source-window validation.

## Provenance

- The peer source review identifies the qualified App producer at
  `src/tools/video-editor/lib/timeline-asset-plans.ts:362-389` as emitting
  `clipType: 'hold'` for image rows with `hold: 5`.
- The current Agent source at `ef851b22c` has `_clip` accepting only
  `('media', kind)`, which rejects that authentic image row before any
  Runtime/browser/HTTP behavior is involved.
- Runtime was verified before and after at `49ce53289bc37d9387a7d9e6b9c9b16072162181`;
  no Runtime files or refs changed.

## Change

`astrid/sdk/timeline/native_occurrence_media_commands.py` now admits the
existing image hold recipe in `_clip`. No new command, schema, alias,
executor, default, provider, or service guard was added. Existing ownership,
selection, physical binding, timing, dependency, and inverse paths remain in
place because the change is confined to the clip-type admission predicate.

Focused recipe coverage exercises both occurrence ADD and SWAP with an
authored `hold` row, checks literal hold preservation and inverse restoration,
and verifies that the same spelling remains refused for video.

## Evidence

- Before the implementation edit, the new ADD/SWAP regression failed 2 cases
  at `_clip` with `media edit requires one matching media clip`; the remaining
  refusal cases passed (`36 passed`).
- After the edit: `test_recipe_occurrence_media.py` — `66 passed`.
- Scoped Ruff passed; `make PY=/home/user/work/venv-agent/bin/python ruff`
  reports `current=2149 baseline=2149`; `git diff --check` passed.

## Known lane blockers

The mandated Runtime-backed occurrence-media tests cannot initialize against
Runtime `49ce532`: their setup still calls retired `publish_parent_composition`
and receives `RetiredRouteError` (`48 errors`). The combined focused command
also reports 23 failures in `test_occurrence_media_manifest_inverse.py` from
the existing authenticated physical-binding normalization requirement; that
file was not changed. The Mypy gate is environment-blocked by missing
`types-PyYAML` and incompatible NumPy stubs in the shared Python 3.13 venv.
