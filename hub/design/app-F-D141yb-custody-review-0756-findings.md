# F D141y-b findings

Verdict: **FAIL_CUSTODY**. This verdict is for the interrupted 0741 result
and custody record, not for a new build attempt.

## F1 — original terminal and child-reap custody is missing

Status: **FAIL_CUSTODY / UNKNOWN**.

The SAFE publication says `evidence/raw-command.exit`, `command.json`,
`results.json`, `report.md`, `DONE`, and `sampler-lifecycle.json` were missing.
The retained wrapper log proves pid 3191 reached finalize at 07:43:59Z and
reported harness rc 0; the manager stop receipt acknowledges pid 3209. Neither
proves the foreground canonical CLI exit, foreground-child reaping, or the
original sampler's TERM/wait/reap. The Main descendant/process-audit receipt
was not present in the available inputs. Do not convert harness rc 0 to a
delivery PASS.

## F2 — disk stop crossed during the invocation and did not signal the CLI

Status: **PASS for the retained trace fact; FAIL_CUSTODY for terminal CLI
disposition**.

Dispatch admission was 4,594,692,096 bytes. The original sampler started at
07:43:11.214010258Z and first sampled 4,592,930,816 bytes. It sampled
3,930,136,576 bytes at 07:43:36.304196498Z, a drop of 664,555,520 bytes from
dispatch and 662,794,240 bytes from the first sample, then recorded
`SAMPLER_TERMINAL reason=below_stop_or_unreadable`. The sampler subshell exits
75; the retained source has no signal to the foreground CLI. Therefore this
is a disk-stop observation, not an authenticated command termination.

## F3 — partial Agent/Runtime output is real but not a whole-run result

Status: **PASS only for the exact raw lines; whole-run qualification FAIL**.

Raw stdout is 165 bytes. It records Agent `PASS in 29s; 1 patch(es)` with
`d362fe9dfdbd / d362fe9dfdbd / d362fe9dfdbd`, and Runtime `PASS in 7s; 1
patch(es)` with `78df31d62c5b / 78df31d62c5b / 78df31d62c5b`. These are retained
partial patch/tree facts. The absent results JSON means bundle and apply
fields are UNKNOWN, not inferred from the three hashes. App and Composition
have no retained result line and are UNKNOWN. There is no whole-run PASS.

## F4 — fixed source tuple and invocation identity authenticate

Status: **PASS**.

The tuple JSON hash is
`63cd645e36569256fad04837b4f32927e1d84ca81186b49315cc18e91c294643`; all
four requested commit/tree pairs resolve exactly in their named clean worktrees.
The byte-exact command extract has parent SHA
`03c2b022a872d47321753e23652bb60a17916f59458240d315a7169028560815`, byte
range `[297154,302506)`, and extract SHA
`0991fa80f48825250a56cc2bc652f4e420d115eb4f28ec251c9643a92e1155c8`.
It contains one canonical argv and no review-created invocation.

## F5 — SAFE transport is complete for the listed partial set, not the private parent

Status: **PASS for byte transport; LIMIT remains**.

All ten listed SAFE artifacts match the publication's byte counts and SHA-256
values. The parent log and private delivery/work staging remain Main INPLACE/KEEP
and cannot be independently rehashed from App. No product payload or credential
was exported.

## F6 — policy/control checks

Status: **PASS for read-only review controls; no test credit**.

Canonical source inspection shows `preflight_all` before staging/work-root
creation and the `build_repo` loop. C0 remains the v2 request/reply contract
with the required request fields, merge/read/idempotency/dry-run controls,
canonical accepted/merged/conflict/invalid replies, history/effects/dependencies,
and guarded undo. No source or product file was changed. Tests, typecheck, lint,
browser, import, generator, staging, cleanup, final build, ZIP, and suite runs
were NOTRUN.

## F7 — own sampler is present-time custody only

Status: **PASS for this review's sampler; not historical evidence**.

This review started a real five-second sampler at 08:10:26.932353099Z, observed
4,944,216,064 bytes initially and 4,944,211,968 bytes at the final samples,
requested TERM, waited with return 0, and recorded `reaped: true`. Its lifecycle
and trace are separate outputs and explicitly do not establish the original
0741 sampler lifecycle.
