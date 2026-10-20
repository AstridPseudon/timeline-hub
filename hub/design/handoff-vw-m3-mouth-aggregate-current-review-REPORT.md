# Verdict: BLOCKER

The selected-cut aggregate proposal is bounded and its retained-source,
cut-selection, pixel-comparison, and denominator claims are supported. It is
not landable as written against current presenter `802669926` because its
query imports `seriesInspection` from
`tests/packs/rendering/presenter_crop_geometry.mjs`, but that exact current
file exports `eraseRegion`, `basis`, `frames`, `params`, `propsFor`, and
`inspect` only. It has no `seriesInspection` export. The proposal therefore
needs the smallest prerequisite: land the existing source/owner-matched
`seriesInspection` helper with the presenter test seam (or revise the query to
an equivalent existing public DrawPlan/component-zero query). Do not replace
this with a guessed ROI or direct geometry copy.

## Evidence

- `handoff-vw-m3-mouth-selected-cut-aggregate-proposal.patch` applies cleanly
  with `git apply --check --whitespace=error-all` and is test/fixture-only:
  four PNGs, inspection/hash manifests, one Node query, and one pytest file.
- The retention archive
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/viewing-mouth-legacy-public-four-stills-v1.tgz`
  is 10,319 bytes with SHA256
  `e7f32e40aa1aa25d81f30d05fd5ccb83a8a19cd8ce4a5a560e9fd93dc73d7c39`.
  Its six members compare byte-for-byte equal to the retention evidence:
  inspection JSON, hash manifest, and original frames 0, 3, 4, 5. Frame 0
  and frame 4 are distinct archive members with equal bytes, not a relabelled
  replacement.
- The real current Agent path, using the retained original files, ran
  `sheet.select_cut` and `sheet.build_context` and resolved the actual flat
  Root cut: index 1, clip `presenter`, track `overlay`, interval `[0,2)`,
  empty occurrence/shot IDs. The actual `builtin.render_lipsync` path read
  `[0,3,4,5]`, compared adjacent pairs `[[0,3],[3,4],[4,5]]`, found
  `[336,336,336]` changed pixels in a 799-pixel crop, and reported the exact
  `3 of 3` finding.
- Direct pure controls on the same current path passed: unordered/duplicate
  frame requests collapse identically; removing key 3 yields `1 of 2`; a
  missing image at key 3 resets adjacency but retains the selected-key
  denominator (`1 of 3`); end-exclusive and start-inclusive windows select
  `[0,3,4]` and `[3,4,5]` respectively; fewer than three selected keys emit
  no pixel aggregate.

## Actual caller boundary

Hook `18ec2b573` is present and correct as a preparation seam: the callback
runs on final serialized Root props and the sorted/deduplicated frame tuple
inside the existing staging lifetime, before capture, and capture refuses
omitted requested frames. The current visualize callers at
`composed_frame.py:350` and `:397` do not pass that callback. The current
`builtin.render_lipsync` consumer still selects `model.mouth_box` and has no
verified retained public component-zero ROI in `LayerContext`.

Thus the future production caller join remains held: pass the existing hook’s
prepared Root/frame lifetime through the existing capture caller, retain a
source/owner-matched component-zero ROI, and carry it into the existing
context. That is not part of this test-only proposal and must not be claimed
as activation, private-crop/statistics deletion, or Gate 6 evidence.

## Commands and results

```text
git apply --check --whitespace=error-all <proposal.patch>
PASS (exit 0)

node --check <presenter_selected_cut_query.mjs>
PASS (exit 0; import/export availability still requires the presenter helper)

PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python - <<'PY' ...
  # actual sheet.select_cut/build_context + builtin.render_lipsync
PASS (exact 3/3 aggregate and cut reference)

PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q \
  -c pyproject.toml -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_remotion_native_window.py
25 passed in 3.70s
```

The proposal worker’s recorded isolated public10 run is consistent with these
checks (`25 passed in 4.71s`, 15 proposal cases plus 10 unchanged crop
neighbors), but it ran against later source `54b9c1fee`, whose helper does
export `seriesInspection`; that is the exact source-drift blocker found here.
No browser, socket, full suite, install, render, product activation, private
crop/statistics deletion, or new xfail was run or claimed.

## Minimal next step

Add/land the source-qualified `seriesInspection` helper on the current
presenter-802 prerequisite, rerun this proposal’s existing targeted lane
against hook `18ec2b573` plus presenter `802669926`, then separately route the
prepared public-zero/source identity into the real lipsync caller before any
consumer replacement or deletion decision.
