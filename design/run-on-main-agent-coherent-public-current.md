# MAIN run handoff: coherent public current Agent full

**Status: HOLD — do not request or run the full lane yet.**

This is a manager handoff for one later MAIN run. It does not build, install,
launch, or run pytest. The local machine is below the 13 GiB admission floor;
no local profile build or full request was made.

The intended run is exactly one current merged Agent tree (`fbba7c5a2`), paired
with public Runtime-client 95, Runtime b92, public Composition 0.0.13/C13,
the settled 164-entry carrier, and the resulting private installed closure of
166 distributions and 166 `RECORD` files. The final pytest invocation remains
the wrapper's ordinary `-q -n 3` invocation, with collection and child/process
exit statuses propagated.

## HOLD gates

The reviewed wrapper is not approved for MAIN:

- The 1008 independent review is **REQUEST CHANGES; do not request the full
  lane**: `design/agent-review-current-full-wrapper-repaired-final-1008.md`.
- The exact reviewed wrapper is branch
  `tl/agt-review-current-full-wrapper-repaired-final-1008`, commit
  `475fb69df31fc5af059669343f1fae4545e8e723`, blob
  `233e115294b9db7b72792f9c2528fb2c99de5dcd`, SHA-256
  `de8b93c85d27e658902635017430cecaebc424efb8a7d3bd8d2be52cdce2c669`.
- Its source/wheel guard compares wheel keys such as
  `astrid_runtime_client/__init__.py` with unnormalised archive keys such as
  `packages/python/astrid_runtime_client/__init__.py`, so a correct public95
  client wheel is refused at lines 286–319.
- No live ORCH suite registration or input lease exists. The related lease is
  explicitly retired; the prose in the 0948 report is not a live caller.
- The reviewed wrapper also asserts Agent `c4b964f6...` / tree
  `d7796be2...`, while this request is for merged Agent `fbba7c5a2` / tree
  `f5ca8f0d...`. Even after the namespace repair, a wrapper approved only for
  c4b cannot claim or run the fbba source. The wrapper successor must carry
  the exact fbba identity and receive its own review.

MAIN may proceed only after one approved wrapper successor has all of the
following: normalized client archive names, exact fbba source constants,
retained 164/166 checks and private-origin checks, retained direct `-q -n 3`
exec, and a real named registration plus lease covering every input below.

## Source tuple to materialize

The Agent source for this request is the worker's exact base, not the stale
`tl/integration` checkout at c4b/e211:

| input | exact identity | MAIN source location (must be created as a durable clean checkout) |
| --- | --- | --- |
| Agent source | branch `hub/tl/agt-m4-main-full-exact-portable-run-handoff-1010` after harness publication; commit `fbba7c5a2a4a656af32c33b1fbe56435b509cfa5`; tree `f5ca8f0d5779d57d0cc6a0cd953bc32e2e5d3064` | `/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/agent-fbba7c5a2` |
| Runtime source | commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`; tree `6abc2f117391de8e7e35c0283f575a002199894d` | `/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/runtime-b92d3e7a` |
| public Runtime-client producer | commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; tree `d3a290b407fa61e6ab2d476f50c068073f70df00`; package `astrid_runtime_client==0.2.14` | `/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/client-95bd3c5f` (full clean Git checkout; build from its `packages/python` subdirectory) |
| C13 Composition | source marker `30da0a5e05d4529a2b97b3c1818cf9e15842d628`; `banodoco-timeline-composition-0.0.13.tgz` SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; 77 regular members; lock SHA-256 `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24` | `/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/composition-c13-30da0a5e` |
| Runtime artifact | `astrid-runtime==0.1.0`; artifact/all76 digest `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` | built into the private profile below from b92; do not substitute private017/0.2.17 |

The Agent checkout must retain `runtime.lock.json` with client
`source_commit` exactly `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`. All three
Git checkouts must be clean. Do not use `/home/user/work/agent` by ambient
default, a recycled worker checkout, the f4ed D13 profile, or an old child
profile relabelled as fbba.

## Durable MAIN layout and profile inputs

These are concrete MAIN-owned destinations, not claims that the paths or
profile already exist:

```text
MAIN_ROOT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2
SOURCE_ROOT=$MAIN_ROOT/source/agent-fbba7c5a2
RUNTIME_CHECKOUT=$MAIN_ROOT/source/runtime-b92d3e7a
CLIENT_CHECKOUT=$MAIN_ROOT/source/client-95bd3c5f
COMPOSITION_ROOT=$MAIN_ROOT/composition-c13-30da0a5e
PROFILE_ROOT=$MAIN_ROOT/profile/agent-coherent-public-current-fbba7c5a2
RUNNER_ROOT=$MAIN_ROOT/runner/approved-current-wrapper
```

The fresh profile must contain, with no symlinks or checkout imports:

```text
$PROFILE_ROOT/venv/bin/python
$PROFILE_ROOT/venv/lib/python3.13/site-packages/
$PROFILE_ROOT/profile/astrid.json
$PROFILE_ROOT/metadata/venv-agent-child-s2.txt
$PROFILE_ROOT/wheelhouse/astrid-0.1.0-py3-none-any.whl
$PROFILE_ROOT/wheelhouse/astrid_runtime-0.1.0-py3-none-any.whl
$PROFILE_ROOT/wheelhouse/astrid_runtime_client-0.2.14-py3-none-any.whl
```

`venv-agent-child-s2.txt` is the copied settled carrier, not an instruction
to reuse the shared or historical `venv-agent-child-s2` installation. Its
contents must remain exactly 164 unique entries with SHA-256
`478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.

The profile must prove all of the following before pytest is admitted:

- exactly 166 installed distributions and exactly 166 `RECORD` files;
- every installed file is covered by the RECORD closure, with regular,
  symlink-free paths below the private site-packages root;
