# Handoff

`PASS_EVIDENCE`; no behavior PASS/REG0/ship claim.

All 38 exact IDs are accounted for in `per-id.json`.

The old tests exercise the deleted pure `TimelineEvent` planner. The supported
caller is `TimelineSession.undo` → `commitTimeline` → Agent `commands.execute`
and `apply_inverse` → Runtime provider/store. The event schema/projection is
still present, so missing `inverses.py` alone does not establish obsolescence.

Owner must decide whether this legacy pure planner/read path remains supported.
If yes, one finite Agent author restores the exact pristine product and test
blobs and runs `python -m pytest -q tests/timeline/test_inverses.py`, without
assertion adaptation or route revival. If no, approve each row as legacy-only
or C0-refused under D120 item 5/G5 with the exact current selector or explicit
no-selector disposition. The fc33e deletion rationale is not owner approval
under MAIN D141ee.

No tests were run by this worker; retained reviewer results remain visible and
unupgraded.
