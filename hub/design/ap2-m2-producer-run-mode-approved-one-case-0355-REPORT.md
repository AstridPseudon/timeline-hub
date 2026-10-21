# AP2 M2 producer run-mode approved actual — blocked

## Result

No actual producer suite was submitted. The first combined preflight identity
check failed: the assigned worker worktree is not based on the approved frozen
source0354.

## Prerequisite review

The explicit run/list source0354 report exists and the delta review explicitly
APPROVES the exact tuple:

- source commit `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`
- source tree `f41a45c01293b0248a27c490bb9e8aa02be33ecd`
- wrapper SHA-256 `11080069b40aab7e9fd9798974cc43d9b244de5f17d930ebc74dc0f935136fc2`
- protected runner SHA-256 `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`
- actual suite `ap2-m2-producer-existing-graph-command-actual-e2e-integration`

The review is an APPROVE, not a HOLD. The list-only suite was not used as
actual evidence, and the stopped0349 row was not retried.

## First failed preflight

Commands:

```text
git rev-parse HEAD
git rev-parse tl/ap2-m2-producer-explicit-run-mode-source-0354^{commit}
git ls-tree -r --name-only HEAD
git ls-tree -r --name-only tl/ap2-m2-producer-explicit-run-mode-source-0354
```

Observed:

- assigned `HEAD`: `976e08c6c8fffd4ebb4e61e8fc1523685a330f87`
- approved source commit: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`
- assigned worktree branch: `tl/ap2-m2-producer-run-mode-approved-one-case-0355`, based on `hub/timeline/app/tl/integration`
- approved source contains `scripts/testing/run-producer-public13-list.sh`,
  `playwright.producer-ownership-current-pin.config.ts`,
  `tests/e2e/local/producer-ownership-current-pin.spec.ts`, and its helper;
  none of those required files is present in the assigned worktree
- `git merge-base --is-ancestor` failed in both directions; the worktree is
  neither the approved source nor an ancestor/descendant of it

Because the source identity failed, I did not run the actual Node/Vite,
graph/short-child, or central browser suite and did not alter the source,
remove `--list`, or retry. No actual packet/trace was generated. The named
suite was not submitted, so there is no result to claim.

## Other observations

- `suites.conf` contains the approved distinct list and actual entries.
- Free disk was 15 GiB, above the 10 GiB floor.
- The assigned worktree was clean before stopping.
- No concurrent producer process was found.
- No local browser, full suite, install, or legacy-cut operation was run.
- Live callers changed: none; this worker made no repository changes.

## Blocker / next step

The orchestrator must provision this worker from the exact frozen
source0354 commit/tree (without changing the approved source or suite) and
re-run the full combined preflight. Only then may this worker submit exactly
one `--no-cache` request for
`ap2-m2-producer-existing-graph-command-actual-e2e-integration`.
