# App original split current-main command custody review

Verdict: **HOLD — the source/spec/config tuple is approved, but the packet needs literal command corrections before the one actual.**

This is a command/process review only. I did not change product source, the
spec body, the config, the driver, dependencies, shared installs, or the
packet. I did not run a browser, build, install, graph creation, localhost
run, live socket, or full suite.

## Source checks that pass

- Exact App source is `435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef`, tree
  `daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273`; both `e1c0d8d52` and
  `2b85341ef` are ancestors.
- The four packet-file SHA-256 values in the table match exact435e. The
  original spec body is unchanged at SHA-256
  `48938cfeffed2f3d6180206a4e7744c00979b31a14021f61c66ff98638f1f574`.
  The fa20 credential correction is byte-identical at the four listed paths.
- The source driver pins Agent `6efc815`, Agent vendor `091aa23`, Runtime
  `95bd3c5`, Runtime producer digest `54205b…`, and Composition archive
  `9412ae…`; its credential actor/scope guard and one-title/one-file/total-1
  list guard are present.
- The hub integration ref is allowed to move. The packet correctly requires
  the selected App checkout to be exact435e and uses the hub ref only as a
  publication check. It must not require the moving hub tip itself to equal
  historical435e.

## Blocking corrections

### 1. The source-only `node -e` command is invalid

Lines 177–181 put backslash-newlines inside a single-quoted shell string.
Those backslashes are literal characters, so Node receives invalid JavaScript
before importing the existing driver. I reproduced this exact shell form:

```text
SyntaxError: Invalid or unexpected token
```

Replace the whole `-e` payload with one physical line (no trailing shell
backslashes):

```bash
  "$NODE" --input-type=module -e 'import { readCurrent013ParentSplitInputs, checkCurrent013ParentSplitSources } from "./scripts/testing/current013-parent-split.mjs"; const input = readCurrent013ParentSplitInputs(process.env, process.cwd()); console.log(JSON.stringify(checkCurrent013ParentSplitSources(input)));'
```

This continues to reuse the existing driver APIs and adds no source guard.

### 2. Private-graph handling contradicts the required main-machine path

Lines 59–61 and 199–215 say a missing private graph is an immediate
prerequisite failure and forbid making a new graph. The requested main-machine
behavior permits main to create an **own isolated copy** from already-installed
read-only dependencies, then verify it. Replace that refusal wording with:

```text
If GRAPH/node_modules is absent, main may materialize an own, physical,
symlink-free copy under GRAPH/node_modules from installed read-only
dependencies already present on the machine. No network, npm install, package
manager postinstall, extraction into shared node_modules, or unqualified pin
is permitted. Before list1, verify the exact public13 Composition archive
9412…d54738, exactly 77 safe regular archive members, the Runtime all76
manifest, and the required React/React-DOM/Remotion/Player/Three/Playwright
peer versions. If any source or byte identity cannot be verified, stop.
```

The copy must not resolve through `/home/user/work/app/node_modules` or any
other shared install. No installation was performed in this review.

### 3. The graph and App `node_modules` guards are prose, not executable

