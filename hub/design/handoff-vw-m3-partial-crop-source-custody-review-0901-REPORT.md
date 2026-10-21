# VW-D09b/c partial crop source custody review 0901

## Absolute verdict

**APPROVE.** The four-file packet at Agent `883833ad4c91e7764950f26b9a07a7c46a6beea4`
(tree `1da635d2e819a2c6ab9f0b4c420034a489dca792`) retains the explicit
32349 qualifier and safely adds one future partial-input case. The partial
physical test remains **NOT RUN** and no pixel qualification is claimed.

The retained explicit source is Agent `ac4e004a664b96d58a00b66c7a2fa702a191f5bd`
(tree `a36a38e234813638530d03a6916dc84768caa9dd`), using the approved public13
artifact SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` and
Node20.19.4 SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

## Retained/new map

- `presenter_crop_entry.mjs` is byte-identical retained registration: ordinary
  `TimelineComposition`, `toRuntimeTheme`, and `resolveHostRegistries`.
- `presenter_crop_capture.mjs` retains the exact browser, bundle, composition,
  four-frame, component-zero, and `finally` cleanup path. Only the mode and
  partial raw input are new; explicit remains the default.
- `presenter_crop_capture.py` retains the explicit 799/387 physical assertions
  and extracts their existing staging/process cleanup into `_capture`; the
  partial test reuses that helper and the same public query/source.
- `test_presenter_crop_equivalence.py` adds only the 14-line pure partial
  697/799/387 denominator control. No old assertion was weakened or removed.
  The old standalone partial fixture files from `ef4ebb23d` are absent, so no
  tracked fixture was duplicated.

The explicit case still asserts source/package/browser/Node/registration,
component frame 0, cleanup, PNG format/size and byte preservation, natural
positive pairs, strict `> .02`, planted 8/15/16/20 mismatches, padding16, and
the `(298,202,345,219)` 799-pixel positive against erase `(300,206,343,215)`
387 pixels. The partial case uses actual `{x:151,y:104}` props, the same
registered `am-presenter` source, same `[0,3,4,5]` frames, and the existing
public `mouth` query. It checks private `(298,202,339,219)` / 697 pixels
against the public crop's private-width subset, with natural, threshold,
padding, planted mismatch, PNG identity, frame-zero, and cleanup controls.

Default remains unqualified: private `model.mouth_box()` is `None`, public
`mouthInspectionRect()` is `null`, and `legacy_qualified` is false. No default
physical claim is introduced. Raw-invalid fallback/statistics remain live.

Custody is safe: archive extraction and all staging writes target the private
temporary project; the `@banodoco` scope is a real owned directory; borrowed
dependencies are leaf symlinks only; linked scope parents are rejected before
writes; the exact archive has no hardlink or symlink members; and fixture hash,
peer identity, process-group, browser, bundle, and temporary-project cleanup
guards remain in force. No DTO/API/pin/render/product change is present.

## Evidence

- Pure controls: **10 passed in 4.88s**.
- Capture collection: **2 collected in 0.19s**, neither physical test run.
- Ruff, Node20.19.4 syntax checks, `test_private_node_modules_staging.py`
  (**3 passed in 0.09s**), and `git diff --check`: **passed**.
- Current packet hashes:
  `presenter_crop_capture.mjs` `38abb1a8854a97473f01dd2886bf805945200f9cc45bd6c61d2e17233c2be49f`;
  `presenter_crop_capture.py` `68291e26500154b0ac2531a0b69558c5ef64d02aac10b8261f8329e036b87016`;
  `presenter_crop_entry.mjs` `5223ef4ecf007124920773bef10a9f543749cd07c943e5143720837f18e29947`;
  `test_presenter_crop_equivalence.py` `2419620a92c9972c1a7e4bd5a3b79790631ced2661227cc9420b6977946957b1`.

Not run: browser, renderer/helper capture, socket, central, Runtime, install,
full suite, or partial physical qualification.
