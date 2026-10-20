# vw-m3-main-cap-capture-result-gate — FAIL

## Terminal result

The existing central result was inspected; no request was submitted or rerun.

- Result ID: `vw-m3-main-cap-controller-repair-e2e-viewing-main6-image-cap-three-stills-1020113140-6461`
- Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-main-cap-controller-repair-e2e-viewing-main6-image-cap-three-stills-1020113140-6461`
- Status: `fail`; exit `1`; elapsed `27s`
- Central command: repaired `handoff-vw-m3-main-cap-controller-repair-controller.py capture`
- Capture outputs: `0` PNGs, `0` metadata files, no actual frame result
- Pixel/golden claim: **none**

The renderer failed during webpack bundling before any Root metadata or still was produced:

```text
Module not found: Error: Can't resolve
'@banodoco/timeline-theme-2rp/src/effects/art-card/component'
```

The missing package is a real dependency-closure mismatch. The frozen MAIN generated registry imports four `@banodoco/timeline-theme-2rp` components, but the qualified physical graph used by the request contains only `@banodoco/timeline-composition` under `@banodoco`; the theme package does not exist there. The graph preflight checked and preserved its frozen identity, but did not prove the generated-registry import closure.

This is a capture graph/staging failure, not evidence that the source or renderer produced a wrong image. It does not justify changing the source vector, selecting a golden, or weakening a guard.

## Guard evidence preserved

- Approved controller SHA256: `41455095972277d6e2b8da04f7796bfb6579cb960c948f64b7fed1e5adc2fde3`
- Approved renderer SHA256: `c5be04066bfef43c76b97464f9ce1cc981ca9fc36a224bd2ffe0a078338437e4`
- Approved command SHA256: `234e79bec954b7378a761f2ad3a9c7aed3fb0c618fe5aefc6cc9fbf4e01581cf`
- Frozen MAIN: `a411628f8fd6129f9c58c332019b56769d997384`
- Frozen Composition6: `67b8aa3d0d6831d3e3504a340ff583c3da253707`
- Frozen source archive SHA256: `6b89215fd014a062a2590c9739e39efd656effec0aefae45b6afa0db0ac4d96d`
- Frozen locked Composition archive SHA256: `78746170f9c337650991dacca7a303c71be89ee5e61c25ef821390c7563df87b`
- Frozen source closure: `2,414` original MAIN files byte-equal after tests
- Frozen Composition package: `29` regular members
- Physical graph: checkout `f8164bef73215272562c4d6974acadbd82c2898a`, `21,488` entries, manifest SHA256 `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`
- Source postflight: passed; graph postflight: unchanged; postflight `valid=false` solely because the bundler command failed
- Offline raw-closure consumer replay: all seven outputs byte-equal (`byte_equal=true`)
- Source route evidence: raw `hold=5` -> projected/serialized `hold=4`; numeric `fps=30`; this is offline source/materialization evidence only
- Static-public binding: executable analog only; no live Runtime/server claim

## Pixel instrument

The independent flat instrument was not allowed to measure nonexistent frames. Its self-test passed, and the actual-file invocation failed closed on the missing frame-90 control. No resize, realignment, or PNG-alpha-as-opacity operation occurred.

```text
--self-test: exit 0
  PASS: synthetic fractions 1, 0.5, 1/30; wrong-color, uninformative-control,
  wrong-dimension, and uninformative-background controls fail closed

actual files: exit 2
  {"status":"FAIL_CLOSED","error":"missing control: .../handoff-vw-m3-main-cap-controller-repair-frame-90.png","png_alpha_is_layer_opacity":false}
```

The requested fixed ROI `(192,108,1536,864)`, source image, background basis `RGB(5,8,20)`, and frame set `(90,105,119)` therefore have no observed pixel measurements. The source prediction `(1, 0.5, 1/30)` remains context only and was not asserted.

## Recommended next step

Repair or re-qualify the private capture dependency closure so the exact generated registry imports resolve. The next attempt must preserve the frozen source/graph guards and add a preflight assertion that every generated-registry package import, including `@banodoco/timeline-theme-2rp`, exists in the staged graph. Then request a new independently reviewed central attempt; do not reuse this failed result as a pixel or golden result.

No repository/product files were changed. No browser, renderer rerun, install, socket, network, service request, shared dependency write, full suite, or git mutation was performed by this gate worker.
