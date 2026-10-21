# Agent D13 current installed/actionable preflight

Status: recovered from the predecessor-0802 log and the 0735/0739/0747
preparation records. This is a handoff record, not a qualification result.
No source audit, build, install, download, native, HTTP, private execution, or
full suite was rerun for this recovery.

## One next step

After the three blockers below are resolved, the manager should create one
fresh, manager-approved private destination from the leased staging base and
run the existing wheel/RECORD chain in **Minimum refresh command** exactly once,
bound to Agent commit `6951c176f326e99f0e4d61c89233d1de49a9c05b` and tree
`386fa1f8afe073edd08f31bd8c430ee9b86e1ab9`. The existing chain does not create
or approve the private destination. It must not mutate the leased stage or any
shared environment.

The eventual named full entry is recorded only as a post-refresh command:
`agent full-c13-a8a40afd-integration`. It must snapshot the manager-pinned
source and use the refreshed private installed pair; no result or collection
count is claimed here.

## Evidence identity and source review

- Candidate source: commit `6951c176f326e99f0e4d61c89233d1de49a9c05b`, tree
  `386fa1f8afe073edd08f31bd8c430ee9b86e1ab9`.
- Candidate parent/current integration: commit
  `7c9ef2ed5e70da1a13e89278496c74321453955a`, tree
  `0ce002cd6d59c3f682e1ac6c9a7b91d29035fe81`.
- Approved donor: commit `c4a50c60fb59ee58604bf111dba05a1f9b1c25b8`, tree
  `ff4969e0c9e33db94f129843ef3e19fcddac3458`.
- The contract, assembler action, pack metadata, `assembly.py`, assembly
  tests, `sync.py`, and publication-chain fixture match the donor. The
  `runtime.lock.json`, `artifacts.json`, `cli-surface.json`, timeline schema,
  and generated Runtime-client files match the `7c9ef2ed` parent. No
  schema/pin/generated contract change was found.
- The native seam is exact: `build_assembler_admission`, native capture/retry,
  `TimelineSession.admit_assembly`/`queue_assembly`, and the action native
  proposal path remain. GenericHost removes only
  `_publish_assembled_timeline`, its call, and the
  `timeline_render_publication` result field; the lower-level generated
  `publish_timeline_render` adapter remains.
- The intentional current-only hunks versus the donor are retained:
  `astrid/core/execution/generic_host.py` keeps the existing Windows
  `platform.private_directory` attempt-root path, and
  `tests/sdk/test_timeline_sync.py` keeps the `runtime_protocol.platform` /
  `Outbox` unlock-on-exception regression and unknown-flight-kind refusal.
  No current safety, Windows, or outbox assertion was weakened.

## Origin and RECORD controls that must remain

- At `tests/packs/video_editing/test_runtime_publication_chain.py:457`, the
  installed-origin correction refuses when `runtime_checkout` and
  `source_checkout` select different installed trees. The required eight
  origins are `host`, `child`, `action`, `client`, `sdk`, `runtime_protocol`,
  `runtime_protocol.platform`, and `astrid_runtime`.
- `host_bootstrap._installed_execution_origins` probes with the selected
  interpreter using isolated `-I`, neutral cwd, and no `PYTHONPATH` or
  `ASTRID_RUNTIME_CHECKOUT`. Installed startup binds `--source-checkout` to
  that interpreter's actual package root. The checkout field remains a test
  locator, not product import authority.
- The approved c4a50c60 RECORD fence is present byte-for-byte. It rejects
  absolute, empty/dot/parent, and symlink-component RECORD paths before
  opening them, then checks wheel/installed hashes, sizes, and package bytes.
  The current fixture retains the traversal, symlink-component, and normal
  `dist-info/RECORD` positive controls.

## Existing installed closure (complete, but stale for the candidate)

