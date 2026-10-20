# App post-c57 next-batch full environment

## Status

Prepared, not submitted. The manager must publish
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/next-batch-full-READY`
with the exact immutable App commit and tree after the cap, Provider/name, and
D10 checks. Until that marker exists, no full request is allowed.

The prior c57 full remains historical exact proof: 19,103 passed, zero actual
failures, and three authorized expected failures. This preparation does not
reclassify or rerun it.

## Reused immutable environment

The next full must use these already-qualified, read-only inputs:

| Input | Required identity |
| --- | --- |
| App | manager-provided immutable worker checkout and exact commit/tree from `next-batch-full-READY` |
| Agent | `/home/user/work/wt/app-m3-agent8130-safety-source-keeper`, commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff` |
| Runtime | `/home/user/work/wt/app-m3-runtime013-producer-source`, commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Runtime producer | Same immutable Runtime2c4 checkout and exact tree; `runtime.lock.json` names commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` |
| Composition | `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular files |
| Peers | React and React DOM `18.3.1`; Remotion, Player, Three, Layout Utils, and Media `4.0.509` |
| Browser source | Existing tracked `vendor/astrid-browser` fallback with `ASTRID_PUBLIC_CHECKOUT` unset |
| Dependency graph | Existing private13 read-only graph; never `/tmp/app-coherent-deps10/node_modules` or any shared install |

The fixed package, lock, and Runtime lock hashes on the prepared App source
are respectively:

```text
package.json      4afacd8c57182a7ba7b2307ad285a083e63d1018ffef290081d8eeedbd155ffd
package-lock.json 7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14
runtime.lock.json 550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2
```

## Existing runner and cache guards

Reuse the existing manager-owned runner; do not add another full runner or
suite:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/app-root-full-environment-final.sh`

Its current SHA256 is
`2b54e6deca361c0d5b3f376c35bf25cba7a50ea8121140cce8c9f0ea105b3e37`.
It already guards the 77-file archive, fixed peers, Runtime artifact count,
lock/vendor provenance, clean exact source pins, and before/after identity.
It creates an owned snapshot dependency overlay, restores the original
`node_modules` link on exit, uses the existing preload with
`--configLoader=runner --no-cache`, and places npm/Vite/Vitest/XDG/TMP caches
under the per-run log directory. Shared installs and shared caches are never
write targets.

## Post-READY registration and one-run rule

After the READY marker exists, the manager must substitute its literal App
commit/tree and immutable App checkout into one named central registration. The
registration must retain the fixed Agent and Runtime pins above and invoke the
existing runner in `full` mode. The effective full command remains:

```text
npm test -- --maxWorkers=2 --configLoader=runner --no-cache
```

The manager may then submit exactly one central `full` request and monitor that
same request ID to terminal completion. No second request, moving integration
checkout, sharedinstall10, install, project TypeScript check, browser/render,
or cache write is permitted.

The terminal classification must compare the exact failed-node set with the
c57 historical record and classify any new failures by cause (collection,
environment/source tuple, or product behavior). Existing expected failures
remain historical/authorized evidence only; they must not be relabeled.
