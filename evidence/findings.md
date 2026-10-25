# D140 independent recipe review

Verdict: `FAIL_SOURCE`.

The author packet is source-only and correctly refuses this venue with a finite
`NOT_READY` census. I did not correct it or run any child, installer, package
acquisition, Store, queue, registry, provider, browser, render, live socket, or
22-root body action.

## Findings

1. **D140-ORDER-001 (blocking): pre-child ordering is wrong.**
   `receive-farm.sh:265-293` requires `CHILD_BOOTSTRAP`, `P4_D73_MANIFEST`,
   `P4_D73_EVIDENCE`, output roots, fresh counters, and `POISON_MANIFEST` in
   the PRE-child census. The challenge ordering permits only preexisting Farm
   inputs there; child registration, child Python, and a new D73 manifest must
   be checked after the stage that produces them.

2. **D140-DURABILITY-002 (blocking): durable core evidence is declarative.**
   `commands.md:77-96` checks JUnit/raw/start-stop/disk/KEEP bindings but the
   core command passes only `P4_D73_EVIDENCE` to the existing launcher. None of
   `JUNIT_ROOT`, `RAW_ROOT`, `STARTSTOP_ROOT`, `DISK_ADMISSION`,
   `RETAINED_ROOT`, or `KEEP_ROOT` is wired into the executed route.

3. **D140-C0-003 (major): the handoff is not an exact C0 wire description.**
   It says `optionalreads` and reply fields `canonical/base/landing`,
   `bindings/effects/dependencies/history/undo_steps`; f103’s schema uses
   step `reads`, `canonical_document`, explicit base/previous/accepted IDs,
   `rebased_onto`, nested records/dependencies, and an outer receipt. Conflict
   head is the details `current` pair. See Runtime f103
   `contract/schemas/timeline-commit.json:310-369,965-1158,1217-1279`.

4. **D140-GATE-004 (major): import-check failure is not an explicit stop.**
   The command invokes the reviewed checker, but neither asserts its exit nor
   gates the next block on mandatory/diagnostic classification. The checker
   returns nonzero for failures, so an operator running the blocks in one shell
   could continue to controls/core after an import failure.

5. **D140-RECEIPT-005 (major): Farm receipt checks are existence-only.**
   `check_readonly_receipt` accepts any regular file and does not authenticate
   tuple, tree, producer, schema, or digest. This cannot establish the required
   final publication receipt.

6. **D140-POISON-006 (major): poison content is not checked before the run.**
   The census checks only that `POISON_MANIFEST` exists. It does not prove that
   it differs from the positive manifest only by forty-zero `agent_sha`.

7. **D140-SCHEMA-007 (major): schema closure paths are detached.**
   Fixed content hashes are checked, but the receiver does not require the
   RECORD/direct_url paths to be the files under the bound installed
   distribution, nor authenticate the trusted manifest by fixed digest.

## Positive observations

The fixed 41ad/f103/569/635f identities and exact source blob hashes were
verified read-only. The command text contains the unchanged 22 unfiltered roots,
uses the existing D73 launcher, preserves the D139a installed-distribution
flags, keeps the canonical 4c/ab1e census historical/supporting-only, and does
not claim actual Farm execution. Agent Main `547e…` and the current Runtime
checkout `0ca…` were not relabelled as the requested exact tuple.

Author custody is limited to committed Git evidence and the permanent author
worker directory. Relative paths printed by the author are not treated as
absolute Farm receipts.
