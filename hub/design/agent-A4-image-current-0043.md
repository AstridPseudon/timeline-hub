## Report

Added [new_image_witness.py](/home/user/work/wt/agt-A4-image-current-0043/test-support/new_image_witness.py), using the real Runtime media realm and preserving raw track `opaque` data.

Tests:

- `py_compile` — passed
- `ruff check` — passed
- `git diff --check` — passed

Live evidence:

- READY input SHA: `09f4afbb93d7f6c74f37f661565b86d2015f3d33f0c3f5e1a6664a346a2f24c4`
- App output was produced and schema/base/selection/intent checks passed.
- Runtime/Agent refused acceptance: `invalid_records: provider executed a different command`.
- Canonical document and head remained unchanged; complete refusal evidence retained.

Blocked marker and commit message were written. No product or shared-environment changes were made. Next step: reconcile the App request’s recorded command/step shape with the Agent provider; no speculative fix or rerun was attempted.