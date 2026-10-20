# Retained pidfd kernel-watch review

**APPROVE the bounded custody correction** at commit `19e4abb2a8083ee331f96cc33b0b4891cc89f1f0`, tree `ecd26c7c6eeb8c6ad53ead2f68a07ab056c3122c`, on `tl/agt-m2-custody-kernel-capability-proof`. The two prior descriptor-proof counterexamples are closed under the documented custody-exclusive observer lifetime. No blocking finding remains in that scope. **macOS UNRUN; actual current D13 join still required.** This does not approve a D13 composition, dependency/version change, merge, or public release.

Read PLAN first, the 16:16 owner grant, both previous HOLD reports and their probe files, and the committed product/test delta. Used a fresh private `git archive` of the exact committed SHA, not the source worker's checkout or edited oracle. Reviewer checkout remains unchanged at `c73b1ab12d5d044fc181bba4343e8b47668d9674` (tree `ddb30a85cd4a38803ae8b8be27ef7974cf6fdf99`). No product or repository test edits were made.

## Why this proof closes the gap

At Linux registration, the descriptor is the result of the existing birth-fenced `os.pidfd_open`, revalidated before storing it. `_PidfdExitProof` captures a private epoll registration there. It never reconstructs membership from descriptor metadata. Proof performs MOD, nonblocking wait, and MOD again, accepting exactly one event for the bound descriptor with IN or IN|HUP. Missing membership, lost observers, errors and other events refuse. No ADD occurs during proof or release.

This checks the actual registered file object. Linux v6.8's `do_epoll_ctl` resolves the current target file and looks up `(file pointer, fd number)`; MOD returns ENOENT when that pair is absent. Readiness is polled from the registered file, and final file release removes its entries. Thus final close cannot leave a registration that a recycled file pointer inherits. A duplicate can keep the old registration alive, but MOD at the substituted descriptor still refuses. These facts are visible in the [Linux v6.8 epoll implementation](https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/eventpoll.c); release ordering is in [file_table.c](https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/file_table.c) and [eventpoll.h](https://raw.githubusercontent.com/torvalds/linux/v6.8/include/linux/eventpoll.h).

On the original pidfd, IN is positive process-exit notification rather than generic file readability: the older backend's `pidfd_poll` reports it only after thread-group exit. See [Linux v6.8 fork.c](https://raw.githubusercontent.com/torvalds/linux/v6.8/kernel/fork.c). Unlike the predecessor fingerprint, this proof does not depend on distinct pidfd inode numbers.

Conditional release records the admitted birth only after successful proof, closes both watch and pidfd, and removes the proof object. Unconditional release does not create terminal provenance. The released sentinel proves exit only with the matching terminal birth. Missing proof maps and arbitrary fake-custody descriptors cannot certify exit.

**Trust boundary:** the private epoll instance, its descriptor lifetime, and its one-time membership must stay exclusively owned by custody. The product creates it once, never extends its membership, and serializes registration/proof/release under the custody lock. This is not protection against arbitrary same-process code replacing a private observer with a separately populated epoll instance, inserting foreign registrations, or rewriting the proof/ledger. Merely closing the observer, losing its registration, or recycling its descriptor to an empty epoll/ordinary file refuses in the independent probes. Approval preserves this explicit design assumption; it does not claim authentication of an arbitrarily replaced observer.

## Independent diagnostics

New `workers/agt-review-custody-epoll-final/probe_epoll.py` imports only the committed product. It does not import either previous probe or the implementation worker's oracle. Final run: **exit 0, 36 scenarios plus an unchanged parent-FD baseline** on Linux `6.18.44-fc-v139`.

- Twenty combinations: intact live original, closed descriptor, ordinary-file substitution, other live pidfd and other dead/reaped pidfd; each with/without an original duplicate, under native and modeled shared metadata. The dead substitute really returns IN|HUP while the original remains alive. All refuse proof, conditional release and synthetic changed-birth census; wrong birth/missing entry refuse too.
- Lost observer controls: closed Python object, raw descriptor close, unregister, unregister/close during wait, allocation failure, registration failure with partial-state cleanup. None grants proof or terminal provenance, even after the original subsequently exits.
- An original ready watch kept alive by a duplicate cannot prove exit through a substituted descriptor, either before or during wait.
- Removing/closing the watch after a genuine positive event refuses at the post-wait MOD. Recycling its fd to an empty epoll or ordinary file also refuses.
- Genuine original zombie and reaped exit prove exit; conditional release preserves a certificate for exactly its birth. Unconditional live release does not certify exit.
- A genuinely exited, admitted descendant permits the intended synthetic PID-reuse cleanup exception. Its replacement and replacement's child are excluded from adoption. Final parent cleanup removes all watches. All probe children are killed/reaped and the parent descriptor set returns to baseline.

