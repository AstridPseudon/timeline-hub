# Agent Gate7 private Python 3.11 mypy exit diagnosis

Date: 2026-10-21 UTC  
Scope: diagnosis only; no checker rerun, source/config/stub/threshold/lock change,
test-service request, daemon, browser, renderer, or network request.

## Finding

The prior worker did start the requested unchanged command and mypy analysis
started. It is not possible to classify the result as pass or fail. The
retained `exit=0` is the dispatcher/Codex worker exit, not the exit of `make`,
the compare wrapper, or mypy.

The strongest evidence is:

- The exact tool call was recorded in the prior worker log at lines 6383–6390:

  ```bash
  set -u
  RECORD=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-gate7-private311-mypy-once
  PRIVATE_ROOT="$RECORD/gate7-private311-source8afe"
  AGENT_SRC="$PRIVATE_ROOT/source/agent-8afe"
  V="$PRIVATE_ROOT/venv/bin/python"
  PYTHONDONTWRITEBYTECODE=1 make -C "$AGENT_SRC" PY="$V" mypy
  exit $?
  ```

- The unchanged Make target is `$(PY) -m scripts.reshape.compare_mypy_baseline`
  followed by the success echo. The compare wrapper uses
  `subprocess.run(..., capture_output=True, text=True, check=False)` and its
  exact child argv is:

  ```text
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-gate7-private311-mypy-once/gate7-private311-source8afe/venv/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
  ```

- Therefore mypy stdout/stderr were held in the compare process until mypy
  returned. There is no durable command stdout file, stderr file, or child
  return-status file. The dispatcher’s outer command was also wrapped as
  `timeout 10800 codex exec ... -o <worker>/report.md - > <worker>/log.txt
  2>&1`; `report.md` is the Codex report, not mypy output.

- The private cache was written from `06:00:16.172Z` through
  `06:00:53.915Z`. It contains 1,324 valid JSON files: 602 under `astrid`, 14
  under `scripts/reshape`, and dependency caches including NumPy and YAML.
  The target cache files are complete JSON pairs, but cache population is only
  evidence that analysis began; it is not a result.

- The next independent process snapshot in the worker log found no `make`,
  compare-wrapper, or mypy process. The prior worker log then ended without a
  result line for the hanging tool call. The worker later wrote `exit` as `0`
  and ended normally after writing `BLOCKED`; those files describe Codex’s
  outer lifecycle. No orphan remained at the recorded observation time.

## Expected lifecycle versus observed lifecycle

Expected for a valid pass: mypy child exits `0`; the compare wrapper parses
stdout/stderr, compares the unchanged baseline, emits its summary; `make`
prints `✓ mypy baseline (no type regression)` and returns `0`; the shell’s
`exit $?` is retained by the command runner. Expected diagnostic failure is
the same lifecycle with a nonzero result and durable diagnostic output. An
unexpected child status is converted by the wrapper to a `RuntimeError` with
the child status and available output.

Observed: cache writes prove the child ran, but neither the child status nor
the wrapper’s post-`subprocess.run` path was retained. There is no final Make
success line, no compare summary, no diagnostic, and no traceback. This is
consistent with the command-runner/control-plane losing the shell/tool call
while it was still active, but that cause is not proven. A self-terminating
mypy failure is also not proven: if the parent had survived a normal child
SIGKILL, `subprocess.run` would have returned a negative status and the wrapper
would have emitted a traceback. The historical cause is `UNKNOWN`.

## Resource/orphan diagnosis

No accessible evidence supports OOM, disk exhaustion, or a surviving orphan:

- `dmesg -T` was not readable (`Operation not permitted`) and
  `journalctl -k --since 2026-10-21 05:50:00 --until 2026-10-21 06:10:00`
  reported no journal files. This makes kernel-level historical attribution
  unavailable.
- The accessible cgroup counters have no memory limit, `memory.failcnt=0`,
  `memory.memsw.failcnt=0`, and `memory.oom_control` reports
  `oom_kill=0`, `under_oom=0`; these are not worker-specific historical proof.
- The worker recorded 13,631,376 KiB (about 12.99 GiB) free on the filesystem
  after the run. Its private tree was about 1.5 GiB. No disk-floor breach was
  recorded.
- The later `ps -ef` showed only the diagnostic sandbox and the snapshot
  command, not a detached checker tree. Thus this was not an observed orphan.

Conclusion: resource cause and exact signal are historical `UNKNOWN`; do not
claim an OOM kill, timeout, mypy pass, or mypy failure.

## Private environment qualification checks

The prior worker’s passed checks remain the available pre-run evidence:
`pip check`, isolated import checks, `python scripts/vendor_lock.py check
runtime.lock.json --producer <private Runtime95 source>`, source/product
identity checks, and unchanged `make -C <private Agent source> PY=<private
venv>/bin/python preflight`.

