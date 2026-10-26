# D141 corrected identity-evidence firstreturn

PASS — bounded read-only identity/hash proof for App candidate `9ada0d906a2efc5cf98b18b112d2d4e9d0657098` / tree `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`.

The actual immutable Git identities are Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70` / tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a` and Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / tree `ac5b862744bece65b2e30565db1777bacd60da28`. The App candidate’s provenance blob and installer manifest agree with those full values. Vendor custody is 160 files with 159 direct Agent Git-blob hashes; Runtime custody is 14 exact lock mappings. The App delta is exactly `public/install-manifest.json` and `vendor/astrid-browser/provenance.json`.

Correction recorded: author0022 adoption/source-custody/handoff and independent0029 review/source-manifest retained a 39-character Agent tree prefix `2ebe2ddf5a61f013953ab1e21d51ebaab746e58`; the actual Git tree is the 40-character `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`. Original file hashes and byte counts are in `identity.json` and `correction.json`; originals were not rewritten.

Disclosures: author0022 had an ENOBUFS attempt on a large PNG before its later large-buffer control; reviewer0029’s private generator rerun received EPERM while spawning Git. Neither is silently counted as a pass, no workaround was attempted, and the current proof is read-only Git/blob/hash validation. Prior bounded source proofs are reused at their recorded scopes; no semantic review, full suite, safety qualification, or MAIN GO claim is made.
