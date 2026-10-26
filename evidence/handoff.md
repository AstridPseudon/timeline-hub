# D141l corrected handoff

The controlling documentary result is `evidence/current-result-corrected.json`; the detailed corrections are in `node-results-corrected.json`, `trace-measurement-corrected.json`, and `id-map-corrected.json`.

Current full remains `FAIL`: job `app-full-1026060654-8638`, source `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, 32 failed tests and one separate collection error. Its chained Node phase is `NOTRUN`.

The standalone Node job `app-full-d141-node-phase-1026063009-19156` remains `FAIL`: 296 passed, 2 failed, 26 actual skipped tests, 324 tests across 33 suites. Its declared skip list has 27 entries; both values are preserved and named separately. The two `ssh-keygen ENOENT` errors are independent call-site findings; the second suite-level uncaught setup failure is not the first test failure.

The corrected full trace includes all 256 rows: MAX `4809617408` from the first sample, MIN `4494544896`, final `4624244736`, and periodic gaps `4.991440548s..5.008102580s`. The Node trace includes all 19 rows: MAX `4798197760`, MIN/final `4625068032`, and periodic gaps `4.995830387s..5.004783044s`. Historical receipt floor `4793895424`, growth `593895424`, stop `4000000000`, and bracket-only semantics are unchanged.

The exact 32 full IDs are mapped against frozen d822 by title/parameterized membership, not filename presence. The three current-only failure files are absent upstream. Frozen d822 has `useTimelineSave.test.tsx` blob `691c67745b750f06571e40530acd9005f2cc0b3b` and recovered-draft fixtures, but no current prepared-video or public-client Undo title predicates; those own IDs are `N/A` pending the genuine pristine result. Node failure files and `ssh-keygen` predicates are present in both current and d822 with identical blobs; this is only an environment hint until actual pristine comparison.

Next prerequisite is manager-owned normal admission and execution of exact pristine d822/tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`, followed by unchanged full and same-kind standalone Node commands and per-ID comparison. Do not infer `REG`/`nonREG`, retry, substitute source, copy tests, inject fixtures, or alter the registered caller/contract. All original evidence and raw `KEEP` directories remain preserved.
