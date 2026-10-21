# App automatic1490 main-only materialization (1135)

Status: PREPARED, not executed. This handoff prepares automatic1490 only;
Trim/split remain local and their split-only credential, READY, LEASE, and
current013-driver requirements do not apply here. It does not authorize an
actual, browser, daemon, build, install, graph build, or new runner.

## Contract decision

The immutable App source is commit
1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf, tree
8e242d1497841f391b6152ecd8d204143fa03b52. The approved packet remains
unchanged at SHA-256
516fe8fffc2b68c58f5a4668a5944489d156fed0a66bfa884ac9937b42cd61a0.

auto-real-proxy-main95.mjs requires only App/Agent/Runtime SHA+tree values,
the Runtime producer checkout, private dependency/run roots, the two Python
executables, Chromium, and its own runner SHA. Its actual input parser does
not read READY, LEASE, PRIVATE13_NODE_MODULES,
WORKSPACE_RUNTIME_TOKEN_FILE, or an external credential path.

The App1490 automatic spec's existing DirectHarness.start() creates its own
temporary realm, starts the pinned Runtime, and invokes the existing
provisionCredential(PRODUCT_ACTOR, ...) before seeding. The harness passes
that private credential to its Vite/discovery children while it remains alive.
Main must not pre-create, copy, print, or invent a credential. Do not apply
the later r69 credential-shape hunk to App1490: that was a split-driver guard
correction, while current source1490 is authoritative for this automatic run.

The temporary GenericPackHost child in the automatic spec is existing test
behavior, not a Main pack-host override. Every list/actual process uses
env -i; ambient ASTRID_PACK* host overrides, NODE_OPTIONS, NODE_PATH,
PYTHONHOME, and LD_* are therefore absent.

## Exact tuple

| input | required identity |
|---|---|
| App | 1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf / 8e242d1497841f391b6152ecd8d204143fa03b52 |
| Agent | 6efc81500a0e0688c2bb41e736503f0fc3e04abb / 2ed2b8a12b5b3391ca221ba6ff05390f71a73556 |
| Agent vendor | 091aa23ec83ea05ffd3b0115a640230d51c8c429 / e3ae90fe482ba6cad6c3f94069127faf76ebceb6 |
| Runtime | 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / d3a290b407fa61e6ab2d476f50c068073f70df00 |
| Runtime artifacts | all 76; manifest SHA a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d; producer sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac |
| App Composition | 0.0.13, SHA 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738, all 77 safe regular members |
| Agent Composition | 0.0.12, SHA 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3, all 77 safe regular members |
| runner | SHA 7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f |
| Chromium | /opt/pw-browsers/chromium-1194/chrome-linux/chrome, 141.0.7390.37, SHA 85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95 |
| Node | /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node, v20.19.4, SHA 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490 |

App/Agent/Runtime keepers and all non-Node byte checks passed read-only in this
preparation. The exact Node path is absent in this worker sandbox, so the
case is not ready here. The retained exact-byte handoff is
ORCH/design/handoff-vw-m3-node20.19.4-retained-app.tgz (archive SHA
e481653ec961f88c9cb8f034740afca3ed1bbc5fa3f9d56efde0eb502372481f). Main
must restore the approved path/hash or obtain an explicit decision to extract
the same bytes privately and change only the path variable; no substitute
Node20/22 is acceptable.

## Automatic-only Main preparation

If the exact App keeper is absent, use the checkout service, never git fetch:

~~~bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
KEEPER=/home/user/work/wt/app-pin-1490fbfe
APP_SHA=1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf
test -d "$KEEPER" || { "$ORCH/bin/request-checkout" app "$APP_SHA" 'exact App1490 keeper for automatic main-only prep'; exit 2; }

