# Handoff

## Outcome

`NONE`: no actual ordinary guarded recovery remains under `$ORCH` and `/home/user/work/wt` that has a supported command, verified ownership, and no KEEP/open-row/reference/dirty-worktree disqualifier.

The prior recorded Main measurement was `4916580352` bytes against the `4960000000`-byte pre-stage floor, a `43419648`-byte gap. The bounded measurement at `2026-10-26T15:11:11Z` was `4899520512` bytes, a `60479488`-byte gap. This is a measurement only; it does not authorize changing the guard.

## Exact finite owner decision

The only remaining plausible owner decision is the already-recorded lossless Main hub operation:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/hub-repack runtime
```

Its read-only precheck is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/hub-repack runtime --dry-run
```

The real command is owner-gated and mutating; this worker did not run it and makes no new permission request. It must retain its existing lock/live-run/free-space/pack-verification guards. No force, alternate cleanup route, dirty-worktree cleanup, or guard lowering is proposed.

The five known non-KEEP Runtime worktrees are not candidates for this worker: manager records mark all five DIRTY and the supported recycle route refused them. Their contents and sizes were intentionally not read. KEEP pins and current proof fixtures remain protected by their rows/custody; marker release or recycle remains an existing manager/lead decision, not a census inference.

## Next step

Main owner/lead should use the existing decision path: either approve the one guarded lossless `hub-repack runtime` operation, or leave the F-final positive-control gate blocked. After any approved operation, the existing sampler and positive-control workflow must re-establish the admission floor; this census does not perform or authorize that work.
