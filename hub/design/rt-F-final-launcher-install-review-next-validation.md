# F-final corrected launcher installation independent readback

Status: **PASS**.

- Actual installer receipt: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-install-next/evidence/installation.json`; recorded terminal exit `0`; live postimage SHA256 `2df2e13fd9396a99f3a8c6395804b4168344b5d61930ea6d676a27a9fb3e1901`.
- Exact predecessor backup: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-install-next/evidence/backups/suites.conf.preimage`; SHA256 `0495919f9ab694d034ca53d77877c90d5553560ac3bbcbf7e90e8b268e227e15`.
- Live registry has 231 lines. Only lines 230–231 differ from the full preimage, matching `delivery-v2-final` and `delivery-v2-dryrun`; `core-v2-final-integration` is byte-identical.
- All bytes outside those reviewed rows, including the four preserved Runtime proof rows, are conserved. The live selected rows equal the protected candidate row file byte-for-byte, including argv, environment, paths, tails, tuple paths/hashes, digests, and order.
- Canonical source/gate tuples match the required hashes, bytes, mode `0644`, owner `0:0`, and non-following regular-file identity. Current integration heads match the tuple.
- All 11 protected candidate source/helper/caller/inventory/installer artifacts match their authenticated hashes and modes; Python files were AST-parsed only. Canonical README/gate notes match their authenticated hashes and metadata.
- The registry’s authenticated immutable entry is checked against the exact preimage backup; its live metadata remains regular, non-symlink, mode `0600`, owner `0:0`, while its live bytes match the postimage hash.
- Prior actual sampler evidence records the 4 GB floor, 5-second sample window, child exit 0, and waited/reaped state; this readback did not recreate custody or rerun installation.

No sourcechecker, activation replay, builder, dry-run, suite, test, clone, ZIP, or product execution was performed.
