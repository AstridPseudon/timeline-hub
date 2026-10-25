# OPS staging review — FAIL

Candidate: commit `017bd30c33f88c2e4bed8fb03e910ee1cde6f7db`, tree
`7f9ce60cc681937681d96cc88b90da7ff3f92e33` on composition `tl/integration`.

## Findings

### OPS-STAGING-001 — high — protected ACTIVE/LEASE path components are removable

`preflight` checks only `KEEP` on target ancestors (lines 429–433), and its
marker scan starts below the target root (`target.rglob("*")`, lines 434–437).
Therefore a target such as `parent/ACTIVE/staging` or
`parent/LEASE/staging` is accepted and removed. A private forced-fallback CLI
control reproduced this for `ACTIVE`, `active`, `LEASE`, and `lease`. A target
whose own basename is one of these markers is also not covered by the
descendant scan. This violates the settled no-lease/active-marker and protected
ancestor/descendant requirements.

### OPS-STAGING-002 — critical — worker replacement TOCTOU can delete the wrong record

`execute` opens `preflight_result.worker` by pathname (line 649), but never
compares that directory's device/inode with the worker observed in preflight.
The subsequent target, archive, log, and quarantine paths are partly pathname
based. A private direct control preflighted valid `workers/w`, renamed it to
`original-w`, installed a different valid worker at `w`, and called
`execute(preflight)`. The candidate returned `packed`, removed the replacement
`w/staging`, and left `original-w/staging` untouched. The worker must be bound
to a stable directory descriptor/identity across preflight and action, with
all subsequent archive/log/listing operations rooted in that descriptor.

### OPS-STAGING-003 — high — lstat/hash race follows a substituted symlink

`_safe_walk` lstat-checks a file and then calls `_sha256_file(path)` by
pathname (lines 223–235). `_verify_evidence` repeats the same pattern for
manifest rows and reads the manifest after a separate regular-file check
(lines 287–291 and 337–350). A private control replaced the checked regular
staging file with a symlink immediately at that boundary; `_safe_walk`
returned the SHA-256 of bytes outside the staging tree and reported no reason.
The archive and evidence checks therefore are not resistant to symlink
substitution during traversal. Hashing must use an already-open descriptor or
an `O_NOFOLLOW`/descriptor-relative operation, and the same rule must apply to
manifest reads and archive source traversal.

### OPS-STAGING-004 — high — symlinked manager lease roots are ignored

`_active_lease_reasons` returns no reasons when `managers` or a manager/notes
directory is a symlink (lines 188–199). A private CLI control made
`ORCH/managers` a symlink to an external tree containing a matching
`runtime.lease`; the candidate packed and removed the target. Unsafe lease
path components must cause refusal, not suppress the lease check, and lease
inspection must be anchored to the validated orchestration root.

## Positive/negative review notes

The author’s eight actual-CLI cases pass, including archive-first packing,
forced low-disk fallback, archive collision, lifecycle/manifest failures,
manager lease in the direct non-symlink layout, traversal/outside paths,
symlink target/descendant, and KEEP protection. Additional private controls
confirmed the failures above. Hardlinked staging files did not cause deletion
of the linked evidence inode in the exercised archive path; however, the
listing does not record link identity, so hardlink semantics remain dependent
on the race checks being repaired.

No source edits were made by this review.