Shared-inode behavior is modeled only through fstat's device/inode/mode fields from binding onward; readlink, children, pidfds, dup2, epoll and exit readiness remain real. This is **not execution on an older Linux kernel**, and census PID recycling is simulated rather than forced. No external exploit or normal production close race was established. One draft diagnostic compared entire stat records, including unrelated timestamps; it was corrected to compare the predecessor's actual identity fields. This was a diagnostic assertion failure, not a product-test failure.

## Original tests, scope and inventory

The complete correction over `f511038d^` changes exactly the three owner-allowed files, +360/-6. The final successor commit itself is +244/-36. All 50 original top-level process-test definitions and all 213 original custody-test definitions, including decorators and assertions, are source-identical against both `f511038d^` and `origin/main` (`96b283d5d6fd8031538f881e486bb2ebf45dce75`). The entire custody test file is byte-identical. No skip/xfail, lost behavior, original expectation, or lane rule changed.

Existing custody signal/authority, admission identity predicates, Darwin session/group handling, and census methods remain intact. Only the existing constructor, Linux registration bookkeeping and release method change inside `ProcessCustody`, with new private proof methods. The process-group exception requires positive original-Popen reap or exact retained exit proof; replacement identities remain excluded from traversal. Unproven reuse and sticky uncertainty still refuse.

`custody_broker.py` is 4,060 physical newlines versus main/inventory 4,031: **+29 <= 50**. `process_group.py` is 817 (<1,200). The rationale entry, inventory test (1,200/50), and lane file are unchanged. The existing one-line Main infrastructure note is present in `design/agent-main-infrastructure-touched.md`.

Reviewed SHA-256 values:

| Path | SHA-256 |
| --- | --- |
| `astrid/core/execution/custody_broker.py` | `9675a9ba92a7d2a14c440f91d13ba2886b48e328d3cc3917538465cc526e4cf2` |
| `astrid/core/execution/process_group.py` | `1234b73f61ee47de14f9006fdd0bf7c8b958da16e9d54ea15ac7fdbe0d4321d2` |
| `tests/core/execution/test_process_group.py` | `c43f3a8be25b68aa729b2c4ff12e83d6a96774d4a6970e7e99d1b9fc0844f43e` |
| `tests/core/execution/test_custody_broker.py` | `ea6b9b779d6c4f857e55da4138cda267d1afdb00f1a7cf989b0149023a753c91` |

## Exact commands and results

Use `O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`, `W=$O/workers/agt-review-custody-epoll-final`, `S=$W/source`. The temporary source archive was removed after review; recreate it from the Agent repository with:

```sh
mkdir -p "$S"
git archive 19e4abb2a8083ee331f96cc33b0b4891cc89f1f0 | tar -x -C "$S"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/probe_epoll.py"
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$W/audit_source.py"
```

Both final commands **exit 0**. Logs: `$W/probe-epoll.log`, `$W/audit-source.log`. Audit checks archive/blob equality, scope, original definitions, unchanged inventory/lane files, changed-method scope, and exact central tree/count/exit.

From `$S`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/core/execution/test_process_group.py::test_observation_uncertainty_persists_without_adopting_unknown_children \
  tests/core/execution/test_process_group.py::test_reaped_root_pid_reuse_does_not_poison_final_tree_observation \
  tests/core/execution/test_process_group.py::test_final_verification_uncertainty_cannot_be_cleared_by_a_later_census \
  tests/core/execution/test_process_group.py::test_terminal_member_birth_mismatch_cannot_be_filtered_away \
  tests/core/execution/test_custody_broker.py::test_unknown_or_reused_target_never_signals \
  tests/core/execution/test_custody_broker.py::test_refresh_failure_never_signals_or_adopts_replacement \
  tests/core/execution/test_custody_broker.py::test_observed_census_does_not_change_linux_pidfd_admission \
  tests/core/execution/test_custody_broker.py::test_linux_descendant_pid_reused_before_registration_is_absent \
  tests/core/execution/test_custody_broker.py::test_linux_descendant_exiting_during_pidfd_bind_is_absent \
  tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale
```

**19 passed in 2.06s**, exit 0, no skips. Log: `$W/targeted.log`. `git diff --check f511038d^ 19e4abb2`: exit 0.

Reused existing central result `agt-m2-custody-kernel-capability-proof-root-prep-current-integration-1020170702-5873`: its `snap` records **exactly the reviewed committed tree**, exit file is 0, summary/log agree: **652 passed, 16 skipped in 27.61s**, zero deselected. Its command, under the service's recorded clean `root-prep-current-integration` environment, was:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py
```

No new central request or full suite was run. The 16 Darwin-native skips remain **macOS UNRUN**, not passes. Shared dependencies were read-only; bytecode/cache generation was disabled and logs/probes stayed in the assigned worker directory.

No blocking dependency remains for this review task. Recommended next step: orchestrator/source owner qualify the actual current D13 join with this exact custody correction and retain the platform/trust-boundary caveats. No claim about that join is made here.
