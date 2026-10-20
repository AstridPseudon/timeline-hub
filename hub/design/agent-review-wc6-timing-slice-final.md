# Agent WC6 timing/narration slice review

**Decision: APPROVE bounded private qualification; HOLD merge/release.**

Reviewed candidate:

- Commit `5962d5791be0463700e04d5dd526eb5554c83fda`
- Tree `9dd8f59f0468e42b1fa3074271067a3fbea7c67`
- Parent/current014 consumer `a4c1307734d620cee81640cab6b25f7b198f0c17`
- Parent tree `49b77c93b181ec1b20f0230a6cdbfa1518ad55ab`

The successor is minimal: two changed files only. `document_diff_to_commands`
now captures and stages same-alias `occurrence.swap-media` before the clip timing
loop. The media command is captured from the exact base and executed into the
working bundle; every next timing command is then captured from the staged bundle.
The source-level guards remain intact: exact authenticated media selection,
original registry binding, all affected consumers, old/new media dependencies,
clip baseline/shape checks, and final explicit-row/payload comparisons. The
authenticated inverse and scalar media-reference machinery is outside the diff,
and the tree has no `own_materialized_read` exemption.

The updated real-body test asserts ordered media→move→set commands, timing edits,
source-window/narration/metadata/opaque/order/mirror preservation, reload, lost-ACK
undo after restart, disjoint rebase, redo, and strict intervening A→B→A refusal.
The inherited a0 Runtime HTTP proof is the live evidence; the fresh bounded local
lane passed **90 tests** with **166 deselected**. No full suite or live-socket rerun
was performed.

The older `publish_authoring_candidate` positives are WC1/WC2 authoring-candidate
behavior and remain unchanged. They must not be described as deleted by this WC6
document-view change. Narration, arbitrary structural rows, and whole-document
fallback publication remain held; the broader SDK legacy timing/narration writers
also remain open.

No generated pin/client/schema files changed. Merge remains conditional on the
later current3c4/private014 join and App gate. Do not mark the entire WC6 row
`DELETED` based on this bounded proof.
