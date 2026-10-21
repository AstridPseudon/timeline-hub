# Agent Gate1 stable transcript-word anchor ingress

Status: bounded capture-present ingress implemented on Main0146ef.

The attached Python checkout now accepts `clip.set(on=...)` only for the
existing registered `clip.anchor` argument envelope:

```python
{
    "field": "on",
    "declaration": '"again"',
    "choice": {
        "source": "occurrence:<id>/clip:<id>",
        "document": {"document_id": "transcript:<sha256>", "version": 1,
                     "content_digest": "sha256:<sha256>"},
        "word_ids": ["word:<sha256>"],
    },
}
```

The command remains `clip.anchor`, with its existing `anchor: follow` intent,
and is now admitted by the attached parent publish allow-list. The existing
command engine still validates ownership, the exact `DocumentPin`, stable word
IDs, source/media identity, interval bounds, and the existing pinned document
capture before the outbox write. `on=None` maps to the existing clear form.
Occurrence-owned clips, text-only values, malformed carriers, and mixed
`.set` calls refuse before mutation; the draft and outbox remain unchanged.

No schema, operation, DTO, pin, source resolver, CLI, sheet path, cache
authority, or legacy save behavior was added. The current SDK has no
non-mutating historical document read: `documents.show` reads the current
document only, while `fetch_bundle` does not materialize
`source_mapping.pinned_documents`. Consequently a fresh or restarted
attached outbox whose exact transcript capture is not already in the fetched
bundle cannot safely preview/replay a word anchor after V2, source removal, or
lost acknowledgement. The smallest missing unit is an existing-authority
SDK read/materialization seam for the exact retained `DocumentPin`, including
its verified bytes; adding a new command field, inline transcript, latest
document fallback, or cached timing would violate the settled contract.

Evidence:

- `tests/sdk/test_timeline_native_checkout.py`: 23 passed, including exact
  carrier capture/publish, clear, missing-capture refusal, text-only refusal,
  and mixed-call draft preservation.
- `tests/editing_conformance/test_native_word_anchor_vectors.py`
  `tests/sdk/test_timing_compiler.py`: 55 passed.
- Central named suite
  `gate1-word-anchor-native-ingress-main95bd-seed80973`: 4 passed in 7.04s
  against Runtime95bd3c5f. The first direct 95bd run exposed only the legacy
  seed fixture's `destination_occupied` setup incompatibility; the corrected
  run used a disposable 80973 seed archive and left the service under test on
  Runtime95bd.
