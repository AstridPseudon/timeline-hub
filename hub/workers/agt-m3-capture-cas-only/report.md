A working-copy capture with no forwarded `authoring_preview` candidate now goes out as explicit CAS-only. The unit tests pass, but the integration lane could not confirm the `tests/sdk/test_capture_source_runtime.py` cases, including the strict xfails. I wrote the commit message and created `DONE`.

## What changed
- **`astrid/sdk/invocation.py`:** at snapshot admission, a capture whose snapshot has a working-copy marker and no forwarded `authoring_preview` is now treated as uncertified.
  - It is no longer left inline for Runtime to treat as a canonical revision.
  - Its snapshot is ingested and sent as `{digest, project_id, timeline_id, source_kind: "cas"}`.
  - It carries no revision id, revision digest or working-copy certificate, and no source is minted.
  - The ref shape matches the one Runtime's new `claim_capture_view` in `capture_validation.py` emits for legacy uncertified captures.
- **Unchanged paths:** a working copy that forwards its candidate stays inline for Runtime to certify. Saved-revision captures behave as before.
- **`tests/sdk/test_visualize_authority_objects.py`:** two new tests.
  - Without a candidate, the capture is sent as exactly the four-key `cas` ref, so nothing is claimed.
  - With a candidate, it stays inline and `authoring_preview` is forwarded unchanged.
- **Probe file:** `tests/sdk/test_zz_probe_forgery_unmarked.py` is emptied rather than deleted, because `rm` and `git rm` were denied here. Its removal still needs doing outside this sandbox.

## Test results
- **Targeted unit run (passed):** `agent targeted --files "tests/sdk/test_visualize_authority_objects.py tests/sdk/test_timeline_capture_projection.py tests/sdk/test_capture_closure_source.py"` gave 62 passed, 2 xfailed, 9 deselected (the integration-marked ones).
- **Integration lane (not green, not verified):** `commit-integration --files tests/sdk/test_capture_source_runtime.py` gave 21 failed, 2 passed. These cannot be attributed to this change.
  - The `commit-integration` suite also runs `test_commit_runtime_m1.py`, and two of its cases fail on a runtime health schema-digest mismatch.
  - The `/home/user/work/runtime` checkout is ahead of what this branch was qualified against. It now includes "refuse forged capture content at admission, label legacy captures uncertified", and it rejects the old fake refs in `test_capture_source_runtime.py` with errors such as "capture differs from authoritative registry".
  - The two strict-xfail tests (missing-candidate refusal and forged content) now fail instead of xfailing, which looks like the Runtime fix landing. I did not touch or relax them.
  - I did not re-run the lane against an older Runtime, so I can't confirm the 21 failures are all drift.

## Next steps
- Rebase `test_capture_source_runtime.py` onto the new Runtime. Its fake `ref()` should use the real ingest and certification path, and the two strict xfails should be removed once they pass for real.
- Once Runtime and Agent are aligned, re-run the `commit-integration` suite.
