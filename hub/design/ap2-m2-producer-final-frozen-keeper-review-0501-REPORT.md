# Producer final frozen keeper review 0501

## Decision

APPROVE the exact frozen keeper and repaired wrapper command.

Reviewed keeper:

- Path: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Final HEAD: `17d2518c341c47a2d8634047b400399886da3a2a`
- Final tree: `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Committed wrapper SHA-256, recomputed from `HEAD:scripts/testing/run-producer-public13-list.sh`:
  `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`

The keeper is clean, has its required `KEEP`, and retains the normal ignored
dependency link `node_modules -> /home/user/work/app/node_modules`.

## Source and byte review

The approved source is `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`, tree
`f41a45c01293b0248a27c490bb9e8aa02be33ecd`, whose parent is
`70dec48e88ea036bf160539b58b68bb64c38f3b3`, whose parent is the approved
baseline `4ef89267f00d193273441ff6dbb955f30d27d708`.

The final keeper is a descendant of that source. The tracked delta from the
approved source is exactly one path:

```text
M scripts/testing/run-producer-public13-list.sh
```

The body, helper, and Playwright config are byte-identical to the approved
source and hash as follows:

```text
tests/e2e/local/producer-ownership-current-pin.spec.ts       d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
tests/e2e/local/support/producer-ownership-current-pin.ts    50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
playwright.producer-ownership-current-pin.config.ts         5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
```

The wrapper keeps the reviewed short alias, private Chromium/cache/temp
paths, EXIT/HUP/INT/TERM cleanup, Chromium executable/options, one-test and
zero-body assertions, timeout/runner controls, and child return-code guards.

## Negative probes

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-frozen-delta-luna-resume-0453/guard-probes.sh
```

PASS: approved source with no delta; approved source with wrapper-only
successor; wrong base; extra tracked file; body/helper/config drift; wrong
final HEAD; wrong final tree; and wrong final wrapper hash. `sh -n` and
`git diff --check` also passed.

## External service binding and result

I added the owned external gate
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`
and two uniquely named central service registrations. The gate checks the
captured service tree, keeper HEAD/tree, committed wrapper hash, clean state,
KEEP marker, and dependency link before invoking the existing wrapper. It
changes directory to the keeper so Vite resolution remains bound to the short
environment.

Authorized service run:

```text
request-test ap2-m2-producer-final-frozen-keeper-review-0501 ap2-m2-producer-final-frozen-keeper-review-0501-preflight --no-cache
```

Result ID:
`ap2-m2-producer-final-frozen-keeper-review-0501-ap2-m2-producer-final-frozen-keeper-review-0501-preflight-1021050416-31261`

PASS, exit 0, captured service tree `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`.
The existing runner reported:

```text
public13 hosted-build resolver PASS version=0.0.13 ...
public13 preflight PASS checks=10 source=agent:8130a401... runtime:2c4ac180... graph=public13 isolation=private
```

The runner cleaned its private short root and restored the keeper's dependency
link. Post-run keeper and review worktrees are clean.

Two earlier attempts stopped in the newly owned gate before the runner: one
needed the keeper as the process working directory for Vite resolution, and
one incorrectly required the service snapshot's synthetic commit SHA to equal
the keeper commit. Both were corrected; the final service run above is the
only passing preflight result and the only result used for approval.

## Smoke and scope

No producer actual, build, full suite, product run, or source edit was made.
The optional existing list/launch seam was not run: it invokes
`npm run build:hosted`, which is disallowed by this task. The smallest
prerequisite for a permitted smoke is an existing central short-environment
launch/list command that does not invoke that build, or explicit authorization
to use the current build-backed seam.

Live callers, producer body, helper, config, pins, and shared dependencies
were unchanged.
