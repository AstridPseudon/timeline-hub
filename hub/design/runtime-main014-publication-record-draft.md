# Main014 Runtime publication-record draft

**DRAFT ONLY — do not mark PUBLISHED, do not replace `runtime-current-tuple.md`, and do not move a consumer pin from this document.**

This is the exact record to complete only after the Runtime manager writes the
literal gate `ORDINARY014 ADOPTION AUTHORIZED` and the authorized merge into
Runtime integration succeeds. The existing public tuple remains 0.2.13 until
then.

## Proposed publication record

```text
PUBLISHED — <UTC timestamp after the successful merge> — Runtime manager

Main014 coordinated Runtime adoption is authorized by the Runtime manager's
recorded `ORDINARY014 ADOPTION AUTHORIZED` decision and the actual merge result
below. The prior public Runtime 0.2.13 tuple remains historical; this record
does not relabel any candidate or staging source.

Runtime candidate/source: 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3
Runtime candidate tree:  d3a290b407fa61e6ab2d476f50c068073f70df00
Actual integration merge: <required post-authorization commit SHA>
Actual integration tree:  <required post-authorization tree SHA>

Agent consumer: 6efc81500a0e0688c2bb41e736503f0fc3e04abb
Agent consumer tree: 2ed2b8a12b5b3391ca221ba6ff05390f71a73556
App normal pin source: 10fa2ff9a8216604aa39e3584f89dc9e7a09080a
App normal pin tree:   01fd2a04ff0c383ec5281043c7e5a4c843d1d835
App actual current bootstrap successor: <required exact App source SHA/tree and proof record>

Runtime package/client: 0.2.14
Runtime schema digest: sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
Raw Agent command schema: sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
Command shape: 55 definitions / 29 operations
Artifact version: sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac

Authorization record: <shared Runtime-manager record containing the literal gate>
Merge record: <successful actual merge result and post-merge identity>
Agent qualification: <exact 6efc source/result record>
App qualification: <exact 10fa/current-bootstrap-successor source/result record>
```

The candidate identities above are immutable and must remain distinct: Runtime
`95bd3c5`, Agent `6efc815`, and App `10fa2ff9` (plus the later exact current
bootstrap successor). The App normal pin is not proof of the actual bootstrap
journey, and the older ordinary014 `a0dca169`/`f021` tuple is not a substitute.

## Preconditions still open

1. Runtime manager records `ORDINARY014 ADOPTION AUTHORIZED`.
2. The authorized Runtime merge succeeds; record its actual commit and tree,
   then re-check the merged tree before updating the current tuple.
3. App HOME returns the exact current bootstrap successor and the real
   same-cohort create/init/restart/lost-response/raw-default proof against
   Agent `6efc815` and Runtime `95bd3c5`.
4. Only after 1–3 are complete may the Runtime manager replace the current
   tuple record and separately perform the authorized consumer adoption.

No source, schema, generated client, artifact, lock, pin, or integration file
was changed by preparing this draft.
