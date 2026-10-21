# Runtime RT03 current6537 reference-source port

Status: source staged on isolated worker branch; native positive remains open.

## Scope

Current Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` receives the exact
reviewed RT03 projection helper from `449d13d291cc3b62ebbdd780d38d8c58732e4e1b`
and its minimal acceptance hook. The helper is a read-model projection of the
Agent-owned closed-v1 parent carrier; it is not a second authoring path.

## Contract retained

The source requires `config.app.astrid.timeline_references`, exact leaf keys,
version `1`, matching `reference_id`, literal role `source`, and an exact
`MediaManifestEntry` pair where `media_id == content_digest` and the pair
occurs exactly once in `dependency_manifest.media`. No display-ID matching,
project catalog lookup, placed occurrence source, or caller-provided media
authority is used.

Projection occupancy is global over `timeline_references`, including foreign
and archived timelines. A pre-existing identity is usable only when the
previous accepted carrier and exact live target row prove that this commit
owns it. Removal uses the same inverse-only-owned-prior proof. Unrelated live
rows and metadata are retained; legacy snapshots use sorted reference IDs and
existing shots. The hook runs in the established transaction after closure and
publish/head advancement, with ledger-first replay still preceding provider
execution and projection.

## Boundary

This source result intentionally does not port raw custody (`f53bf588...`),
materialization, generators, schemas, clients, versions, pins, release, or
native adoption. The exact Agent source tuple
`10226a7f` / tree `e2c08f` / raw `9cb959` / canonical `322733` is reciprocal
SOURCE ACK only. The reviewed raw sibling must be composed later before the
original normal-provider positive can qualify. No fake raw method was added.

## Evidence boundary

Current Runtime commit-port and projection-occupancy guards pass locally. A
direct helper smoke covers projection add, snapshot writing, inverse-shaped
removal, and foreign occupied identity refusal. The donor positive fixture is
not part of this source-only branch because it depends on the excluded raw
capture sibling. No full, socket, browser, render, generation, or native suite
was run.
