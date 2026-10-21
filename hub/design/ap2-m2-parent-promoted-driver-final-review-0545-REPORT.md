# AP2 M2 parent promoted-driver final review 0545

## Verdict

**APPROVE** the exact final durable actual suite row below, limited to the
0535 driver promotion and literal binding. This review does not replay or
replace the original source/body review or the 0526 first-cause diagnosis.

## Final pinned tuple

- Frozen keeper: `/home/user/work/wt/ap2-m2-parent-complete-current-proof-source-0455`
- Keeper HEAD: `a304dce02a185a4774ff5144d5aa451c9702aa46f` (40 hex; clean; `KEEP` present)
- Keeper tree: `a3c82aa91f1336b86491191acf857d88c56179b2`
- Frozen source: `HEAD:tests/e2e/local/support/run-parent-manual-drop-evidence.sh`
- Promoted durable driver: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh`
- Driver SHA-256: `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`
- Helper SHA-256: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`
- Final gate: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh`
- Final gate SHA-256: `2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546`

The promoted driver compares byte-for-byte with the frozen keeper source.
The final gate compares with the 0508 gate at SHA-256
`2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`; its
only changes are the `DRIVER` path and `DRIVER_SHA` binding. The 0535 prose
typo that prints four extra hexadecimal characters does not alter any
executable or binding; the keeper attribution above is the correct 40-hex
identity.

## Approval command

The registered central row is:

```text
app ap2-m2-parent-current-driver-durable-promotion-0535-actual test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh' | cut -d' ' -f1)" = '2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh run
```

The explicit `NORMAL014_USE_BASE_PYTHON=1` is present on the actual row.
The preflight row has the same literal gate/driver hash checks and environment,
with `preflight` in place of `run`; central result
`...-preflight-1021054051-11866` passed, exit 0 in 9 seconds.

## Evidence reviewed

- The corrected offline real-run branch passed positive setup and source,
  artifact, graph/vendor-lock, one-test collection, build-boundary, child
  dispatch, required-case, and evidence-retention controls with exit 0 and
  `runner_status=0`.
- The planted child exit 73 was retained and propagated as 73.
- Zero-test output was refused and failure-trap evidence was retained before
  disposable-root cleanup.
- Wrong captured tree, wrong keeper, wrong helper hash, wrong driver hash,
  wrong root, wrong argv, and unknown mode were refused.
- The central 11866 preflight verified the captured tree, keeper HEAD/tree/
  clean/KEEP, helper and promoted-driver hashes, 76 artifacts and
  manifest/schema pins. Its Playwright listing was exactly:
  `three-products.spec.ts:1440`, `Total: 1 test in 1 file`.
- The protected keeper resolves `node_modules` to the existing shared App
  install. No shared dependency, source, artifact, or keeper mutation was
  made by this review.

## Scope and remaining qualification

The live product caller chain remains unchanged:

```text
onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts
-> useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip
-> existing commit-session/outbox path
```

No App source/body/assertion/helper change is approved here. The actual
mounted browser journey, localhost/live sockets, build, install, and full
suite were not run by this review or by 0535. The only remaining action for
this gate is the one central invocation of the exact hash-pinned actual row
above; its result must determine mounted qualification. Do not silently
substitute the stale `40c7...` driver or the old `2fe1...` gate.

## Review checks

```text
sha256sum <promoted-driver>                         PASS 34ee03...17a2d2
git -C <keeper> show HEAD:<source> | cmp <driver>   PASS byte-identical
diff -u <0508-gate> <final-gate>                   PASS only DRIVER/DRIVER_SHA
sha256sum <helper>                                 PASS af83e8...85fa4
sh -n <promoted-driver>                            PASS (0535)
sh -n <final-gate>                                 PASS
git -C <keeper> rev-parse HEAD/tree/status         PASS a304/a3c/clean
```

No App test suite was run because this was a read-only final binding review;
no product change was made. No blocker remains for the exact central actual.

