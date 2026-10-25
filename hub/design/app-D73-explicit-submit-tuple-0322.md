## D73/P2 report

Implemented the one-time explicit tuple fix in:

- [d66-plain-stack.mjs](/home/user/work/wt/app-D73-explicit-submit-tuple-0322/scripts/testing/d66-plain-stack.mjs:278)
- [d66-plain-stack.test.mjs](/home/user/work/wt/app-D73-explicit-submit-tuple-0322/scripts/testing/d66-plain-stack.test.mjs:375)

Behavior:

- Complete `D66_*_SHA/TREE/CHECKOUT` tuples are validated and preserved through submit planning.
- Partial, malformed, mismatched, dirty, attached, wrong-root, or invalid snapshot inputs reject before checkout requests.
- No explicit tuple retains the original single `captureSubmitPins()` behavior.
- Pending submit plans remain immutable and resume unchanged.
- Existing receipt, preflight, registry, lock, timeout, and normal-request sequencing remain intact.

Tests/checks:

- `/opt/node20/bin/node --test scripts/testing/d66-plain-stack.test.mjs` — **24 passed**
- `/opt/node20/bin/node --check scripts/testing/d66-plain-stack.mjs` — **passed**
- Scoped ESLint with `--max-warnings 0` — **passed**
- `git diff --check` — **passed**
- TypeScript check — not applicable; `.mjs` files are outside the `tsconfig` `src` includes.
- No full suite, browser, service, build, install, or generated-file checks run.

OLDRED: prior submit path recaptured mutable normal homes despite fixed environment pins, matching the reported wrong-Agent repeat evidence.

NEWGREEN: explicit tuple regression passes with the Agent normal home advanced, correct four checkout requests, one preflight, then one normal request. Default capture and refusal controls also pass.

Protected six SHA-256 values remained unchanged:

`2b9723db…1593`, `50960dd2…bf17`, `09f5e2c2…2b9`, `54ea18f3…85f7`, `bf9a5116…0361`, `93c2bf4c…a64b`.

Source blobs:

- `d66-plain-stack.mjs`: base `c42c291d…`, working `2791c8b2…`
- `d66-plain-stack.test.mjs`: base `b8f989ac…`, working `21f9ce72…`

No blockers. Commit message written to the requested path; `DONE` created.