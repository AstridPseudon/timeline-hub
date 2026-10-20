# App postbebadd full-suite preparation

Date: 2026-10-20 UTC  
Worker: `app-m3-postbebadd-current-full-prepare-execute`

## Submission gate

The manager marker
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/postbebadd-full-READY`
was absent during preparation. No central full suite has been requested. The
marker must supply the exact App commit and tree; a later moving
`/home/user/work/app` checkout will not be used as a test source.

The current committed integration candidate is the qualified Native None merge
`c57dcc26162642f503532f143ceb96bb185273aa`, tree
`b02e5380cc664bf07e4703e9a388bce0442ff645`. An immutable App checkout was
requested through `orch/bin/request-checkout`; its result is pending. If READY
names a different commit, request and use that exact pin instead.

READY subsequently named this exact candidate, and the detached checkout was
created at `/home/user/work/wt/app-pin-c57dcc26`. The one central run submitted
after the guard checks is:

`app-full-postbebadd-public13-c57dcc26-agent8130-runtime2c4-1020173410-17473`

The orchestration suite entry is
`full-postbebadd-public13-c57dcc26-agent8130-runtime2c4`; it invokes the
established private13 full wrapper with App c57/tree b02e5380 and per-run
cache/TMPDIR paths.

## Environment and guards

- Private13 dependency overlay (read-only):
  `/tmp/app-public13-pcm-complete-source-tsc-leaf13.01Xcjn/node_modules`.
  It is not `/tmp/app-coherent-deps12/node_modules` and does not resolve into
  `/home/user/work/app/node_modules`.
- Composition archive (read-only):
  `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, 77 files,
  58,477 bytes, SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Peer guards passed against the private13 overlay: React and React DOM
  `18.3.1`; Remotion, `@remotion/player`, `@remotion/three`,
  `@remotion/layout-utils`, and `@remotion/media` all `4.0.509`.
- Immutable Agent source lease: `/home/user/work/wt/app-m3-agent8130-safety-source-keeper`,
  clean, commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Immutable Runtime source/producer lease:
  `/home/user/work/wt/app-m3-runtime013-producer-source`, clean, commit
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- App `runtime.lock.json` names Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`,
  producer version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
  and 13 lock files; Runtime artifact count is expected to be 75.
- Tracked public browser source remains the established bundle: provenance
  commit `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1`, tree
  `07ce61f24ec38a1a60c4a981b6bd666f4971bd67`, 155 files, provenance SHA-256
  `5b0924452cbb51d74be04f0a4a6ac390c462d77a11bebb5274836a4e66468f82`,
  vendor-tree digest
  `4bf1169751a201d4c88024871adbd77ee9673ca068e79cfecf17faa2ef7be98a`.
- The existing snapshot preload is
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs`.
  The full runner must use Vitest `--configLoader=runner --no-cache` and a
  per-run private cache/TMPDIR keyed by the exact App tree. No shared
  `node_modules`, Vite cache, npm cache, or venv may be written.

## Checks completed

From the clean worker snapshot, without install, build, TypeScript, render, or
browser execution:

```text
python3 private13/archive/peer guard: PASS (77/77 archive members)
node scripts/build/verify-astrid-vendor-sources.mjs: PASS (65 pinned, 155 browser, 20 imports)
node scripts/vendor-lock.mjs check runtime.lock.json: PASS
git status --short --branch: clean
```

The package and lock hashes in the candidate commit are package.json
`4afacd8c57182a7ba7b2307ad285a083e63d1018ffef290081d8eeedbd155ffd`,
package-lock.json
`7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14`, and
runtime.lock.json
`550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2`.

The run is now queued/running. Monitor that same result ID; do not retry it.
Classify every terminal failure against
the prior `full-main574-public13-8bd8f741` baseline and
`design/app-full8bd8-current-classification.md`, preserving all behavior
tests.
