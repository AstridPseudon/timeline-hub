# App M2 producer shell custody and startup — 0655

## Decision

**Custody review: APPROVE. Startup qualification: FAIL (stop-on-first-failure).**

The 0647 repair is internally consistent for the requested central checks. I
registered exactly two new named suites against the unchanged service target
`ap2-m2-producer-realm-physical-path-diagnosis-0538`. No old 0626 result was
reused, and no producer actual/body/case was run.

## Reviewed immutable tuple

```text
producer-physical-keeper-gate.sh       c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab
producer-startup-only-gate.sh          46cf870be41d5db7f109b05f11b0c1fcd2c38f5975dbeb0db1bee78907a51d62
producer-startup-custody-gate.sh       4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f
producer-startup-only-probe.mts        4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6
producer-startup-module-format-probe.mts
                                        d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3

App keeper commit/tree: b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 / fd16d32fd3487e56c9fe1ff16582dba240f63b77
wrapper SHA:             329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
Agent commit/tree:      8130a401bf44a518d5a40ae274d398b8c560be55 / 236c3e57e0265c52b81ba8085de3193026176bff
Runtime commit/tree:    2c4ac180c2220bdad966bc01e95ad230e99ce26a / 7ab412cc4bcbe517efcfa806e092336390312e18
tsx bin/CLI:            8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8
tsx loader:              0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1
tsx package:             6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2
```

The retained probe hash is unchanged at `4beb7c22…`; the existing 0626
custody registration remains separate at its old hash
`e218b82a8288d4a9a6f29e6dbbfe082f85e7cd7e8bed9d646aad8b621850cd1b`.
The 0647 custody hash was recomputed as
`4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f`.

The review verified service `PWD`/tree and keeper HEAD/tree are separate
values, canonical `tsx` hashes and alias identity, physical private scratch
and run roots, early EXIT/HUP/INT/TERM cleanup, physical locked graph, source,
Agent, Runtime, artifact, and epoch/head guards, and both literal probe argv
forms. The assigned App worktree remained unchanged. Available space was
12,829,704 KiB (above the 10 GiB floor); the run used only the two private
Agent/Runtime clone roots and did not modify shared graph or dependencies.

Review syntax command:

```sh
for f in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/*.sh; do sh -n "$f"; done
```

Result: PASS. Independent hash/pin/physical-graph/argv/cleanup assertions:
PASS.

## Central runs

Registered only these two `app` entries in the central suite allow-list:

```sh
app ap2-m2-producer-startup-shell-contract-repair-0647-preflight test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh | cut -d' ' -f1)" = 4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh preflight
app ap2-m2-producer-startup-shell-contract-repair-0647-startup test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh | cut -d' ' -f1)" = 4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh startup
```

Exact central commands and results:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-startup-shell-contract-repair-0647-preflight --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# PASS, exit 0, 7s

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-startup-shell-contract-repair-0647-startup --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# FAIL, exit 1, 13s; first failure was the positive health identity assertion
```

Preflight result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-startup-shell-contract-repair-0647-preflight-1021065526-25064/`

Startup result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-startup-shell-contract-repair-0647-startup-1021065559-4382/`

## Actual module, health, and teardown

- Module preflight: `DirectHarness` loaded as ESM; no daemon invoked.
- Startup negative: planted realm-root symlink was refused by Runtime.
- Startup positive: Runtime started, but direct `/v1/health` returned a body
  with `realm_id` absent (`undefined`) while the probe expected harness realm
  `cd19567850a74a098273544f0fa87061`. The HTTP status assertion had passed;
  the probe stopped at the realm identity assertion, so door health was not
  reached.
- No browser, Vite, build, install, list, run, producer body, or producer case
  was invoked.
- The probe's `finally` teardown ran, and the shell trap removed the private
  startup root. No `tla-startup-*` root or logged resolver temp root remained.

## Keeper postflight

Before central execution, a byte-level baseline recorded 5,912 regular files
and 2 symlinks in the protected keeper. After both central runs, the complete
file hash and symlink manifests were identical; Git status was clean; keeper
HEAD/tree remained `b8cc7e1c…` / `fd16d32f…`; and the canonical
`node_modules` link was unchanged. This is a PASS for the full no-new-keeper-
bytes postflight.

## Blocker and next prerequisite

The 0647 custody repair is not startup-qualified because the exact pinned
Runtime health payload does not satisfy the retained probe's `realm_id`
identity contract. Do not rerun either 0647 result or add another suite under
the same failed identity. The next prerequisite is an orchestrator-approved
diagnosis of whether the Runtime health contract or the startup probe is the
wrong side of this mismatch, followed by a new bounded artifact/hash and a
fresh independent review. No source or App worktree files were changed here.
