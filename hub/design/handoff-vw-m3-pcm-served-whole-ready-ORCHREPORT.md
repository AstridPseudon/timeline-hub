# PCM served whole-scope freeze

Preparation-only handoff for one manager-granted central HTTP qualification.
No listener, browser, socket-backed fixture, central request, grant, full
suite, renderer activation, normal-route claim, or phase claim was run.

## Frozen source

- Source worktree: `/home/user/work/wt/vw-m3-pcm-served-whole-ready`
- Branch: `tl/vw-m3-pcm-served-whole-ready`
- Final committed source SHA: `ab935f77378ba5ea1df55ba775654f8bba233ebc`
- Source tree SHA: `16c18d6db01fa330d497ff9147786e65e01e54c8`
- Source preflight and postflight status: empty, including untracked files
- Source HEAD/tree before and after staging: unchanged

The source branch was not edited, checked out, merged, rebased, or committed
by this worker. The source worker and qualified peer graph worktrees remain
clean.

## Stable ORCH project

The manager-facing project is the worker-owned, read-only path:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-served-whole-ready/checks/remotion`

It contains byte-copied current source helpers and Remotion tests. Its
`node_modules` entries are read-only symlinks to the existing qualified graph
at `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`; the
Composition entry points to the existing public12 extraction at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-pcm-producer-current/checks/public12/package`

No dependency was installed, copied, or modified in another worktree.

Helper hashes:

```text
attempt-envelope-pcm.mjs        db7bc06d2b3c9efecac015d59d965ef4dfa718e13f1ef303f190c3831bc95719
compiled-audio-source-clock.mjs 6ce210e91547d8bca901dc23fe3b06eae0d463fa18d6e1cb79d23494f5145ffc
normal-audio-sources.mjs        dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4
```

Staged test hashes:

```text
tests/composition-package.mjs                     b889a9610311b38d2170ffaa5c1819a55af9a4386a8e4817b25c85f9f6f23be7
tests/gapless-mp3-source-origin.test.mjs          269e147352e8ca84d578285c2396977998683e8c56d5f796738771aa221426a6
tests/long-audio-source.test.mjs                   e80f3068bfa738dde13c35a7ed07ff22f1ec6322d0d1c0efba8037cb7ceb5e52
tests/normal-audio-native-sources.test.mjs         d27108f95cbec13b3422aad7a3a46ca370bc7e5dad1e657ae2de2922d77cb0c9
tests/normal-audio-sources.test.mjs                b0139f14f3ce9792503ae218d98c82adfff85b8151a7b91c508fb6382c6b1c3e
```

Environment and graph verification:

- public12 archive SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- public12 package: version `0.0.12`, exactly 77 archive members
- React/react-dom: `18.3.1` / `18.3.1`
- Remotion, media, layout-utils, Player, web-renderer, renderer, bundler,
  CLI: `4.0.509`
- Node executable: `/tmp/vw-m3-agent-gate-node20.19.4/bin/node`
- Node version: `v20.19.4`
- Whole peer graph root/scoped symlink shape: PASS against the qualified
  graph; the project is read-only.

Six qualified render hashes:

```text
@remotion/player/dist/cjs/PlayerUI.js             5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb
@remotion/player/dist/cjs/use-player-methods.js   ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46
@remotion/player/dist/cjs/use-playback.js         6c8369a19d7a29eab5dab4642799172d4f2a7e11dad25edcb673ec5729fb0
@remotion/player/dist/esm/index.mjs                d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12
remotion/dist/esm/index.mjs                        9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8
remotion/dist/cjs/audio/shared-audio-tags.js       471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c
```

## Frozen controller and fixture bytes

The new handoff-named files are byte-identical copies of the approved final
guard-fix artifacts. Their hashes are therefore unchanged from the final
guard review:

```text
controller.py    72f5c85e73082e068b2898e62ce33ce3bb6733129f929eb9333e8de734f63c3e
fixture.py       2298b10a512fe5b32a6ba20ed5b806a189ed4e6a065f125833bc91709b734ba8
regressions.py   d7aa4ee955aca24bc72f48ff2a0cb805e4df41f97c88fd853a3575135c9f17d5
```

Absolute handoff paths:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-controller.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-test_normal_audio_served_sources.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-guard-regressions.py
```

## Checks completed

```text
python -B handoff-vw-m3-pcm-served-whole-ready-controller.py ... --scope whole --check
  PASS: public12 archive / all 77 members / peers / Node / source / helper bytes
ruff check <handoff controller, fixture, regressions>
  PASS: All checks passed
pytest <handoff guard-regressions.py>
  PASS: 4 passed in 0.35s
Node --check <all staged helpers and tests>
  PASS
whole peer graph + version + Node 20.19.4 probe
  PASS
```

## Manager-only grant template

This is the one approved scope: `whole` is exactly seven central-only cases.
It excludes the two ordinary window/layer phase cases. Do not substitute
`with-phase`, normal-route activation, or a render/export claim.

Named suite registration (template; not submitted here):

```text
agent integration-viewing-pcm-served-whole-ready /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-whole-ready-controller.py --source-sha ab935f77378ba5ea1df55ba775654f8bba233ebc --project /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-served-whole-ready/checks/remotion --node /tmp/vw-m3-agent-gate-node20.19.4/bin/node --scope whole
```

If and only if the manager grants that named suite, the central service
request would be:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-pcm-served-whole-ready integration-viewing-pcm-served-whole-ready) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Neither command was run by this worker. The seven-case whole result, when
eventually run centrally, must not be described as phase transport, normal
rendering activation, Player/export parity, or a full M3/Gate 6 result.
