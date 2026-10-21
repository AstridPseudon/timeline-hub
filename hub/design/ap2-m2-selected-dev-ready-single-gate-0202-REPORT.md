# AP2 M2 selected DEV single-gate attempt

## Result

No central DEV gate was submitted. The required independent review rejected
the exact 0156 readiness conversion and requested a readiness-only selector
correction, so this worker stopped before any browser, socket, build, or gate
run.

Reviewed source:

- commit `45cdc3a59b79357be08e20d6ba187fedb16c8373`
- tree `a4f47713c4227075a5f59e42d1006fa1eb831fe3`
- only changed path: `tests/e2e/local/three-products.selected-param-dev.spec.ts`

The independent review is recorded in
`ap2-m2-selected-dev-readiness-review-0202-REPORT.md` with decision
**REQUEST CORRECTION**.

## Review finding

`openSeededTimeline` is operationally safe: it adds no navigation, reload,
retry, recovery click, or mutation. However, it only waits for project display
name text, timeline combobox visibility, and the first track-name field. It
does not prove the exact selected timeline identity, selected clip, or P1
surface. At the post-lost-ACK reload it is followed by an unscoped
`Recover saved edits` lookup without re-establishing the selected clip/P1
surface.

The reviewer confirmed that the existing navigation and both reloads retain
their original timing, hosted connection assertions are unchanged, and the
original P1/P2, removal, refusal, draft, lost-ACK, restart, exact-retry,
reload, undo, and zero-legacy assertions remain one-to-one. The smallest
requested correction is to use existing read-only selectors for the seeded
project and exact selected clip/timeline surface at each readiness boundary,
especially before the post-lost-ACK recovery button. No second navigation,
reload, retry, or changed refusal expectation is allowed.

## Pre-run checks

Frozen tuple checks passed:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`
- locked App graph archive SHA256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- embedded Composition 0.0.13 archive SHA256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

The existing selected DEV collection passed and selected exactly one test:

```text
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node node_modules/playwright/cli.js test \
  --config playwright.three-products.config.ts \
  --grep 'local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo' \
  --list
Total: 1 test in 1 file
```

The selected central driver syntax check passed:

```text
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh
```

The independent review also passed targeted ESLint, one-test Playwright
collection, and `git diff --check`. No central result exists, so there is no
first request/response or assertion to retain and no merge SHA or selected
writer closure to report.

## Next step

Apply only the review-requested readiness-only selector correction, obtain a
new independent approval of that exact source, then request the single
existing selected DEV suite with `--no-cache`. Do not run the gate against this
rejected source.
