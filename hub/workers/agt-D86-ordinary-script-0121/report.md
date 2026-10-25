## Completed

Updated only the three assigned tests:

- Current Runtime provider/native capture migration for ordinary text and S3 media flows.
- Full commit request envelope, provider registration, verified text ingestion, and current `commitTimeline` route in the SDK script test.
- Preserved original assertions, parameters, decorators, branches, fixture inputs, and custody guards.

## Verification

- AST parsing: passed.
- `compileall`: passed.
- Ruff baseline/candidate: candidate passed; two pre-existing import-order findings were normalized.
- Mypy baseline/candidate: both passed.
- `git diff --check`: passed.
- Changed-file allowlist: passed.
- No pytest, collection, service, browser, build, or function execution run.

Dependency identities:

- Agent base: `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`
- Runtime: `a3cd1a3214fa1632879c21d82d1abb9ea720b1de`
- Runtime tree: `64bb0caf0b7b950e02c4075077868a3dcd12ee06`
- Schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

The commit message was written to the requested path, and `DONE` was created.

Unverified seam: the preserved original assertion expects literal revision ID `parent-2`; the current provider may generate deterministic authoring revision IDs instead. No synthetic history or ID override was introduced.