MAIN=/home/user/work/tl-app-main-private-auto1135
SHORT_TMP=/tmp/tl-app-main-private-auto1135
APP="$MAIN/cases/auto1490/source"
GRAPH="$MAIN/cases/auto1490/graph"
PRIVATE="$MAIN/cases/auto1490/private"
EVIDENCE="$MAIN/cases/auto1490/evidence"
HOME_ROOT="$MAIN/cases/auto1490/home"
RUN="$MAIN/cases/auto1490/run"
CACHE="$MAIN/cases/auto1490/cache"
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
AGENT=/home/user/work/wt/agt-pin-6efc8150
RUNTIME=/home/user/work/wt/rt-pin-95bd3c5f
ARCHIVE="$ORCH/artifacts/app-public13-main-node-modules-r25.tgz"
test ! -e "$MAIN" && test ! -e "$SHORT_TMP"
test "$(sha256sum "$ORCH/design/run-on-main-app-automatic-current.md" | awk '{print $1}')" = 516fe8fffc2b68c58f5a4668a5944489d156fed0a66bfa884ac9937b42cd61a0
test -x "$NODE" && test "$(sha256sum "$NODE" | awk '{print $1}')" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
test "$($NODE --version)" = v20.19.4
sha256sum -c "$ARCHIVE.sha256"
test "$(sha256sum "$ARCHIVE" | awk '{print $1}')" = a1ef11b292548c22caa36cc38c683a67b01d9244f8389aade9405e5a7dca581e
for repo in "$KEEPER" "$AGENT" "$RUNTIME"; do test -z "$(git -C "$repo" status --porcelain --untracked-files=normal)"; done
test "$(git -C "$KEEPER" rev-parse HEAD)" = "$APP_SHA"
test "$(git -C "$KEEPER" rev-parse HEAD^{tree})" = 8e242d1497841f391b6152ecd8d204143fa03b52
git -C /home/user/work/app cat-file -e "$APP_SHA^{commit}"
git -C /home/user/work/app merge-base --is-ancestor "$APP_SHA" refs/remotes/hub/timeline/app/tl/integration

mkdir -p "$MAIN/cases/auto1490" "$MAIN/evidence" "$MAIN/home" "$MAIN/run" "$MAIN/cache" "$SHORT_TMP"
chmod 700 "$MAIN" "$MAIN/cases" "$MAIN/cases/auto1490" "$MAIN/evidence" "$MAIN/home" "$MAIN/run" "$MAIN/cache" "$SHORT_TMP"
git clone --no-local --no-hardlinks --no-checkout "$KEEPER" "$MAIN/cases/auto1490/source"
git -C "$APP" checkout --detach "$APP_SHA"
test -z "$(git -C "$APP" status --porcelain --untracked-files=normal)"
test "$(git -C "$APP" rev-parse HEAD^{tree})" = 8e242d1497841f391b6152ecd8d204143fa03b52
mkdir -p "$GRAPH" "$PRIVATE" "$EVIDENCE" "$HOME_ROOT" "$RUN" "$CACHE"
chmod 700 "$GRAPH" "$PRIVATE" "$EVIDENCE" "$HOME_ROOT" "$RUN" "$CACHE"
tar --extract --gzip --file="$ARCHIVE" --directory="$GRAPH" --no-same-owner --no-same-permissions --no-overwrite-dir --keep-old-files
test "$(find -P "$GRAPH/node_modules" -type l -print -quit)" = ''
mkdir "$GRAPH/node_modules/.vite" "$GRAPH/node_modules/.vite-temp"
ln -s "$GRAPH/node_modules" "$APP/node_modules"
test "$(realpath "$APP/node_modules")" = "$(realpath "$GRAPH/node_modules")"
~~~

The r25 audit must report 35,496 total members, 3,147 directories, 32,349
regular files, zero links, and only relative node_modules/ paths. Reject
absolute, .., .vite/.cache/.npm/.aws/.config/realm/credential paths. The
extraction is only into this own graph; never into shared node_modules.

## Pure preflight and list1

Use the approved packet's existing startup-only check and list command from
APP. Only substitute the own APP, GRAPH/node_modules, PRIVATE, HOME_ROOT,
SHORT_TMP, and evidence roots. Keep its runner/spec/config, one worker, zero
retries, retained trace, exact source pins, all76/all77 checks, and
overlay/cache/postflight guards.

The process-local env-i inputs must include:

~~~text
HOME="$HOME_ROOT" LANG=C.UTF-8
PATH="/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/bin:/bin"
ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
ASTRID_APP_DIRECT_DOOR_PORT=17340
TMPDIR="$SHORT_TMP" XDG_RUNTIME_DIR="$MAIN/run/x"
npm_config_cache="$CACHE/npm" npm_config_offline=true
PWTEST_CACHE_DIR="$CACHE/pw" VITE_CACHE_DIR="$CACHE/vite"
XDG_CACHE_HOME="$CACHE/xdg" TSX_DISABLE_CACHE=1
TIMELINE_BUNDLE_AGENT_HEAD=6efc81500a0e0688c2bb41e736503f0fc3e04abb
TIMELINE_BUNDLE_RUNTIME_HEAD=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
TIMELINE_AUTO_REAL_PROXY_APP_SHA="$APP_SHA"
TIMELINE_AUTO_REAL_PROXY_APP_TREE=8e242d1497841f391b6152ecd8d204143fa03b52
TIMELINE_AUTO_REAL_PROXY_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb
TIMELINE_AUTO_REAL_PROXY_AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556
TIMELINE_AUTO_REAL_PROXY_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
TIMELINE_AUTO_REAL_PROXY_RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00
TIMELINE_AUTO_REAL_PROXY_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME"
TIMELINE_AUTO_REAL_PROXY_DEPENDENCY_ROOT="$GRAPH/node_modules"
TIMELINE_AUTO_REAL_PROXY_PRIVATE_ROOT="$PRIVATE"
TIMELINE_AUTO_REAL_PROXY_RUNNER_SHA256=sha256:7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f
~~~

