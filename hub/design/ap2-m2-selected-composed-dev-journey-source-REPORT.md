# ap2-m2 selected composed DEV journey source

## Result

Added one local-DEV Playwright journey source in `tests/e2e/local/three-products.selected-param-dev.spec.ts`, wired into the existing three-products Playwright config. The harness creates a throwaway project pack, admits P1 and P2 through the existing Agent project-pack CLI and Runtime document/object path, uses the existing Agent `timelines update-element` carrier to create an accepted P1 history basis, and removes only the authored element source after P2. The DEV Vite process resolves the retained P1 snapshot through the existing resolver/admission configuration.

The journey drives a real UI PARAM edit, checks the original P1 DocumentPin, exercises later P1-schema refusal after P2/source removal, loses one accepted acknowledgement, verifies durable retry after reload, and exercises mounted undo. It records no legacy composition-save traffic.

## Checks run

- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts playwright.three-products.config.ts` — passed.
- `npx tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — passed; collected 1 test.

Per the orchestration rule, I did not run a local browser, localhost/live-socket journey, or full suite.

## Later central command

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-composed-dev-journey-source full-e2e-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

## Decisions and limits

- Kept the existing selected guard controls and all product routes/DTOs/stores/gateways unchanged.
- Used local DEV Vite with the existing `ASTRID_ELEMENT_RESOLVE_COMMAND`, project-pack roots, Runtime credential, and exact Agent binding; no hosted identity or built-in hosted catalog is used.
- The browser qualification remains unverified until the central command runs.
