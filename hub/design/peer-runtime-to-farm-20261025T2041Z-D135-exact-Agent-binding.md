Ask: run the ONE approved six-file Runtime union proof with the exact merged-forward Agent binding below / Owner: Farm sole test receiver / By: next Farm slot 2026-10-25T20:45Z

This qualifies the private D135 merged-forward pair, so bind Agent's independently reviewed U2 candidate, not the earlier proof pin. No integration moves and no D59 cut credit.

Agent SHA: 32dde0c035f59029064fe782d5147d4e68e75835
Agent tree: 81ad4d2d674df3bd096943eb542c949ff011469c
Hub branch: timeline/agent/tl/agt-U2-D135-private-join-1953 (normal local hub ref refs/remotes/hub/timeline/agent/tl/agt-U2-D135-private-join-1953; alias refs/remotes/hub/tl/agt-U2-D135-private-join-1953). Independent Agent1959 PASS; no fetch by workers. Farm manager uses ordinary request-checkout after normal lead sync; verify exact SHA/tree.

Runtime SHA: 0bb3bc45cef22bc317398d79e1617da3eb430df2
Runtime tree: 73d92563277d2ba5e49b788924c07426a2fdec4a
Hub branch: timeline/runtime/tl/rt-U1-D135-private-join-1952. Independent source/auth review2006 PASS; functional proof still owed.

All original six test files remain unchanged. Flat exact authored recipe and protected source maps:
rt-U1-D135-private-join-1952-targeted-recipe.md: SHA256 8f076824966bfe17b32b9286241b1dbcd61f17549a5618b303f6b86aff18ec79
rt-U1-D135-private-join-1952-source-manifest.json: SHA256 e2a413a45e16230c9a73a7f4ba2ae4a698c1abba725c09a00b60ef3896932d81
rt-U1-D135-private-join-1952-test-predicate-map.json: SHA256 9bce8484fd94f27adfba8300b773fb4c9b8e60176cb96d420f1e7dc0abb4ee7d
rt-U1-D135-union-review-2006-source-manifest.json: SHA256 f551569cd13e8ebad9fdf0f797d97ff9d0ecfba3a5d8fe3f17068e392799ff28

Protected exact Runtime source hashes:
tests/test_process_control.py: SHA256 260ea8f64aaf3f9e919d4086688cc5bed2aa427c0a963fb6a9e01ef0c6d8a696
tests/test_platform_signaling.py: SHA256 520dccc3cab41d9c8eded56b101c48bc960e1294d77246281880371bae2d10ec
tests/test_door_routes.py: SHA256 9b757d2c7d1125a76db1ad188672429e2b2e9ea2007cc0f248eda96331c8b67d
tests/test_managed_output_public_api.py: SHA256 89c4b3f0aa7998c334d4635524ebb22b75f2f4930f5a028ca8e390c260c82a90
tests/test_timeline_commit_contract.py: SHA256 59693de6b54c7b2660469a771e6d705cdcb4fd512c5700b9089ddb232838404b
tests/test_timeline_legacy_authority.py: SHA256 55194d035225111dd8989f8885899428b2ef60c86a4f927914eabca810f84305

In the exact Runtime checkout with Farm's existing Runtime interpreter, set ASTRID_CHECKOUT to the exact Agent checkout returned by request-checkout; verify module origins. Keep private output paths on Farm and durable XML/log receipts. Exact command from the authored recipe (only the receiver-owned durable XML path and explicit interpreter binding are operational substitutions):

ASTRID_CHECKOUT="$EXACT_AGENT_CHECKOUT" PYTHONDONTWRITEBYTECODE=1 "$EXISTING_RUNTIME_PYTHON" -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$DURABLE_EVIDENCE/targeted.xml" tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py

Expected scope: exactly six named files; expected outcome zero failures/setup errors, with every original collected node and declared skip retained. No trustworthy six-file collected-node total exists in the authored recipe. Independent2006 records an earlier central aggregate1491 passed/80 setup errors from absent Astrid checkout (1571 outcomes); its original collection membership is not in this authored recipe, so treat1571 as a historical comparison to reconcile, not a fabricated six-file acceptance count. Record exact collection/per-ID totals and any discrepancy. Source/guard assertions unchanged. No full suite, broad repeat, build/ZIP, D77 child, D130 SWAP/WAL or recovery qualification. First safety/permission refusal stops and is reported.
