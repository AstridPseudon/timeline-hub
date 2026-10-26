# D141 final App source custody findings

Verdict: PASS — FULL FINAL APP SOURCE CUSTODY for the generated metadata/provenance scope only.

- F-001 PASS: Candidate `9ada0d906a2efc5cf98b18b112d2d4e9d0657098` has tree `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`, is a normal child of App base `263b728f014040afc9c6b3fdfb54963b93b757eb`, and has the frozen `7ca61bb3280beca21d98a854af266a382f7ce5df` ancestor.
- F-002 PASS: The actual delta from base is exactly `public/install-manifest.json` and `vendor/astrid-browser/provenance.json`; no product, test, lock, generated-client, schema, config, hook, or other App path changed.
- F-003 PASS: Manifest pins are exact and updater `--plan` is idempotent: Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70`, Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`; every other manifest key is conserved.
- F-004 PASS: Agent checkout HEAD/tree and provenance commit/tree are exact and clean. The 160-file vendor set is verified; all 159 direct Git blobs match provenance and vendor hashes, with zero mismatches. The derived public catalog is covered by the normal verifier and author tool reproduction receipt.
- F-005 PASS: Runtime checkout HEAD/tree is exact and clean. The adopted lock has 14 exact mappings; the canonical-15/protected-8/generated/schema/source/test/hook/vendor-payload bytes are inherited unchanged from the independent qualified records and the App base tree. The independent Runtime receipt is 119/119.
- F-006 EVIDENCE GAP DISCLOSED: The detailed Agent peer receiving-inputs note named by the brief was not available in synchronized ORCH/design paths. The lead relay is the recorded authority; the full commit/tree and actual source inputs were independently verified directly, and no missing details were invented.
- F-007 ENVIRONMENT DISCLOSURE: A private Node generator rerun was denied by sandbox `EPERM` while spawning Git against the read-only Agent checkout. No workaround was used. The author’s durable generator log records private/default file-set and byte equality; independent current verifier, Git-blob, provenance, and conservation checks pass.

No finding requires a source or test change. No full/gate/REG0/MAIN GO claim is made.
