# Runtime OPS-retire-venv guard diagnosis — handoff

## PASS / bounded disposition

The five completed-name `partial or active builder exists` refusals in the
2026-10-23T16:58Z peer result are source-backed false positives. In
`make-child-venv`, the in-flight destination is `D.partial.RUN_ID`; after all
validation, `mv -T "$T" "$D"` publishes the completed child. The source archive
`SRC=$(mktemp -d "$W/.child-venv-source-$N-$RUN_ID.XXXXXX")` is intentionally
retained and is not moved or removed after publish. Therefore a completed
target plus a retained `.child-venv-source-N-*` is immutable source custody,
not proof of an active builder.

The smallest correction is a one-line pattern narrowing in the staged
`retire-child-venv`: `check_builder_artifacts` continues to refuse every
`$N.partial.*` sibling, but no longer refuses retained
`.child-venv-source-$N-*`. No other guard or caller changes.

The two other refusals remain correct: a missing-marker partial cannot be
classified as safe, and an unreadable process executable is fail-closed. No
permission, marker, process, daemon, retry, or deletion action was performed.

## Exact seven cases

False positive on retained source custody: `venv-agent-child-ap2-current-583-9ce-1503`,
`venv-agent-child-ap2-current-583-cfa-1451`,
`venv-agent-child-ap2-current-8c-cfa-1415`,
`venv-agent-child-ap2-p1-f611-1343`, and
`venv-agent-child-ap2-p2-8c355-1356`.

Correct refusal: `venv-agent-child-ap2-p1-5b1-1253.partial.20261023T125224Z-30409`
(`owned child marker is unavailable`) and
`venv-agent-child-ap2-p1-f611-1320.partial.20261023T132158Z-17576`
(`process executable is unreadable`). No inference that either is safe to
delete.

## Packet identity

The private staged packet is under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-guard-diagnosis-1704/evidence/kit/`

Installed packet preserved exactly:

```text
f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15  dispatcher-daemon
4713b456ae4b0dcabdbc64ddf41aff731ac10fe4d11695d315e6743b864aef10  request-retire-venv
48cac6c70578b9435a259da7cb9adbd07bf045a3346d77235a401ca848e02ed5  installed retire-child-venv
```

Staged packet:

```text
a5beb33d046665ef26533a574870ba00f24681387442b1109794bf1c9556f835  staged retire-child-venv
4713b456ae4b0dcabdbc64ddf41aff731ac10fe4d11695d315e6743b864aef10  staged request-retire-venv
f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15  staged dispatcher-daemon
```

The flat scoped patch is alongside this handoff as
`handoff-runtime-OPS-retire-guard-1704.patch`. It contains one changed line
in `retire-child-venv`.

## Qualification commands

All commands used private fixture roots; none exercised production removal.

```text
bash -n evidence/kit/request-retire-venv evidence/kit/dispatcher-daemon evidence/kit/retire-child-venv fixtures/independent-review.sh fixtures/dispatcher-boundary-test.sh  # exit 0
fixtures/independent-review.sh  # exit 0; 37 pass / 0 fail
python3 -m unittest -v fixtures/test_retire_guard.py  # exit 0; 7 tests OK
fixtures/dispatcher-boundary-test.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-guard-diagnosis-1704/evidence/kit  # exit 0; 3/3
git -C /home/user/work/wt/rt-OPS-retire-guard-diagnosis-1704 diff --check  # exit 0; no worktree delta
```

The 37-case matrix retains the prior 36 route/security controls and adds the
completed-custody positive. It still covers partial, marker, reference, age,
live process, replacement-race, immutable/symlink, unreadable-input, FIFO,
and caller-shape controls. A synthetic unreadable `/proc` entry and an
adversarial final delete swap were not fault-injected; those branches were
source-inspected and the real unreadable-process case remains refused.

Independent review and HOST atomic installation are separate. If the staged
correction is approved, the host owner must re-review this exact hash, verify
the dispatcher is idle/not executing the target script, create the timestamped
predecessor backup, and perform the normal `.new`/atomic `mv` installation.
This worker did not install it, invoke the daemon, or propose an alternate
deletion route.
