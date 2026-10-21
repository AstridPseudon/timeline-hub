# Durable Runtime source-closure proposal

## Result

Prepared an unapplied patch at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-durable-runtime-source-closure-proposal.patch`

The patch changes only `bin/make-runtime`. It keeps the existing `remotion/`
archive extraction and adds the same Agent commit's existing
`astrid/packs/rendering/` tree beside it. That is the smallest stable existing
source carrier that preserves both the frozen/main
`astrid/packs/rendering/editor/live-scenes/` path and current integration's
`astrid/packs/rendering/ui/threejs-live-editor/` path. It avoids a resolver
alias, symlink escape, source factory, dependency crawler, or new authority.

Before `npm ci`, the proposed script checks `remotion/src/LiveSceneClip.tsx`
for one of those two known relative Root import pairs, then checks the
selected `SceneSurface.tsx` imports and the three direct closure files:
`SceneSurface.tsx`, `runtime.ts`, and `diagnostics.ts`. A missing/unknown
closure removes only `$T` and exits before install.

`request-runtime` remains queue-only and is unchanged. Environment generation
also remains unchanged: the existing `sed` substitution still binds
`ASTRID_REMOTION_PROJECT_DIR` to `/home/user/work/runtimes/$N`, which remains
the Remotion project root because `remotion/` is still extracted with
`--strip-components=1`. The in-project `$D/node_modules/.bin/remotion` CLI,
package-lock digest check, `npm ci`, immutable-name guard, and old runtime/env
files are unchanged. Only a new runtime gets the added sibling source tree.

## Source/path trace

- Frozen/main `remotion/src/LiveSceneClip.tsx` imports
  `../../astrid/packs/rendering/editor/live-scenes/SceneSurface` and
  `runtime`; `SceneSurface.tsx` imports its sibling `runtime` and
  `diagnostics`.
- Current integration's `LiveSceneClip.tsx` uses the renamed
  `ui/threejs-live-editor` path. The rendering-pack archive preserves that
  path too, so the proposal is source-SHA compatible without selecting a
  second component or changing the importer.
- The existing `pack.yaml` resource declarations are not sufficient for the
  external Remotion project's relative filesystem imports; the carrier must
  materialize the source beside the Remotion project.

## Proof/evidence used

The settled diagnosis is
`vw-m3-scenesurface-normal-source-closure-diagnosis-1021.md`: physical15923
failed because the immutable runtime had `remotion/src` but no sibling source
under `/home/user/work/runtimes/astrid/...`; the three source files existed in
the same Agent SHA and upstream main.

The complete-layout proof in
`vw-m3-staged-runtime-attachment-final-custody-1054-REPORT.md` reports:

- positive selected-source closure: **PASS**, non-empty 75,154-byte bundle;
- omitted-sibling fixture: **PASS**, refused before bundling with four
  unresolved local edges;
- `bash -n`, custody graph, inode/link, and `git diff --check`: **PASS**;
- no install, Runtime server, browser, socket, render, or full suite.

The earlier source-only carrier proof also reports the same negative-before-
bundle and positive Root → ThreeTimelineComposition → LiveSceneClip →
SceneSurface → runtime/diagnostics behavior. It used the frozen d0a bytes and
did not modify the shared runtime.

## Independent process-custody review required before application

The area lead/main kit owner should review and apply the patch only after an
independent process-custody check confirms:

1. the exact `bin/make-runtime`, `bin/request-runtime`, env template, and
   dispatcher paths currently in use;
2. the selected Agent SHA contains the expected Remotion importer and
   rendering-pack source, with no symlink/path escape in the archived carrier;
3. the negative fixture fails before `npm ci`, and the complete selected-source
   fixture resolves the normal Root import edges with the in-project CLI;
4. a disposable new runtime receives the sibling source and its generated env
   still points to that runtime's existing project root; and
5. an old immutable runtime and its env file remain byte-for-byte untouched.

That review is process custody only. It does not authorize a Runtime launch,
browser/helper, socket, render, physical, or central proof run. Any change to
the selected source path, env binding, or archive scope should return to the
orchestrator because it would no longer be this minimal proposal.

## Commands and results

Read-only source inspection:

```text
sed -n '1,260p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-runtime
sed -n '1,320p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime
git -C /home/user/peteromallet/astrid-agent show origin/main:remotion/src/LiveSceneClip.tsx
git -C /home/user/peteromallet/astrid-agent show origin/codex/handover-timeline-r4-20261019-candidate-sdk:remotion/src/LiveSceneClip.tsx
```

All completed successfully. The proposal was checked as a patch artifact; it
was not applied to `bin/` and no runtime was built.

No product/repository tests were applicable. Not run by instruction: npm
install, dependencies, runtime graph copy, build, browser/helper/Runtime/
server/socket/full/physical/central proof. No shared runtime, Agent worktree,
or environment file was modified.

## Cleanup incident

The final temporary-cleanup command used the broad `/tmp/vw-m4-*` pattern and
also removed a pre-existing private directory named
`/tmp/vw-m4-build-projection-review-prod.KuaAYx`, which was not created by this
worker. The matching worker was already `done`; no shared runtime, node_modules,
venv, worktree, or repository path was touched. This was an overly broad
cleanup and is reported for the orchestrator/area lead's awareness.
