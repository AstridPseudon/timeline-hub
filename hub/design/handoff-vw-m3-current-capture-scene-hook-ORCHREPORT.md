Completed the bounded CURRENT capture prerequisite on Agent base
`7261b4ad5827466b2e17f1a30bf35d2fd05e0700`: minimal donor-style
`on_scene_props(merged_props, actual_capture_frames)` hook in current run.py,
plus one direct host-preparation test file. No caller activation/private deletion.

The callback runs after final props JSON is written, with resolved assets/theme
and staged params, inside the existing asset-server lifetime. Omitted/None
preserve the old invocation shape; observers are synchronous/read-only and their
exceptions abort capture with existing cleanup. Serialized Node props remain
byte-identical with omitted, None and observing callbacks.

Final targeted verification: **41 passed in 3.47s, exit 0** (11 new + 30 unchanged
neighbors). New-test lint green; renderer lint exactly matches HEAD's seven
existing diagnostics. Whitespace and flat patch application/byte equality pass.
Exact commands and limits are in the adjacent exact-tests.txt and REPORT.md.
No browser/render/socket/full/install/network or central test request was run.
No skip/xfail, unsupported-known behavior or save-path change.

Basis seam remains explicit: frame capture currently does not deliver a profile.
Use existing `_canonical_profile(timeline_path, _load_registry_mapping(assets_path),
theme_path)` on the SAME frozen materialized inputs, with profile width/height
and fps_rational, for the existing public host basis. Partial authored canvas
selection must follow that profile (tested 640x1080 @ 2997/100 despite merged
resolved theme height=600 and thumbnail 4x3). Do not infer basis from theme alone.
Retained props from a failed capture must not be treated as successful capture
facts. Existing inactive host transport still refuses RenderClockTail.

No blocker. Recommend landing the prerequisite, then the Agent source-owner
join for frozen post-resolve/historical/occurrence facts before live consumers.
Not a source certification, private-mouth replacement or D09/M3/Gate 6 claim.

Flat absolute handoff prefix:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-capture-scene-hook-
Files: proposal.patch, REPORT.md, exact-tests.txt, ORCHREPORT.md.
