# F-final independent artifact review

## Result

**PASS**, with four non-blocking observations recorded in `findings.md`.

The exact Main ZIP is a regular 16,036,421-byte file. Programmatic SHA-256 is `5bf110face517d044e7d94f7476936af5eb99e76b3d33aebae0f4cea06406d9a`, matching the full sidecar token. ZIP integrity, safe-member enumeration, extracted-byte identity, internal `SHA256SUMS`, and the nested scanner extra all pass.

## Repository proof

All four delivered patches were applied with actual `git am` in fresh private alternates-backed repositories at the exact recorded bases. All four exits were 0, and each applied tree equals the expected final tree. All four bundles verified, exposed the expected `refs/heads/tl/integration`, fetched privately, and their tip trees equal the same expected trees. Full IDs and exits are in `review.json` and `source-manifest.json`; raw command output is `tmp/private-git-review.log`.

## README / contract

The delivered README names the exact final tuple and trees, App option B on `fc24f84994dc36cfae9349112782ab4d91dbc73b`, and later conflicts in Elements removal, AgentChat tests, and Runtime pinning. SWAP, Element, and popup ADD remain visible known gaps. The retained App 32-failure plus collection-error, two-Node, and three-lint disclosure; Agent 397-bad/64-disposition/53-kept contexts; and historical non-retarget boundaries remain visible. C0 §1 and §4 were read from the exact Runtime head; packaging inputs are not treated as v2 wire payloads.

## Findings and custody

Meaningful `git diff --check base..result` returns exit 2 for Agent/Runtime/App because the delivered patch preserves whitespace diagnostics (136/4/44 lines respectively); Composition returns 0. This is disclosed and non-blocking because `git am` exits 0 and patch/bundle/wanted trees are identical.

Main’s genuine release at `managers/runtime/INBOX.md` end and `BOARD-HEADER.md` records direct `bin/delivery-build`, exit 0, the exact ZIP, bases, and all-four tree equality. Earlier service failures/refusals and historical monitor limits remain original and are not substituted. My monitor evidence is bounded: the detached sampler emitted one valid sample before harness reaping; a foreground sampler then emitted 5-second samples and exited 130 on explicit Ctrl-C. The review’s 4GB process-group guard did not trip. No continuous peak or historical backfill is claimed.

No source, product, ZIP, sidecar, canonical note, original clone, or Git internal was modified. No full product tests/typecheck/lint were run; N/A for this read-only packaging validation.
