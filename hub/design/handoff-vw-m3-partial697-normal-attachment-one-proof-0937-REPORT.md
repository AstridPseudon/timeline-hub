# Partial697 normal-attachment proof

## Result

PASS. One central named-suite request completed after the diagnosed normal
environment-only attachment was established on this live source. No product,
API, DTO, pin, authority, assertion, threshold, denominator, renderer, or
shared-dependency change was made.

The live source is:

    /home/user/work/wt/vw-m3-partial697-normal-attachment-one-proof-0937

It is Agent commit `b97a36d80c96865f30ab3474201930ca8c2f1458`. The only
worktree change is the authorized untracked top-level read-only carrier:

    /home/user/work/wt/vw-m3-partial697-normal-attachment-one-proof-0937/remotion/node_modules
      -> /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules

The target and real `@banodoco` scope/package parents were checked before the
symlink was created. The shared graph was not written. The readiness control
passed with Composition registry IDs effects=1, animations=6, transitions=2;
archive 77/77 regular files and SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; Node
`v20.19.4` and SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`; and all
12 direct Composition/Remotion/React/esbuild imports resolved inside the
approved graph.

Exact readiness command (exit 0; JSON output SHA-256
`cd8f32cb6e9d93d64aa46e6658aeec7be143f2da3606a1ad9c3cb38f9b5f72e8`):

    PYTHONDONTWRITEBYTECODE=1 python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-partial697-snapshot-dependency-diagnosis-0932-READINESS.py --root /home/user/work/wt/vw-m3-partial697-normal-attachment-one-proof-0937 --graph /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules --artifact /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/artifacts/banodoco-timeline-composition-0.0.13.tgz --node /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node

## Dependency diagnosis carried forward

The prior 0932 absent-attachment control failed closed at
`remotion/node_modules/@banodoco/timeline-composition/package.json`, matching
the 0923 `22788` snapshot failure. The relevant current source paths are:

- `tests/packs/rendering/test_presenter_scene_capability.py:26-31` selects the
  immutable public13 artifact and peer graph; `:43-48` extracts Composition
  privately and leaf-links only borrowed peers.
- `scripts/gen_effect_registry.py:146-155` independently resolves
  `ASTRID_REMOTION_PROJECT_DIR` or `ROOT/remotion` and requires the top-level
  Composition manifest.
- `tests/packs/rendering/presenter_crop_capture.py:35-57` stages the geometry,
  entry and capture helpers and starts Node.
- `tests/packs/rendering/presenter_crop_capture.mjs:5-8,31-49` imports
  `@remotion/bundler`, `@remotion/renderer`, the geometry helper, bundles,
  opens the recorded headless browser, renders four stills, and writes
  `inspection.json`.
- `tests/packs/rendering/presenter_crop_geometry.mjs:3-5` imports the public
  Composition root/evaluation modules; `presenter_scene_capability.mjs:8-14`
  imports esbuild, React, React DOM, Remotion, and Composition/evaluation.

The normal test-service carrier is the source `remotion/node_modules` entry;
`bin/test-run` includes it in the temporary Agent snapshot. No recycled
diagnostic checkout was used.

## Central request and evidence

Exactly one request was made:

    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-partial697-normal-attachment-one-proof-0937 e2e-viewing-partial697-retained-one-physical-0923

It returned ID:

    vw-m3-partial697-normal-attachment-one-proof-0937-e2e-viewing-partial697-retained-one-physical-0923-1021094000-10870

The matching wait was:

    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test vw-m3-partial697-normal-attachment-one-proof-0937-e2e-viewing-partial697-retained-one-physical-0923-1021094000-10870

Result: exit 0, 17 seconds; 2 tests collected, exactly 1 physical partial
case passed in 14.74 seconds. The explicit 799 px case was collected but not
executed. The existing single browser lock wrapped capture, evidence copy and
cleanup. Browser path was
`/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
with the approved prior hash
`63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4`.

Evidence was retained before central scratch cleanup at:

    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-partial697-retained-one-physical-0923-result/results

Files and SHA-256:

    frame-0.png             fa68d076a79c9c553fc79fc83128c55da7ed542aed47640f6e571598b2e3b2f6
    frame-3.png             ddea7b2cb0e89d3cca6df0bd7b70e160338122d5a72d4ad12bed1ebf14e08886
    frame-4.png             fa68d076a79c9c553fc79fc83128c55da7ed542aed47640f6e571598b2e3b2f6
    frame-5.png             79ef9e2d8d7c5456f463bd32e9432c0f9a47a60ccbc7601638f63822f1b425e7
    inspection.json         ea3f33f31542264526fa211e9b45efe7229639c3f1f712536fb4ac961e72454c
    partial-comparisons.json 02643d6ce5130875bed9e022f99fd2697864cd6a111a526d7edc0820a893a3a4

`sha256sum -c sha256sums.txt` passed for all six listed files. Every retained
file is a regular file with `nlink=1`; the four PNGs, JSON files, and manifest
have distinct retained inodes.

Exact retention verification:

    (cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-partial697-retained-one-physical-0923-result/results && sha256sum -c sha256sums.txt)

The comparator recorded the approved expected partial geometry:

- private697 crop `(298,202,339,219)` versus public/compat799 crop
  `(298,202,345,219)`; erase `(300,206,343,215)`.
- areas are `697` private versus `799` public/compat and `387` erase.
- padding is exactly `16/697` private and `16/799` public; erase is zero.
- natural pairs are stable at private `.44763271162123386`, public/compat
  `.42052565707133915`, and erase `.8682170542635659`.
- planted controls retain the strict boundary: private crosses at count 15,
  public/compat at count 16, and erase remains above; controls 8, 15, 16,
  and 20 remain present in the comparator JSON.

These are the intended partial-vs-explicit geometry/denominator facts, not a
claim that private697 and public799 are identical. No threshold or denominator
was changed. Default, raw-invalid, broad D09 and the explicit 799 physical run
remain open/unqualified.

## Tests and limits

- PASS: the qualified static readiness command above.
- PASS: the one central named suite and its retained evidence manifest.
- NOT RUN: Agent full suite, any alternate/full central suite, or any second
  physical request.
- The Gate6 priority worker was allowed the requested handoff window and later
  ended HELD for its separate private-graph storage gate; this partial proof
  did not consume or alter that authority.

Recommended next step: manager custody review of the retained result directory
and the live-source carrier; do not relabel this partial proof as Gate6 parity.
