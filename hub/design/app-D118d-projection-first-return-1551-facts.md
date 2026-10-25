# D118d source facts

The only source change is in `tests/sdk/test_timeline_capture_projection.py`, in `_saved_document()`. Runtime public child-revision reads include `project_id` and `created_at`; the genuine current `read_document()` caller projects them to the canonical image fields before calling `bundle_from_document()`. The corrected helper now uses those exact shot and internal image field sets.

The authored source-item patch, publication commands, opaque fields, pins, order, read rows, golden values, test parameters, and all test-function ASTs are unchanged from candidate `a92c6afe0ccd2359e952fc534788d1fce2169049`. No product guard or arbitrary row stripping was changed.

Static checks pass: Ruff, py_compile, mypy, and `git diff --check`.

The own nine-node check is NOTRUN because free space was 4,953,280,512 bytes, below the required 5,000,000,000-byte light-run floor. The protected prior run had nine setup errors before the Runtime commit path; this correction therefore remains behaviorally unverified here.
