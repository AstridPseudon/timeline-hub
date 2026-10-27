# A-T3-proof-r4 evidence review

Date: 2026-10-27

## Verdict

**PASS for the evidence/blocker review; the proof task remains BLOCKED.** The
worker did not change product code or proof assertions, exercised the merged
proof checks directly, distinguished direct evidence from the central Node 22
failure, and stated the missing owner inputs precisely. This is not an
end-to-end render qualification: the required owner sandbox and custom-pack
snapshot were unavailable.

## Branch and change review

Compared `tl/A-T3-proof-r4` (`832eb8b55a`) with `tl/zoom-integration`
(`b9b60c6eb3`): the only changed path is `evidence/report.md`, added as
worker evidence. There is no product-code or test-source diff. Consequently,
no assertions were removed, weakened, skipped, or marked `xfail`; no product
implementation was changed.

`git diff --check tl/zoom-integration..tl/A-T3-proof-r4` was clean after this
report was written.

## Proof-test evidence

The worker's direct Node 20.19.4 run used a private `/tmp` overlay and
reported **27 passed in 40.19s**. Its command covered the placement test and
`tests/packs/rendering/test_pinned_project_elements.py`, including:

- placement on an occurrence/shot clip that began with built-in
  `clipType: am-discord`;
- two admitted revisions selected by full revision and dispatched with their
  distinct assets; and
- missing/corrupt retained snapshots failing closed without catalog fallback.

The required central request was also run exactly once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  A-review-T3-proof-r4 targeted --files \
  "tests/packs/rendering/test_pinned_project_elements.py tests/packs/rendering/pinned_project_elements.mjs"
```

Result: `A-review-T3-proof-r4-targeted-1027000521-8928`, **failed exit 1**;
**18 passed, 1 failed in 52.01s**. The one failure was
`test_two_revisions_keep_source_dispatch_aliases_and_assets`; the central
service used Node 22.22.0 and failed before the assertion because the JS
subprocess could not resolve `remotion/package.json`:

```text
Error: Cannot find module .../remotion/package.json
Node.js v22.22.0
```

This is a dependency/toolchain failure, not evidence that the proof assertion
failed. The central result is consistent with the worker's direct Node 20
evidence, which passed the same path using its private overlay.

## Blocker and scope compliance

The worker precisely identified the unavailable owner-approved sandbox copy of
project `almost-ready`, timeline `almost-ready-no-first-second-v2`, including
shot clip `c02-02-am-discord`. It also identified the unavailable admitted
smooth-zoom project-pack snapshot/source: only the abbreviated revision prefix
`sha256:1b1e3523...` was known; the full digest, `elementRef`, and Runtime pin
were unavailable.

No substitute source or render was used. Therefore no real child/browser/MP4
export, local Vite still capture, elementRef/pin result, or pixel comparison
was claimed. That is the correct fail-closed outcome for the missing owner
inputs.

The required full suite, real render, and browser were not run. The worker
evidence directory totals 2.7 MB; the largest file is a 2.6 MB run log, and
there are no large fixtures, snapshots, MP4s, or still artifacts.

## Next step

Provide the owner-approved sandbox and the full admitted smooth-zoom
project-pack revision/digest, then rerun placement, real export, local-Vite
parity captures, and pixel comparisons. Re-run the central pinned-project
target after the Node 22/Remotion dependency setup is repaired or the service
uses the approved Node 20 overlay.
