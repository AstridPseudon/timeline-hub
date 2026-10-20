# Install Astrid

Astrid runs on your own computer, and https://astrid.haus connects to it.

On macOS, first install CPython 3.11 or 3.12, Node 20.19 or newer, npm, Git,
Bun, FFmpeg (`brew install ffmpeg`) and OMP, the coding agent Astrid chats
through (`bun install -g @oh-my-pi/pi-coding-agent`, which provides `omp`).
Chat also needs your existing provider authentication.

Then, in the folder where you keep source code, run:

```sh
git clone https://github.com/banodoco/astrid-agent.git
git clone https://github.com/banodoco/astrid-runtime.git
git clone https://github.com/banodoco/astrid-app.git
python3 astrid-agent/scripts/local_install.py --root ~/Astrid \
  --runtime-root astrid-runtime --app-root astrid-app
```

The installer builds Astrid into `~/Astrid` with a fresh workspace, then starts
it in this terminal. When it prints `Open https://astrid.haus`, open that page;
it connects by itself. Keep the terminal open while you work; Ctrl-C stops
Astrid. The first run needs network access to download dependencies.

To start Astrid again later, run:

```sh
~/Astrid/start
```

The installer never replaces anything: `--root` must be a new or empty folder
outside the three checkouts, and it refuses checkouts with uncommitted changes.
Runtime data and caches stay in that folder; your existing workspace and global
agent settings are left alone. Checkouts you already have work too, if they
are on matching commits.

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