Read-only rechecks/identity records for the same private environment:

| Item | Evidence |
| --- | --- |
| Interpreter | `/usr/bin/python3.11`, CPython `3.11.17`; venv executable is `.../gate7-private311-source8afe/venv/bin/python` |
| Agent source | commit `8afe5a87dfe093ac5efd017106acb03cc597509c`, tree `9eac28e8ac1d24d2020c9b3700ea54ddef5812cd`; private source file hashes match those commit blobs |
| Runtime source | commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Agent runtime lock | `sha256 7a05eb67ba9aa2efbcb81ba57225351abf0456e63b67110e5fe75cec16732cb5`; Python 3.11 selects NumPy `2.4.6` |
| Runtime publication lock | `runtime.lock.json` `sha256 920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`, source commit matches Runtime95 |
| Agent wheel | `astrid-0.1.0...whl`, `sha256 585a10fb33821f5babf71089086e847a869ac8d9eca59fd76c18bc82ea1f0751` |
| Runtime wheel | `astrid_runtime-0.1.0...whl`, `sha256 5236bc9dadb51190403b1a61b7e3ea2467f7d221f8532844197dad9c01e4ec78` |
| Client wheel | `astrid_runtime_client-0.2.14...whl`, `sha256 837ce7218ea177eccd036373c900e5f2f27ad0f60f05d945e4feafb3f11add28` |
| NumPy wheel | `2.4.6`, lock-wheel `sha256 89cd468399cfd2504718f0ba50e410dca55a170b61a02ad92bb18c8a65186e93`; installed version `2.4.6` |
| Mypy closure | `mypy 1.17.0`, `mypy_extensions 1.1.0`, `pathspec 1.1.1`, `typing_extensions 4.16.0` |
| Test-only stub | `types-PyYAML 6.0.12.20260906`, wheel `sha256 bca893ff0d51df5c9053137d5d0e6ccd36e939a196356f1d5c16372422f5137b`; not in repository declarations/locks |
| Wheelhouse | `sha256sum -c wheelhouse.sha256` passed for all 169 recorded wheel entries |
| Imports | From `/tmp` with `python -P`, `astrid`, `astrid_runtime_client`, `runtime_protocol`, `banodoco_timeline_schema`, `mypy`, `yaml`, and `numpy` all resolve inside the private venv |

One non-hermetic but non-mypy detail is retained: the private source’s
`remotion/node_modules` is a symlink to the read-only shared
`/home/user/work/runtimes/agent-remotion-main95bd/node_modules`, added only so
the unchanged preflight could check its required directory. No shared install
was modified. The private source also contains wheel-build `build/` and
`astrid.egg-info/` output and the mypy cache; these are outside the repository
worktree and are not typecheck source/config changes.

## Prepared named central-suite command (not run)

The central test service cannot provide a useful result from its normal
worktree snapshot unless its allow-list entry is given absolute access to this
private environment. The following is the single prepared command for a named
entry; it must not be submitted by this diagnosis worker. It captures command
stdout, stderr, exit, timing, and a final status record without changing the
checker target or configuration. `OUT` is deliberately outside the source
tree so it cannot be mistaken for repository output.

```bash
agent gate7-private311-mypy-capture env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin bash -c '
  set -u
  RECORD=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-gate7-private311-mypy-once
  PRIVATE_ROOT="$RECORD/gate7-private311-source8afe"
  AGENT_SRC="$PRIVATE_ROOT/source/agent-8afe"
  V="$PRIVATE_ROOT/venv/bin/python"
  OUT="$RECORD/gate7-private311-mypy-capture"
  mkdir -p "$OUT"
  date -u +%FT%TZ > "$OUT/start"
  set +e
  /usr/bin/time -v -o "$OUT/time.txt" timeout --signal=TERM --kill-after=60 2700s \
    make -C "$AGENT_SRC" PY="$V" mypy >"$OUT/stdout.txt" 2>"$OUT/stderr.txt"
  rc=$?
  printf "%s\n" "$rc" > "$OUT/exit"
  date -u +%FT%TZ > "$OUT/end"
  printf "argv: make -C %s PY=%s mypy\nexit: %s\n" "$AGENT_SRC" "$V" "$rc" > "$OUT/status.txt"
  exit "$rc"
'
```

This command is intentionally only prepared. The current diagnosis does not
rerun mypy and does not request a central suite.

## Unverified / next step

Gate7 remains unqualified. The orchestrator should decide whether to run the
prepared named command once, after registering it with the central service and
preserving this same private source, venv, wheelhouse, Runtime95/client
artifacts, and output paths. A captured `exit` plus stdout/stderr is required
before any pass/fail or baseline comparison claim.
