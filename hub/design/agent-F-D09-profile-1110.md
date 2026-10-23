# F D09 current Remotion profile provisioning

## Result

Provisioned the one authorized ordinary immutable profile through the existing
dispatcher request path:

`/home/user/work/runtimes/agent-remotion-v3-819acf-1110`

The dispatcher result reports a normal `npm ci` build from the exact current
Agent commit `abfa78a657b4ce1cc625104e8472fb29938e3d64`, with lock SHA-256
`f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d` and
Remotion `4.0.509`. No daemon or parallel package installation was invoked.

## Preconditions and custody

- Approved V3 source `b56828de538c10584030cc1a0c3c2ac39fc6cc14` and current
  source `abfa78a657b4ce1cc625104e8472fb29938e3d64` have identical remotion
  tree, package.json, package-lock.json, and commit-named Composition archive
  blobs.
- Before request, free disk was `15,990,509,568` bytes, above the required
  `15.8 GB` floor. Target and `.partial` paths were absent.
- Approved Composition archive is `73,451` bytes, SHA-256
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, with
  `80` regular members. The stale existing archive remains separate at
  `72,134` bytes / SHA-256
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`.
- Profile lock dependency resolves the approved archive and has SRI
  `sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ==`.

## Verification

- `git show abfa78a65:remotion/package-lock.json | sha256sum`: PASS, exact
  requested lock hash.
- Source comparison: `76` tracked remotion files compared, `0` byte
  mismatches.
- Installed Composition: `80` archive members / `80` installed regular files,
  member lists equal, `0` byte mismatches.
- Profile files: `21,501` files, apparent size `330,070,022` bytes, `0`
  writable regular files; package metadata and archive are mode `0444`.
- Node `v20.19.4`, npm `10.8.2`; installed Composition `0.0.14` and Remotion
  `4.0.509`.
- Direct public Composition import: PASS (`27` exports).
- `npm run typecheck`: FAIL in the exact archived source because the commit
  lacks `src/effects.generated.ts`, `src/animations.generated.ts`,
  `src/transitions.generated.ts`, and the two external
  `astrid/.../threejs-live-editor` modules. No source or validator workaround
  was added.
- The existing `__smoke__/bundle.mjs` was not run because it performs bundle
  and composition selection through the browser-adjacent Remotion path, which
  this task explicitly forbids. No D09 body was run.

## Outside-worktree changes

The request created only the new runtime plus the dispatcher result record and
`tests/agent-remotion-v3-819acf-1110.env` (`538` bytes). The dispatcher did
not add a `suites.conf` entry despite reporting a suite name; no new launcher
was added manually. Existing runtimes, f1012 state, shared node_modules,
guards, pins, product/test/service contracts, and Git refs were not modified.
The Agent worktree is clean.

## Recommendation

Use the generated env file for the authorized route. Treat the profile as
custody-qualified for the requested archive/lock/source checks, while keeping
the archived-source typecheck failure and absent suite registration visible to
the manager. Any later D09 activation remains a separate decision and was not
performed here.
