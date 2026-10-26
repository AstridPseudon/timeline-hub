# OPS D141h independent final findings

Verdict: **PASS within the finite source/control scope.** The exact terminal candidate `56f2d56e7d241d303be85df62166570d51602101` / tree `744cca68f672153dd84f7ba20e580b6e917ccf6d` is accepted for Main’s next decision. No product or release qualification is claimed.

## Closed findings

- **D141H-SEC-001 — PASS.** The seven required trace-custody attacks all executed: symlink, FIFO, regular-file replacement, and physical-parent substitution before final append, plus symlink/FIFO/regular replacement before validation. Each refusal was bounded, and the controls observed zero redirected writes. The implementation preserves `O_NOFOLLOW`, regular-file checks, device/inode/owner/mode/link-count checks, physical-parent binding, nonblocking opens, and same-descriptor validation.
- **D141H-VERIFY-001 — PASS.** The original cancellation/reaping control completed. The cancelled body finalized its own trace and was reaped; the mounted `stop-test` caller also produced cancelled/130, trace validation PASS, and sampler reaping.
- **D141H-CANCEL-001 — PASS.** EXIT and deferred signal traps are installed before sampler launch; readiness, child PID, partial reads, descriptor closure, and pending cancellation are preserved.
- **D141H-CANCEL-002 — PASS.** The actual dispatcher stop-test source was read and the mounted caller was run only against an isolated root. It marks `CANCELLED`, selects session children with `ps -g`, excludes the runner, and applies TERM/KILL within its existing bound.
- **D141H-CANCEL-REAP-001 — PASS.** Sampler reaping is bounded at 80 probes of 0.1 seconds with KILL fallback; `df` and same-descriptor validation have 2-second and 5-second timeouts. A SIGSTOP sampler failed closed as exit 125 and was reaped.
- **D141H-CANCEL-EXIT-001 — PASS.** The stopped-sampler path has no unset-lowercase-variable diagnostic and retains the existing caller behavior that turns trace failure into exit 125.

The earlier 0340 and 0402 failures were read before testing. They applied to earlier candidate states: the append-custody control had not run in 0340, and cancellation aborted before it in 0402. The current immutable candidate’s single complete pass reached both areas.

## Contract and scope findings

The approved C0v2 contract remains unchanged and was checked read-only. Its request preserves `api_version`, project/timeline scope, exact `base_revision_id`/`base_publication_id`, ordered `commands`, `label`, `steps` with per-step `patch`, declared `reads`, `merge: fields|atomic`, idempotency, `dry_run`, `source`, `rationale`, and `group_id` (design/commit-v2.md:60-80, 179-246). The reply contract preserves accepted/merged canonical closure receipts with bindings, effects, dependencies, history and guarded undo, conflict reason/head, structured invalid code/path/hint/suggested_command, and preview (design/commit-v2.md:703-715, 1266-1305, 1423-1434, 1565-1633). No DTO edits are present: the candidate commit changes only the five private D141 files.

The production caller was demonstrated read-only: `ORCH/bin/dispatcher-daemon` line 20 invokes `ORCH/bin/test-run` for `TEST <FULLID>`, and the candidate `bin/test-run` identifies that caller at line 2. The control harness itself does not call `--run`, edit the live dispatcher tree, or use a live queue.

## Non-findings and limits

No actual installation, CAS, service request, product test/import/collection, live queue, network, package/environment provisioning, child-venv/runtime activity, Store/bench activity, cleanup/delete, hub write, D130, stopped worktree, build, ZIP, credentials, receipt attachment, full suite, or gate/body qualification was performed. The five-file publication was only an isolated copy/parity smoke performed by the controls.
