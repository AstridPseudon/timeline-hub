# R2 baseline review 1429

**Verdict: PASS for the narrow historical-child-baseline source repair at
`80523b472cc817c2da01bf89c177d5d7dc4c2e10`.**

`_RestoredShot` is a native-only carrier. It is attached only for an inverse
child whose exact payload and internal timeline, complete occurrence-owner set,
and same-scope verified canonical source match an accepted historical closure.
`_verify_document` authenticates revision digests, closure links, owners,
media pins/manifests, and identities. Current base scope is rechecked, foreign
or malformed history refuses, and no root, pin, source mapping, or authored
field is guessed/replaced. JSON round-tripping the carrier removes its native
authority and the unchanged competing-media guard refuses. Captured mutations
cover missing/extra owner, payload, internal timeline, source digest, and
foreign scope, all refusing without mutation.

Immutable evidence packet:
`agent-R2-redo-media-1404-a29df82beb548306.json`, 1,481,631 bytes,
SHA-256 `a29df82beb548306683ab64d738eb776a519587fdb30cad3e997e91468621ef8`;
Agent base `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`; Runtime
`cfa0af0d476e6954df041c08d7ef378fd6782932`. Its source hashes match this
tree, guard/inverse/doc-patch/vendor/artifact files are unchanged, and public
module origins match final files. Preview, forward, whole undo, and exact undo
retry accepted. The one redo reached Runtime but was refused before write as
`invalid_records: inverse stage write differs from its sequential input`.
Database, document, head, and history before/after are identical.

That retained refusal is an **Agent inverse source/effect-orientation owner**,
not a Runtime defect. The prepared native write for
`occurrence:f2-occurrence/[shot_id]` has before=`shot-placement-*`, while the
Runtime-authenticated sequential canonical input has the physical
`document-diff-...-shot`; after=`selected-shot` agrees with the authored redo.
The next Agent function is the inverse-stage native/effect correspondence in
`astrid/sdk/timeline/inverse.py` and its `_commit_patch.py` binding boundary.
Runtime must continue rejecting this mismatch until that source record is
repaired.

This review does not claim public redo, whole-redo, or G5 completion.