- the 164 carrier plus exactly the two Runtime/client product distributions,
  with product versions `astrid==0.1.0`, `astrid-runtime==0.1.0`, and
  `astrid-runtime-client==0.2.14`;
- product wheel bytes equal installed bytes and exact source bytes from the
  fbba, b92, and public95 source identities; the Agent wheel carries the same
  public95 client payload as the public client wheel;
- `astrid`, `astrid_runtime`, `runtime_protocol`,
  `astrid_runtime_client`, and `banodoco_timeline_schema` resolve inside this
  private site only; source `astrid` during pytest is supplied by `SOURCE_ROOT`
  and the installed Runtime/client/schema packages by the private site;
- `profile/astrid.json` is exactly the existing four-field SourceProfile
  shape, with both `runtime_checkout` and `source_checkout` equal to the
  private site-packages path and `runtime_environment` equal to
  `$PROFILE_ROOT/venv`.

## Construction prerequisites (MAIN only, after HOLD clears)

Do these together in a private MAIN-owned root; do not write shared venvs,
shared node_modules, or recycled worker paths. First require more than 13 GiB
free under `/home/user/work`.

1. Materialize the four exact source inputs above. The Agent, Runtime, and
   public95 client locations must be full clean Git checkouts so the wrapper's
   `git_identity` and exact-source archive guards can inspect their commits and
   trees; build the client wheel from its `packages/python` subdirectory.
   Copy/archive the C13 source/artifact into its durable MAIN path and verify
   commit, tree, clean status, and the Agent runtime-lock client commit before
   any wheel is built.
2. Build the three product wheels from private source copies, without network
   or build isolation:

   ```bash
   python3.13 -m pip wheel \
     --no-index --no-build-isolation --no-deps \
     --wheel-dir /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/wheelhouse \
     /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/runtime-b92d3e7a \
     /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/client-95bd3c5f/packages/python \
     /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/agent-fbba7c5a2
   ```

   The output must be exactly the three product wheels named above. Record
   their SHA-256 and source identities. This command is not executed by this
   worker.
3. Build a new Python 3.13 venv at `$PROFILE_ROOT/venv`, and materialize the
   exact 164-pin closure from the read-only approved wheel/byte inventory.
   The inventory path and its private materialization command are a MAIN
   prerequisite not present in this worker handoff; MAIN must name them in
   the result. It is not valid to point the profile at the existing D13
   `private-profile-f4edcb4b` or to rename an existing child environment.
4. After the complete 164-pin closure is private and verified, install only
   the three locally built product wheels into that venv:

   ```bash
   /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/venv/bin/pip install \
     --no-index --no-deps --force-reinstall \
     /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/wheelhouse/astrid-runtime-0.1.0-py3-none-any.whl \
     /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/wheelhouse/astrid-0.1.0-py3-none-any.whl \
     /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/wheelhouse/astrid_runtime_client-0.2.14-py3-none-any.whl
   ```
5. Prepare C13 under `$COMPOSITION_ROOT` with `.source-commit` equal to
   `30da0a5e05d4529a2b97b3c1818cf9e15842d628`, the exact 0.0.13 tarball hash
   above, a private symlink-free `node_modules`, and Node `v20.19.4`. The
   approved lock is the exact `c4d7030b...` SHA above. Do not mutate the
   shared `/home/user/work/app/node_modules`.

## Exact MAIN environment command (after approval and construction)

The approved successor wrapper must be placed in the durable runner root by
MAIN and its blob/sha256 recorded in the result. Do not copy it from a
recycled worker path. The command below is the one intended invocation; it
must not be run while this document is HOLD or with the rejected 475fb
wrapper:

```bash
env -i \
  HOME=/root \
  LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  SOURCE_ROOT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/agent-fbba7c5a2 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/runtime-b92d3e7a \
  RUNTIME_CLIENT_CHECKOUT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/source/client-95bd3c5f \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/composition-c13-30da0a5e \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy \
  FULL_COHERENT_PUBLIC_PROFILE_ROOT=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2 \
  FULL_COHERENT_PUBLIC_AGENT_WHEEL=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/wheelhouse/astrid-0.1.0-py3-none-any.whl \
  FULL_COHERENT_PUBLIC_PINS=/home/user/work/main-timeline/coherent-public-current-fbba7c5a2/profile/agent-coherent-public-current-fbba7c5a2/metadata/venv-agent-child-s2.txt \
  bash /home/user/work/main-timeline/coherent-public-current-fbba7c5a2/runner/approved-current-wrapper/full_coherent_public_current_integration.sh
```

The wrapper's final line must remain exactly:

```text
exec "$PROFILE_PY" -m pytest -q -n 3 "$@"
```

No marker, cache-provider override, `--basetemp`, cleanup wrapper, launcher,
socket, browser, renderer, or body substitution is permitted. The wrapper's
positive collection and child/process exit checks must be retained and rerun
as compact guard checks before this one full request.

## MAIN result contract

MAIN owns the execution and must write
`design/run-on-main-result-coherent-public-current.md`. That result must name:

- the actual durable runner branch/commit/blob and wrapper SHA-256;
- the actual fbba source checkout commit/tree and the exact b92/95/C13
  identities above;
- profile root, venv, pin carrier, all wheel paths and wheel hashes;
- the 166-distribution/RECORD closure, eight private origins, source/wheel/
  installed-byte parity, C13/node checks, and free-space admission;
- the exact `env -i` command used and the terminal full-suite result,
  including collection, child, signal, and nonzero-exit behavior;
- any missing prerequisite or refusal. A profile preflight or setup refusal
  is not a full result, and an old c4b/D13/s2 run must not be relabelled as
  this fbba run.

