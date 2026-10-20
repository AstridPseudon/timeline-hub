# App public13 PCM consumer project typecheck

## Result

**PASS.** The approved App candidate was checked once with the required project
configuration, using a private leaf13 dependency overlay. The valid invocation
exited `0` with zero diagnostics. No App source, test, configuration, lockfile,
or shared dependency was changed. This is a source typecheck only; it makes no
parity, merge, integration-pin, release, or production-qualification claim.

## Exact source

| Item | Identity |
| --- | --- |
| App commit | `35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a` |
| App tree | `db0da562200367715858b11d258b40a3f5664b20` |
| Candidate parent | `2b3c431fb0efb967c59662c50f5a5bd694f9157e` |
| Candidate delta | Seven bounded public13/PCM consumer files, matching the approved review |

The candidate delta is exactly:

```text
src/tools/video-editor/compositions/AudioTrack.test.tsx
src/tools/video-editor/compositions/AudioTrack.tsx
src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
src/tools/video-editor/compositions/compiledAudioSourceClock.test.ts
src/tools/video-editor/compositions/compiledAudioSourceClock.ts
src/tools/video-editor/compositions/continuousPCM.contract.test.tsx
src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx
```

The worktree was clean before and after the check. The existing `tsconfig.app.json`
was used unchanged: strict `src` checking, ES2020/DOM libs, bundler resolution,
existing root aliases, existing test exclusions, and `skipLibCheck`.

## Dependency and lock provenance

The own leaf overlay was `/tmp/app-public13-pcm-project-typecheck-leaf13.fZ1m9h`.
It linked the actual worktree `src`, `vendor`, `config`, and `supabase` roots and
`tsconfig.app.json`; the public13 Composition package was extracted as regular
files from the immutable archive. Other package entries were links to the
read-only retained dependency tree. No install, network access, patch, or write
to `/home/user/work/app/node_modules` occurred.

| Fact | Value |
| --- | --- |
| Composition archive | `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` |
| Archive size | `58,477` bytes |
| Archive SHA-256 | `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |
| Archive SHA-512 | `eaa80401c7d8a841ae89eb284650458f54271200ca759b22b1076b322bce36d73794072df2d85dcd56cd57a2fb958e5fd83f6fbd32191d30fcbca85f5a02ceb9` |
| Lock integrity | `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==` |
| Installed package | `@banodoco/timeline-composition@0.0.13` |
| Installed archive files | 77 regular files; all 77 names and bytes matched the archive |
| Node / npm | `v22.22.0` / `10.9.4` |
| TypeScript | `5.9.3`; SHA-256 `8d5fa5bd883fec0979fc2004f1fe1d99aef40570155d550eadc0b03b55513bf0` |

The package identity check confirmed the lock version/resolved/integrity and
Composition peer declarations. Shared peers resolved at these versions from the
read-only shared install: React and React DOM `18.3.1`; Remotion, `@remotion/media`,
`@remotion/layout-utils`, and `@remotion/player` `4.0.509`; Three `0.185.1`.

The normal Runtime013 lock check passed:

```text
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
ok runtime.lock.json (matches pinned producer commit)
```

The lock identifies producer commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`,
producer version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
and 13 locked files.

## Exact typecheck

Working directory was the own leaf overlay. The completed valid command was:

```sh
flock /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 \
  /tmp/app-public13-pcm-project-typecheck-leaf13.fZ1m9h/node_modules/typescript/bin/tsc \
  --noEmit -p tsconfig.app.json
```

Start: `2026-10-20T14:36:54Z`  
End: `2026-10-20T14:37:44Z`  
Exit: `0`  
Combined stdout/stderr: `0` bytes, `0` lines.

There are no current diagnostics to attribute to the seven-file candidate delta;
therefore base-vs-current attribution is **none required**. No base typecheck was
run, in keeping with the one-valid-project-check boundary.

Execution note: a provisional shell launch was interrupted before returning, and
a subsequent provisional overlay run reported two missing-module errors because
the temporary overlay omitted tracked `config` and `supabase` roots. Those errors
were explicitly discarded as overlay setup failures, not App diagnostics. The
overlay was corrected, and the command above is the only result used. The final
overlay includes all four actual source roots and produced zero diagnostics.

## Limits and next steps

No product fix, config weakening, library bump, duplicate typecheck, broad Vitest
run, full suite, browser/e2e, build, socket/live-runtime test, parity test, merge,
or integration-pin claim was made. The orchestrator may use this as the bounded
public13 PCM consumer source-typecheck evidence and must keep later cap and
automatic-placement sources separate.
