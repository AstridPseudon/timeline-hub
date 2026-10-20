# Retained Linux pidfd exit proof through a bind-time kernel watch

Worker: agt-m2-custody-kernel-capability-proof. Predecessor: `36f8427283ccfa7edfc0b29fb8c3fd5ea79c2966`. Qualified source tree: `ecd26c7c6eeb8c6ad53ead2f68a07ab056c3122c`. This is the bounded custody correction, not approval of the D13 join.

## Decision and capability assumptions

Replace the metadata fingerprint with one private epoll instance per admitted Linux pidfd. Capture membership once during the existing birth-fenced `pidfd_open` registration. Reuse the existing custody lock for capture, proof, and release. `_PidfdExitProof` belongs in the existing process-only helper seam, `process_group.py`; no new module or public API is needed.

The captured descriptor must be the actual result of custody's existing `pidfd_open`, surrounded by its existing identity checks. Arbitrary caller-supplied descriptors never gain proof authority. The private epoll instance and its membership remain exclusively owned by custody; proof only performs MOD and wait, never ADD. This is a trusted same-process lifetime assumption, not protection against arbitrary code mutating private proof objects or epoll membership. Signaling, admission, sessions, adoption, ownership, census checks, and Darwin authority are unchanged.

The kernel key is `(struct file *, descriptor number)`, not inode metadata. In Linux v6.8, `do_epoll_ctl` takes the target file reference with `fdget`, uses `ep_find(ep, tf.file, fd)`, and MOD returns ENOENT if the original registration is missing. `ep_item_poll` polls the registered file. `eventpoll_release_file` removes its entries when the underlying open file description is finally released. See [the kernel implementation](https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/eventpoll.c) and [epoll's documented key/lifetime](https://man7.org/linux/man-pages/man7/epoll.7.html). Epoll does **not** keep the pidfd's open file description alive after final close. Instead the watch disappears, so a subsequently recycled file pointer cannot inherit it.

## Proof and lifetime

1. MOD the original registration to prove that this descriptor still resolves to the registered open file description.
2. Accept only exactly one event for that descriptor, with IN or IN|HUP. Errors, HUP alone, malformed events, and wait errors refuse proof.
3. MOD again to reject substitution during the wait. Events came from the retained kernel registration, not a newly registered numeric descriptor.
4. Conditional release records birth-bound terminal provenance only after this proof. Unconditional release creates no proof. Both release paths close the epoll and pidfd and remove the proof object. Failed epoll capture closes partial state and conservatively disables this exit exception while retaining existing signal custody.

Closing the sole original fd destroys its registration. Keeping a duplicate alive may preserve a stale watch, but MOD on a different file at the original number still fails. A different live or dead pidfd therefore cannot provide the original's proof even when inode/device/mode/link metadata are shared. An intact original pidfd remains valid after its process exits and is reaped; its proof allows the existing PID-reuse cleanup exception while the existing ancestry guards exclude replacements and their children.

No extra pidfd or duplicate is retained. The additional epoll fd is non-inheritable and released with custody. Watch allocation/registration failure and missing watches refuse the reuse exception; there is no metadata fallback. Loss of a descriptor may require explicit unconditional disposal after the caller's existing cleanup policy, and never becomes terminal provenance.

## Scope and limits

Only `custody_broker.py`, `process_group.py`, and their direct process test file change. The Timeline proof helper is extracted into the existing helper seam to satisfy inventory without updating entries or thresholds: broker 4,085 -> 4,060 lines, versus inventory/main 4,031 (+29 <= 50); helper module 817 lines (<1,200). No generic framework or separate helper module.

Host is Linux `6.18.44-fc-v139`. Shared old-kernel metadata are modeled from binding onward; child lifetimes, pidfds, descriptor duplication/substitution, and readiness are real kernel operations. This is not execution on Linux v6.8. PID recycling in census tests is simulated, not forced. No normal production close race or external exploit is claimed. Darwin's 16 existing native tests remain UNRUN here. A separate fresh security review of the harness-committed fix and the actual current D13 join qualification are mandatory before merge. This worker does neither merge nor commit.

See the worker report for commands, results, source hashes, and predecessor counterexample replay. Prior review diagnostics/evidence were read only and remain untouched.
