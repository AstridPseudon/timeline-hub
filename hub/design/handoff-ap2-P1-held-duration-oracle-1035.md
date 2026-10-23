# P1 held-duration oracle handoff

The App proof spec has a single authorized test-only correction at
`tests/e2e/local/three-products.p1-chain.spec.ts:448`: the merged right clip
now expects `hold: originalClip.hold - SPLIT_AT`, which is the faithful numeric
post-split hold 6 from seed hold 8 and split-at 2. Source In changes only
`from` 0→3 and preserves hold 6, `to` 8, and `at` 2. No fixture, second case,
or other assertion changed.

Scoped ESLint, original Playwright `--list` (2 tests), root/App/Node
typechecks, and `git diff --check` all passed. No browser, HTTP/body, full,
build, service, or `request-test` execution was run. This remains a proposal:
no body credit or H3/P1 integrated credit; independent no-weakening review is
the next step.
