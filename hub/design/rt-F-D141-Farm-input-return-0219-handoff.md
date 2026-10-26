# D141 Farm input-producer handoff

Status: `SOURCE_PASS / VENUE_NOT_READY`.

The 01:50Z Farm census had 22 non-pass checks. Agent, Runtime, and App
checkout receipts were `PASS`; only the Composition receipt was `MISMATCH`
because its earlier filename used 39 hex characters. Farm already requested
the corrected normal checkout with the full 40-hex Composition commit.

Use `input-map.json` as the complete 22-row map and `commands.md` as the
owner-command packet. The receiver remains the production caller:
`ops-d140-farm/receive-farm.sh --check-only`, with producer closure delegated
to `ops-d140-farm/receipts.py`.

The next legitimate sequence is:

1. D139a kit owner supplies the current CAS2309/installed2314 installation
   summary and installation receipt.
2. D139a schema owner binds the physical installed distribution, exact
   18-row RECORD, direct_url, and trusted manifest.
3. D139 census owner binds the unchanged 2149 JSON input and its expected
   hash; 2216 remains supporting review only.
4. Farm control-plane owners bind the original dependency wheelhouse, central
   service/suite, D73 dry route, D124 core route, current profile, disk
   witness destination and retained root.
5. Farm receipt owner binds the already-requested corrected full-40-hex
   Composition receipt and its digest. Do not request Agent, Runtime, or App
   receipts again; those closures passed in the actual census.
6. Run the existing pre-child check-only census. Only if it is READY may the
   lead issue the one normal installed-schema child request from
   `ops-d140-farm/commands.md`.
7. Continue through registered-child/import, D134 controls, and the unchanged
   D124 core only under the existing stop gates.

The prepared Composition receipt is in `evidence/qualified-inputs/` with its
provenance manifest. It is not silently substituted into the Farm queue: the
normal receiver still requires its original path, digest binding, worker
metadata, KEEP marker and clean checkout.

Blocked precisely on the external venue/owners listed above. No adapter is
necessary: the existing normal producer supports the portable output shape,
but its actual schema carrier and remaining venue inputs are absent. The
Composition receipt remains pending normal Farm admission; the Agent,
Runtime, and App receipt closures are not blockers.
