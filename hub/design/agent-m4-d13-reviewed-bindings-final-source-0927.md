# D13 reviewed bindings final source — 2026-10-21

## Result

The f4ed test tree now contains only the approved 0914 tracked binding/setup
helper and its offline tests:

- `/home/user/work/wt/agt-m4-d13-reviewed-bindings-final-source-0927/tests/packs/video_editing/d13_bindings.py`
- `/home/user/work/wt/agt-m4-d13-reviewed-bindings-final-source-0927/tests/packs/video_editing/test_d13_bindings.py`

Both files are byte-identical to donor commit
`806860a046fc4eba467f8b4a80871d62ef2d2e7c`, tree
`70e47954b1651b33e9fcdcea1ac421e5bb1d58dc`. The product source remains
Agent `f4edcb4bce531be3ea8c6389069429175b048c2a`, tree
`1cbd18011b56c41a5ef31f155c15bd373c1208e6`; the current worktree has no
other changed paths. The harness will create the separate test-only commit.

No proof body, launcher, daemon, Runtime/HTTP/socket operation, browser or
renderer operation, native execution, install/download, schema/DTO/pin,
authority, grant, or full suite was added or run.

## Existing carriers derived from verified paths/hashes

The corrected 0908 private profile, independently approved by 0917, is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b`

Its existing profile retains exactly these four keys and values:

```json
{
  "profile": "astrid",
  "runtime_checkout": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages",
  "source_checkout": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages",
  "runtime_environment": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv"
}
```

The existing seven-key binding carrier is derived as:

```json
{
  "agent_commit": "f4edcb4bce531be3ea8c6389069429175b048c2a",
  "agent_tree": "1cbd18011b56c41a5ef31f155c15bd373c1208e6",
  "agent_wheel": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/wheelhouse/astrid-0.1.0-py3-none-any.whl",
  "agent_wheel_sha256": "7455220aa1d3f8c67c7c9cee0f7a6571fb4f51882eca2543ead25943eebd185a",
  "source_checkout": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages",
  "source_digest": "f6cdf8c2daada3f4877802baf839cdbecede7943fc3c0312d2aa4d4933abe09a",
  "runtime_environment": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv"
}
```

No new carrier field or authority value was introduced. The normal fixture's
credentials, project, task, and grants remain execution-time fixture state;
the test opt-in is not production authority.

## Prerequisite inventory

The 0908 custody report and 0917 independent review are reused unchanged;
no broad re-audit was performed. Their recorded checks pass for the selected
private profile: zero symlinks/hardlinks, contained RECORD rows, exact Agent /
Runtime / client wheel payloads, exact versions, eight isolated origins, and
schema-first resolution.

The 0914 read-only inventory is reused for the immutable Remotion/tool
closure: supported Chromium cache, fonts/provenance, OMP/native inputs,
media/tool resources, and VibeComfy. The concrete resources are:

| resource | path | SHA-256 / identity |
| --- | --- | --- |
| Node | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` | `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`; v20.19.4 |
| Chromium | `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` | `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95` |
| FFmpeg | `/usr/bin/ffmpeg` | `ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41` |
| FFprobe | `/usr/bin/ffprobe` | `272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f` |
| Remotion lock | `/home/user/work/runtimes/agent-remotion-f4ed-0013/package-lock.json` | `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24` |
| VibeComfy | `/home/user/work/fixtures/vibecomfy` | `31f90bb03d330283b76e7dbdda51197be787090d` |

Remotion fonts are under
`/home/user/work/runtimes/agent-remotion-f4ed-0013/public/fonts`, with the
existing `FONT_PROVENANCE.md` and non-empty bundled `.woff2` closure. The
normal native positive obtains execution media through its existing fixture;
no media artifact or grant was fabricated here.

The helper's constructed `env -i` shape contains only its existing named
inputs (`HOME`, locale, PATH, temp/bytecode controls, installed profile,
selected pack/source/tool paths, schema path, and source manifest). The
forbidden `NODE_OPTIONS`, `NODE_PATH`, `PYTHONHOME`, `PYTHONPATH`, and every
`LD_*` variable are absent; `ASTRID_RUNTIME_CHECKOUT` is added only by the
existing named-collection command builder as its explicit checkout selector.

Read-only source archive/wheel parity against the required clean KEEP checkout
`/home/user/work/wt/agt-pin-f4edcb4b` returned `[]` from
`d13_bindings.source_archive_matches_checkout(...)`. That checkout is exactly
f4ed/tree `1cbd1801...`; the installed pack source digest is the seven-key
`source_digest` above.

## Targeted evidence

Commands run in the current test tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/d13-reviewed-bindings-pytest \
  tests/packs/video_editing/test_d13_bindings.py
3 passed in 0.83s

/home/user/work/venv-agent/bin/python -m ruff check \
  tests/packs/video_editing/d13_bindings.py \
  tests/packs/video_editing/test_d13_bindings.py
All checks passed.

git diff --check
passed
```

The helper and test files were compared with `git show 806860a04:<path>` and
matched exactly. The worktree changed-path check reports only those two test
files.

## One later named run (not executed here)

After READY, the manager owns exactly one named run of the original positive
collection, with normal fixture authority. The existing suite selects only:

`tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render`

The complete `env -i` command to export for that later run is:

```text
env -i \
  HOME=/home/user/work/wt/agt-m4-d13-reviewed-bindings-final-source-0927/.d13-home \
  LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/bin:/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 \
  TMPDIR=/home/user/work/wt/agt-m4-d13-reviewed-bindings-final-source-0927/.d13-tmp \
  ASTRID_HOST_EXECUTION_PROFILE=installed \
  ASTRID_PACK_HOST_PYTHON=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/bin/python \
  ASTRID_PACKS_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages/astrid/packs/rendering \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-f4ed-0013 \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-f4ed-0013/node_modules \
  ASTRID_FFMPEG_EXECUTABLE=/usr/bin/ffmpeg \
  ASTRID_FFPROBE_EXECUTABLE=/usr/bin/ffprobe \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages \
  ASTRID_RUNTIME_SOURCE_MANIFEST=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/profile/astrid.json \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/agt-pin-f4edcb4b \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/bin/python \
  -B -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  /home/user/work/wt/agt-m4-d13-reviewed-bindings-final-source-0927/tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

This command is exported only; it was not run by this worker. No additional
external approval was identified in the existing contract. The 0917 approval
is the recorded independent review of the corrected private profile, not an
inferred production authority or a new approval flow.
