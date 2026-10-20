# Independent review: Agent single-occurrence cap contract

## Disposition

**ACCEPT before merge.** Candidate `5bf1731a0c1dbb26e9a276df660172807a1bcd5e`
(`tl/agt-m3-single-occurrence-cap-contract`, parent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`)
is a bounded fixture/test/product-contract-doc patch. It needs no Agent product,
SDK timing, package-pin, Runtime, or product-schema change.

The commit changes only:

- `docs/design/visual-compile-contract.md`;
- `tests/editing_conformance/fixtures/main_image_cap_raw_closure.json`;
- `tests/editing_conformance/fixtures/visual_compile_contract.json`;
- `tests/editing_conformance/test_compile_contracts.py`.

The separate raw fixture is justified by the exact byte-preservation/hash
requirement. The larger shared fixture is not speculative bloat: it retains the
full editor analog needed for the stored-2000/content-5000/next-4000 positive,
and the exact closure's complete projected config, registry, serialized output,
and cited MAIN observations. No source/README/process doc was changed.

## Contract checks

- Candidate raw fixture SHA256:
  `ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04`.
  It is byte-identical to
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-image-cap-source-vector-raw-closure.json`.
- Candidate shared corpus SHA256:
  `43783e0f40ef1922b54af855379c8538074c8b1df3a7abd4472a8db93877a484`.
- The raw closure has exactly one occurrence, stored `duration_ms: 4000`,
  authored `hold: 5` and `fade_out: 1`, and no next occurrence.
- The normal managed path is genuinely exercised: exact `_Runtime` reads feed
  `resolve_managed_render_snapshot` / `project_runtime_parent_composition`,
  then validation, materialization, and `_serialize_timeline`. The test compares
  both full projected outputs to the shared fixture, checks projected and
  serialized hold `4`, and verifies the raw object and input bytes remain equal.
  No cap, next occurrence, `canonicalTiming`, or other production input is
  inserted by the test.
- The public 0.0.12 pure evaluator receives the actual serialized output. It
  proves numeric 30fps: frame 90 opacity `1`, frame 105 opacity `0.5`, frame
  119 present with opacity `1/30`, frame 120 absent, and own/draw duration 120.
  Raw hold-5 direct `clipOpacity` is retained only as the explicitly labelled
  diagnostic (`1`).
- The editor analog remains positive and unchanged in meaning: authored
  occurrence 2000ms, next same-lane start 4000ms, content hold 5, supplied
  effective cap 4000ms, projected hold 4; the authored graph remains unchanged.
- Existing A8/B10 overlap, overhang clamp, rational-clock, projector, timing,
  reflow, and managed-render neighbors pass. The two existing audio xfails are
  unchanged; no new xfail is present.
- No production source, package pin, Runtime schema, or product schema path is
  changed. The `schema_version: 5` increment is scoped to the shared test corpus
  metadata for the added vectors.

The App effective-duration discrepancy remains an external policy-resolution
item. This Agent review does not approve or imply an App policy change. The
document makes no claim of live Runtime acceptance, renderer/browser pixels,
audio parity, owner-film behavior, or Gate 6 closure; MAIN pixels are only the
cited reference from `app-main-cap-half-golden.md` / the MAIN reference.

## Evidence

All candidate tests were run from a temporary `git archive 5bf1731a` extraction
under `/tmp`, leaving the assigned worktree unchanged. Shared dependencies and
caches were not modified.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/agt-review-single-cap.9yuzKV \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  /tmp/agt-review-single-cap.9yuzKV/tests/editing_conformance/test_compile_contracts.py
```

Result: **32 passed, 2 xfailed**. The only xfails are the pre-existing audio
vectors `fade-in-needs-prepared-envelope-source` and
`fade-out-needs-prepared-envelope-source`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/agt-review-single-cap.9yuzKV \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  /tmp/agt-review-single-cap.9yuzKV/tests/editing_conformance/test_compile_contracts.py \
  /tmp/agt-review-single-cap.9yuzKV/tests/timeline/test_shot_composition_projection.py \
  /tmp/agt-review-single-cap.9yuzKV/tests/core/timeline/test_shot_composition_projection_volume.py \
  /tmp/agt-review-single-cap.9yuzKV/tests/sdk/test_timing_compiler.py \
  /tmp/agt-review-single-cap.9yuzKV/tests/sdk/test_timeline_reflow_golden.py \
  /tmp/agt-review-single-cap.9yuzKV/tests/packs/rendering/test_managed_timeline_render.py
```

Result: **152 passed, 2 xfailed in 16.95s**.

Direct private public-entry check with Node `v20.19.4` and the extracted
Composition 0.0.12 artifact returned:

```text
{"f90":1,"f105":0.5,"f119":1,"f120":0,"own":120,"draw":120}
```

Additional checks: Ruff passed on the touched Python test; `git diff --check`
passed; exact raw-source `cmp` passed; the candidate has zero diff under
`astrid/`, `remotion/package.json`, `runtime.lock.json`, and
`astrid/core/timeline/schema`.

No full suite, browser, live socket, real Runtime, or pixel rerun was requested
or run.

## Follow-up

Merge the candidate as-is. Keep App policy reconciliation separate and preserve
the App editor positive while deciding how its single-occurrence consumer should
honor the stored 4000ms cap.
