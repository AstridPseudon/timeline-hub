## D29 custody/AST review

- **Canonical artifact / fixture lint delta: PASS**
- **Actual production command: FAIL**

Verified:

- Patch: 5,653 bytes, SHA-256 `01c26c4b...763d4dd`; byte-identical to 2110.
- Fixture: 8,709 bytes, SHA-256 `0159a9d7...9d1366a`.
- Manifest: 2,956 bytes, SHA-256 `e3240b2f...4fac4b`.
- Patched maker: 28,041 bytes, SHA-256 `873ddcfa...d70149`.
- Patched requester: 2,735 bytes, SHA-256 `471fd470...b33b5f`.
- Base commit `abd47e68...` is an ancestor of artifact HEAD `c95e205c...`.
- Diff scope is only fixture + manifest; no Runtime source/config/suppression changes.

Checks passed:

- Zero-fuzz patch replay and dual-target `cmp`.
- `bash -n`, five embedded-Python compilations, fixture compilation.
- Default and isolated Ruff: 0 findings.
- Expanded Ruff: 57 → 52; only requested findings removed. Remaining baseline findings: E501=31, E701=2, E702=19.
- Normalized AST equivalence, all 27 assertions, all 14 cases retained.

Production-command failure:

- Manifest lock token is 63 characters: ends `...e330be18`.
- Agent commit `079580ca...` lockfile is 151,418 bytes with SHA-256 `f4fc0a32...e330be18d` (64 characters).
- Private patched requester probe correctly refused with status 2: `REFUSED: invalid lock SHA-256`; no queue file was written.

No 14-case rerun, full suite, browser, build, network, or live production execution was performed. Independent 2117 normal/env-i evidence remains retained. Recommended next step: metadata-only correction of the manifest lock SHA; do not alter the patch, requester, fixture behavior, or Runtime source.