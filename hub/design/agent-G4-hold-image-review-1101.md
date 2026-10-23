# G4 image-hold compatibility review

## Verdict

**FAIL overall / HOLD for integration.** The scoped Agent source and recipe
change is correct, but the mandatory current-Runtime held-image acceptance
proof is not executable with the existing fixture. The source-level result is
PASS; no Runtime-backed acceptance PASS is claimed.

## Source and recipe review

The qualified App producer at
`src/tools/video-editor/lib/timeline-asset-plans.ts:362-389` emits the literal
image row `{clipType: 'hold', hold: 5}`. It does not rewrite the row or invent
timing. In `native_occurrence_media_commands.py`, `_verified` authenticates the
selection and derives `kind` from verified `media_type`; `_clip` now admits
`hold` only for `kind == 'image'`. A video row with `clipType: 'hold'` still
fails the existing matching-media check.

The ADD and SWAP regression preserves the literal `clipType`, `hold`, raw
unknown fields, absent/null distinctions, asset selection, shared-selection
and physical-ownership guards, inverse restoration, source-window and
interval checks. The original test functions/assertions remain; the diff only
extends the input helper and adds the hold positive plus video-hold refusal
coverage. No schema, executor, default, service, pin, fixture, or contract
file changed.

## Runtime evidence and classification

The normal current Runtime is `49ce53289bc37d9387a7d9e6b9c9b16072162181`.
The existing Runtime occurrence-media acceptance fixture fails in setup before
the command can be accepted: it calls retired `publish_parent_composition`,
which raises `RetiredRouteError` (`timeline_commit_required`). The direct
focused run reproduced all four image/video × ADD/SWAP setup errors. The
author's broader focused run recorded the same fixture-wide 48 setup errors.

A bounded scratch control reused the existing current-Runtime birth/provider
path and changed only the in-memory authored image row to `clipType: 'hold'`.
It reached real Runtime commit validation but was refused before semantic
acceptance with `provider occurrence alias is outside its boundary` (422,
`invalid_records`); the same fixture's finite-frame negative control also
returns current Runtime 422 while the old assertion expects 409. Therefore no
real held-image positive or negative acceptance result is credited.

The separate 23 manifest-inverse failures are existing authenticated
physical-binding normalization failures (`inverse needs authenticated physical
binding normalization`). The reviewed fixture retains exact parent/shot/internal
revision content and retained media pins; the failure occurs at the inverse
history boundary guard before those exact-byte/retained-source assertions can
qualify. They are not a new hold regression and were not broadly rerun.

## Checks

- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_occurrence_media.py` — **66 passed**.
- Scoped Ruff — **passed**.
- `make PY=/home/user/work/venv-agent/bin/python ruff` — **2149/2149**.
- `TMPDIR=/tmp/agt-G4-hold-image-review-1101 MYPY_CACHE_DIR=/tmp/agt-G4-hold-image-review-1101/mypy-cache make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **1912/1912**.
- `scripts/artifact_manifest.py --check` — **passed**.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **passed**; frozen Runtime `34eac004` matches. The current `49ce532` intentionally does not match that lock selector.
- `git diff --check` and protected-file diff — **passed**; only the two assigned source/test files differ from `ce1d1cca8`.

## First-return gap

The integration owner must first replace the retired setup with the current
commit path and repair/authenticate the exact parent bytes and physical source
binding. Then rerun a bounded real-Runtime image-hold ADD/SWAP positive and
video-hold negative control. Keep the current literal-row, source-custody,
selection, ownership, timing, inverse, and refusal guards unchanged.
