# Short temp device/inode binding

## Result

The operational helper now binds each claimed `/tmp/vw-*` root to its
`st_dev`/`st_ino`. The existing claim marker records `pid`, `dev`, and `ino`;
validation opens that marker with `O_NOFOLLOW`, verifies its ownership/mode,
and refuses when its recorded identity differs from the current root. Cleanup
revalidates the bound identity before auditing, before each cleanup walk, and
before removing the root. The claim marker is retained until the final
identity check so cleanup can finish safely.

The self-test reproduces the 0841 probe: it copies the original marker into a
different inode at the same path, and cleanup refuses while leaving that
replacement root intact. The original owned root still cleans, including an
ordinary Chrome-shaped symlink leaf whose outside target remains untouched.

The complete successor packet is in this worker directory. It uses the fresh,
unspent namespace `gate6-20261021T0845`; only `run.sh` and `issue.mjs` carry
that new namespace reference. The reviewed App harness and all frozen runner,
source, graph, byte, toolchain, freshness, fd9, child-marker, and accounting
controls remain unchanged. The normal managed export still uses the accounted
attempt/.r root described by the 0832 trace.

## Exact delta

`short-player-temp-device-inode.patch` contains the complete delta from the
0803 frozen runner siblings: the fresh namespace references, the existing
short test-process temp propagation, the device/inode-bound helper, and the
updated source hashes. No product, App, DTO/API, store, pin, package, graph,
or dependency change was made. The Composition worktree itself is clean.

## Controls and tests

All commands below were run without a central request, physical browser run,
issuance, installation, or shared-dependency write:

* `PYTHONDONTWRITEBYTECODE=1 python3 -B short-player-temp-controls.py --self-test` — PASS: 188-byte witness, 107-byte bound, original cleanup, exact replacement refusal, ownership/foreign-root/symlink-root and safe symlink-leaf controls.
* Direct CLI `--claim` followed by `--cleanup` on a fresh mode-0700 `/tmp/vw-*` root from `/tmp` — PASS; both helper mode paths completed and the root was removed only after identity validation.
* Foreign-CWD Bash/Node/Python syntax checks — PASS.
* Foreign-CWD checksum verification using the packet's `SHA256SUMS` entries — PASS.
* Private-copy `patch --dry-run -p1` and apply/byte-compare against the 0803 siblings — PASS.
* `git diff --check` and `git status --short` in the Composition worktree — PASS; no repository changes.
* `bash "$worker/run.sh" --preflight` from `/tmp` — stopped with exit 1 at the frozen validation probe's sandbox `EPERM` while spawning `/home/user/work/venv-runtime/bin/python` (`prepare.mjs:46`). The new helper claim and cleanup both passed, the fresh physical namespace remained absent, and no tuple/grant/marker was issued.

The normal issuance/physical path was intentionally not run. Independent
custody review remains required before any central execution.

## Decisions and limits

The fix uses the existing marker and validation/cleanup helper seam; no new
process registry or framework was introduced. A parent-held descriptor was not
needed for this stated claim/cleanup lifetime because every helper operation
rechecks the recorded root identity, while the marker itself is opened without
following links. The known local sandbox EPERM prevents claiming a full local
preflight result; central/physical evidence remains unverified.