The driver only checks that `PRIVATE13_NODE_MODULES` is a directory and is not
the shared root. It does not prove that the App's effective module resolution
uses that graph, nor that graph contents/links are private. Add these pure
preflight checks before list1 (with the packet's existing variables):

```bash
test "$(realpath "$APP/node_modules")" = "$(realpath "$GRAPH/node_modules")"
test ! -L "$GRAPH/node_modules"
test -z "$(find "$GRAPH/node_modules" -type l -print -quit)"
test "$(sha256sum "$APP/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | awk '{print $1}')" = 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
test "$(tar -tzf "$APP/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | awk '!/\/$/{n++; if ($0 !~ /^package\// || $0 ~ /(^|\/)\.\.\//) bad=1} END { if (n != 77 || bad) exit 1; print n }')" = 77
```

Also make the stated peer checks executable against `$GRAPH/node_modules`:
Composition `0.0.13`, React and React-DOM `18.3.1`, Remotion and
`@remotion/player` `4.0.509`, Three `0.185.1`, and Playwright plus
`@playwright/test` `1.60.0`. The graph-root and shared-node_modules realpaths
must be recorded before and after the actual.

### 4. Direct list1 does not use the existing driver’s effective argv/env

The existing `checkList1` API runs:

```text
npm run test:e2e:three-products -- --config playwright.parent-split.config.ts --list
```

and injects `TIMELINE_BUNDLE_AGENT_HEAD` and
`TIMELINE_BUNDLE_RUNTIME_HEAD`. The packet’s direct list uses `npm exec` and
omits those bundle-head variables. Although Playwright list mode does not run
the `beforeAll` source check, this is not the same effective child context as
the existing driver. Replace lines 188–195 with the same `npm run` argv and
carry the two exact bundle heads, plus the same private module/cache/browser
environment used by the actual. Require exit 0, exactly one title, exactly one
file, and `Total: 1 test in 1 file`; any zero-test or extra-test output is a
refusal.

### 5. The actual bypasses the existing driver’s source/cache/postflight custody

The direct actual at lines 224–253 does not call `runCurrent013ParentSplit`.
Consequently it does not enforce the driver’s `TIMELINE_CURRENT013_RUN` and
cache identity, does not rerun the source checks immediately before the child,
and has no `finally` postflight to detect source drift. It also claims to carry
the preflight assignments but omits `PRIVATE13_NODE_MODULES`, READY/LEASE,
short-temp, config, Agent-vendor, Runtime-producer, App SHA/tree, and the
credential guard variables.

Use the existing driver API for the guarded actual, or, if the direct
Playwright argv is retained, add every omitted guard variable to the actual
`env -i` and add executable postflight checks preserving the child status:
exact App/Agent/vendor/Runtime HEAD+tree, clean statuses, archive/manifest
hashes and counts, App-module-to-private-graph resolution, shared-install
realpaths, and credential-file identity. Do not add a new source guard or
framework. The current prose at lines 256–260 is not an executable substitute.

### 6. Effective preflight/list environment needs parity

The source preflight intentionally omits `TIMELINE_CURRENT013_RUN`, which is
correct. For list1 and the actual, set the exact bundle heads, both Chromium
variables, `XDG_RUNTIME_DIR="$SOCKET"`, `TMPDIR="$TMP"`, and private npm,
Playwright, Vite, and XDG cache directories. The current preflight does not
set `PLAYWRIGHT_BROWSERS_PATH`, and the list does not carry the bundle heads.
`PROFILE=$MAIN/p` is checked but never passed to an existing API; it is not an
effective Chromium-profile guard and must not be reported as one. The effective
temporary roots are `TMPDIR` and `XDG_RUNTIME_DIR`; check their physical
0700 status and path lengths.

Add a read-only direct-door availability check before list1 (for example an
`ss`/`awk` check for listener `17340`). Do not bind a probe socket or start a
service during pure preflight.

## Recommended execution order after correction

1. Validate the exact App checkout, ancestry, clean statuses, five pinned
   source roles, Node/Chromium executables, credential, private graph/peer
   identities, archive/all77 and Runtime/all76 facts, cache/temp custody, and
   door availability.
2. Run the corrected existing source-only driver API with the one-line `-e`
   payload; do not set `TIMELINE_CURRENT013_RUN=1` there.
3. Run exactly one corrected existing `npm run … --list`, requiring one test in
   one file.
4. Run exactly one actual with the effective `env -i` and the existing
   config/spec/driver custody. Preserve evidence and run the executable
   postflight even on nonzero child exit.

## Checks run in this worker

```text
node --input-type=module -e 'const x = 1;\
console.log(x);'
  FAIL as expected: SyntaxError: Invalid or unexpected token

node --check scripts/testing/current013-parent-split.mjs
node --check scripts/testing/current013-parent-split.test.mjs
  PASS

node --experimental-vm-modules --test scripts/testing/current013-parent-split.test.mjs
  PASS — 1 file subtest, 0 failed, 0 skipped, exit 0
```

No browser/build/install/graph/full/live-socket test was run. Recommended next
step: apply the literal packet corrections, then let main perform the single
preflight/list/actual sequence once on its own private verified environment.
