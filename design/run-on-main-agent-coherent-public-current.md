# MAIN run handoff: coherent public current Agent full

**Status: CODE APPROVED / STORAGE HOLD - the source-coherent wrapper delta is
independently APPROVED. Do not request or run the full lane until the new
immutable Remotion runtime and private profile are present, and free storage
is above the existing >13 GiB admission floor.**

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
| C13 Composition | source marker `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`; 77 regular tarball members; tarball SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; lock SHA-256 `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24` | `/home/user/work/runtimes/agent-remotion-0014` |
| Runtime artifact | `astrid-runtime==0.1.0`; all76 artifact digest `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` | built privately from Runtime b92; do not substitute another profile |

`runtime.lock.json` in the Agent checkout must name client source commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. All three Git checkouts must be
clean and their HEAD commit/tree must be checked before any wheel is built.

## Remotion source-coherence audit

The old C13 runtime was built from Agent commit
`30da0a5e05d4529a2b97b3c1818cf9e15842d628`. I compared the complete tracked
`remotion/` tree at that commit with Agent target b3c, not just the package
version or lock. Both trees contain 73 files, but their remotion subtree
objects differ: old `08236aaf8c63e43dafba6baa4fe412343edd6a99`, target
`aa2b36555203f7f1a82cc5cb399b0b447f03b808`. The exact comparison was:

```text
git diff --name-status 30da0a5e05d4529a2b97b3c1818cf9e15842d628 b3c96a758c1cfa2a609d1498e0e9ee401b32cc40 -- remotion
M       remotion/scripts/fetch-shared-browser.mjs
M       remotion/src/LiveSceneClip.tsx
```

The other 71 tracked Remotion blobs are byte-identical. The differing blobs
are exact and material:

```text
remotion/scripts/fetch-shared-browser.mjs
  30da blob cf16755930ecc41e7c21891a236c7e8062568bd3
  b3c  blob f82c1268bb6cfd7221faeb029a38ef8addfb155e
remotion/src/LiveSceneClip.tsx
  30da blob cf14ed357ea607d8807ae883cd1ef444468da1ba
  b3c  blob 1aace8ab33c39114c75aad60ba664a319dfeaacf
```

`LiveSceneClip.tsx` changes the consumed SceneSurface import path, and the
browser installer source also differs. Therefore the old 30da runtime is not
source-coherent with the b3c full. The fact that the C13 package version,
tarball, and package-lock hash stay the same does not prove host-source
coherence.

MAIN must request a new immutable runtime from b3c using the existing
request-runtime path and the same C13 lock:

```text
Runtime name: agent-remotion-0014
Request:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime agent-remotion-0014 b3c96a758c1cfa2a609d1498e0e9ee401b32cc40 c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24
Expected immutable project: /home/user/work/runtimes/agent-remotion-0014
Expected generated env file: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion-0014.env
Expected runtime env values:
PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0014
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages
```

The request was not made by this worker. The new runtime, its env file, its
`.source-commit`, its 0.0.13 artifact, its exact C13 lock, and its private
symlink-free `node_modules` are currently missing. The existing 0013 runtime
must not be relabelled or mutated.

## Durable wrapper and final delta

The wrapper source is
`scripts/full_coherent_public_current_integration.sh`. The previously
approved wrapper baseline was published at:

```text
hub/tl/agt-m4-full-wrapper-current-batch-main-request-finalize-1023:
scripts/full_coherent_public_current_integration.sh
```

Its exact commit `297fbe0e5cf9bc37c7115dae294838f96df95f16`, tree
`a4fdb4a28b9d7a88267105f8261518336a18047e`, blob
`aa8dda3e9cf81301c163294ceec805d97be0d5c8`, and SHA-256
`09822614697e50a0764c2a125bfd0575baadeeb2f87661b4b3a4a10551e96438` are
historical provenance only. That baseline is not an executable target: its C13
marker still names old 30da and it must not be used for this full.

The approved durable publication target is the exact wrapper at the verified
branch:

```text
hub/tl/agt-review-main-full-remotion-binding-delta-1102:
scripts/full_coherent_public_current_integration.sh
```