The leased coherent staging base is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging`

It is read-only for this task and must remain leased. The recovered profile is
Python `3.13.16`, approximately 944 MiB, with 13,580,521,472 bytes free at the
0739 check. It is a complete **old** installed pair, not the candidate:

| component | source identity | installed artifact |
| --- | --- | --- |
| Agent | `6f2d8c350ad6838d2a2cd8da98e49465b1ab2406`, tree `698ae4df6ea9e9e89746fffabfaab15ac0c7d47f` | `astrid==0.1.0`; wheel SHA-256 `fa2f824d1068f6233dc852960726d597f21a243d768ff0cafe258b7afe391346` |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d` | `astrid-runtime==0.1.0`; wheel SHA-256 `12df54644e1acac46b9c396135ef345808a98515965f1f12f479f32adf3c9b0a` |
| Runtime client/artifacts | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` | `astrid-runtime-client==0.2.14`; wheel SHA-256 `567605b13254f88ddeddad7b570553a2c50b5092908e6c4153553f9867e37254` |

The complete dependency carrier is
`metadata/venv-agent-child-s2.txt`: 164 unique lock entries, SHA-256
`478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
The 0735 record copied 163 of 164 entries byte-for-byte from the read-only
carrier; `astrid` was the held entry and was not copied from the old source.
The installed product tuple is `astrid==0.1.0`, `astrid-runtime==0.1.0`, and
`astrid-runtime-client==0.2.14`. The stage has 166 valid RECORD files / 26,283
rows, 3,268/3,268 source-archive Git-blob parity, and zero symlinks. The
old Agent source and wheel facts above must not be relabeled as candidate
`6951c176` evidence.

The exact 164-entry lock content follows (including its two VCS entries):

