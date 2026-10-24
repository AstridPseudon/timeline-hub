## Report — R0 D61

Implemented the approved additive `HistoryEntry.recorder_abi` field:

- Optional integer enum: `1 | 2`
- Python: `NotRequired[Literal[1, 2]]`
- TypeScript: `recorder_abi?: 1 | 2`
- Absence remains legacy-compatible.
- Request, commit result, preview, conflict, and error shapes unchanged.
- No producer/auth/custody changes.

Generated outputs and `contract/artifacts.json` were regenerated normally.

### Identity and digests

- HEAD: `e68cf231641db98a72805a586b51ab5c4fae2c16`
- Final test snapshot tree: `bb35f386027336cbd1ae9baed9f4aa2f04369441`
- OpenAPI unchanged: `302523509996d42fb1d978912f4e6ea022d8ba596896c6cc307161d2cdc5c075`
- Schema: `dada51…c5089` → `3654ca…39815`
- Contract schema digest: `sha256:4118b1…b413d2` → `sha256:867f35…51708b`
- Resource bundle: `b6a155…5b39c` → `e4da5c…51961e1`
- Artifact manifest version: `sha256:9af2df…6eb24` → `sha256:084f3f…a8ade5`

Canonical-15 mapping: unchanged files remained byte-identical; changed files were Python/TS metadata and DTO artifacts only. Exact hashes were verified against e68.

### Verification

- Generator and artifact manifest generation: passed.
- Generator `--check`: passed.
- Artifact manifest `--check`: passed.
- Two regenerations produced identical diffs: SHA `4fb9bd62827f731aa81831071edb3c606f1548fc41868ae8a5bce0dd62e2b895`.
- Schema probe: omitted, `1`, and `2` accepted; `0`, `3`, `1.5`, boolean, string, array, and null rejected.
- Pyright: `0 errors`.
- TypeScript `tsc --noEmit`: passed.
- `git diff --check`: passed.
- Ruff: 160 existing generated-file diagnostics; normalized comparison against e68 showed zero new diagnostics.
- Requested pytest locally: `143 passed`, socket tests blocked by sandbox permission.
- Central targeted run: `148 passed`, 15 recorded-response errors because the allow-listed suite lacked `ASTRID_CHECKOUT`.

Producer qualification and consumer adoption remain held as directed.