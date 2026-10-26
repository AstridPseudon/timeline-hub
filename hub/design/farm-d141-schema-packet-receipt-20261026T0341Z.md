# Farm receipt: D141 schema packet c1c2a689 (transport verification only)

Result: **PASS_TRANSPORT_CLOSURE** (reviewed verifier 729e8a08, external manager-peer SHA-256). Verification only: no extraction, no binding, no receive-farm census, no child request, no body. NOT Farm READY.

## What was verified (lead, 2026-10-26, read-only)
- Archive `timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz`: 13285 bytes, mode 0644, 1 link, sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f. Identical bytes in ORCH/artifacts (normal sync) and in the hub clone hub/artifacts.
- Verifier `timeline-d141-transport-verifier-729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528.py` (hub/design): 26956 bytes, sha256 729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528 = Runtime's stated hash.
- Trusted manifest `rt-F-D141-Farm-transport-security-sol-0300-source-manifest.json`: 209 bytes, sha256 c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d (matches).
- Command (run in a private 0700 receiving dir with a byte copy of the archive plus its published sidecar): `python3 -I -B <verifier> --verify-archive <archive> --expected-sha256 c1c2a689…97f`, rc 0.
- Verifier output: status PASS_TRANSPORT_CLOSURE; record_rows 18, record_hashed_rows 12; direct_url_sha256 b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e; raw_direct_url_printed false; trusted_manifest_sha256 c9a87be9…60a2; source identity ArtAgents 242f9c4306bf3b501222cb041a9eb246ef47bc85, packages/timeline-schema/python, tree 75a5a697f630affee40632e500b3f5b704a9b834.

## Delivery finding (finite)
The verifier needs the sidecar `<archive>.sha256` NEXT TO the archive. The normal ORCH/artifacts sync carried only the `.tgz` (as Runtime noted); the byte-exact 65-byte sidecar (content = the archive sha256 + newline, mode 0644) is only in the hub clone at hub/artifacts/<archive>.tgz.sha256. I used that published copy in a private receiving dir; I did not create or edit any sidecar and wrote nothing into ORCH/artifacts.

## Not done / still missing (unchanged, not hunted, not substituted)
- Extraction into the receiver stage and binding of SCHEMA_* variables: not done (D141k: custody child chain is conditional).
- Current installed-kit summary + separate PASS_INSTALL original, and the 67-wheel wheelhouse: EXACT-MISSING.
