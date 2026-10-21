# App2 Main014 normal-pin preflight

Date: 2026-10-20 UTC  
Worker branch: `tl/ap2-m2-main014-normal-pin-preflight`  
Base: `f54cd98ed91de213763b196e4ed770b557897a8b`, tree
`84fa578160ca10e09294b7757178d457858249bf`

## Result and ownership

This worker made no App source, lock, generated-file, fixture, dependency, or
shared-install changes. The App worktree remains clean.

The normal pin is already owned by HOME/App: branch
`hub/tl/app-m3-main014-final95-normal-owned-pin` contains commit
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a`, tree
`01fd2a04ff0c383ec5281043c7e5a4c843d1d835`, parent
`f54cd98ed91de213763b196e4ed770b557897a8b`. The explicit App peer ACK at
`design/peer-app-to-runtime-agent-20261020T2353-final95-pin-ack.md` says HOME
owns the root lock/generated files and dispatched that worker for normal
update/check only. This satisfies the brief's live-pin duplication condition;
this worker did not duplicate the generated-file edit.

The paired Agent final95 consumer SHA/tree is not yet available in the current
handoff. App native/browser qualification must wait for that matched pair.

## Exact Runtime candidate

- Server commit: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- Server tree: `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Immutable producer: `/home/user/work/wt/rt-pin-95bd3c5f` (detached at the
  exact commit/tree; clean)
- Contract/client: `0.2.14` / `0.2.14`
- Protocol: `workspace.v1`
- Runtime schema: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
- Raw Agent schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
  (55 definitions / 29 operations)
- Health schema: `sha256:dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e`
- Services schema: `sha256:10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018`
- Raw commit bundle: `sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`
- 76-artifact manifest SHA: `sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`
- Producer/version: `astrid-runtime` /
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`
- Runtime qualification: full31902, 5,988 passed / 26 skipped / 15 xfailed /
  12 warnings, exit 0; no publication or integration adoption implied.

## App lock inventory and normal-update delta

Current `runtime.lock.json` has 13 entries: nine response fixtures, three
generated TypeScript/client entries, and the timeline schema. The candidate
manifest/source comparison found:

- Unchanged: all nine response fixtures.
- Unchanged: `vendor/timeline-schema/python/banodoco_timeline_schema/timeline.schema.json`.
- Would update from the exact producer bytes:
  - `src/integrations/runtime/generated-contract-metadata.ts`:
    `sha256:0829f42a52fd74e596f5925814766cb87d60919203991b22f07f6869ab6ace44` -> `sha256:4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044`
  - `src/integrations/runtime/generated.ts`:
    `sha256:dd542c8c04ecce1af3d21413cf82ac6316879c0f3d2dacae5f88754c3b395ee8` -> `sha256:c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d`
  - `src/integrations/runtime/timeline-commit-types.ts`:
    `sha256:e3d625cea11e5e0318c1a3020b1baba62c3726c4d7fe4b3d03d810d48743331d` -> `sha256:f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564`

The corresponding generated metadata changes contract `0.2.13` to `0.2.14`
and schema digest `8de823...` to `7d4afa...`; generated client types add the
candidate's health/service and timeline command types. No hand-written
semantic or schema edit is authorized.

The handoff's normal commands are:

```sh
RUNTIME_PRODUCER=/home/user/work/wt/rt-pin-95bd3c5f
node scripts/vendor-lock.mjs update runtime.lock.json --producer "$RUNTIME_PRODUCER"
node scripts/vendor-lock.mjs check runtime.lock.json --producer "$RUNTIME_PRODUCER"
```

Important implementation detail: `vendor-lock.mjs` validates that the
producer HEAD equals `runtime.lock.json.source_commit` before updating. Since
the current lock is still public `2c4ac180c...`, the repository's existing
normal wrapper `node scripts/sync-runtime-client.mjs "$RUNTIME_PRODUCER"`
must perform the source-commit transition and delegate to that updater; do not
manually copy bytes or edit generated content. The existing HOME branch has
the expected source commit, producer version, and three changed generated
hashes in its lock.

## Read-only checks and tests

Passed:

```text
node scripts/vendor-lock.mjs check runtime.lock.json
  ok runtime.lock.json

node --test scripts/runtime-schema-guard.test.mjs
  1 passed, 0 failed

./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/integrations/runtime/client.test.ts \
  src/integrations/runtime/clientStatus.test.ts \
  src/integrations/runtime/clientSharedSession.test.ts \
  src/integrations/runtime/client.runtimeOrigin.test.ts
  4 files passed, 44 tests passed
```

The candidate check was intentionally read-only and refused as expected:

```text
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f
  exit 1: checkout HEAD ...95bd does not match pinned source_commit ...2c4ac180
```

This proves the base lock remains public013; it is not a candidate failure.

The combined lock/client Vitest invocation produced 46 passed tests and 11
`vendorLock.test.ts` failures because this sandbox rejects that test's fixture
subprocess calls with `spawnSync git EPERM` at `git init`. The direct lock
checker and four pure client files above pass. No full, browser, render, live
socket, or historical old-pair suite was run.

## Next handoff

Use HOME's existing `10fa2ff9...` branch for independent release/pin review.
Before any matched App qualification, obtain the exact Agent final95 consumer
SHA/tree and rerun the current-source paired tests against the same Runtime
tuple. Keep public013/current tuple, old `a0`/`f021`/`f8`/private15 labels,
publication markers, and integration adoption unchanged.
