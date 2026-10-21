# UNAPPLIED1144 runtime-layout custody review

## Verdict

**HOLD — not approved for installation/application as currently packaged.**

The corrected nested layout itself is compatible and custody-safe: a new
runtime root is `$D/remotion` plus sibling `$D/astrid`, both archived with the
same Agent SHA. The hold is caused by current ORCH integration inputs and one
real downstream caller, not by the `../../astrid` layout design.

Patch under review (not applied):

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-layout-proposal-correction-1144.patch`

Patch SHA256: `8217d5ac876d8729bba375dce91845378b5b7043fb1ec85b155d1c2cbfdbab34`

Composition base: `tl/integration` at
`df7b86308902fae90eda1dc3080d17d8fc30ea78`; Composition worktree remained
clean.

## Independent findings

- Source-only fixture passed for Agent SHA
  `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`: old flattened layout failed as
  expected; nested layout resolved `remotion/src/LiveSceneClip.tsx` through
  `astrid/packs/rendering/editor/live-scenes/SceneSurface.tsx`, then sibling
  `runtime.ts` and `diagnostics.ts`.
- The same fixture passed for current integration Agent SHA
  `1a50cf3f30398500e9f1ccf0b94d59fe7a8bdb3f`: old layout failed as expected;
  nested layout resolved through
  `astrid/packs/rendering/ui/threejs-live-editor/SceneSurface.tsx`, then its
  sibling `runtime.ts` and `diagnostics.ts`.
- Both archive scopes contain zero Git symlink entries. The two archives use
  the same `$S` argument in the proposal; no source alias, resolver rewrite,
  source factory, crawler, or shared `runtimes/astrid` destination is added.
- The proposal's new project paths agree internally: `npm ci`, lock digest,
  Remotion version reporting, generated `ASTRID_REMOTION_PROJECT_DIR`, and
  generated dependency-root references use `$D/remotion`; the source carrier
  remains `$D/astrid`.
- Existing name validation, `$D.partial` staging, cleanup-on-failure,
  `mv $T $D`, Node 20.19.4, exact lock check, normal `npm ci`, read-only
  chmod, `request-runtime`, and old runtime-name/API behavior are unchanged by
  the patch. No existing runtime or environment was modified in this review.

## Blocking current-kit facts

1. The current ORCH kit has no
   `$ORCH/tests/agent-remotion-0012.env` and zero
   `agent remotion-0012-nodes` rows in `$ORCH/tests/suites.conf`, although
   current `bin/make-runtime` still reads both. With the current files, the
   proposed script's `sed` reports a missing template and creates an empty new
   env file; its fallback `grep` finds no source row, so no new suite is
   registered. Because the script has no `set -e`, it can still reach its
   success-looking final echo. This must be repaired or explicitly replaced by
   the lead before installation; silently selecting another template would
   change the reviewed input contract.
2. `bin/make-child-venv:20` is an actual dynamic caller that substitutes
   `agent-remotion-0012` with `$RT` but does not append `/remotion`. If a new
   nested runtime is passed as `RT`, its generated child suite still binds
   `ASTRID_REMOTION_PROJECT_DIR` to `$D`, which is now the runtime container,
   not the Remotion project. Adjust that caller (or explicitly prohibit nested
   runtime names there) before using a generated child suite. Existing suites
   for immutable old runtimes must remain unchanged.

The current existing runtime
`/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b` remains an old
flat-layout API target. Its package-lock SHA is
`c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`; its
existing env file is currently empty. This review did not alter either item
and does not treat the empty env as valid evidence.

## Checks run

Passed:

- `patch --dry-run -p1` and apply in an exact private copy of current
  `bin/make-runtime`.
- `bash -n` on the patched private copy.
- `node --check` on the supplied source fixture.
- Independent `git archive` preparation plus the Node path-resolution fixture
  for both d0a and current integration; old layout failed and nested layout
  passed in both cases. The fixture removed its exact real temporary root.
- Git-tree symlink census for `remotion` and `astrid/packs/rendering` at both
  SHAs: zero symlink entries.
- Read-only contract/path inspection and synthetic sed witness: generated
  project path `/home/user/work/runtimes/$N/remotion`, dependency path
  `/home/user/work/runtimes/$N/remotion/node_modules`.
- Composition `git status --short --branch`: clean.

Not run by instruction: npm install/ci, runtime creation, graph copy, build,
browser/helper, Runtime/server/socket, central, render, physical, or full
suite proof. No repository product file was changed.

## Required lead application steps

1. Restore or deliberately re-establish the authoritative baseline env
   template and `remotion-0012-nodes` suite source row; record their exact
   bytes. If the current kit's contract has changed, revise and independently
   review the patch rather than applying this hash unchanged.
2. Fix or fence the `make-child-venv` nested-runtime caller above.
3. Apply only this reviewed `bin/make-runtime` patch, request one new unique
   runtime name with one Agent SHA and exact lock SHA, and verify the final
   root has `remotion/` and sibling `astrid/` from that same SHA.
4. Before any Gate6/physical work, verify the generated env, suite, and CLI
   all point at `$D/remotion`; verify old immutable runtime/env bytes and names
   are unchanged; and verify no shared `runtimes/astrid` path was created.

