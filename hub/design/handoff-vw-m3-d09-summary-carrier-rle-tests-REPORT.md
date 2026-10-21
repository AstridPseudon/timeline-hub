# D09 public Scene-summary RLE test packet

## Result

Added one 143-line test packet at
`tests/sdk/test_scene_public_summary_rle.py`. It feeds the existing public13
Scene-answer shape through the active `_scene_only_spans` carrier and checks
the existing `_scene_problems` consumer after privately applying the approved
`handoff-vw-m3-d09-frozen-span-final.patch` unchanged.

The packet proves:

- exact summary rows `(0,30) COVERED/CONTENT`, `(30,45) GAP`, and
  `(45,90) COVERED/EMPTY` while retaining 90 detailed rows, clip membership,
  and findings;
- one-sided `DIP (0,15)` followed by `COVERED/CONTENT (15,60)` with the
  half-open boundary retained;
- a generated 300-answer/300-membership case summarized as one contiguous
  class/content row;
- `GAP` versus `COVERED/EMPTY` distinction and sparse-row non-bridging.

The durable `PATCH` is test-only and contains only the new test file. The
approved helper was applied privately for validation and reversed before
completion. No existing tests, golden JSON, evaluator, geometry, API, store,
or authority code was changed.

## Proposed exact row mappings

| D09 missing row | Proposed active-surface evidence |
| --- | --- |
| 3: coverage summary RLE | `test_public_scene_summary_preserves_exact_coverage_boundaries_and_detail` |
| 5: one-sided fade summary | `test_public_one_sided_fade_summary_is_dip_then_covered_at_half_open_boundary` |
| 13: 300-clip boundary summary | `test_public_300_clip_answers_merge_to_one_class_content_summary` |
| adjacency guard | `test_summary_does_not_bridge_sparse_public_span_rows_or_gap_and_empty` |

## Evidence

- Base: Agent `5c5173dcb57669a9d43e5add2674543333f1c6d2`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_scene_public_summary_rle.py` — **4 passed**.
- Private helper lane: `... test_scene_public_summary_rle.py test_scene_summary_projection.py test_scene_caller_preservation.py test_coverage_empty_cut.py` — **26 passed** (4 packet tests + 22 summary/carrier neighbors).
- Save neighbor: `... tests/sdk/test_scene_save_core.py` — **16 passed**.
- Combined private lane including save neighbor — **42 passed**.
- `ruff format --check tests/sdk/test_scene_public_summary_rle.py` — passed.
- `ruff check tests/sdk/test_scene_public_summary_rle.py` — passed.
- `git diff --check` while privately patched — passed.
- `git apply --check PATCH` from the clean tree — passed.
- Final product worktree has only the untracked new test packet; the approved
  helper and its temporary regression test are absent.

## Qualification boundary

This packet uses the existing public13 answer schema and public Scene carrier;
it does not invoke the installed public13 Node host. Therefore it proves the
active Agent carrier/consumer projection, not a live managed public13 render.
The exact unverified capability is a real installed-public13 host run emitting
these 90-frame and 300-frame answer rows under managed source binding. No
`UNKNOWN` or refusal result is used as a substitute. No browser, full suite,
physical run, or central Node qualification was run.
