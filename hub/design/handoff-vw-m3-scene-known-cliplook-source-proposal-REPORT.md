# Report

## Result

Implemented the source-only Composition proposal for public Scene evaluation of
known clip-look behavior:

- Crop uses the existing `render-bounds` crop/viewport helpers for known element
  support; media crop continues through its existing media bounds path.
- `scale-in` and `fade-up` entrance wrappers use a shared pure helper for the
  same Remotion spring/interpolate math used by their render components.
- Scene bounds and effective opacity now reflect the actual wrapper geometry,
  including fade-up's vertical translation. Entrance clocks remain half-open.
- Unsupported entrance shapes and exit animation remain unknown. Unknown custom
  modifier bounds remain unknown and cannot be made known by a builtin wrapper.
- No public Scene layer shape, function signature, DTO, package metadata, lock,
  build, or release artifact changed.

## Tests

Passed typecheck:

```text
/home/user/work/app/node_modules/.bin/tsc -p typescript/tsconfig.test.json --noEmit --pretty false
```

Passed focused compiled source tests (6 suites):

```text
/home/user/work/app/node_modules/.bin/tsc -p typescript/tsconfig.test.json --pretty false
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --import ./typescript/tests/register-extensionless.mjs --test \
  typescript/test-dist/tests/animations.test.js \
  typescript/test-dist/tests/clip-opacity.test.js \
  typescript/test-dist/tests/registries.test.js \
  typescript/test-dist/tests/scene-evaluation.test.js \
  typescript/test-dist/tests/scene-diagnostics.test.js \
  typescript/test-dist/tests/transition-policy.test.js
```

Result: 6 passed, 0 failed. `git diff --check` passed. Generated `test-dist`
and the temporary worktree dependency symlink were removed.

Not run: full suite, browser/localhost/socket tests, render or pixel capture,
package build/pack/publish, or release qualification.

## Decisions

- Shared the existing render wrapper calculation by extracting only the
  `fade-up`/`scale-in` style math into the pure clip-look helper; the renderer
  components call that helper too.
- Scene opacity clamps the effective semantic value to the existing [0, 1]
  policy after wrapper multiplication, while renderer style output remains
  unchanged (including its existing spring overshoot).
- Known wrapper transforms retain known outer bounds but invalidate component
  internal diagnostic regions, since those regions are not transformed by the
  public capability contract.

## Blockers / next steps

No implementation blocker. The proposal remains unmerged as requested; an
orchestrator/manager review should decide whether to integrate it and whether
additional media/element caller parity evidence is required.

The supplied prior-report and R4-doc directories were absent from this sandbox;
the implementation was checked against the checked-out Composition source and
the available D09 map under `scratchpad/orch/design`.
