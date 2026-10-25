# Validation

## Result

`FAIL` for independent qualification, with the original D127c body failure
preserved. This packet is source/evidence review only; no profiling, browser,
Runtime request, or product test was run.

## Read-only checks

- App HEAD/tree: `b5c9eadfa1950f46feac50d7d6a89c47f27f4881` /
  `8e10af0976b012205f27a18a432c750a27de0725`.
- App source hashes in `source-manifest.json` match the committed checkout and
  the three hashes recorded by the prior 2132 packet.
- The pinned product Runtime helper hashes to `6c9daef...`; the external normal-
  home helper used by the prior packet hashes to `095c252b...`. Their differing
  bytes were verified read-only.
- `node --check scripts/testing/d66-plain-stack.mjs` passed.
- Python AST parse of `scripts/testing/sitecustomize.py` and the external helper
  passed (`python3 -c ...; print("python AST OK")`).
- Prior `first-seam.json` and prior `source-manifest.json` parsed successfully.
- `git diff --exit-code -- scripts/testing/d66-plain-stack.mjs
  scripts/testing/sitecustomize.py
  tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` passed.
- Output JSON (`review.json`, `source-manifest.json`) was parsed after writing;
  output paths and SHA-256 values were verified before handoff.

## Not run by design

No pytest, Vitest, npm test, TypeScript check, lint, browser, localhost,
socket/service, bootstrap, acquisition, request replay, profiling, sampling,
raw-pstats read, full suite, or product acceptance test was run. The task is
read-only and contains no source changes, so repeated product tests/typecheck/
lint would not add evidence.
