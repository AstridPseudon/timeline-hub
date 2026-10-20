# Files

## App owner scope

```text
tests/e2e/local/support/harness.ts
tests/e2e/timeline/viewing-parity/fixture.ts
tests/e2e/timeline/viewing-parity/harness.ts
tests/e2e/timeline/viewing-parity/native-fixture-helper.py
tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts
```

## Requalification delta

```text
tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts
```

The module is 158 lines and remains below the 500-line limit. It uses only existing
Node test/harness facilities plus ephemeral `git archive` extraction and removes that
temporary source directory in `finally`.

