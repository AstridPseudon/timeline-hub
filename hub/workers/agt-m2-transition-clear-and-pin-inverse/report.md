Implemented and marked complete.

- Preserved legacy `clear=["transition"]` behavior and unrelated effect/component refs.
- Added explicit closed removal pair: `clear=["transition","elementRef"]`, with strict transition identity validation.
- Added exact absent/null/legacy inverse coverage.
- Restored strict first-selected transition document inverse; introduced pins are cleaned through existing accepted-history seams.
- Fixed nested `values.elementRef` schema resolution.
- Frozen fixtures/docs remain untouched.

Tests:

- Scalar/schema/transition neighbors: `133 passed`
- Selected schema: `32 passed`
- Clip scalar provider: `15 passed`
- Transition provider: `2 passed`
- Focused transition regressions: `12 passed, 98 deselected`
- `git diff --check`: passed
- No full or whole-root suites run.

Base HEAD: `e529366e1881c7391f4e005aad22e753c3fa9224`  
Base tree: `fe853633e545eb2e49559ebe8b1556cdc53371b7`

Commit message and `DONE` marker written. Next step is App2/Runtime peer agreement on the exact closed args before generation.