The exact approved wrapper identity is recorded below. This target resolves to
the independently approved source-coherent wrapper; its C13 marker and fallback
runtime path are the b3c/0014 values described below.

This worktree changes only the wrapper metadata needed for source coherence:
`EXPECTED_C13_SOURCE` becomes b3c and the fallback project path becomes
`/home/user/work/runtimes/agent-remotion-0014`. The strict artifact, source,
wheel, install, 164-pin, 166-distribution/RECORD, import-origin, and direct
pytest exit/SIGTERM guards are retained. Independent review APPROVES this
two-line delta at commit `fc4c23d079f17aa4d8f167b385c7e5bda2edd299`, tree
`7ce6a0b8022928cd98a2f7cd448bf9d24a442587`, wrapper blob
`198a94ad1f1c9921705399febb7e7f71dffd419d`, SHA-256
`0e1b5ccd2157788d53d6ba7fa6c0e1adc362e97f190e734cc023bf4ff92e87d`.
This approval is code-only: the b3c-source `agent-remotion-0014` runtime is
absent and the private profile is not built, so storage remains HOLD.

The previously approved source delta from the repaired
`594c16e1f21340f179296fa341e22233df7efa54` blob was the expected-Agent
snapshot/provenance update:

```text
EXPECTED_AGENT_COMMIT=b3c96a758c1cfa2a609d1498e0e9ee401b32cc40
EXPECTED_AGENT_TREE=3467b7bffb0fe6edf9178c9a9de4d446c8ab8857
```

The two missing-wheel diagnostics now say `b3c Agent`. The repaired client
archive map remains exactly:

```text
packages/python/astrid_runtime_client/ -> astrid_runtime_client/
```

The new source-coherence delta is now approved. The review verified that no
other wrapper line changed and retained
the strict 164-pin carrier/hash, 166 installed distributions and `RECORD`
files, complete RECORD closure, regular/symlink-free files, all76 source and
wheel/install byte checks, the Agent/public95 client payload equality, eight
private import origins, C13/Node/ffmpeg checks, compact positive and wrong-byte
prefix guards, and direct child/process exit and SIGTERM propagation.

Before activation, MAIN must use the normal durable lease for one exact run.
The lease must cover the successor wrapper path and its full committed
commit/tree/blob/SHA-256, the Agent/Runtime/client commit and tree tuple, the
b3c Remotion runtime and C13 hashes, the private profile and all three product
wheels, the 164-pin carrier, Node, VibeComfy, ffmpeg, ffprobe, and private C13
`node_modules`. The lease must name the exact `env -i` command below and refuse
the full while any input is missing, dirty, symlinked, or has an unverified
identity. Do not use the old wrapper SHA as the successor hash and do not
invent a lease result before MAIN records it.

## MAIN-owned profile and missing-file census

Use one private root:

```text
MAIN_ROOT=/home/user/work/main-timeline/coherent-public-current-b3c96a758
SOURCE_ROOT=$MAIN_ROOT/source/agent-b3c96a758
RUNTIME_CHECKOUT=$MAIN_ROOT/source/runtime-b92d3e7a
CLIENT_CHECKOUT=$MAIN_ROOT/source/client-95bd3c5f
COMPOSITION_ROOT=/home/user/work/runtimes/agent-remotion-0014
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
$RUNNER_ROOT/full_coherent_public_current_integration.sh (successor wrapper with recorded commit/tree/blob/SHA-256)
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

Require more than 13 GiB free under `/home/user/work`. Request the new
`agent-remotion-0014` runtime as specified above, then materialize the exact
source checkouts and verify commit, tree, clean status, b3c Remotion source
marker, tarball/lock hashes, and Agent runtime-lock client commit. Then build
only into the private wheelhouse, without network or build isolation:

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

Use the new `agent-remotion-0014` runtime with the exact b3c source marker,
0.0.13 tarball, C13 lock, private symlink-free `node_modules`, and Node
`v20.19.4`. Do not mutate `/home/user/work/app/node_modules`, the existing
0013 runtime, any other shared runtime, or any shared venv.

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
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0014 \
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
request remains HOLD until the source-coherence wrapper delta is independently
APPROVED, the new runtime is present and verified, and MAIN has materialized
the private profile. The exact final command above is the one allowed command;
it is not a claim that the profile or runtime already exists.

## Storage budget measurement (worker 1048, 2026-10-21T10:51:38Z)

This is a retained-size measurement, not a transient-peak claim. Measurements
use `du -sx -B1` (allocated bytes) and divide by 2^30. The exact current
source checkouts are present and clean at the following identities:

- Agent `/home/user/work/agent`: b3c96a758c1cfa2a609d1498e0e9ee401b32cc40,
  tree 3467b7bffb0fe6edf9178c9a9de4d446c8ab8857 — 119,758,848 bytes,
  0.111534 GiB.
- Runtime `/home/user/work/runtime`: b92d3e7a05eec65c142294ef4873edd059e9b31d,
  tree 6abc2f117391de8e7e35c0283f575a002199894d — 12,046,336 bytes,
  0.011219 GiB.
- Runtime client `/home/user/work/wt/rt-pin-95bd3c5f`:
  95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3, tree
  d3a290b407fa61e6ab2d476f50c068073f70df00 — 12,054,528 bytes,
  0.011227 GiB.

The separate source-checkout subtotal is therefore 143,859,712 bytes,
0.133980 GiB. It is not added again through the profile measurement below.

The existing coherent 164-pin/166-distribution reference profile was measured
at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b`.
Its `audit.txt` proves 166 RECORD files and the eight private origins, and its
`preflight.txt` records the 164-entry carrier. This is a size reference only:
its Agent is f4edcb4b, not the current b3c target. The profile components,
excluding its embedded `source/agent` copy and the 4,096-byte pip cache, are:

- venv: 658,956,288 bytes, 0.613701 GiB;
- wheelhouse: 57,868,288 bytes, 0.053894 GiB;
- profile and metadata: 28,672 bytes, 0.000027 GiB;
- profile subtotal: 716,853,248 bytes, 0.667622 GiB.

The existing immutable C13 reference runtime
`/home/user/work/runtimes/agent-remotion-0013` measured 394,047,488 bytes,
0.366985 GiB, including its 393,027,584-byte (0.366035 GiB) `node_modules`.
Its marker is the old 30da source, and its graph contains 33 symlinks; it is
not evidence for the absent b3c-source `agent-remotion-0014` symlink-free
graph. The exact 0014 runtime is therefore UNKNOWN and is not silently
substituted in this budget.

Adding the separately measured profile reference, exact current source
checkout analogues, and old C13 runtime gives a retained setup subtotal of
1,254,760,448 bytes, 1.168587 GiB. The only retained pytest scratch found at
`/tmp/pytest-of-root` was 9,211,904 bytes (0.008579 GiB), but it comes from
unrelated prior targeted runs and is not a bound for this full run; it is not
added to the setup subtotal. The historical profile tarball
`.../agt-m4-d13-final-current-wheel-profile-build-0851/private-profile-f4edcb4b.tgz`
was 413,593,693 bytes (0.385189 GiB), but it is a retained packaging artifact,
not a MAIN setup requirement or a measured concurrent peak, so it is also not
added.

Run scratch and peak: UNKNOWN. There is no MAIN full result, no `-n 3` full
run, and no real service peak log measuring pytest temporary files, worker
scratch, or concurrent setup/build phases. The retained end-state sizes above
must not be presented as a transient peak. Consequently there is no supported
measured peak plus 2 GiB margin from which to lower the admission floor. A
naive retained-subtotal-plus-2-GiB calculation would be 3.168587 GiB, but it
is explicitly not an admissible threshold because the missing peak is
UNKNOWN.

At measurement time, `df -B1 /home/user/work` reported 12,480,892,928 bytes
free, 11.623737 GiB. The existing >13 GiB requirement is 13,958,643,712
bytes; the measured shortfall is 1,477,750,784 bytes, 1.376263 GiB. Storage
need remains plainly: preserve the >13 GiB admission floor until MAIN has an
actual source-coherent setup/full-run peak measurement with known `-n 3`
concurrency and a 2 GiB margin. Do not change the wrapper threshold based on
this report.

