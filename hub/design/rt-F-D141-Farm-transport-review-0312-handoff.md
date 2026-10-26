# D141i transport review handoff

Status: **PASS_TRANSPORT_SECURITY_REVIEW / FARM_NOT_READY**.

Frozen target: commit `25ddf3fec4631c0e689d91dae358e68bd045309b`, tree
`e43261f85b5044f1cb90b647fc26f8fac01ae728`.

Immutable inputs:

- Archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz`, SHA-256 `c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f`, 13285 bytes, mode 0644, uid/gid 0/0, nlink 1.
- Helper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-transport-verifier-729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528.py`, SHA-256 `729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528`, 26956 bytes, mode 0644, uid/gid 0/0, nlink 1.
- Trusted source identity: ArtAgents `242f9c4306bf3b501222cb041a9eb246ef47bc85`, `packages/timeline-schema/python`, source tree `75a5a697f630affee40632e500b3f5b704a9b834`; manifest SHA `c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d`.
- Closure: RECORD SHA `844b2a2e…`, 1593 bytes, mode 0644, 18 rows / 12 hashed / six named unhashed; direct_url SHA `b7a0a4f9…`, 254 bytes, mode 0644.

Real receiving sequence, still gated and not run:

1. Obtain helper SHA and archive SHA separately from the existing trusted
   manager peer. Verify the helper bytes, bind `ARCHIVE`, `VERIFIER`, and
   `MANAGER_PEER_SHA256`, then run the external-SHA verifier command recorded
   in `validation.md`.
2. On `PASS_TRANSPORT_CLOSURE` and independent review PASS only, create a new
   private empty physical `STAGE` mode 0700 with no concurrent writers; clear
   `TAR_OPTIONS`; use fixed `/usr/bin/tar` with `--no-same-owner`,
   `--same-permissions`, and `--keep-old-files`.
3. Recheck extracted regular files, single links, bytes, modes, allowed
   receiving ownership, and exact closure. Bind the extracted distribution,
   trusted manifest, RECORD, and direct_url to the existing D139a receiver
   variables.
4. Only after genuine D139a/Farm bindings exist, run unchanged
   `D140_PHASE=pre-child ops-d140-farm/receive-farm.sh --check-only`.
   Transport PASS alone must never infer Farm READY.

C0v2 remains unchanged, including base revision/publication pair, commands,
label, steps with patches/reads, merge/read semantics, dry-run/idempotency,
and accepted/merged/conflict/invalid/preview replies. The current kit summary
plus separate matching `PASS_INSTALL` pair and original67 wheelhouse remain
missing; no substitution or bootstrap extraction is authorized.
