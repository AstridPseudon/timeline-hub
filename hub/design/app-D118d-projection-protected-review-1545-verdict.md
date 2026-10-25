# D118d independent protected review

Verdict: **FAIL** — exact unapplied setup seam.

The exact nine-node own9 command ran with 5,089,345,536 bytes free at dispatch and ended with nine setup errors. Every node stops at `tests/sdk/test_timeline_capture_projection.py:284` in the newly added `bundle_from_document(document)` call. The current canonical verifier rejects the `_saved_document()` rows because they retain `project_id`, producing `AuthoringBundleError: project scope belongs on the canonical document`. Therefore the registered Runtime `doc.patch` is never reached, and accepted canonical source-item provenance is not proven.

The source-only conservation claims do hold: the branch changes only the assigned test file by +52 lines; the original fixture tail is byte-identical; all 43 original assertions remain and the only added assertion checks setup acceptance; decorators, parameters, test names, and original inputs/goldens remain unchanged. The added request is visibly routed through the test's authenticated `RuntimeService.commit_timeline` adapter and uses the v2-shaped fields, but source inspection cannot substitute for the failed exact behavior gate.

The change exactly matches historical commit `28081580dc95f02470d82ad81b826335d8e4bd09`. Its prior `PASS_SOURCE` review explicitly did not run behavioral qualification, so it does not clear this failure. The D120 upstream check was performed directly at `92443771676ef2bbb547d0a103d708fa8bec4c63`; the target path is absent.

No source, product, test, generated, pin, or Git files were modified by this review.
