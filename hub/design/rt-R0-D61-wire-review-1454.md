## Report — R0 D61/D62 wire review

- Source: PASS
- Results: PASS
- Final source: `6e8ae0142655eb7a6d10083d2d3ae5d434b5c94e`
- Final tree: `bb35f386027336cbd1ae9baed9f4aa2f04369441`
- Comparison e68 tree: `a2cbedd185c7e576e20ed060d993deba17111b78`

Verified only the approved additive field:

- Python: `NotRequired[Literal[1, 2]]`
- TypeScript: `recorder_abi?: 1 | 2`
- Omission remains legacy-compatible.
- Request, accepted/merged, preview, conflict, and invalid/error shapes are unchanged.
- No producer, source, authentication, or authority claim was added.
- Production `list_timeline_commits()` returns `HistoryPage`/`HistoryEntry`.

Checks:

- Generator twice: deterministic; both diff hashes `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Generator `--check`: pass
- Artifact manifest `--check`: pass
- Schema probes: omitted/1/2 accepted; 0/3/1.5/bool/string/array/null rejected
- Ruff: 162 baseline diagnostics; zero normalized new diagnostics versus e68
- Pyright: 60 baseline generated-client diagnostics; zero normalized new diagnostics versus e68
- TypeScript `tsc --noEmit`: pass
- `git diff --check`: pass

Central corrected suite:

`rt-R0-D61-wire-review-1454-rt-R0-D61-wire-review-1454-recorded-response-corrected-1024145537-21071`

- Same final tree
- `16 passed`
- JUnit SHA-256: `b5f52c0658ac44c09b9e228cd61cccb9b2d33890e933c84e4cbf1dcc9fdf47c8`
- Evidence: [recorded-responses.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R0-D61-wire-review-1454/evidence/recorded-responses.xml)

The earlier central run’s `148 passed, 15 errors` was on the identical tree; all 15 errors were missing `ASTRID_CHECKOUT`. No unchanged passing bodies were rerun.

Exact canonical-15 inventory and digests are retained in [digest-inventory.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R0-D61-wire-review-1454/evidence/digest-inventory.tsv). Primary digests:

- OpenAPI: `302523509996d42fb1d978912f4e6ea022d8ba596896c6cc307161d2cdc5c075` unchanged
- Contract schema: `dada51…c5089` → `3654ca3c68f5b3d2022ee91f532aa388b198033d6ae54cda8d8b25cecf739815`
- Runtime bundle: `b6a155…5b39c` → `e4da5c0edc728869a7e78b5820b36f0a0756e1891af64a4f8c0fc37d705196e1`
- Schema digest: `sha256:4118b1…b413d2` → `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`
- Artifact version: `sha256:9af2df…6eb24` → `sha256:084f3f2510edff28c18d33aac4a459f8aa6df3cb4fd71cba4fb292274ea8ade5`

One uniquely named corrected suite row was added to `tests/suites.conf`; no product files were changed. Producer Sol1450/security qualification remains a separate required gate.