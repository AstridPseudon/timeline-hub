# Agent V1 meta resume repair

The V1 incoming-copy failure was an allowlist/container seam mismatch. The
Runtime-vendored canonical schema already admitted `meta` on `TimelineConfig`,
clips, and tracks, but Agent’s `_TIMELINE_TOP_ALLOWED`, `_CLIP_ALLOWED`, and
`_TRACK_ALLOWED` rejected those known fields.

The repair keeps the shared renderer schema strict:

```text
Timeline.validate/load/save
        |
        +-- validate_timeline_meta_locations
        |      top meta
        |      tracks[i].meta
        |      clips[i].meta
        |
        +-- _known_timeline_payload
               strips only admitted opaque meta before shared render validation
```

Each admitted occurrence accepts up to 64 namespace keys. Namespace keys are
1–128 ASCII characters matching `^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$`; each
namespace value is an object whose descendants are finite JSON values. The
limits are 65,536 canonical UTF-8 bytes per namespace, 262,144 bytes for the
whole object, and 32 nested container levels. Values are never normalized or
interpreted as references. `params.meta` is not visited by this seam.

Unknown container fields remain refused by
`validate_timeline_config_for_container`, while the existing domain passthrough
behavior for unknown top-level load/save fields remains unchanged. Generated
schemas, Runtime pins, and SDK `commit.py` remain untouched.
