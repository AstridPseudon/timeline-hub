# Install the local branches in one command

On macOS, first install CPython 3.11 or 3.12, Node 20.19 or newer, npm, Git,
and FFmpeg with both `ffmpeg` and `ffprobe` executables. They are required for
media import, including still images. For a Homebrew installation, the media
prerequisite is `brew install ffmpeg`. This command installs the app from
prepared prerequisites; it is not a zero-prerequisite machine bootstrap.
Check out the matching Astrid, Workspace Runtime, and Reigh app branches and
commit any local changes. The installer records all three exact commits and
refuses dirty checkouts. Select a new installation directory outside all three
checkouts; an existing installation or workspace is never replaced.

From the Astrid checkout:

```sh
python3 scripts/local_install.py \
  --root /absolute/path/to/new-local-install \
  --runtime-root /absolute/path/to/banodoco-workspace-runtime \
  --app-root /absolute/path/to/reigh-app
```

This builds both Python wheels from clean Git snapshots, verifies their
package contents against the selected sources, consumes Astrid's hash-locked
build/runtime dependencies, and installs the noneditable pair in the new
directory. It builds Reigh with `npm ci` and the selected Astrid browser
inputs, creates a fresh Runtime-owned workspace, checks its installed
identity and schema, and starts the app at `http://localhost:2222`.
Network access is needed for dependencies on the first run.

Runtime discovery, credentials, application state, and caches stay in that
installation directory. The person's existing workspace, agent skill links,
and global instructions are not changed. The Runtime profile binds the
installed site-packages tree and private interpreter. Browser build inputs
remain separate from Python execution; the launcher never uses `PYTHONPATH`.
Project creation uses the app's supported Runtime connection.
The installer validates and records the exact FFmpeg/FFprobe executables,
versions, and hashes before creating a workspace. It exposes them through
private executable links in the runtime venv. If they are outside PATH,
pass `--ffmpeg /absolute/path/to/ffmpeg --ffprobe /absolute/path/to/ffprobe`.
Missing tools fail before installation state or a realm is created.

The app runs in the foreground. Ctrl-C stops this app launch and the new
Runtime through its supported lifecycle. To restart the installed pair later:

```sh
/absolute/path/to/new-local-install/with-env \
  /absolute/path/to/new-local-install/venv/bin/astrid-runtime up --profile astrid \
  --data-root /absolute/path/to/new-local-install/support --json
/absolute/path/to/new-local-install/with-env sh -c \
  'cd /absolute/path/to/new-local-install/sources/app && exec npm run dev:local'
```

To stop Runtime separately, replace `up` with `down` in the Runtime command.
The installer leaves `install.json`, `runtime-receipt.json`, the exact wheels,
and a credential-free `with-env` wrapper for later inspection and restart.

For a fresh installation check without keeping servers running, add
`--check-only`. It still installs packages, creates a new workspace,
builds Reigh, checks the app connection, and creates/reads back one
`installation-check` project in that fresh workspace, imports a small PNG,
and verifies its Runtime-owned readback; it then stops that new Runtime.
Choose unused ports with `--port`, `--proxy-port`, and `--acp-port` when another
local installation is running. `--wheelhouse /absolute/path/to/dependency-cache`
reuses hash-verified runtime dependency wheels offline; Astrid and Runtime
product wheels are always rebuilt from the selected commits. The build
toolchain still comes from the checked-in hashed build lock.

This local source route verifies app startup, Runtime project access, and
image media import.
Rendering, creative providers, and OMP/agent execution require their own
artifacts and credentials and are not provisioned or qualified here. It does
not certify the maintained published release, update an existing realm, or
perform a backup/restore qualification.