```text
agent-detector==2.0.0
aiodns==4.0.4
aiofiles==25.1.0
aiohappyeyeballs==2.7.1
aiohttp==3.14.5
aiohttp-retry==2.9.1
aioquic==1.7.0
aiosignal==1.4.0
annotated-doc==0.0.5
annotated-types==0.8.0
anthropic==1.0.0
anyio==4.14.2
astrid @ file:///home/user/work/wt/.orch-astrid-d8749a9c
asyncstdlib==3.14.0
attrs==26.1.0
backoff==2.2.1
backports.zstd==1.8.0
banodoco-timeline-schema @ git+https://github.com/banodoco/ArtAgents.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#subdirectory=packages/timeline-schema/python
bcrypt==5.0.0
boto3==1.43.114
botocore==1.43.114
brotli==1.2.0
build==1.4.0
certifi==2026.7.22
cffi==2.1.1
charset-normalizer==3.5.1
click==8.4.2
colorama==0.4.6
coverage==7.16.2
cryptography==50.0.0
detect-installer==0.2.1
distro==1.9.0
dnspython==2.9.0
docstring_parser==0.18.0
email-validator==2.3.0
execnet==2.1.2
fal_client==1.0.1
fastapi==0.149.0
fastapi-cli==0.0.32
fastapi-cloud-cli==0.26.0
fastar==0.12.0
filelock==3.32.4
fonttools==4.67.0
frozenlist==1.8.0
google-auth==2.56.3
google-genai==2.19.0
googleapis-common-protos==1.75.5
h11==0.16.0
httpcore==1.0.9
httpcore2==2.12.0
httptools==0.9.0
httpx==0.28.1
httpx-sse==0.4.3
httpx2==2.12.0
idna==3.19
iniconfig==2.3.1
inquirerpy==0.3.4
invoke==3.0.3
itsdangerous==2.2.0
jaraco.classes==3.4.0
jaraco.context==6.1.2
jaraco.functools==4.6.0
jeepney==0.9.0
Jinja2==3.1.6
jiter==0.16.0
jmespath==1.1.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
keyring==25.7.0
markdown-it-py==4.2.0
MarkupSafe==3.0.4
mdurl==0.1.2
more-itertools==11.1.0
msgpack==1.2.1
multidict==7.1.0
mypy==1.17.0
mypy_extensions==1.1.0
numpy==2.5.2
openai==2.54.0
opencv-python-headless==5.0.0.93
opentelemetry-api==1.45.1
opentelemetry-exporter-http-transport==0.66b1
opentelemetry-exporter-otlp-common==0.66b1
opentelemetry-exporter-otlp-proto-common==1.45.1
opentelemetry-exporter-otlp-proto-http==1.45.1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
packaging==26.3
paramiko==5.1.0
pathspec==1.1.1
pfzy==0.3.4
pillow==12.3.0
pip==26.2.1
platformdirs==4.11.3
pluggy==1.7.0
prettytable==3.18.0
prompt_toolkit==3.0.53
propcache==0.5.4
protobuf==7.36.2
psutil==7.2.2
py-cpuinfo==9.0.0
pyasn1==0.6.4
pyasn1_modules==0.4.2
pycares==5.2.0
pycparser==3.0
pydantic==2.13.4
pydantic-extra-types==2.11.1
pydantic-settings==2.16.0
pydantic_core==2.46.4
Pygments==2.21.0
PyJWT==2.13.0
pylsqpack==1.0.0
PyNaCl==1.6.2
pyOpenSSL==26.4.0
pyproject_hooks==1.2.0
pytest==9.0.2
pytest-cov==7.1.0
pytest-split==0.11.0
pytest-timeout==2.4.0
pytest-xdist==3.8.0
python-dateutil==2.9.0.post0
python-dotenv==1.2.4
python-multipart==0.0.32
PyYAML==6.0.3
referencing==0.37.0
requests==2.34.2
rich==15.0.0
rich-toolkit==0.20.6
rignore==0.8.1
rpds-py==2026.6.3
ruff==0.12.0
runpod==1.12.0
runpod-lifecycle @ git+https://github.com/banodoco/runpod-lifecycle.git@db79345536985c701b7aff2eb5eec36667aae204
s3transfer==0.19.2
scenedetect==0.6.4
SecretStorage==3.5.0
sentry-sdk==2.72.0
service-identity==26.1.0
setuptools==80.9.0
shellingham==1.5.4
six==1.17.0
sniffio==1.3.1
starlette==1.9.0
tenacity==9.1.4
tomli==2.5.0
tomlkit==0.15.2
tqdm==4.70.0
tqdm-loggable==0.4.1
truststore==0.10.4
typer==0.27.3
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.7.0
uvicorn==0.54.0
uvloop==0.23.0
watchdog==6.0.0
watchfiles==1.3.0
wcwidth==0.9.2
websockets==16.1.1
wheel==0.46.3
xxhash==4.0.1
yarl==1.25.1
zopfli==0.4.3
```

The old installed import probe passed for `astrid`,
`astrid_runtime_client`, `runtime_protocol`, `astrid_runtime`,
`banodoco_timeline_schema`, NumPy, Pillow, OpenCV, and PyYAML, all under the
private site-packages root. That is closure evidence for the old stage only.

## Preflight paths, environment, and argv

Read-only findings from 0735/0739/0747 and 0802:

- Old child environment: `/home/user/work/venv-agent-child-c13-a8a40afd`,
  Python 3.13 site-packages below that path. It contains Agent/client/schema
  but lacks both `runtime_protocol/` and `astrid_runtime/` required by the
  eight-origin probe. Its `.astrid-source-commit` is old
  `a8a40afd37e5560a14fa5e1a09ace6018596793e`, not the candidate.
- Runtime checkout: `/home/user/work/runtime`, expected b92 commit
  `b92d3e7a05eec65c142294ef4873edd059e9b31d`.
- Named-full Remotion: `/home/user/work/runtimes/agent-remotion-0013`;
  Composition `0.0.13`, Remotion `4.0.509`, package-lock SHA-256
  `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
  Do not substitute historical `agent-remotion-current`.
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, version
  `20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Media tools: `/usr/bin/ffmpeg` 6.1.1-3ubuntu5, SHA-256
  `ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41`;
  `/usr/bin/ffprobe` 6.1.1-3ubuntu5, SHA-256
  `272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f`.
