# Agent wrapper client-prefix first-cause repair — worker report

## Result

Repaired only the diagnosed 1008 false refusal in
`scripts/full_coherent_public_current_integration.sh`. The embedded preflight
now uses explicit archive-source-root → canonical-wheel-root maps. The public
client map is exactly:

```text
packages/python/astrid_runtime_client/ -> astrid_runtime_client/
```

Agent and Runtime package roots retain identity maps. Wheel and archive members
are canonicalized only through those known roots; unsafe traversal, unknown
roots, duplicate members, missing members, and byte differences refuse. The
existing 164-pin/hash, 166-RECORD/distribution closure, install/source bytes,
eight-origin, C13, disk, pytest argv, collection, child, and signal guards are
otherwise unchanged.

## Exact reviewable source

- Worktree: `/home/user/work/wt/agt-m4-full-wrapper-client-prefix-firstcause-repair-1014`
- Branch: `tl/agt-m4-full-wrapper-client-prefix-firstcause-repair-1014`
- Base/HEAD: `475fb69df31fc5af059669343f1fae4545e8e723`
- HEAD tree before harness commit: `23dab4e59b36d8c70e52b9eeb1a8bcc4203f50ce`
- Changed file blob: `594c16e1f21340f179296fa341e22233df7efa54`
- Changed file SHA-256: `5d899819082448b90f583cd83268fd768fdbf8138aca290be43c15bb05a5314d`
- Diff: one file, wrapper only; no product endpoints, DTOs, stores,
  authorities, generated files, pins, shared dependencies, or other worktrees
  changed.

The durable MAIN suite/lease registration contract is recorded at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-full-wrapper-client-prefix-firstcause-repair-1014.md`.
It deliberately does not edit the shared `suites.conf` or lease files;
handoff 1010 owns activation and the final request. No live caller or active
lease for this wrapper exists at report time.

## Tests

All passed; no build, install, profile, pytest body, live socket, browser,
renderer, or full suite was run.

- `bash -n scripts/full_coherent_public_current_integration.sh` — PASS.
- `git diff --check` — PASS.
- AST parsing of both embedded Python blocks — PASS.
- Compact embedded-function seam test — PASS: correct client prefix maps
  archive bytes to wheel bytes; wrong bytes refuse; traversal, extra root, and
  missing member cases refuse.
- `SOURCE_ROOT="$PWD" FULL_COHERENT_PUBLIC_PROFILE_ROOT= FULL_COHERENT_PUBLIC_AGENT_WHEEL= FULL_COHERENT_PUBLIC_PINS= bash scripts/full_coherent_public_current_integration.sh` — exit **2** as expected; setup refusal occurred before pytest and retained missing-profile/wheel/source and storage diagnostics.

The independent 1008 review is the first-cause basis:
`agent-review-current-full-wrapper-repaired-final-1008.md` — REQUEST CHANGES
for the unnormalized client source prefix and absent live registration. A new
independent delta review is required before MAIN activation; no third blind
full request was made.

## Handoff files

- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-full-wrapper-client-prefix-firstcause-repair-1014/commit-msg`
- Completion marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-full-wrapper-client-prefix-firstcause-repair-1014/DONE`
- Blocked marker: not created; the bounded repair is complete.
