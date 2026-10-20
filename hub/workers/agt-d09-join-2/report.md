I applied the check.py formatter slice, but not the run.py join. The brief names run.py, but `proposal.patch` touches `astrid/sdk/timeline/check.py` and adds `tests/sdk/test_scene_caller_preservation.py`, and nothing in it changes `run.py`. The targeted run is green: 143 passed, 17 deselected.

## What I applied
- **Patch choice:** I used `proposal.patch` (the known-caller-preservation one), not `donor-amendment.patch`. The two are alternatives, and the REPORT recommends `proposal.patch`, which applies directly to 4a75f68f. The donor amendment only works against the unapplied older deletion proposal.
- **check.py:** `check()` now sends the existing `picture_gaps`, `empty_cuts` and `dips` formatters through a new private `_scene_problems(spans)` helper. Their findings go into `problems`, never `blocking`. Only real UNKNOWN/UNAVAILABLE spans add a `scene` line. Cut addresses, deliberate-hold buckets and wording are unchanged.
- **Tests:** the six new formatter tests use supplied span doubles. Structural invalidity still blocks, and scene advice does not erase it.
- **Critical review:**
  - Saving stays renderer-free: no new imports, flags or providers.
  - Unknown scene checks are advisory.
  - The M1 commits (a76c6537, a610cd30, d9a849e8) are untouched.
  - `core/onscreen.py` stays held.
  - There is no new refusal, no blanket xfail and no skip.

## The five old blocking assertions
I reconciled each under the advisory rule. The four in `tests/sdk/test_coverage_empty_cut.py` are background-only, deliberate hold, inset and translucent. The fifth is `test_a_picture_gap_blocks_publishing_and_says_what_is_left_on_screen` in `tests/sdk/test_timeline_reflow_golden.py`. In each I kept the diagnostic, cut/address and wording assertions. Only the `valid is False` / blocking expectation changed, to "reported in `problems`, `valid`, and not blocking". The reason for each is in the D09 note in `design/deletion-ledger.agent.md`; I did not edit the viewing ledger.

I kept the old test names even though some now read misleadingly. `tests/removed.yaml` tracks test names, and I didn't want to trip it with renames. Rename them if you prefer.

## Tests
Run through the central service with `bin/request-test agt-d09-join-2 targeted --files "<files>"`. I didn't request a full suite. The files were:
- `tests/sdk/test_scene_caller_preservation.py`
- `tests/core/timeline/test_onscreen.py`
- `tests/core/timeline/test_onscreen_more.py`
- `tests/sdk/test_coverage_empty_cut.py`
- `tests/sdk/test_timeline_reflow_golden.py`
- `tests/sdk/test_timeline_checkout.py`
- `tests/packs/rendering/test_labels_overlay.py`
- `tests/packs/rendering/test_timeline_visualize_labels.py`
- `tests/packs/test_pack_migration_m4_shells.py`

Before the reconciliation the same run gave 5 failed, 135 passed, and the failures were exactly those five tests.

## Not done
- **The trusted-source join is missing.** Reusing one resolved registry, theme, merged props, post-resolve candidate and revision/occurrence identity for check and labels needs an Agent source/capture boundary that doesn't exist on this base. The REPORT says so explicitly and says not to invent it, and I didn't.
- **Default callers are unchanged.** They still use the existing `_on_screen()` and the config-only label path. That path is not exercised end to end, so this is a companion slice and D09 is not complete.
- **The join still needs an owner.** Per the REPORT it means extending the capture path with a pass-through of what `run.py` already computes at lines 1100–1115, plus an occurrence-aware mapping back to checkout clips. I recommend scoping that as its own unit.

The commit message is at `orch/workers/agt-d09-join-2/commit-msg` and DONE is created.
