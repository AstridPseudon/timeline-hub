SOURCE READY — frozen MAIN image/cap fixture (no pixels)
 
MAIN a411628f8fd6129f9c58c332019b56769d997384; Composition6 67b8aa3d0d6831d3e3504a340ff583c3da253707. Original MAIN managed resolver / core projector / normal render prep produces hold4 from raw hold5. This is contrary to the suggested raw5 expected direction. Agent must not choose a golden from that expectation. Report and trace preserve this evidence; actual frame105 is pending the capture worker.

Every artifact below has absolute prefix:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-image-cap-source-vector-

Required flat files:
- raw-closure.json — exact synthetic parent/shot/internal records, with raw hold5 and cap4000ms.
- image.png — generated16x16 RGB240 test input, SHA256 ec19e1c7d1d247d56db54f73e6514c92a82147a1b6ab59eaa30edeebca2e82b6.
- replay.py — uses ORIGINAL MAIN's existing test transport + ORIGINAL product helpers; no copied projector/policy.
- main-source.tar.gz — frozen original MAIN source/tests and original locked6 code after MAIN registry generation; NO shared dependencies/symlinks/caches.
- locked-composition6.tar.gz — exact MAIN-lock-matching archive, 29 files.
- source-identity.json — MAIN source/component + locked/post-generation Composition member hashes.
- freeze.json — artifact hashes and 2,414 original MAIN files byte-equal after tests.
- main-projected-config.json / main-managed-registry.json / main-materialized-timeline.json / main-serialized-timeline.json.
- main-props-template.json — exact native managed input before runtime-dependent URL binding.
- main-props-static-analog.json — exact prepared props with ONLY the static-public analog file binding image-cap.png.
- trace.json / fixture-label.json / prior-proof-match.json / REPORT.md.
- targeted-main.log / generator.log / replay.log.
- prepare.py — historical producing script, not the consumer replay command.

Source archive SHA256: 6b89215fd014a062a2590c9739e39efd656effec0aefae45b6afa0db0ac4d96d.
Locked6 archive SHA256: 78746170f9c337650991dacca7a303c71be89ee5e61c25ef821390c7563df87b.
All original + generated Composition and MAIN source subset hashes match the existing qualified90PNG proof; that was a DIFFERENT film.

Consumer offline replay commands (run ONLY in YOUR OWN real directory; no shared links/parents):
 
```sh
W=/absolute/path/to/YOUR/worker-folder
S="$W/main-image-cap-source"
F=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-image-cap-source-vector-
mkdir "$S"
tar -xzf "${F}main-source.tar.gz" -C "$S"
P="$W/replayed-image-cap-"
cp "${F}raw-closure.json" "${P}raw-closure.json"
cp "${F}image.png" "${P}image.png"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "${F}replay.py" "$P"
cmp "${P}main-projected-config.json" "${F}main-projected-config.json"
cmp "${P}main-serialized-timeline.json" "${F}main-serialized-timeline.json"
cmp "${P}main-props-static-analog.json" "${F}main-props-static-analog.json"
cp "${F}image.png" "$S/remotion/public/image-cap.png"
```

The original MAIN Root is "$S/remotion/src/Root.tsx", entry "$S/remotion/src/index.ts"; normal composition ID TimelineComposition. Use the frozen generated maps already in "$S/remotion/node_modules/@banodoco/timeline-composition/typescript/src"; bind six preflight-qualified peers using OWN REAL scope directories / leaf links. Do not replace the existing private Composition directory or link through any shared scope. The original webpack aliases are "$S/remotion/webpack-alias.mjs". Attach exact "${P}main-props-static-analog.json" to the approved static-public analog capture, explicitly labelled; or resolve the managed template through the REAL InvocationAssetServer in the capture lifetime and verify ONLY file URL binding differs.

Do not feed manually assembled clamped props as the source proof: replay raw-closure first and require byte-equal outputs above. No full normal task/admission/execute route was run here; exact pure prep and real managed-byte materialization were run. Static URL resolver is explicitly an analog, not a live Runtime/server claim. No timestamp/file digest purports to grant capture.

MAIN source predicts metadata1920x1080 / fps30 / duration120; frames90,105,119 are valid. Source predicts media opacity1,0.5,1/30 from the unchanged locked6 fade hook; these are inference only, NOT a new asserted visual golden. Frame120 is outside metadata; do not seek-clamp an excluded-end test. Capture worker owns normal Root metadata verification, actual PNGs and opacity measurement. Follow its central grant + six-peer/source prepost + >=10GiB disk preflight. This SOURCE READY does not waive those conditions. No local/browser/render/socket command is included or authorized by this fixture.

Original targeted MAIN files: 66 passed in5.86s. No full suite, local render/browser, sockets, install, network, git mutation, product edits, rewritten behavior tests or shared dependency writes.
