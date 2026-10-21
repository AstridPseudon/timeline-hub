# AP2 M2 producer-0355 result cut or cause — blocked

## Scope

This worker was assigned to consume exactly one approved, actual producer
run-mode result and classify only the assertions reached by that run. No
product change or row-local deletion was made.

## First failure and exact cause

The assigned worktree is integration HEAD
`976e08c6c8fffd4ebb4e61e8fc1523685a330f87`, tree
`196cb0c8c630bd21b851ce8a9d1d0e056edd9a2f`. The approved producer source is
commit `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`, tree
`f41a45c01293b0248a27c490bb9e8aa02be33ecd`.

The approved source is available as the local ref
`tl/ap2-m2-producer-explicit-run-mode-source-0354`, but it is not the assigned
worktree source. The assigned tree is neither an ancestor nor a descendant of
the approved source. All required producer-run files are absent from the
assigned tree and present in the approved source:

- `scripts/testing/run-producer-public13-list.sh`
- `playwright.producer-ownership-current-pin.config.ts`
- `tests/e2e/local/producer-ownership-current-pin.spec.ts`
- `tests/e2e/local/support/producer-ownership-current-pin.ts`

The approved wrapper hash is
`11080069b40aab7e9fd9798974cc43d9b244de5f17d930ebc74dc0f935136fc2`.
Because the source identity failed before execution, this is an environment /
worker-provisioning cause, not a product or fixture cause.

## Actual-run result

No actual suite was submitted, waited on, retried, or replayed. The named
actual suite was `ap2-m2-producer-existing-graph-command-actual-e2e-integration`.
The available producer records contain only the prior list-only/stage result
and the blocked 0355 preflight; there is no actual packet, trace, assertion
count, or result directory to classify.

Therefore these intended assertions are all unexecuted and unverified:

- accepted owned stale REMOVE and Scene MOVE/HOLD behavior;
- visible atomic refusal for protected foreign/user rows;
- full raw and order preservation;
- original reload, lost acknowledgement, restart, exact body/key retry,
  undo, and zero-legacy execution.

No PASS or FAIL is claimed for any producer behavior. No first packet beyond
the failed source-identity preflight exists to preserve.

## Callers and cuts

The approved source's only named test-service callers are the distinct list
and actual entries in `scratchpad/orch/tests/suites.conf`; the wrapper's only
repository self-reference is its suite command. No App product caller changed
in this worker. The central ordinary snapshot fallback and all unqualified
producer families remain live. No newly dead row-local leaf was identified or
prepared.

## Commands and results

- `git status --short` — PASS; assigned worktree was clean.
- `git rev-parse HEAD` — `976e08c6c8fffd4ebb4e61e8fc1523685a330f87`.
- `git rev-parse tl/ap2-m2-producer-explicit-run-mode-source-0354^{commit}` —
  `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`.
- `git rev-parse HEAD^{tree}` and the approved source tree check — mismatch;
  preflight failed.
- Required-path presence checks — all four missing in the assigned tree and
  present in the approved source.
- Central queue/result inspection — no actual producer-0355 result found.
- `df -Pk . /tmp` — 15,414,792 KiB free; above the 10 GiB floor.

No Node/Vite build, browser/socket suite, full suite, local browser run,
install, source edit, retry, legacy cut, or test submission was performed.

## Blocker

The exact approved source must be provisioned for the worker before the
authorized single actual run can exist. Until then, producer behavior and any
cut remain unqualified.
