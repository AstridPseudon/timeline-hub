# Runtime reciprocal review — complete transition source fcf8

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK — bounded source/tree/schema review for exact Agent commit
`fcf8cc8c1a5458f40c2e40b12009bad70bf42c6b`.**

This ACK covers the committed future-source proposal only. It is not Runtime
schema acceptance, generation, pinning, public allocation, activation, native
execution, or a claim that the transition source runs under the current
private017 contract.

## Exact identity and delta

- Agent source commit: `fcf8cc8c1a5458f40c2e40b12009bad70bf42c6b`.
- Parent: `eebfe1035839b628e472b204c0c204a1d4127e2f`.
- Candidate tree: `236fa26cd9cf3e31c2dc25ef45045f2c155f16a8`.
- Runtime review base: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.

The parent-to-candidate delta is exactly the nine current `b3c96a758` paths
identified by the Agent 1039 review:

```text
astrid/sdk/media_transcript.py
astrid/sdk/timeline_sheet.py
astrid/sdk/timeline_transcripts.py
tests/editing_conformance/test_commit_runtime_occurrence_media.py
tests/editing_conformance/test_commit_runtime_parent_media_swap.py
tests/editing_conformance/test_native_sheet_ordinary_runtime.py
tests/integrations/test_generic_host_remotion_render.py
tests/sdk/test_media_transcript.py
tests/sdk/test_timeline_sheet_native.py
```

Each candidate blob equals the corresponding committed `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40` blob. No transition implementation, schema, generated client, pin, DTO, store, authority, or caller path is in this delta. The transition implementation remains the composed source from `eebfe103`, whose provenance is the independently reviewed corrected `1acc64610019cd13e344a4a4d75e84280b8b7f16` / ca9 source line.

## Schema and private017 boundaries

The candidate Agent schema is unchanged by fcf8:

- complete raw SHA-256: `95193e5a1f90a8072f55deb19f8b7ac63dc5054130c14eab097f0dd73f149729`;
- complete canonical SHA-256: `8500046e82587856c16cd6e241f27c886f9089538884a0b806fa75138a57cb49`;
- 65 definitions / 37 `EditCommand.allOf` clauses;
- transition-stripped canonical floor: `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`, the frozen ed5 floor;
- transition-stripped raw floor: `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`;
- ordinary canonical floor: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

The source is based on Agent `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`,
tree `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`; therefore this complete
source **does require private017 materialization in the containing successor**.
It is not the ordinary-only source. Agent owns any ordinary-only complete
source and no ordinary source was composed here.

`runtime.lock.json` plus all 15 entries named by its `files` map are byte-
identical between fcf8 and 6c. This preserves the normal private017 lock and
client/fixture bytes exactly; it does not make the new transition schema
acceptable under that lock.

## Current Runtime acceptance boundary

Runtime b92's current bundle schema is SHA-256
`6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`.
Its `ClipSetArgs` still admits the hold-only values shape and states that
transition authoring is outside v1; it has no transition SET fields or
transition `schema_source` in that carrier. Thus the exact missing piece is a
Runtime-owned, normally generated and reciprocally qualified successor schema/
artifact for this existing `clip.set` transition carrier, followed by the
normal private017 materialization/qualification. No current Runtime schema,
client, pin, or public artifact was changed or guessed here.

## Evidence

Reused without relabelling:

- Agent review 1039: **154 + 174 + 7** passing focused lanes, plus its exact
  nine-current-blob finding and private017-byte inventory.
- Agent repair 1043: **13 + 1 + 5** passing focused checks, exact nine-blob
  restoration, and the recorded WC8 environment/health-schema mismatch before
  behavior assertions.
- Runtime feature ACK 1038: the corrected transition source/schema fit and
  current hold-only Runtime carrier boundary.

Reproduced from an extracted archive of the committed fcf8 tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  tests/sdk/test_timeline_materialization_schema_union.py::test_only_carrier_additions_separate_union_from_exact_complete_ordinary_source \
  tests/sdk/test_timeline_materialization_schema_union.py::test_write_order_successor_preserves_frozen_10226_schema_bytes \
  tests/sdk/test_timeline_materialization_schema_union.py::test_transition_successor_strips_to_exact_ed5_canonical_schema
```

Result: **3 passed in 1.18s**. The same pure probe verified the exact nine-path
allowlist/blob equality, complete schema hash, and private017 lock plus all 15
locked-path byte equality. No Runtime pytest, full suite, browser, live socket,
renderer, install, generation, pin, public allocation, activation, or native
run was performed.

## Disposition

SOURCE ACK is appropriate because fcf8 is a committed, exactly identified
successor whose only delta from eebfe is the requested nine current b3c blobs;
the reviewed transition semantics, ed5 and ordinary floors, and private017
bytes remain intact. Generation remains **HOLD** until Runtime produces and
qualifies the matching successor schema/artifact, with private017 materialized
in that containing successor. No product write was made in this Runtime
worktree.