- VibeComfy path: `/home/user/work/fixtures/vibecomfy`; the record reports
  prefix `31f90bb…` only. Full commit/tree is **UNKNOWN**; missing datum is the
  complete VibeComfy commit identity. Its path was real at review time.
- No standard Chromium, `chromium-browser`, `google-chrome`, or
  `chrome-headless-shell` executable was found. The named full command does
  not use a browser; native/render qualification still cannot claim one.
- Disk was above the 5 GiB guard: 13,580,521,472 bytes free on the leased
  profile filesystem at 0739; the current candidate worktree was about 115 MiB.
- The worker shell inherited `NODE_OPTIONS` and `NODE_PATH`. Any later
  Remotion-capable command must use `env -i` and therefore have no
  `NODE_OPTIONS`, `NODE_PATH`, any `LD_*`, or `PYTHONHOME`. The installed-origin
  probe also deliberately has no `PYTHONPATH`, `ASTRID_RUNTIME_CHECKOUT`, or
  `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`.
- No active Runtime daemon/socket or trusted credential was established. No
  final fonts/OMP/native/media/public-input closure was proven.

## Minimum refresh command (manager-only; do not run as this task)

This is the recovered 0735 chain with the 0802 correction that makes the
source cwd explicit and requires an already-materialized private destination.
The 0735 record additionally requires readable merged document approval,
installed-origin approval, and ancestry/blob-preservation records bound to the
same commit/tree, plus approved `NODE`, `REMOTION`, `BROWSER`, `FFMPEG`, and
`FFPROBE` paths. The named 0739 full entry itself has no browser argv.

The exact 0735 admission variables and non-mutating checks are:

```bash
: "${STAGE:?leased profile-staging path}" "${PRIVATE_ROOT:?manager-approved private destination}" "${AGENT_SOURCE:?clean Agent checkout}" "${AGENT_COMMIT:?exact manager-selected commit}" "${AGENT_TREE:?exact manager-selected tree}" "${DOCUMENT_APPROVAL:?merged document-adapter APPROVE+HTTP record}" "${ORIGIN_APPROVAL:?merged installed-origin APPROVE record}" "${ANCESTRY_RECORD:?commit/tree/blob-preservation record}" "${NODE:?approved Node executable}" "${REMOTION:?approved Remotion tree}" "${BROWSER:?approved browser executable}" "${FFMPEG:?approved ffmpeg}" "${FFPROBE:?approved ffprobe}"
test -d "$STAGE" && test ! -L "$STAGE" && test -d "$PRIVATE_ROOT/wheelhouse" && test -x "$PRIVATE_ROOT/venv/bin/pip" && test "$STAGE" != "$PRIVATE_ROOT" && test -r "$DOCUMENT_APPROVAL" && test -r "$ORIGIN_APPROVAL" && test -r "$ANCESTRY_RECORD" && test -x "$NODE" && test -d "$REMOTION" && test -x "$BROWSER" && test -x "$FFMPEG" && test -x "$FFPROBE" && test -z "${PYTHONPATH:-}${NODE_OPTIONS:-}${NODE_PATH:-}" && test "$(git -C "$AGENT_SOURCE" rev-parse HEAD)" = "$AGENT_COMMIT" && test "$(git -C "$AGENT_SOURCE" rev-parse HEAD^{tree})" = "$AGENT_TREE" && test -z "$(git -C "$AGENT_SOURCE" status --porcelain)"
```

The 0802 correction adds the already-materialized `PRIVATE_ROOT` condition;
the removed 0735 product helper did not provision it. The later pack-host and
Remotion commands must add `env -i` clearing for `PYTHONHOME` and all `LD_*`
variables as shown below; the original admission line above is preserved
exactly and only checks its three named ambient variables.

