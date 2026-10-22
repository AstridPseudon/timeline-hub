# V1 timeline schema inventory

Date: 2026-10-22 UTC  
Scope: PLAN v2.1 §3 V1, viewing H0, and `contract/commit-v2.md` §6. This is a
read-only inventory correction. U1 is not merged; no implementation is included.

## Canonical boundary and the four copies

The shared authored/compiled TimelineConfig boundary is Runtime's
`contract/schemas/timeline-config.schema.json`. Its SHA-256 is
`f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1`, and the
four reported paths are byte-identical:

| path | role | bytes | SHA-256 / equality |
| --- | --- | ---: | --- |
| `/home/user/work/runtime/contract/schemas/timeline-config.schema.json` | Runtime boundary artifact | 11662 | `f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1` |
| `/home/user/work/agent/astrid/core/timeline/schema/timeline-config.schema.json` | Agent vendored copy | 11662 | same; `cmp` OK |
| `/home/user/work/app/vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json` | App Python package copy | 11662 | same; `cmp` OK |
| `/home/user/work/app/node_modules/@banodoco/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json` | App installed path | 11662 | same; `cmp` OK; `realpath`/inode is the preceding App vendor copy |

The App `vendor/timeline-schema/typescript/dist/timeline.schema.json` is not a
fifth canonical copy: it is compiled/presentation output, 23,145 bytes with
SHA-256 `fa0c07b91a54b5f5776ebd50ef785be0bef0a634888a0467cb3e6b84f0fedf0b`,
and differs from the canonical Python/Runtime JSON. Runtime's
`contract/schemas/timeline.json` and `shot-composition.json` are envelope/raw
container schemas, not additional TimelineConfig copies. Composition has no
document-schema JSON artifact.

## Ownership and generation map

Runtime provenance records the package owner as
`@banodoco/timeline-schema#TimelineConfig`, version `0.0.2`, source commit
`242f9c4306bf3b501222cb041a9eb246ef47bc85`, source tree
`75a5a697f630affee40632e500b3f5b704a9b834`, and source artifact
`python/banodoco_timeline_schema/timeline.schema.json`. Agent and App runtime
locks map their copies from Runtime's canonical artifact; the Runtime artifact
manifest tracks the canonical digest.

The frozen R4 Runtime candidate has
`generators/materialize_timeline_schema.py`. It is a candidate/post-U1
generator, not a current integration check: current Runtime `tl/integration`
does not contain that file. Its default source is
`/home/user/banodoco/banodoco-workspace/packages/timeline-schema`, which is
absent in this environment. It accepts `--source <timeline-schema-root>` (or
`BANODOCO_TIMELINE_SCHEMA_ROOT`) and reads
`python/banodoco_timeline_schema/timeline.schema.json`; the exact post-U1
handoff is therefore a package root containing that relative artifact, passed
explicitly to the candidate generator or made available at its configured
default. The available App path
`/home/user/work/app/vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json`
is a consumer/vendor copy, not a newly inferred authoritative source, and is
not promoted to one.

Current, honest checks are:

```text
Runtime current: python generators/generate.py --check
Runtime current: python scripts/artifact_manifest.py --check
Runtime post-U1 candidate only: python generators/materialize_timeline_schema.py --check
Runtime post-U1 candidate with handoff: python generators/materialize_timeline_schema.py --check --source <timeline-schema-root>
Agent: python scripts/vendor_lock.py check runtime.lock.json --producer <runtime>
App package: npm run gen:types; npm run gen:python; npm run check:codegen
App package Makefile: make gen  # Python generator only
App Runtime lock: node scripts/vendor-lock.mjs check runtime.lock.json --producer <runtime>
Composition: npm run gen-registry:check  # built-in registry only, not document schema
```

In App, `vendor/timeline-schema/Makefile` target `gen` runs only
`python scripts/gen_python_types.py`. It is not equivalent to both package
generation commands. The package's `npm run gen:types` and `npm run gen:python`
are the separate TypeScript and Python generation steps; `npm run build` also
runs `gen:types` before TypeScript compilation.

The current Agent/App Runtime lock checks report the expected pre-U1 Runtime
commit-pin mismatch, while the four actual artifacts remain byte-equal. This
is integration sequencing, not evidence of schema byte drift.

## Contract §6 locations and project/timeline placement

`contract/commit-v2.md` §6 places optional `meta` on authored payload data at
these locations: parent composition payloads; TimelineConfig payloads at the
parent and internal-timeline levels; shot payloads; occurrence rows; clip rows;
track rows; and registry asset records. Namespace values are opaque JSON
objects, preserved verbatim, with §6's namespace, size, depth, null, and
reference rules. `meta` is not on immutable revision-image wrappers, manifests,
commands, receipts, or the outer envelope.

The addressing contract makes the scope precise. `ref: "parent"` addresses the
parent composition payload, `shot:<id>` a reachable shot payload, and
`internal:<timeline_id>` a reachable child timeline payload. The authenticated
`project_id`/`timeline_id` select the project/timeline commit scope; they are
identity fields, not writable payload locations. Thus project/timeline placement
is at the addressed authored payload scope (`parent`, `shot:<id>`, or
`internal:<timeline_id>`), not in immutable image/envelope metadata. The
contract defines no separate `project.meta` or `timeline.meta` object. If a
separate project-level metadata location is later required, the exact source
need is an orchestrator-approved contract addition; this inventory adds no
field and changes no contract.

The current raw schema maps those locations as follows:

| §6 location | Current raw/container source | V1 inventory status |
| --- | --- | --- |
| Parent payload | `shot-composition.json` `ParentComposition`, lines 151–172; the object is `additionalProperties: true` and contains `config`, `registry`, `clips`, and `occurrences` | Raw parent payload preserves unknown `meta`; Agent must validate the namespace when V1 is implemented |
| Parent config | `ParentComposition.config` → `RawTimelinePayload`, lines 156–159 and 24–74 | Open raw payload; `meta` is an authored sibling, not an envelope field |
| Internal config | `InternalTimelineRevisionInput.payload` → `RawTimelinePayload`, lines 274–285 and 24–74 | Open raw payload; same authored `meta` rule as parent config |
| Shot payload | `ShotRevisionInput.payload` → `ShotPayload`, lines 193–208 | Open raw payload; `metadata`/`provenance` are named open bags and unknown `meta` remains an authored sibling |
| Occurrence row | `Occurrence`, lines 174–191 | Open row; `additionalProperties: true` preserves unknown `meta` |
| Track row | `RawTrack`, lines 76–99, within `RawTimelinePayload.tracks` | Open raw row; compiled track is stricter and currently has only open `app` |
| Clip row | `RawClip`, lines 100–119, within `RawTimelinePayload.clips` or parent `clips` | Open raw row; compiled `TimelineClip` is a separate stricter layer |
| Registry record | `ParentComposition.registry`, lines 160–165, is an open Runtime-managed map; the `{assets: ...}` record wrapper is used by Agent/Composition | Raw registry container is open, but the current end-to-end asset-record path rejects/omits generic `meta` as detailed below |

This is raw-container preservation, not compiled-schema validation. The
compiled TimelineConfig artifact has closed root/track/clip/asset objects
(root lines 138–142; `AssetEntry` lines 492–533), while its existing `app` bags
are open. Open raw payloads therefore cannot be treated as proof that the
current Agent validator, managed renderer, or Composition consumer already
supports §6 registry `meta`.

## Actual V1 gaps and consumer behavior

### Registry asset records

The end-to-end registry-asset gap is concrete in the current Agent and
Composition paths:

1. Agent `astrid/core/timeline/banodoco_schema.py:375-393` defines
   `_ASSET_ENTRY_ALLOWED` without `meta`. `astrid/core/timeline/validators/registry.py:29-40`
   passes each asset entry to `_raise_unknown_keys(..., _ASSET_ENTRY_ALLOWED)`;
   a registry asset `meta` key is therefore rejected by the current validator.
2. Agent `astrid/packs/rendering/actions/render/managed_timeline.py:64-71`
   removes only the fixed `EDITOR_ASSET_METADATA_KEYS`
   (`handle`, `filename`, `pixel_provenance`, `source`, `size`, `size_bytes`).
   It does not remove or validate generic `meta`; after that fixed-key filtering,
   strict registry validation still has the gap above. V1 must preserve opaque
   `meta` while stripping only known render-only editor keys.
3. The compiled `AssetEntry` also excludes `meta` and closes the object
   (`timeline-config.schema.json:492-533`).
4. Composition `typescript/src/types.ts:81-98` `AssetRegistryEntry` has no
   `meta`. `TimelineComposition.tsx:68-73,113-119` resolves and passes known
   asset fields; it has no generic `meta` read. This is an ignore-unknown
   consumer boundary, but its public type does not currently describe the
   contract's registry-record namespace.

### Compatibility reads

`astrid_render_clock`, `astrid_bounds`, `liveScene`, and `astrid_layer` are
Agent renderer compatibility reads, not Composition reads. Bounded source
examples are Agent `packs/rendering/rendering/renderers/remotion/run.py:922-946`
(`metadata.astrid_layer`, `app.astrid_render_clock`),
`packs/rendering/actions/timeline_visualize/composed_frame.py:658-666`
(`config.app.astrid_bounds`), and
`packs/rendering/rendering/renderers/threejs/run.py:189-190,618-619`
(`clip.app.liveScene`); Composition has zero source matches for these names.
Composition currently ignores unknown object keys by not reading them. The
inventory must not attribute these compatibility paths to Composition.

## Minimal post-U1 implementation seams (not performed here)

After U1, and only after the authoritative materialized source/provenance is
available, the minimal V1 seams are:

- Runtime/package ownership: materialize the updated canonical schema and
  provenance through the U1 generator/source handoff; keep the four-copy
  digest/cmp invariant.
- Agent: update `astrid/core/timeline/banodoco_schema.py` and
  `astrid/core/timeline/validators/registry.py` so §6 `meta` is admitted and
  bounded in timeline/track/clip/registry projections; update the managed
  renderer seam only so fixed render-only editor keys are stripped and opaque
  `meta` is retained/ignored rather than treated as render fields.
- App: regenerate package mirrors with the separate `npm run gen:types` and
  `npm run gen:python` commands, then re-vendor through the Runtime lock. Do
  not substitute `make gen` for both generators.
- Composition: update the `AssetRegistryEntry` boundary/type and verify an
  unknown registry `meta` is ignored by the evaluator, unless source review
  identifies a narrower adapter. No compatibility-read implementation belongs
  in Composition.

Runtime raw acceptance must preserve opaque namespaces without interpreting
references; Agent raw/payload validation and the stricter compiled schema remain
distinct concerns. No V1 implementation, generated file, pin, dependency,
version, test, or product change is part of this inventory.

## Evidence summary

The exact bounded evidence and command results for this correction are in the
worker reports:

- `scratchpad/orch/workers/vw-V1-schema-inventory-fix/REPORT.md`
- `scratchpad/orch/workers/vw-V1-schema-inventory-fix/report.md`

