# Validation record

All checks below were read-only source/object/hash inspections. No product import, module collection, provider call, preflight, test, typecheck, lint, generator, vendor-lock, package, environment, network, or service command was run.

## Authenticated object checks

```text
git -C /home/user/work/agent show -s --format='%H %T %P' 28e56cacb42d3da85b02e5b3543895b44f3d0f70
28e56cacb42d3da85b02e5b3543895b44f3d0f70 2ebe2ddf5a61f013953ab1e21d51ebaab746e58a c585cb2aa73c5298d474e614cb2144f58f27e605 b4eb5db76fda523407b90a9dbe820f4e20cc1f1d

git -C /home/user/work/agent show -s --format='%H %T %P' ecdc242ed9b673f641759ecf029f95e89a2c6f92
ecdc242ed9b673f641759ecf029f95e89a2c6f92 d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735 432f9dcbc66fb80b539d9ef709a63ef8065dbc92 00ec0f2f841401b69dad26fb1b23d31cce11efab

git -C /home/user/work/agent show -s --format='%H %T %P' ec0a9f5baef2c31bc5179087b83f044524575182
ec0a9f5baef2c31bc5179087b83f044524575182 83b84c79941917fde535ee3ddba5533a776cace3 73e369b1a2f0448f033d252edae9b09fd64547de 66720e11e8daa26a4e192a83d592cbe5caafc109

git -C /home/user/work/runtime show -s --format='%H %T %P' 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d
6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d ac5b862744bece65b2e30565db1777bacd60da28 0ca306dfd3cf4e21976271cc4b2e779b10e025b0 24107e83b096264e59f64ed5bd65e00650567f22

git -C /home/user/work/runtime show -s --format='%H %T %P' 95d98f038320d5d46bd679ac000ab3e15825c935
95d98f038320d5d46bd679ac000ab3e15825c935 78df31d62c5b9ba4c84dee4ea346e43a767718c1 857e4c3bce8fd7fc862d7e6e5831e63f24e8cce5 012889c1b0bbfe5f290f757cb6d31dd7d995ccc7
```

All named commit, tree, and parent objects resolved as the full 40-character values above.

## Exact delta and blob checks

```text
git -C /home/user/work/agent diff --name-status ecdc242ed9b673f641759ecf029f95e89a2c6f92 ec0a9f5baef2c31bc5179087b83f044524575182
11 paths: 2 production paths and 9 test paths

git -C /home/user/work/agent diff --stat ecdc242ed9b673f641759ecf029f95e89a2c6f92 ec0a9f5baef2c31bc5179087b83f044524575182
1869 insertions(+), 13 deletions(-)

git -C /home/user/work/agent diff --check ecdc242ed9b673f641759ecf029f95e89a2c6f92 ec0a9f5baef2c31bc5179087b83f044524575182
exit 0
```

Exact changed production blobs and SHA-256 values are recorded in `source-manifest.json`. `git show` of both production blobs was inspected. `inverses.py` is additive and pure; `cli_native.py` changes only normal CLI conflict/error and human-presentation paths.

## Closure and custody checks

```text
git -C /home/user/work/agent diff --quiet 28e56cacb42d3da85b02e5b3543895b44f3d0f70 ec0a9f5baef2c31bc5179087b83f044524575182 -- astrid/sdk/timeline/api.py astrid/sdk/timeline/capture.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/_common.py astrid/core/timeline/authoring_bundle.py astrid_runtime_client/generated.py astrid_runtime_client/contract_metadata.py
exit 0

git -C /home/user/work/runtime diff --name-status 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d 95d98f038320d5d46bd679ac000ab3e15825c935
conformance/typescript/contract-metadata.ts
conformance/typescript/generated.ts
runtime_protocol/upgrade.py
```

Static inspection of the exact P5 source showed `tests/test_timeline_commit_crash.py:81` calling `migrate_canonical_to_current`, direct `astrid.sdk.timeline.capture`/`commit` imports, and Runtime `tests/conftest.py`/`tests/lanes.py` resolution. `_validate_candidate` is only called from `upgrade_realm`; no P5 call reaches it. No final Agent production source imports `astrid.core.timeline.inverses`. `astrid/packs/timeline/cli.py` does call `cli_native.py`, proving that changed presenter is a real production caller, but P5 does not call that CLI route.

`runtime.lock.json` SHA-256 is `cc1661b12d9d0a4600c79adab4e2d962db455b5819dee78a0353787d8d4f2b82` at both ecdc and ec0a. Its source commit is Runtime 95d; its 15 mappings match the unchanged Runtime manifest/source hashes. The original XML, 0513 custody JSON, 0619 corrected derivative, 0637 applicability review/manifest, 0646 publication, and final HOME/Agent publications were hashed in place; all hashes are recorded in `source-manifest.json`.

## Original proof custody

The retained XML is 5,658 bytes and hashes to `04b7bcea10a693d691a4ccaff85df8c94a0e1e634ea14ae1de87f0a25ddca688`; it records 38 tests, all passed, with no failures/errors/skips/xfails. The original run’s source hash packet records Runtime `__init__`, Runtime metadata/manifest, Agent `api.py`, Agent generated client, and Agent metadata hashes. The 0619 correction is metadata-only and corrects the stale Agent tree text to the authenticated Agent 8585 tree; it does not retarget the original receipt.

## Explicit NOTRUN

```text
imports: NOTRUN
collection: NOTRUN
provider calls: NOTRUN
preflight: NOTRUN
targeted tests: NOTRUN
full suite: NOTRUN
P5 rerun/body: NOTRUN
typecheck: NOTRUN
lint: NOTRUN
vendor-lock/generator: NOTRUN
```
