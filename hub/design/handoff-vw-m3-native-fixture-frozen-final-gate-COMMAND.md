# Native fixture frozen-pair final attribution gate commands

Read-only object checks:

```sh
git -C /home/user/banodoco/banodoco-workspace-runtime \
  show -s --format='%H %T %s' 2c4ac180c2220bdad966bc01e95ad230e99ce26a
git -C /home/user/peteromallet/astrid-agent \
  show -s --format='%H %T %s' d8749a9ce12a699672faf3ad96b4e4cbea9245c2
git -C /home/user/banodoco/reigh-app \
  show -s --format='commit=%H tree=%T parent=%P subject=%s' \
  dba11c8432cee8df6e8bced4eae4d82e79f2b652
git -C /home/user/banodoco/reigh-app \
  diff --name-status \
  dba11c8432cee8df6e8bced4eae4d82e79f2b652 \
  e43c4c34107bb474beb5e86e669cb4d75d961e7a
```

Expected verified results:

```text
Runtime 2c4ac180... 7ab412cc4bcbe517efcfa806e092336390312e18
Agent   d8749a9c... 75354d38c898729bac09619679f5421faba319ed
Owner App dba11c843... tree 79fca36dcc07d83d457bc2db5f822cad28054d71
Central App tree e43c4c34107bb474beb5e86e669cb4d75d961e7a
Central-tree delta: only tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts
```

Targeted evidence already recorded by the owner-port worker:

```sh
npx eslint tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts \
  --report-unused-disable-directives --max-warnings 0 --no-cache
node --import tsx --test \
  tests/e2e/timeline/viewing-parity/harness.test.ts \
  tests/e2e/timeline/viewing-parity/media.test.ts \
  tests/e2e/timeline/viewing-parity/canvas.test.ts \
  tests/e2e/timeline/viewing-parity/authority.test.ts \
  tests/e2e/timeline/viewing-parity/admission.test.ts
```

Results: ESLint PASS; five neighboring unit files PASS.

Central records reviewed, not rerun for this final gate:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141730-11929/log.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141813-18235/log.txt
```

The first record failed on the unfiltered Python empty `-c` path entry. The
second record passed 1/1 and printed literal Runtime/Agent commit, tree, archive
SHA, module origins, before manifests, after manifests, zero legacy writes, and
forged-task zero-write assertions.
