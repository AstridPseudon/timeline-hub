# Runtime handoff: G5/R2r independent authentic archive review

## Verdict

**PASS.** Independent current-reader restore and fidelity review completed.

Qualified archive:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/evidence/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz`

SHA-256:

`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`

## Qualified reader tuple

- Current Runtime reader: worktree
  `/home/user/work/wt/rt-G5-authentic-review-1640`.
- Commit/tree before and after restore:
  `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` /
  `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`.
- Module origin before and after:
  `/home/user/work/wt/rt-G5-authentic-review-1640/runtime_protocol/service.py`.
- Restored head: revision
  `a3e671256f1c42b8837d3e118c97b21b`, publication/receipt
  `txn-11c90075be6c4c8bb9e2627366f0fe4f`.
- Predecessor: `film-parent-v1`, receipt
  `txn-55c0651b2cd64255ae06e73f9708220a`.
- Parent digest:
  `sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`.

## Review closure

The fresh restore passed current `verify_backup`, `restore_backup`, and
`verify_baseline`. Archive members were safety-inspected before extraction.
The authenticated manifest matched the retained manifest. The restored
canonical document matched the expectation and retained capture readback,
including the two music clips, legacy word app/null/opaque/absence semantics,
registry, occurrences, physical shared media identity, and dependency
manifest. All three shots, all three internal timelines, and all five required
CAS/media bodies matched their expected hashes and sizes. Read-only SQL checks
confirmed the predecessor chain, publication event, idempotency receipt, and
event witness.

The retained authoring adapter checks establish old public Runtime source
`0ba9622a3e98a85577ef893be85988ba7f203b88` / tree
`c0bbd76656ac21439d11bf928eb970d60fe6e690`, normal head CAS, UUID revision,
and public `RuntimeService.publish_parent_composition`; no direct SQL/CAS or
history fabrication path and no literal `m1-journey-baseline` were found.

Durable evidence:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/evidence/g5-sdk-authentic-review-1640-current-reader.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/evidence/g5-sdk-authentic-review-1640-manifest.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/evidence/g5-sdk-authentic-review-1640-sourcechecks.json`

No key material was retained in review outputs. No archive was overwritten.

## Consumer boundary

This qualifies fixture fidelity only. It does not run or credit Agent's
original FOUR bodies, and it makes no schema/client/frozen34e change. The
manager may now run the unchanged original FOUR once source-ready, against the
qualified restored head/publication tuple, through the ordinary v2 caller with
the existing request/reply, dry-run, and HTTP idempotency contract.

## Evidence limits

Targeted fixture tests and adapter compilation passed. No full/browser/native
suite was run, per task scope. The four-body behavior and consumer invocation
remain unverified until that manager-controlled run.
