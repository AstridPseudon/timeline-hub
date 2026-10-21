# Agent owned-raw reference source review

## Verdict

**APPROVE — source compatibility only.** I found no exact counterexample in
the specified Agent tree or its reciprocal Runtime carrier. This approves the
bounded source seam; it does not claim that the original strict positive is
qualified end to end, that a producer/public adoption/freeze exists, or that
the new operation is accepted by the old `6ba` validator.

## Exact inputs

- Agent commit: `d1f5f7824a5ede5587088735fad6e6870f0b95db`, tree
  `ca825c4bf900400487f9a1ca6b8c1651d63d5a68`.
- Runtime commit: `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`, tree
  `d82f37052847949e77c12e1704c3f27c6dd56a46`.
- Runtime source handoff reviewed:
  `runtime-rt03-committed-carrier-source-handoff.md`.
- The Agent commit changes only the new conformance test and three schema
  compatibility tests (204 insertions, 16 deletions); no source handoff was
  mistakenly added to the repository.

## Agent source boundary

`timeline.reference` is parent-only, `role: source`, and carries exactly the
existing two-field `MediaManifestEntry` shape:

```json
{"media_id":"sha256:<64 lowercase hex>","content_digest":"sha256:<same digest>"}
```

The command schema has `additionalProperties: false`; neither the command nor
its `media` object can carry `media_info`, MIME, size, generation identity,
alias, placement, or a managed-output tuple. The commit provider calls only the
optional Runtime `raw_media_info(pin)` for the exact command pin and constructs
the private `verified_media` row from that result. The unit `VERIFIED` fixture
is therefore a boundary fixture, not a Runtime custody claim.

The native recipe:

- requires `select == "parent"` and an exact digest-equal pin;
- reads the parent asset collection, target asset identity, and target
  namespaced reference path before writing;
- reserves one existing parent asset ID and records the stable owner binding;
- writes only `config.app.astrid.timeline_references[reference_id]` plus the
  existing parent asset registry entry and the exact `reference.media`
  dependency;
- creates no clip, shot, occurrence, track, placement, alias, or managed
  tuple, and performs no generation, freeze, pin, or public adoption.

The empty-parent positive is exact: one created asset, one dependency, empty
placements/shots/clips, and one manifest media entry. Occupied reference/asset
identity refuses atomically. The implementation uses the existing recorder,
created-ID reservation, read/binding guards, ordering, replay, and guarded
inverse machinery; two references retain insertion order and exact inverse /
redo restores it. The source conformance also checks document-to-bundle
round-trip and `_strip_derived` identity. Existing inverse intervening-write
guards cover ABA rather than adding a reference-specific bypass; no new
authority is inferred from equal bytes.

The three schema compatibility probes remove only `TimelineReferenceArgs` and
the new operation before comparing against the prior frozen floor. Thus the
prior floor remains exact while this operation is additive.

## Runtime reciprocal seam

The committed Runtime port is compatible with the same existing carrier and
the existing internal `MediaInfo` result. It is private/request-scoped and
distinct from base-only `media_info` and five-field `selected_media`.

For `raw_media_info(pin)`, Runtime requires the exact pin to occur in the
declared command object, requires same-project `managed` ownership, opens one
CAS descriptor, and verifies regular-file identity, size, full SHA-256, and
stable descriptor identity. Missing, unowned, foreign, malformed, or changed
objects refuse. The memo is request-local. Before acceptance, Runtime
re-reads the captured descriptor, requires the pin in the candidate dependency
manifest, and adds only the captured raw object to the authorized-media set;
existing ledger replay remains first, so an exact retry does not re-read raw
media. Refusal is before persistence/publication/input writes.

The Runtime source changes no OpenAPI/schema/generated-client/endpoint/table
surface. `contract/artifacts.json` is unchanged at 76 entries with SHA-256
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` on both
base and candidate.

## Evidence

Successful bounded probes, run against the exact source trees:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-f53bf588" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --timeout=60 \
  tests/editing_conformance/test_recipe_m2_parent_reference.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py
67 passed in 175.22s (0:02:55)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --timeout=60 \
  tests/test_timeline_raw_capture.py
6 passed in 1.78s
```

Also checked: the Runtime artifact file has identical base/candidate SHA-256
and `git diff --check` is clean. No full, matrix, browser, renderer, live
socket, generated-client, schema-generation, pin, or release suite was run.

## Qualification prerequisites and callers

The real Runtime/Agent qualification must use the exact pair above (one FD
custody path) and prove the declared-pin -> Runtime read result -> Agent
capture -> candidate-manifest -> acceptance recheck seam. It must retain the
normal existing `MediaManifestEntry` contract and must not treat an old
`6ba` validator result as acceptance of `timeline.reference`.

No live caller changes are required or present in this source-only review.
The next qualification step is one concrete paired commit-path probe using
the installed f53 Runtime provider; it must not broaden the operation into
generation, freeze, pin, adoption, placement, or public artifact claims.
