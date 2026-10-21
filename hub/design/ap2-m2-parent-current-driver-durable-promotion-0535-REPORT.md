# AP2 M2 parent current-driver durable promotion 0535

## Result

Promoted the already-existing current parent source driver to one new
worker-owned durable artifact. No App product/source/test/body/helper/source
keeper change was made. The existing 0508 gate was copied and changed only in
its `DRIVER` path and `DRIVER_SHA` binding.

The original durable artifacts remain immutable:

- Original driver: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`
- Original 0508 gate: `2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`

## Final artifacts and source tuple

- New driver: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh`
  - SHA-256: `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`
  - Git blob: `c0c185090c8511060694d7a4d0e0d815ca50a719`
  - Byte-identical to `HEAD:tests/e2e/local/support/run-parent-manual-drop-evidence.sh` in keeper `a304dce02a185a4774ff5144d5aa451c9702aa46f`.
- New gate: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh`
  - SHA-256: `2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546`
  - Delta from 0508: only `DRIVER` and `DRIVER_SHA`.
- Captured service tree: `a3c82aa91f1336b86491191acf857d88c56179b2`.
- Protected keeper: HEAD `a304dce02a185a4774ff5144d5aa451c9702aa46f`, clean, `KEEP` present.
- Helper unchanged: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
- Existing evidence/source pins, root, selector, timeout, authority, and guards are unchanged.

## Suite registration

Added exactly two new rows to `scratchpad/orch/tests/suites.conf`:

```text
app ap2-m2-parent-current-driver-durable-promotion-0535-preflight <literal gate SHA check> <literal driver SHA check> env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh <new gate> preflight
app ap2-m2-parent-current-driver-durable-promotion-0535-actual <literal gate SHA check> <literal driver SHA check> env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh <new gate> run
```

The actual row explicitly forwards `NORMAL014_USE_BASE_PYTHON=1`. No old row,
caller, selector, or source artifact was changed.

## Verification

Independent checks before central submission:

```text
sh -n <new driver>                         PASS
sh -n <new gate>                           PASS
git show HEAD:<source driver> | cmp ...    PASS
diff old-0508-gate new-gate                 only DRIVER/DRIVER_SHA lines
git diff --check                            PASS
```

Existing 0526 real-branch controls, using private temporary build and
Playwright stubs and the real driver/setup path:

- Positive setup, exact source/artifact/graph/vendor-lock checks, one-test
  listing, build boundary, child dispatch, required-case verification, and
  evidence retention: exit `0`, `runner_status=0`.
- Stubbed child failure: exit `73`, `runner_status=73`, stderr retained in
  `runner-tail.log`, and the status propagated.
- Driver probe: zero-test output refused and failure-trap evidence retention
  passed.
- Refusals: unknown mode exit `2`; wrong driver digest exit `1`; wrong root
  exit `1`.

No credential-bearing xtrace or secret output was used. Private temporary
records and stubs were removed; shared node modules, runtime graphs, and
venvs were read-only.

One initial diagnostic attempt used non-executable temporary stubs and thus
ran a real Vite build in a disposable `/tmp` overlay before the child reached
its known port refusal. It produced no App/source/shared-dependency change,
was not used as evidence, and was followed by the corrected stubbed controls
above. No browser or mounted actual ran.

Required one source-only central preflight, after the corrected offline pass:

```text
request: ap2-m2-parent-current-driver-durable-promotion-0535-preflight --no-cache
result: ap2-m2-parent-current-driver-durable-promotion-0535-ap2-m2-parent-current-driver-durable-promotion-0535-preflight-1021054051-11866
status: PASS, exit 0, 9s
```

Central output verified the captured tree, keeper HEAD/tree/clean/KEEP,
helper and new driver hashes, 76 artifacts, manifest/schema pins, the
parent-media source preflight, and exact collection:
`three-products.spec.ts:1440`, `Total: 1 test in 1 file`.

Central retained refusal controls passed for wrong captured tree, wrong
keeper, wrong helper hash, and wrong argv. No actual suite, browser, live
socket, full suite, dependency install, or product qualification was run.

## Live callers and next step

Live product callers remain unchanged:

```text
onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
existing commit-session/outbox path
```

The mounted parent behavior remains unqualified. The orchestrator may decide
whether to authorize one future actual using the new hash-pinned rows; this
worker did not request or run it.
