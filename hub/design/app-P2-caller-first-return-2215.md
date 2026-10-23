## Result

READY static P2 row qualification.

- Updated only `full-e2e-three-products` in [suites.conf](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf:75).
- Preserved corrected ordering: hosted build runs before private graph mount.
- Changed graph package probe to use the pinned `$NODE` executable.
- Preserved exact eight-test invocation and P3 row.

## Evidence

- Outer/inner `bash -n`: PASS.
- Outer interception: `argc=2`, `arg1=-c`, payload 12,556 bytes, SHA256 `52bc48c577492f8cc096ae307cf8aa02d16a91322dc5dfe3f0dd33326d2dd589`.
- Node: `v20.19.4`; npm: `10.8.2`.
- Graph: 80 files, version `0.0.14`, generated files absent, resolver paths valid.
- Source/tree: App `e6d72d3d…`, tree `6513960e…`; Agent `079580ca…`; Runtime `2a9e347f…`.
- P2 spec counts: 3 + 3 + 2 = 8; expected hashes preserved.
- Suite file: 247 lines. P3 row SHA unchanged during this work.

Retained actual 3502 remains FAIL-fast before body (`vite: not found`); all eight tests were NOTRUN. No build, setup, backend, browser, service, dispatcher, or body was launched.

Commit message and `DONE` marker created.