## Final MAIN handoff consolidation (2026-10-21)

**Status remains CODE APPROVED / STORAGE HOLD.** The approved code identity is
wrapper commit `fc4c23d079f17aa4d8f167b385c7e5bda2edd299`, tree
`7ce6a0b8022928cd98a2f7cd448bf9d24a442587`, blob
`198a94ad1f1c9921705399febb7e7f71dffd419d`, SHA-256
`0e1b5ccd2157788d53d6ba7fa6c0e1adc362e97f190e734cc023bf4ff92e87d`.
The product source remains Agent b3c/tree3467; C13 remains Composition
0.0.13, not 0.0.14. The `agent-remotion-0014` name is only the new immutable
runtime destination: that runtime must be built from the exact b3c source.

MAIN is blocked until every prerequisite below is present and independently
verified in the MAIN profile:

1. Clean full-Git checkouts at `/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/agent-b3c96a758` (Agent b3c/tree3467 and `runtime.lock.json` naming client 95bd), `.../source/runtime-b92d3e7a` (Runtime b92/tree6abc), and `.../source/client-95bd3c5f` (client 95bd/tree d3a290), with exact HEAD/tree checks.
2. Immutable `/home/user/work/runtimes/agent-remotion-0014` with `.source-commit` b3c, the C13 0.0.13 tarball SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, the C13 lock SHA-256 `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`, and a private symlink-free `node_modules`; the generated `agent-remotion-0014.env` must point to that runtime and Node v20.19.4.
3. The durable runner at `/home/user/work/main-timeline/coherent-public-current-b3c96a758/runner/approved-current-wrapper/full_coherent_public_current_integration.sh` must match the approved wrapper identity above.
4. Private `/home/user/work/main-timeline/coherent-public-current-b3c96a758/profile/agent-coherent-public-current-b3c96a758` must contain `venv/bin/python`, private site-packages, `profile/astrid.json`, the 164-pin carrier SHA-256 `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`, metadata `venv-agent-child-s2.txt`, and exactly the three local product wheels (Agent 0.1.0, Runtime 0.1.0, client 0.2.14). It must verify 166 distributions, 166 `RECORD` files, eight private import origins, and source/wheel/install byte parity.
5. `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `/home/user/work/fixtures/vibecomfy/`, `/usr/bin/ffmpeg`, and `/usr/bin/ffprobe` must pass the wrapper checks. The required `env -i` invocation and direct final `exec "$PROFILE_PY" -m pytest -q -n 3 "$@"` remain unchanged.
6. MAIN must measure more than 13 GiB free on its own `/home/user/work` filesystem immediately before admission: threshold `13,958,643,712` bytes. No retained-size estimate substitutes for the missing transient `-n 3` setup/full-run peak.

Storage is still below the gate. The worker-side current read-only
`df -B1 /home/user/work` is `12,755,468,288` bytes free (`11.879456 GiB`),
short by `1,203,175,424` bytes (`1.120544 GiB`). The MAIN note separately
reports approximately 11 GB available; that is an admission fact for MAIN,
not a substitute for a MAIN-time measurement. The retained measurement at
2026-10-21T10:51:38Z was `12,480,892,928` bytes (`11.623737 GiB`), short by
`1,477,750,784` bytes (`1.376263 GiB`). Its retained `du -sx -B1` setup
subtotal was `1,254,760,448` bytes (`1.168587 GiB`): profile reference
`716,853,248`, exact source-checkout analogues `143,859,712`, and old C13
reference runtime `394,047,488`. The b3c-source 0014 runtime and the
transient full-run peak are UNKNOWN. Do not lower the >13 GiB floor.

Lead action: free or otherwise obtain the missing MAIN storage, then have
MAIN request/materialize the exact 0014 runtime and private profile, complete
the prerequisite census, and make exactly one allowed `env -i` full request.
Until that happens, do not request a full or named suite, build/install/run
anything, substitute 0013 or C13/14, or claim a MAIN result. Record the
terminal result only after the exact run; this handoff is not that result.
