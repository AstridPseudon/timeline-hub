# MAIN run handoff: coherent public current Agent full

**Status: HOLD — do not request or run the full lane until the final wrapper
delta receives independent APPROVE.**

This handoff supersedes the 1010 draft. It records one exact MAIN run against
the frozen current Agent source. This worker did not build, install, launch,
run pytest, or request a full suite. MAIN must resolve the target SHA and tree
once at setup start, then refuse any source drift.

## Exact source tuple

The Agent target is the current merged source at `hub/tl/integration`, resolved
at setup start to commit
`b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`, tree
`3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`. The matching
`hub/timeline/agent/tl/integration` ref was also at this SHA/tree at review.
The checkout used by MAIN must be clean, full Git, and must retain the exact
runtime lock below; `/home/user/work/agent`, a worker checkout, or a relabelled
old profile is not an authority.

| input | exact identity | durable MAIN location |
| --- | --- | --- |
| Agent source | branch `hub/tl/integration`; commit `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`; tree `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857` | `/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/agent-b3c96a758` |
| Runtime source | commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`; tree `6abc2f117391de8e7e35c0283f575a002199894d` | `/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/runtime-b92d3e7a` |
| public Runtime-client source | commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; tree `d3a290b407fa61e6ab2d476f50c068073f70df00`; package `astrid_runtime_client==0.2.14` | `/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/client-95bd3c5f` (build from `packages/python`) |
| C13 Composition | source marker `30da0a5e05d4529a2b97b3c1818cf9e15842d628`; 77 regular tarball members; tarball SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; lock SHA-256 `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24` | `/home/user/work/main-timeline/coherent-public-current-b3c96a758/composition-c13-30da0a5e` |
| Runtime artifact | `astrid-runtime==0.1.0`; all76 artifact digest `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` | built privately from Runtime b92; do not substitute another profile |

`runtime.lock.json` in the Agent checkout must name client source commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. All three Git checkouts must be
clean and their HEAD commit/tree must be checked before any wheel is built.

## Durable wrapper and final delta

The wrapper source is
`scripts/full_coherent_public_current_integration.sh`. Its durable publication
target is:

```text
hub/tl/agt-m4-full-wrapper-current-batch-main-request-finalize-1023:
scripts/full_coherent_public_current_integration.sh
```

The final worktree blob is
`aa8dda3e9cf81301c163294ceec805d97be0d5c8`, SHA-256
`09822614697e50a0764c2a125bfd0575baadeeb2f87661b4b3a4a10551e96438`.
The harness has not yet published the final commit, so the wrapper commit is
**pending harness publication**; do not claim the pre-delta `ea1150b...`
worktree HEAD as the final wrapper commit. After publication, record the full
commit SHA and confirm that it contains this exact blob before MAIN activation.

The only source delta from the repaired `594c16e1f21340f179296fa341e22233df7efa54`
blob is the expected-Agent snapshot/provenance update:

```text
EXPECTED_AGENT_COMMIT=b3c96a758c1cfa2a609d1498e0e9ee401b32cc40
EXPECTED_AGENT_TREE=3467b7bffb0fe6edf9178c9a9de4d446c8ab8857
```

The two missing-wheel diagnostics now say `b3c Agent`. The repaired client
archive map remains exactly:

```text
packages/python/astrid_runtime_client/ -> astrid_runtime_client/
```

Independent delta review must approve this four-line identity/provenance
change and verify that no other wrapper line changed. That review must retain
the strict 164-pin carrier/hash, 166 installed distributions and `RECORD`
files, complete RECORD closure, regular/symlink-free files, all76 source and
wheel/install byte checks, the Agent/public95 client payload equality, eight
private import origins, C13/Node/ffmpeg checks, compact positive and wrong-byte
prefix guards, and direct child/process exit and SIGTERM propagation.

## MAIN-owned profile and missing-file census

Use one private root:

```text
MAIN_ROOT=/home/user/work/main-timeline/coherent-public-current-b3c96a758
SOURCE_ROOT=$MAIN_ROOT/source/agent-b3c96a758
RUNTIME_CHECKOUT=$MAIN_ROOT/source/runtime-b92d3e7a
CLIENT_CHECKOUT=$MAIN_ROOT/source/client-95bd3c5f
COMPOSITION_ROOT=$MAIN_ROOT/composition-c13-30da0a5e
PROFILE_ROOT=$MAIN_ROOT/profile/agent-coherent-public-current-b3c96a758
RUNNER_ROOT=$MAIN_ROOT/runner/approved-current-wrapper
```

Before pytest admission, enumerate this complete required-file set once and
report every missing path in one refusal; do not invent a venv, retry a broad
preflight, or reuse a stale profile:

```text
$SOURCE_ROOT/.git/HEAD and exact Git object/tree
$SOURCE_ROOT/runtime.lock.json
$RUNTIME_CHECKOUT/.git/HEAD and exact Git object/tree
$CLIENT_CHECKOUT/.git/HEAD and exact Git object/tree
$COMPOSITION_ROOT/.source-commit
$COMPOSITION_ROOT/artifacts/banodoco-timeline-composition-0.0.13.tgz
$COMPOSITION_ROOT/package-lock.json
$COMPOSITION_ROOT/node_modules/ (private, symlink-free)
$PROFILE_ROOT/venv/bin/python
$PROFILE_ROOT/venv/lib/python3.13/site-packages/
$PROFILE_ROOT/profile/astrid.json
$PROFILE_ROOT/metadata/venv-agent-child-s2.txt
$PROFILE_ROOT/wheelhouse/astrid-0.1.0-py3-none-any.whl
$PROFILE_ROOT/wheelhouse/astrid_runtime-0.1.0-py3-none-any.whl
$PROFILE_ROOT/wheelhouse/astrid_runtime_client-0.2.14-py3-none-any.whl
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
/home/user/work/fixtures/vibecomfy/
/usr/bin/ffmpeg
/usr/bin/ffprobe
```

The fresh profile must be private and symlink-free. Its carrier must contain
exactly 164 unique entries and SHA-256
`478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
The installed site must prove exactly 166 distributions and 166 `RECORD`
files, with the carrier plus the two Runtime/client product distributions;
product versions are Agent `0.1.0`, Runtime `0.1.0`, client `0.2.14`, and
schema `0.0.2`. Wheel bytes, installed bytes, and exact git-archive source
bytes must agree for Agent b3c, Runtime b92, and client 95. The Agent wheel
must carry the exact public95 client payload. `astrid`,
`astrid_runtime`, `runtime_protocol`, `astrid_runtime_client`, and
`banodoco_timeline_schema` must resolve only from the private site during the
installed-package probe; pytest's source `astrid` comes from `SOURCE_ROOT`.

