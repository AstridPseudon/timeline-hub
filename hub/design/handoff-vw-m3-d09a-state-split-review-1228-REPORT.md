# vw-m3-d09a-state-split-review-1228

## Verdict

**REQUEST CHANGES** on `8aeba6ac401487a45688789337d9aee7797d420e`.

## Exact counterexample

The qualified public path regressed in `builtin.py`:

- `tl/integration` used `_public_crop(public["rect"], ...)` when the exact
  public source/clip/frame evidence qualified, and called `model.mouth_box`
  only when public evidence did not qualify.
- The author patch removes `_public_crop` and unconditionally calls
  `model.mouth_box(presenter, 0)` at the pixel-check path (author line 527).
- The direct selected-cut test changed its original
  `mouth_box`-must-not-be-called tripwire into an assertion that the private
  crop is called. This weakens/reverses an existing positive requirement.

An isolated old/new assertion supplied qualified public motion states, made
`model.mouth_state` and `model.mouth_box` fail if consulted, and ran the same
`render_lipsync` call:

- `tl/integration`: passed (`qualified public state accepted without private
  state or crop`).
- Author branch archive: failed at `builtin.py:527` with
  `AssertionError: private mouth_box called on qualified public evidence`.

Minimal correction: preserve the active public crop for a qualified public
ROI; use `model.mouth_box` only for the already-existing fallback cases,
including public semantic motion with no public ROI. Restore the original
private-crop tripwire rather than changing it to require the regression.
Keep the new public semantic-state path and its explicit-invalid/null/missing
fallback behavior.

## Changed-hunk review

The state split itself is directionally correct in the reviewed hunk:

- exact frame, source/clip address, basis, evidence mode, and public
  `diagnostics.motion.mouth` checks remain guarded;
- `0.0` still maps to `closed`;
- explicit invalid/null `params.mouth`, stale/forged/partial rows, and missing
  rows still fail closed to private semantic fallback;
- the original aggregate/statistic assertions, strict `> 2%` threshold, and
  `799` denominator were not converted or weakened.

The requested correction must not alter those rules or add public fields,
geometry capability, API, pin, or activation changes.

## Evidence

- `git diff --stat refs/heads/tl/integration refs/heads/tl/vw-m3-d09a-pixel-state-public-split-1226` — only `builtin.py` and the direct aggregate test changed.
- `git diff --check refs/heads/tl/integration refs/heads/tl/vw-m3-d09a-pixel-state-public-split-1226` — passed.
- Isolated old/new direct assertion described above — old passed; author branch failed with the exact counterexample.
- Author report claims the targeted suites passed: aggregate `28 passed`; motion/crop neighbors `9 passed, 33 deselected`. These were not treated as approval because the changed test now requires the private crop on the qualified path.
- No full, browser, install, or central suite was run.

No product files were modified by this review.
