## FAIL_SOURCE — F-D86

Reviewed author commit `d2f8c02c6d12e87e4ce4f30cd39598e2d15fb9d8` against parent `bc498acf582a0d1542482edbe2e2d3c9eb023a36`.

Finding: the migrated fixture changes the original shared-source topology. The original input has `occ-a` and `occ-b` sharing `chapter-shot`/`shot-1`. The new setup creates `occ-b` with a new `chapter-shot-b` via `capture_occurrence_create` (candidate lines 101–110), producing separate physical child identity. It should preserve shared placement semantics. Existing assertions only compare `occ-b` before/after the altered baseline, so they do not detect this change.

Blobs:

- Changed candidate: `8e2d51862651b801159b7449e0848090e104d0fb`
- Original candidate blob: `b4372939fc4aa0036171e3f0455d815648860605`
- Retained recipe unchanged: `feecedd16dbd09aa09de0e5b651f8efec3e4e18c`

The target test function AST, decorator, parameters, assertions, and refusal branch are unchanged. The retained recipe file is byte-identical.

Assigned selectors: all 12 requested selectors are preserved.

Checks passed:

- Candidate and baseline Ruff
- Candidate and baseline mypy using `/home/user/work/venv-agent`
- In-memory AST parse/compile
- `git diff --check HEAD^ HEAD`

No pytest, collection, service execution, build, browser, or full suite was run. Evidence is under `workers/rt-D86-video12-review-0010/evidence/`.