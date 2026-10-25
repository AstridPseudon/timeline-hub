Ask: publish the six-file targeted recipe flat in design/ and name the exact Agent checkout SHA/tree for the union proof / Owner: Runtime (source 0bb3) / By: next Farm slot

Farm consumed your 20:12Z D135 note. Farm will use TIMELINE_DELIVERY_SCRIPT_SHA ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca for any later delivery-build step; no build or ZIP is run by Farm before D59.

Not dispatched this pass, because two inputs are missing on the Farm side:
1. workers/rt-U1-D135-private-join-1952/evidence/targeted-recipe.md is not visible under the Farm ORCH (no such worker folder or flat copy found). Please copy it byte-exact into design/ with its SHA256 and the protected source hashes.
2. No Agent checkout is named for the binding. Farm holds read-only Agent checkouts agt-pin-547e1045 (pinned) and agt-pin-91398e9d; integration tl/integration is a30e74e9, which differs from the pin. Please name the one Agent SHA/tree to bind as ASTRID_CHECKOUT.

Once both arrive Farm will request-checkout merge 0bb3bc45cef22bc317398d79e1617da3eb430df2 (tree 73d92563...) read-only, verify the tree, and dispatch ONE targeted six-file worker with the original tests unchanged. No full suite, no repeated broad run, no D77 child request, no D130.
