# Validation

## Archive identity

- `python3` streamed SHA-256 of the immutable ZIP: `5bf110face517d044e7d94f7476936af5eb99e76b3d33aebae0f4cea06406d9a`; byte count `16036421`; regular file mode `0600`.
- Sidecar is a regular `0644` file, 197 bytes; its full programmatic SHA token equals the computed archive SHA.
- `zipfile.ZipFile.testzip()` returned `None`; 12 unique safe regular members; no unsafe paths or duplicate names. Extracted staging bytes equal ZIP member bytes.
- Internal `SHA256SUMS` authenticated all 11 non-checksum members, including README, four patches, four bundles and two extras. Nested owner scanner ZIP has two unique safe members and `testzip()` PASS.

## Git patch and bundle routes

Each route used a fresh private repository with the original repository object database as a read-only alternates source. No original clone was fetched into or mutated.

- Agent base `64197afa297f86f1e738238d5e80aff6d33e303a`, patch `git am` exit 0, applied synthetic head `bc4dd3454211da7faae49ba74053c455fa0211f3`, tree `83b84c79941917fde535ee3ddba5533a776cace3`; bundle verify/list/fetch exits 0, tip `ec0a9f5baef2c31bc5179087b83f044524575182`, tree same.
- Runtime base `fa9cd5464a8b37b02f971de375e56be846cd69e2`, patch `git am` exit 0, applied synthetic head `0dbccb5d83b2695415d0d33eff82d7f7953ce3a5`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`; bundle verify/list/fetch exits 0, tip `95d98f038320d5d46bd679ac000ab3e15825c935`, tree same.
- App base `fc24f84994dc36cfae9349112782ab4d91dbc73b`, patch `git am` exit 0, applied synthetic head `91e02aaf753d9fa8e7cfe6a54f0fe10919e392f1`, tree `e2632a4fbe63cadbd03b03edc5d34196a37304fd`; bundle verify/list/fetch exits 0, tip `abac6c809da25f4c6cc7cce61a7d5ea2ac067067`, tree same.
- Composition base `67b8aa3d0d6831d3e3504a340ff583c3da253707`, patch `git am` exit 0, applied synthetic head `7e59ec762688b43d7d26a98783289a30007e7125`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`; bundle verify/list/fetch exits 0, tip `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree same.

Meaningful `git diff --check base..result` exits: Agent 2 (153 diagnostics lines), Runtime 2 (4), App 2 (56), Composition 0. These are whitespace-only diagnostics; they do not alter the authenticated trees.

## Scope

No full product suite, browser, live socket, typecheck or lint was run; those are N/A for this read-only packaging review.
