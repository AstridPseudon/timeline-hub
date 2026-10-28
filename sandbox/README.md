# U1 local Timeline sandbox

This is a disposable CLI/SDK path through the Agent wheel and a local Astrid
Runtime. It uses generated PNG stand-ins and a new Runtime data root for each
smoke run. It does not need credentials or media from a real project.

## Build and install

Requirements: Linux or macOS, Python 3.12, Git, and network access to download
the hash-locked dependencies. The Runtime daemon also needs local loopback
socket access. Run these commands from the Agent checkout. The Runtime source
is read from `/home/user/work/runtime` at the exact commit in
`runtime.lock.json`; all build outputs stay outside both checkouts:

```bash
AGENT_ROOT="$PWD"
RUNTIME_REPO="/home/user/work/runtime"
TASK_TMP="${TMPDIR:-/tmp}/astrid-u1"
mkdir -p "$TASK_TMP/wheelhouse"

# Build the Agent wheel with its product build lock. The installed-artifact
# helper keeps its source snapshot, builder venv and wheel under TASK_TMP.
SMOKE_WHEEL_WORKSPACE="$TASK_TMP/agent-build" PYTHON_BIN=python3.12 bash scripts/smoke_wheel_install.sh
cp "$TASK_TMP/agent-build/dist/astrid-0.1.0-py3-none-any.whl" "$TASK_TMP/wheelhouse/"

# Build Runtime from the commit pinned by runtime.lock.json, not its mutable
# working tree. Run from the Runtime checkout.
RUNTIME_SHA="$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["source_commit"])' "$AGENT_ROOT/runtime.lock.json")"
mkdir -p "$TASK_TMP/runtime-source"
git -C "$RUNTIME_REPO" archive "$RUNTIME_SHA" | tar -x -C "$TASK_TMP/runtime-source"
python3 -m venv "$TASK_TMP/build-venv"
"$TASK_TMP/build-venv/bin/python" -m pip install --require-hashes -r "$AGENT_ROOT/requirements/build.lock"
"$TASK_TMP/build-venv/bin/python" -m build --wheel --no-isolation --outdir "$TASK_TMP/wheelhouse" "$TASK_TMP/runtime-source"

# The maintained release runbook's universal runtime lock is the available
# hash-locked dependency closure for this local pair. Download it once into the
# wheelhouse, then install without reaching an index.
cp "$AGENT_ROOT/requirements/runtime.lock" "$TASK_TMP/wheelhouse/python-requirements.lock"
python3.12 -m venv "$TASK_TMP/venv"
"$TASK_TMP/venv/bin/python" -m pip download --require-hashes -r "$TASK_TMP/wheelhouse/python-requirements.lock" -d "$TASK_TMP/wheelhouse"
"$TASK_TMP/venv/bin/python" -m pip install --no-index --no-deps \
  "$TASK_TMP/wheelhouse/astrid-0.1.0-py3-none-any.whl" \
  "$TASK_TMP/wheelhouse/astrid_runtime-0.1.0-py3-none-any.whl"
"$TASK_TMP/venv/bin/python" -m pip install --no-index --find-links "$TASK_TMP/wheelhouse" \
  --require-hashes -r "$TASK_TMP/wheelhouse/python-requirements.lock"
"$TASK_TMP/venv/bin/python" -m pip check
```

For a different checkout location, set `AGENT_ROOT` and `RUNTIME_REPO` to its paths.
Set `TASK_TMP` to a private temporary directory; do not use a shared venv or
wheelhouse. The Agent wheel contains the canonical `astrid_runtime_client`, so
the pair is exactly one Agent wheel plus one Runtime service wheel.

## Run the smoke

From the Agent checkout, in a fresh shell each time:

```bash
export ASTRID_SANDBOX_VENV="${TMPDIR:-/tmp}/astrid-u1/venv"
export ASTRID_RUNTIME_CHECKOUT="${TMPDIR:-/tmp}/astrid-u1/runtime-source"
bash scripts/u1_sandbox_smoke.sh
```

The script creates a uniquely named project and timeline, imports three
generated images, commits one image onto V1, shows the saved timeline, captures
the timeline at one second to PNG, undoes the accepted commit, then shows the
timeline again. Each run starts and stops its own Runtime instance. Its printed
`SMOKE_ROOT` retains the disposable Runtime data and frame PNG for inspection;
the script does not remove user data. The frame is read back through
`media open --materialize` from the Runtime managed PNG artifact.

## Recipe notes

The current `docs/setup/release-recipe.md` still marks the producer manifest,
both final wheel names/hashes, and `python-requirements.lock` as
`PENDING_PRODUCER_HANDOFF`; it therefore cannot supply a final published
wheelhouse. For this local U1 qualification, the Agent's `requirements/build.lock`
and `requirements/runtime.lock` from the maintained reproducible-release
runbook are used instead. The release recipe's `pip install --no-index
--require-hashes -r ...` example also omits `--find-links "$ASTRID_WHEELHOUSE"`;
without that option, pip cannot locate dependency wheels downloaded into a
separate wheelhouse. This sandbox adds `--find-links` and leaves the lock,
Agent/Runtime contract, and product code unchanged.

The frame smoke uses `--mode inputs`, the render-free route also shown by the
release recipe. Its PNG is a declared-placement view and labels itself
“metadata only”; it does not contain composed source pixels. A composed frame
needs the separately paired rendering resources (Remotion bundle, browser,
fonts and media tools) that the current release manifest still lists as
pending.
