# Gate6 frozen source guard checklist

These values come from the approved owner controller successor and existing
frozen runtime graph. They are guard inputs, not permission to mint a tuple.

## Source tuple

```text
Agent server source: d0a5072bbe7b7ce9489f43aa0a81027ec400343
Agent server tree:   6adb4a1190dfb2874e101565f37eccd392b1ae2f
Runtime server source: 8f105c26e3b62f9c2683f717a9773a12bc775a8e
Runtime server tree:   b7f456d5135cba6049980ebc43a91c7a72ab8f7e
Runtime official producer source: 2c4ac180c2220bdad966bc01e95ad230e99ce26a
Runtime official producer tree:   7ab412cc4bcbe517efcfa806e092336390312e18
Runtime artifact version: sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56
Official client contract version: 0.2.13 (public client013)
Runtime schema digest:    sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4
Runtime component manifest: sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
Runtime artifact files: 75
Composition source: 5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8
Composition public artifact: sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
Composition public regular members: 77
```

Immutable d0a runtime graph:

```text
project: /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b
lock digest: c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24
whole graph digest: 4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c
graph files: 21455
```

## Six peer byte guards

The tuple must pin these exact files for both App and Agent consumers:

```text
node_modules/remotion/dist/cjs/audio/shared-audio-tags.js  sha256:471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c
node_modules/remotion/dist/esm/index.mjs                   sha256:9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8
node_modules/@remotion/player/dist/cjs/use-player-methods.js sha256:ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46
node_modules/@remotion/player/dist/esm/index.mjs              sha256:d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12
node_modules/@remotion/player/dist/cjs/use-playback.js        sha256:6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0
node_modules/@remotion/player/dist/cjs/PlayerUI.js             sha256:5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb
```

## Toolchain and controller guards

```text
Node: v20.19.4
Node SHA-256: 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
Chrome: 155.0.8059.84
Chrome package: 155.0.8059.84-1
Chrome binary SHA-256: cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76
Chrome tree SHA-256: 5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e
Chrome tree files: 255
Minimum free bytes: 10 GiB
Browser lock: /tmp/timeline-viewing-browser.lock, held centrally
```

The controller also requires a real private dependency graph, direct short
`/tmp/timeline-tab-audio-*` temp ownership, clean Agent/Runtime sources, exact
Composition/package manifests, unchanged source versions before/after setup,
and the owner-port readiness set. Missing or mismatched inputs refuse before
capture.

## Required official-client fields

The frozen tuple `client` object must state `official: true`, producer source
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, producer tree
`7ab412cc4bcbe517efcfa806e092336390312e18`, producer version
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
artifact count `75`, and a safe relative file map containing at least
`src/integrations/runtime/generated.ts`. The App source/tree and complete
file-map digests remain manager-supplied; do not infer them from an install.

## Fresh grant and marker

`TAB_AUDIO_GRANT_PATH` must name a fresh JSON grant with `approved: true`,
profile `native-codec-chrome155`, exact Chrome executable/version/binary/tree
hashes, exact Node version/hash, and the selected App source/tree. The
`TAB_AUDIO_RUN_MARKER` JSON must match the grant's App source/tree. Existing or
reused grants/markers are refused and no marker is created by this packet.
