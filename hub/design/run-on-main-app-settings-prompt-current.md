# Main95 prompt-only Settings proof packet

**Decision: APPROVE for main execution.** The final App source is committed,
the prompt case is statically bound, and this packet is now pinned to the
exact runner blob on the final r46 tree. This record contains no product PASS;
the central preflight/list and one actual remain unrun here.

## Final source identity

- Exact source ref: `timeline/app/tl/app-m2-prompt-final-current-merge-forward-r46`
  (App ref `tl/app-m2-prompt-final-current-merge-forward-r46`).
- Final App commit: `dfb96f10a3f33abcbef733ee55d9874e3aaeba01`.
- Final App tree: `47798b03f705b0f2888c6d738264cf48f9c76062`.
- Merge parents: reviewed prompt `fb23bf75e0985c77b14c38f97776ca950f1b47bc`
  and current `92c30b570cf8105dc021a64874c258e6c950b841`; both are ancestors
  of the final commit.
- The final commit is already committed. No pending harness commit is being
  represented here.

The prior callback/proof identities remain historical provenance only:
`cd927abfa09b6f8571cfeb282763855af3e44541` (callback source) and
`f18ec17cc45de18c3355e01170d3e868db17e4b7` (staged proof source). They are
not execution source pins and no old-source fallback is permitted.

## Case and source boundary

The only new case is this exact title:

`M2 real embedded settings prompt: native shot.set preserves exact raw settings, retries after restart, and undoes through Runtime`

The source path is native: `BatchSettingsForm` renders `#batchVideoPrompt`,
`BatchModeContent` calls `onBatchVideoPromptChange`, and the approved callback
captures `{ prompt }` through the occurrence-owned native `shot.set` path
before updating the local draft. The case retains the existing assertions for
raw `negativePrompt: null` and `x_settings_opaque`, exact prompt-only writes,
identical lost-ack retry body and idempotency key after restart, Runtime inverse
undo, and zero legacy composition-revision POSTs.

The existing `SettingsAutoDisable` body and all of its assertions remain
unchanged; this packet does not replay that already-approved PASS.

## Frozen roles and graph

| Role | Exact identity |
|---|---|
| Agent execution | commit `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` |
| Agent public vendor | commit `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` |
| Runtime producer/execution | commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Composition | `0.0.13`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular archive members |
| Browser | `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`, `Chromium 141.0.7390.37` |
| Node | `/opt/node20/bin/node`, required version `20.19.4` |

The approved private graph is the existing real, non-symlink directory
`/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules`
with its existing `READY` and `LEASE` records. It is read-only. The shared
`/home/user/work/app/node_modules` must not be written or replaced outside the
runner's existing temporary overlay/restore operation.

## Runner identity and resolved cause

The exact final-r46 runner blob is:

`sha256:d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42`

The stale requested `b7d0732b02a533a091c76bb7a163376900725db1b5ac067979a638134800ed88`
originated in the approved r44 donor commit
`140431bd3a46a0c25b569013fe21aaff30c83050` and was copied forward into the
r47 packet without being recomputed after the final composition. It is
historical donor provenance, not the final execution-source identity.

The exact blob comparison is:

- approved callback `cd927abfa09b6f8571cfeb282763855af3e44541`:
  `sha256:c148574748970ccbbbacac5514b419a66731115b8736e89adf7ad45bfb827b9d`
- r44 proof donor `140431bd3a46a0c25b569013fe21aaff30c83050`:
  `sha256:b7d0732b02a533a091c76bb7a163376900725db1b5ac067979a638134800ed88`
- composed `fb23bf75e0985c77b14c38f97776ca950f1b47bc`:
  `sha256:d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42`
- final `dfb96f10a3f33abcbef733ee55d9874e3aaeba01`:
  `sha256:d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42`

Callback-to-donor changed line 6’s comment, line 62’s `SETTINGS_CASE` from
the old scalar SettingsAutoDisable title to the distinct prompt title, and
lines 417–420’s discovery labels. Donor-to-composed and composed-to-final
left the prompt selector and all guards intact; only the line 6 and 417–420
diagnostic labels were restored to their SettingsAutoDisable wording.
The donor-to-final source diff is limited to harmless comment/diagnostic
labels: line 6 changes the comment from “distinct native settings-prompt” to
“existing SettingsAutoDisable”, and lines 417–420 change discovery error and
log labels from `settings-prompt` to `SettingsAutoDisable`. The actual
selector at line 62 remains the exact distinct prompt title, and the spawn
argv, discovery cardinality guard, source/credential/environment pins, and
all other process guards are byte-identical. These labels do not alter which
test `--grep SETTINGS_CASE` selects; no process, credential, or source-guard
drift exists. The final source is therefore preserved unchanged and the
packet binds to
`d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42`, rather
than accepting the stale donor hash.

