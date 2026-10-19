# Runtime coordination — shot-root schema refresh

This handoff is held until the PLAN M1 gate is recorded. It is explicitly after
the label-only `0.2.2` release sourced from Agent `86bfe1860cd2b4fe661bde88051ed4b690b94ce1`;
it must not be bundled with or used to replace that release.

## Next canonical Agent source

- Source path: `astrid/core/timeline/schema/edit-command.schema.json`
- Source SHA-256: `a92aaadf2d98f37e304769c8e5f779274aafafab83e81e83ed6bd40752d3b47a`
- Source branch: `tl/agt-m2-root-schema-slice` (harness commit is pending)
- Change: the four `shot:S` reference-pattern admissions in `ScopedId`,
  `EntityRef`, `TargetKey`, and `AnchorIdentity`.

The Runtime owner should refresh its normal schema/artifact bundle from this
exact source after the label-only release. No DTO, ABI, endpoint, generated
client, producer, or handler change is part of this handoff.

## Qualification boundary

Draft 2020-12 validation covers the sealed `a0dad5fc` migration command's wire
envelope, shot-root select/binding/created facts, empty-root `TargetKey` paths,
malformed empty/slashed/ambiguous root IDs, and the original M1 envelopes.
The migration operation remains intentionally unknown to this branch's registry;
this proves schema admission only, not registered-handler or Runtime acceptance.
