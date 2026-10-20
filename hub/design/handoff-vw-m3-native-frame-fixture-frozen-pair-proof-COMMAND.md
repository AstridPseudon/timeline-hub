# Commands

## Exact five-file App scope at the owner commit

```text
git show -s --format='%H %T' dba11c8432cee8df6e8bced4eae4d82e79f2b652
git diff dba11c843^ dba11c843 --name-status
```

The owner commit tree is `79fca36dcc07d83d457bc2db5f822cad28054d71` and its exact five
files are the three App harness/fixture modules plus the helper and the no-browser native
integration module. The requalification delta is only the existing integration module.

## Targeted unit lane

```text
npx eslint tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0 --no-cache
node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts
```

## Central named no-browser HTTP lane

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-native-frame-fixture-frozen-pair-proof integration-viewing-native-retained-fixture)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Successful result: 1 pass, exit 0, request ID
`vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141813-18235`.
The registered suite command's literal environment is recorded by the central result; the
test overrides those moving checkout values with owned archives made from the two frozen
commits and rejects any module import outside those archives.

