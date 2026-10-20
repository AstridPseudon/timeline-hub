# Flat handoff: native frame-0 capture audit (`1020051823-16742`)

To `vw-m3-native-frame-zero-triage`: retained offline evidence supports a capture/viewport/state artifact. It does not support a frame-0 composition, source-prop, codec, or DPR mismatch. No gate claim.

Facts:

- Actual Player PNG and independently decoded MP4 frame 0 are both 1920x1080.
- Original Player PNG SHA-256: `d47a187e3b634142486311cd21914e2375e4a0343efa32681f0fed049cc8553`. Original MP4 SHA-256: `ba653c490689847a31033babc48dba64f6322549fa2b98b12e615ea58658bbc9`. Derived MP4 frame-0 PNG SHA-256: `87f328b7f1cf96036821cd3180ae99068110e46b03f282cc5fff52b134ee8837`; derived only, originals unchanged.
- Direct RGB comparison: `2,073,545/2,073,600` pixels outside channel bound 2; max channel error 203; mean channel absolute error 72.252703.
- 8x6 regions: 47/48 have 100% pixels outside bound 2; the remaining center/lower region has 99.8727% outside. This is global contamination, not a shift/seam.
- Player PNG has solid black x=0..239 and x=1680..1919 sidebands, plus visible `Rendered film` modal/editor UI, controls, Download button, and timeline chrome. Decoded MP4 frame 0 is the clean composition gradient.
- Fixture evidence: frame 0 is a still hold; video begins at frame 120; frame-0 marker null is expected; later video marker frames pass. Retained trace records time 0, media-ready source, first-frame cover opacity 0, viewport 2000x1200, native host marker, 1920x1080 child, scale 1. The test asserted DPR 1.
- Page snapshot/source evidence shows the `Rendered film` dialog open during the diagnostic. Retained files do not prove the exact locator/overlay mechanism, nor retain a returned occlusion/bbox result.

Inference: the capture saved non-composition UI/background/sibling overlay content while the render-result UI remained open. Dimensions/readiness/DPR are weaker explanations. No browser rerun or alternate capture was performed.

Source artifacts:

- Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-capture-zero-audit/REPORT.md`
- Analysis source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-capture-zero-audit/analyze-retained.mjs`
- Numeric output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-capture-zero-audit/pixel-audit.json`
- Original files: `/tmp/viewing-native-frame-parity-2EZi8v/player-export-normal-profi-1fbe1-al-CPU-Remotion-task-output-native-codec-chrome155/viewing-parity/{player-frame-000-positive.png,final-export.mp4}`

Recommended authorized rerun diagnostics: assert/close `[data-video-editor-render-player]` before capture; retain modal presence, preview/Player bounding boxes, computed overflow/z-index, page screenshot, and element screenshot; keep the raw comparison unchanged; then run the existing magenta-overlay negative control and preserve its expected failure. Preserve null frame-0 marker semantics and use a later video-marker frame as the readiness control.

