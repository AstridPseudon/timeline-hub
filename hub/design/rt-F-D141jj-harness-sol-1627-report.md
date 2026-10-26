# Qualification: FAIL

The sole allowed isolation repair is complete and diagnostic evidence is captured, but source qualification **does not pass**. One complete checker invocation exits1 at preserved `stale-nonapp-upstream`. No production source repair, retry, installer activation or integration.

## Changes and decisions

Only private derivative `check_jj.py` and data under this absolute evidence root were written. `checker-diff.patch` contains all four hunks:

- Line23 binds `CANDIDATE` to the genuine immutable original root `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate`. No candidate copy or manifest hash refresh.
- Lines223–225 allocate a private `mkdtemp` service directory for each low-admission refusal unless an explicitly malformed service root was supplied; then set TMPDIR/TMP/TEMP to that per-invocation directory.
- Line322 creates positive service TMPDIR with mode0700.
- Lines416–418 apply the identical per-invocation isolation to normal refusals. Explicit wrong-stage owner/mode fixtures remain unchanged; all original assertions/handlers/raises and refusal purposes remain unchanged.

Inspected whole ordering before editing: actual caller -> inherited lifecycle -> D68 alternates-backed staging -> stub positive; then manifest refusal; installer no-install and receiving/preimage controls; root mismatch; stale non-App upstream; owner/mode/stage refusals; wrong App base/tree; dirty/symlink/ref-drift checks. Low-admission branch retained. No lifecycle/production guard changed.

## Findings and blockers

See `findings.md` and `review.json` for every finding. Isolation eliminates the trace collision. The next existing defect is exposed: stale fixture advances HEAD without moving origin/main, so the exact stale-upstream condition is false. D68 runs successfully and creates a PASS receipt for that mislabeled negative; assertion remains failing. Static inspection also shows that genuine D68 refusal returns a code/writes a FAIL receipt, whereas negative helper expects an exception/no receipt, and stage-owner spoofing trips source-owner validation earlier. Fixing these changes fixture meaning/negative entry-point semantics beyond the authorized isolation-only repair, so no further checker attempt or source change was made. Remaining negatives unverified in this run; seven purposes preserved, not claimed passing.

## Commands and evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-harness-sol-1627/evidence/check_jj.py` — exit1, actual positive PASS, no-install/preimage controls PASS, stale-source-manifest PASS, root mismatch PASS, then original stale-upstream assertion fails. One complete command, no retries; `tmp/check_jj.log` contains the failure.
- `ruff check --isolated --no-cache --select F /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-harness-sol-1627/evidence/check_jj.py` — exit0.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-harness-sol-1627/evidence/tmp/validate.py` — final exit0: scoped AST/private compile/JSON, all40 assertions/3 handlers/3 raises unchanged, exact original checker+11 source bytes/modes conserved, immutable builder conserved, authorized four-repo tuple/trees/refs clean, all13 SAFE blobs verified against original immutable Git objects. Earlier validator setup errors and no-index status interpretation are recorded in `validation.md`.
- Diff check: no-index exit1 with empty diagnostics (expected differences), no whitespace errors. Types N/A.
- Original same33 actual PASS log retained, not rerun; all11 candidate hashes match its controlling review. Original positive check exit1 remains historical FAIL; never converted into qualification PASS.

`source-manifest.json` is unchanged manifest content SHA256 `7c3fa7c10dd4afb7e01f6af32aaf28ffb94a16c81730095d36bc514683b27852`; `tmp/source-identity-before.json` and `review.json` retain original checker and all11 per-file hashes/modes. Source tuple remains Appabac6c80/Agentec0a9f5b/Runtime95d98f03/Composition635f4de0, Appbasefc24f849, others64197afa/fa9cd546/67b8aa3d. No worktree file written.

## Resource and custody limits

One heavy checker process, two sequential bounded D68 staging operations because stale negative unexpectedly succeeds; total measured stage bytes 1880490, limit100000000. Positive admission 5213392896, poststage 5211492352; negative admission 5210284032, poststage 5208756224. All exceed pre4960000000/post4860000000 floors. No source repos copied, only original alternates-backed no-checkout staging. No cleanup/deletion command, no shared dependency writes.

First-tool sampler launch did not survive; first replacement failed while stopping absent initial PID. Initial coverage gap is disclosed, so **not complete whole-worker monitoring**. Persistent supervised real5s sampling covers checker/validation; no floor tripped. Final PID/exit/wait/reap recorded in `sampler-lifecycle.json`. Test invocation uses real private evidence/tmp directory, not harness tmpdir pointer.

## Recommended next step

Manager independently review FAIL and separately authorize the non-isolation harness corrections if desired. No installation, product merge, realbuilder, rehearsal, service action, ZIP or publication follows from this result.


Final sampler: supervisor PID 8, sampler PID 9, PGID 8; supervisor exited0, sampler exited0, sampler waited/reaped=true. 82 durable samples; minimum available 5208170496 bytes; max observed gap 5.129s. No 4,000,000,000-byte floor trip. Initial launch gap and small post-stop report bookkeeping remain outside coverage; no claim of complete whole-worker monitoring. Final supervised validator exited0 and was waited/reaped.
