# 1156 runtime child existing-env carrier custody review

## Verdict

**REQUEST CHANGES.** The 1156 packet is not ready for application. The
runtime/source-layout and immutable-destination direction is sound, but two
changed-hunk gaps allow malformed suite inputs to pass after allocation or to
produce a malformed child suite.

This is an independent review of proposal 1156 only. I read the settled plan,
the 1156 report, patch, commands, source fixture, and the prior 1149 custody
review. I did not review the unchanged 1054 stage and made no product or ORCH
kit changes.

## Required minimal fixes

1. In the new `bin/make-runtime` prerequisite hunk (patch lines 20-31 and
   62-66), validate the selected `agent remotion-0012-nodes` source row before
   creating `$D.partial`. It currently checks only that a row exists. A row
   with no `ASTRID_REMOTION_PROJECT_DIR` carrier is accepted and copied without
   one; a row with a foreign/broken carrier is also accepted and its path is
   not rewritten by the later substitutions. Require exactly one carrier token
   and an accepted legacy value (`/home/user/work/runtimes/agent-remotion-0012`
   or that path plus `/remotion`), or replace exactly one carrier token with
   the generated `$D/remotion` value. This keeps missing, foreign, broken, and
   duplicate suite inputs refused before runtime allocation.

2. In the new `bin/make-child-venv` hunk (patch lines 94-104), replace the
   presence-only `case` check with an exact-one carrier check. The current awk
   loop rewrites every carrier token, so a duplicate carrier is accepted and
   emitted twice. The supplied fixture requires exactly one carrier, but does
   not exercise the patched shell hunk. Also require exactly one
   `venv-agent-child-s2` selector before replacing it; otherwise a duplicate
   selector leaves an old selector in the generated child suite.

These are narrow validation changes in the proposed hunks; no baseline or
legacy input should be invented to work around them.

## What passed

- The supplied source-only fixture syntax check passed:

  `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-source-fixture.mjs`

- The fixture execution passed its old-flat, new-nested, missing-env,
  foreign-env, broken-env, and missing-suite-carrier assertions. Its exact
  temporary root was removed by `finally`.

- The 1156 patch dry-run and application passed in a private temporary copy of
  the two kit scripts. `bash -n` passed for both patched scripts. The private
  root was removed after the check.

- Patched-script refusal probes passed with exit status 2 for both
  `make-runtime` and `make-child-venv`; each listed the absent authoritative
  `agent-remotion-0012.env` and `agent remotion-0012-nodes` row before any
  `$D.partial`, venv, install, or source allocation.

- Read-only source inspection found the current Agent `tl/integration` nested
  imports in `remotion/src/LiveSceneClip.tsx` and the three sibling closure
  files under `astrid/packs/rendering/ui/threejs-live-editor/`. No symlink
  entries were present in the relevant current tree. The patch preserves the
  Node 20.19.4 path, lock digest check against
  `remotion/package-lock.json`, staged `$D.partial` layout, final `mv`, and
  read-only chmod behavior; no runtime was built.

- Composition worktree status was clean and `git diff --check` passed.

## Direct evidence for the request

Using the exact new child-hunk presence test with two carrier tokens prints
`ACCEPTED`, and the exact awk carry emits two carrier tokens. Using the exact
new runtime row-presence test with a suite row that has no carrier also prints
`ACCEPTED`. Therefore the two findings are changed-hunk behavior, not merely
unverified speculation.

## Explicit limits and prerequisite

The authoritative legacy inputs are currently absent:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion-0012.env`
- the `agent remotion-0012-nodes` row in
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`

This is an explicit deployment prerequisite. The review does not invent a
baseline. After the two validation fixes and deliberate restoration of the
exact legacy bytes, the lead should re-run the 1156 fixture and private
preallocation probes, then perform the separately authorized runtime/child
creation proof.

Not run by instruction: runtime build, npm/PyPI install, venv creation,
application to `bin/`, source/graph copy, browser, sockets, server, render,
physical proof, central test service, or any full suite.

## Inputs and command record

- Proposal report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-REPORT.md`
- Proposal patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156.patch`
- Fixture: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-source-fixture.mjs`
- Prior review: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-layout-1144-custody-review-1149-REPORT.md`
- Worker transcript: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-runtime-layout1156-custody-review-1209/log.txt`
