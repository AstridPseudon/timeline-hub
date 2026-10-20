# Voiceover padding carrier proposal — 2026-10-20 21:47:40 UTC

## Status

UNFROZEN PROPOSAL — peer ACK required before normal voiceover generation.

This note is the bounded prerequisite for the original prepared voiceover
`padding_seconds` value. It does not lower occurrence extent, parent ripple,
media, or any other generated voiceover field.

## Source finding

`prepare_draft_voiceover` returns the caller's original value at
`prepared["padding_seconds"]`. Its detached candidate currently uses the
existing authored voiceover provenance field
`payload.metadata.draft_voiceover`, but does not carry that scalar. The
existing `shot.set` command binds `shot.owner` to
`occurrence:<id>`, records `shot.source`, and writes the whole
`payload.metadata.draft_voiceover` object as one leaf. Supplying only
`{"padding_seconds": value}` therefore drops existing provenance siblings;
it is not a leaf-only nested write.

The exact authored target is proposed as:

```text
occurrence:<occurrence_id>/shot::payload.metadata.draft_voiceover.padding_seconds
```

It is not a root/settings field, an occurrence extent, or a derived timing
mirror. No source mapping, placement array, parent config, DTO, endpoint, or
store is involved.

## Smallest closed extension

Extend the existing occurrence-owned `shot.set` recorder with one nested
scalar path under its already admitted `metadata.draft_voiceover` object:

```json
{
  "values": {"metadata": {"draft_voiceover": {"padding_seconds": 0.15}}},
  "clear": []
}
```

The corresponding explicit clear is:

```json
{
  "values": {},
  "clear": ["metadata.draft_voiceover.padding_seconds"]
}
```

The extension must retain the existing `shot.owner` binding and exact
`shot.source` dependency, write only this nested leaf, preserve every other
metadata/provenance sibling and sibling occurrence, and record the exact
before/after presence state. A finite nonnegative JSON number is the only set
value; `null` is a present value; clear is absence. An absent parent may be
created only for a set, while a present non-object or null parent must refuse
without writes. Clearing an absent leaf is a recorded no-op with exact
absence, and empty containers must retain their original presence/null shape.

The prepared result must first carry the original value into this existing
authored field; the recorder must not recompute it from audio duration or
placement extent. Compile/reload must retain the exact scalar. Strict inverse,
redo, disjoint rebase, same-leaf ABA refusal, and shared-occurrence isolation
are required.

## Executable witness

`tests/editing_conformance/test_recipe_native_voiceover.py::test_original_prepared_padding_has_a_leaf_only_roundtrip_carrier`
is a strict expected failure. It demonstrates that the current whole-object
carrier loses an existing opaque provenance sibling when asked to carry only
the prepared padding leaf, while retaining the original voiceover positives.
It is intentionally not a normal-generation proof.

## ACK request

Runtime and App2 owners: please ACK this exact path and closed set/clear
semantics before activation or freeze. Until ACK, this worker claims no normal
voiceover generation or padding lowering.

## Extent-worker handoff

Extent worker: this proposal owns only the authored
`draft_voiceover.padding_seconds` scalar. It does not claim or modify
`duration_ms`, placement starts, parent duration, child clip extents, or the
ripple time map. The extent command may consume this exact source value after
the carrier is ACKed; it must not infer padding from the prepared extent or
recompute it from audio duration.
