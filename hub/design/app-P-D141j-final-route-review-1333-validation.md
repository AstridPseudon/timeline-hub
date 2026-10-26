# Validation

All controls used the original pinned Node 20 executable and read-only source inputs.

- `.../node pure-route-control.mjs` → `PASS_PURE_PROSPECTIVE_ONLY`; normal recipe 1,172 bytes / `dbfb3788c869f5f1e2a1e6e6f967305c5aa714c94185f021ec1861db43314f78`; candidate checkout unmaterialized.
- `.../node check-source.mjs` → `PASS_SOURCE_BLOBS_AND_TUPLE`; candidate, Agent, Runtime and Composition commit/tree identities plus all listed candidate blobs and the 67,914-byte Runtime helper matched.
- `.../node synthetic-controls.mjs` → `PASS_FAITHFUL_INTERCEPTS_ONLY`; exact JSON reached intercepted service, Playwright-launch and native seams; all side effects were false/not executed.
- `.../node production-propagation-control.mjs` → `PASS_REAL_D66_PLAYWRIGHT_SEAM`; the immutable D66 `playwrightLaunchEnv` preserved `TIMELINE_D141J_VISIBILITY_CAPTURE` at the actual launch-env seam.
- Read-only source inspection verified the popup occurrence/selector, D66 env spread, real App fixture assignment, collector install/retention, four emitter boundaries and unchanged checker.
- Five one-second disk samples completed with available space above the 4 GB stop threshold.

The first exact control attempt exposed only the retired Composition source-worker path; after correcting that locator in the private control copy to the assigned 635f worktree, the same three controls passed. No product source, tests, generated files, pins, registry, Git metadata, checkout, request, browser, collection, body or native run was changed or executed.

Not run by instruction: request-test, wait-test, row CAS, registration, checkout request/materialization, installation, service, Runtime/App request, browser, native D66, body production, product tests, full suite, lint or typecheck.
