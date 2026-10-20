# App2 parent snapshot tree guard candidate

## Result

Updated only the App-owned current013 private integration guard and its focused
test. App snapshots now accept the test service's synthetic commit HEAD when
the existing `TIMELINE_CURRENT013_APP_TREE` metadata exactly matches
`HEAD^{tree}` and the App source is clean. The observed synthetic HEAD is
retained in the returned source report. Agent, Runtime, and Runtime-producer
HEAD checks remain exact real-SHA checks.

Changed paths:

- `scripts/testing/current013-integration.mjs`
- `scripts/testing/current013-integration.test.mjs`

The pure `assertAppSnapshotIdentity` guard refuses a changed tree, dirty
source, or malformed App HEAD. Existing absolute path, venv, cache/build,
vendor, artifact, manifest, metadata, lock, and postflight checks are
unchanged. No product code, `bin/test-run`, shared dependency, or evidence
cleanup path was changed.

## Tests

```sh
node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs
```

Result: **16 passed, 0 failed, 0 skipped**. This includes same-tree synthetic
HEAD acceptance plus changed-tree and dirty-source refusal, existing source
custody controls, and the unchanged launcher/vendor failure controls.

```sh
node --check scripts/testing/current013-integration.mjs
node --check scripts/testing/current013-integration.test.mjs
git diff --check
```

All passed.

No request-test, browser, socket, localhost, full suite, build, dependency
installation, or central gate was run, per the brief.

## Decision and later gate

The existing test-service App tree metadata is the sole expected App identity;
no new public field or ancestry/any-HEAD fallback was added. App HEAD is
reported as observed snapshot evidence only after the exact tree and clean
source checks pass.

After independent guard review and private driver registration/update, the
single later gate request is:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-snapshot-tree-guard-source ap2-m2-parent-retained-evidence-real-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

This worker did not execute it. The registered private driver must point at
this tree/clean App guard before that one request; its Runtime/Agent producer
pins, cache prerequisite, absolute paths, and evidence copy-before-cleanup
remain required.

## Blockers / next steps

No implementation blocker. Independent guard review is next. The later central
result remains unverified until the manager updates the private retained-
evidence driver and runs the one authorized gate.
