# VW-D09b/c partial-crop retention process-custody review 0918

## Absolute verdict

**APPROVE — changed retention/cleanup seam only.** The 0916 final report and
patch are present. The packet safely preserves the partial physical result
before private scratch cleanup and serializes only values already computed by
the partial test. The partial physical capture itself remains **NOT RUN**;
this is not a pixel qualification.

The 0901 approval of the unchanged fixture was read. This review does not
repeat the unchanged physical assertions or perform a review-of-review.

## Scope decision

The only source change is the final three-line JSON print in
`tests/packs/rendering/presenter_crop_capture.py` after all partial assertions.
The future command collects two tests and executes only
`test_actual_registered_presenter_partial_crop_pixels`. It retains the four
PNG frames and `inspection.json`, validates the compact comparison JSON,
checks source/destination custody, then removes only its own `/tmp` scratch.

The pure retention control passed for foreign, symlink-leaf, and
symlink-ancestor destinations. Realpath checks passed for the worker/result
ancestry. Existing evidence confirms all explicit799/partial697
natural/threshold/padding/mismatch/registration/source/public13/Node/frame0/
cleanup assertions remain present.

## Commands and results

- `bash -n ORCH/design/handoff-vw-m3-partial-crop-raw-evidence-retention-source-0916-COMMAND` — PASS.
- `bash ORCH/design/handoff-vw-m3-partial-crop-raw-evidence-retention-source-0916-COMMAND --retention-control` — PASS.
- Literal worker/result ancestry `realpath` checks — PASS.
- Source diff inspection and `git diff --check` — PASS.
- Reused 0916 evidence: pure `10 passed`, staging `3 passed`, collection `2`;
  Ruff passed.

No browser/helper/renderer/socket/central/Runtime/Node-host/full/install or
physical command was run.

## Exact hashes

Source packet:

```text
38abb1a8854a97473f01dd2886bf805945200f9cc45bd6c61d2e17233c2be49f  presenter_crop_capture.mjs
791bad8f50398c32e4f81798afa40b1f356db3cd61ac134b882294fcfdffd653  presenter_crop_capture.py
5223ef4ecf007124920773bef10a9f543749cd07c943e5143720837f18e29947  presenter_crop_entry.mjs
2419620a92c9972c1a7e4bd5a3b79790631ced2661227cc9420b6977946957b1  test_presenter_crop_equivalence.py
```

Custody packet:

```text
e8b583001610ae576d75cf6217f0fed0db675fd84c8d61deaab16f1887cd7cb4  0916-COMMAND
b0dd8767c69cd5cde32822a38d4a6052bcfe1f60829c454abf16e88ef145560b  0916-PATCH
86be256cc298c10c9d5ae41a0242615a785a2d3264ea52a20a32b48df4c8f5a4  0916-REPORT.md
866baff23faeac8aadbe013decb201a50ff7f1657f384c7b16dbc2c49cd728dd  0916-ASSERTION-MAP.md
ceb5bc44970ac28d25e0ac5437ed9bd8207d052dec8f91f6a5ac9d5c990650ee  0916-HASH
```

Environment pins retained from the approved packet: public13
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
Node20.19.4 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`,
Chromium1194 `63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4`.

## Next step

Register and execute the exact 0916 runner once under the normal central grant
and browser lock. Preserve its `results` directory as the raw-evidence packet.
