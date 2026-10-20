# App public13 PCM complete-source typecheck

## Result

**PASS.** The complete assigned App worktree was checked once with the required
project configuration and a private leaf13 dependency overlay. The valid
invocation exited `0` with zero diagnostics. No product source, configuration,
lockfile, or shared dependency was changed.

This is bounded public13 + PCM source typecheck evidence only. It makes no
parity, merge, integration-pin, release, build, browser, or production claim.

## Source and pin identity

| Item | Identity |
| --- | --- |
| App commit | `35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a` |
| App tree | `db0da562200367715858b11d258b40a3f5664b20` |
| Candidate parent | `2b3c431fb0efb967c59662c50f5a5bd694f9157e` |
| `package.json` SHA-256 | `a2ac9c9d946bd2d0ee1b2283154d94adad926f6282fff4417aeaf7520f138437` |
| `package-lock.json` SHA-256 | `7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14` |
| `tsconfig.app.json` SHA-256 | `61f9b16cd7f141d23ce4520d7c5412728df8906dde981f6e5b33c8bc5b100516` |
| Worktree status | clean; ignored `node_modules` link only was redirected |

The existing `tsconfig.app.json` was used unchanged: strict `src` checking,
ES2020/DOM libs, bundler resolution, existing aliases and exclusions, `noEmit`,
and `skipLibCheck`.

## Dependency overlay

The worktree's ignored root link pointed to this private overlay:

`/tmp/app-public13-pcm-complete-source-tsc-leaf13.01Xcjn/node_modules`

The overlay extracted only the approved Composition archive as regular files;
all other top-level dependencies were symlinks to the retained read-only shared
install at `/home/user/work/app/node_modules`. No install, network access, or
write to shared dependencies occurred.

| Fact | Value |
| --- | --- |
| Composition archive | `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` |
| Archive size | `58,477` bytes |
| Archive SHA-256 | `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |
| Archive SHA-512 | `eaa80401c7d8a841ae89eb284650458f54271200ca759b22b1076b322bce36d73794072df2d85dcd56cd57a2fb958e5fd83f6fbd32191d30fcbca85f5a02ceb9` |
| Lock integrity | `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==` |
| Archive/extracted regular files | `77/77` byte-exact |
| Installed Composition | `@banodoco/timeline-composition@0.0.13` |
| TypeScript | `5.9.3`; executable SHA-256 `8d5fa5bd883fec0979fc2004f1fe1d99aef40570155d550eadc0b03b55513bf0` |

Composition peers resolved from the shared read-only install at the pinned
versions: React and React DOM `18.3.1`; Remotion, `@remotion/media`, and
`@remotion/layout-utils` `4.0.509`.

Before invoking `tsc`, both previously missing imports were verified in this
actual complete worktree:

- `config/hosted-origin.json` — present; SHA-256 `0fa6eeffa4f6efb6aa5485de821b4dc454f2f77fba2386035de7dac41159f455`
- `supabase/functions/create-task/resolvers/shared/lineage.ts` — present; SHA-256 `e4de4d0cf87d786ba20ff2ae85f19c20194f528d1fd873b676447f54c536f8c0`

## Exact check

```sh
flock /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 \
  /tmp/app-public13-pcm-complete-source-tsc-leaf13.01Xcjn/node_modules/typescript/bin/tsc \
  --noEmit -p tsconfig.app.json
```

- Start: `2026-10-20T14:39:40Z`
- End: `2026-10-20T14:40:32Z`
- Exit: `0`
- Diagnostics: none; combined stdout/stderr `0` bytes, `0` lines
- Invocation count: one; no retry

## Classification of the earlier result

The earlier two `TS2307` diagnostics for `config/hosted-origin.json` and
`supabase/functions/create-task/resolvers/shared/lineage.ts` were invalid local
environment evidence, not product diagnostics. That worker's leaf overlay was
based on a copied incomplete source tree and omitted the tracked `config` and
`supabase` roots. This run preserved the complete worktree's real relative
locations, verified both files before `tsc`, and used the unchanged project
configuration. The earlier diagnostics were discarded and not attributed to
the candidate.

No full/Vitest/build/browser/socket check was run.