```bash
set -euo pipefail
: "${STAGE:?leased profile-staging path}" "${PRIVATE_ROOT:?approved private destination}" \
  "${AGENT_SOURCE:?clean checkout}" "${AGENT_COMMIT:?manager-pinned commit}" \
  "${AGENT_TREE:?manager-pinned tree}"
test "$AGENT_COMMIT" = 6951c176f326e99f0e4d61c89233d1de49a9c05b
test "$AGENT_TREE" = 386fa1f8afe073edd08f31bd8c430ee9b86e1ab9
test -d "$STAGE" && test ! -L "$STAGE" && test -d "$STAGE/venv/lib/python3.13/site-packages"
test "$STAGE" != "$PRIVATE_ROOT" && test -d "$PRIVATE_ROOT/wheelhouse" && test -x "$PRIVATE_ROOT/venv/bin/pip"
test "$(git -C "$AGENT_SOURCE" rev-parse HEAD)" = "$AGENT_COMMIT"
test "$(git -C "$AGENT_SOURCE" rev-parse HEAD^{tree})" = "$AGENT_TREE"
test -z "$(git -C "$AGENT_SOURCE" status --porcelain)"
test -z "${PYTHONPATH:-}${NODE_OPTIONS:-}${NODE_PATH:-}${PYTHONHOME:-}"
env -i HOME=/tmp/timeline-d13-refresh LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent-child-published14-b9797941/bin/python -m pip wheel \
  --no-index --no-build-isolation --no-deps --wheel-dir "$PRIVATE_ROOT/wheelhouse" "$AGENT_SOURCE"
cp "$STAGE/wheelhouse/astrid_runtime-0.1.0-py3-none-any.whl" \
  "$STAGE/wheelhouse/astrid_runtime_client-0.2.14-py3-none-any.whl" \
  "$PRIVATE_ROOT/wheelhouse/"
"$PRIVATE_ROOT/venv/bin/pip" install --no-index --no-deps --force-reinstall \
  "$PRIVATE_ROOT/wheelhouse/astrid-0.1.0-py3-none-any.whl"
(cd "$AGENT_SOURCE" && bash scripts/smoke_wheel_install.sh \
  --wheel "$PRIVATE_ROOT/wheelhouse/astrid-0.1.0-py3-none-any.whl" \
  --venv "$PRIVATE_ROOT/venv")
(cd "$AGENT_SOURCE" && "$PRIVATE_ROOT/venv/bin/python" -m scripts.reshape.authority_lint \
  --installed-root "$PRIVATE_ROOT/venv/lib/python3.13/site-packages" --json)
```

The existing product entrypoints are `scripts/smoke_wheel_install.sh` and
`scripts.reshape.authority_lint`; no provisioning or authority helper is
introduced. The command assumes `PRIVATE_ROOT` already exists with its
wheelhouse and venv, is distinct from `STAGE`, has no symlink parent, and does
not overlap a shared dependency root. The 0735 approval variables are
requirements, not evidence that approvals currently exist.

## Post-refresh named-full argv record (not run)

The 0747 correction says to use the existing named entry only after pinning
`SOURCE_COMMIT` and `SOURCE_TREE`; the central service snapshots that exact
source and `$PWD` is its snapshot root. The source identity must not be
derived by the command.

