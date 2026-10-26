# D141 Agent failure guarded two-document CAS validation

Status: **PASS_INSTALLED_EXACT_REVIEWED_CANDIDATES**.

- The source `check_join.py` ran before CAS and passed its exact preimage/candidate assertions; it was not edited and was not reused after replacement.
- Immediate preimage guards matched both regular-0644 authorized files. Candidate hashes, complete prefixes, and single suffix occurrences matched.
- The protected review JSON and `runtime-D141-Agent-failure-protected-publication-1440.json` were `PASS_EVIDENCE`, with declared publication bytes and hashes verified.
- The actual `bin/delivery-build` at SHA-256 `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca` was imported and `render_readme` called function-only with four controlled repositories and missing-gate fallback.
- The 568-file outside inventory was durably serialized before writes. Exact predecessor backups were fsynced before mutation and their directory was fsynced.
- Each target used staged file fsync, atomic replacement, directory fsync, and immediate readback. The after inventory has 568 individually equal outside entries.
- An independent post-CAS audit confirmed both canonical files are byte-identical to the accepted candidates.
- First-tool sampler coverage is a limitation because inspection preceded sampling; the subsequent five-second sampler recorded PID/exit/wait/reap and remained above the 4 GB stop.

No product, test, generated, pin, schema, kit, queue, registry, service, build, staging, clone, ZIP, or worker merge request was created or changed.
