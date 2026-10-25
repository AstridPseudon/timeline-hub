# Pinokio installer interface

Pinokio owns the foreground process. The installer owns the backend program
directory, versions, tool downloads, workspace provisioning, updates, backups,
skill sync and uninstall. The launcher owns the editor checkout/build/server.
These commands require a release manifest containing the agent and Runtime
changes; landing the changes and updating release pins are separate operations.

## Ownership and lifecycle

`python -m astrid install --managed-by pinokio --root ABSOLUTE_PATH` installs
without a LaunchAgent, systemd user unit or Scheduled Task. `pinokio` is the
only accepted manager. `--data-root ABSOLUTE_PATH` is optional; the default is
the normal per-user Runtime workspace outside the backend directory. Program
and workspace directories must be separate. Windows program paths retain the
existing limit of 90 characters.

`install.json` records `managed_by: "pinokio"`. Update and uninstall with the
same explicit `--root` retain the manager, even when the option is omitted.
The existing per-user `astrid-install.json` selection records the manager,
program root and data root under the existing installer lock. It is next to
the default program root: `~/.local/share/astrid-install.json` on macOS,
`${XDG_DATA_HOME:-~/.local/share}/astrid-install.json` on Linux, and
`%LOCALAPPDATA%\astrid-install.json` on Windows.

An active login-service install prevents a Pinokio install and the error names
that installation. Ordinary install/update without an explicit root refuses a
Pinokio selection with:

> Astrid on this computer is managed by Pinokio. Update it from Pinokio.

Install/repair, update and uninstall require the selected Runtime to be stopped:

> Stop Astrid in Pinokio first, then try again.

This refusal avoids racing Pinokio's process ownership. The installer uses
Runtime's `down` lifecycle only to clean up an update's temporary migration
daemon or a failed transaction. Updates still back up, migrate and roll back
through the normal Runtime APIs. They finish stopped. Workspace identity is
checked without starting a browser door. Pinokio performs startup/readiness.

Doctor uses the installed version and can also resolve Pinokio's per-user
selection without `--root`. Skill sync remains best effort. Uninstall retains
workspace data unless `--delete-data` is explicitly requested, and releases the
manager/program pointer after successful removal. The existing uninstalled
workspace receipt remains for a later reinstall. Partial removal retains its
manager pointer so removal can be retried.

## Interface for the launcher

All paths below are absolute. The editor checkout is an `astrid-app` checkout
whose `public/install-manifest.json` pins the matching backend halves. Supplying
`--manifest PATH` or `--manifest=PATH` makes both bootstraps read that file before
fetching tools/packages. It avoids fetching the hosted manifest; installation
still downloads the tools and sources named by the selected manifest.

### macOS / Linux

```sh
ASTRID_ROOT="$PWD/backend"
APP_CHECKOUT="$PWD/editor"

# Install: backend only, using the hosted editor.
curl -fsSL https://astrid.haus/install | sh -s -- --root "$ASTRID_ROOT" --managed-by pinokio

# Install fully local: backend pins from this editor checkout.
sh "$APP_CHECKOUT/public/install" --root "$ASTRID_ROOT" --managed-by pinokio --manifest "$APP_CHECKOUT/public/install-manifest.json"

# Run with the hosted editor.
"$ASTRID_ROOT/run"

# Run fully local; the launcher separately serves the editor at 127.0.0.1:5180.
ASTRID_APP_LOOPBACK_ORIGIN=off "$ASTRID_ROOT/run" --hosted-origin off

# Update after stopping Astrid in Pinokio.
curl -fsSL https://astrid.haus/install | sh -s -- --update --root "$ASTRID_ROOT" --managed-by pinokio

# Update fully local from the selected editor checkout's manifest.
sh "$APP_CHECKOUT/public/install" --update --root "$ASTRID_ROOT" --managed-by pinokio --manifest "$APP_CHECKOUT/public/install-manifest.json"

# Uninstall after stopping; workspace data is retained.
curl -fsSL https://astrid.haus/install | sh -s -- --uninstall --root "$ASTRID_ROOT" --managed-by pinokio
```

### Windows PowerShell

