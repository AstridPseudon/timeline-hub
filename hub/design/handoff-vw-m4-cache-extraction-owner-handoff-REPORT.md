# M4 cache extraction owner handoff

## Verdict

**READY FOR THE AGENT OWNER GATE / MERGE QUEUE.** This is a handoff of the
existing cohesive extraction; it is not a new review or an activation claim.

## Exact source and scope

- Repository: Agent.
- Candidate branch: `tl/vw-m4-cache-extraction-owner-handoff`.
- Candidate commit: `32c72018d7c8fbeab5c3596d638ce4a3bb0b060d`.
- Candidate tree: `81fd1f0f8ec4af09ae6cc54f00654578de65a1cd`.
- Actual comparison parent/base: `f711cbd29be0b0cb1a51328ea5093b954db3c158`.
- Parent is the prior extraction worker's `tl/integration` base; no merge,
  rebase, checkout, push, or ref mutation was performed here.
- The actual diff is exactly two files: one new private helper and one import
  compatibility edit. It is `72` insertions / `60` deletions (`63` added,
  `9` retained/reformatted additions, and `60` removed by numstat).
- `filmstrip_cards.py`: `1968` lines at the parent, `1917` at the candidate.
- `_filmstrip_cache.py`: `63` lines at the candidate.
- No tests, public rows, PNG layout code, cache key code, source admission,
  fallback policy, or activation code changed.

The only moved behavior is the pair of existing cohesive joins:
`attach_frame_addresses` and `_contact_overlay_for_layers`. Their old public
import path remains available through `filmstrip_cards.py`; the helper is
private and has no new provider, store, DTO, or compiler surface.

## Preserved behavior inventory

The unchanged test sources retain the required assertions:

- `test_scene_cache_payload.py` keeps exact cache-key equality, PNG byte/hash
  integrity, exact `root_source`, valid PNG reuse, no query/private-visibility
  work on a hit, changed-input and changed-renderer misses, stale/forged
  key/source/basis/address/frame/PNG rejection, and failed-batch
  no-mint/partial-file cleanup. It also retains the `cannot mint` guard.
- The default-off / PNG-only fallback remains covered by
  `test_default_provider_keeps_png_only_cache_reusable_across_owners`, with
  `payload is None`, byte-identical PNG reuse, no scene payload, and address
  fallback assertions.
- `test_scene_source_carry.py` keeps historical-source joins, mixed cached and
  fresh observations, fallback invocation only for the cached frame, no-scene
  and partial-file refusal, frozen-source checks, public address rows, and
  empty/unknown transport answers.
- The label and card suites retain opt-in/default-off label behavior, visible
  address ordering, contact overlays, public frame rows, PNG geometry/text/
  fallback-font behavior, and non-mutation checks.

No assertion was removed, weakened, skipped, or changed to refusal. The
base-to-candidate diff contains no test-file delta, so the prior evidence is
reusable on this exact candidate tree.

## Evidence

Reused unchanged-tree results from the extraction worker:

- `/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_scene_cache_payload.py tests/packs/rendering/test_timeline_visualize_labels.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_scene_source_carry.py -k 'not native'` — **133 passed, 19 deselected**.
- `/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_scene_cache_payload.py tests/packs/rendering/test_timeline_visualize_labels.py tests/packs/rendering/test_labels_overlay.py` — **55 passed**.
- `/home/user/work/venv-agent/bin/python -m pytest -q tests/reshape/test_compare_baselines.py::test_the_tree_has_exactly_the_baselined_structure_violations` — **1 passed**.
- `/home/user/work/venv-agent/bin/ruff check --select I,F401 astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py` — **passed**.
- `git diff --check f711cbd29be0b0cb1a51328ea5093b954db3c158 32c72018d7c8fbeab5c3596d638ce4a3bb0b060d` — **passed**.

The candidate worktree was clean during this handoff. Native Remotion cases
were not claimed: the prior direct attempt had `19` native cases blocked by
the unavailable shared `node_modules/react`. No full/native rerun, browser,
renderer, live socket, install, or cache activation was performed.

## Required next step

Agent owner/manager should perform its normal owner gate and merge-queue
decision against the exact candidate SHA above. D09 remains held and is not
retired or activated by this handoff.
