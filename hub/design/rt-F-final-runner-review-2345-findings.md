# F-final independent runner review findings

## FAIL — F1: the production route still uses the predecessor runner

The successor runner directly reviewed here is
`49df8dfe2a5f889c49894c1e302181ca893547e74d0943abba7faf4c7e36c8c2` and its
private core-route stub produced 101 unique Runtime test targets. However,
`runtime-final-service-rows.txt:1` still executes
`rt-F-final-2252-first-return-1130/evidence/candidate/run-final-services.py`
with predecessor hash
`a2d463b32c9a1e13be1c0c7f1c003867094554b3a9a78ed6c332d273e03ce963`.
`run-final-delivery.py:24-28` pins that same predecessor. Therefore the
existing actual service route still runs the D136c 98-target selector and the
new 101-target inventory remains dead metadata on the route.

The installer is also inconsistent: `install-final-services.py:37-42` points
at the predecessor artifact root while `CORE_RUNNER_SHA256` is `5ab35...`, but
the pointed file hashes `a2d463...`; its private `validate_artifacts()` call
refused before any mutation.

## FAIL — F2: traversal is accepted by the inventory validator

`run-final-services.py:47-57` checks count, uniqueness, a `tests/` prefix, and
non-absolute paths, but not parent-directory components. A private negative
control with `tests/../../outside.py` was accepted. Missing inventory,
duplicate target, and absolute target controls were correctly refused. The
validator must reject traversal before the runner qualifies.

## Passing bounded checks

- Direct successor core argv: 101/101 unique targets, all three required
  additions present, TypeScript `npm test` leg preserved.
- All 101 listed target files exist in `/home/user/work/runtime`.
- D73 acceptance: PASS; D59 positive-once/poison-zero/pending-refusal: PASS.
- Compile19, JSON7, Bash3, RuffF, and exact predecessor-config mypy13: PASS.
- Candidate comparison: 66/66 files retained; only runner source and derived
  bytecode changed. All 41 matrix blobs are byte-identical.
- Final/source tuple remains pending; no live capture, install, service, body,
  full suite, network, or product worktree mutation occurred.