Create $MAIN/run/x, private npm/playwright/Vite/XDG caches, and evidence
directories as physical mode 0700. Assert TMPDIR, XDG runtime, the harness
credential-pattern path
$PRIVATE/real-proxy-9999999999/tmpdir/astrid-direct-XXXXXX/product-credential.json,
and $MAIN/run/x/timeline.sock are all shorter than 100 characters. Run an
env-i Node check inside the child process for absent NODE_OPTIONS, NODE_PATH,
PYTHONHOME, and LD_*; this same process-local check applies to list and
actual. Keep all ASTRID_PACK* host overrides absent. Check door 17340 is free
without binding a probe.

Guard the physical graph and peers exactly:

~~~text
@banodoco/timeline-composition 0.0.13
react                       18.3.1
react-dom                   18.3.1
remotion                    4.0.509
@remotion/player            4.0.509
@remotion/three             4.0.509
three                       0.185.1
playwright                  1.60.0
@playwright/test            1.60.0
~~~

Also assert App/Agent archive hashes and all 77 safe members, Runtime manifest
hash and 76 entries, runner hash, source HEAD/tree/clean state, and exact
APP/node_modules to graph realpath. Snapshot sorted private/shared module
digests before list1 and compare after the actual.

Run the packet's existing startup-only command and exact list:

~~~bash
cd "$APP"
env -i "${COMMON_ENV[@]}" TIMELINE_AUTO_REAL_PROXY_RUN=1 TIMELINE_AUTO_REAL_PROXY_STARTUP_ONLY=1 TIMELINE_AUTO_REAL_PROXY_RECORD_DIR="$EVIDENCE/preflight" "$NODE" scripts/testing/auto-real-proxy-main95.mjs
env -i "${COMMON_ENV[@]}" npm exec -- playwright test --config playwright.auto-real-proxy.config.ts tests/e2e/local/auto-real-proxy.spec.ts --list > "$EVIDENCE/list.txt" 2>&1
~~~

Require both exit 0, exact file/title once, and Total: 1 test in 1 file.
Any zero-test, extra test, failure, skip, or unexpected test is a refusal.

## Existing actual only

After pure preflight/list1 pass and separate Main authorization, invoke only:

~~~bash
set +e
env -i "${COMMON_ENV[@]}" TIMELINE_AUTO_REAL_PROXY_RUN=1 TIMELINE_AUTO_REAL_PROXY_RECORD_DIR="$EVIDENCE/recorded" "$NODE" scripts/testing/auto-real-proxy-main95.mjs > "$EVIDENCE/runner.log" 2>&1
STATUS=$?
set -e
~~~

Do not replace the runner with direct Playwright, a wrapper, selector, retry
loop, daemon, graph, credential setup, or browser flow. Its existing
overlay, private caches, durable record, source checks, restore, and finally
postflight remain authoritative. Run postflight even when STATUS is nonzero:
source HEAD/tree/clean state, runner/archive/manifest hashes, graph symlink-free
state and package versions, App-to-graph realpath, and unchanged shared-module
digests. Retain recorded/runner-result.json and
recorded/auto-http-failures.json. Expected success is one passed test, zero
failures and no relevant retained HTTP failures; ACP noise is diagnostic only.

## Missing prerequisites together

1. This worker lacks the required hash-43d6 Node at the approved toolchain
   path; Main must restore/check it before any startup or list.
2. Main must create the fresh physical 0700 automatic-only root, graph,
   private run/evidence, HOME, TMPDIR, XDG runtime, and caches.
3. Main must safely extract r25 only into that graph and pass all76/all77,
   symlink-free, module/peer, archive, manifest, source, and browser guards.
4. Main must preserve the approved packet checksum and exact existing runner,
   spec, and config. The historical REFUSED-PREFLIGHT remains a refusal from
   the superseded packet/authorization hold, not an actual.
5. Door 17340 must be free and every list/actual child must use env-i.
6. External READY, LEASE, split credentials, split driver, r69 source hunk,
   hand-written token, and shared-install mutation are not automatic1490
   prerequisites.

No actual, browser, daemon, build, install, new graph, or shared dependency
mutation was performed by this worker. Read-only tuple and r25 archive checks
passed; automatic main execution remains blocked only on Node restoration plus
Main's own materialization and authorized startup/list/one-actual sequence.

