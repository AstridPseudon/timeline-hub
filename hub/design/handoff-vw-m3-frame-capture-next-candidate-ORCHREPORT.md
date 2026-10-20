# Next native frame candidate — prepared, no run grant

Read `PLAN.md`, the native-frame-zero-triage report, and the original combined
candidate report/controller. Prepared the next diagnostic candidate from the
bounded Close-button/backdrop-detached capture fix on App
`7989ee28242c866fe8ea34f28e2e116faeaa0d86` (tree
`5f8d7059ebc8d2422a85f53b675f316fd83ce147`). No browser, render, socket, central
test-service, full suite, install, network request, or actual candidate run was
started or requested.

## Frozen candidate

- Fixture/config/profile remain `normal-profile-native1920`,
  `playwright.viewing-parity.normal-profile-native1920.config.ts`, and
  `native-codec-chrome155`.
- Original640/default analog collection remains unchanged and still lists the
  same four shared cases. The named native1920/Chrome155 collection also lists
  exactly those four cases.
- The controller now uses one-shot identity
  `vw-m3-frame-capture-next-candidate-20261020`, requires the final-clean App
  SHA/tree above, and retains the source, peer, six target-hash, browser,
  export-browser, Playwright, full shared Composition graph, `.git`
  device/inode/content, source-directory device/inode, finally/postflight,
  flock, and QUIET guards from the original controller.
- Frozen environment is Node `v20.19.4`, Chrome `155.0.8059.84`, full Chrome
  directory 255 files, export headless-shell1194 directory 12 files, and
  Playwright directory 106 files. The source preflight confirms clean Agent
  `b70b9d569b2c80885d72734c61cd57e64c3715a8`, Runtime
  `9f9b25c000485e919f30f1411831fe2d5a3c1316`, Composition
  `ff0536bb53d84db5008b859be304b932b1dd5252`, and Remotion
  `f8164bef73215272562c4d6974acadbd82c2898a` peers, including the six
  Remotion/Player target hashes per consumer and both 77-file Composition
  installs.
- App content freeze is 5,959 files,
  `47f87b3686d594899233865f96ed55785c378c54a59eb735996c26332c658717`.
- No `READY_GRANTED__*` or `RUN_STARTED__*` marker exists in this worker
  directory. The manager must create a new grant only after final-SHA review.

## Capture fix review and red conditions

The actual fix closes the named `Rendered film` dialog through its normal
`Close` button, waits for the dialog to detach, waits for
`[data-dialog-backdrop]` to detach, then performs the existing Player-ref
seek/readiness/native capture. It does not alter authored pixels, fixture media,
the evaluator, comparator, thresholds, or capture dimensions. The four direct
capture-preparation tests cover normal dismissal, fixture-only capture,
close failure, and lingering-backdrop refusal.

The prior central result remains diagnostic only: 2 PASS / 2 FAIL, with the
failed positive and negative baselines caused by the retained modal/backdrop
capture. This candidate has not rerun it. The separate Agent/App theme
background divergence remains strict RED and is intentionally not patched;
theme, fixture, comparator, and thresholds are untouched. No parity, PCM,
Gate 6, current-tuple, public10/public11, or M3 qualification is claimed.

## Direct evidence

All commands ran from `/home/user/work/wt/vw-m3-frame-capture-next-candidate`:

```text
node --import tsx tests/e2e/timeline/viewing-parity/frames.test.ts       PASS 4/4
node --import tsx tests/e2e/timeline/viewing-parity/canvas.test.ts       PASS 8/8
node --import tsx tests/e2e/timeline/viewing-parity/compare.test.ts      PASS 3/3
node --import tsx tests/e2e/timeline/viewing-parity/diagnostics.test.ts  PASS 141/141
node --import tsx tests/e2e/timeline/viewing-parity/harness.test.ts      PASS 5/5
eslint ...scoped parity/config/spec paths... --max-warnings 0            PASS
playwright ...config.ts --list (original640)                            PASS, 4 collected
playwright ...normal-profile-native1920.config.ts --list                PASS, 4 collected
playwright ... --project native-codec-chrome155 --list                  PASS, 4 collected
node --check run-native-frame-parity.mjs                                  PASS
bash -n setup-native-frame-parity.sh                                      PASS
python verify-scope.py                                                    PASS
git diff --check                                                          PASS
```

The parity TypeScript check was run and remains the known pre-existing failure
at `tests/e2e/local/support/harness.ts:630` (`clips/never[]`); no changed-file
error was reported. The source preflight controller mode passed and explicitly
reported that no browser started. It verified the final App freeze and all
selected source/environment graphs.

## Handoff

Worker artifacts are in this directory. Flat copies with the
`handoff-vw-m3-frame-capture-next-candidate-` prefix are in `orch/design/`:
the report, README, controller, setup script, full candidate patch, bounded
capture patch, source freeze/preflight, and scope check. The controller and
setup script are READY-only artifacts; do not restore or invent a grant while
the manager’s final-SHA permission is pending.

Recommended next step: manager reviews the final App SHA/content freeze and
creates the unique grant only if the candidate is accepted; then the central
service may run the named four-case diagnostic under the existing flock. Keep
all failures and the theme-background RED result visible.
