# OPS D141g-a paired finite closure verification

## Verdict

**FAIL for paired source/control closure; NOT_READY for external release.** The
single prescribed author control run completed with 68 cases and exit 0, but its
own explicit verdict is `SEC001=NEEDS`, `SEC002=PASS`, `freeze2=NEEDS`, and
`release=NOT_READY`. After the 04:30 time-box, these findings go to Main with
no further author loop.

## Findings

### D141G-A-CANCEL-001 — NEEDS / blocking paired closure

The paired 68-case harness proves the direct runner-group cancellation path can
finalize the body-owned trace (`body-cancel-self-finalized-reaped`), but it does
not include the donor's actual mounted `request-stop-test` caller semantics or
the frozen-sampler failure/125 case. The required distinction remains material:
the mounted caller selects session children and excludes the runner, while the
paired control uses direct `killpg(body_pid, SIGTERM)`. The immutable Runtime
donor `56f2d56e…` independently PASSed both in its own 49-case scope, but that
does not qualify this paired receiver.

### D141G-A-CANCEL-002 — UNKNOWN / bounded ownership not proven

The current paired source starts a `timeout` child and waits for it, but the
retained paired evidence has no process-table witness proving that an exited
timeout child is always reaped across cancellation. The earlier retained race
showed trace finalization can precede terminal status; the exact child-ownership
cause remains UNKNOWN. No claim is made beyond this bounded evidence gap.

### D141H-SEC-001 — NEEDS / blocking paired closure

The current run's seven descriptor/inode/physical-parent custody attacks all
returned bounded PASS and observed no redirected writes. However, the paired
control still reports `SEC001=NEEDS` because the complete donor cancellation
and sampler-lifecycle cases are not present in the paired harness. The donor's
`O_NOFOLLOW`, regular-file, owner 0600, single-link, nonblocking, parent binding,
same-descriptor append/validation, bounded reaping, and frozen-sampler controls
remain accepted only for immutable Runtime donor `56f2d56e…` / independent
0418, not for the paired receiver as a complete closure.

### D141G-SEC-002 — PASS within bounded source/control scope

The production validator no longer accepts `D141g-paired-control` or an
arbitrary renamed pair authority. Matching-hash wrong-suite, wrong-source,
wrong-twin, wrong-command, replay, corrupt-pair, and unauthorized-source
attacks refused before launch and before artifacts. The only positive route is
the exact historical `D141g-next-app-journey` 520d binding, which is not a
freeze-2 release binding.

### D141L-APP-001 — NEEDS / external release blocker

The available App packet is historical prospective 520d with `registration=false`
and command hashes `600fca0f…` / `82f4ad3c…`. No reviewed normal App freeze-2
head plus genuine new production-builder output and D66 atomic registration
was available. The source/control result must therefore be distinguished from
release readiness: Runtime's bounded controls do not authorize App, and no
current hashes may be invented, preregistered, or refreshed blindly.

## Prior finding disposition

The 0344 symlink/FIFO failure is closed for the immutable Runtime donor and the
current paired seven-attack subset, but not promoted to complete paired SEC001
closure. The 0418 donor PASS is retained as donor evidence only. The 0400 SEC002
correction is independently confirmed by this run. No source correction or
additional author loop is authorized by this report.
