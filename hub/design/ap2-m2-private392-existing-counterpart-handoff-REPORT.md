# App private392 existing counterpart handoff

## Result

The already-qualified private392 App counterpart exists. No regeneration or
new pin is needed. The runner base is the retained App source branch:

| Item | Exact identity |
| --- | --- |
| Generated-counterpart approval branch | `tl/ap2-m2-private392-app-counterpart-preparation` |
| Approved counterpart commit/tree | `acc27e8dcf13b2296e7738d2e06199777ab3cb1f` / `ee76df404b0d2cae283cb70951264c97b94416a0` |
| Runner-ready source branch | `tl/ap2-m2-private392-unmocked-door-driver-source` |
| Runner-ready source commit/tree | `85ae206b815381da31c229cc9107e322cb9c612f` / `593ab0296b8cd14e06b1e5251f48ef1fe9125ea1` |
| Runner-ready source parent | `cb45dbb1d02b007938a0ec8fd379aaaba941fc55` |
| App lock blob SHA-256 | `3ee0aa69fbff9faeff76a44aedc4e7fb70a69970ceec25c0fde788dbdb37d873` |
| HTTP driver source SHA-256 | `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981` |

The source branch contains the approved generated counterpart plus the exact
unmocked Door driver. Its recorded source controls are the earlier 3-file,
30-test App control lane, ESLint, TypeScript no-emit, producer-backed
vendor-lock, and `git diff --check`, all passing. It does not claim HTTP/Door
qualification; the prior central run stopped at the hosted build before test
collection.

Do not use `tl/ap2-m2-private392-current-postbuild-app-proof` (`483e7b8d…`,
tree `09e1ce…`) or the current `tl/integration` App tree for this test: both
carry public Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
That refusal against private f8da is correct and remains a guard.

## Exact contract and source bytes

The retained source lock has 13 entries and records:

```json
{
  "producer": "astrid-runtime",
  "producer_version": "sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d",
  "source_commit": "f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414"
}
```

The three generated App files are byte-identical to their locked producer
files, with these hashes:

- `src/integrations/runtime/generated-contract-metadata.ts` — `44bad1f8e9df2e1e473fb6af7b10d9ed3e3cbd0e0e23e67c842328e548cb722b`
- `src/integrations/runtime/generated.ts` — `54144eb6dbc27b595ca428122faea48348519958fd6aea25a47dbfd7199fd451`
- `src/integrations/runtime/timeline-commit-types.ts` — `8b2522dd630ea2b2b004c87acd527ad0d30f24e429ba7069b791bf3a94aa08f7`

The vendored timeline schema is `f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1`.
The Agent/Runtime edit-command schema is byte-identical:
`39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
Runtime identity is protocol `workspace.v1`, package `0.2.13`, health/schema
`242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`, raw
timeline bundle `fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`,
component manifest `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
and 75 manifest artifacts.

## Read-only verification

Exact detached checkouts are present and clean:

- Agent: `/home/user/work/wt/agt-pin-1303ce6b`, HEAD
  `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`, tree
  `2f2685d85c3f65b458795100a8045371eb19ee06`, parent `e010e6a3868e963471244491bb6672c3e4a5135e`.
- Runtime: `/home/user/work/wt/rt-pin-f8da4b6d`, HEAD
  `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`, tree
  `8be43e13acb436120f8a63b1a178d64c49422461`.

A read-only audit of the committed App source branch compared all 13 locked
consumer blobs with the Runtime checkout and its committed 75-artifact
manifest: **PASS**, every consumer byte, lock hash, and producer-manifest hash
matched. The original source worker also recorded the exact normal command as
passing:

```sh
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
# ok runtime.lock.json (matches pinned producer commit)
```

I did not run that command in this worktree because its lock is the public
2c4/6f000 lock and the task forbids rewriting it or creating another App copy.

## Exact runner environment

Use the runner source from `tl/ap2-m2-private392-app-http-runner-minimal-source`
at `7a8762e05a97dbd3fdf2c188aa14292d066933c5`, whose wrapper hard-checks the
Agent/Runtime identities above and driver hash `85a6f1b2…`. `APP_ROOT` must be
an exact checkout/snapshot of the runner-ready App branch at `85ae206b…`.

```sh
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b \
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
sh /path/to/private392-http-runner.sh /absolute/path/to/app-85ae206b
```

The wrapper must start with `ASTRID_PUBLIC_CHECKOUT` and
`ASTRID_APP_DIRECT_DIST` unset. It creates and removes its own disposable
`index.html`, temp root, and Vite cache; it then runs exactly one selector:

```text
node_modules/.bin/vitest run --config config/testing/vitest.runtime-restore.integration.config.ts --no-cache --maxWorkers=1 --no-file-parallelism tests/integration/runtimePrivate392Consumer.test.ts
```

The required Python paths `/home/user/work/venv-agent/bin/python` and
`/home/user/work/venv-runtime/bin/python` are absent in this sandbox. The only
Python environment found is `/home/user/work/venv-app2-native`; it was not
substituted, modified, or used because the reviewed launch contract requires
the two exact paths. Therefore no new HTTP/socket/browser/build/request-test
run was started here.

## Next step

The runner service should use the exact `85ae206b` App source and the exact
Agent/Runtime checkouts and venv paths above, then run the one existing HTTP
selector. Preserve every wrapper guard, including the public-lock mismatch,
75-artifact audit, schema byte equality, clean checkouts, project/credential
checks, lost-ACK/reload/exact-retry, stale zero-write, guarded undo, and zero
legacy POST assertions. No public lock edit, generated artifact, new pin, or
dependency change is authorized by this handoff.
