# Handoff: ap2-P2-popup-native-fixture-1219

**Disposition: BLOCKED at the public native seam; no App file changed.**

The only retired writer in `preparePopupSeed` is still the
`composition-revisions` POST. Replacing it faithfully requires adding a
second occurrence that shares the seed's exact physical shot/revision/internal
closure. Current Agent public source refuses that operation through
`emit_document_commands`/`doc.patch`; `occurrence.create` makes a fresh child,
`occurrence.duplicate` makes an isolated copied child, and `occurrence.fork`
only rehomes an existing occurrence. Therefore I did not encode a clone,
manually synthesize authority, or retain a misleading partial migration.

Smallest owner need: provide or qualify a public semantic carrier for a second
occurrence retaining the source physical child identity. After that seam lands,
the named test can replace only the setup block and preserve all existing
gesture and proof assertions.

Evidence and exact command results are in the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-popup-native-fixture-1219/report.md`
