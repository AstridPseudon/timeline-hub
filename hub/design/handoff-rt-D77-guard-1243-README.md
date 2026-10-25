# D77 private phase guard repair

This is a private diagnostic, with no product, installer, pin, schema or C0
changes. `d77_phase_guard.py` is the single reusable monitor. It has no live
phase launcher. `omp_steps()` only constructs the exact retained OMP sequence;
`Monitor.run()` owns its execution. No real download, install, npm-ci, staging,
render or pressure probe was run for this repair.

The successful 1237 heredoc was recovered by shell decoding the retained worker
log. `retained-1237-wrapper.txt` is that original executable source, stored as
text and never executed here. Its SHA-256 is
`6948b5fbe9b59b424de8b214454ef3501f1fbc6cd3476cda3a7ecdbfc9d12940`.
`retained-1237-source.json` records the source log and retained result hashes.
Neither original was modified. The log contains the original `status=complete`
despite two cancelled commands; the retained result had already been corrected
to `cancelled-lower-bound` by worker 1237.

The old wrapper monitored only subprocess commands. It ran source extraction,
Bun acquisition, native fetch/extract and file moves in its own unmonitored
process, and mixed recursive `du` with guard polling. Native fetch fell from
4,710,780,928 to 4,393,435,136 free bytes over about 2.024 seconds. The ABI and
link commands then launched below the floor. Exit zero on cancellation did not
prevent continuation or a complete status.

The repair:

- Checks >5,200,000,000 free bytes before the first mutation and again after
  setup before Bun install. Every command gets a fresh reserve check before
  launch. Thresholds remain 4,500,000,000 phase and 4,000,000,000 overall.
- Runs source extraction, Bun fetch/extract/chmod/version, unchanged install and
  views commands, lock checks, native fetch/extract/moves/hash, unchanged ABI
  probe and link through the same monitor. Worker descendants inherit the
  monitor-owned process group, including the version probe.
- Samples `statvfs` every 50 ms independently of recursive allocation telemetry.
  Optional bounded `du` runs at boundaries only, with admission rechecked after
  it. The helper has a 180-second default deadline, capped at 1,200 seconds.
- Latches caller cancellation, monitor failure, deadline, command failure and
  low space. No later step starts. SIGINT, then SIGTERM if necessary, target
  only the group created for this command. Cleanup checks live descendants,
  even after the leader exits. Cancellation plus exit zero cannot be complete.
- Returns `unsupported-normal-cancellation-seam` if bounds are missing or
  normal cleanup fails. It retains unfinished process handles for the caller,
  sends no SIGKILL, and never forces a global process. A caller must stop and
  resolve an unsupported tool before any further measurement.

The reserve is `ceil(rate * (0.05 + 0.5)) + burst + 50,000,000` bytes. The rate
and burst must bound all concurrent filesystem writers and in-flight writes;
the declared normal cancellation must finish within 0.5 seconds. Children must
retain the owned process group and user. These are prerequisites, not inferred
facts about Bun, npm or the installer. Scheduling stalls, unbounded writes,
detached descendants and other writers can invalidate polling guarantees.
There are deliberately no live-tool default bounds. Tools without credible
bounds need a supported, bounded normal cancellation seam first. The finite
controls establish wrapper behavior under declared bounds, not live safety.

The fast-growth controls declare 400 MB/s and zero burst, giving a 270 MB
reserve and a 4.77 GB cancellation threshold. A command at the exact retained
4.710 GB native-fetch start is refused before launch. Genuine finite children
simulate growth through the free-stat callback, without allocating that space.
Private fake installer tools exercise the authored OMP worker path, using tiny
files and fixture-only source/lock digests; original pins are checked separately
against the recovered source. No real installer tools are imported by controls.

Run the targeted controls from the worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s diagnostics -p test_d77_phase_guard.py -v
```

The harness's `$TMPDIR` holds only tiny stub files. Shared dependencies and all
other worktrees remain untouched. `evidence/controls.json` and `evidence/tests.log`
contain the finite results; `evidence/frozen-source.json` identifies the exact
review source. No full suite was requested or run.

`phase_complete` means every declared step exited successfully with verified
group cleanup and no latched cancellation. It is not a complete peak bound:
allocation observations are boundary samples and explicitly lower bounds.
Worker 1237's 1,623,728,128 allocated bytes remain an observed lower bound,
not a complete upper bound. No stage-fit claim follows from these controls.
The next action is one independent review of the frozen source and controls;
only the manager can authorize a subsequent isolated npm measurement.

Per the report rule, the final response supplies the report. Shared `design/`
and worker `report.md` are not written by this worker; evidence stays here.
