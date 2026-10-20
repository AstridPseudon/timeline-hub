# Retained-pidfd successor: independent security review

**HOLD** on `36f8427283ccfa7edfc0b29fb8c3fd5ea79c2966`, tree `001877d1cd14c716c3fca18606413f01aab44c49`. The old closed-fd, ordinary-fd and unconditional-release counterexamples are fixed on this Linux 6.18 host. The new fingerprint does not identify a process capability on Linux kernels using the singleton anonymous inode for pidfds. A fresh diagnostic reproduces false exit proof under those kernel metadata semantics, including false conditional-release provenance. Owner 16:16 condition (1) therefore remains unmet without a further correction or an explicit, enforced platform qualification.

No production close race or external exploit was established. This is the same bounded descriptor-fault review condition as the previous HOLD; no new security escalation is requested. This review is complete, rather than blocked awaiting implementation.

## Exact source and existing qualification

Read PLAN, the 16:16 owner grant in Agent INBOX, the prior review requirements/report, and the committed product/tests. The actual branch is `tl/agt-m2-custody-retained-capability-fix`; the concatenated `fix36f84272` in the brief identifies its head, not another ref. Reviewed an unmodified private `git archive` of that exact commit, independently of either worker checkout. Reviewer worktree HEAD stayed `79b33f8a1e69b27fd53f3cd5230301b84d0d4ef1`, clean.

The successor is exactly two files, **+88/-7**, over `f511038ded7a0ae49e2935efc37800b63038d0b3`. Together with that predecessor it is exactly the allowed three files, **+151/-5**, over `f511038d^`. No D13, rendering, Composition dependency or 0.0.14 pin changes are included. This review cannot clear a wholesale D13/014 merge or release; the real current D13 join remains a separate qualification.

SHA-256 of reviewed blobs:

| Path | SHA-256 |
| --- | --- |
| `astrid/core/execution/custody_broker.py` | `f8f9bc3e4028571df3e0d70489a7fcb5bc3487a7262b18c878346d7ee7137bb7` |
| `astrid/core/execution/process_group.py` | `df8d111c415b2700d1421a1a592bce38267b939395945adbf7600412db8d1cb1` |
| `tests/core/execution/test_process_group.py` | `1065454547f4a6b9f9a04c4c6d4804640dc9bf13362136525971b466a7cc350c` |
| `tests/core/execution/test_custody_broker.py` | `ea6b9b779d6c4f857e55da4138cda267d1afdb00f1a7cf989b0149023a753c91` |