```bash
set -euo pipefail
: "${SOURCE_COMMIT:?manager-pinned before enqueue}" "${SOURCE_TREE:?manager-pinned before enqueue}"
SOURCE_ROOT="$PWD"
PY=/home/user/work/venv-agent-child-c13-a8a40afd/bin/python
SITE=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages
RUNTIME=/home/user/work/runtime
REMOTION=/home/user/work/runtimes/agent-remotion-0013
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
test "$(git -C "$SOURCE_ROOT" rev-parse --show-toplevel)" = "$SOURCE_ROOT"
test "$(git -C "$SOURCE_ROOT" rev-parse HEAD)" = "$SOURCE_COMMIT"
test "$(git -C "$SOURCE_ROOT" rev-parse HEAD^{tree})" = "$SOURCE_TREE"
test -z "$(git -C "$SOURCE_ROOT" status --porcelain)"
test -x "$PY" && test -d "$SITE" && test -d "$REMOTION/node_modules" && test -x "$NODE"
test -x /usr/bin/ffmpeg && test -x /usr/bin/ffprobe
test "$(git -C "$RUNTIME" rev-parse HEAD)" = b92d3e7a05eec65c142294ef4873edd059e9b31d
test "$(sed -n 's/.*\"source_commit\": \"\([^\"]*\)\".*/\1/p' "$SOURCE_ROOT/runtime.lock.json")" = 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
(cd /tmp && env -i HOME=/tmp/timeline-m4-full-home LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 "$PY" -I -B -c 'import importlib.util; site="/site-packages/"; names=("astrid","astrid_runtime_client","banodoco_timeline_schema","numpy","PIL","cv2","yaml"); assert all((s:=importlib.util.find_spec(n)) and site in str(s.origin) for n in names), [(n, importlib.util.find_spec(n)) for n in names]')
run_pytest() { (cd "$SOURCE_ROOT" && env -i HOME=/tmp/timeline-m4-full-home LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH="$(dirname "$NODE"):/usr/bin:/bin" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME" ASTRID_REMOTION_PROJECT_DIR="$REMOTION" ASTRID_NODE_EXECUTABLE="$NODE" \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SITE" ASTRID_TEST_NODE_MODULES="$REMOTION/node_modules" \
  ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 "$PY" -B -m pytest -o addopts= -p no:cacheprovider "$SOURCE_ROOT/tests" "$@" ); }
COLLECTED="$(run_pytest --collect-only -q)"
COUNT="$(printf '%s\n' "$COLLECTED" | sed -nE 's/^([0-9]+) tests collected.*/\1/p' | tail -1)"
test "${COUNT:-0}" -gt 0
run_pytest -q -n 3
```

This command has an explicit `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`
test locator for the existing suite; it is not installed import authority.
The neutral `cd /tmp` probe is separated from collection/execution at the real
snapshot root and passes the absolute snapshot `tests` path. The command
requires a non-zero collection count, but the 0739 collection probe produced
no result within its 30-second window. The current collection count is
**UNKNOWN**; missing datum is a completed collection output for the refreshed
candidate profile.

## Actual three blockers recovered from predecessor-0802

1. The final Agent wheel and private installed profile are not materialized
   for `6951c176/tree386fa`. The available C13 child is tied to `a8a40afd` and
   lacks the installed `runtime_protocol` and `astrid_runtime` origins.
2. The source approval/HTTP record for the current document repair remains
   open: the 0745 review found an unsatisfiable source-pin assertion and asks
   for one corrected authenticated node. The 0739 report explicitly says its
   HTTP node was collected, not executed.
3. The named full command has no observed collection count. Do not enqueue it
   until source/tree, wheel/RECORD, eight origins, Runtime b92/client 95bd,
   schema, tools, private cwd/argv, and cleared environment all pass together.

## Prior evidence and non-evidence

The 0736 source report, as recovered by the 0802 log, recorded:

- `tests/sdk/test_timeline_assembly.py` plus
  `tests/sdk/test_timeline_sync.py`: 73 passed;
- D13 offline binding/RECORD controls: 9 passed, 4 deselected;
- assembler plus legacy-refusal controls: 10 passed;
- legacy publisher regression: 1 strict expected failure.

Those results are historical evidence from the predecessor and were not rerun.
The 0735/0739/0747 syntax and read-only path checks passed, but no current
candidate wheel, installed profile, collection count, HTTP proof, native run,
or full-suite result is claimed.

## Source records recovered

- Predecessor full log/report:
  `scratchpad/orch/workers/agt-m2-d13-current-source-installed-preflight-0802/`.
- Profile preparation and refresh record:
  `scratchpad/orch/workers/agt-m4-coherent-profile-preparation-record-only-0735/`.
- Current full prerequisite and command:
  `scratchpad/orch/workers/agt-m4-current-public-full-prerequisite-selection-0739/`.
- Snapshot-cwd correction:
  `scratchpad/orch/workers/agt-m4-final-full-command-cwd-snapshot-correction-0747/`.
