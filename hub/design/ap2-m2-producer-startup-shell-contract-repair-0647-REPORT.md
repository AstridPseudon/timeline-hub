# App M2 producer startup shell contract repair — 0647

## Result

Prepared a self-contained correction of the 0626 startup artifacts in the
worker-owned record:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/
```

No App source files, shared worktrees, shared `node_modules`, shared venvs,
branches, refs, or suite configuration were changed. No central run was
requested. The 0641 diagnosis is confirmed: 0626 reached its first use of an
undefined `SERVICE_ROOT` at custody line 81 after the source gate's ten checks;
0545 placed `RUN_ROOT` below `SHORT_APP_ROOT`, a symlink to the protected
keeper.

## Minimal artifact correction

- Copied the 0545 source gate and the two immutable `.mts` probes into this
  worker's record without changing their bytes.
- Copied the 0626 custody/startup gates into this worker's record and changed
  only their owned-artifact paths plus the required shell contract:
  - custody captures `SERVICE_ROOT=$PWD` and `SERVICE_TREE` before child-gate
    directory changes; `KEEPER_HEAD` and `KEEPER_TREE` remain separate pins;
  - custody runs the format probe from the captured service cwd, so `SERVICE_ROOT`
    is defined before its former line-81 use;
  - startup installs its EXIT/HUP/INT/TERM cleanup trap immediately after the
    physical `mktemp` root is created;
  - startup keeps the short App alias for import/cwd resolution, but puts
    `RUN_ROOT` at `$SHORT_ENV_ROOT/.public13-effective-ordinary`, a physical
    private root rather than below the keeper symlink;
  - startup asserts the private run root is physical before creating private
    Agent/Runtime clones.

The keeper remains the original protected checkout, with its `KEEP` marker,
clean status, `/home/user/work/app/node_modules` link, HEAD
`b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`, and tree
`fd16d32fd3487e56c9fe1ff16582dba240f63b77`.

## Final artifact hashes

```text
producer-physical-keeper-gate.sh       c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab
producer-startup-only-gate.sh          46cf870be41d5db7f109b05f11b0c1fcd2c38f5975dbeb0db1bee78907a51d62
producer-startup-custody-gate.sh       4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f
producer-startup-only-probe.mts        4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6
producer-startup-module-format-probe.mts
                                        d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
```

Retained pins:

```text
Agent commit/tree:       8130a401bf44a518d5a40ae274d398b8c560be55 / 236c3e57e0265c52b81ba8085de3193026176bff
Runtime commit/tree:     2c4ac180c2220bdad966bc01e95ad230e99ce26a / 7ab412cc4bcbe517efcfa806e092336390312e18
App HEAD/tree:           b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 / fd16d32fd3487e56c9fe1ff16582dba240f63b77
wrapper:                 329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
body commit/tree:        36dd91257fd13dcad0d58b48c790caa5063b4c8c / d908845dbc8e5ebf96698d08621557e904f20c52
spec/helper/config:      d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89 /
                          50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016 /
                          5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
