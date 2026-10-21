# AP2 M2 selected retention/custody one-original review 0911

## Verdict

**HOLD overall.** The new owned 0903 retention/process hunk is approved by
static and offline review, and its prerequisites were available, but the one
authorized central actual was registered with an over-strict service-HEAD
precondition and failed before the owned runner launched. No retry or repair
was submitted.

The service snapshot preserved the required App tree
92391f9a57dd38ce327b0a63990725053ea34601; its HEAD was a synthetic snapshot
commit, so the first registration predicate requiring service
HEAD=a50ca4a0 was wrong. The settled requirement was a matching service tree,
not a matching service commit.

## Source and tool identity

| item | identity |
| --- | --- |
| service/source App | a50ca4a0172cce9c73ce3c040290bf9479098b0f / tree 92391f9a57dd38ce327b0a63990725053ea34601 |
| selected original spec | SHA-256 10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1 |
| selected harness | SHA-256 1585677bafef583110e86a04a4490a968a8db499b0e9d566c6b890eab228ce6c |
| owned 0903 runner | SHA-256 4459f2c9acd7ce411f92beab33c216e549c98fe1fad996706998e6c5aaab85a3 |
| shared helper | SHA-256 96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109 |
| Agent/Runtime source | Agent 6efc81500a0e0688c2bb41e736503f0fc3e04abb, Runtime 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c |
| Runtime graph | manifest a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d, 76 artifacts, schema 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d |
| Composition graph | outer 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30, embedded package 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738, 77 members |

The protected keeper is the exact detached checkout
/home/user/work/wt/app-pin-a50ca4a0, clean at the App HEAD/tree above, with
an empty KEEP. The 0903 durable tool also retained its empty
artifacts/KEEP. No fake Git metadata or replacement worker path was used.

## Review and checks

The runner was reviewed against the immutable 0858/0852/0844 bindings and the
0903 retention report. The owned delta keeps child status 17, retains only
bounded DOM/error-context/trace plus child log, identity and SHA manifest,
labels empty output PREBODY, refuses missing/copy/destination failures,
accepts physical roots, and cleans successful runs. It does not copy
credentials or environment dumps. Existing service-tree, keeper, metadata,
artifact-version, Node/Vite/Vitest/Playwright, argv/list1/zero-test,
short-path, origin and credential guards remain present.

Commands and results:

    sh -n <owned runner>
    PASS

    SELECTED_FINAL95_MODE=preflight <owned runner> <service source checkout>
    PASS: all 11 aggregate checks, including exact one-test list1

    registration guard
    PASS: computed runner hash was 64 lowercase hex; synthetic 62-character
    hash was rejected; stored suite command contained the computed hash once;
    stored command passed bash -n

The central registration was added programmatically to the App suite table
with the computed runner hash. The exact request was:

    request-test ap2-m2-selected-retention-custody-one-original-0911 \
      ap2-m2-selected-retention-custody-one-original-0911-actual --no-cache

## Actual result

Run ID:

    ap2-m2-selected-retention-custody-one-original-0911-ap2-m2-selected-retention-custody-one-original-0911-actual-1021091220-18044

wait-test result: fail exit=1 in 1s, service tree
92391f9a57dd38ce327b0a63990725053ea34601.

Reached: central service snapshot and registration command evaluation.

Unreached: owned runner, source/tool setup, build, Playwright collection and
execution, browser, Runtime handshake, fixture setup, P1/P2 admission, source
removal, refusal/dirty-draft, lost-ACK exact retry, restart/reload recovery,
inverse/undo, and zero-legacy assertion.

First failure: the stored command's first predicate required
git -C "$PWD" rev-parse HEAD = a50ca4a0; the central service's synthetic
snapshot HEAD did not satisfy it. log.txt is zero bytes and no durable 0903
failure packet/manifest was produced because the owned runner was never
invoked. This is not a selected behavior result and no writer cut is claimed.

## Changes and next step

No App product/spec/runner/helper/artifact/source file was changed in this
review worktree. The only orchestration mutation was the one named suite
registration needed for the single attempted service request. The worktree is
clean; keeper and durable leases remain protected.

The next attempt must be separately authorized after correcting only the
registration precondition to accept the matching service tree (while keeping
the exact keeper HEAD/tree, runner hash, selector, budgets, source, graph and
all guards). Do not relabel this failed setup as a behavioral failure or
success, and do not repeat it under this authorization.
