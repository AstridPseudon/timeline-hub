# Runtime D17 independent authority review

Verdict: **FAIL; do not merge the author commit as-is.** Reviewed exact author commit `36f24786942acd55af2395c1372dd4ac3d4c658a` / tree `00a0d74d211a0e79d8513478eb1160cf4fd3ea20`, parent `eb13b2051d4d30a4d8b7df8878bb7451701eab5a` / tree `5c307b9173aaccdb79697304bf5d5ac64a2487cc`.

Findings:

1. `RequestCommitPort.validate()` adds media IDs from an authenticated `source_revision_closure()` directly to `authorized_media` (`runtime_protocol/timeline_commit_port.py:501-511`). A provider can therefore include a source media pin in the candidate manifest without calling the required `raw_media_info(pin)` for that copied pin. The handoff requires explicit per-pin raw capture. The current focused test only exercises forged media against an empty source media closure.
2. Same-parent scoped Pyright found one new production diagnostic at `runtime_protocol/timeline_commit_store.py:501`: `reportOptionalSubscript` (`document` possibly `None`). Ruff had no identity delta (21/21); Pyright was 80 current vs 79 parent.

The rest of the authority seam is sound on inspection: the exact five-field reference, same-project/different-active-timeline active scope, authenticated callback, accepted historical publication/revision/digest pair, full closure capture, source-head advancement behavior, archive/revocation/pair/digest/foreign/outside/forged-media/changed-capture refusals, and pre-persist acceptance revalidation all use the existing Runtime provider/store path. No Runtime semantic executor, schema/client tuple, or Agent-owned semantic behavior was added.

Evidence: required focused/auth/read-basis suite `93 passed`; port/input/source-document/raw neighbors `88 passed`; py_compile, diff check, new-test Ruff, and frozen-77 (`77 compared, 0 changed`) passed. Existing test files were untouched; only the new focused test was added. No full/P5/browser suite was run. Full evidence is in the worker report.

Next action: require authenticated `raw_media_info()` capture for every copied source media pin (and add a positive source-media test that refuses omission), then resolve/baseline the new Pyright diagnostic and re-review. Agent semantic source-copy ownership remains separate and unqualified.