tsx bin/CLI:             8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8
tsx loader:              0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1
tsx package:             6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2
```

## Cheap shell invocation contract diagnosis

- Custody modes are exactly `preflight|startup|list|run`; missing or unknown
  modes exit 2. `preflight` runs the source gate in the captured service cwd,
  then invokes only the format-only `.mts` probe. `startup` delegates to the
  startup-only gate. `list|run` delegate to the existing source gate.
- The service cwd carrier is the invocation `PWD`, captured as
  `SERVICE_ROOT`; its committed tree is `SERVICE_TREE`. The keeper's original
  commit is independently captured as `KEEPER_HEAD`, with `KEEPER_TREE` used
  for the shared-tree comparison. A wrong cwd fails the service-tree and
  wrapper checks.
- The startup gate checks the service tree, keeper HEAD/tree/clean/link/KEEP,
  locked graph presence, then invokes source preflight. Its exported runtime
  roots are the private `RUN_ROOT/agent` and `RUN_ROOT/runtime`; the Agent and
  Runtime clones are `--shared` and are only created inside that private root.
  No install or source edit was performed here.
- The short source alias is intentionally the only symlink:
  `SHORT_APP_ROOT` points at the keeper for import resolution and cwd
  shortening. `RUN_ROOT`, `TMPDIR`, XDG roots, npm/Vite/Playwright caches,
  browser output, and the clone roots are under the physical
  `SHORT_ENV_ROOT`. Cleanup uses `find -P` over that physical root and cannot
  traverse the App alias into the keeper.
- The exact probe entry is the owned `.mts` path passed as argv 1 to `tsx`;
  the format probe receives `SERVICE_ROOT`, while startup receives
  `SHORT_APP_ROOT`. The immutable startup probe retains both the planted
  Runtime-root symlink refusal and the physical-root positive check.
- The existing wrapper's graph/resource contract remains pinned: locked graph
  `app-ap2-m2-locked-graph` and its source archive are physical and hash-bound;
  its ordinary selector forwards the exact Playwright list/run argv and
  requires one discovered test (`Total: 1 test in 1 file`). No flock or new
  resource/copy implementation was added.
- Inherited environment is not trusted for custody location: `SERVICE_ROOT`
  is explicitly assigned from `PWD`. Startup explicitly exports checkout,
  Python, bundle-head, browser, cache, `TMPDIR`, XDG, bytecode, user-site, and
  Node settings, and unsets direct App checkout overrides. The shell contract
  does not modify shared dependency paths.

## Cheap preflight evidence

Commands and results:

```text
sh -n producer-physical-keeper-gate.sh                 PASS
sh -n producer-startup-only-gate.sh                    PASS
sh -n producer-startup-custody-gate.sh                 PASS
cheap contract assertions                              PASS 21 / FAIL 0
```

The local custody preflight was run once from this clean App source checkout.
The source gate passed all ten checks and printed its existing graph/source
preflight PASS. The subsequent real `tsx` format probe could not open its IPC
pipe in this sandbox and failed with `listen EPERM` before module execution.
This is not claimed as ESM or startup qualification; central review is still
required.

Mutation checks used temporary copies and were cleaned with `find -P`:

```text
wrong FORMAT_PROBE path       exit 1
wrong PROBE_SHA                exit 1
unset inherited SERVICE_ROOT  exit 1 at sandbox tsx EPERM, not nounset
missing custody argv           exit 2
invalid custody mode           exit 2
wrong custody cwd              nonzero
```

The physical private-root placement/cleanup check passed without changing the
keeper. Keeper status was clean before and after all checks.

## Suite discovery and reviewer recipes

The exact central target remains
`ap2-m2-producer-realm-physical-path-diagnosis-0538`. The old 0626 suite
entries were not edited. The final custody hash is
`4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f`.

The generated literal suite entries are:

```text
app ap2-m2-producer-startup-shell-contract-repair-0647-preflight test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh | cut -d' ' -f1)" = 4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh preflight
app ap2-m2-producer-startup-shell-contract-repair-0647-startup test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh | cut -d' ' -f1)" = 4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh startup
```

List discovery was inspected from the existing wrapper contract but not
invoked: its `list` path calls Playwright, which is outside this cheap pass.

After independent custody review, run exactly one fresh central preflight:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-startup-shell-contract-repair-0647-preflight --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

If and only if that preflight passes, run exactly one fresh central startup
smoke:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-startup-shell-contract-repair-0647-startup --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Do not run list/run/producer body, browser, Vite, build, daemon, or full
suites as part of this handoff.

## Blockers and next steps

Blocked only on the required independent custody review and central execution;
no artifact or source decision remains unresolved. The local sandbox cannot
qualify the real `tsx` ESM entry because IPC socket creation is denied. The
next reviewer should verify the final custody hash, run the one preflight, then
the one startup smoke, and confirm the keeper has no new untracked bytes.
