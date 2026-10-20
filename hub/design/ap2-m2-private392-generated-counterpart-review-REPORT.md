# App private392 generated-counterpart review

## Verdict

**APPROVE the isolated private392 App proposal.** This is a read-only
generated-contract/private-pin review. It does not adopt the proposal, create
an integration/public pin, activate the App consumer, or qualify the native
provider/Door path.

The approval is bounded by the settled PLAN: the existing App source guards,
the normal Agent private pin, and Runtime's final private392 approval remain
mandatory before any matched native qualification or consumer activation.

## Exact identities and scope

| Item | Exact value |
| --- | --- |
| App review HEAD/tree | `acc27e8dcf13b2296e7738d2e06199777ab3cb1f` / `ee76df404b0d2cae283cb70951264c97b94416a0` |
| App parent/base | `220b0f10328358049c15c580470d1a5771ad9bc8` |
| Runtime producer commit/tree | `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414` / `8be43e13acb436120f8a63b1a178d64c49422461` |
| Agent source commit/tree | `e010e6a3868e963471244491bb6672c3e4a5135e` / `70414cf6875d2c97c45f33e0a5158c80bd7391d9` |
| Agent/Runtime command schema | `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` |
| Runtime protocol/package | `workspace.v1` / `0.2.13` |
| Component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Runtime health/schema digest | `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042` |
| Runtime raw bundle digest | `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3` |
| Runtime artifact-manifest version | `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d` |
| Runtime artifact count | `75` |

The App delta is exactly four files: `runtime.lock.json` and the three
existing generated Runtime TypeScript files. No producer, UI, command
session, provider, route, DTO, schema, public API, test, publication, or
activation file changed.

## Contract and generation findings

- `runtime.lock.json` pins exactly Runtime `f8da4b6d...`, not the prior
  `2c4ac180...`/artifact `6f000...` cohort.
- The exact detached Runtime checkout was verified at commit `f8da4b6d...`
  and tree `8be43e13...`; it is clean.
- Runtime `contract/artifacts.json` contains 75 paths. Independent recomputation
  found all 75 producer files present with their declared hashes.
- The Agent e010 schema and Runtime
  `contract/schemas/edit-command.json` are byte-identical at schema392.
  The schema has 56 definitions and includes the existing 30-operation/
  12-explicit-v2 inventory described by the source handoffs.
- App generated metadata, `generated.ts`, and `timeline-commit-types.ts` are
  byte-identical to the exact Runtime producer files. Their lock hashes also
  match the local bytes and producer bytes. The closed
  `ProjectDataWriteArgs` type is present in `timeline-commit-types.ts` and is
  exported by the generated root `generated.ts` surface.
- The generated files retain normal “do not edit by hand” markers. The
  producer-backed vendor-lock checker validates the pinned Git HEAD, committed
  manifest bytes, manifest hashes, lock hashes, and consumer bytes. Together
  with exact byte equality and the preparation report's normal
  `vendor-lock.mjs update` result, this is evidence of normal generation from
  the real checkout rather than hand-edited types.
- No old952, a0, public013, or opacity/transition schema identity is mixed
  into this delta. Existing `transition` members in the generated clip union
  are unchanged ordinary schema content; no opacity/transition operation or
  source was added or relabeled.

## App compatibility boundary

`src/tools/video-editor/commands/projectDataMember.ts` is byte-identical to
the parent candidate. Its existing boundary remains intact: only the closed
parent `project-data.write` v1 shape is admitted; target/key and finite JSON
are checked; reserved keys and size/count limits are enforced; replace and
merge are lowered to native replace commands with exact leaf guards; and
unsupported mixed batches refuse atomically while retaining the draft.

There is no active production caller or wire activation in this proposal. No
fallback writer, endpoint, DTO, public/integration pin, or generated-byte
override was introduced. The proposal is therefore compatible while inert;
it must remain behind the normal Agent pin and matched Runtime/native gates.

## Checks

Passed in the clean review worktree:

```text
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
ok runtime.lock.json (matches pinned producer commit)

git diff --check
passed

node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/projectDataMember.test.ts
1 file, 9 tests passed

node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/client.test.ts src/integrations/runtime/timelineCommit.test.ts
2 files, 64 tests passed
```

The initially attempted `--configLoader=runner` form failed before test
collection because this repository config uses CommonJS `__dirname`; the
default loader with `--no-cache` passed and required no source change. The
vendor-lock fixture tests were not rerun locally; the preparation report's
attempt failed at temporary `git init` with worker-sandbox `spawnSync git
EPERM`. The direct producer-backed lock check and independent 75-artifact and
byte audits passed, so no central fixture run was needed for this bounded
review. No full, browser, localhost, live socket, native/provider/Door,
publication, activation, or integration suite was run.

## Recommendation

Accept this isolated generated counterpart for the next review gate, without
adopting it. Keep the existing App source guards and Runtime final approval
as prerequisites. The next authorized action is one matched private392
Agent/Runtime native/provider/Door qualification after the normal Agent pin;
consumer activation and public/integration adoption remain out of scope.
