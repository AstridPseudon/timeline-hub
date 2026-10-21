# AP2 M2 producer run-mode delta review — 0524

## Decision

**HOLD.** There is no reviewable closed-repair candidate. The required new
durable gate artifact, final 64-hex digest, uniquely named registrations,
offline actual-dispatch proof, and closed-repair final report are absent.
Therefore I cannot approve an actual command or claim Gate 5/6 evidence.

The smallest remaining defect is outside App source: worker
`ap2-m2-producer-run-mode-closed-repair-0524` produced no candidate artifact
or report. Its worktree is still clean at the frozen base and contains no
source or suite-registration delta.

## Confirmed frozen chain and failure

- Frozen keeper: `/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453`
- Frozen HEAD/tree: `17d2518c341c47a2d8634047b400399886da3a2a` /
  `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- Immutable 0501 gate (untouched):
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh`
- Immutable gate SHA-256: `460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7`
- Frozen wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`

The central result
`ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793`
is a recorded invocation failure, exit 2, with zero collection/body tests.
Its exact command reached the unchanged gate after both existing 64-hex hash
guards and invoked:

```text
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh run
```

The gate accepts only `preflight|list` and returned its usage line before
changing directory to the keeper or invoking the wrapper. The wrapper itself
supports `list|run|preflight`; the defect is the outer gate whitelist only.

## Candidate and evidence status

- Closed-repair report: absent at the required path when reviewed.
- New gate artifact: absent; no final digest exists.
- New preflight/actual suite registrations: absent; current producer entries
  still point at the immutable 0501 gate or earlier unrelated gates.
- Offline dispatch proof: not run because there is no new gate to traverse.
- New central source-only preflight: not run because there is no new command.
- Actual, browser, build, full suite, install, and product/source edits: none.
- Live callers, producer body/helper/config, pins, protected root, captured
  tree, and shared dependencies: unchanged.

## Checks performed

```text
sh -n <immutable 0501 gate>                         PASS
sh -n scripts/testing/run-producer-public13-list.sh PASS
git -C <frozen keeper> diff --check                 PASS
git -C <frozen keeper> status --short --branch      clean
```

The previously recorded `6793` result was inspected rather than rerun; it is
preserved as an invocation failure and is not product evidence.

## Required next step

Create one owned durable copy of the immutable gate changing only its mode
whitelist to admit `run`, hash that whole artifact, register preflight and
actual commands with the new gate digest before invocation plus the unchanged
wrapper digest, then complete the required real-gate offline dispatch proof
and one central preflight. This review must be repeated before any actual is
submitted.
