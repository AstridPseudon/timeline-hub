# D141hh P1/P3 notes CAS validation

Status: **PASS_INSTALLED_EXACT_REVIEWED_CANDIDATES**.

- Return-1307 candidates were independently bound to the terminal source publication and the sole controlling return-review-1310 PASS publication; original-1252 candidates were not installed.
- The readonly checker passed before and after CAS with no `--write`; exact installed hashes are README `3c32a426cd21947dfe8a29cec38d9830831b8bbdcd533e3884b7ab762c90ddd4` and gate-results `c610ccb16859599dde480ea3ffde40803ca4347b10914d501b762ec1af8c81eb`.
- Exact 0644 predecessor backups, durable individually hashed 568-entry outside maps, staged atomic replacement, directory fsync, and readback passed.
- Accepted prefixes, one bounded suffix per document, all 32 IDs, ledgers, witnesses, gap and monitor limitations remain conserved.
- `render_readme` passed function-only with controlled agent/runtime/app/composition inputs and missing-gate fallback; caller and production-bin SHA-256 matched `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`.
- The initial sampler attempt terminated before a sample; the corrected retained five-second trace recorded 36 samples above the 4 GB stop and was waited/reaped. This limitation is disclosed, not backfilled.
- No proof result, canonical prose beyond the two authorized files, product test, full suite, build, service, pin, REG0, or ZIP claim was made.
