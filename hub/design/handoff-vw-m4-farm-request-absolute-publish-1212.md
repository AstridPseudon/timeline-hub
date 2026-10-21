# Farm request absolute publication handoff 1212

Published the exact document bytes from Composition worker branch
`tl/vw-m3-gate6-farm-ready-packet-1209`, commit `b242d54d416a57a58a71fa7bed152abac9784abb`:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-viewing-gate6-1209.md`

The published file compares byte-for-byte with
`b242d54d4:design/run-on-farm-viewing-gate6-1209.md`; its Git blob is
`d747e1acc7e280e59e628bfc64ecdf260e0eba46` and its SHA-256 is
`54e53f11b55d543c77035e88b4a33f9e05a4ef613a22cc7d085b46d93604a5b9`.

## Inspection

The current document contains the complete required material:

- five immutable source identities, each with hub ref, commit, and tree (App,
  Agent/sdk, Runtime server, Runtime producer/client artifacts, Composition);
- all four frozen R4 provenance refs with commit and tree;
- the complete `env -i` child invocation, including the named path bindings,
  exact App source/tree environment values, and toolchain settings;
- the exact ordered `run.sh --preflight` and physical `run.sh` commands;
- the five required physical bodies and the single blocker list.

The flat transport worker 1210 input is at this real path:

`/home/user/work/wt/vw-m3-gate6-farm-transport-1210/design/`

Its packet files use the `handoff-vw-gate6-farm-1210-` prefix, with the request
at `handoff-vw-gate6-farm-1210-REQUEST.md`. The 1210 worker has not changed the
1209 document and its files remain uncommitted in that worktree.

## Missing prerequisites reported by the current document

The document remains `Status: HOLD`. It identifies these prerequisites as
missing or unverified:

1. A fresh manager grant note naming the transported 1153 packet, unchanged
   1054 stage, and fresh marker path.
2. Complete independent transport of the 1054 sibling source graph and the
   separate b70 helper carrier; a flat Remotion copy, shared node_modules, or
   cross-source hardlink is refused.
3. Central preflight and the one authorized physical final gate remain
   unverified.

The fresh grant is not treated here as a source-merge condition; farm-phase
authorization remains with the manager. No grant, marker, test, browser,
Runtime, socket, render, or physical run was requested or performed. No
repo-local Composition design file was added.

## Verification commands

- `cmp -s /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-viewing-gate6-1209.md <(git show b242d54d4:design/run-on-farm-viewing-gate6-1209.md)` — PASS.
- `git hash-object /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-viewing-gate6-1209.md` — PASS; blob matches `d747e1acc7e280e59e628bfc64ecdf260e0eba46`.
- `git status --short --branch` in the assigned Composition worktree — PASS; clean, no source edits.
