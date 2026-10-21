# Agent WC10 custom raw config: existing-carrier correction

Status: **CUSTOM ORIGINAL POSITIVE OPEN; NO EXISTING NATIVE RAW CARRIER**
(read-only source trace, 2026-10-21). This correction replaces the prior
output-derivation proposal. Runtime owns the remote creator; this page records
the Agent-side contract and the unresolved cross-product seam for Runtime/App
HOME ACK. No implementation, schema registration, generated client,
activation, or positive conversion is included here.

## Source contract and upstream behavior

The original `timelines create` positive accepts this exact non-default config
and publishes it as `parent_composition.config`:

```json
{
  "tracks": [],
  "theme_overrides": {
    "visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}
  }
}
```

This is `DEFAULT_CONFIG` in `tests/v10/test_timelines_create.py:24-29`.
The upstream `origin/main` CLI constructs that raw shape at
`astrid/packs/timeline/cli.py:175-192`; upstream
`RemoteTimelines.create_empty` copies the caller config unchanged into the
publication at `astrid/sdk/remote.py:476-546`, including all unknown siblings,
explicit `null`s, and absent fields. The rendering contract says that canvas
and fps are stored at `theme_overrides.visual.canvas`, not at `output`
(`astrid/packs/rendering/docs/SKILL.md:54-70`). The positive therefore proves
authored raw-config roundtrip, not merely equivalent output geometry.

The current native caller's v1 `timeline.init` is a different recipe. Its
schema accepts only the fixed App output object
(`astrid/core/timeline/schema/edit-command.schema.json:2393-2442`), and its
implementation writes only `parent.config.output`, `parent.name`,
`parent.slug`, and `parent.registry.assets`
(`astrid/sdk/timeline/native_initialize.py:7-22`). Converting the canvas to
`output.resolution` would lose the authored `theme_overrides` path and any
opaque config siblings; it cannot claim the original positive's roundtrip.

## Existing carrier trace

On current Runtime, `create_timeline` is the provider-backed initial carrier:
it creates the shell and installs the authenticated empty bootstrap when the
timeline commit provider is enabled (`runtime_protocol/service.py:1697-1743`).
That bootstrap is the pristine native-init basis; it does not accept the
caller's original config. The old raw carrier,
`publish_parent_composition`, is explicitly refused once a tracked head exists
(`runtime_protocol/service.py:2779-2807`, especially the
`timeline_commit_required` refusal at `:2804-2807`). Thus there is no existing
provider-backed path that carries this fixture's raw config into the initial
head.

The smallest **existing** init footprint is therefore v1 unchanged. It
preserves the supported App default only. There is no honest v2 example that
uses the existing `output` field: that would be a lossy projection, not raw
preservation. Do not add a generic root writer, normalize the config, refuse
opaque siblings while calling the result a roundtrip, or silently convert
`theme_overrides.visual.canvas` into `output`.

## Precise unresolved requirement

To close the custom original positive, the paired products need an
authenticated, idempotent initial-head carrier that accepts the caller's full
raw `parent_composition.config` and preserves, exactly:

- the original config path (`theme_overrides.visual.canvas`),
- explicit `null` versus absence,
- unknown/opaque sibling fields and their authored values,
- the existing pristine/ordinal/placement/shot guards, and
- the existing receipt, retry, inverse, and later-edit refusal semantics.

The carrier must be scoped to the authenticated pristine bootstrap and must
not become a generic root replacement writer. Existing
`publish_parent_composition` is the only traced raw carrier, but Runtime
refuses it for provider-backed tracked timelines; v1 `timeline.init` has no
raw-config target. Selecting or designing the next carrier is therefore
unresolved and requires an explicit cross-product decision; this page does
not invent a schema or product change.

## HOME ACK questions

Runtime HOME (`runtime_protocol/service.py:1697-1743` and `:2779-2807`):

1. Confirm that provider-backed `create_timeline` plus v1 `timeline.init` is
   the accepted default path, and that the old publication route cannot be
   used as an unrecorded custom-config escape hatch.
2. Identify the existing Runtime-authorized carrier, if one exists, that can
   pass the exact raw `parent_composition.config` into the initial head without
   a generic root writer. If none exists, acknowledge this as an open seam
   rather than approving output conversion.

App HOME (`src/tools/video-editor/lib/defaults.ts:25-99` and
`src/tools/video-editor/commands/bootstrapCapture.ts:7-27`):

1. Confirm that `DEFAULT_OUTPUT`/`withDefaultTimelineOutput` is an App output
   projection and not evidence that an Agent `theme_overrides` config may be
   rewritten to `output`.
2. Confirm that `captureBootstrap` remains limited to the exact App defaults
   until the raw-config carrier is resolved; do not claim the custom original
   positive is covered by App bootstrap capture.

Until those ACKs and a paired proof exist, keep `timeline.init` v1 unchanged
and keep the custom original positive OPEN. This document makes no product,
schema, or test change.
