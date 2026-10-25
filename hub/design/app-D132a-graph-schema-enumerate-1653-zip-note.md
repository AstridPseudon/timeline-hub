# ZIP note

Worker-authored source note: this change migrates the enumerated authored setup value at `root_values()[0].value.payload.metadata` from explicit `null` to `{}` because the frozen `PreparedCommit` schema requires an object at that slot. Open-object content nulls remain unchanged. This note makes no ZIP, build, packaging, or delivery claim.
