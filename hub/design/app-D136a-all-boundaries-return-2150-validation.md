# D136a validation

## Checks run for this review

These checks were read-only and did not execute tests or fixtures:

| Command | Result |
|---|---|
| `git status --short` in the assigned worktree | PASS: clean source worktree before evidence generation |
| `git diff --check` | PASS |
| `git diff --name-status 90b59fd2f517b8ebb2afb1b5b76931d4bbf689db..HEAD -- ':(exclude)evidence'` | PASS: no source changes |
| `git rev-parse HEAD^{tree}` | PASS: `0b66c7a0c1b1af0400055cce16827e42a2908dd9` |
| `git -C /home/user/work/wt/rt-pin-ab1e4f61 status --short` | PASS: immutable Runtime pin clean |
| `git -C /home/user/work/wt/rt-pin-ab1e4f61 rev-parse HEAD` | PASS: `ab1e4f6141987706132916e2da16477f5a019464` |
| SHA-256 verification of manifest-listed Agent and Runtime files | PASS: hashes recorded in `source-manifest.json` |
| `python3 -m json.tool` on `review.json`, `table.json`, and `source-manifest.json` | PASS after generation |
| AST parse of the focused Agent source files | PASS; no type/lint/test execution requested |
| `sha256sum` on all six generated outputs | PASS; hashes captured in the worker command log and final report |

## Reused evidence, not rerun

The exact final20db original9 harness evidence is reused from the earlier D136a review: 9 collected, 9 setup errors, 0 failures, 0 passes, 0 skips, exit 1, common first seam B022. The prior focused source review also recorded its source checks as passing. This worker did not repeat pytest, collection, fixture execution, browser/collector/profile/benchmark/child/acquisition, or any full suite.

## Output custody

All SAFE outputs were written below the required absolute root, not a relative `evidence/` path:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D136a-all-boundaries-return-2150/evidence/`

Files: `review.json`, `boundaries.md`, `table.json`, `source-manifest.json`, `validation.md`, and `findings.md`.

Raw XML/log/private payloads remain withheld; only safe source paths, conditions, counts, hashes and custody metadata are reported.

## Limitations

No dynamic claim is made for branches after the proven refusal. The table is complete for the statically reached source path and explicitly marks missing records and ownership as UNKNOWN. The pristine 886a comparison reports source absence only and is not used to infer a product REG.
