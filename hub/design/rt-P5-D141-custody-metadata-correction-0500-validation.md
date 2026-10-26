# D141 P5 custody metadata correction validation

Status: PASS for the finite read-only factual correction. This document does not requalify a source, grant new head/gate credit, or relabel the original 15 REG / 38 own-failure census.

## Immutable inputs and conservation

- Original independent0445 custody: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-F-D141-REG-join-P5-review-0445-p5-custody.json`; SHA-256 `2d5adb2b41ff2e82e7b562f0c2d1092a8cd702dd6c31964a98032141834e53cd`; 10146 bytes. It was not overwritten.
- P5 service request `runtime-d141-p5-cut-1026013331-6934`: retained request/status/exit/result-row artifacts remain in place. Status `pass`, exit `0`, summary `38 passed in 31.02s`.
- P5 XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-d141-p5-cut-1026013331-6934/d66/d141-p5-cut.xml`; SHA-256 `04b7bcea10a693d691a4ccaff85df8c94a0e1e634ea14ae1de87f0a25ddca688`; 38 testcase elements, 38 unique testcase identities, all 38 passed, zero failures/errors/skips/xfails.
- Original inventories remain unchanged: 0107 SHA-256 `ddb475cfabe47921c01580ab75eae68fb10f3eb6d715b5dcc2abdfebc3425a86`; 0116 SHA-256 `b03e68fc35d00404b08bb5f9a09562841410438459b01ec1e508376027effe93`.
- Preserved P5 source tuple: Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / tree `ac5b862744bece65b2e30565db1777bacd60da28`; Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70` / tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`; full source hashes and module origins are conserved verbatim from the original receipt.
- Normal snap is preserved: key `e8182b2e4664b58aeb805c15bf758f90` (32 lowercase hex), tree `ac5b862744bece65b2e30565db1777bacd60da28`.
- P5 measured trace is preserved: first `4633554944` bytes, five-second sampling, periodic samples present, final/terminal `4607021056` bytes, stop `4607033344` bytes, `KEEP`, trace validation `PASS: 9 actual samples`, no heavy marker claim.
- Witnesses were recomputed from retained bytes: start `aea28a0d46dcb84deb7e10888aab05e4f9f53d2e83a7e64c7f182aebbfb09186` and stop `aea28a0d46dcb84deb7e10888aab05e4f9f53d2e83a7e64c7f182aebbfb09186`; both files are 17 bytes and the hashes are equal. Equality is true and is disclosed; it is not a bad citation.

## Mechanical identity correction

Each corrected node ID is formed mechanically as `classname::name` from the corresponding XML testcase element, preserving parameter spelling exactly. This yields 38 unique full pytest IDs once. The sorted-set SHA-256 remains `024cd7c2dd2f90c142727b1825bf5d6ee3ee72384547f6cfc925267586c5075c`. No identity was inferred from a suffix alone. The corrected receipt changes only the metadata presentation plus derivative provenance; request, result, source tuple, snap, counts, trace, custody, and applicability remain conserved.

The published REG validation used abbreviated source identities. They are corrected here to the exact actual `reg.json` identities: Runtime `fa9cd5464a8b37b02f971de375e56be846cd69e2` / tree `124e10dbcd54fb90219e783ec11aa34f8c91590c`; Agent `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` / tree `0a3691a49b63fd7b0c22fb3478e9cf1947f266ed`. Final source applicability remains separately owed.

## Controller blob recovery

Controller commit `2ece450dda33be64fce6c1356bfd3cf5d1417972` was read with `git ls-tree` / `git show` only. Safe authored receipt/source/validation/handoff blobs were recovered byte-exactly under `evidence/recovered/`. Raw XML, logs, service payloads, and credentials were not exported. Byte identity is recorded in `publication-manifest.json` by donorGitblob, SHA256, size, and actualtarget.

## C0 request/closure checklist (unchanged contract evidence)

- request: base pair `base_revision_id` + `base_publication_id`; commands; label; per-step `steps[].patch`; declared `reads`; `merge` = `fields|atomic`; `Idempotency-Key`; `dry_run`.
- commands: semantic commands or `doc.patch`; step patches partition command ordinals and carry prior values; no alternate writer is introduced by this correction.
- accepted/merged closure: authenticated receipt bindings, effects, dependencies, history, and guarded whole/per-step undo remain the required closure records.
- conflict: includes `reason` and `head`.
- invalid: includes `code`, `path`, `hint`, and `suggested command`.
- preview/dry-run: no store, history, idempotency, or head mutation.

No service/queue/registry rerun, source semantic review, test, typecheck, lint, collection, import, preflight, or control rerun was executed for this correction. Production continues to use the actual retained receipts; no new head gate credit is claimed.