## Central command contract (not run here)

The existing runner remains the only framework. It must be invoked twice by
the central service: first with `TIMELINE_MAIN95_PROMPT_SKIP_BROWSER=1` to run
preflight, resolver checks, and exactly-one-case discovery; then once without
that variable for the single actual browser case. The same Chrome executable,
browser path, credential file, source tuple, nested tuple, private graph,
`READY`/`LEASE`, and output/cache roots are required in both phases.

The outer shell must preserve the existing product credential file through
`WORKSPACE_RUNTIME_TOKEN_FILE="${WORKSPACE_RUNTIME_TOKEN_FILE:?}"`; it must
not print the token contents. It must verify the exact App HEAD/tree above,
clean App/Agent/vendor/Runtime checkouts, Runtime lock and metadata, vendor
provenance, Composition archive/all-77 graph, browser hash/version, runner
hash, exact case discovery, request body/key assertions, and runner source
pre/postflight equality before allowing the Node process to start.

Use short physical mode-0700 paths so every socket-bearing path is under 100
characters:

```sh
ROOT=/tmp/tl-m95-prompt-r47
TMPDIR=$ROOT/tmp
XDG_RUNTIME_DIR=$ROOT/runtime
PLAYWRIGHT_PROFILE_DIR=$ROOT/profile
PWTEST_CACHE_DIR=$ROOT/pw-cache
XDG_CACHE_HOME=$ROOT/xdg-cache
VITE_CACHE_DIR=$ROOT/vite-cache
PLAYWRIGHT_OUTPUT_DIR=$ROOT/output
HOME=$ROOT/home
```

The wrapper must `install -d -m 0700` each path, reject symlinks, assert
`realpath "$TMPDIR" = "$TMPDIR"` and the equivalent runtime/profile checks,
and reject every `XDG_*`/cache/profile/socket path whose length is 100 or
more. The outer shell/global environment is not modified; only the launched
pack-host environment is constructed with `env -i`. That environment must
contain the explicit approved variables below and must not contain
`NODE_OPTIONS`, `NODE_PATH`, `LD_*`, or `PYTHONHOME`.

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock bash -c '
  set -Eeuo pipefail
  APP=/home/user/work/app
  ROOT=/tmp/tl-m95-prompt-r47
  install -d -m 0700 "$ROOT" "$ROOT/tmp" "$ROOT/runtime" "$ROOT/profile" \
    "$ROOT/pw-cache" "$ROOT/xdg-cache" "$ROOT/vite-cache" "$ROOT/output" "$ROOT/home"
  test "$(git -C "$APP" rev-parse HEAD)" = dfb96f10a3f33abcbef733ee55d9874e3aaeba01
  test "$(git -C "$APP" rev-parse HEAD^{tree})" = 47798b03f705b0f2888c6d738264cf48f9c76062
  test -z "$(git -C "$APP" status --porcelain --untracked-files=normal)"
  test "$(realpath "$ROOT/tmp")" = "$ROOT/tmp"
  test "$(realpath "$ROOT/runtime")" = "$ROOT/runtime"
  test "$(realpath "$ROOT/profile")" = "$ROOT/profile"
  for p in "$ROOT/tmp" "$ROOT/runtime" "$ROOT/profile" "$ROOT/pw-cache" "$ROOT/xdg-cache" "$ROOT/vite-cache" "$ROOT/output" "$ROOT/home"; do
    test ! -L "$p"
    test "$(stat -c %a "$p")" = 700
    test "${#p}" -lt 100
  done
  : "${WORKSPACE_RUNTIME_TOKEN_FILE:?existing product credential file is required}"
  exec env -i \
    PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin \
    HOME="$ROOT/home" TMPDIR="$ROOT/tmp" XDG_RUNTIME_DIR="$ROOT/runtime" \
    PLAYWRIGHT_PROFILE_DIR="$ROOT/profile" PWTEST_CACHE_DIR="$ROOT/pw-cache" \
    XDG_CACHE_HOME="$ROOT/xdg-cache" VITE_CACHE_DIR="$ROOT/vite-cache" \
    PLAYWRIGHT_OUTPUT_DIR="$ROOT/output" \
    WORKSPACE_RUNTIME_TOKEN_FILE="$WORKSPACE_RUNTIME_TOKEN_FILE" \
    TIMELINE_MAIN95_PROMPT_RUN=1 \
    TIMELINE_MAIN95_PROMPT_SKIP_BROWSER=1 \
    TIMELINE_MAIN95_PROMPT_APP_TREE=47798b03f705b0f2888c6d738264cf48f9c76062 \
    TIMELINE_MAIN95_PROMPT_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
    TIMELINE_MAIN95_PROMPT_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
    TIMELINE_MAIN95_PROMPT_RUNNER_SHA256=sha256:d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42 \
    ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6efc8150 \
    TIMELINE_MAIN95_PROMPT_VENDOR_CHECKOUT=/home/user/work/wt/agt-pin-091aa23e \
    ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
    TIMELINE_MAIN95_PROMPT_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
    ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
    ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
    PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
    TIMELINE_MAIN95_PROMPT_PRIVATE13_NODE_MODULES=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules \
    TIMELINE_MAIN95_PROMPT_PRIVATE13_READY=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/READY \
    TIMELINE_MAIN95_PROMPT_PRIVATE13_LEASE=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/LEASE \
    TIMELINE_CURRENT013_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
    TIMELINE_CURRENT013_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
    TIMELINE_CURRENT013_PUBLIC_SOURCE_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 \
    /opt/node20/bin/node "$APP/scripts/testing/main95-prompt-settings-integration.mjs"
