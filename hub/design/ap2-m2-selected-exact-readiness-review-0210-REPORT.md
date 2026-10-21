# AP2 M2 selected exact readiness correction review

## Decision

**APPROVE** exact candidate commit `a0a73dae3303bf5174267fcb53f3fe8ae3cbc426`, tree `2fc6328ed0ea1ecba55269be6f976354406035f2`, on branch `tl/ap2-m2-selected-exact-readiness-correction-0210`.

This is the smallest correction to the rejected `45cdc3a59b79357be08e20d6ba187fedb16c8373` / `a4f47713c4227075a5f59e42d1006fa1eb831fe3` source. It changes only `tests/e2e/local/three-products.selected-param-dev.spec.ts`.

## Review result

The candidate adds read-only existing selectors at all three existing readiness boundaries:

- exact `video-editor-provider` `data-timeline-id` matching `selected.timelineId`;
- exact selected clip visibility using the existing `data-clip-id` locator;
- the existing parameter surface, with the retained `Amount` value `8` checked before lost-ACK recovery.

The third boundary now proves the selected P1 surface after the lost-ACK reload and before locating or clicking `Recover saved edits`. The original P1 schema pin assertions remain the authority for P1 identity.

The diff is additions only. Existing `page.goto` (1), `page.reload` (2), recovery click (1), route abort (1), P1 pin assertions (4), refusal/retry, undo, and zero-legacy-write assertions are retained. No navigation, extra reload, retry, recovery mutation, timeout increase, helper change, production change, or changed refusal expectation was added.

## Verification

Passed:

```text
npm exec -- eslint --no-cache tests/e2e/local/three-products.selected-param-dev.spec.ts tests/e2e/local/support/app.ts
exit 0

npm exec -- playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
exit 0; Total: 1 test in 1 file

git diff --check a0a73dae3303bf5174267fcb53f3fe8ae3cbc426^ a0a73dae3303bf5174267fcb53f3fe8ae3cbc426
exit 0
```

The candidate was checked from a private archived copy with the shared `node_modules` installation read-only. The frozen ref was stable after the required 30-second wait; free space was 17 GiB.

Not run: browser execution, localhost/live sockets, central gate, or any full suite, as required by the brief.

## Next step

Merge/adopt this exact commit and tree for the selected DEV readiness correction. The real browser gate remains separate evidence and is not claimed by this review.
