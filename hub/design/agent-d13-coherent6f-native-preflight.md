# Agent D13 coherent-6f native preflight

Date: 2026-10-21. This is a preflight and handoff record only. It does not
qualify the native/socket/render/browser/full lane and does not activate a
pin, schema, caller, or broader 18/688 suite.

## Installed tuple

The manager-owned private attempt is complete at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging`

Selected interpreter:

`.../profile-staging/venv/bin/python` (Python 3.13.16, noneditable install).

| component | source / artifact | installed artifact hash or identity |
| --- | --- | --- |
| Agent | commit `6f2d8c350ad6838d2a2cd8da98e49465b1ab2406`, tree `698ae4df6ea9e9e89746fffabfaab15ac0c7d47f` | `astrid==0.1.0`, wheel `fa2f824d1068f6233dc852960726d597f21a243d768ff0cafe258b7afe391346` |
| Agent ancestry | approved security source parent `89a5bb654bdcdd7e3f555c3645f3fc8bcf7824f1` + current `a08a500077c7551fa8455b936d82adc2aae08f41` | exact merge tree verified from Git blob parity: 3268/3268 files |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31`, tree `6abc2f117391de8e7e35c0283f575a002199894d` | `astrid-runtime==0.1.0`, `12df54644e1acac46b9c396135ef345808a98515965f1f12f479f32adf3c9b0a` |
| client/artifacts | immutable `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` | `astrid-runtime-client==0.2.14`, `567605b13254f88ddeddad7b570553a2c50b5092908e6c4153553f9867e37254` |
| dependency lock | `metadata/venv-agent-child-s2.txt` | 164 unique entries, SHA-256 `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761` |

The existing Runtime b92/client 95 wheel bytes were retained; no Runtime,
client, pin, or shared environment rebuild was performed. Product origins and
representative native/data imports all resolve below the private
`venv/lib/python3.13/site-packages`. The production installed-origin probe
passed all eight required keys: `host`, `child`, `action`, `client`, `sdk`,
`runtime_protocol`, `runtime_protocol.platform`, and `astrid_runtime`.

The existing SourceProfile carrier is the only profile shape, in
`profile/astrid.json`:

```json
{
  "profile": "astrid",
  "runtime_checkout": "<private-site-packages>",
  "source_checkout": "<private-site-packages>",
  "runtime_environment": "<private-venv>"
}
```

The final private audit found 166 `RECORD` files / 26,283 rows, every recorded
path contained and hash-valid, and zero symlinks in the stage. Forty-eight
inherited dependency Python shebangs were rewritten to this private
interpreter; five Agent console scripts were generated with it. Private
`RECORD` rows were refreshed for those intentional launcher rewrites.

## Proof already run

From `/tmp`, with `env -i`, neutral cwd, no `PYTHONPATH`, and `python -I -B`:

- Actual imports passed for `astrid`, `astrid_runtime_client`,
  `runtime_protocol`, `astrid_runtime`, `banodoco_timeline_schema`, NumPy,
  Pillow, OpenCV, and PyYAML. No import origin had a symlink component or a
  checkout path in `sys.path`.
- `python -I -B -m astrid --help` exited 0.
- `python -I -B -m astrid doctor --json` exited 1 with the normal Runtime
  unavailable diagnostic because no daemon/catalog was present. It did not
  produce the former `ModuleNotFoundError` or `UnboundLocalError` masking
  signature. Doctor was not treated as a Runtime pass.
- The exact Agent archive was compared to commit `6f2d8c…` using Git blob
  hashes; all 3268 files matched. The private stage is about 944 MiB and
  currently has 13,913,112,576 bytes free on its filesystem.

No native process, Runtime socket, renderer, browser, real render, or full
suite was run by this preflight.

## Existing D13 positive and later command

On approved source `6f2d8c…`, the positive remains active (not xfailed):

`tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render`

This is the one node selected by the existing
`d13-native-positive-render-integration` lane. Its retained assertions cover
the registered `rendering.assemble_timeline` producer, ordered managed-media
reads, settled proposal, `producer.guard`, lost acknowledgement, durable
flight identity, restart/exact retry, accepted revision/publication identity,
ordinary revision-pinned render admission, MP4/`ffprobe`, and guarded undo.
The adjacent canonical proposal and legacy-refusal tests remain safety
coverage; they are not substituted for the one native positive.

The prior reviewed source-context command, recorded here as the exact node
shape and not as a command to replay, was:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default:/root/.local/bin:/usr/local/bin:/usr/sbin:/bin \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-main95bd \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-main95bd/node_modules \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages \
  /home/user/work/venv-agent-child-c13-a8a40afd/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

That historical source command is not the installed-profile proof: it has
checkout/PYTHONPATH authority and a different child. The manager's one later
run must preserve the node, Remotion, and exact test node while binding the
selected installed profile above and proving the eight installed origins
before entry. No native execution is authorized by this document.

## Runtime, browser, tools, and resource closure

- Runtime/client contract closure is present: protocol `workspace.v1`, client
  contract `0.2.14`, schema digest
  `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
  component manifest digest
  `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
  133 operations, and the retained Runtime artifact identities from the
  staging report.
- Node is present at
  `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, version
  `20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Remotion profile is present at
  `/home/user/work/runtimes/agent-remotion-main95bd` with private-read-only
  use required later; package lock SHA-256 is
  `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
  Its declared Composition is `0.0.13` and Remotion is `4.0.509`.
- `/usr/bin/ffmpeg` and `/usr/bin/ffprobe` are present (6.1.1-3ubuntu5) with
  hashes `ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41`
  and `272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f`.
- A usable Chromium/chrome-headless-shell executable was not found in the
  checked system or shared cache paths. Fonts, OMP/native inputs, film media,
  and the final public-input manifest are not proven by this install task.

## Authority, isolation, and grants

The trusted import authority is the selected interpreter plus its immutable,
noneditable private site-packages tree, entered through the existing
SourceProfile carrier. The profile is provenance/selection data; it adds no
new field or authority. Runtime credentials remain Runtime-owned and are not
copied into this stage. The isolated doctor reported authorization not
observed; no credential or native execution grant is active.

Only the named private staging record was mutated. The shared Runtime checkout
remains clean, the Agent worktree remains clean, no shared venv/node_modules
was written, no source checkout or `PYTHONPATH` was used for installed proof,
and the stage has no symlinks. No private attempt data is shared with another
profile.

## Readiness decision

Ready for the manager:

- exact 6f2d8c source wheel installed and source ancestry recorded;
- exact b92 Runtime, immutable 95 client, and 164-entry lock closure present;
- installed origins, hashes, RECORD containment, shebangs, symlinks, help, and
  normal unavailable doctor behavior independently checked;
- one existing D13 positive node identified without changing its assertions.

Not ready for the one native positive run:

- no active Runtime daemon/socket or trusted Runtime credential/grant;
- no verified browser executable/headless-shell resource;
- no final fonts/OMP/native/media/public-input resource closure;
- the known historical command still names source/PYTHONPATH roots and the old
  child, so the manager must bind the private installed profile before entry;
- native/socket/render/browser/full execution is explicitly pending.

Manager next step: perform exactly one later `d13-native-positive-render-integration`
run on the exact installed tuple after resolving the not-ready resources and
authority, then report the real node result. Do not request broader 18/688,
full, schema/pin, caller-activation, or render/browser runs from this
preflight.
