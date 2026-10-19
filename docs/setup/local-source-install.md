# Install Astrid from local source

On macOS, install CPython 3.11 or 3.12, Node 20.19 or newer, npm, Git, Bun,
the supported OMP agent executable, and FFmpeg (`ffmpeg` and `ffprobe`;
`brew install ffmpeg`). Chat also needs your existing provider authentication.

Use matching, clean checkouts of Astrid, Astrid Runtime, and Astrid App. The
installer records their commits and refuses dirty checkouts. Choose a new
install directory outside those checkouts; it never replaces an existing
installation or workspace.

From the Astrid checkout, run:

```sh
python3 scripts/local_install.py \
  --root /absolute/path/to/new-local-install \
  --runtime-root /absolute/path/to/astrid-runtime \
  --app-root /absolute/path/to/astrid-app
```

The installer builds the selected sources, creates a fresh workspace, and
starts Astrid in this terminal. When it prints `Open https://astrid.haus`, open
that page; it connects by itself. Ctrl-C stops Astrid. The first run needs
network access to download dependencies. Runtime data and caches stay in the
install directory; your existing workspace and global agent settings are left
alone.

To start Astrid again later, run:

```sh
/absolute/path/to/new-local-install/start
```

Options:

- `--ffmpeg /path/to/ffmpeg --ffprobe /path/to/ffprobe` and
  `--bun /path/to/bun --omp /path/to/omp`: tools that are not on `PATH`.
- `--port`, `--proxy-port`, `--acp-port`: other ports, when another local
  installation is running.
- `--wheelhouse /path/to/dependency-cache`: reuse hash-verified dependency
  wheels offline.
- `--check-only`: install, check startup, workspace access, image import and
  one chat reply with your configured model, then stop, leaving no servers
  running.

Rendering and creative providers need their own artifacts and credentials;
this install does not set them up.
