# Validation

This is an evidence-only first return for F ZIP-tail(b), D54a/D59 pristine-upstream
preparation. No production, test suite, core/full/P4 runner, clone, build, ZIP,
provider, render, Store, registry, install, source-Git write, or live service
operation was performed. Scoped lint/type checks are N/A for prose/JSON evidence.

## First-return mapping

The five blocking review findings are corrected in the durable artifacts:

1. C0 step field: `commands.md` now uses `steps[].reads`, matching the contract.
2. C0 idempotency: `Idempotency-Key` is shown only as HTTP metadata, outside the
   JSON body.
3. Missing inputs: all five missing route roots and the missing D73 launcher carry
   `UNKNOWN_MISSING_UPSTREAM_SELECTOR` in `selector-map.json`; absence is not
   zero or PASS.
4. Frozen refs: `source-manifest.json` and `inputs.json` retain the named
   immutable commits/trees and separately record the exact frozen-R4 resolutions.
   No ref was moved or historical capture retargeted.
5. Matrix count: `source-manifest.json` records 41 as the historical directory
   count, 34 manifest entries, 33 stable source-only entries, one manifest
   self-file, and seven generated caches. All cache hashes are explicitly
   unqualified; the recorded run-cache hash mismatch is disclosed.

The census1850 PASS is cited only as read-only merge-tree/object/ref evidence.
It does not claim clone execution or a pristine gate.

## Commands and exits

From the assigned worktree:

- `python3 -m json.tool evidence/inputs.json >/dev/null` — exit 0.
- `python3 -m json.tool evidence/selector-map.json >/dev/null` — exit 0.
- `python3 -m json.tool evidence/source-manifest.json >/dev/null` — exit 0.
- `awk '/^~~~sh/{f=1;next}/^~~~/{if(f){print;f=0};next}f' evidence/commands.md | bash -n` — exit 0 for normal and preflight blocks.
- Selector crosswalk Python assertion — exit 0; roots=22, missing_roots=5,
  D54a_selectors=5, launcher=UNKNOWN_MISSING_UPSTREAM_SELECTOR.
- Matrix/hash crosswalk Python assertion — exit 0; advertised=41,
  manifest_entries=34, source_only=33, caches=7, cache_qualified=0.
- Named commit/frozen-ref/tree shell crosswalk — exit 0; named_commits=4,
  frozen_refs=3, composition_ref=1, trees=4.
- Runtime 7070 source AST/SHA-256 crosswalk — exit 0; Python AST and hashes
  100/100, TypeScript identity exactly `packages/typescript: npm test`.
- `git diff --check` — exit 0.

Final durable artifact SHA-256 (after this correction):

- `commands.md`: `26e4037bb7b63977e3a140c2a5a7cbd2e64146f18e991662a4a76ecc2144b16d`
- `inputs.json`: `71452986726ca177f39d5e6e96dc8b76b648cb60cf8699e39f0ba0c308cfef21`
- `selector-map.json`: `5adbe81d6dc3749994798810569c47a6bb9347ee94efef75217e3fab650846e6`
- `source-manifest.json`: `911e9e2dddfc265a5c2303ffe2660df6a7d378b2818b4e82aaa310460f95e1b1`

No targeted/full suite was run because this preparation explicitly forbids
tests and runner execution. The missing upstream roots and D73 launcher mean
no executable pristine-upstream gate is claimed.


