## Verdict: PASS

All three mappings are exact:

1. `tests/packs/timeline/test_cli_native.py::test_track_label_dispatch_matches_native_capture[args0-\u753b\u9762 \U0001f3ac]` → `test_track_label_apply_matches_native_capture[args0-\u753b\u9762 \U0001f3ac]`
2. `tests/packs/timeline/test_cli_native.py::test_track_label_dispatch_matches_native_capture[args1-]` → `test_track_label_apply_matches_native_capture[args1-]`
3. `tests/packs/timeline/test_cli_native.py::test_track_label_dispatch_matches_native_capture[args2-None]` → `test_track_label_apply_matches_native_capture[args2-None]`

The three input tuples are unchanged: Unicode label, empty label, and clear/remove. Command capture, `parent/track:picture`, `pub1` receipt/publication, and final label predicates are retained. The intentional route change is CLI `edit track-label` to native sheet `show` → edit → connected `apply`, with `source.via` changing from `cli` to `sheet`. The clear case seeds an existing label before removal.

Source identities verified:

- Original commit: `c36ca8c94b695b0e25b7d42c89f194661f187423`
- Current commit: `9cd3dbe865a941c052bda04ae0d61306d18f8f26`
- Original test SHA256: `94f395884528cd252146d5ea2d5025cffb9633b760ae154f1943dfedc3b717c1`
- Current test SHA256: `29d820f1623ec3b93978928a0bfbccd78cdbadc290e39c04b42ce3fee0bfcd2c`

Production trace verified: connected `_cmd_apply` → `commit_edit(sheet=True)` → `NativeSheet.apply` → `TimelineSession.commit_many` → generated `commit_timeline`/`commitTimeline` request → Runtime coordinator and store preview/accept authority. The full request/reply contract remains unchanged.

Evidence reused, not rerun:

- CLI0404 targeted command: `11 passed in 1.63s`
- Integrated0500: `71 + 5 + 53` aggregate passes on current head. D32 correctly does not infer original-node credit from this aggregate.

Fresh permitted checks:

- Stdlib AST/predicate comparison: passed.
- `git diff --check`: passed.
- `git status`: clean.

No product/test edits or behavioral test bodies were run. Mapping is independently verified; original-node behavioral credit remains unverified per the task restriction.