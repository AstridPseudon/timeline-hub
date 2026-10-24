# MAIN affected-node qualification bundle (F-D85/D86)

This finite, source-only handoff prepares one later MAIN test-service qualification batch. It selects exactly 251 canonical nodes from the 550-row rehearsal rollup and keeps all remaining rollup records visible in `batch-manifest.json`; the 126 records whose category is not `NEW-OURS core` are in `deferred_records` and excluded. D23 (ordinal 279), D67 (ordinal 308), and D77 (ordinal 549) remain visible with original cause/status fields.

`main-affected-batch-recipe.sh` uses the existing `p4-d73-pinned-launch.sh` pattern and exact selector argv from `selector-argv.txt`. It runs one pytest body with `-n 3` and unchanged strict `--timeout=45`; there are no per-family runs and no D59 credit. This bundle does not install/request a service, run pytest, alter pins/generated/schema/shared-ledger files, or change product/test/helper bodies.

`submit-input.env` leaves final Agent/Runtime/App/Composition checkouts, the D73 four-SHA manifest, pinned Python/Node, schema, evidence directory, request id, and normal-MAIN authored temporary profile as explicit receiving inputs. The normal profile may differ from rehearsal and must be bound explicitly, never silently substituted.

Current source hashes and observed commit are in `source-manifest.json`; final source-join commits/hashes, D73 receipts, genuine checkout receipts, and parsed-command preflight remain pending the receiving MAIN submission. `hash-manifest.json` covers this bundle and all external inputs used to prepare it.
