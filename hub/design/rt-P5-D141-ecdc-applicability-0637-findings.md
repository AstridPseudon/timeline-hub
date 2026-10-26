# P5 D141 successor source applicability

## Verdict: PASS_SOURCE_APPLICABILITY

This is one finite, read-only applicability finding for the bounded successor
`Agent 8585ed9c0404d0187b2ce70242d25114a32747c2` → genuine normal Agent
`ecdc242ed9b673f641759ecf029f95e89a2c6f92`. The production caller’s retained
P5 source closure is unchanged across that successor. The original P5 body is
not retargeted and no new P5 receipt is created.

## Findings

1. The exact requested Agent diff has only three modified paths:

   ```text
   M  runtime.lock.json
   M  tests/timeline/test_authoring_feedback.py
   M  tests/timeline/test_authoring_media.py
   ```

   It is three one-line replacements. The two test-only replacements rename a
   local fake-session method from `_bundle` to `_capture_bundle`; they do not
   touch the retained P5 Runtime tests, provider, capture, or commit source.

2. `runtime.lock.json` changes only `source_commit`, from Runtime
   `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` to exact Runtime
   `95d98f038320d5d46bd679ac000ab3e15825c935`. Its 15 consumer/source/hash
   payloads, manifest, producer, and producer version are unchanged. The
   successor lock is mechanically checked against Runtime 95d’s
   `contract/artifacts.json` and all 15 exact Runtime source bytes: 15/15
   match. These payloads are source custody evidence only, not a new body or
   REG0 result.

3. The 15-entry Runtime manifest is byte-identical at Runtime 6a and Runtime
   95d (`sha256:9bbce65e5b8dd4fd7ca1f24105ffb88d341e5d5beb10348e555dda79145c4dd3`),
   so the lock pointer is an authenticated source selection, not a manifest
   or artifact-content change.

4. The retained Agent production/provider boundary is unchanged at the
   successor. Exact Git blobs and SHA-256 bytes for `astrid/sdk/timeline/api.py`,
   `astrid/sdk/timeline/capture.py`, `astrid/sdk/timeline/commit.py`,
   `astrid_runtime_client/generated.py`, and
   `astrid_runtime_client/contract_metadata.py` are equal at 8585 and ecdc.
   Runtime’s provider imports `astrid.sdk.timeline.commit`; the P5 tests
   explicitly import Agent capture and commit helpers. No changed successor
   blob is on this closure.

5. Runtime 6a → 95d has exactly three changed paths: generated
   `conformance/typescript/contract-metadata.ts`, generated
   `conformance/typescript/generated.ts`, and `runtime_protocol/upgrade.py`.
   The generated TypeScript files are not imported by the retained P5 path.
   `upgrade.py` is imported by the crash setup, but P5 calls
   `migrate_canonical_to_current` at
   `tests/test_timeline_commit_crash.py:81`; the changed
   `_validate_candidate` hunk is called from `upgrade_realm` only. Therefore
   the changed Runtime hunk is not executed by the retained P5 migration
   route.

6. Collection/lanes resolution is explicit. P5’s pytest process loads Runtime
   `tests/conftest.py` and Runtime `tests/lanes.py`. Runtime
   `tests/astrid_checkout.py` only prepends `ASTRID_CHECKOUT` for the Agent
   package namespace; it does not prepend Agent’s `tests/` directory. The
   earlier Agent `tests/conftest.py` and `tests/lanes.py` changes therefore
   remain outside P5. The current successor does not change either file.

7. The authoritative normal-home receipt identifies ecdc’s full commit, tree,
   and parents as:

   ```text
   ecdc242ed9b673f641759ecf029f95e89a2c6f92
   d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735
   432f9dcbc66fb80b539d9ef709a63ef8065dbc92
   00ec0f2f841401b69dad26fb1b23d31cce11efab
   ```

   Local Git independently returns the same values. Runtime 95d and
   Composition 635f are also authenticated in `source-manifest.json`.

8. The retained original body remains exactly the separate Runtime 6a / Agent
   28e proof: request `runtime-d141-p5-cut-1026013331-6934`, XML SHA-256
   `04b7bcea10a693d691a4ccaff85df8c94a0e1e634ea14ae1de87f0a25ddca688`,
   case-set SHA-256
   `024cd7c2dd2f90c142727b1825bf5d6ee3ee72384547f6cfc925267586c5075c`, and
   exact counts 38 unique / 38 passed / 0 failed / 0 errors / 0 skipped / 0
   xfail, summary `38 passed in 31.02s`. The 0513 independent applicability
   output and 0619 immutable tree correction were read back by their recorded
   hashes and remain unchanged; their hashes are listed in
   `source-manifest.json`.

## Limits

Tests, typecheck, lint, import, collection, provider, preflight, and P5 body
execution are **NOTRUN**, as required. No product/test/fixture/input/assertion/
generated/pin/DTO edit, source refresh, service/queue/registry/kit/CAS
operation, acquisition, cleanup/deletion, Store/hub/Git write, build/ZIP,
credential action, D130 action, stopped-investigation retry, new proof receipt,
or retarget was performed.
