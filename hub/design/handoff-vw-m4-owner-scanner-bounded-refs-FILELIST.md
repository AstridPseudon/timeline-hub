# Delivery file list

Artifacts: `owner_film_cliplook_scan-v1.0.1.zip` and
`owner-film-viewing-tools-v1.0.1.tgz`

Package contents:

- `README.md` — owner prerequisites and exact local run command.
- `VERSION` — `1.0.1`.
- `owner_film_cliplook_scan.py` — standalone portable scanner entrypoint.
- `tests/conftest.py` — explicit `--agent-root` pytest option.
- `tests/test_owner_film_cliplook_scan.py` — synthetic portable CLI and semantic smokes.
- `reference/predecessor-ORCHREPORT.md` and `reference/predecessor-owner-film-cliplook-scan.json` — preserved predecessor report/JSON.
- `reference/extension-ORCHREPORT.md` and `reference/extension-owner-film-differences-scan.json` — preserved three-category extension report/JSON.
- `ORCHREPORT.md` — delivery verification report.
- `FILELIST.md` — this manifest.

The adjacent `.sha256` files contain only the SHA-256 digest of their
respective v1.0.1 archive. The preserved v1.0.0 archives and digests are
outside this candidate and are never overwritten. Archives and digests are
delivery transport artifacts and are not included inside either archive. Both archives are flat,
deterministic packages with zeroed member timestamps and uid/gid metadata.
