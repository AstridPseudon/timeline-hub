# F D141 final App unit notes installation validation

Status: **PASS_INSTALLED_EXACT_CANDIDATES**.

- Protected App review `app-F-D141-final-unit-notes-review-0909`: `PASS`; no content or custody finding was unresolved. Ordinary Main admission `app-D141-final-notes-host-admission-0902` was present before mutation.
- Runtime 0849 preimages matched exactly: README `13f2b3409d42313dd2ed02d1d479bc5e27cb74f7ec29151e30199428fe0bc776` / 35,560 bytes; gate-results `b29945990c34adc8d8ae0b25f8c6621c4c509f43c84b22adb7dedca141815b47` / 25,966 bytes.
- Accepted private candidates matched exactly: README `48013c7fbcb8f72a7d4371540b50a4abcc43dd8c6274d90726beec82b8f9fc02` / 38,282 bytes; gate-results `506e4461b63e81af490e4b43c5eb7fe2717ebb07825c77d216a59967d863a55d` / 35,582 bytes.
- Both targets are regular non-symlinks, mode `0644`; exact byte backups are in `evidence/backups/`.
- Staged atomic replacements used preimage CAS, readback, rollback staging, and delivery-directory fsync. Rollback was not used. Unknown preimage drift would have stopped before mutation.
- All 568 outside files were individually recorded before and after; path, byte count, mode, and SHA-256 inventories are equal. The installer completed this equality check before final evidence serialization.
- Both candidates preserve the full preimage prefix and append only the accepted suffix. Protected candidate checks retain one disclosure per document, all 32 IDs, balanced fences, and `OWN/N/A` classification.
- Exact production caller function only: `delivery-build.render_readme`, controlled four-repository input. Placeholders resolved, rendered disclosure occurs twice, complete ID table once, and missing-gate fallback retains `Not recorded yet.` with no template placeholder.
- Original 4de/d822 measurements remain original; 82e9 remains separate applicability evidence; the exact two Node findings and exactly three inherited lint findings remain visible. Scope is the narrow finite App unit REG comparison only.
- Continuous five-second available-byte sampling was run with durable fsync per sample; the 4,000,000,000-byte stop floor was not reached. See `disk-trace.txt`.

No real delivery-build invocation, main(), rehearsal, clone, patch/export, bundle, test/service, build, ZIP, product test, source record, repository, pin, ledger, or Git file was changed.