```powershell
$AstridRoot = Join-Path (Get-Location).Path 'backend'
$AppCheckout = Join-Path (Get-Location).Path 'editor'

# Install: backend only.
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --root $AstridRoot --managed-by pinokio

# Install fully local.
& "$AppCheckout\public\install.ps1" --root $AstridRoot --managed-by pinokio --manifest "$AppCheckout\public\install-manifest.json"

# Run with the hosted editor.
$env:ASTRID_APP_LOOPBACK_ORIGIN = $null
& "$AstridRoot\run.cmd"

# Run fully local; the launcher separately serves the editor at 127.0.0.1:5180.
$env:ASTRID_APP_LOOPBACK_ORIGIN = 'off'
& "$AstridRoot\run.cmd" --hosted-origin off

# Update after stopping Astrid in Pinokio.
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update --root $AstridRoot --managed-by pinokio

# Update fully local.
& "$AppCheckout\public\install.ps1" --update --root $AstridRoot --managed-by pinokio --manifest "$AppCheckout\public\install-manifest.json"

# Uninstall after stopping; workspace data is retained.
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall --root $AstridRoot --managed-by pinokio
```

`run`/`run.cmd` resolve `current` on every invocation, load `version.json`, apply
`version.env`, scrub ambient Python/Runtime connection overrides, and set
`ASTRID_INSTALL_MANAGED_BY=pinokio`. Extra arguments reach `astrid-runtime run`.
The Runtime argv and supported `service-env.json` settings come from
`service.command`. POSIX replaces the launcher with that command via `exec`.
Windows evaluates the same foreground command inside the console interpreter;
the hidden login task's `pythonw.exe` and output redirection are intentionally
not used, so console signals reach the Runtime itself. Runtime handles SIGINT,
SIGTERM, Ctrl+Break, and native console close/logoff/shutdown requests through
its normal stop path.

### Pinned Node, npm and npx

`<root>/current` is a text version name. Set `V=<root>/versions/<current>`.
`V/version.json` contains the authoritative absolute Node path at
`env.ASTRID_NODE_EXECUTABLE`; Node is pinned to **20.19.4**.

| Platform | Node relative to V | npm / npx JavaScript entrypoints relative to V |
| --- | --- | --- |
| macOS | `tools/node/node-v20.19.4-darwin-<arm64 or x64>/bin/node` | `tools/node/node-v20.19.4-darwin-<arch>/lib/node_modules/npm/bin/{npm-cli.js,npx-cli.js}` |
| Linux | `tools/node/node-v20.19.4-linux-<arm64 or x64>/bin/node` | `tools/node/node-v20.19.4-linux-<arch>/lib/node_modules/npm/bin/{npm-cli.js,npx-cli.js}` |
| Windows x64 | `tools\node\node-v20.19.4-win-x64\node.exe` | `tools\node\node-v20.19.4-win-x64\node_modules\npm\bin\{npm-cli.js,npx-cli.js}` |

The extractor skips POSIX npm/npx symlinks. Invoke Node with the JavaScript
entrypoint; an ambient `npm` or `npx` is unnecessary. For example:

```sh
V="$ASTRID_ROOT/versions/$(cat "$ASTRID_ROOT/current")"
NODE=$("$V/py/bin/python" -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["env"]["ASTRID_NODE_EXECUTABLE"])' "$V/version.json")
NPM_CLI=$(find "$V/tools/node" -type f -name npm-cli.js)
NPX_CLI=$(find "$V/tools/node" -type f -name npx-cli.js)
cd "$APP_CHECKOUT"
"$NODE" "$NPM_CLI" ci --no-audit --no-fund
```

```powershell
$Version = (Get-Content -Raw "$AstridRoot\current").Trim()
$V = Join-Path $AstridRoot "versions\$Version"
$Node = (Get-Content -Raw "$V\version.json" | ConvertFrom-Json).env.ASTRID_NODE_EXECUTABLE
$NpmCli = (Get-ChildItem "$V\tools\node" -Recurse -File -Filter npm-cli.js).FullName
$NpxCli = (Get-ChildItem "$V\tools\node" -Recurse -File -Filter npx-cli.js).FullName
Set-Location $AppCheckout
& $Node $NpmCli ci --no-audit --no-fund
```

## Platform qualification

