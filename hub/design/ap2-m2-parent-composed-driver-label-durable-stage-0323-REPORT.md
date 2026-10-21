# Parent composed driver label and durable stage

## Result

Completed the final delivery-only correction. The reviewed driver from
`45fbfc867` is unchanged in executable behavior; line 51 now labels the
`895c...` digest as the private dependency-graph archive instead of calling it
the public Composition archive:

```text
- public13_archive_sha=sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
+ private_dependency_graph_archive_sha=sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
```

The official immutable Composition 0.0.13 archive remains `9412ae25...` in
the unchanged shared source helper. Both digest values are unchanged. A search
found no reader of the old evidence key, so this is a human-label correction,
not a semantic metadata-consumer rename. No source guard, control flow,
assertion, selector, product file, or dependency was changed.

The corrected existing driver was copied byte-for-byte to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh`

It is executable, 10,067 bytes, and has the same SHA-256 as the worktree
driver: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`.

## Registered row

Added exactly one row at `suites.conf:107`; the previous rows at 34, 42, 105,
and 106 are unchanged:

```text
app ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh run "$PWD"
```

Row SHA-256 including its newline: `e1179d6438f3658058d0d9b6d1897bd8c19ea1a315fa8f747c52e371980096d0`.
The retained old rows hash to `c4adb58aed2169d2344895912306651b1eb5842bbb6f6cb8edacf8d757394bc3`
(line 105) and `1f3e29f4560af0b9c7afc5cba5475482790519eda1f5b92fb90256462a9a3545`
(line 106), matching their prior records.

## Identity and helper hashes

- Reviewed `45fbfc867` driver SHA-256: `038e73f7b903b31bd073bce2c9f5e84a1beb5991c38c97620e9d920448ef9366`; Git blob `1e9235496acb53b61f51fb151e9cca7de7a38433`.
- Corrected worktree and durable driver SHA-256: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`; Git blob `c08411be9210bef91f2e3a9a731022a73e18b6fb` for the worktree copy.
- `normal014-source-common.sh`: `3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014`.
- `normal014-app-central.sh`: `8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e`.
- `normal014-parent-media-central.sh`: `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd`.
- Private dependency-graph archive: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Official Composition 0.0.13 archive: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Checks

All disposable directories used private `TMPDIR` locations and were cleaned.
The frozen product/test source remained separate from this changed driver tree:
App commit `da6d910f7ab3dfc71142ece7f632d43341238882`, tree
`6809757f93ca5e166b24b8bc0160ca09005e984a`.

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — passed.
- `sh -n <durable>/run-parent-manual-drop-evidence.sh` — passed.
- `NORMAL014_RECORD_DIR=<private> sh <durable>/run-parent-manual-drop-evidence.sh probe` — passed; the failure-trap probe retained evidence before cleaning its disposable root.
- `git diff --check` — passed; the worktree diff is exactly one added line and one removed line at driver line 51.
- Source-only preflight, using the existing shared path and the frozen source:

  ```sh
  env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 TMPDIR=<private> \
    sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh preflight \
    /home/user/work/wt/ap2-m2-parent-exact-negative-source-finish-0230
  ```

  Passed with `verified artifacts=76`, manifest
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, schema
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, the
  expected parent replacement collection marker, and the final source-tuple
  verdict.

- Actual selector collection, from a private extraction of the exact
  `da6d/tree680` source with private cache/output paths:

  ```sh
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
    --grep 'M2 real mounted manual video drop' --list
  ```

  Passed: exactly one case, `three-products.spec.ts:1440`, the manual-drop case.

- Existing source guard negative checks all refused with exit 1:
  - wrong source role: `NORMAL014_APP_SOURCE=bootstrap` against the parent source;
  - wrong pin: replaced the expected runtime-lock pin with an all-zero value;
  - missing provenance: a non-App-root path without the required package/Git source identity.

An initial preflight without `NORMAL014_USE_BASE_PYTHON=1` reached the artifact
checks but attempted the helper's default offline `jsonschema` resolution and
failed before qualification. It installed nothing and changed no shared
dependency; the established base-Python source-only path above passed.

## Scope boundary and live callers

No browser, localhost/live socket, hosted build, dependency install, central
request, full suite, or actual mounted ADD authorization was run. The driver
preflight mode itself was not invoked because its existing App-central path
performs the prohibited hosted build/browser collection; the approved
source-only path was run directly as above. The service's eventual `$PWD`
source input must remain the frozen `author0230` `da6d/tree680` snapshot.

Current suite callers are:

- `suites.conf:34` — retained relative frozen-existing-add row;
- `suites.conf:42` — separate retained-evidence durable row;
- `suites.conf:105` — relative final95 parent row;
- `suites.conf:106` — prior reviewed durable driver row;
- `suites.conf:107` — this worker's corrected durable driver row.

The product-side live path remains the reviewed parent drop route:
`onTimelineDrop` → `useExternalDrop.ts:dispatchTimelineDrop` →
`external-drop-utils.ts:handleFileDrop` → parent-media commands →
`useAssetManagement.placePreparedAsset` → native `createTimelineCommands.addClip`
→ existing commit-session/outbox path.

## Next step

The durable artifact and named row are ready for the manager's separately
authorized central run, if desired. No behavior qualification is claimed by
this delivery-only task.
