# Runtime D17 final independent authority review

Verdict: **FAIL** against the original D17 review findings.

Reviewed exact current commit `2d95afef817748c86b463d3cfb260b1275851053`
over integration `7ca1a227815404252fec1e4768e550610f9c5705`; original author
commit `36f24786942acd55af2395c1372dd4ac3d4c658a` is not an ancestor.

F1 is fixed: source-closure media is no longer directly authorized. Every
copied source media pin must be consumed by `raw_media_info(pin)`, and the
real-media positive, missing-capture pre-write refusal, forged-pin, and changed
capture controls pass.

F2 remains open: `document.get("parent_revision")` in
`runtime_protocol/timeline_commit_store.py:501` still triggers Pyright
`reportOptionalMemberAccess` because `document` is possibly `None`. This is not
validated narrowing and does not satisfy the no-ignore/no-budget requirement.

Evidence: required acceptance **118 passed**; bounded port/input/source/raw
neighbors **88 passed**; source-media subset **4 passed**; py_compile, diff
check, focused-test Ruff, frozen-77 (**77/0**), and original focused-test AST
preservation passed. Scoped Ruff is **21/21** with no identity delta. Scoped
Pyright is **80 current / 79 parent**, with the remaining optional-document
diagnostic in the added source method. No full/browser/P5/Agent suites were run.

No production repair was made. Resolve F2 with a real guard/narrowing and repeat
the same evidence before merge.

Inherited old ABI-1 fixture failure status is **unverified** because the
author’s repository-wide `.` run was interrupted/environment-dependent; no
ABI-1 repair or full-suite claim is made.
