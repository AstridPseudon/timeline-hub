# Independent review commands

```text
git -C /home/user/work/app show -s --format=fuller dba11c8432cee8df6e8bced4eae4d82e79f2b652
git -C /home/user/work/app diff-tree --no-commit-id --name-status -r dba11c8432cee8df6e8bced4eae4d82e79f2b652
git -C /home/user/work/app show --format= dba11c8432cee8df6e8bced4eae4d82e79f2b652 -- tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/fixture.ts tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/native-fixture-helper.py tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts
git -C /home/user/work/runtime log -8 --format='%h %H %ad %s' --date=iso
git -C /home/user/work/agent log -8 --format='%h %H %ad %s' --date=iso
 rg/sed inspection of Runtime timeline_commit_store.py, service.py, store.py, capture_validation.py
cat central .../summary and .../log.txt
```

Results: exact source commit and five-file scope verified; native closure/CAS
guards verified by source inspection; central native integration result 1/1.
No browser/render/full/localhost/network/install run.
