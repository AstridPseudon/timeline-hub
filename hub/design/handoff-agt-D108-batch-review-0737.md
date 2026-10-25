# F-D108 protected batch review

Read-only review against the settled PLAN and `tl/integration` `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`. No repository, census, ledger, foreign-source, or Runtime-authored file was changed.

## Scope A — D07 coverage candidate

**Verdict: PASS_SOURCE.** This is source qualification only: no functional pass, normal merge, or MAIN claim.

The candidate is exactly the full delta from `tl/agt-F-D108-D07-coverage-0732` (`f45e6c732d35dc7a04cd6fc0d019f5f67bcc522b`) against `070dfc5e`: one file, `tests/editing_conformance/test_recipe_m2_clip_trim.py`, +94/-0. Existing functions, parameters, markers, assertions, and the full captured core tuple are AST/body-conserved. Candidate and parent both parse/compile, Ruff, mypy, and pass `git diff --check`.

Predicate review is individually clear:

- D07-1 is covered by `test_native_group_preserves_exact_track_scoped_ripple_timing_and_audio`: first visual `(at, from, to)` changes `(0,0,1)` to `(0,0,1.5)`, later same-track visual is `at=1.5` with source `[0,1]`, audio remains `(0,0,2)`, and compiled duration is `2.5`.
- D07-2 is covered by `test_native_speed_two_preserves_source_window_move_and_endpoint_length`: `at=4`, source `[2,4]`, speed `2`, no obsolete aliases, frames `(120,150)`, move to `10`, move to `20`, and endpoint `21.5` yields `to=5` with playback endpoint `21.5`. The refusal uses valid source data and the registered current `clip.move` duration/window guard: source `[2,4]` at speed `2` implies one second, while authored `duration=3` is contradictory. This protects the same inconsistent duration/window property as the old placement refusal; it is not an unrelated rejection. It does not restore `place_media`, `move`, or `retime`, and does not invent ABA/inverse obligations.
- D07-3 is covered separately by `test_native_group_preserves_shifted_source_window_and_audio_bytes`: first visual grows to `4.5`, later visual moves to `1.5` while retaining literal source `[8,9]`, and the unrelated audio row is byte-equal to its deep copy. The compiled `2.5` duration is consistent with the same current sequence.

The tests use only current `capture_clip_trim`, `capture_move`, `execute`, and `document_from_bundle`; their source registry duration is valid for every tested endpoint. No retired writer, `retime`/`retime_with_ripple` API, flag, or policy was revived. The old audio-target and `parent_duration="preserve"` refusal calls remain separately classified as approved interface retirement and were not incorrectly required as live current behavior. No assertion weakening or invented original ABA was found. The only intentional API translation is D07-2’s same-property current guard described above; no contract or intent doubt remains at source level.

Naming correction: the authored candidate handoff was named `handoff-agt-F-D108-D07-coverage-0732.md/.json`; the extra `F-` is wrong in the required output name. The target rename is only to `handoff-agt-D108-D07-coverage-0732.md/.json` (drop `F-`, preserve contents). This review artifact is separately and correctly named `handoff-agt-D108-batch-review-0737.md/.json`.

## Scope B — census source-return

**Verdict: FAIL_SOURCE.** The accounting and restoration evidence is authentic, but one required live Windows selector is absent from the current Agent source and has no approved exclusion or current equivalent.

Verified facts:

- Exact AST set logic is raw `105` (`99a03feaf7d0343ad08837609df17bdd19b0af88ce671ef50bd4fb85b63c0714`), declared `104` after removing only the approved D18 scope exclusion (`468170f22ffa162ad5543ff70f9c72aecb084b4f8f54cc9dbc1d5fc6bd40f912`), and reconstructed `103` after the separate Windows registration omission (`235833c98214b57d7255cb422e1d0340d9d0b386e679cb475e86449428fcf310`). The declared-minus-reconstructed set is exactly `tests/test_installer_windows_tasks.py::test_register_scheduled_task_accepts_rendered_xml_string`.
- D18 is an approved scope exclusion, not retirement. Its fresh selector and renamed current selector are not exact-equivalent, but that is outside this census disposition.
- The current Windows file retains `test_task_cleanup_preserves_powershell_success_and_failure` and lacks `test_register_scheduled_task_accepts_rendered_xml_string`. Both are required F-final test sets; the cleanup set does not substitute for registration coverage.
- The 0724 author amended the Runtime-authored crosswalk at the wrong target. The 0731 return evidence shows the amendment was snapshotted, the original worker patch/log/source identities were consulted, and both Runtime files were restored to the exact claimed Git blob preimages: Markdown `354c2aa0a41371568eb672d434dba9743b15d004`, JSON `cd7847582b8f73f445768d3ac519de4d28f06630`. The Agent census handoff is explicitly a derivative, not an inherited Runtime original. JSON/set/hash checks pass.

The Windows behavior is live. The precise faithful current-API proposal is to restore the fresh selector’s body as a test-only addition in `tests/test_installer_windows_tasks.py`, using unchanged current `Service.register`, `Service.unregister`, `Service.powershell`, `service.TASK`, `service.TASK_QUERY`, `service.render`, and `Version`: monkeypatch a unique task name and filtered query; make `render` inert by replacing two `<Enabled>true</Enabled>` occurrences; use the `Service(..., system="win32")` and `Version(...)` constructors; call `manager.register(version, data)`; assert the UTF-8 XML starts with `<Task ` and contains no XML declaration; query the task with `Get-ScheduledTask -TaskName ... -ErrorAction Stop`; and always unregister in `finally`. This is a proposal only; this review did not execute Windows, imports, or tests.

Static command outputs and hashes are in [static-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108-batch-review-0737/evidence/static-review.md). No full suite was requested.
