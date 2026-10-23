# OPS-retire-venv-1539 corrected return

## Verdict

**PASS — corrected immutable three-file packet prepared for independent review; no live installation or publication was performed.**

Packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-return-1539/evidence/kit/`

The exact original packet remains untouched at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-1512/evidence/kit/`

## Corrections

- `retire-child-venv` now treats every present pending entry as an inspection obligation. Dangling symlinks, directories, other non-regular entries, and unreadable entries refuse before the named request exemption; the regular named request still remains exempt from reference matching.
- Present running-worker `brief.md` and `env` paths now include dangling symlinks in the inspection set, so every present uninspectable path refuses. Truly absent optional files remain allowed.
- `ancestor_pid` uses a narrow stderr-suppressed `printf` failure return to avoid the prior process-substitution broken-pipe diagnostics. No process guard or traversal logic changed.
- `request-retire-venv` is byte-identical to the prior packet. `dispatcher-daemon` remains byte-identical to authoritative ORCH except for the single existing `RETIREVENV` branch line.

## Evidence

- `evidence/independent-review.sh` is the durable reconstructed independent fixture source.
- `evidence/independent-tests.log` reports **SUMMARY pass=36 fail=0**.
- `evidence/old-candidate-independent-tests.log` retains the prior independent **SUMMARY pass=33 fail=3** result; all three old failures are now green.
- `evidence/hashmanifest.txt`, `evidence/packet.patch`, `evidence/dispatcher.diff`, `evidence/handler-fix.diff`, and `evidence/final-validation.log` record source identity and scope.

## Exact validation

- `bash -n evidence/kit/request-retire-venv evidence/kit/dispatcher-daemon evidence/kit/retire-child-venv` — PASS, exit 0.
- `evidence/independent-review.sh` — PASS, exit 0, 36/36. This covers the eligible aged read-only success, malformed names/paths, symlinks, young and exact-one-hour targets, builder markers, provisioner markers, suite/env references, pending dangling/non-regular entries, running-worker metadata and dangling env, unreadable input, process argv/exe/cwd/open-fd, FIFO continuation, outside sentinel, exact dispatcher call shape, and positional request payload.
- `sha256sum -c evidence/hashmanifest.txt` — PASS, exit 0.
- Dispatcher diff — expected diff exit 1; exactly one non-header added line and zero non-header removed lines.
- Request writer comparison with the prior packet — PASS, `cmp` exit 0.
- `shellcheck` — unavailable (`command -v shellcheck` exit 1); no ShellCheck result is claimed.
- Corrected fixture log contains no `Broken pipe` diagnostics.

## Limits and next steps

No actual dispatcher daemon, `ensure-daemons`, `run-manager`, `hub-sync`, live installation, timestamped predecessor backup, real venv build/removal, network, Git operation, or normal publication was run. Fixture work stayed under temporary paths; the production default remains `/home/user/work`, and the fixture root override does not add production authority.

Next: independent review of this corrected packet, then the separate host-side idle atomic install with timestamped backup and normal publication. This is a report-only / NEVERMERGE product branch.
