# AP2 M2 selected DEV readiness conversion review

## Decision

**REQUEST CORRECTION — do not approve source `45cdc3a59b79357be08e20d6ba187fedb16c8373` / tree `a4f47713c4227075a5f59e42d1006fa1eb831fe3`.**

The conversion is minimal and correctly removes the same-origin DEV-only
`expectConnected` pill assertion, but its replacement is not sufficient as a
readiness proof at all three boundaries.

## Source findings

`tests/e2e/local/support/app.ts:80-84` shows that `openSeededTimeline` only
waits for:

- project combobox text matching `harness.seed.projectName`;
- timeline combobox visibility; and
- the first track-name field to be visible.

It does not assert the selected timeline identity, the selected clip/P1
surface, or the P1 `DocumentPin`. The project check is also by display name,
not project ID. The helper itself is safe in the requested operational sense:
it contains no `page.goto`, `page.reload`, recovery click, route retry, or
other recovery mutation.

The first two call sites retain stronger downstream checks: the exact selected
clip is visible, the element-params panel is visible, and after P2/source
removal the value `8` plus the later refused request's P1 schema pin remain
asserted. The third call site, after the lost-ACK `page.reload()`, has only the
generic helper followed by the unscoped `Recover saved edits` button. It does
not re-establish the selected clip/P1 data before recovery.

## Mapping review

The one-to-one source diff is otherwise correct. Only
`tests/e2e/local/three-products.selected-param-dev.spec.ts` changed:

- initial readiness: `page.goto()` remains in place; only
  `expectConnected(page)` was removed;
- P2/source-removal boundary: the existing `page.reload()` remains exactly
  once, before the helper and the original clip/params/value assertions;
- lost-ACK boundary: the existing `page.reload()` remains exactly once, before
  the helper and the original recovery/retry assertions.

The original assertions remain unchanged: P1 first edit and exact schema
source, P2 revision change and authored-source removal, P1 refusal, draft/lost
acknowledgement, retry state, restart/reload, exact retry body and idempotency
key, inverse undo, and zero legacy writes. No refused state is bypassed.

Hosted connection assertions were not changed: the only changed path is the
same-origin DEV spec; `expectConnected` and its hosted/local callers in the
support module and other specs are untouched.

## Smallest correction requested

Keep the existing navigation, the two existing reloads, and every original
behavior assertion. Replace the generic readiness use with read-only existing
selectors that verify the seeded project and the exact selected clip/timeline
surface at each boundary. In particular, at the post-lost-ACK reload, verify
the exact `data-clip-id="${selected.clipId}"` clip (and the existing
`astrid-element-params`/Amount surface where needed) before locating
`Recover saved edits`. Do not add a `goto`, second reload, automatic retry,
recovery click, or changed refusal expectation. The retained P1 schema-pin
assertions must remain the authority for P1 identity.

## Verification

Passed:

```text
npm exec -- eslint --no-cache tests/e2e/local/three-products.selected-param-dev.spec.ts tests/e2e/local/support/app.ts
  exit 0

npm exec -- playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
  exit 0; Total: 1 test in 1 file

git diff --check HEAD^ HEAD
  passed
```

Not run: browser execution, localhost/live sockets, the central gate, any
full suite, or any source edit. The reviewed source is therefore not
approved pending the readiness-only selector correction.
