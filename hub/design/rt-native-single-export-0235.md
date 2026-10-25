## Report

Created safe packet at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-native-single-export-0235/evidence/`

Includes exact tuple/trees, checkout receipts, source hashes, service versions, command, test membership, bounded parent first-failure record, and byte-preserved XML:

- Original XML SHA256: `43e81d9ba94b729b7770d02ebc4a4fd66e097a6fd06c88f53b0a0ff558b3869b`
- Readiness XML SHA256: `273b9b26dac69b0d1737d91d70dc8ad8c530ffbbcc73a4dfbfff7cebf32a6018`
- Packet size: 38,573 bytes

Validation commands passed:

- `sha256sum -c evidence/packet-sha256.txt`
- `jq empty` on packet and producer manifests
- `cmp` against producer XML and central artifacts
- Exact command comparison against the private producer summary
- Credential/URL pattern scan
- `git status --short` — clean

No tests, collection, browser/service execution, semantic GO review, or new collector were run.

The central log and full summary remain private; only hashes and the exact safe command are exported. Readiness attachment bodies/diagnostics are not copied.

Commit message written to:

`.../workers/rt-native-single-export-0235/commit-msg`

DONE marker created at:

`.../workers/rt-native-single-export-0235/DONE`