macOS tests exercise temporary homes, fake services and an isolated no-pip venv
with a fake Runtime, including foreground PID continuity and descendant cleanup
on SIGINT/SIGTERM. Linux and Windows service/command renderings and manager
boundaries are tested without registering real services. Windows native console
API behavior is mocked. PowerShell execution requires `pwsh`, unavailable on
the development Mac. A real Windows run must prove PowerShell 5.1 argument
binding, `run.cmd` quoting/status, Ctrl+Break, console-close cleanup, native Job
containment, Windows ACL/file-lock behavior and Pinokio Stop. A real Linux run
must prove native process/signal cleanup. No end-to-end Pinokio or editor-server
qualification is claimed by these tests.

## X1 validation, 25 October 2026

Tests ran sequentially with test timeouts disabled, using existing lab
interpreters and temporary homes/fake services. No tools or model assets were
downloaded. No real login service, live Runtime, production directory or live
workspace was used.

| Focused run | Result |
| --- | --- |
| Installer lifecycle/platform/recovery/launcher/cleanup/shim/import/policy subset below | 245 passed, 13 native Windows tests skipped, 27 integration-lane cases deselected |
| Final Pinokio/cleanup/current repeat after partial-uninstall marker fix | 68 passed |
| Installer backup/tools/schema/Remotion/support/sources/ACL/checksum/OMP subset | 190 passed |
| Runtime foreground/signaling/Windows platform subset | 120 passed, 21 native Linux/Windows tests skipped |
| POSIX bootstrap plus two PowerShell source contracts | 32 passed |

The first global-Python run lacked an installed Runtime in isolated child
interpreters and used a symlinked Homebrew interpreter. It was rerun with the
existing lab venv. The first ACL subset used macOS's symlinked `/var` temporary
path; `TMPDIR=/private/tmp` resolved that environment issue. PowerShell execution
was attempted and could not launch because `pwsh` is absent (`ENOENT`). Agent
Ruff and all three worktrees' `git diff --check` passed.

Reproduction commands from the corresponding worktree roots:

```sh
# Agent worktree.
PY=/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/review-agent109-custody/.venv/bin/python
export PYTHONPATH=/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/pinokio-runtime-run
TMPDIR=/private/tmp "$PY" -m pytest -o timeout=0 -q \
  tests/test_installer_pinokio_lifecycle.py tests/test_installer_pinokio_launcher.py \
  tests/test_installer_pinokio_integration.py tests/test_installer_lifecycle.py \
  tests/test_installer_platforms.py tests/test_installer_update_recovery.py \
  tests/test_installer_cleanup.py tests/test_installer_current.py \
  tests/test_installer_service_env.py tests/test_installer_startup_stop.py \
  tests/test_installer_launcher_repair.py tests/test_installer_windows_tasks.py \
  tests/test_installer_shim.py tests/test_installer_bootstrap_imports.py tests/test_skip_policy.py

TMPDIR=/private/tmp "$PY" -m pytest -o timeout=0 -q \
  tests/test_installer_pinokio_lifecycle.py tests/test_installer_pinokio_launcher.py \
  tests/test_installer_pinokio_integration.py tests/test_installer_cleanup.py tests/test_installer_current.py

TMPDIR=/private/tmp "$PY" -m pytest -o timeout=0 -q \
  tests/test_installer_backup.py tests/test_installer_tools.py tests/test_installer_schema.py \
  tests/test_installer_remotion.py tests/test_installer_support.py tests/test_installer_sources.py \
  tests/test_installer_acl.py tests/test_installer_asset_checksums.py tests/test_installer_omp_source.py

# Runtime worktree.
ASTRID_CHECKOUT=/Users/hannahomalley/Developer/astrid-video/astrid-local/labs/pinokio-agent \
  /Users/hannahomalley/Developer/astrid-video/astrid-local/labs/review-runtime-small/.venv/bin/python \
  -m pytest -o timeout=0 -q tests/test_foreground.py tests/test_platform_signaling.py tests/test_platform_windows.py

# App bootstrap worktree.
sh -n public/install
node --test --test-name-pattern='POSIX|PowerShell opens install log appends|PowerShell bootstrap source selects local manifest' \
  scripts/installer/bootstrap.test.mjs scripts/installer/bootstrap-powershell.test.mjs
```

The first command now also collects the two final partial-uninstall regression
cases; its previously recorded count predates those additions. The focused
68-test repeat includes both.
