Repaired all four findings in the two allowed artifacts. Status remains **PREPARED / NOT_GRANTED**; no rows installed or original journeys run.

- Require exact Agent079 parent/base, independently qualified source and delta, and dispatched read-only checkout custody.
- Replace substring receipt checks with canonical origins and structured identities binding source, backend, clients, child name, key and root.
- Remove unsupported `scope` and duplicate wire inventory entries.
- Preserve caller bodies, waits, tails, stages, exports and product bytes.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 "$TMPDIR/controls.py"` — **51 controls passed** through the actual D41 validator; modeled identity/path inputs, no validator replacement.
- Unchanged `bypass-0945.py` — parent **ACCEPTED** the design-file exploit; repair **REFUSED** it. The modeled unqualified-parent bypass also changed from acceptance to refusal.
- `real-receipts.py` — authentic retained 0256 receipts passed, read in place.
- `preservation.py` — passed: **60 P2 / 106 P3 fingerprints**, bodies/tails/stages and **248 outside rows**, 466341 bytes, digest `b33d30918d6e2ae039dfa296bc75b1e0b2674828b53f07a16ee029933d5ad734`.
- Eight generated-shell `bash -n` checks, Python compilation, JSON parsing and `git diff --check` against all three task bases passed.
- Product/spec/pin/client/kit blobs remain identical; type/lint checks were reused by identity.

Base: `b2f7113cc28915e232c791ad4b6f885c27143eca`. Final artifact SHA256:

- Python: `715decc20513d6bee477760e339acc544da68e4500d6092ddd1205a9a4de488a`
- JSON: `7bc09e0c5136b9a032a3cc47003ef50fb2d3aa6a0431a30e0623ceb5844438fe`

Decision: retain `qualified_source: null` until a reviewed caller update binds the actual source; manifest self-PASS cannot qualify it. Existing dispatcher metadata supplies source origin, avoiding a new receipt format.

Remaining inputs: reviewed Agent backport, joined App source, snapshot authorization and authentic new child receipts. Also, inherited `installed_sha256` values differ from current live rows; historical values were retained and the discrepancy reported.

Commit message and DONE marker written. Independent cumulative review is next.