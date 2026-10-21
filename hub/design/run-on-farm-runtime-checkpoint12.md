Status: HOLD

# Runtime 12:00 checkpoint full — test farm request

## Scope and source identity

- Repo: Runtime
- Hub/integration branch: `tl/integration`
- Runtime checkout for the farm: `/home/user/work/runtime`
- Current Runtime commit: `b92d3e7a05eec65c142294ef4873edd059e9b31d`
- Current Runtime tree: `6abc2f117391de8e7e35c0283f575a002199894d`
- Current observed Runtime checkout is clean and is on `tl/integration`.
- This is one Runtime repository full suite, with no targeted file list.

The normal Agent dependency is the existing checkout `/home/user/work/agent` on
`tl/integration`, supplied through `ASTRID_CHECKOUT` and `PYTHONPATH`. The
current observed normal-Agent identity is commit
`1a50cf3f30398500e9f1ccf0b94d59fe7a8bdb3f`, tree
`b286a34197313b552132b442915b8f318b7bb062`; the farm must re-check this
identity when the checkpoint head is selected.

The public014 compatibility identity remains the existing lock, not a new
checkout or release: `/home/user/work/agent/runtime.lock.json` selects Runtime
producer commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, client `0.2.14`,
schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
and producer version
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
The farm must verify that lock before running; it must not substitute a private
consumer or private candidate.

## Exact farm command

Use the existing tested retained-owned-temp wrapper from
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py`.
Run exactly once from the Runtime checkout, after the farm's preflight:

```sh
cd /home/user/work/runtime && \
env -i \
  HOME=/root \
  LANG=C.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  ASTRID_CHECKOUT=/home/user/work/agent \
  PYTHONPATH=/home/user/work/runtime:/home/user/work/agent \
  /home/user/work/venv-runtime/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py \
  -- /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

Required paths and identities:

- Runtime interpreter: `/home/user/work/venv-runtime/bin/python` (the command
  invokes this interpreter both for the wrapper and pytest).
- Normal Agent source: `/home/user/work/agent`; its `runtime.lock.json` is the
  public014 lock described above.
- Agent venv path retained for dependency/origin preflight only:
  `/home/user/work/venv-agent/bin/python`. It is not a substitute for the
  Runtime interpreter in this command.
- Tool path: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin` (Node
  `20.19.4` if inspected by the farm preflight). Runtime full does not invoke
  Node, Remotion, a browser, a renderer, or a native run.

The wrapper creates one fresh mode-0700 `/tmp/rt-full-*` root, sets
`TMPDIR`, `TMP`, and `TEMP` to it, adds pytest `--basetemp` under that root,
and retains the root for diagnostics. The farm must use short private run
directories (including any socket, runtime, or browser-related directory it
creates) with the longest socket path under 100 bytes. For any Remotion host
that the farm environment probes or starts, `NODE_OPTIONS`, `NODE_PATH`, all
`LD_*`, and `PYTHONHOME` must be unset locally; do not alter the wrapper or
unset them globally. A zero-test collection or any test failure is a FAIL.

## Prerequisite and stop conditions

Before the expensive run, the farm lead must verify all of the following in one
preflight and list every failure before stopping:

1. Runtime commit and tree match the identities above (or the refreshed
   checkpoint identities below), and the Runtime checkout is clean.
2. Normal Agent checkout and tree are the selected checkpoint dependency;
   imports resolve from `/home/user/work/agent`, not an installed or private
   consumer. The public014 lock remains exact and its 76-artifact/runtime
   metadata is unchanged.
3. Both venv paths, the Runtime pytest entrypoint, and the tool path exist and
   are readable. Shared venvs, runtimes, node_modules, and toolchains are
   read-only.
4. The wrapper path exists and is the retained-owned-temp wrapper named above;
   no new wrapper framework, storage-floor override, archive, install, or
   checkout process is introduced.
5. A short private temp/run directory is available with mode 0700, the farm has
   at least 5 GiB free, and no unrelated process owns the run's private paths.
6. The command is exactly the one above, with no `|| true`, test weakening,
   retry, browser, renderer, native, or archive/install step.

## Prior accepted evidence

The unchanged current b92 run must not be repeated locally. The accepted
retained-owned-temp result is:

- Result: `runtime-full-retained-owned-temp-integration-1021035028-28646`
- Runtime tree: `6abc2f117391de8e7e35c0283f575a002199894d`
- Exit: `0`
- Counts: `6002 passed, 26 skipped, 15 xfailed, 12 warnings`
- Duration: `298.37s` (`299s` service result)
- Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-full-retained-owned-temp-integration-1021035028-28646/log.txt`
- Summary: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-full-retained-owned-temp-integration-1021035028-28646/summary`
- Retained root reported by the log: `/tmp/rt-full-vmr8_qka`

That run used the same wrapper and pytest command with the non-scrubbed suite
environment: `ASTRID_CHECKOUT=/home/user/work/agent`,
`PYTHONPATH=$PWD:/home/user/work/agent`,
`/home/user/work/venv-runtime/bin/python -m pytest -q -n 3`. Its log has no
failures; the skips are Windows-native cases, the xfails are the held RT02/D04
legacy writer/clip-replacement cases, and the warnings are Python 3.13 fork
deprecations. It is evidence for b92/tree6abc, not an all-gates, ZIP, browser,
renderer, or owner-film claim.

## Checkpoint-head refresh

No new integration merge is required for the unchanged b92 checkpoint. If the
manager selects a new Runtime integration merge before 12:00, the packet needs
only an identity refresh: replace the Runtime commit/tree above, re-check the
normal Agent commit/tree and public014 lock, and record the farm log path. The
retained wrapper, exact pytest command, prerequisites, and HOLD state do not
change. The manager marks this request READY and sends it only after that head
selection; this worker does not submit or execute it.