Verified central result `agt-m2-custody-retained-capability-fix-root-prep-current-integration-1020164410-30585`: `snap` records **exactly the reviewed tree**, `exit` is 0, summary and log agree on **629 passed, 16 skipped in 58.42s**, zero deselected. The command was:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py
```

The service used its recorded clean `root-prep-current-integration` environment, including `PYTHONPATH="$PWD"` and `PYTHONDONTWRITEBYTECODE=1`. No new central or full-suite request was made. The 16 skipped Darwin-native cases were not executed on macOS; full macOS tests are **UNRUN**. The existing result cannot establish that every platform's strict tests passed.

The process-test delta only adds three definitions (the predecessor regression and two successor tests). AST/source-segment comparison against both `f511038d^` and `origin/main` (`96b283d5d6fd8031538f881e486bb2ebf45dce75`) found zero changed/removed original definitions: 50 process and 213 custody definitions. The custody test file is byte-identical. No original assertions, skip/xfail policy or expectations changed.

## Remaining proof gap

At `custody_broker.py:3905–3930`, the stored identity consists solely of `(st_dev, st_ino, st_mode, readlink)`. Polling is now correctly restricted to exactly one `POLLIN` or `POLLIN|POLLHUP` event, with the fingerprint checked before and after. However, those checks only identify the same capability if the metadata distinguish process objects.

Linux v6.8's [`__pidfd_prepare()`](https://raw.githubusercontent.com/torvalds/linux/v6.8/kernel/fork.c) constructs pidfds with `anon_inode_getfile("[pidfd]", ...)`. Its [`anon_inode_getfile()` implementation](https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/anon_inodes.c) reuses one inode. Consequently different processes' pidfds have the same device, inode, mode and link text. The newer [v6.12 pidfs implementation](https://raw.githubusercontent.com/torvalds/linux/v6.12/fs/pidfs.c) instead supplies process inode numbers, while keeping the same link text. The modern host's successful substitution negative does not establish portability to the older implementation. No corresponding kernel/backend qualification is enforced by the reviewed bind/proof paths; admission checks pidfd syscall availability.

Fresh diagnostic: `workers/agt-review-custody-capability-successor/probe_successor.py`, output in `probe-successor.log`. It was authored from the original requirements and inspected APIs; it does not import or copy the code worker's modified reviewer oracle. The legacy case changes **only fstat's pidfd metadata** to the common tuple produced by the older backend, from bind onward. `pidfd_open`, child lifetimes, `/proc/self/fd` readlink, `dup2` substitution and `poll` remain real kernel operations. It does not overwrite the product's handle ledger, fingerprint map, proof method or terminal-provenance map.

Reproduction: bind a live original child; retain another child's pidfd; kill/reap that other child; replace the original descriptor number with the other pidfd. The diagnostic prints:

```text
original_alive=True
real_poll=[(3, 17)]                 # POLLIN|POLLHUP, genuinely from the OTHER child
false_exit=True
changed_census_refused=False
released=True
persisted_false_exit=True
```

Both fingerprint checks match the shared metadata. Conditional release at lines 3883–3887 then stamps the original birth as terminal and closes the substituted descriptor. The sentinel thereafter preserves the false proof. The changed birth census is synthetic; no real PID recycling was forced. This is a deterministic kernel-semantics model on Linux 6.18, **not an actual Linux 6.8 execution**. The source above establishes why its shared metadata premise is valid.

## Passing controls and retained guards

The same fresh diagnostic's real Linux 6.18 controls all passed: live original; closed fd; `/dev/null`; substituted live and exited other-process pidfds; wrong birth/missing entry; conditional-release refusal; and changed-census refusal for each intact negative. Injected `POLLNVAL`, `POLLERR`, HUP alone, mixed error bits, wrong-fd/duplicate/empty events, poll exceptions and substitution during polling also refused. A live unconditional release did not certify exit. Genuine zombie and reaped-original exit did prove exit, and conditional release preserved that proof for only the bound birth.

Registration, observation, proof and release share the same reentrant lock; no internal production close race was found. Registration rejects changed births and clears old terminal provenance on initial binding. Unconditional release cannot mint new terminal provenance. Signal authority/implementation, sessions/groups, admission ownership, sticky uncertainty and final absence checks remain unchanged. Reaped-root exception and ancestry birth guards still exclude replacements. No numeric-PID/group kill fallback or new adoption path was added. These safeguards do not make a shared inode an exact capability identity.

## Commands, inventory and next step

Let `O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`, `W=$O/workers/agt-review-custody-capability-successor`, `S=$W/source`. Recreate `$S` from `git archive 36f8427283ccfa7edfc0b29fb8c3fd5ea79c2966` in the Agent repository. The review's temporary archive is removed after use.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/probe_successor.py"
```

Exit 0: eight passing host control groups plus the asserted counterexample above. Diagnostic exit 0 means the reproduction matched its assertions, **not** that the security condition passed. An initial draft had a nonexistent snapshot-helper name; correcting the diagnostic to the inspected `_process_snapshot` API yielded the recorded run. Product source was unchanged.

From `$S`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/execution/test_process_group.py -k 'observation_uncertainty_persists or reaped_root_pid_reuse or retained_pidfd_exit_proof'
```

**7 passed, 62 deselected in 0.42s**, exit 0. `git diff f511038d^ 36f84272 --check`: exit 0.

Main inventory note: `custody_broker.py` has **4,085 physical newlines**, versus **4,031** in main and its retained rationale entry: **+54**, four beyond the permitted 50-line drift. Report this to the source owner for the normal cohesive extraction or justified inventory update under PLAN. Do not loosen the 1200/50 thresholds. No inventory edit or broad structure-suite claim is made here.

Recommended next step: correct exact capability validation, conservatively refusing the reuse exception wherever that identity cannot be proven, and add a different-pidfd/shared-inode negative. Re-review the minimal committed correction. Then qualify the actual current D13 join separately. No product edits, original-test changes, shared-dependency writes, commit/merge/checkout, push or release were performed.
