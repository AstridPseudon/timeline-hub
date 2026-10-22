# V1 timeline schema inventory

## Canonical boundary

Use Runtime `contract/schemas/timeline-config.schema.json` as the shared
TimelineConfig boundary. Its bytes hash to
`f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1`.

The four reported paths are byte-identical:

- Runtime `contract/schemas/timeline-config.schema.json`;
- Agent `astrid/core/timeline/schema/timeline-config.schema.json`;
- App `vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json`;
- App `node_modules/@banodoco/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json` (a symlink to the preceding path).

The App `typescript/dist/timeline.schema.json` is compiled/presentation output,
23,145 bytes with SHA-256
`fa0c07b91a54b5f5776ebd50ef785be0bef0a634888a0467cb3e6b84f0fedf0b`; it is
not equal to the canonical artifact. Composition has no document-schema JSON.

## Ownership and drift map

The authored package owner recorded by Runtime provenance is
`@banodoco/timeline-schema#TimelineConfig`, v0.0.2, source commit
`242f9c4306bf3b501222cb041a9eb246ef47bc85`, source artifact
`python/banodoco_timeline_schema/timeline.schema.json`. Runtime owns the
inter-repo materialization and digest boundary. The frozen U1 candidate's
`generators/materialize_timeline_schema.py` supports `--check` and
`--source`; current `tl/integration` does not yet contain that U1 generator.

Freshness/generation commands already present:

```text
Runtime: python generators/materialize_timeline_schema.py --check
Runtime: python generators/generate.py [--check]
Runtime: python scripts/artifact_manifest.py [--check]
Agent:   python scripts/vendor_lock.py check|update runtime.lock.json --producer <runtime>
Agent:   python scripts/gen_remotion_types.py  # emits remotion/src/types.generated.ts
App:     npm run gen:types | gen:python | check:codegen  # in vendor/timeline-schema
App:     node scripts/vendor-lock.mjs check runtime.lock.json --producer <runtime>
Composition: npm run gen-registry:check  # registry only, not document schema
```

Agent and App Runtime locks map their copies from Runtime's contract artifact.
Runtime `contract/artifacts.json` tracks its digest. Current lock checks fail
only because U1's expected Runtime commit pin is not the current integration
head; the schema bytes themselves match.

## Nodes and unknown data

- Outer Runtime `timeline.json`: `project_id`, `timeline_id`, compact `shots`
  (`shot_id`, start/duration), and references.
- Runtime `shot-composition.json`: Runtime-owned `project_id`/`timeline_id`
  envelope; `ParentComposition` contains config, registry, clips and
  occurrences; occurrences require occurrence/shot revision/placement/duration/
  track; shot revisions carry open payloads and immutable internal-timeline
  links.
- Shared TimelineConfig: root `clips` and `tracks`; `TimelineClip` requires
  `id`, `at`, `track`; tracks carry id/kind/label/role; `AssetEntry` describes
  registry entry metadata. Registry container ownership remains Runtime
  (`ParentComposition.registry`), with Agent/Composition wrappers for
  `{assets: ...}`.
- Runtime raw payloads and registries are open and preserve unknown siblings.
  Agent retains opaque `app` metadata in persisted data but removes it only
  from the shared validation projection. Agent renderer removes editor-only
  registry metadata before strict render validation.
- Composition/Remotion do not interpret generic `meta`; unknown fields are
  ignored. Explicit compatibility reads are limited to selected `app` and
  `metadata` keys (`astrid_render_clock`, `astrid_bounds`, `liveScene`, and
  `astrid_layer`).

No implementation, generated file, pin, or test change belongs in V1 inventory;
see the worker `REPORT.md` for the complete evidence and exact output.
