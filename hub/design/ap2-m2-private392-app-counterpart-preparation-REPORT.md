# App private392 counterpart preparation

## Result

Prepared the isolated App generated-client counterpart from the exact Runtime
producer checkout. This is preparation only: no integration/public pin,
consumer activation, package publication, provider/native/Door test, browser,
localhost, socket, or full-suite run was performed.

The App worktree contains only the normal generated-client/vendor-lock delta:

- `runtime.lock.json`
- `src/integrations/runtime/generated-contract-metadata.ts`
- `src/integrations/runtime/generated.ts`
- `src/integrations/runtime/timeline-commit-types.ts`

No App producer, data-provider, command-session, UI, route, DTO, schema, or
public API was changed.

## Authoritative identities

The private392 handoffs identify the exact pair as:

| Item | Exact value |
| --- | --- |
| Agent source commit | `e010e6a3868e963471244491bb6672c3e4a5135e` |
| Agent source tree | `70414cf6875d2c97c45f33e0a5158c80bd7391d9` |
| Agent schema digest | `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` |
| Runtime producer commit | `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414` |
| Runtime producer tree | `8be43e13acb436120f8a63b1a178d64c49422461` |
| Runtime package/protocol | `0.2.13` / `workspace.v1` |
| Runtime component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Runtime health/schema digest | `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042` |
| Runtime raw bundle digest | `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3` |
| Runtime artifact manifest digest | `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d` |
| Generated shape | 56 definitions, 30 operations, 12 explicit v2 branches |

The exact producer checkout was requested through the orchestrator checkout
tool and is at:

`/home/user/work/wt/rt-pin-f8da4b6d`

It is detached at the exact producer commit and has tree
`8be43e13acb436120f8a63b1a178d64c49422461`.

The Agent and Runtime private392 source reviews are both APPROVE, but the
normal owned Agent private pin and matched native/provider/Door pair are still
explicit prerequisites. The old952/a0 bytes and public013/ordinary014 cohorts
were not used or relabeled.

## Generated counterpart

The existing App command:

```text
node scripts/vendor-lock.mjs update runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
```

was run after staging the exact producer commit in the lock, and copied only
the already locked 13 Runtime artifacts. The generated App files now contain
the closed `ProjectDataWriteArgs` root export and the producer's existing
timeline types. No hand-edited generated schema or new wire/DTO field was
introduced.

The private lock records:

```json
{
  "producer": "astrid-runtime",
  "producer_version": "sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d",
  "source_commit": "f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414"
}
```

The exact generated consumer hashes are:

- `generated-contract-metadata.ts`: `sha256:44bad1f8e9df2e1e473fb6af7b10d9ed3e3cbd0e0e23e67c842328e548cb722b`
- `generated.ts`: `sha256:54144eb6dbc27b595ca428122faea48348519958fd6aea25a47dbfd7199fd451`
- `timeline-commit-types.ts`: `sha256:8b2522dd630ea2b2b004c87acd527ad0d30f24e429ba7069b791bf3a94aa08f7`

The corresponding producer bytes have the same hashes. No generated artifact
outside the existing lock was added.

## Existing App guard and staged consumer proposal

The already integrated inactive
`src/tools/video-editor/commands/projectDataMember.ts` remains unchanged.
Its original guard review remains the boundary:

- only closed `project-data.write` v1 parent commands are admitted;
- extension target and canonical key are validated;
- finite JSON and reserved object keys are rejected;
- entry, namespace-entry-count, and total namespace limits remain enforced;
- replace and merge are lowered to native `mode: "replace"` commands with
  exact leaf expectations;
- unsupported mixed batches refuse atomically and retain the draft;
- no broad UI JSON admission or delete emulation is added.

The exact ordinary proposal to qualify after the normal Agent pin and matched
private pair are approved is the existing project-data member shape used by
the App guard review:

```json
{
  "version": 1,
  "source": "com.example.compiler-canary",
  "operations": [
    {
      "op": "project-data.write",
      "target": "com.example.compiler-canary",
      "payload": {
        "key": "settings",
        "value": {
          "volume": 3,
          "nested": {
            "late": true
          }
        },
        "mode": "merge"
      },
      "order": 5
    },
    {
      "op": "project-data.write",
      "target": "com.example.compiler-canary",
      "payload": {
        "key": "settings",
        "value": {
          "theme": "dark",
          "nested": {
            "first": true
          }
        },
        "mode": "merge"
      },
      "order": 1
    },
    {
      "op": "project-data.write",
      "target": "com.example.compiler-canary",
      "payload": {
        "key": "replacement",
        "value": {
          "fresh": true
        },
        "mode": "replace"
      }
    }
  ]
}
```

This is the existing focused App proposal fixture, not an activated UI path.
The real current scene-phase producer
(`src/tools/video-editor/dev/scene-phase-markers/extension.ts`) is
replace-only and remains on its existing `TimelinePatch` path; it was not
rewired here. There is currently no active production caller of
`captureProjectDataMember`, so activation must wait for the explicit native
pair gate.

After activation approval, the proposal must lower to three ordered native
`project-data.write` commands, submit through the existing command
session/outbox and normal `/v1` Runtime commit, and prove:

1. local replace/merge preview preserves the opaque sibling and exact key
   order/guards;
2. the accepted `/v1` commit is sent once;
3. the acknowledgement is lost;
4. the App reloads/restarts and retries the exact persisted idempotency
   request;
5. Runtime returns the original receipt, without a duplicate revision;
6. the App reloads the accepted document and performs guarded undo;
7. mismatched leaf/namespace and opaque-value cases refuse visibly with the
   draft retained; and
8. no legacy project-data/fallback whole-document save traffic occurs.

The actual native/provider/Door command is deliberately not run in this
preparation worker. The future central qualification should use the existing
App three-products harness and its command-session/outbox path, with the exact
producer checkout and the final normal Agent private pin, rather than a
synthetic Runtime transport or fabricated document authority.

## Checks run

Passed:

```text
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
ok runtime.lock.json (matches pinned producer commit)

node .../vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/projectDataMember.test.ts
1 file, 9 tests passed

node .../vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/client.test.ts src/integrations/runtime/timelineCommit.test.ts
2 files, 64 tests passed

git diff --check
passed
```

The command below was also run as a neighbour check, but its fixture tests
cannot spawn their temporary `git init` under this worker sandbox:

```text
node .../vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/vendorLock.test.ts src/tools/video-editor/commands/projectDataMember.test.ts
```

Result: 1 file passed (9 tests); 11 vendor-lock fixture tests failed before
their assertions with `spawnSync git EPERM`. The direct producer-backed
`vendor-lock.mjs check` above passed and is the qualifying artifact check.
No tests were skipped or weakened.

No full suite, browser, localhost, live socket, provider/native/Door,
integration/public pin, release, consumer activation, or package publication
was run.

## Status/next step

No Agent or Runtime manager `STATUS.md` was present in the supplied
orchestrator manager directory; the exact private392 source/final-review
handoffs were available and were used as authority. This is a reporting
limitation, not a substituted identity.

Next step is the orchestrator/manager review of this isolated generated
counterpart, then the normal Agent private pin, then exactly one matched
private392 native/provider/Door qualification. Only after those gates pass may
the App consumer be wired or a public/integration adoption be considered.

