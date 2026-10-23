# Handoff: ap2-P2-inverse-delta-review-0436

## Result

FAIL.

The 43-line delta correctly extends ABI1 Undo checks to generated default label, authoritative nonempty step patch/dependencies, effective merge mode, and exact `source` shape. However, the inverse path still asserts that authoritative response/history commands equal the minimal ABI1 request command (`tests/e2e/local/three-products.p2-tour.spec.ts:248` and `:340`, invoked for Undo at `:487`/`:497`).

App `undoTimeline` sends only `timeline.inverse` with `args.publications`, no request label/steps. Agent `commands.execute` adds inverse `intent`, `resolved`, captured reads/selections/bindings/created, and generated expect/authorship guards to the recorded command. Runtime returns that normalized command in `data.commands` and stores it in `records.commands`. Expected actual form is therefore the minimal inverse object plus those provider-generated fields, not strict equality with `post.body.commands`.

Static evidence:

- Playwright `--list`: PASS, exactly 3 tests.
- `npm exec tsc -- --noEmit`: PASS; root project excludes e2e.
- exact-file ESLint: PASS.
- `git diff --check`: PASS.

No product/test edits, browser/socket/service/body/full/build execution, or commit was performed.
