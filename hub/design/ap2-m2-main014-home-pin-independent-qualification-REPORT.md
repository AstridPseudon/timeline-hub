# Main014 App final95 normal-pin independent qualification

Date: 2026-10-21 UTC

## Disposition

**APPROVE** the bounded App consumer pin/source unit for private staging:

- App consumer commit: `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`
- App consumer tree: `01fd2a04ff0c383ec5281043c7e5a4c843d1d835`
- Parent/current App integration: `f54cd98ed91de213763b196e4ed770b557897a8b`
- Runtime producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, checkout
  `/home/user/work/wt/rt-pin-95bd3c5f`
- Contract/client: `0.2.14` / `0.2.14`

**HOLD** actual matched Agent/App/Runtime qualification, adoption, publication,
and activation. The exact new Agent final95 consumer SHA/tree has not been
provided. Historical `58973`, old `a0`, and public integration `0.2.13` are
not relabeled as this new pair.

## Independent source and lock review

The preflight report and explicit HOME peer ACK were read. HOME owns this exact
pin, so this worker reused it and made no duplicate generated or lock edit.
No earlier independent approval of exact `10fa2ff9` / `01fd2a04` was present in
the available reports.

The App commit is one child of the current `tl/integration` parent. Its diff is
exactly four intended paths:

```text
runtime.lock.json
src/integrations/runtime/generated-contract-metadata.ts
src/integrations/runtime/generated.ts
src/integrations/runtime/timeline-commit-types.ts
```

`runtime.lock.json` has exactly 13 entries. Comparing it with the parent shows
only these three generated blobs changed; all nine response fixtures and the
timeline schema entry are unchanged. No test or assertion path changed, so no
passing expectation was removed, weakened, skipped, or converted to refusal.
The changed sources contain no private392/private15 or old public013/a0/f021
pin reference.

The normal-updater provenance is intact. `scripts/sync-runtime-client.mjs`
selects the producer HEAD, updates only the lock source commit, and delegates
to `scripts/vendor-lock.mjs update`; the latter verifies the pinned HEAD,
committed manifest, working manifest, producer artifact hashes, and consumer
bytes before copying. The commit's four-file diff contains no hand-copied
generated source or schema override.

The detached producer is clean at the exact requested commit/tree. Independent
byte audit results:

- committed and working producer manifest are identical;
- all 76 manifest artifact entries match their producer working bytes;
- manifest SHA-256 is `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`;
- producer/version is `astrid-runtime` /
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
- raw Agent schema is `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
- Runtime schema is `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.

`git diff --check HEAD^ HEAD` passed. The App parent is exactly current
`hub/tl/integration`; no integration/public tuple or adoption edit was made.

## Tests

Passed locally:

```text
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f
  ok (matches pinned producer commit)

node --test scripts/runtime-schema-guard.test.mjs
  1 passed, 0 failed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/client.test.ts \
  src/integrations/runtime/clientStatus.test.ts \
  src/integrations/runtime/clientSharedSession.test.ts \
  src/integrations/runtime/client.runtimeOrigin.test.ts
  4 files passed, 44 tests passed
```

The local vendor-lock fixture run reached the tests but the sandbox denied its
temporary child `git init` calls: 2 passed and 11 failed at
`spawnSync git EPERM`. The required central targeted rerun was then requested
against this worktree:

```text
request-test ap2-m2-main014-home-pin-independent-qualification targeted \
  --files "src/integrations/runtime/vendorLock.test.ts"
```

Central result
`ap2-m2-main014-home-pin-independent-qualification-targeted-1021000351-21815`:
**1 file passed, 13 tests passed, exit 0**. The 11 local failures are therefore
classified as the sandbox temporary-Git restriction, not a product failure.

No full, browser, render, live-socket, or historical suite was run.

## Required next pair

Obtain and record the exact Agent final95 consumer SHA/tree first. Then run the
current-source Agent Runtime cohort against the immutable Runtime producer,
not the public013 checkout, using the bounded current-provider suite:

```sh
AGENT_CHECKOUT=/path/to/exact-agent-final95-checkout
cd "$AGENT_CHECKOUT"
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
PYTHONPATH="$AGENT_CHECKOUT" \
/home/user/work/venv-agent/bin/python -m pytest -q -m integration \
  tests/sdk/test_timeline_pristine_initialize_runtime.py \
  tests/editing_conformance/test_commit_runtime_occurrence_create.py \
  tests/editing_conformance/test_commit_runtime_parent_media.py \
  tests/editing_conformance/test_commit_runtime_text_binding.py \
  tests/editing_conformance/test_native_word_anchor.py \
  tests/editing_conformance/test_next_command_cohort_runtime.py \
  tests/editing_conformance/test_commit_runtime_m1.py \
  tests/editing_conformance/test_commit_runtime_identity.py \
  tests/sdk/test_timeline_producer_guard_runtime.py \
  tests/sdk/test_timeline_native_frontends.py
```

The App side must then rerun its current-source consumer/client lane against
the same pair. Until that Agent SHA/tree and matched result exist, this report
does not approve native/browser or integration adoption.
