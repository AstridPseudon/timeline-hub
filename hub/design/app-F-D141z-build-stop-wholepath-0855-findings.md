# F D141z wholepath findings

Result: **FAIL remains controlling; no new acceptance claim.** This is a finite
read-only source map for the same return0855 owner. It confirms independent0847
FAIL6 and identifies the exact receiving gap separately from intrinsic source
gaps.

## 1. Existing compatible heavy route

The normal ownership route is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run`, not the candidate's private lock:

- `test-run:4-5,50-59` classifies `full*` as heavy, rejects an existing heavy
  state, applies the configured floor, records `heavy` and `key.running`, and
  launches the body through `setsid nohup --run`.
- `test-run:61-121` starts the donor sampler as the exact body child, retains
  its ready binding, and terminalizes via `d141-append-final.py`.
- `test-run:123-159` enters the existing bench-store lease, binding the
  registered suite command before acquiring the lease.
- `test-run:161-249` is the lifecycle supervisor: child subreaping,
  `PR_SET_PDEATHSIG`, `BENCH_CONTROL_FD` process-group discovery, TERM/KILL,
  `waitpid`, and cancellation/parent-death return 130.
- `test-run:294-312` finalizes trace before terminal status and only then
  removes running markers.

The candidate instead opens `/tmp/timeline-final-delivery-heavy.lock` at
`delivery_lifecycle.py:203-210`, which is not consulted by `test-run` and does
not consult `alive heavy`, `bench-store`, `D/heavy`, or `C/key.running`.
Concurrent candidate and normal-service bodies can therefore be admitted by
different mechanisms. This is intrinsic F3.

## 2. Actual finalcaller → D68 → builder and stop surfaces

The candidate route is:

`run-final-delivery.py:171-191` → `delivery_lifecycle.run_delivery` →
`delivery_lifecycle.py:229-250` starts the D68 process in a new session →
`runtime-D141z-input-0812-delivery_gate_build.py:308-328` stages the four repos,
imports the builder, and calls `main_with_args`/`main` in that same D68 process.
The D68 wrapper itself is not the mounted service supervisor and does not
create the builder process.

The candidate lifecycle does provide a local process-group path:

- `delivery_lifecycle.py:224` enables `PR_SET_CHILD_SUBREAPER`, but there is
  no `PR_SET_PDEATHSIG` equivalent.
- `:246-317` starts the command with `start_new_session=True`, discovers known
  descendants/groups, sends TERM then KILL, and calls `_reap`/`waitpid`.
- `:197-202,295-306` handles only local SIGTERM/SIGINT, an optional
  `cancel_path`, timeout, and sampler state. It does not implement the
  mounted `CANCELLED`/control-pipe/parent-death contract from `test-run`.
- `:321-335` validates the trace by pathname after stopping the sampler;
  there is no donor append-final descriptor handoff.

Consequently the source does not qualify early leader exit while a descendant
remains, mounted stop semantics, or supervisor parent death. These are F4/F5
intrinsic failures, not proof that the original 0741 outcome succeeded or
failed; that historical outcome remains unknown.

## 3. Binding and descriptor custody

Passing donor purpose is concrete, not a copied PASS flag:

- `d141-disk-trace.py:42-67` binds every physical parent directory using
  `O_NOFOLLOW` and a device/inode/owner/mode hash.
- `:98-107` creates the trace with `O_EXCL|O_NOFOLLOW`, requires one-link,
  owner-only mode 0600 regular-file identity, and publishes all binding fields.
- `d141-append-final.py:97-123` reopens and checks the parent hash, opens the
  same trace by descriptor, checks device/inode/owner/mode/link count, appends
  the final row, and calls `d141-validate-trace.py --fd` with `pass_fds` and
  the binding.
- The validator's `--fd` path (`d141-validate-trace.py:123-132`) fstats the
  already-bound descriptor before reading it.

The failed candidate accepts any line beginning `ready\t`
(`delivery_lifecycle.py:156-165`), stores it as an opaque string, monitors the
trace by pathname (`:275-292`), and invokes the validator in path mode
(`:125-135,331-335`). It never parses or checks the binding and never calls
append-final. A same-user replacement of the pathname can therefore become
the monitored/validated file. This is intrinsic F2.

The acceptance weakens this further: `check.sh:60-67,125-126` installs a
permissive validator stub for all lifecycle cases; only the direct helper
case at `:205-211` uses the real sampler. The normal case reaches
`candidate.run_wrapper` once (`:189`), but no case reaches `candidate.main`.

## 4. Harmless source seams

There is no existing harmless App fixture that truly reaches `main()` without
the genuine route. `run-final-delivery.py:220-223` checks the absent core
runner, core inventory, canonical D68 wrapper, and caller-supplied builder
before dispatch. `check.sh` therefore exercises `run_wrapper` once and calls
`run_delivery` directly for all other cases. Its stub builder waits for its
child (`check.sh:76-83`), and its cancel case writes a timer-created local
file (`:176-187`); neither is the installed early-leader/mounted cancellation
seam.

The actionable source conclusion is to restore/use the existing genuine
receiving coordinates and normal ownership route, then have the later owner
review the real caller path. This report does not propose a new interface,
lock, admission exception, or test harness.

## 5. Exact dependency coordinates

The following are the source-declared genuine inputs and their exact hashes;
the first two and the canonical D68 path are absent at the App venue, rather
than inferred absent from Main:

| coordinate | SHA-256 | read-only state |
| --- | --- | --- |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-route-return-sol-2349/evidence/candidate/run-final-services.py` | `8aea49759e600d18f5ed1f5e297269aa8dddad3a24024f776ac37e7c7d53acd7` | absent |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-route-return-sol-2349/evidence/candidate/core-inventory.json` | `e6a1fa17796e493532c3927e2ec6fc8fdb4e1928b7540be8c6644b3d0894bb14` | absent |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-D68-review-1554/evidence/delivery_gate_build.py` | `bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779` | absent at canonical path; exact safe copy is under `design/` |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build` | `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca` | present at donor bin; not in App source tree |

Donor hashes verified read-only: `test-run` `f674569b…`, append-final
`14546f70…`, sampler `d7b989ea…`, validator `b1cb8c23…`. The complete values
are in `source-map.json`.

## Classification

- Intrinsic: F2 custody, F3 admission interoperability, F4 main/D68 bypass,
  F5 mounted/parent-death/early-leader qualification, and F6 two tracked
  CPython 3.13 bytecode files outside the four-file author manifest.
- Host input gap: F1 canonical Runtime dependency coordinates are absent on
  App; the six SAFE0812 originals and exact hashes were read, not installed.
- Unknown: original 0741 exit/reaping outcome; no replay/backfill.
- C0: unchanged. This investigation adds no Runtime payload validator,
  schema, or wire shape.
