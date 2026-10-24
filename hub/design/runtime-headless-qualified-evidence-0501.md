# R5 headless qualification evidence

This is a contemporaneous qualification record, not a fabricated raw capture.

- Qualification command was run once, exactly as assigned, from Runtime worktree `rt-R5-headless-qualified-0501`.
- Result: 13 collected; 12 passed; 1 failed.
- Failing node: `test_cas_correct_republish_after_reading_the_head_is_accepted`.
- Failure assertion: `entry["records"]["commands"][0]["created"]` did not equal the retained expected order asset, clip, track. The observed first actual item was the parent track; the expected first item was the parent asset.
- No rerun was performed after this failure.
- Static source inspection identifies the production source owner as Agent `astrid/sdk/timeline/_doc_patch.py`, `allocations()`, which processes parent track allocations before clip allocations and then registry asset allocations across the submitted changes. Runtime `timeline_commit_store.py` reserves the Agent-provided `created` references without reordering them.
- Complete request/prepared/native/effects/bindings/source-history and before/after SQL/head/history capture is unavailable: the retained test has no bounded capture seam before the failing assertion, and capturing it would require rerunning the stateful case. No values were fabricated.
- No credentials or tokens were included in this record.

Provenance:

- Runtime commit: `66657fda44ecaf878b74e8eb7eaf5e54330f3fb0`
- Runtime tree: `51aa45329150f3665f4fd060323a9df78ebe4468`
- Runtime parent: `faf6a5477f9f6e4d96829046957518fef7a0dbed`
- Agent archived commit: `9cd3dbe865a941c052bda04ae0d61306d18f8f26`
- Agent archived tree: `57f0231da0d7904ecd8778169973d6384e0ae141`
- Agent module origin: `/tmp/w-fab1c00f16/astrid-exact9cd3dbe/astrid/__init__.py`
- Agent patch module origin: `/tmp/w-fab1c00f16/astrid-exact9cd3dbe/astrid/sdk/timeline/_commit_patch.py`
- Runtime module origin: `/home/user/work/wt/rt-R5-headless-qualified-0501/runtime_protocol/__init__.py`
- Archived `_commit_patch.py` SHA-256: `c12b641754dff344e01824379b117304ee78259743c3c3b057fb22301e404238`
