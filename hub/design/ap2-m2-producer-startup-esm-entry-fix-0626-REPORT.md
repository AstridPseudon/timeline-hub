# App M2 producer startup ESM entry fix — 0626

## Result

Prepared the narrowly scoped worker-owned ESM startup artifacts. The App
worktree is unchanged and clean. The required central source preflight was
requested exactly once and failed before producing gate/module output; the
startup smoke was not requested.

## Source tuple

- Exact target: `ap2-m2-producer-realm-physical-path-diagnosis-0538`
- App HEAD/tree: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` /
  `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Original keeper: `/home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545`
- Keeper HEAD/tree pin: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` /
  `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55` /
  `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
  `7ab412cc4bcbe517efcfa806e092336390312e18`

## Owned artifacts and final hashes

All files are under the worker-owned directory
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-esm-entry-fix-0626/`.

| Artifact | SHA-256 | Purpose |
|---|---|---|
| `producer-startup-only-probe.mts` | `4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6` | Exact byte copy of the failing `.ts` probe; `.mts` forces ESM. |
| `producer-startup-module-format-probe.mts` | `d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3` | Tiny format-only probe; imports the existing `DirectHarness`, awaits a resolved promise at top level, and does not start a daemon. |
| `producer-startup-only-gate.sh` | `dbd346763a431c2ae69de4e0fff523511b8c170c13a5a78c58458abb4bbf4d9a` | Existing startup gate copied with only the probe path changed to the owned `.mts`. |
| `producer-startup-custody-gate.sh` | `e218b82a8288d4a9a6f29e6dbbfe082f85e7cd7e8bed9d646aad8b621850cd1b` | Existing tree custody gate copied with owned startup/probe paths, format-probe hash binding, and the format check in `preflight`. |

The original artifacts remain unchanged: custody gate
`66a0410164b53fef514ad661a04e5b8322355636a3840ea6519ea0dd981710c9`, startup
gate `8f3be0c8fcb18ab474b8d5b31c8b6a17b1cdc3d02324b4159d184c266357013c`, and
`.ts` probe `4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6`.
Canonical TSX equality and all inherited Agent, Runtime, wrapper, body,
physical-TMPDIR, and Runtime symlink guards remain literal and unchanged.

## Central commands and results

Literal suite entries were generated from the final custody hash:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-esm-entry-fix-0626/producer-startup-custody-gate.sh | cut -d' ' -f1)" = e218b82a8288d4a9a6f29e6dbbfe082f85e7cd7e8bed9d646aad8b621850cd1b && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-esm-entry-fix-0626/producer-startup-custody-gate.sh preflight
```

Requested once through exact target `ap2-m2-producer-realm-physical-path-diagnosis-0538`:

- Result ID: `ap2-m2-producer-startup-esm-entry-fix-0626-ap2-m2-producer-startup-esm-entry-fix-0626-preflight-1021062810-19823`
- Result: `fail`, exit `1`, in `1s`
- Captured App tree: `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Gate log and runner log: empty; no module-format output and no source-preflight count

The shared 0545 keeper is currently dirty with an untracked
`.public13-effective-ordinary/` tree containing `agent/` and `runtime/` paths.
The copied custody gate preserves the required clean-keeper predicate, and this
worker did not clean or modify that other worker's worktree. The central result
therefore does not qualify the new module-format check. The prior 0617 evidence
still records the old source preflight as PASS with 10 checks, but that is not
evidence for this new artifact tuple.

The startup command was intentionally not requested after the first new
preflight failure. No real module/health result is claimed. No daemon, local
socket, browser, Vite, build, producer body/case, full suite, install, or retry
was run by this worker. No App files were changed; the App worktree remains
clean.

The registered startup command (not run) was:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-esm-entry-fix-0626/producer-startup-custody-gate.sh | cut -d' ' -f1)" = e218b82a8288d4a9a6f29e6dbbfe082f85e7cd7e8bed9d646aad8b621850cd1b && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-esm-entry-fix-0626/producer-startup-custody-gate.sh startup
```

## Blocker and next step

The orchestrator/manager must restore the original keeper's clean state using
the owner of that worktree, then independently rerun the one source preflight
and, only on PASS, the one startup smoke. Do not alter the owned artifacts or
weaken the clean-keeper, source-tree, TSX, physical-TMPDIR, or Runtime guards.
