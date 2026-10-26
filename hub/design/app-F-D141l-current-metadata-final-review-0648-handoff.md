# D141l final handoff

The final result is `PASS_CUSTODY_TESTS_FAIL`: documentary custody, raw bindings, corrected receipts, trace measurements, and source identity qualify; the current full and standalone Node test results remain FAIL.

Current source is App `tl/integration` `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, with both recorded parents and clean status. The exact frozen pristine target is d822 `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` / tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`.

The full job remains `19745 PASS / 32 FAIL`, plus one separate collection error; chained Node was `NOTRUN`. Standalone Node remains `296 PASS / 2 FAIL / 26 actual skips` across 324 tests and 33 suites, with 27 distinct declared skip entries. The two `ssh-keygen ENOENT` call sites remain separate findings. No XML was emitted.

The exact pristine target `app-pin-d822d2f5` now exists operationally, with genuine full job `app-pin-d822d2f5-full-1026063854-17524` queued and source preparation worker `app-F-D141l-pristine-queue-prep-0639` active; this is a dependency, not an outcome. The next prerequisite is manager-owned normal pristine admission and execution through the genuine `request-test -> dispatcher/test-run` caller, using the unchanged registered full and Node commands and original receipt/trace validators. Compare each exact failure ID and only then classify REG/nonREG. Do not infer from filename presence, source-only predicates, the queued job, or the environment hint; do not copy tests, inject fixtures, repair SSH, alter the contract, or rerun the current product body.
