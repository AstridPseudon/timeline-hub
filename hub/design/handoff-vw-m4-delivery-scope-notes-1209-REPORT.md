# vw-m4-delivery-scope-notes-1209

Updated the existing Composition architecture/build/delivery page only:
`/home/user/work/wt/vw-m4-delivery-scope-notes-1209/README.md`.
No new architecture page, source/runtime copy, test, package payload, scanner
artifact, or instructions payload was created or changed.

## Documentation changes

- Updated the page from historical Composition 0.0.13 wording to qualified
  0.0.14: source `df7b86308902fae90eda1dc3080d17d8fc30ea78`, tree
  `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`, archive SHA-256
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`,
  80 regular members, and the exact package-smoke integrity.
- Named the public evaluator sources and legitimate Composition/Agent/App host
  adapters explicitly. The page keeps one evaluator and does not describe
  host adapters as duplicate evaluators.
- Documented the existing normal Main imported-theme route:
  `media.import_file`/CAS descriptor -> `inputs.theme` -> GenericHost
  `theme.json` -> existing resolver -> Root props, with source paths for the
  GenericHost, resolver, App theme authority, and render payload assembly.
- Recorded the exact release14 duration signature from
  `typescript/src/lib/duration.ts`.
- Recorded owner-film crop/geometry triage as deferred solely for heavy proof,
  retaining the private fallback, statistics, strict thresholds, 697 vs 799
  non-equivalence, 16/697 vs 16/799 crossings, and the 387-pixel erase control.
  `InspectionMouth` is explicitly not in 0.0.14.
- Kept physical Gate6 open and listed the five comparison obligations as
  unrun after the latest attempt failed before any comparison body (0 executed,
  5 not run, no media). Agent/App 0.0.14 adoption, route journeys, ZIP
  application, and owner-film viewing remain unclaimed.
- Explicitly stated that Scanner108 payload `204a` and `instructions969` are
  immutable and not edited by this documentation change.

## Verification run by this worker

From `/home/user/work/wt/vw-m4-delivery-scope-notes-1209`:

```sh
set -eu
ARCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz
test "$(realpath -e "$ARCH")" = "$ARCH"
test "$(sha256sum "$ARCH" | awk '{print $1}')" = 21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e
test "$(tar -tzf "$ARCH" | awk '!/\/$/{n++} END{print n+0}')" = 80
test "$(node -p "require('./package.json').version")" = 0.0.14
rg -q 'export \{prepareScene, querySceneFrame.*querySceneOcclusion\}' typescript/src/evaluation.ts
rg -q 'getTimelineDurationInFrames = <T extends Pick<TimelineConfig, '\''clips'\''>' typescript/src/lib/duration.ts
git diff --check
```

Result: all checks passed (`archive=PASS`, `package-version=PASS`, public
evaluator source `PASS`, duration signature source `PASS`, `git diff --check`
`PASS`). No repository test suite was run because this is documentation-only.

## Source evidence and exact unrun logs

- Release14 qualification: `design/release14-qualified-handoff.md` and
  `design/handoff-vw-release14-package-smoke-summary.txt`.
- Main imported-theme proof: `design/vw-m3-theme-terminal-home-proof-handoff-0918-REPORT.md`;
  central log
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747/log.txt`.
- Scope ruling and crop triage: `design/orchestrator-scope-triage-20261021T1147Z.md`,
  `design/handoff-vw-m4-scope-triage-ledger-1209-REPORT.md`, and
  `design/handoff-vw-m3-d09bc-one-partial-crop-proof-source-0849-REPORT.md`.
- Scanner108 immutable review: `design/handoff-vw-m4-scanner108-codec-repair-1.0.8-REPORT.md`
  and `design/handoff-vw-m4-scanner108-independent-gate-REPORT.md`.
- Latest Gate6 physical attempt (FAIL before bodies): summary and log under
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-canonical1140-sole-executor-1145-full-e2e-viewing-canonical1140-physical-1145-1021114631-32323/`.
- Held farm packet for the next authorized Gate6 run:
  `design/handoff-vw-m3-gate6-farm-ready-packet-1209-REPORT.md` and
  `design/run-on-farm-viewing-gate6-1209.md`.

No build output or temporary files were created in the worktree.
