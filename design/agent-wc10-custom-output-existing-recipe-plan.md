# Agent WC10 custom output: existing-recipe source proposal

Status: **NO EXISTING PUBLISHED CARRIER FOR THE ORIGINAL CUSTOM POSITIVE**
(read-only source trace, 2026-10-21). Runtime owns the actual remote creator;
this is the Agent-side source contract and smallest-carrier proposal for
Runtime/App HOME ACK. No implementation, schema registration, generated
client, activation, or positive conversion is included here.

## One-screen source contract

The original `timelines create` positive accepts this exact non-default config
and publishes it as the parent config:

```json
{
  "tracks": [],
  "theme_overrides": {
    "visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}
  }
}
```

That is `DEFAULT_CONFIG` in the pre-native positive
(`tests/v10/test_timelines_create.py`, parent of `a9f16a9ae`). Its legacy
writer sends the whole `parent_composition.config` unchanged, followed by
empty `registry`, `clips`, `occurrences`, no shots, and the caller's `-head`
key. The positive therefore proves authored custom canvas geometry, not merely
that a shell exists.

The `a9f16a9ae` stage keeps the shell call but refuses every config except
`{"tracks": []}` before the shell is created, then captures a `timeline.init`
whose output is hard-coded to `1280x720`, `30`, `output.mp4`, `null`, `null`.
The frozen 6ba recipe has the same semantic boundary: `TimelineInitArgs`
requires those five exact output values and `native_initialize.initialize`
writes only `parent.config.output`, `parent.name`, `parent.slug`, and
`parent.registry.assets`.

**Exact missing field:** the existing `timeline.init` command has no accepted
way to carry the original explicit canvas `{width: 1920, height: 1080,
fps: 30}` into the authored Main output settings. Its `output.resolution` is
fixed at `1280x720`, and no init read/write target exists for the source's
`theme_overrides.visual.canvas` path. `withDefaultTimelineOutput` in App can
derive output locally, but it is not a Runtime-accepted recorded carrier.

## Existing Main fields and recording footprint

App Main's actual authored output contract is
`src/tools/video-editor/lib/defaults.ts:25-31`:

```json
{
  "resolution": "1280x720",
  "fps": 30,
  "file": "output.mp4",
  "background": null,
  "background_scale": null
}
```

The App bootstrap capture writes this object at
`parent.config.output` (`src/tools/video-editor/commands/bootstrapCapture.ts:23-27`),
not at `theme_overrides.visual.canvas`. Agent's existing command recorder has
the matching four targets, in this order:

1. read the whole pristine `parent` (`config.clips=[]`, `config.tracks=[]`,
   `registry={}`, `clips=[]`);
2. read/guard `parent.config.output` absent;
3. read/guard `parent.name` absent;
4. read/guard `parent.slug` absent;
5. read/guard `parent.registry.assets` absent;
6. write `parent.config.output`, `parent.name`, `parent.slug`, then
   `parent.registry.assets={}`.

`native_initialize.initialize` also requires ordinal zero, no placements or
shots, and the exact pristine parent. Existing recording/replay/inverse code
already retains tagged absence versus explicit `null`, object key order, raw
unknown siblings, and exact selection/order guards. The Runtime provider's
bootstrap-history check supplies the separate defaults-over-later-edits and
edit-then-undo refusal. These are constraints on the proposed extension, not
permission to loosen the current recipe.

## Smallest proposal: extend the existing recipe, never add a writer

Keep `timeline.init` v1 byte-for-byte and semantically unchanged for the
default path. Add a versioned explicit-output form to the **same** operation
(use v2 if the captured custom input is considered a changed capture
meaning), with the existing five authored output fields and the existing
`parent.config.output` target:

```json
{
  "schema_version": 1,
  "op": "timeline.init",
  "version": "2",
  "select": "parent",
  "args": {
    "name": "Main",
    "slug": "main",
    "output": {
      "resolution": "1920x1080",
      "fps": 30,
      "file": "output.mp4",
      "background": null,
      "background_scale": null
    }
  }
}
```

The caller-side adapter may accept the old config shape only when it is the
precise known custom-canvas shape above, derive `resolution` from its integer
width/height, retain the default file/background fields, and capture this
existing recipe. Omitted config continues to use v1's
`1280x720@30/output.mp4/null/null` defaults. Do not accept a generic `config`
argument, replace the parent root, create a dummy film, or add a second
operation/store/DTO.

The v2 capture must retain the current guard and recorder footprint. It must
refuse, before the shell, any extra or unknown key, explicit null where a
field is absent, malformed/nonfinite canvas member, changed track/row order,
opaque sibling, pre-authored output/name/slug/assets, nonempty placements or
shots, or any accepted history that is not the authenticated pristine
bootstrap. Refusal must leave the original input untouched. A committed v2
retry must replay the original receipt; inverse and inverse-of-inverse must
use the recorded write/absence claims; an edit or edit-then-undo must still
refuse a fresh initialization. No later defaulting may overwrite authored
output fields.

This is a proposal only. Runtime/App HOME should ACK the carrier shape and
whether v2 is required before any implementation or qualification is
started. The current custom positive remains a hold-condition regression until
that ACK and a later paired proof.