'
```

For the one actual phase, repeat the exact command once with only
`TIMELINE_MAIN95_PROMPT_SKIP_BROWSER=1` removed. Do not add `npm`, a new
framework, a new graph, a shared dependency path, a source fallback, or a
second browser case. The exact child argv from the existing runner is:

```text
/opt/node20/bin/node --test config/vite/timelineCompositionPackage.test.mjs
/opt/node20/bin/node /home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules/.bin/playwright test --config playwright.shot-name.config.ts --grep "M2 real embedded settings prompt: native shot.set preserves exact raw settings, retries after restart, and undoes through Runtime" --list
/opt/node20/bin/node /home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules/.bin/playwright test --config playwright.shot-name.config.ts --grep "M2 real embedded settings prompt: native shot.set preserves exact raw settings, retries after restart, and undoes through Runtime"
```

There is no spawned `npm` argv in this runner; the exact spawned argv is the
Node/Playwright list above. The list phase must report `Total: 1 test in 1
file` and exactly one `shot-name-command.spec.ts` location before the one
actual phase is eligible.

## Evidence and limits

- `git rev-parse` final r46 commit/tree — PASS: `dfb96f10a3f33abcbef733ee55d9874e3aaeba01` / `47798b03f705b0f2888c6d738264cf48f9c76062`.
- Both required parent ancestry checks — PASS for `fb23bf75e0985c77b14c38f97776ca950f1b47bc` and `92c30b570cf8105dc021a64874c258e6c950b841`.
- `git diff --check` — PASS.
- `node --check scripts/testing/main95-prompt-settings-integration.mjs` — PASS.
- `node --test scripts/testing/main95-prompt-settings-integration.test.mjs` — PASS, 1 file / 1 test.
- Exact prompt title/source scan — PASS; `SETTINGS_CASE` and the new test title are identical, and the source guard still requires one test in one file.
- Exact runner blob comparison — PASS: composed `fb23bf75e0985c77b14c38f97776ca950f1b47bc` and final r46 `dfb96f10a3f33abcbef733ee55d9874e3aaeba01` both contain `d52ae2c084130bef6e2733da03088a7cfb8e516908e547645125e6d973cb2d42`; stale `b7d0732b02a533a091c76bb7a163376900725db1b5ac067979a638134800ed88` is only the r44 donor blob.
- Prior r44 private-overlay Playwright `--list` evidence — PASS: exactly one prompt test and zero final failures; this worker did not rerun discovery.

No browser, Runtime door, actual prompt journey, current `--list` discovery
against the graph, build, install, dependency graph construction,
localhost/live socket, full suite, or actual execution was run by this worker.
Until the central list phase passes, the prompt journey, retry/restart, raw
readback, inverse, and zero-legacy behavior remain unverified.
