# D116 exact NEW4 review verdict

## Evidence fidelity: PASS

The retained proof is faithful to the requested run: Agent `795608e1b9d8077487b26eea50b65c1e79c3f522`, Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` / tree `de2954a0ceadb4455903d9abdfec3b773318a50f`, four exact nodes, admission `5005950976` bytes, one launch, and raw result `3 failed, 1 error in 28.85s` with no passes. Source review PASS and clean custody are retained. The raw XML/log remain private; only hashes and safe fields are recorded.

## Functional result: FAIL

Three cases reach the current public checkout/CLI path and fail at the exact transcript-pin consumer: `native_word_anchor.py:100`, wrapped at line 381 as `CommandError kind=invalid_anchor`. The trace is current seed → authenticated binding/topology setup → public Checkout or commands-file caller → Runtime `commit_timeline` → registered Agent provider → `_hydrate`/`transcript_source` → `compile_authored`/`binding`. This is the same live seam documented by D107. The published D107 owner remains UNKNOWN and the exact persisted record remains EXACTMISSING; do not duplicate the diagnosis or invent a pin, manifest, history row, or private capture.

Gate3 is a separate companion setup failure. `native_checkout_current_fixture.py:79` removes parent occurrence membership and lines 80-88 adds a parent clip; the public `emit_document_commands` path cannot represent the membership change as `doc.patch`. R1 rejects `parent` path `['occurrences']` membership edits with `closure membership and edges require semantic commands`. Safe generic edits are ordinary fields/list operations under `parent/config/tracks`, `parent/clips`/`parent/config/clips`, verified `parent/registry/assets/<id>`, and non-edge fields of an existing occurrence; occurrence membership and occurrence edge identities require the semantic command owner. The exact gate3 topology therefore needs an authored-input/contract/semantic-command decision, not an emitter bypass.

No legitimate companion-only correction is established under the fixed original inputs, topology, predicate maps, tests, guards, shared fixtures, and product. Any correction would require changing the gate3 topology construction or using the semantic-command seam, and the transcript issue requires the existing D107 persisted-record owner. No correction was applied.

No pytest, collection, typecheck, service, browser, full, family, or positive-control rerun was performed.
