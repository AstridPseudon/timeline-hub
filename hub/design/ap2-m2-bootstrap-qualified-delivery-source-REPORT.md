# AP2-M2 bootstrap qualified delivery source

## Result

The custody-approved bootstrap-only source delta is delivered on latest HOME
`ce6deafa3` (the current `hub/tl/integration` base). The exact reviewed donor
patch from `e9d04f4bf0b9c06d184541655f20a4ca832d0370` to
`hub/tl/ap2-m2-bootstrap-only-current-home-port` was applied without changing
current settings authority, ShotEditor, shotSet, or harness paths.

The resulting worktree is byte-identical to the approved source on all 16
reviewed paths and has no other changed or untracked paths. The custody review
approval remains the source of truth; no independent audit or behavior change
was added here.

## Correction: delivery is source-only and public activation is held

The earlier custody wording must not be read as “no public activation
change.” The delivered source is the `b69c85ea7` App delta, and its live
`createDefaultTimeline` path calls
`RuntimeDataProvider.initializeNativeBootstrapTimeline`. The live product
callers are `useProjectCRUD.ts:154`, `VideoEditorPage.tsx:461`
(`ensureProjectHasTimeline`) and `VideoEditorPage.tsx:551`
(`createCanonicalTimeline`); the provider path then calls
`AstridRuntimeClient.createTimeline` and emits `timeline.init@1` plus
`track.create@1`.

That is incompatible with the exact pinned public013 Runtime: contract
`0.2.13`, producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, schema
`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
whose edit-command schema has `track.create` but no `timeline.init`.
HOME owns the revert. This source delivery is therefore **HELD** for public
use until matched Main014 Agent/Runtime/App adoption and real create/init/
restart proof. A private202 overlay test is separate private evidence and
cannot establish public readiness.

## Verification

- Targeted Vitest: 4 files, 128 tests passed.
- Timeline scope test: 1 passed.
- Focused ESLint: passed with `--report-unused-disable-directives --max-warnings 0`.
- `npm run typecheck:strict-islands`: passed.
- Bootstrap parity fixture: 12 passed; one pre-existing unknown-mark warning.
- Bootstrap Playwright `--list`: exactly 1 matching test listed; no browser run.
- `git diff --check`, exact 16-path source comparison, and scope comparison passed.

No hosted build, browser execution, localhost/live socket, central
`request-test`, or full suite was run. The post-build-repair native gate remains
for the orchestrator after the removed fallback setup is repaired.

The required merge-forward attempt failed before any merge because the sandbox
Git metadata is read-only: it could not create
`/home/user/banodoco/reigh-app/.git/worktrees/ap2-m2-bootstrap-qualified-delivery-source/ORIG_HEAD.lock`.