The existing four-field `profile/astrid.json` shape must be preserved, with
both checkout fields set to the private site-packages path and
`runtime_environment` set to `$PROFILE_ROOT/venv`. The 164-pin file is copied
into this private profile; it is not a pointer to any shared or historical
environment.

## Construction prerequisites (MAIN only, after APPROVE)

Require more than 13 GiB free under `/home/user/work`. Materialize the exact
source checkouts and C13 artifact in `MAIN_ROOT`; verify commit, tree, clean
status, source marker, tarball/lock hashes, and Agent runtime-lock client
commit. Then build only into the private wheelhouse, without network or build
isolation:

```bash
python3.13 -m pip wheel --no-index --no-build-isolation --no-deps \
  --wheel-dir "$PROFILE_ROOT/wheelhouse" \
  "$RUNTIME_CHECKOUT" \
  "$CLIENT_CHECKOUT/packages/python" \
  "$SOURCE_ROOT"
```

The output must be exactly the three named product wheels. Build a new Python
3.13 venv at `$PROFILE_ROOT/venv` and materialize the approved 164-pin closure
from MAIN's private, read-only wheel/byte inventory. The inventory path and
materialization command must be named in MAIN's result; do not point at a
shared venv or relabel an older child environment. After the closure is
private and verified, install only the three locally built product wheels with
`pip install --no-index --no-deps --force-reinstall`.

Prepare C13 with the exact source marker, tarball, lock, private
symlink-free `node_modules`, and Node `v20.19.4`. Do not mutate
`/home/user/work/app/node_modules`, any shared runtime, or any shared venv.

## Exact MAIN invocation

After independent delta APPROVE, durable wrapper publication, source/profile
preflight, and the compact guard checks, MAIN may make exactly one request.
The command must be run with no ambient variables:

```bash
env -i \
  HOME=/root \
  LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  SOURCE_ROOT=/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/agent-b3c96a758 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/runtime-b92d3e7a \
  RUNTIME_CLIENT_CHECKOUT=/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/client-95bd3c5f \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/main-timeline/coherent-public-current-b3c96a758/composition-c13-30da0a5e \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy \
  FULL_COHERENT_PUBLIC_PROFILE_ROOT=/home/user/work/main-timeline/coherent-public-current-b3c96a758/profile/agent-coherent-public-current-b3c96a758 \
  FULL_COHERENT_PUBLIC_AGENT_WHEEL=/home/user/work/main-timeline/coherent-public-current-b3c96a758/profile/agent-coherent-public-current-b3c96a758/wheelhouse/astrid-0.1.0-py3-none-any.whl \
  FULL_COHERENT_PUBLIC_PINS=/home/user/work/main-timeline/coherent-public-current-b3c96a758/profile/agent-coherent-public-current-b3c96a758/metadata/venv-agent-child-s2.txt \
  bash /home/user/work/main-timeline/coherent-public-current-b3c96a758/runner/approved-current-wrapper/full_coherent_public_current_integration.sh
```

The wrapper's final command must remain exactly:

```text
exec "$PROFILE_PY" -m pytest -q -n 3 "$@"
```

No marker, cache/basetemp override, launcher, cleanup wrapper, socket,
browser, renderer, retry loop, or body substitution is permitted. The direct
exec must preserve collection, child, signal, and nonzero-exit statuses.

## MAIN result contract

MAIN must write `design/run-on-main-result-coherent-public-current.md` with
the actual durable wrapper commit/blob/SHA-256, the exact Agent b3 commit/tree,
Runtime b92, client 95, C13 identity/hash, profile/venv/carrier and all wheel
paths/hashes, 166/RECORD and eight-origin results, source/wheel/install byte
parity, Node/C13/tool checks, free-space admission, the exact `env -i`
command, and the terminal full-suite result. A setup refusal or profile
preflight is not a full result and must not be relabelled as one. The current
request remains HOLD until the final wrapper delta is independently APPROVED.
