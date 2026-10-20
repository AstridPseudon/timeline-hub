# App render/download gate readiness

This note records the one manager-owned browser gate for the ordinary App
Render action and its native download. It is a readiness contract, not a test
result. The gate must run once, centrally, after the safety batch and before
merge.

## Scope

Run only the existing test named:

`normal App Render action downloads a valid native-size MP4 without a parity comparison`

Its source is the manager-owned viewing observer branch:

- `playwright.viewing-parity.config.ts`
- `tests/e2e/timeline/player-export-frame-parity.spec.ts`
- `tests/e2e/timeline/viewing-parity/bootstrap.ts`

Do not select the Player, frame-comparison, audio-comparison, or planted
mismatch tests for this gate. This worker does not import the observer or
controller scaffold.

## Central command

Run from the App worktree, with the central test service's single browser slot
and an explicit source tuple:

```sh
flock -w 600 /tmp/timeline-viewing-browser.lock env \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/browser-artifacts/${PWD##*/} \
  ASTRID_CHECKOUT=/home/user/work/agent \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/agent/remotion \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  npm exec -- playwright test \
    --config playwright.viewing-parity.config.ts \
    --grep 'normal App Render action downloads a valid native-size MP4 without a parity comparison' \
    --workers=1
```

The command must use the normal owned source path
`$ASTRID_CHECKOUT/tests/packs/rendering/real_pack_host.py`. The bootstrap must
start that helper with the absolute `ASTRID_PYTHON`, pass the Runtime realm and
support paths, and wait for the real `rendering.render` capability to be ready.
No alternate fixture host, synthetic output, existing server, or compatibility
dependency tree qualifies this gate.

## Source and dependency guards

Before the browser starts, `sourceVersions()` must verify the frozen tuple and
the helper must verify it again afterward. The historical-compatible SAFETY
route was allowed at 05:15, but it is historical evidence only. The current
release remains pending the approved Runtime/Agent pins; a run must not be
reported as current-release-qualified until those pins are frozen.

The retained 0.0.8 guard is exact:

- App and Agent consume the public `@banodoco/timeline-composition` 0.0.8
  artifact with SHA-256
  `sha256:93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa`.
- The artifact contains exactly 77 regular package files, with no duplicate or
  unexpected member.
- Peers are React 18.3.1, React DOM 18.3.1, Remotion 4.0.509,
  `@remotion/player` 4.0.509, and Composition 0.0.8.
- App's declared render graph is sourced from App `2bfde69e`, package-lock
  SHA-256 `5b45cde0fb848455cecbd0480de827f1abb82052367f0add680e364347ce90ce`,
  with audio patch `ea4f3a9eb`.
- Agent's declared render graph is sourced from Agent `fc324e8`,
  `remotion/package-lock` SHA-256
  `35cea68df7ee4cc009438e7a079e6b871e4721f1856e14352ba38e48e74224df`, and
  upstream Remotion 4.0.509.
- The App and Agent graph manifests remain exact, and the installed browser is
  `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.

For source-only safety lanes, the only allowed dependency indirection is the
ignored symlink below. Verify the physical target before running tests:

```sh
readlink -f node_modules
# /tmp/app-m2-coherent-deps8/node_modules
```

The seven product/test files in this worker remain byte-equal to both reviewed
source guards `320784f82` and `f08c3b976`. No package, lockfile, theme, pin,
endpoint, authority, or observer/controller source is part of this unit.

## What the normal test proves

The real pack host produces one admitted managed MP4 through the ordinary App
Render action. The test checks task authority and provenance, one same-project
location read followed by one full object read, HTTP 200/no Range/no redirect,
exact object size and digest, native MP4 metadata, and a same-page blob
download. It intentionally does not claim Player/frame/audio parity or source
policy qualification.
