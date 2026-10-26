# D141y-b validation

## Scope and result

Read-only review result: **FAIL_CUSTODY**. No canonical invocation was made by
this worker. No replay, subset, test, import, generator, staging write,
cleanup, final build, ZIP, or product change was made. Tests/typecheck/lint:
**NOTRUN by task scope**. No suite or browser request was submitted.

## Exact read-only checks

1. `sha256sum PLAN.md BOARD-HEADER.md runtime-D141yb-custody-host-0756-brief.md runtime-D141yb-partial-safe-publication-0756.json` — PASS; hashes are recorded in `source-manifest.json`.
2. SAFE publication byte check — PASS, 10/10 destination files matched the
   publication's declared byte count and SHA-256. The private parent log and
   delivery/work staging were not available on App and were not reconstructed.
3. Fixed tuple Git check, using `git cat-file -e <sha>^{commit}`,
   `git rev-parse <sha>^{commit}`, `git rev-parse <sha>^{tree}`,
   `git status --porcelain --untracked-files=all`, and
   `git merge-base --is-ancestor origin/main <sha>` in each named source
   worktree — PASS for all four commits/trees and clean states. Recorded
   origin/main reads: Agent `64197afa297f86f1e738238d5e80aff6d33e303a`,
   Runtime `fa9cd5464a8b37b02f971de375e56be846cd69e2`, App
   `fc24f84994dc36cfae9349112782ab4d91dbc73b`, Composition
   `67b8aa3d0d6831d3e3504a340ff583c3da253707`; all ancestry checks returned 0.
4. Tuple SHA — PASS:
   `63cd645e36569256fad04837b4f32927e1d84ca81186b49315cc18e91c294643`.
5. Original SAFE artifact sizes/hashes — PASS: command extract 5352 bytes,
   raw stdout 165 bytes, raw stderr 0 bytes, trace 629 bytes, tuple 675 bytes,
   metadata 238 bytes, wrapper 167 bytes, sampler PID 3 bytes, and stop receipt
   89 bytes, with hashes in `source-manifest.json`.
6. Original invocation review — PASS for one exact canonical argv from the
   byte-range extract; original exit, command JSON, results JSON, report,
   DONE, and original sampler lifecycle are missing, not inferred.
7. Delivery source review — PASS. `bin/delivery-build` SHA is
   `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`.
   Lines 659–666 call `preflight_all` before lines 667–680 create staging or
   enter `build_repo`; no result JSON is available to turn the partial output
   into complete patch/bundle/apply proof.
8. Runtime lifecycle source review — PASS read-only. The documented controls
   require authoritative ownership and a retained direct-child wait/reap for
   cleanup; no such genuine Main receipt for original pid 3209/descendants was
   available to this worker.
9. C0 read-only check — PASS/unchanged. `contract/commit-v2.md` SHA is
   `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7` and
   retains the required request fields, merge/read/idempotency/dry-run controls,
   canonical replies, authenticated records/effects/dependencies/history,
   guarded undo, and unchanged preview semantics.
10. Output JSON parse — PASS: `review.json`, `source-manifest.json`, and
    `sampler-lifecycle.json` parse as JSON.

## Original result classification

| Repository | Patch | Tree | Bundle | Apply | Scope |
|---|---|---|---|---|---|
| Agent | PASS_PARTIAL | PASS_PARTIAL | UNKNOWN | UNKNOWN | raw stdout: 29s, one patch, equal tree prefixes |
| Runtime | PASS_PARTIAL | PASS_PARTIAL | UNKNOWN | UNKNOWN | raw stdout: 7s, one patch, equal tree prefixes |
| App | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | no retained result line |
| Composition | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | no retained result line |

This table deliberately does not claim NOT_REACHED for App/Composition because
the retained interrupted artifact set has no complete results record. It also
does not claim a whole-run PASS from the Agent/Runtime partial lines.

## Original trace reconciliation

Dispatch was `4594692096` bytes. The retained sampler began at
`2026-10-26T07:43:11.214010258Z` and first sampled `4592930816`. At
`2026-10-26T07:43:36.304196498Z` it sampled `3930136576`, below the
`4000000000` stop, and exited 75 from its sampler branch. The inline source
does not signal the foreground CLI. Manager stop acknowledged pid 3209;
wrapper pid 3191 finalized at 07:43:59Z with harness rc 0. Actual command exit
and child reaping remain UNKNOWN.

## Review-only sampler

The separate sampler trace and lifecycle show start
`2026-10-26T08:10:26.932353099Z`, five-second samples at
`4944216064`, `4944211968`, and `4944211968`, TERM request, kill return 0,
wait return 0, and `reaped: true`. This proves only this worker's present-time
sampler custody.

## Output hashes

The following were hashed after writing and parsing the outputs. The validation
file's own digest is reported in the final worker report to avoid a circular
self-entry.

```text
report.md             e4c56f86feb1ab9f9b6f3e42f0f23d7e7d731e24227d9c133eb05f336ea2bc27
review.json           ecb3c38ecf96fb8722f5bb1c9b3cb9db9fd0a0e6446f80091d8385de4eb40e8d
findings.md           4def5b50b76e3bc61fde3fe10ab992aabae400222d482bf9ab0c07e62bb30168
source-manifest.json  566d2e005d1d7c3c7f3e755a7c004229d001b875627ecab6c5ea341bce0a585e
handoff.md            d37d9605da005a9e8af71dd8b2a1b89c44993c302786b46f14f9b5df31e6b74e
disk-trace.txt        49cb6c51bad2f7ace5fc9625333cc9d26b13d95eb5f47092ea50e8f21ea73f1f
sampler-lifecycle.json da77102afddc0b76eb7046b33cae440af444c597d4d4dd7a40beea3699cb6289
```
